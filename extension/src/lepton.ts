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

/** Lance `lepton ARGS` dans `cwd` ; `onOutput` reçoit stdout et stderr au fil de l'eau ;
 *  `notFound` met en forme le message d'exécutable absent (traduit par l'appelant). */
export function runLepton(
  exe: string,
  args: string[],
  cwd: string,
  onOutput?: (text: string) => void,
  signal?: AbortSignal,
  notFound: (exe: string) => string = (e) => `lepton not found: ${e} (setting lepton.path)`,
): Promise<LeptonResult> {
  return new Promise((resolve) => {
    let stdout = "";
    let stderr = "";
    const child = spawn(exe, args, { cwd, stdio: ["ignore", "pipe", "pipe"] });
    child.stdout.setEncoding("utf8").on("data", (d: string) => {
      stdout += d;
      onOutput?.(d);
    });
    child.stderr.setEncoding("utf8").on("data", (d: string) => {
      stderr += d;
      onOutput?.(d);
    });
    const abort = () => child.kill("SIGINT");
    signal?.addEventListener("abort", abort, { once: true });
    child.on("error", (e: NodeJS.ErrnoException) => {
      signal?.removeEventListener("abort", abort);
      const message = e.code === "ENOENT" ? notFound(exe) : e.message;
      onOutput?.(message + "\n");
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
  kind: "clone" | "link" | "directory" | "regular" | "absent" | "ignored";
  status: "owned" | "ambiguous" | "none";
  source: string | null;
  owner: (ScionRef & { clone_path: string }) | null;
  candidates: ScionRef[];
}

/** Sortie de `lepton seed status --json`, champs lus par l'extension. */
export interface StatusResult {
  rootstock: string;
  trunk: string;
  scions: (ScionRef & { role: string; stem: string })[];
}

/** JSON de la sortie standard de lepton ; `undefined` si elle n'en est pas. */
export function parseJson<T>(result: LeptonResult): T | undefined {
  try {
    return JSON.parse(result.stdout) as T;
  } catch {
    return undefined;
  }
}
