// Extension Lepton (ENV-12) : couche mince au-dessus de l'outil lepton.
import * as vscode from "vscode";
import { Commands } from "./commands";

export function activate(context: vscode.ExtensionContext): void {
  const output = vscode.window.createOutputChannel("Lepton");
  context.subscriptions.push(output);
  new Commands(output).register(context);
}

export function deactivate(): void {}
