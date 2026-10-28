# OBSIDIAN OS

Native Linux OS project with a neon-blue Qt desktop shell, EDEN interface, system applications, compilers and experimental `.obs` packages.

## Build bootable ISO
Use a Debian Linux machine with sudo:

```bash
sudo apt-get update
sudo apt-get install -y live-build debootstrap xorriso squashfs-tools
bash scripts/stage.sh
sudo bash scripts/build-iso.sh
```

Expected output on successful build: `out/obsidian-os-amd64.iso`. The GitHub Actions workflow also attempts this build and uploads the ISO artifact on success.

## Run the native desktop shell
```bash
sudo apt-get install -y python3-pyside6.qtwidgets python3-pyside6.qtcore python3-pyside6.qtgui
python3 obsidian/shell.py
```

## Experimental .obs SDK
```bash
python3 tools/obs.py init demo
python3 tools/obs.py build demo
python3 tools/obs.py inspect demo.obs
```

## Status
**Early native OS foundation, not a finished OS.** Debian live-build + XFCE session + native Qt OBSIDIAN shell. ISO build and boot have not been verified. EDEN currently has no AI inference model. Several app screens are placeholders. `.obs` packages are unsigned archives; there is no trusted installer or sandbox yet. Do not use for security-critical work.

Next: confirm ISO CI, boot-test in VM, add visual assets and real OS integrations, signed package management and security validation.
