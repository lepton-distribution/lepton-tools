// F5 (CFG-7, ENV-12 §2bis) : fautes des manifestes en erreur dans *Problèmes*. La validation JSON
// intégrée ne signale qu'en avertissement ; lepton generate la coupe dans l'espace.
// - À la saisie : `lepton check --json --stdin FICHIER` sur le contenu non enregistré de
//   lepton-greffon.json et lepton-graine.json (schéma du seul fichier), temporisé, hors file
//   (lecture seule), le dernier appel gagne. Le XML reste à lemminx (portée exacte).
// - À l'enregistrement d'un manifeste ou du XML mklepton, et par la palette (L3-5) :
//   `lepton check --json`, contrôle complet du rootstock (GRA-2, GRF-5, CFG-5, trunk).
// Un document a soit les diagnostics de la saisie (depuis sa dernière modification), soit ceux du
// contrôle complet (depuis son dernier enregistrement) : jamais les deux.
import * as path from "node:path";
import * as vscode from "vscode";
import { Anomaly, CheckResult, EXIT_OK, EXIT_USER, diagnosticMessage, parseJson, placeOf, runLepton } from "./lepton";
import { LeptonRunner } from "./runner";

const MANIFESTS = new Set(["lepton-greffon.json", "lepton-graine.json"]);
const XML_DEFAULT = "**/mkconf_*.xml";
const SOURCE = "lepton";

function toDiagnostic(a: Anomaly): vscode.Diagnostic {
  const p = placeOf(a);
  // fin de ligne : position au-delà de la ligne, ramenée à sa fin par l'éditeur
  const range = new vscode.Range(p.line, p.character, p.endLine, p.endCharacter ?? Number.MAX_SAFE_INTEGER);
  const d = new vscode.Diagnostic(range, diagnosticMessage(a), vscode.DiagnosticSeverity.Error);
  d.source = SOURCE;
  return d;
}

/** Diagnostics regroupés par fichier ; chemins de lepton relatifs au répertoire de travail. */
function byFile(anomalies: Anomaly[], cwd: string): Map<string, vscode.Diagnostic[]> {
  const files = new Map<string, vscode.Diagnostic[]>();
  for (const a of anomalies) {
    const file = path.resolve(cwd, a.file);
    files.set(file, [...(files.get(file) ?? []), toDiagnostic(a)]);
  }
  return files;
}

export class Diagnostics implements vscode.Disposable {
  private readonly typing = vscode.languages.createDiagnosticCollection("lepton");
  private readonly full = vscode.languages.createDiagnosticCollection("lepton check");
  private readonly timers = new Map<string, NodeJS.Timeout>();
  private readonly running = new Map<string, AbortController>();
  private readonly subscriptions: vscode.Disposable[];

  constructor(private readonly runner: LeptonRunner) {
    this.subscriptions = [
      vscode.workspace.onDidOpenTextDocument((d) => this.schedule(d, 0)),
      vscode.workspace.onDidChangeTextDocument((e) => {
        if (e.contentChanges.length && this.isManifest(e.document)) {
          this.full.delete(e.document.uri);
          this.schedule(e.document);
        }
      }),
      vscode.workspace.onDidSaveTextDocument((d) => {
        if (this.enabled() && (this.isManifest(d) || this.isMkconf(d))) {
          this.cancel(d.uri);
          void this.checkAll();
        }
      }),
      vscode.workspace.onDidCloseTextDocument((d) => {
        this.cancel(d.uri);
        this.typing.delete(d.uri);
      }),
      vscode.workspace.onDidChangeConfiguration((e) => {
        if (e.affectsConfiguration("lepton.diagnostics.enabled")) {
          this.refresh();
        }
      }),
    ];
  }

  dispose(): void {
    this.timers.forEach((timer) => clearTimeout(timer));
    this.running.forEach((abort) => abort.abort());
    this.subscriptions.forEach((s) => s.dispose());
    this.typing.dispose();
    this.full.dispose();
  }

  /** Documents déjà ouverts à l'activation, ou réglage changé. */
  refresh(): void {
    if (!this.enabled()) {
      this.typing.clear();
      return;
    }
    vscode.workspace.textDocuments.forEach((d) => this.schedule(d, 0));
  }

  private config() {
    return vscode.workspace.getConfiguration("lepton");
  }

