#!/usr/bin/env bash
set -euo pipefail
ISO="${1:-out/obsidian-os-amd64.iso}"
test -s "$ISO" || { echo "Missing ISO: $ISO" >&2; exit 1; }
command -v qemu-system-x86_64 >/dev/null || { echo "qemu-system-x86_64 required" >&2; exit 1; }
mkdir -p out
# Serial console availability varies by live image; capture firmware and kernel output for inspection.
timeout 150s qemu-system-x86_64 \
  -m 2048 -smp 2 -cdrom "$ISO" -boot d \
  -display none -serial file:out/qemu-serial.log -monitor none \
  -no-reboot || status=$?
status="${status:-0}"
if [ "$status" != 124 ] && [ "$status" != 0 ]; then
  echo "QEMU exited with status $status; inspect out/qemu-serial.log" >&2
  exit "$status"
fi
echo "QEMU ran. This is a boot smoke attempt, not proof of graphical login."
