// Complétude du bilinguisme (décision du 2026-10-20) : toute chaîne traduisible des sources et toute
// clé de package.nls.json a sa traduction française, sans traduction orpheline.
import * as assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

const root = join(__dirname, "..", "..");            // out/test → extension/
const read = (rel: string) => readFileSync(join(root, rel), "utf8");
const json = (rel: string) => JSON.parse(read(rel)) as Record<string, string>;

/** Chaînes passées à t("…") ou vscode.l10n.t("…") (toujours entre guillemets doubles). */
function sourceStrings(): Set<string> {
  const found = new Set<string>();
  for (const f of readdirSync(join(root, "src")).filter((n) => n.endsWith(".ts"))) {
    for (const m of read(join("src", f)).matchAll(/\bt\(\s*"((?:[^"\\]|\\.)*)"/g)) {
      found.add(JSON.parse(`"${m[1]}"`));
    }
  }
  return found;
}

test("chaînes du code : traduites en français, aucune traduction orpheline", () => {
  const strings = sourceStrings();
  const bundle = json("l10n/bundle.l10n.fr.json");
  assert.ok(strings.size > 20);
  assert.deepEqual([...strings].filter((s) => !(s in bundle)), []);
  assert.deepEqual(Object.keys(bundle).filter((k) => !strings.has(k)), []);
  for (const [en, fr] of Object.entries(bundle)) {
    const args = (s: string) => (s.match(/\{\d+\}/g) ?? []).sort().join();
    assert.equal(args(fr), args(en), `arguments de « ${en} »`);
  }
});

test("package.json : toute clé %…% définie en anglais et en français", () => {
  const used = new Set([...read("package.json").matchAll(/"%([^%"]+)%"/g)].map((m) => m[1]));
  const en = json("package.nls.json");
  const fr = json("package.nls.fr.json");
  assert.deepEqual([...used].filter((k) => !(k in en)), []);
  assert.deepEqual(Object.keys(en).filter((k) => !used.has(k)), []);
  assert.deepEqual(Object.keys(fr).sort(), Object.keys(en).sort());
});
