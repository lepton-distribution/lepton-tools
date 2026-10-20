// Regroupement d'événements et file d'exécution (F2, F3, F4) : un observateur qui appellerait
// lepton à chaque événement saturerait scion (fiche ENV-12, pièges connus).
// Module sans dépendance à l'API de l'éditeur : testé par node:test.

/** Accumule des éléments distincts et les livre ensemble `delay()` ms après le dernier ajout. */
export class Batcher<T> {
  private readonly pending = new Set<T>();
  private timer: NodeJS.Timeout | undefined;

  constructor(
    private readonly delay: () => number,
    private readonly fire: (items: T[]) => void | Promise<void>,
  ) {}

  add(item: T): void {
    this.pending.add(item);
    if (this.timer) {
      clearTimeout(this.timer);
    }
    this.timer = setTimeout(() => void this.flush(), this.delay());
  }

  async flush(): Promise<void> {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = undefined;
    }
    const items = [...this.pending];
    this.pending.clear();
    if (items.length) {
      await this.fire(items);
    }
  }

  dispose(): void {
    if (this.timer) {
      clearTimeout(this.timer);
    }
    this.pending.clear();
  }
}

/** Exécute les tâches une à une, dans l'ordre d'arrivée : jamais deux lepton à la fois sur un rootstock. */
export class SerialQueue {
  private tail: Promise<unknown> = Promise.resolve();

  run<T>(task: () => Promise<T>): Promise<T> {
    const next = this.tail.then(task, task);
    this.tail = next.catch(() => undefined);
    return next;
  }
}

/** Répertoire de `--compile-commands-dir` dans les arguments de clangd (`=DIR` ou argument suivant). */
export function compileCommandsDir(args: unknown): string | undefined {
  if (!Array.isArray(args)) {
    return undefined;
  }
  const opt = "--compile-commands-dir";
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (typeof a !== "string") {
      continue;
    }
    if (a.startsWith(opt + "=")) {
      return a.slice(opt.length + 1) || undefined;
    }
    if (a === opt && typeof args[i + 1] === "string") {
      return args[i + 1];
    }
  }
  return undefined;
}
