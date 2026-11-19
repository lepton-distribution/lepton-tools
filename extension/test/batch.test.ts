// Tests du regroupement d'événements, de la file d'exécution et de la lecture des arguments de clangd.
import * as assert from "node:assert/strict";
import { test } from "node:test";
import {
  Batcher, SerialQueue, compileCommandsDir, databaseDirectories, deletedClones, isUnder, splitRoots,
} from "../src/batch";

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

test("événements regroupés et dédoublonnés, délai relancé à chaque ajout", async () => {
  const fired: string[][] = [];
  const b = new Batcher<string>(() => 50, (items) => void fired.push(items));
  b.add("a");
  await sleep(30);
  b.add("b");
  b.add("a");
  await sleep(30);
  assert.deepEqual(fired, []);                       // 60 ms après le premier, 30 après le dernier
  await sleep(40);
  assert.deepEqual(fired, [["a", "b"]]);
  b.add("c");
  await b.flush();                                   // livraison immédiate
  assert.deepEqual(fired, [["a", "b"], ["c"]]);
  b.add("d");
  b.dispose();
  await sleep(70);
  assert.equal(fired.length, 2);                     // abandonné
});

test("file : une tâche à la fois, dans l'ordre, malgré un échec", async () => {
  const q = new SerialQueue();
  const log: string[] = [];
  const task = (name: string, ms: number, fail = false) => () =>
    new Promise<string>((resolve, reject) => {
      log.push(`début ${name}`);
      setTimeout(() => {
        log.push(`fin ${name}`);
        fail ? reject(new Error(name)) : resolve(name);
      }, ms);
    });
  const a = q.run(task("a", 30));
  const b = q.run(task("b", 5, true));
  const c = q.run(task("c", 5));
  assert.equal(await a, "a");
  await assert.rejects(b, /b/);
  assert.equal(await c, "c");
  assert.deepEqual(log, ["début a", "fin a", "début b", "fin b", "début c", "fin c"]);
});

test("--compile-commands-dir lu dans clangd.arguments", () => {
  assert.equal(compileCommandsDir(["--compile-commands-dir=/r/build/.active", "--background-index"]),
    "/r/build/.active");
  assert.equal(compileCommandsDir(["--background-index", "--compile-commands-dir", "/r/b"]), "/r/b");
  assert.equal(compileCommandsDir(["--background-index"]), undefined);
  assert.equal(compileCommandsDir(["--compile-commands-dir="]), undefined);
  assert.equal(compileCommandsDir(undefined), undefined);
  assert.equal(compileCommandsDir("--compile-commands-dir=/x"), undefined);
});

test("répertoires de construction d'une base compile_commands.json", () => {
  const db = JSON.stringify([
    { directory: "/r/build/b", file: "x.c" }, { directory: "/r/build/a", file: "y.c" },
    { directory: "/r/build/b", file: "z.c" }, { file: "sans-répertoire.c" },
  ]);
  assert.deepEqual(databaseDirectories(db), ["/r/build/a", "/r/build/b"]);
  assert.deepEqual(databaseDirectories("{}"), []);
  assert.deepEqual(databaseDirectories("pas du JSON"), []);
});

// D24 (ENV-64, PA-115 (a′)) : la racine scion/ d'un clone créé ou supprimé en entier n'est pas regreffée.

test("D24 : lot en attente filtré (refresh : greffons qui ne sont plus observés)", async () => {
  const fired: string[][] = [];
  const b = new Batcher<string>(() => 30, (items) => void fired.push(items));
  b.add("/d/a/scion/x.c");
  b.add("/d/b/scion");
  b.retain((p) => isUnder(p, ["/d/a/scion"]));
  await b.flush();
  assert.deepEqual(fired, [["/d/a/scion/x.c"]]);
  b.add("/d/b/scion/y.c");
  b.retain(() => false);                             // lot vidé : rien n'est livré
  await new Promise((r) => setTimeout(r, 50));
  assert.equal(fired.length, 1);
});

test("D24 : chemin sous une racine (la racine elle-même comprise, pas un préfixe de nom)", () => {
  assert.equal(isUnder("/d/a/scion", ["/d/a/scion"]), true);
  assert.equal(isUnder("/d/a/scion/sys/x.c", ["/d/b/scion", "/d/a/scion"]), true);
  assert.equal(isUnder("/d/a/scion2/x.c", ["/d/a/scion"]), false);
  assert.equal(isUnder("/d/a", ["/d/a/scion"]), false);
  assert.equal(isUnder("/d/a/scion", []), false);
});

test("D24 : racines séparées des autres chemins (racines de tous les greffons observés jusqu'ici)", () => {
  const roots = new Set(["/d/a/scion", "/d/b/scion"]);
  assert.deepEqual(splitRoots(["/d/a/scion", "/d/a/scion/x.c", "/d/c/scion", "/d/b/scion"], roots),
    { roots: ["/d/a/scion", "/d/b/scion"], others: ["/d/a/scion/x.c", "/d/c/scion"] });
  assert.deepEqual(splitRoots(["/d/a/scion/x.c"], roots), { roots: [], others: ["/d/a/scion/x.c"] });
});

test("D24 : clone supprimé hors de lepton = racine absente d'un greffon encore greffé", () => {
  const grafted = [{ stem: "/d/a/scion", name: "a" }, { stem: "/d/b/scion", name: "b" }];
  const present = new Set(["/d/b/scion"]);
  const exists = (p: string) => present.has(p);
  // a : absente et greffée (clone supprimé à la main) ; b : présente (seed replace, clone recréé) ;
  // c : absente, non greffée (seed remove --purge, graft-remove --purge)
  assert.deepEqual(deletedClones(["/d/a/scion", "/d/b/scion", "/d/c/scion"], exists, grafted), ["a"]);
  assert.deepEqual(deletedClones(["/d/c/scion"], exists, grafted), []);
  assert.deepEqual(deletedClones(["/d/a/scion"], exists, []), []);
});
