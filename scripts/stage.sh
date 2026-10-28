#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$ROOT/config/includes.chroot/opt/obsidian-source"
cp -a "$ROOT/obsidian" "$ROOT/tools" "$ROOT/config/includes.chroot/opt/obsidian-source/"
