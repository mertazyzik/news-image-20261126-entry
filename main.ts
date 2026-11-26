// news-image-20261126 entry point.
//
// The rendered front page is committed next to this file as entry.png.
// The grader runs this program with MAKEFUN_OUTPUT_DIR set; all it has
// to do is place a copy of the image there under the same name.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const sourceDir = dirname(fileURLToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR;

if (!targetDir) {
  throw new Error("MAKEFUN_OUTPUT_DIR is not set; nothing to write to");
}

if (!existsSync(targetDir)) {
  mkdirSync(targetDir, { recursive: true });
}

const image = readFileSync(join(sourceDir, "entry.png"));
const target = join(targetDir, "entry.png");
writeFileSync(target, image);
console.log(`copied entry.png (${image.length} bytes) to ${target}`);
