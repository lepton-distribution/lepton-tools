// F8 : correspondance clone → trunk des sources de l'adaptateur de débogage.
import * as assert from "node:assert/strict";
import { test } from "node:test";
import { rewriteSources, sourceMap, toTrunk } from "../src/srcmap";

const map = sourceMap("/r/trunk", ["/r/depots/a/master/scion", "", "/r/depots/a/master/scion-x/scion"]);
const grafted = new Set(["/r/trunk/sys/b.c", "/r/trunk/k/c.c"]);
const exists = (p: string) => grafted.has(p);

test("chemin du clone ramené au lien du trunk, s'il existe", () => {
  assert.equal(toTrunk(map, "/r/depots/a/master/scion/sys/b.c", exists), "/r/trunk/sys/b.c");
  assert.equal(toTrunk(map, "/r/depots/a/master/scion-x/scion/k/c.c", exists), "/r/trunk/k/c.c");
  assert.equal(toTrunk(map, "/r/depots/a/master/scion/sys/absent.c", exists), "/r/depots/a/master/scion/sys/absent.c");
  assert.equal(toTrunk(map, "/opt/gcc/include/stdio.h", exists), "/opt/gcc/include/stdio.h");
  assert.equal(toTrunk(map, "/r/depots/a/master/scionX/sys/b.c", exists), "/r/depots/a/master/scionX/sys/b.c");
});

test("message DAP : source et sources réécrits, le reste intact", () => {
  const msg = {
    type: "response", command: "stackTrace",
    body: {
      stackFrames: [
        { id: 1, name: "main", line: 48, source: { name: "b.c", path: "/r/depots/a/master/scion/sys/b.c" } },
        { id: 2, name: "??", line: 0 },
        { id: 3, name: "f", line: 1, source: { name: "x.S", sourceReference: 7 } },
      ],
      sources: [{ path: "/r/depots/a/master/scion-x/scion/k/c.c" }],
      path: "/r/depots/a/master/scion/sys/b.c",
    },
  };
  rewriteSources(msg, (p) => toTrunk(map, p, exists));
  assert.equal(msg.body.stackFrames[0].source?.path, "/r/trunk/sys/b.c");
  assert.deepEqual(msg.body.stackFrames[2].source, { name: "x.S", sourceReference: 7 });
  assert.equal(msg.body.sources[0].path, "/r/trunk/k/c.c");
  assert.equal(msg.body.path, "/r/depots/a/master/scion/sys/b.c");     // hors d'un objet source
});
