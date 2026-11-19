// Tests du point d'appel de lepton (node:test, sans l'éditeur) : un faux lepton en shell.
import * as assert from "node:assert/strict";
import { chmodSync, mkdirSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir, userInfo } from "node:os";
import { join } from "node:path";
import { test } from "node:test";
import {
  EXIT_FAILURE, EXIT_INTERRUPT, diagnosticMessage, foreignHome, inputPath, lastMessage, parseJson, placeOf,
  resolveLepton, runLepton,
} from "../src/lepton";

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
  let errors = "";
  const r = await runLepton(exe, ["file", "add", "a b.c"], cwd, (t, stream) => {
    streamed += t;
    if (stream === "stderr") errors += t;
  });
  assert.equal(r.code, 1);
  assert.match(r.stdout, /args=file add a b\.c/);
  assert.ok(r.stdout.includes("cwd=" + (await import("node:fs")).realpathSync(cwd)));
  assert.ok(streamed.includes("lepton: erreur: refus") && streamed.includes("args=file add"));
  assert.ok(errors.includes("lepton: erreur: refus") && !errors.includes("args="));
  assert.equal(lastMessage(r), "lepton: erreur: refus → faire autrement");
});

test("exécutable absent : code 2 et message (mis en forme par l'appelant)", async () => {
  const r = await runLepton("/nonexistent/lepton", ["check"], tmpdir());
  assert.equal(r.code, EXIT_FAILURE);
  assert.match(lastMessage(r), /lepton not found: \/nonexistent\/lepton/);
  const fr = await runLepton("/nonexistent/lepton", [], tmpdir(), undefined, undefined, (e) => `introuvable ${e}`);
  assert.equal(lastMessage(fr), "introuvable /nonexistent/lepton");
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

test("D23 : lepton.path, `~`, `~<utilisateur courant>` et `${userHome}` développés", () => {
  const home = "/h/moi";
  const me = userInfo().username;
  assert.equal(resolveLepton("~/.local/bin/lepton", home), "/h/moi/.local/bin/lepton");
  assert.equal(resolveLepton(`~${me}/.local/bin/lepton`, home), "/h/moi/.local/bin/lepton");
  assert.equal(resolveLepton("${userHome}/.local/bin/lepton", home), "/h/moi/.local/bin/lepton");
  assert.equal(resolveLepton("~", home), "/h/moi");
  assert.equal(resolveLepton("${userHome}", home), "/h/moi");
  // laissés tels quels : autre compte (message précisé par l'appelant), $HOME, variable hors tête
  assert.equal(resolveLepton("~inconnu64/bin/lepton", home), "~inconnu64/bin/lepton");
  assert.equal(resolveLepton("$HOME/bin/lepton", home), "$HOME/bin/lepton");
  assert.equal(resolveLepton("/opt/${userHome}/lepton", home), "/opt/${userHome}/lepton");
  assert.equal(resolveLepton("${userHome}x/lepton", home), "${userHome}x/lepton");
  assert.equal(resolveLepton("lepton", home), "lepton");
});

test("D23 : `~<autre compte>` reconnu (message d'introuvable précisé)", () => {
  const me = userInfo().username;
  assert.equal(foreignHome("~inconnu64/bin/lepton"), true);
  assert.equal(foreignHome("~inconnu64"), true);
  assert.equal(foreignHome("~/bin/lepton"), false);
  assert.equal(foreignHome(`~${me}/bin/lepton`), false);
  assert.equal(foreignHome("/opt/~x/lepton"), false);
  assert.equal(foreignHome("lepton"), false);
});

test("D31 : chemin saisi ouvert comme lepton le lit (`~`, relatif au rootstock)", () => {
  const home = "/h/moi";
  const me = userInfo().username;
  assert.equal(inputPath("~/src/x.c", "/r", home), "/h/moi/src/x.c");
  assert.equal(inputPath(`~${me}/src/x.c`, "/r", home), "/h/moi/src/x.c");
  assert.equal(inputPath("trunk/x.c", "/r", home), "/r/trunk/x.c");
  assert.equal(inputPath("../autre/x.c", "/r/s", home), "/r/autre/x.c");
  assert.equal(inputPath("/abs/x.c", "/r", home), "/abs/x.c");
  // lepton ne développe pas ${userHome} dans un chemin : relatif, comme lui
  assert.equal(inputPath("${userHome}/x.c", "/r", home), "/r/${userHome}/x.c");
  // autre compte : dossier inconnu de Node, pas d'ouverture
  assert.equal(inputPath("~inconnu64/x.c", "/r", home), undefined);
});

test("JSON de lepton : lu, ou undefined", () => {
  assert.deepEqual(parseJson({ code: 0, stdout: '{"a": 1}\n', stderr: "" }), { a: 1 });
  assert.equal(parseJson({ code: 1, stdout: "texte", stderr: "" }), undefined);
});

test("entrée standard transmise (check --stdin)", async () => {
  const exe = fakeLepton('echo "args=$*"; cat');
  const r = await runLepton(exe, ["check", "--stdin", "lepton-graine.json"], tmpdir(), undefined, undefined,
    undefined, "{\n  \"é\": 1\n}");
  assert.equal(r.code, 0);
  assert.equal(r.stdout, 'args=check --stdin lepton-graine.json\n{\n  "é": 1\n}');
  const none = await runLepton(fakeLepton("cat; echo fin"), [], tmpdir());   // sans input : stdin fermée
  assert.equal(none.stdout, "fin\n");
});

test("portée d'une anomalie : situation de lepton, ligne entière, première ligne", () => {
  const a = { file: "f", location: "/bsp", message: "m" };
  assert.deepEqual(placeOf({ ...a, line: 11, column: 3, end_line: 11, end_column: 8 }),
    { line: 10, character: 2, endLine: 10, endCharacter: 7 });
  assert.deepEqual(placeOf({ ...a, line: 9, column: null, end_line: null, end_column: null }),
    { line: 8, character: 0, endLine: 8 });
  assert.deepEqual(placeOf(a), { line: 0, character: 0, endLine: 0 });
  assert.deepEqual(placeOf({ ...a, line: 2, column: 7 }), { line: 1, character: 6, endLine: 1, endCharacter: 7 });
});

test("texte d'un diagnostic : emplacement en tête, numéro de ligne de xmllint retiré si situé", () => {
  assert.equal(diagnosticMessage({ file: "f", location: "/projet", message: "champ non autorisé : x" }),
    "/projet: champ non autorisé : x");
  assert.equal(diagnosticMessage({ file: "f", location: "/", message: "champ obligatoire absent : noyau" }),
    "champ obligatoire absent : noyau");
  assert.equal(diagnosticMessage({ file: "f.xml", location: "", message: "9: Schemas validity error", line: 9 }),
    "Schemas validity error");
  assert.equal(diagnosticMessage({ file: "f.xml", location: "", message: "9: x" }), "9: x");
});

test("sortie JSON de check lue telle quelle", () => {
  const out = { files: ["g.json"], anomalies: [{ file: "g.json", location: "/", message: "m", line: 1, column: 1,
    end_line: 1, end_column: 2 }] };
  assert.deepEqual(parseJson({ code: 1, stdout: JSON.stringify(out), stderr: "" }), out);
});
