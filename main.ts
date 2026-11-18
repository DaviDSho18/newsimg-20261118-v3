import * as crypto from "node:crypto";
import * as fs from "node:fs";
import * as path from "node:path";
import * as process from "node:process";
import { fileURLToPath } from "node:url";

function getFileSha256(filePath: string): string {
  const content = fs.readFileSync(filePath);
  return crypto.createHash("sha256").update(content).digest("hex");
}

// Determine module and file paths
const moduleDir = path.dirname(fileURLToPath(import.meta.url));
const imageFileName = "entry.png";
const sourceFilePath = path.join(moduleDir, imageFileName);

// Validate source entry existence
if (!fs.existsSync(sourceFilePath)) {
  console.error(`Source image missing: ${sourceFilePath}`);
  process.exit(1);
}

// Determine destination directory and path
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destinationFilePath = path.join(outputDirectory, imageFileName);

// Create destination directory if missing
if (!fs.existsSync(outputDirectory)) {
  fs.mkdirSync(outputDirectory, { recursive: true });
}

// Copy competition entry image
fs.copyFileSync(sourceFilePath, destinationFilePath);

// Distinct verification step: confirm file integrity and match
if (!fs.existsSync(destinationFilePath)) {
  console.error(`Verification failed: destination file missing at ${destinationFilePath}`);
  process.exit(1);
}

const sourceSize = fs.statSync(sourceFilePath).size;
const destSize = fs.statSync(destinationFilePath).size;

if (sourceSize !== destSize) {
  console.error(
    `Verification failed: size mismatch (source: ${sourceSize} bytes, destination: ${destSize} bytes)`
  );
  process.exit(1);
}

const sourceDigest = getFileSha256(sourceFilePath);
const destDigest = getFileSha256(destinationFilePath);

if (sourceDigest !== destDigest) {
  console.error(
    `Verification failed: SHA-256 mismatch!\n  Source: ${sourceDigest}\n  Dest:   ${destDigest}`
  );
  process.exit(1);
}

console.log(
  `Delivery verified successfully:\n` +
    `  Destination: ${destinationFilePath}\n` +
    `  Size:        ${destSize} bytes\n` +
    `  SHA-256:     ${destDigest}`
);
