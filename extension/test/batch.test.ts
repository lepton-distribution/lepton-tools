// Tests du regroupement d'événements, de la file d'exécution et de la lecture des arguments de clangd.
import * as assert from "node:assert/strict";
import { test } from "node:test";
import { Batcher, SerialQueue, compileCommandsDir } from "../src/batch";

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
