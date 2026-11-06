// Correspondance clone → trunk des sources affichées à l'arrêt (F8, R3 d'ENV-9, écart PA-1) : gdb
// rend le chemin résolu (`fullname` = clone) d'un fichier compilé par le trunk ; on le ramène au lien
// du trunk, d'après `stem` et `trunk` de `lepton seed status --json` (comme la vue, en sens inverse).
// Clé projetée d'un dépôt tiers (ENV-41) : le chemin du clone ne se retrouve pas dans le trunk ; la
// table fichier par fichier `projection` (racine `root`) de seed status en tient lieu.
// Module sans dépendance à l'API de l'éditeur : testé par node:test.
import * as path from "node:path";

export interface SourceMap {
  trunk: string;
  /** `<clone>/scion` résolu de chaque greffon, du plus long au plus court. */
  stems: string[];
  /** Fichier d'un clone tiers projeté (absolu) → lien du trunk (absolu). */
  files: Map<string, string>;
}

/** Clé projetée de `seed status --json` : racine résolue du clone tiers et table clone → trunk. */
export interface Projection {
  root: string;
  projection: Record<string, string>;
}

export function sourceMap(trunk: string, stems: string[], projections: Projection[] = []): SourceMap {
  const files = new Map<string, string>();
  for (const p of projections) {
    for (const [clone, rel] of Object.entries(p.projection ?? {})) {
      files.set(path.join(p.root, clone), path.join(trunk, rel));
    }
  }
  return { trunk, stems: stems.filter((s) => s).sort((a, b) => b.length - a.length), files };
}

/** Chemin du trunk d'un fichier du clone, s'il y est greffé (`exists`) ; sinon le chemin inchangé. */
export function toTrunk(map: SourceMap, file: string, exists: (p: string) => boolean): string {
  const projected = map.files.get(file);
  if (projected !== undefined) {
    return exists(projected) ? projected : file;
  }
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
