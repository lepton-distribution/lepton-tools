// Extension Lepton (ENV-12) : couche mince au-dessus de l'outil lepton.
import * as vscode from "vscode";
import { ClangdRestarter } from "./clangd";
import { Commands } from "./commands";
import { LeptonRunner } from "./runner";
import { Watchers } from "./watch";

export function activate(context: vscode.ExtensionContext): void {
  const output = vscode.window.createOutputChannel("Lepton");
  const runner = new LeptonRunner(output);
  const commands = new Commands(runner);
  commands.register(context);
  const watchers = new Watchers(runner, commands);
  const clangd = new ClangdRestarter(output);
  context.subscriptions.push(output, runner, watchers, clangd);
  void watchers.refresh();
  void clangd.start();
}

export function deactivate(): void {}
