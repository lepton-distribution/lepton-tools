// F4 (O10, R1) : relance de clangd quand la base compile_commands.json qu'il lit apparaît ou change
// de contenu (premier preset configuré après l'ouverture, changement de preset par CMake Tools).
// Le répertoire vient du réglage clangd.arguments (`--compile-commands-dir`, écrit par lepton
// generate) ; scrutation par fs.watchFile, valable même si le répertoire n'existe pas encore.
import { createHash } from "node:crypto";
import { promises as fs, unwatchFile, watchFile } from "node:fs";
import * as path from "node:path";
import * as vscode from "vscode";
import { Batcher, compileCommandsDir } from "./batch";

const CLANGD_EXTENSION = "llvm-vs-code-extensions.vscode-clangd";
const POLL_MS = 2000;
const SETTLE_MS = 2000;

async function digest(file: string): Promise<string | undefined> {
  try {
    return createHash("sha256").update(await fs.readFile(file)).digest("hex");
  } catch {
    return undefined;
  }
}

export class ClangdRestarter implements vscode.Disposable {
  private file: string | undefined;
  private last: string | undefined;
  private readonly settle = new Batcher<string>(() => SETTLE_MS, () => this.check());
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
    this.subscription.dispose();
  }

  private stop(): void {
    if (this.file) {
      unwatchFile(this.file);
      this.file = undefined;
    }
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
    this.last = await digest(this.file);         // état lu par clangd à son démarrage
    watchFile(this.file, { interval: POLL_MS }, () => this.settle.add("change"));
    this.output.appendLine(vscode.l10n.t("clangd restarted when {0} changes", this.file) + "\n");
  }

  private async check(): Promise<void> {
    if (!this.file) {
      return;
    }
    const current = await digest(this.file);
    if (current === undefined || current === this.last) {
      return;                                   // supprimée, ou recopiée à l'identique
    }
    this.last = current;
    if (!vscode.extensions.getExtension(CLANGD_EXTENSION)?.isActive) {
      return;
    }
    this.output.appendLine(vscode.l10n.t("{0} changed: clangd restarted", this.file) + "\n");
    await vscode.commands.executeCommand("clangd.restart");
    vscode.window.setStatusBarMessage(vscode.l10n.t("lepton: clangd restarted (new compilation database)"), 5000);
  }
}
