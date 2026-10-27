// Répertoires de la vue IDE-1 (F6) : fichiers groupés par répertoire, chaînes de répertoires sans
// fichier compactées en un seul nœud (« sys/root/src/kernel »). Pure présentation des chemins donnés
// par lepton. Module sans dépendance à l'API de l'éditeur : testé par node:test.

export interface DirNode<T> {
  /** Chemin relatif complet du répertoire (séparateur `/`), "" pour la racine. */
  path: string;
  /** Libellé : segments compactés depuis le parent. */
  label: string;
  dirs: DirNode<T>[];
  files: { name: string; item: T }[];
}

/** Arborescence des `items` d'après leur chemin relatif (`/`), répertoires et fichiers triés. */
export function buildDirs<T>(items: T[], relative: (item: T) => string): DirNode<T> {
  const root: DirNode<T> = { path: "", label: "", dirs: [], files: [] };
  for (const item of items) {
    const parts = relative(item).split("/").filter((p) => p);
    let node = root;
    for (const part of parts.slice(0, -1)) {
      let next = node.dirs.find((d) => d.label === part);
      if (!next) {
        next = { path: node.path ? `${node.path}/${part}` : part, label: part, dirs: [], files: [] };
        node.dirs.push(next);
      }
      node = next;
    }
    node.files.push({ name: parts[parts.length - 1] ?? "", item });
  }
  return sortDirs(compact(root));
}

function compact<T>(node: DirNode<T>): DirNode<T> {
  node.dirs = node.dirs.map((d) => {
    let c = d;
    while (c.files.length === 0 && c.dirs.length === 1) {
      const only = c.dirs[0];
      c = { ...only, label: `${c.label}/${only.label}` };
    }
    return compact(c);
  });
  return node;
}

function sortDirs<T>(node: DirNode<T>): DirNode<T> {
  node.dirs.sort((a, b) => a.label.localeCompare(b.label));
  node.files.sort((a, b) => a.name.localeCompare(b.name));
  node.dirs.forEach(sortDirs);
  return node;
}

/** Description courte de l'état git d'un greffon : « branche commit ●N » (N fichiers modifiés). */
export function gitSummary(s: { branch: string | null; commit: string | null; dirty: number | null }): string {
  if (!s.commit) {
    return "";
  }
  const dirty = s.dirty ? ` ●${s.dirty}` : "";
  return `${s.branch ?? "HEAD"} ${s.commit}${dirty}`;
}
