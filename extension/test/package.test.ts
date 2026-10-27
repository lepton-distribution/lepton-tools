// Cohérence du paquet : commandes déclarées enregistrées par le code ; `.vsix` versionné de la version
// courante, seul dans dist/ (installé par scripts/install-vscodium.sh, décision du 2026-10-27).
import * as assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { test } from "node:test";

const root = join(__dirname, "..", "..");            // out/test → extension/
const pkg = JSON.parse(readFileSync(join(root, "package.json"), "utf8"));

test("toute commande de package.json est enregistrée dans src/", () => {
  const sources = readdirSync(join(root, "src")).filter((n) => n.endsWith(".ts"))
    .map((n) => readFileSync(join(root, "src", n), "utf8")).join("\n");
  const declared: string[] = pkg.contributes.commands.map((c: { command: string }) => c.command);
  assert.ok(declared.length > 20);
  assert.deepEqual(declared.filter((id) => !sources.includes(`"${id}"`)), []);
});

test("dist/ : un seul .vsix, celui de la version de package.json", () => {
  assert.deepEqual(readdirSync(join(root, "dist")).filter((n) => n.endsWith(".vsix")),
    [`${pkg.name}-${pkg.version}.vsix`]);
});
