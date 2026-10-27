// F8 : sources de l'arrêt (pile, points d'arrêt) ouvertes par le trunk et non par le clone (R3).
// L'adaptateur (Cortex-Debug, CodeLLDB…) rend le chemin résolu par gdb ; ses messages sont réécrits
// avant d'atteindre l'éditeur. Correspondance d'après lepton seed status --json, lue à chaque session.
import { existsSync } from "node:fs";
import * as vscode from "vscode";
import { StatusResult, parseJson } from "./lepton";
import { LeptonRunner } from "./runner";
import { SourceMap, rewriteSources, sourceMap, toTrunk } from "./srcmap";

export class DebugSources implements vscode.Disposable {
  private readonly disposables: vscode.Disposable[] = [];

  constructor(private readonly runner: LeptonRunner) {
    this.disposables.push(vscode.debug.registerDebugAdapterTrackerFactory("*", {
      createDebugAdapterTracker: (session) => this.tracker(session),
    }));
  }

  private async tracker(session: vscode.DebugSession): Promise<vscode.DebugAdapterTracker | undefined> {
    if (!vscode.workspace.getConfiguration("lepton").get<boolean>("debug.trunkPaths", true)) {
      return undefined;
    }
    const result = await this.runner.exec(["seed", "status", "--json"]);
    const status = result && parseJson<StatusResult>(result);
    if (!status?.scions) {
      return undefined;                         // espace sans graine : aucune réécriture
    }
    const map: SourceMap = sourceMap(status.trunk, status.scions.map((s) => s.stem));
    const cache = new Map<string, string>();
    const rewrite = (p: string) => {
      let trunk = cache.get(p);
      if (trunk === undefined) {
        trunk = toTrunk(map, p, existsSync);
        cache.set(p, trunk);
      }
      return trunk;
    };
    this.runner.output.appendLine(vscode.l10n.t("Debug session {0}: sources shown through the trunk ({1} scion(s))",
      session.name, map.stems.length));
    return { onDidSendMessage: (message) => rewriteSources(message, rewrite) };
  }

  dispose(): void {
    this.disposables.forEach((d) => d.dispose());
  }
}
