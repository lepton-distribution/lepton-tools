#!/usr/bin/env node
// ENV-64, D23 : effet du réglage `lepton.path` sur resolveLepton et runLepton, hors de l'éditeur.
// Usage : node d23.cjs <extension/out/src/lepton.js> [<répertoire de travail>]
// Chaque ligne : forme, valeur du réglage, exécutable résolu, code de `lepton --version`, première
// ligne de sortie (stdout, sinon stderr). $HOME est remplacé par <HOME>, l'utilisateur par <U>.
// Le message d'exécutable absent est celui de runLepton par défaut (anglais) ; dans l'éditeur, il
// est traduit (« lepton introuvable : … (réglage lepton.path) »).
"use strict";
const { homedir, userInfo, tmpdir } = require("node:os");
const { mkdtempSync, realpathSync } = require("node:fs");
const { join, relative, resolve } = require("node:path");

const [modulePath, cwdArg] = process.argv.slice(2);
if (!modulePath) {
  console.error("usage : node d23.cjs <extension/out/src/lepton.js> [<cwd>]");
  process.exit(2);
}
const { resolveLepton, runLepton } = require(resolve(modulePath));
const home = homedir();
const user = userInfo().username;
const cwd = cwdArg ? resolve(cwdArg) : realpathSync(mkdtempSync(join(tmpdir(), "d23-")));
const pipx = join(home, ".local", "bin", "lepton");

const forms = [
  ["vide", ""],
  ["absolu", pipx],
  ["tilde", "~/.local/bin/lepton"],
  ["tilde-utilisateur", `~${user}/.local/bin/lepton`],
  ["tilde-inconnu", "~inconnu64/.local/bin/lepton"],
  ["tilde-seul", "~"],
  ["userHome", "${userHome}/.local/bin/lepton"],
  ["env-HOME", "$HOME/.local/bin/lepton"],
  ["relatif-cwd", relative(cwd, pipx)],
  ["relatif-point", "./lepton"],
  ["nom-nu", "lepton"],
];

const norm = (s) => s.split(home).join("<HOME>").split(user).join("<U>").split(cwd).join("<CWD>");

(async () => {
  console.log(["forme", "réglage", "résolu", "code", "sortie"].join("\t"));
  for (const [name, value] of forms) {
    const exe = resolveLepton(value);
    const r = await runLepton(exe, ["--version"], cwd);
    const first = (r.stdout.trim() || r.stderr.trim()).split("\n")[0];
    console.log([name, norm(value), norm(exe), r.code, norm(first)].join("\t"));
  }
})();
