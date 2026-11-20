// gta6-meme-x-01 entry program (Node 22, standard library only).
// The entry itself is the X post named in POST.json: the house reads
// the post from X, so this program's only job is to hand POST.json
// over unchanged. It copies POST.json from the repository root (the
// bot directory) into the output directory, creating that directory
// first, and exits non-zero with a message on stderr if the file
// cannot be read or written.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR || '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const source = join(botDir, 'POST.json');
const target = join(outputDir, 'POST.json');

// Fail early, before anything reaches the output directory, when
// POST.json is not a JSON object naming an X post: the gate refuses
// such an entry anyway, and a clear local error is easier to fix.
let post;
try {
  post = JSON.parse(readFileSync(source, 'utf8'));
} catch (error) {
  console.error('POST.json is not readable JSON: ' + error.message);
  process.exit(1);
}
const postUrl = /^https:\/\/(www\.|mobile\.)?(x\.com|twitter\.com)\/[^/]+\/status\/\d+/.test(post?.url ?? '');
if (!postUrl) {
  console.error('POST.json must name an X post: {"url": "https://x.com/<handle>/status/<id>"}');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(source, target);
} catch (error) {
  console.error('could not copy ' + source + ' to ' + target + ': ' + error.message);
  process.exit(1);
}
