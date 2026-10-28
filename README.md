# OBSIDIAN OS 🐺

**Your PC. Your rules. Your privacy.**

OBSIDIAN OS is Cyber Pulse's vision for a futuristic, privacy-first Linux operating system. We're building a real bootable desktop OS, not just a website that looks like one.

Think dark neon-blue vibes, actual Linux apps, built-in coding tools, and **EDEN** — the AI assistant designed to help you understand your system, code, and security alerts without handing over all your data.

## What's the vibe?
- **Neon desktop:** Dark, futuristic UI built with Qt over a Linux desktop session. We're still matching the original screen references.
- **EDEN AI:** A local-first assistant that can connect to an Ollama model on your own machine. No model downloaded? EDEN tells you instead of pretending.
- **Security first:** Local permission checks and policy decisions. AI explains events; trusted code enforces rules.
- **Developer-ready:** Python, C/C++, Node.js and Rust are included in the ISO package configuration.
- **.obs apps:** A custom experimental app package format. The SDK can create, build and inspect packages, but secure installation and signing aren't ready.
- **Built-in apps:** File Manager, Terminal, Settings, Network, System Monitor, EDEN, Developer Studio and more. Some screens are still works in progress.

## Get the code running

### Build the bootable Linux ISO
Use a Debian-compatible Linux build environment with enough free disk space:

```bash
sudo apt-get update
sudo apt-get install -y live-build debootstrap xorriso squashfs-tools
bash scripts/stage.sh
sudo bash scripts/build-iso.sh
```

If the build works, you'll get `out/obsidian-os-amd64.iso`. You can also check **Actions** for the automated ISO workflow. Don't flash this onto your main computer until it passes VM and hardware tests.

### Launch the native desktop shell
```bash
sudo apt-get install -y python3-pyside6.qtwidgets python3-pyside6.qtcore python3-pyside6.qtgui
python3 obsidian/shell.py
```

### Make your first .obs package
```bash
python3 tools/obs.py init myapp
python3 tools/obs.py build myapp
python3 tools/obs.py inspect myapp.obs
```

### Run the checks
```bash
python3 -m compileall -q obsidian tools
python3 -m unittest discover -s tests -v
```

## Real status — no fake flex
**OBSIDIAN is under active development.** The repository has a Linux ISO build pipeline, native Qt shell, EDEN local-model client, defensive security utilities, package SDK and tests. A successful boot, complete visual match, full installer, signed .obs installation, production-grade cybersecurity and full EDEN model are **not yet verified or complete**.

**Roadmap:** Bootable VM → native UI matching the reference screens → real app integrations → secure .obs installation → EDEN tools and local AI → installer, updates, rollback, hardware tests.

Built for **Cyber Pulse**. *Build Beyond the Idea.*
