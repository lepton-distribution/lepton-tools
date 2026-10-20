// Observateurs de fichiers (ENV-12 lot 3) :
// - F2 (FIC-1) : créations et suppressions dans scion/ des clones greffés → `lepton graft --path …`,
//   événements regroupés ;
// - F3 (FIC-3) : fichier régulier créé dans le trunk → `lepton file owner --json`, puis
//   `lepton file add --adopt` (déplacé dans le clone propriétaire, lien à sa place).
// Les répertoires observés et le propriétaire viennent de lepton ; aucune règle de greffon ici.
import { promises as fs } from "node:fs";
import * as path from "node:path";
import * as vscode from "vscode";
import { Batcher } from "./batch";
import { Commands } from "./commands";
import { EXIT_OK, OwnerResult, StatusResult, lastMessage, parseJson } from "./lepton";
import { LeptonRunner } from "./runner";

const t = (message: string, ...args: (string | number)[]) => vscode.l10n.t(message, ...args);
const ADOPT_DELAY_MS = 300;

export class Watchers implements vscode.Disposable {
  private watchers: vscode.Disposable[] = [];
  private signature = "";
  private readonly grafts: Batcher<string>;
  private readonly adoptions: Batcher<string>;
  private readonly subscriptions: vscode.Disposable[] = [];

  constructor(private readonly runner: LeptonRunner, private readonly commands: Commands) {
    this.grafts = new Batcher(
      () => Math.max(100, this.config().get<number>("autoGraft.delay", 1000)),
      (paths) => this.graft(paths));
    this.adoptions = new Batcher(() => ADOPT_DELAY_MS, async (paths) => {
      for (const p of paths) {
        await this.adopt(p);
      }
    });
    this.subscriptions.push(
      runner.onDidRunCommand(() => void this.refresh()),
      vscode.workspace.onDidChangeConfiguration((e) => {
        if (e.affectsConfiguration("lepton")) {
          void this.refresh(true);
        }
      }),
    );
  }

  private config(): vscode.WorkspaceConfiguration {
    return vscode.workspace.getConfiguration("lepton");
  }

  dispose(): void {
    this.clear();
    this.grafts.dispose();
    this.adoptions.dispose();
    this.subscriptions.forEach((d) => d.dispose());
  }

  private clear(): void {
    this.watchers.forEach((w) => w.dispose());
    this.watchers = [];
    this.signature = "";
  }

  /** Répertoires observés d'après `lepton seed status --json` (trunk, `stem` de chaque greffon). */
  async refresh(force = false): Promise<void> {
    const autoGraft = this.config().get<boolean>("autoGraft.enabled", true);
    const redirect = this.config().get<boolean>("redirectTrunkCreations", true);
    if (!autoGraft && !redirect) {
      this.clear();
      return;
    }
    const result = await this.runner.exec(["seed", "status", "--json"]);
    const status = result && parseJson<StatusResult>(result);
    if (!status?.trunk || !Array.isArray(status.scions)) {
      return;                         // pas de rootstock ici : rien à observer
    }
    const stems = autoGraft ? status.scions.map((s) => s.stem).filter((s) => s).sort() : [];
    const trunk = redirect ? status.trunk : "";
    const signature = JSON.stringify([trunk, stems]);
    if (!force && signature === this.signature) {
      return;
    }
    this.clear();
    this.signature = signature;
    for (const stem of stems) {
      const w = vscode.workspace.createFileSystemWatcher(
        new vscode.RelativePattern(vscode.Uri.file(stem), "**"), false, true, false);
      w.onDidCreate((u) => this.grafts.add(u.fsPath));
      w.onDidDelete((u) => this.grafts.add(u.fsPath));
      this.watchers.push(w);
    }
    if (trunk) {
      const w = vscode.workspace.createFileSystemWatcher(
        new vscode.RelativePattern(vscode.Uri.file(trunk), "**"), false, true, true);
      w.onDidCreate((u) => this.adoptions.add(u.fsPath));
      this.watchers.push(w);
    }
    this.runner.output.appendLine(t("Watching {0} scion(s){1}", stems.length,
      trunk ? t(" and the trunk {0}", trunk) : "") + "\n");
  }

  // ------------------------------------------------------------------ F2

  private async graft(paths: string[]): Promise<void> {
    const result = await this.runner.exec(["graft", ...paths.flatMap((p) => ["--path", p])]);
    if (!result) {
      return;
    }
    if (result.code === EXIT_OK) {
      vscode.window.setStatusBarMessage(t("lepton: regrafted ({0} change(s))", paths.length), 5000);
    } else {
      void this.runner.report(t("automatic regraft"), result, true);
    }
  }

  // ------------------------------------------------------------------ F3

  private async adopt(full: string): Promise<void> {
    try {
      if (!(await fs.lstat(full)).isFile()) {
        return;                       // lien posé par la regreffe, répertoire (légitime, E6)
      }
    } catch {
      return;                         // déjà déplacé ou supprimé
    }
    const result = await this.runner.exec(["file", "owner", full, "--json"]);
    const owner = result && parseJson<OwnerResult>(result);
    if (!owner || owner.kind !== "regular") {
      return;                         // liste de scion, fichier système, ou hors rootstock
    }
    const name = path.basename(full);
    let scion: string[] = [];
    if (owner.status === "ambiguous") {
      const chosen = await this.commands.pickScion(
        t("{0} created in the trunk: several scions own this directory, choose its owner", name),
        owner.candidates);
      if (!chosen) {
        return this.leftInTrunk(full);
      }
      scion = ["--scion", chosen];
    } else if (owner.status === "none") {
      const choose = t("Choose the scion");
      const remove = t("Delete from the trunk");
      const answer = await vscode.window.showWarningMessage(
        t("{0} created in the trunk: no scion owns this directory.", name), choose, remove);
      if (answer === remove) {
        await vscode.workspace.fs.delete(vscode.Uri.file(full), { useTrash: true });
        return;
      }
      const chosen = answer === choose ? await this.commands.pickScion(t("Owner of {0}", name)) : undefined;
      if (!chosen) {
        return this.leftInTrunk(full);
      }
      scion = ["--scion", chosen];
    }
    const adopted = await this.runner.exec(["file", "add", full, "--adopt", ...scion]);
    if (adopted?.code === EXIT_OK) {
      vscode.window.setStatusBarMessage(t("lepton: {0} moved to its scion", name), 5000);
    } else if (adopted) {
      vscode.window.showWarningMessage(t("lepton: {0} left in the trunk — {1}", name, lastMessage(adopted)));
    }
  }

  /** Erreur persistante, suppression proposée : VSCodium 1.135 ne garde affichée qu'une notification
   *  d'erreur munie d'un bouton (`sticky`) ; lepton check signale aussi ce fichier en erreur. */
  private async leftInTrunk(full: string): Promise<void> {
    const remove = t("Delete from the trunk");
    const answer = await vscode.window.showErrorMessage(
      t("{0} stays a regular file of the trunk: regrafting is blocked until it is moved or deleted (reported by lepton check).", path.basename(full)), remove);
    if (answer === remove) {
      await vscode.workspace.fs.delete(vscode.Uri.file(full), { useTrash: true });
    }
  }
}
