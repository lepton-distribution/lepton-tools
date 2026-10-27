// F6 (IDE-1) : vue « Architecture », exécutif → bibliothèques → greffons → répertoires → fichiers,
// d'après `lepton seed tree --json` (API fichier CMake du preset actif, lue par lepton) ; état git des
// greffons d'après les mêmes entrées que `lepton seed status`. Aucune règle de greffon ici : l'extension
// présente ce que lepton rend et relaie les actions (file add / remove).
import * as path from "node:path";
import * as vscode from "vscode";
import { Batcher } from "./batch";
import { DirNode, buildDirs, gitSummary } from "./layout";
import { EXIT_OK, StatusScion, TreeFile, TreeResult, TreeScion, lastMessage, parseJson } from "./lepton";
import { LeptonRunner } from "./runner";

const t = (message: string, ...args: (string | number)[]) => vscode.l10n.t(message, ...args);
const REFRESH_MS = 1000;
// Changements qui modifient la vue : preset actif (base de clangd copiée par CMake Tools), nouvelle
// réponse de l'API fichier (configuration d'un preset) ; relatifs à build/.
const BUILD_PATTERN = "{.active/compile_commands.json,*/.cmake/api/v1/reply/index-*.json}";

type Node =
  | { kind: "message"; text: string }
  | { kind: "executable"; name: string; libraries: TreeResult["executables"][number]["libraries"] }
  | { kind: "library"; exe: string; name: string; type: string; scions: TreeScion[] }
  | { kind: "scion"; group: TreeScion }
  | { kind: "seed"; scions: StatusScion[] }
  | { kind: "status"; scion: StatusScion }
  | { kind: "dir"; group: TreeScion; dir: DirNode<TreeFile> }
  | { kind: "file"; group: TreeScion; file: TreeFile; name: string };

export class ArchitectureView implements vscode.TreeDataProvider<Node>, vscode.Disposable {
  private data: TreeResult | undefined;
  private error: string | undefined;
  private loaded = false;
  private stale = true;
  private view: vscode.TreeView<Node> | undefined;
  private buildWatcher: vscode.FileSystemWatcher | undefined;
  private buildRoot = "";
  private readonly changed = new vscode.EventEmitter<Node | undefined>();
  readonly onDidChangeTreeData = this.changed.event;
  private readonly refreshes = new Batcher<string>(() => REFRESH_MS, () => this.reload());
  private readonly subscriptions: vscode.Disposable[] = [];

  constructor(private readonly runner: LeptonRunner, changes: vscode.Event<void>[]) {
    for (const e of changes) {
      this.subscriptions.push(e(() => this.refresh()));
    }
  }

  register(context: vscode.ExtensionContext): void {
    this.view = vscode.window.createTreeView("lepton.architecture", { treeDataProvider: this, showCollapseAll: true });
    this.subscriptions.push(this.view, this.view.onDidChangeVisibility((e) => {
      if (e.visible && this.stale) {
        this.refresh();
      }
    }));
    const table: [string, (n?: Node) => unknown][] = [
      ["lepton.tree.refresh", () => this.refresh()],
      ["lepton.tree.newFile", (n) => this.newFile(n)],
      ["lepton.tree.removeFile", (n) => this.removeFile(n)],
      ["lepton.tree.revealInClone", (n) => this.revealInClone(n)],
    ];
    for (const [id, fn] of table) {
      context.subscriptions.push(vscode.commands.registerCommand(id, fn));
    }
  }

  dispose(): void {
    this.refreshes.dispose();
    this.buildWatcher?.dispose();
    this.changed.dispose();
    this.subscriptions.forEach((d) => d.dispose());
  }

  /** Relecture regroupée ; différée tant que la vue est masquée. */
  refresh(): void {
    this.stale = true;
    if (this.view?.visible) {
      this.refreshes.add("refresh");
    }
  }

  private async reload(): Promise<void> {
    this.stale = false;
    const result = await this.runner.exec(["seed", "tree", "--json"]);
    const data = result && parseJson<TreeResult>(result);
    this.loaded = true;
    if (result && data?.scions) {
      this.data = data;
      this.error = undefined;
      this.watchBuild(data.build_root);
    } else {
      this.data = undefined;
      this.error = result ? lastMessage(result) || t("lepton seed tree --json: unreadable output") : undefined;
    }
    if (this.view) {
      this.view.description = this.data?.preset ?? undefined;
    }
    this.changed.fire(undefined);
  }

