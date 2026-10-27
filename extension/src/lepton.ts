// Seul point d'appel de l'outil lepton (ENV-12) : l'extension relaie des arguments et lit les
// sorties de lepton ; aucune logique de graine ni de greffon ici (SPECIFICATION §Architecture).
// Module sans dépendance à l'API de l'éditeur : testé par node:test.
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

// Codes de retour de lepton (lepton/cli.py)
export const EXIT_OK = 0;
export const EXIT_USER = 1;
export const EXIT_FAILURE = 2;
export const EXIT_INTERRUPT = 130;

export interface LeptonResult {
  code: number;
  stdout: string;
  stderr: string;
}

/** Exécutable : réglage `lepton.path`, sinon installation pipx (INS-6), sinon `lepton` du PATH. */
export function resolveLepton(configured: string, home: string = homedir()): string {
  if (configured) {
    return configured;
  }
  const pipx = join(home, ".local", "bin", "lepton");
  return existsSync(pipx) ? pipx : "lepton";
}

/** Lance `lepton ARGS` dans `cwd` ; `onOutput` reçoit stdout et stderr au fil de l'eau (flux nommé) ;
 *  `notFound` met en forme le message d'exécutable absent (traduit par l'appelant) ; `input` est
 *  écrit sur l'entrée standard (`check --stdin`). */
export function runLepton(
  exe: string,
  args: string[],
  cwd: string,
  onOutput?: (text: string, stream: "stdout" | "stderr") => void,
  signal?: AbortSignal,
  notFound: (exe: string) => string = (e) => `lepton not found: ${e} (setting lepton.path)`,
  input?: string,
): Promise<LeptonResult> {
  return new Promise((resolve) => {
    let stdout = "";
    let stderr = "";
    const child = spawn(exe, args, { cwd, stdio: ["pipe", "pipe", "pipe"] });
    child.stdin.on("error", () => undefined);          // lepton terminé avant d'avoir tout lu
    child.stdin.end(input ?? "", "utf8");              // sans input : entrée standard vide
    child.stdout.setEncoding("utf8").on("data", (d: string) => {
      stdout += d;
      onOutput?.(d, "stdout");
    });
    child.stderr.setEncoding("utf8").on("data", (d: string) => {
      stderr += d;
      onOutput?.(d, "stderr");
    });
    const abort = () => child.kill("SIGINT");
    signal?.addEventListener("abort", abort, { once: true });
    child.on("error", (e: NodeJS.ErrnoException) => {
      signal?.removeEventListener("abort", abort);
      const message = e.code === "ENOENT" ? notFound(exe) : e.message;
      onOutput?.(message + "\n", "stderr");
      resolve({ code: EXIT_FAILURE, stdout, stderr: stderr + message + "\n" });
    });
    child.on("close", (code, sig) => {
      signal?.removeEventListener("abort", abort);
      resolve({ code: code ?? (sig ? EXIT_INTERRUPT : EXIT_FAILURE), stdout, stderr });
    });
  });
}

/** Dernier message de lepton sur stderr (« lepton: erreur: … » et sa ligne « → … »), sinon dernière ligne. */
export function lastMessage(result: LeptonResult): string {
  const lines = result.stderr.split("\n").map((l) => l.trim()).filter((l) => l);
  const start = lines.map((l) => l.startsWith("lepton:")).lastIndexOf(true);
  return lines.slice(start >= 0 ? start : Math.max(lines.length - 1, 0)).join(" ");
}

/** Greffon tel que le décrit lepton (`file owner --json`, `seed status --json`). */
export interface ScionRef {
  name: string;
  key: string;
  in_seed: boolean;
}

/** Sortie de `lepton file owner PATH --json` (rapports/env-8-interface.md §12). */
export interface OwnerResult {
  path: string;
  relative: string;
  trunk_path: string;
  kind: "clone" | "link" | "unlinked" | "directory" | "regular" | "absent" | "ignored";
  status: "owned" | "ambiguous" | "none";
  source: string | null;
  owner: (ScionRef & { clone_path: string }) | null;
  candidates: ScionRef[];
}

/** Greffon de `lepton seed status --json`, avec son état git. */
export interface StatusScion extends ScionRef {
  role: string;
  stem: string;
  path: string;
  version: string;
  location: string | null;
  branch: string | null;
  commit: string | null;
  dirty: number | null;
  dirty_files: string[];
}

/** Sortie de `lepton seed status --json`, champs lus par l'extension. */
export interface StatusResult {
  rootstock: string;
  trunk: string;
  scions: StatusScion[];
}

/** Fichier de `lepton seed tree --json` : `trunk_path` nul pour une source générée (hors trunk). */
export interface TreeFile {
  relative: string;
  trunk_path: string | null;
  clone_path: string;
  kind: "compiled" | "header" | "unbuilt";
}

/** Fichiers d'un greffon (`key` nul : source générée ou hors greffon). */
export interface TreeScion {
  key: string | null;
  name: string | null;
  generated: boolean;
  files: TreeFile[];
}

export interface TreeLibrary {
  name: string;
  type: string;
  scions: TreeScion[];
}

/** Sortie de `lepton seed tree --json` (rapports/env-8-interface.md §14) ; `scions` = `seed status`. */
export interface TreeResult {
  rootstock: string;
  trunk: string;
  preset: string | null;
  preset_reason: string;
  build: string | null;
  build_root: string;
  source: "codemodel" | "manifests";
  message: string | null;
  scions: StatusScion[];
  executables: { name: string; libraries: TreeLibrary[] }[];
  by_scion: TreeScion[];
}

/** JSON de la sortie standard de lepton ; `undefined` si elle n'en est pas. */
export function parseJson<T>(result: LeptonResult): T | undefined {
  try {
    return JSON.parse(result.stdout) as T;
  } catch {
    return undefined;
  }
}

/** Anomalie de `lepton check --json` : portée à partir de 1, fin exclue, `null` si inconnue
 *  (XML : ligne seule ; rapports/env-8-interface.md §13). */
export interface Anomaly {
  file: string;
  location: string;
  message: string;
  line?: number | null;
  column?: number | null;
  end_line?: number | null;
  end_column?: number | null;
}

/** Sortie de `lepton check --json`. */
export interface CheckResult {
  files: string[];
  anomalies: Anomaly[];
}

/** Portée d'un diagnostic, à partir de 0 ; `endCharacter` absent : jusqu'à la fin de la ligne. */
export interface Place {
  line: number;
  character: number;
  endLine: number;
  endCharacter?: number;
}

/** Portée de l'éditeur pour une anomalie : telle quelle si lepton la donne, ligne entière si la
 *  colonne manque, première ligne si rien n'est situé. */
export function placeOf(a: Anomaly): Place {
  if (!a.line || a.line < 1) {
    return { line: 0, character: 0, endLine: 0 };
  }
  const line = a.line - 1;
  if (!a.column || a.column < 1) {
    return { line, character: 0, endLine: line };
  }
  const endLine = a.end_line && a.end_line >= a.line ? a.end_line - 1 : line;
  const endCharacter = a.end_column && a.end_column >= 1 ? a.end_column - 1 : a.column;
  return { line, character: a.column - 1, endLine, endCharacter };
}

/** Texte du diagnostic : emplacement de lepton (pointeur, chemin XML) en tête, sans le numéro de
 *  ligne de xmllint quand la ligne est déjà située. */
export function diagnosticMessage(a: Anomaly): string {
  const message = a.line ? a.message.replace(/^\d+: /, "") : a.message;
  return a.location && a.location !== "/" ? `${a.location}: ${message}` : message;
}
