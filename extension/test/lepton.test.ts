// Tests du point d'appel de lepton (node:test, sans l'éditeur) : un faux lepton en shell.
import * as assert from "node:assert/strict";
import { chmodSync, mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import { EXIT_FAILURE, EXIT_INTERRUPT, lastMessage, resolveLepton, runLepton } from "../src/lepton";

function fakeLepton(body: string): string {
  const dir = mkdtempSync(join(tmpdir(), "lepton-ext-"));
  const exe = join(dir, "lepton");
  writeFileSync(exe, `#!/bin/sh\n${body}\n`);
  chmodSync(exe, 0o755);
  return exe;
}

test("arguments, répertoire de travail et code de retour transmis", async () => {
  const exe = fakeLepton('echo "cwd=$(pwd -P) args=$*"; echo "lepton: erreur: refus" >&2; echo "  → faire autrement" >&2; exit 1');
  const cwd = mkdtempSync(join(tmpdir(), "lepton-cwd-"));
  let streamed = "";
  const r = await runLepton(exe, ["file", "add", "a b.c"], cwd, (t) => (streamed += t));
  assert.equal(r.code, 1);
  assert.match(r.stdout, /args=file add a b\.c/);
  assert.ok(r.stdout.includes("cwd=" + (await import("node:fs")).realpathSync(cwd)));
  assert.ok(streamed.includes("lepton: erreur: refus"));
  assert.equal(lastMessage(r), "lepton: erreur: refus → faire autrement");
});

test("exécutable absent : code 2 et message", async () => {
  const r = await runLepton("/nonexistent/lepton", ["check"], tmpdir());
  assert.equal(r.code, EXIT_FAILURE);
  assert.match(lastMessage(r), /lepton introuvable/);
});

test("annulation : SIGINT, code 130", async () => {
  const exe = fakeLepton("sleep 5");
  const abort = new AbortController();
  const pending = runLepton(exe, [], tmpdir(), undefined, abort.signal);
  setTimeout(() => abort.abort(), 100);
  assert.equal((await pending).code, EXIT_INTERRUPT);
});

test("résolution de l'exécutable", () => {
  const home = mkdtempSync(join(tmpdir(), "lepton-home-"));
  assert.equal(resolveLepton("/opt/lepton", home), "/opt/lepton");
  assert.equal(resolveLepton("", home), "lepton");
  mkdirSync(join(home, ".local", "bin"), { recursive: true });
  writeFileSync(join(home, ".local", "bin", "lepton"), "");
  assert.equal(resolveLepton("", home), join(home, ".local", "bin", "lepton"));
});
