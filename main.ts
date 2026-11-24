// news-image-20261124 — entrypoint.
// Copies the pre-rendered entry.png (drawn by draw.py) into the
// make.fun output directory. Node 22 standard library only, no network.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png missing next to main.ts");
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log("entry.png written to", join(outDir, "entry.png"));