  private watchBuild(root: string): void {
    if (root === this.buildRoot) {
      return;
    }
    this.buildWatcher?.dispose();
    this.buildRoot = root;
    this.buildWatcher = vscode.workspace.createFileSystemWatcher(
      new vscode.RelativePattern(vscode.Uri.file(root), BUILD_PATTERN));
    for (const ev of [this.buildWatcher.onDidCreate, this.buildWatcher.onDidChange]) {
      ev(() => this.refresh());
    }
  }

  // ------------------------------------------------------------------ nœuds

  private status(key: string | null): StatusScion | undefined {
    return key ? this.data?.scions.find((s) => s.key === key) : undefined;
  }

  getChildren(node?: Node): Node[] {
    if (!node) {
      return this.roots();
    }
    switch (node.kind) {
      case "executable":
        return node.libraries.map((l) => ({ kind: "library", exe: node.name, name: l.name, type: l.type, scions: l.scions }));
      case "library":
        return node.scions.map((g) => ({ kind: "scion", group: g }));
      case "scion":
        return this.dirChildren(node.group, this.dirsOf(node.group));
      case "dir":
        return this.dirChildren(node.group, node.dir);
      case "seed":
        return node.scions.map((s) => ({ kind: "status", scion: s }));
      default:
        return [];
    }
  }

  private roots(): Node[] {
    if (!this.loaded) {
      this.refresh();
      return [];
    }
    if (!this.data) {
      return this.error ? [{ kind: "message", text: this.error }] : [];
    }
    const nodes: Node[] = [];
    if (this.data.message) {
      nodes.push({ kind: "message", text: this.data.message });
    }
    nodes.push(...this.data.executables.map((e): Node => ({ kind: "executable", name: e.name, libraries: e.libraries })));
    nodes.push(...this.data.by_scion.map((g): Node => ({ kind: "scion", group: g })));
    nodes.push({ kind: "seed", scions: this.data.scions });
    return nodes;
  }

  /** Répertoires d'un greffon : chemins du trunk ; sources générées relatives au répertoire de construction. */
  private dirsOf(group: TreeScion): DirNode<TreeFile> {
    const build = this.data?.build ?? "";
    return buildDirs(group.files, (f) =>
      f.trunk_path ? f.relative : path.relative(build, f.clone_path).split(path.sep).join("/"));
  }

  private dirChildren(group: TreeScion, dir: DirNode<TreeFile>): Node[] {
    return [
      ...dir.dirs.map((d): Node => ({ kind: "dir", group, dir: d })),
      ...dir.files.map((f): Node => ({ kind: "file", group, file: f.item, name: f.name })),
    ];
  }

  getTreeItem(node: Node): vscode.TreeItem {
    const C = vscode.TreeItemCollapsibleState;
    switch (node.kind) {
      case "message": {
        const item = new vscode.TreeItem(node.text, C.None);
        item.iconPath = new vscode.ThemeIcon("info");
        item.tooltip = node.text;
        return item;
      }
      case "executable": {
        const item = new vscode.TreeItem(node.name, node.name === "lepton" ? C.Expanded : C.Collapsed);
        item.iconPath = new vscode.ThemeIcon("file-binary");
        item.description = t("executable");
        return item;
      }
      case "library": {
        const own = node.name === node.exe;
        const item = new vscode.TreeItem(own ? t("{0} (own sources)", node.name) : node.name, C.Collapsed);
        item.iconPath = new vscode.ThemeIcon(own ? "file-code" : "library");
        item.description = node.type;
        return item;
      }
      case "scion":
        return this.scionItem(node.group);
      case "seed": {
        const item = new vscode.TreeItem(t("Scions of the seed"), C.Collapsed);
        item.iconPath = new vscode.ThemeIcon("repo");
        item.description = String(node.scions.length);
        return item;
      }
      case "status":
        return this.statusItem(node.scion);
      case "dir": {
        const item = new vscode.TreeItem(node.dir.label, C.Collapsed);
        item.iconPath = vscode.ThemeIcon.Folder;
        item.contextValue = node.group.key ? "lepton.dir" : undefined;
        item.tooltip = node.dir.path;
        return item;
      }
      case "file": {
        const target = vscode.Uri.file(node.file.trunk_path ?? node.file.clone_path);
        const item = new vscode.TreeItem(target, C.None);
        item.label = node.name;
        item.description = node.file.kind === "header" ? t("header") : undefined;
        item.tooltip = node.file.trunk_path ? `${node.file.trunk_path}\n→ ${node.file.clone_path}` : node.file.clone_path;
        item.command = { command: "vscode.open", title: t("Open"), arguments: [target] };
        item.contextValue = node.group.key ? "lepton.file" : undefined;
        return item;
      }
    }
  }

