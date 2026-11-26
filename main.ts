import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry point: copy the rendered front page into the grader's output dir.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR;
if (!outDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set");
}
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");
copyFileSync(src, dst);
console.log("wrote entry.png to " + outDir);
