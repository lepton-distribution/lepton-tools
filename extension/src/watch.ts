// Observateurs de fichiers (ENV-12 lot 3) :
// - F2 (FIC-1) : créations et suppressions dans scion/ des clones greffés → `lepton graft --path …`,
//   événements regroupés ;
// - F3 (FIC-3) : fichier régulier créé dans le trunk → `lepton file owner --json`, puis
//   `lepton file add --adopt` (déplacé dans le clone propriétaire, lien à sa place) ;
// - L3-4 (lot 5) : lien greffé supprimé du trunk par l'utilisateur (`file owner` : `unlinked`) →
//   « Supprimer du greffon » (`file remove`) ou « Restaurer le lien » (`graft --path`).
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
const UNLINK_DELAY_MS = 500;
const LEPTON_QUIET_MS = 3000;     // suppressions venues d'un lepton en cours ou tout juste fini : ignorées
const UNLINK_MAX = 20;            // au-delà : suppression en masse (scion, git), pas une action de l'explorateur

export class Watchers implements vscode.Disposable {
  private watchers: vscode.Disposable[] = [];
  private signature = "";
  private readonly grafts: Batcher<string>;
  private readonly adoptions: Batcher<string>;
  private readonly unlinks: Batcher<string>;
  private readonly subscriptions: vscode.Disposable[] = [];
  private readonly grafted = new vscode.EventEmitter<void>();
  /** Émis après une regreffe automatique (F2) ou une adoption (F3) : le trunk a changé. */
  readonly onDidChangeTrunk = this.grafted.event;

  constructor(private readonly runner: LeptonRunner, private readonly commands: Commands) {
    this.grafts = new Batcher(
      () => Math.max(100, this.config().get<number>("autoGraft.delay", 1000)),
      (paths) => this.graft(paths));
    this.adoptions = new Batcher(() => ADOPT_DELAY_MS, async (paths) => {
      for (const p of paths) {
        await this.adopt(p);
      }
    });
    this.unlinks = new Batcher(() => UNLINK_DELAY_MS, (paths) => this.unlinked(paths));
    this.subscriptions.push(
      this.grafted,
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
    this.unlinks.dispose();
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
    const askUnlink = this.config().get<boolean>("confirmTrunkDeletions", true);
    if (!autoGraft && !redirect && !askUnlink) {
      this.clear();
      return;
    }
    const result = await this.runner.exec(["seed", "status", "--json"]);
    const status = result && parseJson<StatusResult>(result);
    if (!status?.trunk || !Array.isArray(status.scions)) {
      return;                         // pas de rootstock ici : rien à observer
    }
    const stems = autoGraft ? status.scions.map((s) => s.stem).filter((s) => s).sort() : [];
    const trunk = redirect || askUnlink ? status.trunk : "";
    const signature = JSON.stringify([trunk, stems, redirect, askUnlink]);
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
        new vscode.RelativePattern(vscode.Uri.file(trunk), "**"), !redirect, true, !askUnlink);
      w.onDidCreate((u) => this.adoptions.add(u.fsPath));
      w.onDidDelete((u) => {
        if (!this.runner.recentlyBusy(LEPTON_QUIET_MS)) {
          this.unlinks.add(u.fsPath);
        }
      });
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
      this.grafted.fire();
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
      this.grafted.fire();
      vscode.window.setStatusBarMessage(t("lepton: {0} moved to its scion", name), 5000);
    } else if (adopted) {
      vscode.window.showWarningMessage(t("lepton: {0} left in the trunk — {1}", name, lastMessage(adopted)));
    }
  }

  // ------------------------------------------------------------------ L3-4

  /** Liens supprimés du trunk alors que le fichier reste dans le clone : il reviendrait à la regreffe
   *  suivante ; l'utilisateur choisit de le retirer du greffon ou de restaurer le lien. */
  private async unlinked(paths: string[]): Promise<void> {
    if (paths.length > UNLINK_MAX) {
      this.runner.output.appendLine(t("{0} deletions in the trunk: not examined (bulk deletion)", paths.length) + "\n");
      return;
    }
    const found: OwnerResult[] = [];
    for (const p of paths) {
      const result = await this.runner.exec(["file", "owner", p, "--json"]);
      const owner = result && parseJson<OwnerResult>(result);
      if (owner?.kind === "unlinked" && owner.owner) {
        found.push(owner);
      }
    }
    if (!found.length) {
      return;
    }
    const remove = t("Remove from the scion");
    const restore = t("Restore the link");
    const message = found.length === 1
      ? t("{0} was deleted from the trunk only: the scion {1} still has it, and the next regraft brings it back.",
        path.basename(found[0].trunk_path), found[0].owner!.name)
      : t("{0} files were deleted from the trunk only: their scions still have them, and the next regraft brings them back.",
        found.length);
    const answer = await vscode.window.showWarningMessage(message, remove, restore);
    if (answer === remove) {
      for (const o of found) {
        await this.runner.run(t("remove {0}", path.basename(o.trunk_path)), ["file", "remove", o.trunk_path]);
      }
    } else if (answer === restore) {
      await this.runner.run(t("restore {0} link(s)", found.length),
        ["graft", ...found.flatMap((o) => ["--path", o.trunk_path])], { quiet: true });
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
