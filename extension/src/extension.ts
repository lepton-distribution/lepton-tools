// Extension Lepton (ENV-12) : couche mince au-dessus de l'outil lepton.
import * as vscode from "vscode";
import { ClangdRestarter } from "./clangd";
import { Commands } from "./commands";
import { DebugSources } from "./debug";
import { Diagnostics } from "./diagnostics";
import { LeptonRunner } from "./runner";
import { ArchitectureView } from "./tree";
import { Watchers } from "./watch";

export function activate(context: vscode.ExtensionContext): void {
  const output = vscode.window.createOutputChannel("Lepton");
  const runner = new LeptonRunner(output);
  const diagnostics = new Diagnostics(runner);
  const commands = new Commands(runner, diagnostics);
  commands.register(context);
  const watchers = new Watchers(runner, commands);
  const clangd = new ClangdRestarter(output);
  const architecture = new ArchitectureView(runner, [runner.onDidRunCommand, watchers.onDidChangeTrunk]);
  architecture.register(context);
  const debugSources = new DebugSources(runner);
  context.subscriptions.push(output, runner, watchers, clangd, diagnostics, architecture, debugSources);
  void watchers.refresh();
  void clangd.start();
  diagnostics.refresh();
}

export function deactivate(): void {}
