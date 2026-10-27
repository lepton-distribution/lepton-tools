// Correspondance clone → trunk des sources affichées à l'arrêt (F8, R3 d'ENV-9, écart PA-1) : gdb
// rend le chemin résolu (`fullname` = clone) d'un fichier compilé par le trunk ; on le ramène au lien
// du trunk, d'après `stem` et `trunk` de `lepton seed status --json` (comme la vue, en sens inverse).
// Module sans dépendance à l'API de l'éditeur : testé par node:test.
import * as path from "node:path";

export interface SourceMap {
  trunk: string;
  /** `<clone>/scion` résolu de chaque greffon, du plus long au plus court. */
  stems: string[];
}

export function sourceMap(trunk: string, stems: string[]): SourceMap {
  return { trunk, stems: stems.filter((s) => s).sort((a, b) => b.length - a.length) };
}

/** Chemin du trunk d'un fichier du clone, s'il y est greffé (`exists`) ; sinon le chemin inchangé. */
export function toTrunk(map: SourceMap, file: string, exists: (p: string) => boolean): string {
  for (const stem of map.stems) {
    if (file.startsWith(stem + path.sep)) {
      const candidate = path.join(map.trunk, file.slice(stem.length + 1));
      return exists(candidate) ? candidate : file;
    }
  }
  return file;
}

/** Réécrit en place les `path` des objets `source` (et des listes `sources`) d'un message DAP. */
export function rewriteSources(message: unknown, rewrite: (p: string) => string): void {
  if (Array.isArray(message)) {
    message.forEach((m) => rewriteSources(m, rewrite));
    return;
  }
  if (!message || typeof message !== "object") {
    return;
  }
  for (const [key, value] of Object.entries(message as Record<string, unknown>)) {
    if (key === "source") {
      fixPath(value, rewrite);
    } else if (key === "sources" && Array.isArray(value)) {
      value.forEach((v) => fixPath(v, rewrite));
    }
    rewriteSources(value, rewrite);
  }
}

function fixPath(source: unknown, rewrite: (p: string) => string): void {
  const s = source as { path?: unknown } | null;
  if (s && typeof s === "object" && typeof s.path === "string") {
    s.path = rewrite(s.path);
  }
}
