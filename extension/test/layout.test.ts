// Vue IDE-1 (F6) : répertoires compactés et résumé git des greffons.
import * as assert from "node:assert/strict";
import { test } from "node:test";
import { DirNode, buildDirs, gitSummary } from "../src/layout";

const shape = (d: DirNode<string>): unknown =>
  ({ [d.label]: [...d.dirs.map(shape), ...d.files.map((f) => f.name)] });

test("répertoires : chaînes sans fichier compactées, tri, chemin complet conservé", () => {
  const root = buildDirs([
    "sys/root/src/kernel/core/b.c",
    "sys/root/src/kernel/core/a.c",
    "sys/root/src/kernel/core/arch/cortexm/start.c",
    "sys/root/src/lib/libc/libc.c",
    "top.c",
  ], (s) => s);
  assert.deepEqual(shape(root), {
    "": [
      { "sys/root/src": [
        { "kernel/core": [{ "arch/cortexm": ["start.c"] }, "a.c", "b.c"] },
        { "lib/libc": ["libc.c"] },
      ] },
      "top.c",
    ],
  });
  const kernel = root.dirs[0].dirs[0];
  assert.equal(kernel.path, "sys/root/src/kernel/core");
  assert.equal(kernel.dirs[0].path, "sys/root/src/kernel/core/arch/cortexm");
  assert.equal(kernel.files[0].item, "sys/root/src/kernel/core/a.c");
});

test("résumé git : branche, commit, fichiers modifiés ; vide sans commit", () => {
  assert.equal(gitSummary({ branch: "master", commit: "1dde0af", dirty: 0 }), "master 1dde0af");
  assert.equal(gitSummary({ branch: null, commit: "1dde0af", dirty: 2 }), "HEAD 1dde0af ●2");
  assert.equal(gitSummary({ branch: null, commit: null, dirty: null }), "");
});
