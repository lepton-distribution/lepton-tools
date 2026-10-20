// Commandes de palette (F1, IDE-6) : chaque commande recueille ses arguments puis appelle lepton ;
// lepton décide et refuse, l'extension affiche (ENV-12 : aucune logique de graine ni de greffon).
import * as path from "node:path";
import * as vscode from "vscode";
import { EXIT_OK, OwnerResult, ScionRef, StatusResult, parseJson } from "./lepton";
import { LeptonRunner } from "./runner";

const t = (message: string, ...args: (string | number)[]) => vscode.l10n.t(message, ...args);

export class Commands {
  constructor(private readonly runner: LeptonRunner) {}

  register(context: vscode.ExtensionContext): void {
    const table: [string, (...a: any[]) => unknown][] = [
      ["lepton.seedStatus", () => this.seedStatus()],
      ["lepton.seedAdd", () => this.seedAdd()],
      ["lepton.seedRemove", () => this.seedRemove()],
      ["lepton.seedReplace", () => this.seedReplace()],
      ["lepton.seedLock", () => this.seedLock()],
      ["lepton.scionNew", () => this.scionNew()],
      ["lepton.scionRemove", () => this.scionRemove()],
      ["lepton.fileAdd", (uri?: vscode.Uri) => this.pathAdd("file", uri)],
      ["lepton.dirAdd", (uri?: vscode.Uri) => this.pathAdd("dir", uri)],
      ["lepton.fileRemove", (uri?: vscode.Uri) => this.pathRemove("file", uri)],
      ["lepton.dirRemove", (uri?: vscode.Uri) => this.pathRemove("dir", uri)],
      ["lepton.fileMove", (uri?: vscode.Uri) => this.fileMove(uri)],
      ["lepton.graft", () => this.runner.run(t("regraft"), ["graft"])],
      ["lepton.check", () => this.runner.run(t("check"), ["check"], { show: true })],
      ["lepton.generate", () => this.runner.run(t("generate"), ["generate"])],
    ];
    for (const [id, fn] of table) {
      context.subscriptions.push(vscode.commands.registerCommand(id, fn));
    }
  }

  // ------------------------------------------------------------------ saisies

  private async ask(prompt: string, placeHolder?: string, optional = false): Promise<string | undefined> {
    const value = await vscode.window.showInputBox({ prompt, placeHolder, ignoreFocusOut: true });
    if (value === undefined || (!optional && !value.trim())) {
      return undefined;
    }
    return value.trim();
  }

  private async pick(items: string[], placeHolder: string): Promise<string | undefined> {
    return vscode.window.showQuickPick(items, { placeHolder, ignoreFocusOut: true });
  }

  private async confirm(message: string, action: string): Promise<boolean> {
    return (await vscode.window.showWarningMessage(message, { modal: true }, action)) === action;
  }

  /** Greffons du rootstock d'après `lepton seed status --json`, présentés tels quels ;
   *  `among` : restreint aux greffons nommés (candidats donnés par lepton). */
  async pickScion(placeHolder: string, among?: ScionRef[]): Promise<string | undefined> {
    let items: { label: string; description?: string }[];
    if (among) {
      items = among.map((s) => ({ label: s.name, description: s.key }));
    } else {
      const result = await this.runner.exec(["seed", "status", "--json"]);
      const status = result && parseJson<StatusResult>(result);
      if (!status?.scions) {
        vscode.window.showErrorMessage(t("lepton seed status --json: unreadable output"));
        return undefined;
      }
      items = status.scions.map((s) => ({ label: s.name, description: s.role }));
    }
    const chosen = await vscode.window.showQuickPick(items, { placeHolder, ignoreFocusOut: true });
    return chosen?.label;
  }

  /** `--version V` et `--path P` facultatifs (seed add, seed replace). */
  private async originOptions(): Promise<string[] | undefined> {
    const version = await this.ask(t("Version (branch or tag of a URL) — empty: lepton's default"), "master", true);
    if (version === undefined) {
      return undefined;
    }
    const sub = await this.ask(t("Path of the scion in the repository — empty: none"), undefined, true);
    if (sub === undefined) {
      return undefined;
    }
    return [...(version ? ["--version", version] : []), ...(sub ? ["--path", sub] : [])];
  }

  // ------------------------------------------------------------------ graine (GRA)

  private async seedStatus(): Promise<void> {
    await this.runner.run(t("seed status"), ["seed", "status"], { show: true, quiet: true });
  }

  private async seedAdd(): Promise<void> {
    const scion = await this.ask(t("Scion name (name field of its manifest)"));
    if (!scion) return;
    const location = await this.ask(t("Origin: git URL[@VERSION][:PATH] or local directory"));
    if (!location) return;
    const type = await this.pick(["famille", "bsp", "application", "bibliotheque"], t("Scion type"));
    if (!type) return;
    const options = await this.originOptions();
    if (!options) return;
    await this.runner.run(t("add {0}", scion), ["seed", "add", scion, location, "--type", type, ...options]);
  }

  private async seedRemove(): Promise<void> {
    const scion = await this.pickScion(t("Scion to remove from the seed"));
    if (!scion) return;
    const keep = t("keep the clone");
    const purge = t("also delete the clone (--purge)");
    const mode = await this.pick([keep, purge], t("Clone of the scion"));
    if (!mode) return;
    const message = mode === purge
      ? t("Remove {0} from the seed and delete its clone?", scion)
      : t("Remove {0} from the seed?", scion);
    if (!(await this.confirm(message, t("Remove")))) return;
    await this.runner.run(t("remove {0}", scion), ["seed", "remove", scion, ...(mode === purge ? ["--purge"] : [])]);
  }

