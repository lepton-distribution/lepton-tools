// F8 : sources de l'arrêt (pile, points d'arrêt) ouvertes par le trunk et non par le clone (R3).
// L'adaptateur (Cortex-Debug, CodeLLDB…) rend le chemin résolu par gdb ; ses messages sont réécrits
// avant d'atteindre l'éditeur. Correspondance d'après lepton seed status --json, lue à l'activation,
// après chaque commande et au début de chaque session, sans que le lancement l'attende.
import { existsSync } from "node:fs";
import * as vscode from "vscode";
import { StatusResult, parseJson } from "./lepton";
import { LeptonRunner } from "./runner";
import { SourceMap, rewriteSources, sourceMap, toTrunk } from "./srcmap";

export class DebugSources implements vscode.Disposable {
  private readonly disposables: vscode.Disposable[] = [];
  private map: SourceMap | undefined;

  constructor(private readonly runner: LeptonRunner) {
    this.disposables.push(
      vscode.debug.registerDebugAdapterTrackerFactory("*", {
        createDebugAdapterTracker: (session) => this.tracker(session),
      }),
      runner.onDidRunCommand(() => void this.load()),
    );
    void this.load();
  }

  /** Table clone → trunk ; aucune graine : pas de table, aucune réécriture. */
  private async load(): Promise<void> {
    const result = await this.runner.exec(["seed", "status", "--json"]);
    const status = result && parseJson<StatusResult>(result);
    this.map = status?.scions ? sourceMap(status.trunk, status.scions.map((s) => s.stem)) : undefined;
  }

  /** Rendu sans attendre lepton : VSCodium 1.135 abandonne sans le signaler un traceur rendu après
   *  1 s (`Promise.race` de l'hôte d'extensions ; L6-6, première session d'une fenêtre). */
  private tracker(session: vscode.DebugSession): vscode.DebugAdapterTracker | undefined {
    if (!vscode.workspace.getConfiguration("lepton").get<boolean>("debug.trunkPaths", true)) {
      return undefined;
    }
    void this.load();                           // graine changée hors de l'éditeur
    const cache = new Map<string, string>();
    let used: SourceMap | undefined;
    const rewrite = (p: string) => {
      const map = this.map;
      if (!map) {
        return p;
      }
      if (map !== used) {
        cache.clear();
        used = map;
      }
      let trunk = cache.get(p);
      if (trunk === undefined) {
        trunk = toTrunk(map, p, existsSync);
        cache.set(p, trunk);
      }
      return trunk;
    };
    if (this.map) {
      this.runner.output.appendLine(vscode.l10n.t("Debug session {0}: sources shown through the trunk ({1} scion(s))",
        session.name, this.map.stems.length));
    }
    return { onDidSendMessage: (message) => rewriteSources(message, rewrite) };
  }

  dispose(): void {
    this.disposables.forEach((d) => d.dispose());
  }
}