  private scionItem(group: TreeScion): vscode.TreeItem {
    const s = this.status(group.key);
    const label = group.name ?? (group.generated ? t("generated") : t("outside scions"));
    const item = new vscode.TreeItem(label, vscode.TreeItemCollapsibleState.Collapsed);
    item.iconPath = new vscode.ThemeIcon(group.generated ? "gear" : "repo");
    item.description = s ? gitSummary(s) : undefined;
    item.tooltip = s ? this.statusTooltip(s) : undefined;
    item.contextValue = s ? "lepton.scion" : undefined;
    return item;
  }

  private statusItem(s: StatusScion): vscode.TreeItem {
    const item = new vscode.TreeItem(s.name, vscode.TreeItemCollapsibleState.None);
    item.iconPath = new vscode.ThemeIcon(s.dirty ? "repo-forked" : "repo");
    item.description = [s.role, gitSummary(s)].filter((x) => x).join(" · ");
    item.tooltip = this.statusTooltip(s);
    item.contextValue = "lepton.scion";
    return item;
  }

  private statusTooltip(s: StatusScion): vscode.MarkdownString {
    const md = new vscode.MarkdownString();
    md.appendMarkdown(`**${s.name}** — ${s.role}\n\n`);
    md.appendMarkdown(`${t("key")}: \`${s.key}\`  \n${t("version")}: \`${s.version}\`  \n`);
    md.appendMarkdown(`${t("origin")}: \`${s.location ?? t("(outside the seed)")}\`  \n${t("clone")}: \`${s.path}\``);
    if (s.dirty_files.length) {
      md.appendMarkdown(`\n\n${t("{0} modified file(s):", s.dirty_files.length)}\n`);
      for (const f of s.dirty_files.slice(0, 20)) {
        md.appendMarkdown(`\n- \`${f}\``);
      }
    }
    return md;
  }

  // ------------------------------------------------------------------ actions

  private async newFile(node?: Node): Promise<void> {
    if (node?.kind !== "dir" || !node.group.name || !this.data) {
      return;
    }
    const dir = path.join(this.data.trunk, ...node.dir.path.split("/"));
    const name = await vscode.window.showInputBox({ prompt: t("New file in {0}", dir), ignoreFocusOut: true });
    if (!name?.trim()) {
      return;
    }
    const full = path.join(dir, name.trim());
    const result = await this.runner.run(t("create {0}", path.basename(full)),
      ["file", "add", full, "--scion", node.group.name]);
    if (result?.code === EXIT_OK) {
      await vscode.window.showTextDocument(vscode.Uri.file(full));
    }
  }

  private async removeFile(node?: Node): Promise<void> {
    if (node?.kind !== "file" || !node.file.trunk_path) {
      return;
    }
    const remove = t("Remove");
    const answer = await vscode.window.showWarningMessage(
      t("Remove {0} from its scion?", node.file.trunk_path), { modal: true }, remove);
    if (answer === remove) {
      await this.runner.run(t("remove {0}", node.name), ["file", "remove", node.file.trunk_path]);
    }
  }

  /** Fichier ou répertoire du clone, dans le dossier « git · … » de l'espace s'il y est, sinon dans
   *  le Finder / gestionnaire de fichiers. */
  private async revealInClone(node?: Node): Promise<void> {
    let target: string | undefined;
    if (node?.kind === "file") {
      target = node.file.clone_path;
    } else if (node?.kind === "dir") {
      target = this.status(node.group.key) && path.join(this.status(node.group.key)!.stem, ...node.dir.path.split("/"));
    } else if (node?.kind === "scion") {
      target = this.status(node.group.key)?.stem;
    } else if (node?.kind === "status") {
      target = node.scion.stem;
    }
    if (!target) {
      return;
    }
    const uri = vscode.Uri.file(target);
    if (vscode.workspace.getWorkspaceFolder(uri)) {
      await vscode.commands.executeCommand("revealInExplorer", uri);
    } else {
      await vscode.commands.executeCommand("revealFileInOS", uri);
    }
  }
}