  private async seedReplace(): Promise<void> {
    const scion = await this.pickScion(t("Scion whose origin changes"));
    if (!scion) return;
    const location = await this.ask(t("New origin: git URL[@VERSION][:PATH] or local directory"));
    if (!location) return;
    const options = await this.originOptions();
    if (!options) return;
    await this.runner.run(t("replace {0}", scion), ["seed", "replace", scion, location, ...options]);
  }

  private async seedLock(): Promise<void> {
    const modes: [string, string[]][] = [
      [t("lock (lepton-graine.lock.json)"), []],
      [t("verify the clones against the lock (--verify)"), ["--verify"]],
      [t("restore the clones to the lock (--restore)"), ["--restore"]],
    ];
    const mode = await this.pick(modes.map((m) => m[0]), t("Seed lock"));
    const args = modes.find((m) => m[0] === mode)?.[1];
    if (!args) return;
    if (args.includes("--restore") &&
        !(await this.confirm(t("Reset the clones of remote origin to the locked commit, then regraft?"),
          t("Restore")))) {
      return;
    }
    await this.runner.run(t("seed lock"), ["seed", "lock", ...args], { show: true });
  }

  // ------------------------------------------------------------------ greffons (GRF)

  private async scionNew(): Promise<void> {
    const name = await this.ask(t("Name of the new scion"));
    if (!name) return;
    const type = await this.pick(["application", "bibliotheque", "bsp"], t("Scion type"));
    if (!type) return;
    const args = ["scion", "new", name, "--type", type];
    if (type === "bsp") {
      const from = await this.pickScion(t("Grafted BSP to copy (--from)"));
      if (!from) return;
      args.push("--from", from);
    }
    await this.runner.run(t("create {0}", name), args);
  }

  private async scionRemove(): Promise<void> {
    const scion = await this.pickScion(t("Scion to remove (repository kept)"));
    if (!scion) return;
    if (!(await this.confirm(t("Remove the scion {0} (its repository is kept)?", scion), t("Remove")))) return;
    await this.runner.run(t("remove {0}", scion), ["scion", "remove", scion]);
  }

  // ------------------------------------------------------------------ fichiers (FIC)

  /** Chemin désigné dans l'explorateur, sinon fichier actif, sinon saisie. */
  private async target(uri: vscode.Uri | undefined, prompt: string): Promise<string | undefined> {
    if (uri?.scheme === "file") {
      return uri.fsPath;
    }
    const active = vscode.window.activeTextEditor?.document.uri;
    return this.ask(prompt, active?.scheme === "file" ? active.fsPath : undefined);
  }

  /** `--scion NAME` d'après `lepton file owner --json` : [] si lepton détermine le propriétaire (ou
   *  laisse lepton refuser), le choix de l'utilisateur sinon ; undefined si abandon. */
  async ownerOption(full: string): Promise<string[] | undefined> {
    const result = await this.runner.exec(["file", "owner", full, "--json"]);
    const owner = result && parseJson<OwnerResult>(result);
    if (!owner || owner.status === "owned") {
      return [];
    }
    const name = path.basename(full);
    const scion = owner.status === "ambiguous"
      ? await this.pickScion(t("Several scions own this directory: owner of {0}", name), owner.candidates)
      : await this.pickScion(t("No scion owns this directory: owner of {0}", name));
    return scion ? ["--scion", scion] : undefined;
  }

  private async pathAdd(kind: "file" | "dir", uri?: vscode.Uri): Promise<void> {
    let full: string | undefined;
    if (uri?.scheme === "file") {
      const name = await this.ask(kind === "file"
        ? t("New file in {0}", uri.fsPath) : t("New directory in {0}", uri.fsPath));
      if (!name) return;
      full = path.join(uri.fsPath, name);
    } else {
      full = await this.ask(kind === "file"
        ? t("Path of the new file (trunk or clone)") : t("Path of the new directory (trunk or clone)"));
    }
    if (!full) return;
    const scion = await this.ownerOption(full);
    if (!scion) return;
    const result = await this.runner.run(t("create {0}", path.basename(full)), [kind, "add", full, ...scion]);
    if (result?.code === EXIT_OK && kind === "file") {
      await vscode.window.showTextDocument(vscode.Uri.file(full));
    }
  }

  private async pathRemove(kind: "file" | "dir", uri?: vscode.Uri): Promise<void> {
    const target = await this.target(uri, kind === "file"
      ? t("Path of the file to remove (trunk or clone)") : t("Path of the directory to remove (trunk or clone)"));
    if (!target) return;
    if (!(await this.confirm(t("Remove {0} from its scion?", target), t("Remove")))) return;
    await this.runner.run(t("remove {0}", path.basename(target)), [kind, "remove", target]);
  }

  private async fileMove(uri?: vscode.Uri): Promise<void> {
    const source = await this.target(uri, t("File to move (trunk or clone)"));
    if (!source) return;
    const destination = await vscode.window.showInputBox({
      prompt: t("Destination (trunk or clone)"), value: source, ignoreFocusOut: true,
      valueSelection: [source.length - path.basename(source).length, source.length],
    });
    if (!destination || destination === source) return;
    const result = await this.runner.run(t("move {0}", path.basename(source)), ["file", "mv", source, destination]);
    if (result?.code === EXIT_OK) {
      await vscode.window.showTextDocument(vscode.Uri.file(destination));
    }
  }
}
