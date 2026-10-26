# Discodo_Launcher

Open-source desktop game library and launcher written in Rust.

> Discodo launches the real executable selected by the user. Discord Rich Presence is an optional, transparent integration using an application ID you control; it does not impersonate another game's Discord application or bypass Discord Quests.

## Features

- Native dark desktop UI built with egui/eframe.
- Searchable catalog of popular PC games.
- Per-game executable selection and validation.
- Launch real games with their working directory set correctly.
- Optional Discord Rich Presence for your own Discord application.
- Steam integration planned as a safe, opt-in shortcut exporter with backups.
- Translation data packs for 15 locales: English, Russian, German, French, Spanish, Italian, Chinese, Japanese, Korean, Brazilian Portuguese, Polish, Turkish, Kazakh, Czech, and Ukrainian. The current visible selector is wired for English/Russian; full runtime locale switching remains unfinished.
- Portable JSON catalog and user settings.
- MIT licensed.

## Requirements

- Rust stable (edition 2024)
- Windows 10/11, Linux, or macOS (platform integration varies)
- Discord desktop client for Rich Presence

## Run

```bash
cargo run
```

## Build release

```bash
cargo build --release
```

## Configuration

On first launch, select a game's actual executable from the details panel. The launcher does not guess installation paths or replace another process's identity.

To enable Rich Presence, configure your own Discord application's Client ID in Settings. Availability depends on Discord's local IPC and application configuration.

## Roadmap

- [x] Native UI and searchable game catalog
- [x] Launch real executables
- [x] Per-game executable picker
- [x] English/Russian UI
- [ ] Persist user preferences between launches
- [ ] Long-lived Discord Rich Presence connection
- [ ] Steam shortcut export with automatic backup and validation
- [ ] Cover art manager and local cache
- [x] Translation JSON packs for 15 locales (runtime UI wiring still in progress)
- [ ] Full runtime switching across all 15 locales
- [ ] More accessibility options
- [ ] CI build checks for Windows, Linux, and macOS

## License

MIT — see [LICENSE](LICENSE).
