#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p out
# Clean old build bits so yesterday's files don't mess with today's ISO.
lb clean --purge || true
lb config --distribution bookworm --architectures amd64 --binary-images iso-hybrid --archive-areas "main contrib non-free-firmware" --debian-installer none --bootappend-live "boot=live components quiet splash"
# This is the real Linux live image build, not a fake progress bar.
lb build
ISO="$(find . -maxdepth 1 -type f -name '*.hybrid.iso' -print -quit)"
test -n "$ISO"
cp "$ISO" out/obsidian-os-amd64.iso
sha256sum out/obsidian-os-amd64.iso > out/SHA256SUMS
echo "Created out/obsidian-os-amd64.iso"