  private enabled(): boolean {
    return this.config().get<boolean>("diagnostics.enabled", true);
  }

  private isManifest(d: vscode.TextDocument): boolean {
    return d.uri.scheme === "file" && MANIFESTS.has(path.basename(d.uri.fsPath));
  }

  /** XML mklepton : motifs de `xml.fileAssociations` écrits par lepton generate. */
  private isMkconf(d: vscode.TextDocument): boolean {
    if (d.uri.scheme !== "file") {
      return false;
    }
    const assoc = vscode.workspace.getConfiguration("xml").get<{ pattern?: string }[]>("fileAssociations", []);
    const patterns = assoc.map((e) => e.pattern).filter((p): p is string => !!p);
    return (patterns.length ? patterns : [XML_DEFAULT]).some((pattern) => vscode.languages.match({ pattern }, d) > 0);
  }

  private cancel(uri: vscode.Uri): void {
    const key = uri.toString();
    clearTimeout(this.timers.get(key));
    this.timers.delete(key);
    this.running.get(key)?.abort();
    this.running.delete(key);
  }

  private schedule(d: vscode.TextDocument, delay?: number): void {
    if (!this.enabled() || !this.isManifest(d)) {
      return;
    }
    this.cancel(d.uri);
    const ms = delay ?? this.config().get<number>("diagnostics.delay", 400);
    this.timers.set(d.uri.toString(), setTimeout(() => void this.checkTyped(d), ms));
  }

  /** Schéma du seul document, sur son contenu non enregistré. */
  private async checkTyped(d: vscode.TextDocument): Promise<void> {
    const key = d.uri.toString();
    this.timers.delete(key);
    const cwd = this.runner.cwd();
    if (!cwd || d.isClosed) {
      return;
    }
    const version = d.version;
    const abort = new AbortController();
    this.running.set(key, abort);
    const result = await runLepton(this.runner.exe(), ["check", "--json", "--stdin", d.uri.fsPath], cwd,
      undefined, abort.signal, undefined, d.getText());
    if (abort.signal.aborted || d.isClosed || d.version !== version) {
      return;
    }
    this.running.delete(key);
    const report = parseJson<CheckResult>(result);
    if (!report) {          // lepton absent ou en échec : signalé dans le canal, diagnostics laissés
      this.runner.output.appendLine(`lepton check --stdin ${d.uri.fsPath} → code ${result.code}`);
      this.runner.output.append(result.stderr);
      return;
    }
    this.full.delete(d.uri);
    this.typing.set(d.uri, report.anomalies.map(toDiagnostic));
  }

  /** Contrôle complet du rootstock ; `notify` : commande de la palette (résultat annoncé). */
  async checkAll(notify = false): Promise<void> {
    const cwd = this.runner.cwd();
    if (!cwd) {
      if (notify) {
        vscode.window.showErrorMessage(
          vscode.l10n.t("Lepton: no folder open (open the workspace generated by lepton generate)."));
      }
      return;
    }
    const result = await this.runner.exec(["check", "--json"]);
    if (!result) {
      return;
    }
    const report = parseJson<CheckResult>(result);
    const title = vscode.l10n.t("check");
    if (!report) {
      if (notify) {
        void this.runner.report(title, result, false);
      }
      return;
    }
    const files = byFile(report.anomalies, cwd);
    this.full.clear();
    for (const [file, diagnostics] of files) {
      this.full.set(vscode.Uri.file(file), diagnostics);
    }
    for (const file of report.files) {           // contrôlés : le contrôle complet prime
      const uri = vscode.Uri.file(path.resolve(cwd, file));
      this.cancel(uri);
      this.typing.delete(uri);
    }
    if (!notify) {
      return;
    }
    if (result.code === EXIT_OK) {
      vscode.window.showInformationMessage(vscode.l10n.t("lepton: {0} — done", title));
    } else if (result.code === EXIT_USER) {
      const show = vscode.l10n.t("Show Problems");
      const choice = await vscode.window.showWarningMessage(
        vscode.l10n.t("lepton: {0} — {1} anomaly(ies), see Problems", title, report.anomalies.length), show);
      if (choice === show) {
        void vscode.commands.executeCommand("workbench.actions.view.problems");
      }
    } else {
      void this.runner.report(title, result, false);
    }
  }
}
