# Walkthrough - Rebrand to WebSpider 3D (WebSpider Studios)

The codebase has been rebranded from **Mixar** to **WebSpider 3D**, developed by **WebSpider Studios**. Every single reference in C++ source code, Python modules, build scripts, DNA/RNA structures, UI labels, icons, splash screens, documentation, and configuration files has been updated cleanly.

---

## Key Changes Made

### 1. Build System & Configuration
- **Script Settings**: Rebranded `scripts/unix/settings.sh` and `scripts/windows/settings.bat` with `WEBSPIDER_ENV`, `WEBSPIDER_BACKEND_URL`, `WEBSPIDER_APP_NAME="WebSpider 3D"`, `WEBSPIDER_VENDOR="WebSpider Studios"`, `WEBSPIDER_WEBSITE="https://webspider3d.com"`.
- **Config Generators**: Updated `scripts/generate_config.py` to output `webspider.json` with default endpoints (`https://api.webspider3d.com`, `https://www.webspider3d.com`).
- **Build Scripts**: Renamed generated configuration headers to `webspider_env_config.h` and Python environment marker to `src/scripts/webspider/config/_build_env.py`. Renamed `cmake/mixar_overrides.cmake` to `cmake/webspider_overrides.cmake`.
- **Root Environment & Makefile**: Updated [.env.example](file:///e:/WebSpider%203D/.env.example) and [Makefile](file:///e:/WebSpider%203D/Makefile).

### 2. C/C++ Engine Overlay (`src/source/`)
- Renamed C++ editor space directories:
  - `space_mixar_assets` → `space_webspider_assets`
  - `space_mixar_layers` → `space_webspider_layers`
  - `space_mixar_properties` → `space_webspider_properties`
  - `space_mixie` → `space_webspider_ai`
  - `space_mixie_chat` → `space_webspider_chat`
- Renamed C++ files:
  - `mixar_local_auth_server.cc/.h` → `webspider_local_auth_server.cc/.h`
  - `versioning_mixar_200.hh` → `versioning_webspider_200.hh`
  - All `mixie_*` C++ space source/header files → `webspider_ai_*` and `webspider_chat_*`.
- Updated C++ space enums and types (`SPACE_WEBSPIDER_ASSETS`, `SPACE_WEBSPIDER_LAYERS`, `SPACE_WEBSPIDER_PROPERTIES`, `SPACE_WEBSPIDER_CHAT`, `SPACE_WEBSPIDER_AI`).
- Updated window title strings and local authentication titles.

### 3. Python Addon & Modules (`src/scripts/`)
- Renamed Python package directory `src/scripts/mixar` → `src/scripts/webspider`.
- Renamed Python preset directory `src/scripts/presets/mixar` → `src/scripts/presets/webspider`.
- Renamed launcher script `src/release/scripts/mixar_launcher.py` → `src/release/scripts/webspider_launcher.py`.
- Renamed `space_mixie` → `space_webspider_ai` and `space_mixie_chat` → `space_webspider_chat` in Python modules.
- Updated all module imports across Python files (`from webspider...`, `import webspider...`).
- Updated operator `bl_idname`s, RNA property names, and category names (`webspider.*`, `webspider_ai.*`).

### 4. Brand Visual Assets & Packaging
- Generated new high-resolution logo asset (`webspider_logo.png`) for onboarding/UI.
- Generated new high-resolution 16:9 splash screen asset (`splash.png`).
- Renamed SVG & ICO icons:
  - `mixar_icon.svg` → `webspider_icon.svg`
  - `mixar_icons.svg` → `webspider_icons.svg`
  - `winmixar.ico` → `winwebspider.ico`
  - `winmixarfile.ico` → `winwebspiderfile.ico`
  - `LicenseRef-Mixar-Brand.txt` → `LicenseRef-WebSpider-Brand.txt`
- Updated desktop manifests and MSIX packaging templates (`webspider3d.desktop`, `org.webspider.WebSpider3D.metainfo.xml`, `webspider3d.exe.manifest.in`, `WixUI_Blender.wxs`).

### 5. Documentation & Metadata
- Updated [README.md](file:///e:/WebSpider%203D/README.md), [CLAUDE.md](file:///e:/WebSpider%203D/CLAUDE.md), `AUTHORS`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `MAINTAINERS.md`, `NOTICE.md`, `SECURITY.md`, `SUPPORT.md`, `TRADEMARKS.md`.

---

## Verification Results

### Search Verification
- `git grep -i "mixar"` → **0 results**.
- `git grep -i "mixie"` → **0 results**.

### Runtime Config & Module Verification
- Executed `scripts/generate_config.py` → Successfully generated `build/Dev/bin/config/webspider.json` with `https://api.webspider3d.com` and `https://www.webspider3d.com`.
- Executed Python package import test (`import webspider`) → **Imported successfully without errors**.
