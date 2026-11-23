import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for news-image-20261123: copy the pre-rendered front page
// (drawn by draw.py from verified 23 November 2026 news) to the output
// directory. Standard library only, no network, fully deterministic:
// the same input bytes always produce the same output bytes.
// The program never writes to its own repository at run time.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
