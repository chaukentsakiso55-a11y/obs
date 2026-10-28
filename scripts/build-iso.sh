#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p out
# Clean up old build leftovers before making a fresh ISO.
lb clean --purge || true
# Debian packages need Debian mirrors. No mixing Ubuntu and Bookworm.
lb config --distribution bookworm --architectures amd64 --binary-images iso-hybrid --archive-areas "main contrib non-free-firmware" --debian-installer none --bootappend-live "boot=live components quiet splash" --mirror-bootstrap "https://deb.debian.org/debian/" --mirror-chroot "https://deb.debian.org/debian/" --mirror-binary "https://deb.debian.org/debian/"
# Build the real live image.
lb build
ISO="$(find . -maxdepth 1 -type f -name '*.hybrid.iso' -print -quit)"
test -n "$ISO"
cp "$ISO" out/obsidian-os-amd64.iso
sha256sum out/obsidian-os-amd64.iso > out/SHA256SUMS
echo "Created out/obsidian-os-amd64.iso"
