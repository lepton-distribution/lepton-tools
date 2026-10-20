// F4 (O10, R1) : relance de clangd quand la base compile_commands.json qu'il lit apparaît ou change
// de contenu (premier preset configuré après l'ouverture, changement de preset par CMake Tools),
// et quand un en-tête est créé sous un répertoire de construction de cette base (en-têtes générés
// à la première construction d'un preset : clangd ne relit pas un #include d'abord introuvable).
// Le répertoire vient du réglage clangd.arguments (`--compile-commands-dir`, écrit par lepton
// generate) ; scrutation par fs.watchFile, valable même si le répertoire n'existe pas encore.
import { createHash } from "node:crypto";
import { promises as fs, unwatchFile, watchFile } from "node:fs";
import * as path from "node:path";
import * as vscode from "vscode";
import { Batcher, compileCommandsDir, databaseDirectories } from "./batch";

const CLANGD_EXTENSION = "llvm-vs-code-extensions.vscode-clangd";
const POLL_MS = 2000;
const SETTLE_MS = 2000;
const HEADERS = "**/*.{h,hh,hpp,hxx}";

async function read(file: string): Promise<string | undefined> {
  try {
    return await fs.readFile(file, "utf8");
  } catch {
    return undefined;
  }
}

const digest = (text: string | undefined) =>
  text === undefined ? undefined : createHash("sha256").update(text).digest("hex");

export class ClangdRestarter implements vscode.Disposable {
  private file: string | undefined;
  private last: string | undefined;
  private readonly settle = new Batcher<string>(() => SETTLE_MS, () => this.check());
  private readonly headers = new Batcher<string>(() => SETTLE_MS, (created) => this.restart(
    vscode.l10n.t("{0} header(s) created under the build directories ({1})", created.length,
      path.basename(created[0]))));
  private headerWatchers: vscode.Disposable[] = [];
  private directories = "";
  private readonly subscription: vscode.Disposable;

  constructor(private readonly output: vscode.OutputChannel) {
    this.subscription = vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration("clangd.arguments") || e.affectsConfiguration("lepton.restartClangd")) {
        void this.start();
      }
    });
  }

  dispose(): void {
    this.stop();
    this.settle.dispose();
    this.headers.dispose();
    this.subscription.dispose();
  }

  private stop(): void {
    if (this.file) {
      unwatchFile(this.file);
      this.file = undefined;
    }
    this.watchHeaders([]);
  }

  /** Créations d'en-têtes sous les répertoires de construction de la base active. */
  private watchHeaders(dirs: string[]): void {
    const signature = JSON.stringify(dirs);
    if (signature === this.directories) {
      return;
    }
    this.headerWatchers.forEach((w) => w.dispose());
    this.headerWatchers = dirs.map((dir) => {
      const w = vscode.workspace.createFileSystemWatcher(
        new vscode.RelativePattern(vscode.Uri.file(dir), HEADERS), false, true, true);
      w.onDidCreate((u) => this.headers.add(u.fsPath));
      return w;
    });
    this.directories = signature;
  }

  async start(): Promise<void> {
    this.stop();
    if (!vscode.workspace.getConfiguration("lepton").get<boolean>("restartClangd", true)) {
      return;
    }
    const dir = compileCommandsDir(vscode.workspace.getConfiguration("clangd").get("arguments"));
    if (!dir) {
      return;
    }
    this.file = path.join(dir, "compile_commands.json");
    const text = await read(this.file);         // état lu par clangd à son démarrage
    this.last = digest(text);
    this.watchHeaders(text === undefined ? [] : databaseDirectories(text));
    watchFile(this.file, { interval: POLL_MS }, () => this.settle.add("change"));
    this.output.appendLine(vscode.l10n.t("clangd restarted when {0} changes", this.file) + "\n");
  }

  private async check(): Promise<void> {
    if (!this.file) {
      return;
    }
    const text = await read(this.file);
    const current = digest(text);
    if (current === undefined || current === this.last) {
      return;                                   // supprimée, ou recopiée à l'identique
    }
    this.last = current;
    this.watchHeaders(databaseDirectories(text!));
    await this.restart(vscode.l10n.t("{0} changed", this.file));
  }

  private async restart(reason: string): Promise<void> {
    if (!vscode.extensions.getExtension(CLANGD_EXTENSION)?.isActive) {
      return;
    }
    this.output.appendLine(vscode.l10n.t("{0}: clangd restarted", reason) + "\n");
    await vscode.commands.executeCommand("clangd.restart");
    vscode.window.setStatusBarMessage(vscode.l10n.t("lepton: clangd restarted"), 5000);
  }
}
