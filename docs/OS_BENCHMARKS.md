# OBSIDIAN OS — comparative engineering benchmarks

Sources:
- KDE Plasma desktop: https://github.com/KDE/plasma-desktop
- KDE Plasma official: https://kde.org/plasma-desktop/
- Fedora Workstation: https://fedoraproject.org/workstation/
- Fedora KDE: https://fedoraproject.org/en/kde/
- NixOS: https://nixos.org/guides/how-nix-works/

| Capability | Mature Linux desktops | OBSIDIAN current | Acceptance test |
|---|---|---|---|
| Boot on common PCs | Distribution-supported hardware | ISO workflow only | UEFI and BIOS QEMU boots + physical tests |
| Windows/workspaces | Mature window manager | XFCE underneath; Qt shell tabbed | Independently movable, resizable windows |
| App installation | Distribution packages, Flatpak | .obs build/inspect prototype | Signed install/uninstall/update with rollback |
| Desktop accessibility | Screen readers, keyboard navigation | Qt defaults, unreviewed | Keyboard-only and screen-reader audit |
| Reliable upgrades | Package updates; NixOS generations | No atomic updates | Interrupted update recovery test |
| Security | App sandboxing, permissions, logs | EDEN stub | Independent telemetry and audited controls |
| Developer tools | Python, C/C++, Rust, JS | Package list includes compilers | Compile and execute hello-world examples |
| Recovery | Varies by distro | Live boot only | Installer, encrypted install and rescue tests |
| Visual identity | Native desktop themes | Neon Qt starter | Screen-by-screen screenshot comparisons |

## Priorities
P0: fix ISO build, boot in QEMU, basic login, network, disk, terminal, desktop.
P1: make native window behavior and apps real; complete .obs package specification and trust model.
P2: EDEN local inference (resource-aware) and deterministic security integrations.
P3: transactional updates, rollback, installer, encrypted storage, accessibility.
P4: enterprise identity/finance connectors with least privilege, evidence handling, and human review.

Do not call OBSIDIAN better than other operating systems until it has comparable independent performance, compatibility, accessibility and security test results.
