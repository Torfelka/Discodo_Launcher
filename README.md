<div align="center">

# Discodo Launcher

**A lightweight desktop game library built with Rust.**

Search your collection, choose each game's executable, and launch it from one clean interface.

[![Rust](https://img.shields.io/badge/Rust-2024_edition-b7410e?logo=rust&logoColor=white)](https://www.rust-lang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-6c75d9)](#requirements)
[![Games](https://img.shields.io/badge/Game_catalog-50-2c9b72)](data/games.json)

[**Features**](#features) · [**Quick start**](#quick-start) · [**Build**](#build-from-source) · [**Roadmap**](#roadmap) · [**Contributing**](#contributing)

</div>

---

## Overview

Discodo Launcher is an open-source Rust desktop application for keeping a searchable list of PC games and starting the real executable you choose for each entry. The catalog ships with 50 popular games and can be extended through `data/games.json`.

> **Transparency first:** Discodo launches the executable selected by the user. It does not pretend to be another game's process, spoof another application's Discord identity, or bypass Discord Quests. Discord Rich Presence and Steam shortcut export are future integrations, not features that are already working.

## Features

- **Native desktop UI** powered by [egui](https://github.com/emilk/egui) and [eframe](https://github.com/emilk/egui).
- **50-game starter catalog** with genres, descriptions, executable hints, Steam App IDs where applicable, and color-coded cover placeholders.
- **Search** by game title or genre.
- **Choose an executable** using a native file picker for each game.
- **Launch real programs** with their parent directory set as the working directory.
- **Localization files** for 15 languages.
- **Cross-platform CI workflow** configured for Windows, Linux, and macOS.
- **MIT license** and a small, approachable Rust codebase.

## Preview

The current UI uses a dark theme, a searchable library sidebar, a selected-game detail panel, executable selection, and a status bar. The colored game tiles are placeholders; real cover-art loading is not implemented yet.

## Quick start

### 1. Install Rust

Install the stable Rust toolchain from [rustup.rs](https://rustup.rs/). This project uses **Rust edition 2024**, so use a recent stable Rust release.

After installation, open a new terminal and verify:

```powershell
rustc --version
cargo --version
```

### 2. Download the repository

Option A — with Git:

```bash
git clone https://github.com/Torfelka/Discodo_Launcher.git
cd Discodo_Launcher
```

Option B — without Git: open the repository page, choose **Code → Download ZIP**, extract it, then open a terminal in the extracted `Discodo_Launcher` folder.

### 3. Run the app

From the repository root:

```bash
cargo run
```

The first build downloads Rust dependencies, so it may take a few minutes. When the app opens, select a game, click **Choose EXE…**, browse to that game's actual executable, and press **Play**.

### Windows notes

- Install the **Visual Studio Build Tools** with the **Desktop development with C++** workload if Rust reports missing MSVC linker or Windows SDK components.
- Use PowerShell or Windows Terminal in the project directory.
- Build output appears at `target\debug\discodo_launcher.exe`.

### Linux notes

A C/C++ compiler and GUI development libraries may be needed by eframe's windowing backend. On Ubuntu/Debian, a starting point is:

```bash
sudo apt update
sudo apt install build-essential pkg-config libxkbcommon-dev libwayland-dev libx11-dev libxcb1-dev libgl1-mesa-dev
```

Then run `cargo run` again. Package names vary by distribution and desktop environment.

### macOS notes

Install Xcode Command Line Tools if needed:

```bash
xcode-select --install
```

Then run `cargo run` from the project directory.

## Build from source

Debug build:

```bash
cargo build
```

Optimized release build:

```bash
cargo build --release
```

Run the catalog tests:

```bash
cargo test
```

The release binary is written under `target/release/` (the exact executable suffix depends on the operating system).

## Adding a game

Edit `data/games.json` and add an object following this shape:

```json
{
  "id": "my-game",
  "name": "My Game",
  "genre": "Adventure",
  "description": "A short description of the game.",
  "executable_hint": "MyGame.exe",
  "steam_app_id": null,
  "cover_color": [85, 110, 160]
}
```

Keep `id` unique, use `null` when a Steam App ID is not applicable or verified, and treat `executable_hint` as a hint only. The user still selects the actual file installed on their machine.

## Localization

Translation data files are in `data/locales/`:

| Locale | File |
|---|---|
| English | `en.json` |
| Russian | `ru.json` |
| German | `de.json` |
| French | `fr.json` |
| Spanish | `es.json` |
| Italian | `it.json` |
| Chinese | `zh.json` |
| Japanese | `ja.json` |
| Korean | `ko.json` |
| Brazilian Portuguese | `pt-BR.json` |
| Polish | `pl.json` |
| Turkish | `tr.json` |
| Kazakh | `kk.json` |
| Czech | `cs.json` |
| Ukrainian | `uk.json` |

**Current limitation:** these translation packs are present in the repository, but the runtime UI currently only has a basic English/Russian selector and does not yet load all locale JSON files. Full localization wiring is on the roadmap.

## Integrations and limitations

| Area | Status |
|---|---|
| Searchable game library | Implemented |
| Select and launch real executable | Implemented |
| 50-game catalog | Implemented |
| English/Russian basic UI toggle | Partial |
| 15 locale data packs | Added; not fully wired into UI |
| Persistent executable-path settings | Not implemented yet |
| Discord Rich Presence using your own application | Planned |
| Steam non-Steam shortcut export | Planned; Steam files are not modified |
| Real cover art and cover cache | Planned |
| Prebuilt release downloads | Not published yet |

Do not enter a Discord Client ID expecting Rich Presence to work in this version: the connection and settings screen have not been implemented yet.

## Roadmap

- [x] Native Rust desktop shell
- [x] Searchable game catalog with 50 entries
- [x] Per-game executable selection and launch
- [x] Catalog integrity tests
- [x] 15 translation JSON packs
- [x] GitHub Actions build-check workflow
- [ ] Load and apply all locale files at runtime
- [ ] Persist selected executable paths and settings
- [ ] Long-lived Discord Rich Presence using a user-owned application
- [ ] Safe Steam shortcut export with backup, deduplication, and validation
- [ ] Real cover art and local image cache
- [ ] Tagged releases and downloadable builds

## Contributing

Issues and pull requests are welcome. Before submitting a change, run:

```bash
cargo fmt --check
cargo test
cargo check --all-targets
```

For catalog changes, verify IDs and executable hints and avoid inventing unverified Steam App IDs. Please describe platform-specific behavior and include reproduction steps for bug reports.

## License

Discodo Launcher is distributed under the [MIT License](LICENSE).

---

<div align="center">

Made by **Torfelka** · Open source · Rust

</div>
