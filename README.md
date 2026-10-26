# Discodo Launcher

<div align="center">

**Python desktop launcher · searchable library with 5,000+ Steam entries**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776ab?logo=python&logoColor=white)](https://python.org)
[![CI](https://github.com/Torfelka/Discodo_Launcher/actions/workflows/ci.yml/badge.svg)](https://github.com/Torfelka/Discodo_Launcher/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-6c75d9)](#requirements)

</div>

Discodo Launcher is an open-source desktop library for finding PC games, saving each game's real executable, and launching it from one dark, searchable interface. It fetches Steam's public app catalog on first run and caches it locally, providing far more than 5,000 entries without bundling a huge static JSON file.

## Features
- **Thousands of catalog entries** — Steam's public app list contains far more than 5,000 entries; no API key is required.
- **Popular games with cover art** — curated featured titles have descriptions and on-demand Steam CDN covers.
- **No covers for the long tail** — less prominent entries remain lightweight text rows.
- **Dark desktop UI** — search, popular/installed filters, details, favorites, and a game-folder shortcut.
- **Saved settings** — executable paths, language, and favorites persist locally.
- **Offline cache** — the last catalog remains available if Steam cannot be reached.
- **15 interface languages** — English, Russian, German, French, Spanish, Italian, Chinese, Japanese, Korean, Brazilian Portuguese, Polish, Turkish, Kazakh, Czech, and Ukrainian.
- **Python tests and cross-platform CI**.

> Steam's public endpoint lists Steam apps, not only games; it can include tools, demos, soundtracks, and other app types. Discord Rich Presence and Steam shortcut writing are not implemented. Discodo launches the real executable selected by the user and does not spoof another game's identity or bypass Discord Quests.

## Quick start

### Requirements
- Python **3.10+**
- Tkinter (included with most Windows Python installations; on Ubuntu/Debian install `python3-tk`)
- Internet for the initial catalog download
- Pillow for cover images

### Windows
1. Install Python from [python.org](https://www.python.org/downloads/) and enable **Add Python to PATH**.
2. Download this repository using **Code → Download ZIP**, extract it, or clone it:

   ```powershell
   git clone https://github.com/Torfelka/Discodo_Launcher.git
   cd Discodo_Launcher
   ```

3. Install and run:

   ```powershell
   py -m pip install -r requirements.txt
   py app.py
   ```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pip git
git clone https://github.com/Torfelka/Discodo_Launcher.git
cd Discodo_Launcher
python3 -m pip install -r requirements.txt
python3 app.py
```

### macOS
Install Python 3 from [python.org](https://www.python.org/downloads/), then:

```bash
git clone https://github.com/Torfelka/Discodo_Launcher.git
cd Discodo_Launcher
python3 -m pip install -r requirements.txt
python3 app.py
```

### First launch
1. The app opens and displays any cached catalog.
2. Steam's public app list downloads in the background; the counter updates when ready.
3. Search by title or App ID. **Popular** shows featured titles; **Installed** shows entries with a saved executable path.
4. Select a title, click **Browse…**, and choose its actual installed executable.
5. Click **PLAY GAME**. The path is saved for next time.

Featured covers download only when a featured game is selected and are cached locally. Other catalog entries intentionally have no cover.

## Data and privacy
- Catalog: Steam public endpoint `ISteamApps/GetAppList/v2/`.
- Covers: Steam's CDN using the app ID.
- Settings and cache are stored under `%LOCALAPPDATA%\DiscodoLauncher` on Windows or the user's cache/home directory on other systems.
- No Steam or Discord login is requested.

## Tests
```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py catalog.py launcher.py tests
```

## Project structure
```text
Discodo_Launcher/
├── app.py
├── catalog.py
├── launcher.py
├── requirements.txt
├── data/popular_games.json
├── data/locales/
├── tests/test_catalog.py
└── .github/workflows/ci.yml
```

## Roadmap
- [x] Replace Rust with Python
- [x] Searchable 5,000+ Steam app catalog and local cache
- [x] Featured games with on-demand cover art
- [x] Persist paths, favorites, and language
- [x] Python CI and unit tests
- [ ] Detect installed Steam games automatically
- [ ] Optional Rich Presence using a user-owned Discord application
- [ ] Safe Steam shortcut export with validation and backup
- [ ] Packaged Windows release

## Contributing
Issues and pull requests are welcome. Please run the unit tests and include reproduction steps.

## License
MIT — see [LICENSE](LICENSE).

<div align="center">Made by **Torfelka** · Python · Open source</div>
