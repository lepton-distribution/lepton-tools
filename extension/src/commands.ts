// Commandes de palette (F1, IDE-6) : chaque commande recueille ses arguments puis appelle lepton ;
// lepton décide et refuse, l'extension affiche (ENV-12 : aucune logique de graine ni de greffon).
import * as path from "node:path";
import * as vscode from "vscode";
import {
  EXIT_INTERRUPT,
  EXIT_OK,
  EXIT_USER,
  LeptonResult,
  lastMessage,
  resolveLepton,
  runLepton,
} from "./lepton";

const SHOW_OUTPUT = "Afficher la sortie";

interface ScionEntry {
  name: string;
  role: string;
}

export class Commands {
  constructor(private readonly output: vscode.OutputChannel) {}

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
      ["lepton.graft", () => this.run("regreffer", ["graft"])],
      ["lepton.check", () => this.run("vérifier", ["check"], { show: true })],
      ["lepton.generate", () => this.run("générer", ["generate"])],
    ];
    for (const [id, fn] of table) {
      context.subscriptions.push(vscode.commands.registerCommand(id, fn));
    }
  }

  // ------------------------------------------------------------------ appel de lepton

  /** Répertoire de travail : celui de l'espace généré (rootstock), sinon le premier dossier ouvert. */
  private cwd(): string | undefined {
    const ws = vscode.workspace.workspaceFile;
    if (ws?.scheme === "file") {
      return path.dirname(ws.fsPath);
    }
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
  }

  async run(title: string, args: string[], opts: { show?: boolean; quiet?: boolean } = {}):
    Promise<LeptonResult | undefined> {
    const cwd = this.cwd();
    if (!cwd) {
      vscode.window.showErrorMessage("Lepton : aucun dossier ouvert (ouvrir l'espace généré par lepton generate).");
      return undefined;
    }
    const exe = resolveLepton(vscode.workspace.getConfiguration("lepton").get<string>("path", ""));
    this.output.appendLine(`$ ${exe} ${args.join(" ")}    (${cwd})`);
    if (opts.show) {
      this.output.show(true);
    }
    const result = await vscode.window.withProgress(
      { location: vscode.ProgressLocation.Notification, title: `lepton : ${title}`, cancellable: true },
      (_progress, token) => {
        const abort = new AbortController();
        token.onCancellationRequested(() => abort.abort());
        return runLepton(exe, args, cwd, (t) => this.output.append(t), abort.signal);
      },
    );
    this.output.appendLine(`→ code ${result.code}\n`);
    this.report(title, result, opts.quiet ?? false);
    return result;
  }

  private async report(title: string, result: LeptonResult, quiet: boolean): Promise<void> {
    let choice: string | undefined;
    if (result.code === EXIT_OK) {
      if (!quiet) {
        vscode.window.showInformationMessage(`lepton : ${title} — terminé`);
      }
      return;
    } else if (result.code === EXIT_INTERRUPT) {
      choice = await vscode.window.showWarningMessage(`lepton : ${title} — interrompu`, SHOW_OUTPUT);
    } else if (result.code === EXIT_USER) {
      choice = await vscode.window.showWarningMessage(`lepton : ${title} — ${lastMessage(result) || "refus"}`,
        SHOW_OUTPUT);
    } else {
      choice = await vscode.window.showErrorMessage(
        `lepton : ${title} — échec (code ${result.code}) ${lastMessage(result)}`, SHOW_OUTPUT);
    }
    if (choice === SHOW_OUTPUT) {
      this.output.show();
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

  /** Greffons du rootstock d'après `lepton seed status --json`, présentés tels quels. */
  private async pickScion(placeHolder: string): Promise<string | undefined> {
    const result = await this.run("état de la graine", ["seed", "status", "--json"], { quiet: true });
    if (result?.code !== EXIT_OK) {
      return undefined;
    }
    let scions: ScionEntry[];
    try {
      scions = JSON.parse(result.stdout).scions;
    } catch {
      vscode.window.showErrorMessage("lepton seed status --json : sortie illisible");
      return undefined;
    }
    const chosen = await vscode.window.showQuickPick(
      scions.map((s) => ({ label: s.name, description: s.role })),
      { placeHolder, ignoreFocusOut: true },
    );
    return chosen?.label;
  }

  /** `--version V` et `--path P` facultatifs (seed add, seed replace). */
  private async originOptions(): Promise<string[] | undefined> {
    const version = await this.ask("Version (branche ou tag d'une URL) — vide : défaut de lepton", "master", true);
    if (version === undefined) {
      return undefined;
    }
    const sub = await this.ask("Chemin du greffon dans le dépôt — vide : aucun", undefined, true);
    if (sub === undefined) {
      return undefined;
    }
    return [...(version ? ["--version", version] : []), ...(sub ? ["--path", sub] : [])];
  }

  // ------------------------------------------------------------------ graine (GRA)

  private async seedStatus(): Promise<void> {
    await this.run("état de la graine", ["seed", "status"], { show: true, quiet: true });
  }

  private async seedAdd(): Promise<void> {
    const scion = await this.ask("Nom du greffon (champ nom de son manifeste)");
    if (!scion) return;
    const location = await this.ask("Origine : URL git[@VERSION][:PATH] ou répertoire local");
    if (!location) return;
    const type = await this.pick(["famille", "bsp", "application", "bibliotheque"], "Type du greffon");
    if (!type) return;
    const options = await this.originOptions();
    if (!options) return;
    await this.run(`ajouter ${scion}`, ["seed", "add", scion, location, "--type", type, ...options]);
  }

  private async seedRemove(): Promise<void> {
    const scion = await this.pickScion("Greffon à retirer de la graine");
    if (!scion) return;
    const mode = await this.pick(["conserver le clone", "supprimer aussi le clone (--purge)"], "Clone du greffon");
    if (!mode) return;
    const purge = mode.includes("--purge");
    if (!(await this.confirm(`Retirer ${scion} de la graine${purge ? " et supprimer son clone" : ""} ?`, "Retirer"))) {
      return;
    }
    await this.run(`retirer ${scion}`, ["seed", "remove", scion, ...(purge ? ["--purge"] : [])]);
  }

  private async seedReplace(): Promise<void> {
    const scion = await this.pickScion("Greffon dont l'origine change");
    if (!scion) return;
    const location = await this.ask("Nouvelle origine : URL git[@VERSION][:PATH] ou répertoire local");
    if (!location) return;
    const options = await this.originOptions();
    if (!options) return;
    await this.run(`remplacer ${scion}`, ["seed", "replace", scion, location, ...options]);
  }

  private async seedLock(): Promise<void> {
    const modes: Record<string, string[]> = {
      "figer (lepton-graine.lock.json)": [],
      "vérifier les clones contre le verrou (--verify)": ["--verify"],
      "restaurer les clones au verrou (--restore)": ["--restore"],
    };
    const mode = await this.pick(Object.keys(modes), "Verrou de la graine");
    if (!mode) return;
    if (modes[mode].includes("--restore") &&
        !(await this.confirm("Remettre les clones d'origine distante au commit du verrou, puis regreffer ?",
          "Restaurer"))) {
      return;
    }
    await this.run("verrou de la graine", ["seed", "lock", ...modes[mode]], { show: true });
  }

  // ------------------------------------------------------------------ greffons (GRF)

  private async scionNew(): Promise<void> {
    const name = await this.ask("Nom du nouveau greffon");
    if (!name) return;
    const type = await this.pick(["application", "bibliotheque", "bsp"], "Type du greffon");
    if (!type) return;
    const args = ["scion", "new", name, "--type", type];
    if (type === "bsp") {
      const from = await this.pickScion("BSP greffé à copier (--from)");
      if (!from) return;
      args.push("--from", from);
    }
    await this.run(`créer ${name}`, args);
  }

  private async scionRemove(): Promise<void> {
    const scion = await this.pickScion("Greffon à retirer (dépôt conservé)");
    if (!scion) return;
    if (!(await this.confirm(`Retirer le greffon ${scion} (son dépôt est conservé) ?`, "Retirer"))) return;
    await this.run(`retirer ${scion}`, ["scion", "remove", scion]);
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

  private async pathAdd(kind: "file" | "dir", uri?: vscode.Uri): Promise<void> {
    const what = kind === "file" ? "fichier" : "répertoire";
    let full: string | undefined;
    if (uri?.scheme === "file") {
      const name = await this.ask(`Nouveau ${what} dans ${uri.fsPath}`);
      if (!name) return;
      full = path.join(uri.fsPath, name);
    } else {
      full = await this.ask(`Chemin du nouveau ${what} (trunk ou clone)`);
    }
    if (!full) return;
    let result = await this.run(`créer ${path.basename(full)}`, [kind, "add", full]);
    // lepton propose « --scion NAME » quand le propriétaire n'est pas déterminé (files._new_path_owner)
    if (result?.code === EXIT_USER && lastMessage(result).includes("--scion") &&
        (await vscode.window.showInformationMessage("Désigner le greffon propriétaire (--scion) ?",
          "Choisir le greffon")) === "Choisir le greffon") {
      const scion = await this.pickScion(`Greffon propriétaire de ${path.basename(full)}`);
      if (!scion) return;
      result = await this.run(`créer ${path.basename(full)}`, [kind, "add", full, "--scion", scion]);
    }
    if (result?.code === EXIT_OK && kind === "file") {
      await vscode.window.showTextDocument(vscode.Uri.file(full));
    }
  }

  private async pathRemove(kind: "file" | "dir", uri?: vscode.Uri): Promise<void> {
    const what = kind === "file" ? "fichier" : "répertoire";
    const target = await this.target(uri, `Chemin du ${what} à retirer (trunk ou clone)`);
    if (!target) return;
    if (!(await this.confirm(`Retirer ${target} de son greffon ?`, "Retirer"))) return;
    await this.run(`retirer ${path.basename(target)}`, [kind, "remove", target]);
  }

  private async fileMove(uri?: vscode.Uri): Promise<void> {
    const source = await this.target(uri, "Fichier à déplacer (trunk ou clone)");
    if (!source) return;
    const destination = await vscode.window.showInputBox({
      prompt: "Destination (trunk ou clone)", value: source, ignoreFocusOut: true,
      valueSelection: [source.length - path.basename(source).length, source.length],
    });
    if (!destination || destination === source) return;
    const result = await this.run(`déplacer ${path.basename(source)}`, ["file", "mv", source, destination]);
    if (result?.code === EXIT_OK) {
      await vscode.window.showTextDocument(vscode.Uri.file(destination));
    }
  }
}
