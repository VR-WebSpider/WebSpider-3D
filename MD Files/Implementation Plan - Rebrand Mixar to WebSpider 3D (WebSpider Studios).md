# Implementation Plan - Rebrand WebSpider 3D to WebSpider 3D (WebSpider Studios)

Completely rebrand the **WebSpider 3D** codebase to **WebSpider 3D**, developed by **WebSpider Studios**.
Every single reference—including app name, studio branding, AI assistant name ("WebSpider AI" → "WebSpider AI"), C++ space editors, Python package paths, environment headers, build scripts, DNA/RNA structures, UI labels, icons, splash screens, documentation, and configuration files—will be updated systematically without breaking functionality or compromising capabilities.

---

## Technical Naming Mapping

| Target Category | Original Brand / Name | Rebranded Name |
| :--- | :--- | :--- |
| **Product / App Name** | WebSpider 3D / WebSpider 3D | **WebSpider 3D** |
| **Studio / Organization** | WebSpider Studios / WebSpider Studios | **WebSpider Studios** |
| **AI Assistant Name** | WebSpider AI | **WebSpider AI** |
| **Domain / API Endpoint** | `webspider3d.com` / `api.webspider3d.com` | `webspider3d.com` / `api.webspider3d.com` |
| **Executable Name** | `webspider3d.exe` / `webspider3d-launcher` | `webspider3d.exe` / `webspider-launcher` |
| **User Config Directory** | `~/.webspider3d` | `~/.webspider3d` |
| **Runtime Config File** | `webspider.json` | `webspider.json` |
| **C++ Header File** | `webspider_env_config.h` | `webspider_env_config.h` |
| **Python Package** | `src/scripts/webspider` | `src/scripts/webspider` |
| **Presets Package** | `src/scripts/presets/webspider3d` | `src/scripts/presets/webspider` |
| **DNA/RNA Space Types** | `SPACE_WEBSPIDER_*`, `SPACE_WEBSPIDER_AI` | `SPACE_WEBSPIDER_*`, `SPACE_WEBSPIDER_AI` |
| **C++ Editor Space Dirs**| `space_webspider3d_*`, `space_webspider_ai_*` | `space_webspider_*`, `space_webspider_ai` |
| **Brand License File** | `LicenseRef-WebSpider-Brand.txt` | `LicenseRef-WebSpider-Brand.txt` |

---

## User Review Required

> [!IMPORTANT]
> - All `webspider3d` and `webspider_ai` references across C++ source code, Python modules, build scripts, and metadata will be renamed.
> - The Python addon package directory `src/scripts/webspider/` will be moved to `src/scripts/webspider/`.
> - C++ editor directories (e.g. `src/source/blender/editors/space_webspider_layers`) will be renamed to match the WebSpider 3D namespace.
> - Brand graphics (`splash.png`, `webspider_logo.png`, SVGs, and ICO files) will be updated with generated WebSpider Studios branding assets.

---

## Proposed Changes

### Phase 1: Core Build System & Scripts (`scripts/`, `cmake/`, `Makefile`)

#### [MODIFY] [scripts/unix/build.sh](file:///e:/WebSpider%203D/scripts/unix/build.sh)
#### [MODIFY] [scripts/unix/settings.sh](file:///e:/WebSpider%203D/scripts/unix/settings.sh)
#### [MODIFY] [scripts/unix/overlay.sh](file:///e:/WebSpider%203D/scripts/unix/overlay.sh)
#### [MODIFY] [scripts/unix/package.sh](file:///e:/WebSpider%203D/scripts/unix/package.sh)
#### [MODIFY] [scripts/windows/build.bat](file:///e:/WebSpider%203D/scripts/windows/build.bat)
#### [MODIFY] [scripts/windows/settings.bat](file:///e:/WebSpider%203D/scripts/windows/settings.bat)
#### [MODIFY] [scripts/windows/overlay.bat](file:///e:/WebSpider%203D/scripts/windows/overlay.bat)
#### [MODIFY] [scripts/generate_config.py](file:///e:/WebSpider%203D/scripts/generate_config.py)
#### [MODIFY] [Makefile](file:///e:/WebSpider%203D/Makefile)
#### [MODIFY] [.env.example](file:///e:/WebSpider%203D/.env.example)

- Update environment variables: `WEBSPIDER_ENV` → `WEBSPIDER_ENV`, `WEBSPIDER_API_URL` → `WEBSPIDER_API_URL`, `WEBSPIDER_UPSTREAM_DIR` → `WEBSPIDER_UPSTREAM_DIR`.
- Update output config filenames (`webspider.json`, `webspider_env_config.h`, `_build_env.py`).
- Update overlay script paths from `src/scripts/webspider` to `src/scripts/webspider`.

---

### Phase 2: C/C++ Engine Overlay (`src/source/`)

#### [RENAME] `src/source/blender/editors/space_webspider_assets` → `src/source/blender/editors/space_webspider_assets`
#### [RENAME] `src/source/blender/editors/space_webspider_layers` → `src/source/blender/editors/space_webspider_layers`
#### [RENAME] `src/source/blender/editors/space_webspider_properties` → `src/source/blender/editors/space_webspider_properties`
#### [RENAME] `src/source/blender/editors/space_webspider_ai` → `src/source/blender/editors/space_webspider_ai`
#### [RENAME] `src/source/blender/editors/space_webspider_chat` → `src/source/blender/editors/space_webspider_chat`
#### [RENAME] `src/source/creator/webspider_local_auth_server.cc` → `src/source/creator/webspider_local_auth_server.cc`
#### [RENAME] `src/source/creator/webspider_local_auth_server.h` → `src/source/creator/webspider_local_auth_server.h`
#### [RENAME] `src/source/blender/blenloader/versioning_webspider_200.hh` → `src/source/blender/blenloader/versioning_webspider_200.hh`

#### [MODIFY] [DNA_space_enums.h](file:///e:/WebSpider%203D/src/source/blender/makesdna/DNA_space_enums.h)
#### [MODIFY] [DNA_space_types.h](file:///e:/WebSpider%203D/src/source/blender/makesdna/DNA_space_types.h)
#### [MODIFY] [BKE_blender_version.h](file:///e:/WebSpider%203D/src/source/blender/blenkernel/BKE_blender_version.h)
#### [MODIFY] [creator_startup.cc](file:///e:/WebSpider%203D/src/source/creator/creator_startup.cc)
#### [MODIFY] [creator_auth.cc](file:///e:/WebSpider%203D/src/source/creator/creator_auth.cc)
#### [MODIFY] [blender_launcher_win32.c](file:///e:/WebSpider%203D/src/source/creator/blender_launcher_win32.c)
#### [MODIFY] [CMakeLists.txt files in src/source/](file:///e:/WebSpider%203D/src/source/creator/CMakeLists.txt)

- Replace space constants (`SPACE_WEBSPIDER_*`, `SPACE_WEBSPIDER_AI_*` → `SPACE_WEBSPIDER_*`, `SPACE_WEBSPIDER_AI_*`).
- Replace window title prefixes ("WebSpider 3D 5.0" → "WebSpider 3D").
- Update splash screen titles and local auth server titles ("WebSpider 3D Login" → "WebSpider 3D Login").

---

### Phase 3: Python Addon & Bootstrap Infrastructure (`src/scripts/`)

#### [RENAME] `src/scripts/webspider/` → `src/scripts/webspider/`
#### [RENAME] `src/scripts/presets/webspider3d/` → `src/scripts/presets/webspider/`

#### [MODIFY] [src/scripts/startup/bootstrap/__init__.py](file:///e:/WebSpider%203D/src/scripts/startup/bootstrap/__init__.py)
#### [MODIFY] [src/scripts/startup/bl_ui/space_topbar.py](file:///e:/WebSpider%203D/src/scripts/startup/bl_ui/space_topbar.py)
#### [MODIFY] [src/scripts/startup/bl_ui/space_toolsystem_toolbar.py](file:///e:/WebSpider%203D/src/scripts/startup/bl_ui/space_toolsystem_toolbar.py)
#### [MODIFY] [src/scripts/webspider/__init__.py](file:///e:/WebSpider%203D/src/scripts/webspider/__init__.py)
#### [MODIFY] All modules in `src/scripts/webspider/modules/`:
  - `agent_bubble/`, `agent_scene_strip/`, `agent_viewport_lock/`
  - `asset_search/`, `auth/`, `byok/`, `common/`, `hunyuan/`
  - `mesh_segment/`, `moodboard/`, `onboarding/`, `operation_history/`
  - `paint/`, `scene_graph/`, `space_webspider_ai/`, `space_webspider_chat/`
  - `space_texture_sets/`, `texel_density/`, `uv_editor/`, `workflow/`

- Rename Python imports from `webspider3d.*` to `webspider.*`.
- Rename operator bl_idnames (`webspider_ai.*` → `webspider.*` / `webspider_ai.*`, `webspider3d.*` → `webspider.*`).
- Rename RNA property prefixes (`webspider_ai_*` / `webspider3d_*` → `webspider_*`).
- Update UI panel labels, tab titles, headers ("WebSpider AI" → "WebSpider AI", "WebSpider 3D" → "WebSpider 3D").
- Update home directory paths (`~/.webspider3d` → `~/.webspider3d`).

---

### Phase 4: Brand Visual Assets & Packaging

#### [NEW] Rebranded Splash Image & Logos
- Generate WebSpider 3D splash screen asset (`splash.png`).
- Generate WebSpider Studios logo asset (`webspider_logo.png`).
- Update SVG/ICO icon files (`webspider_icon.svg` → `webspider_icon.svg`, `webspider_icons.svg` → `webspider_icons.svg`, `winwebspider.ico` → `winwebspider.ico`).

#### [MODIFY] Release Manifests & Desktop Entries
- `src/release/freedesktop/webspider3d.desktop` → `src/release/freedesktop/webspider3d.desktop`
- `src/release/freedesktop/org.webspider.WebSpider3D.metainfo.xml` → `org.webspider.WebSpider3D.metainfo.xml`
- `src/release/windows/manifest/webspider3d.exe.manifest.in` → `webspider3d.exe.manifest.in`
- `src/release/windows/installer_wix/WixUI_Blender.wxs`
- `src/release/windows/msix/AppxManifest.xml.template`

---

### Phase 5: Documentation & License Header Updates

#### [MODIFY] Root Documentation Files
- [README.md](file:///e:/WebSpider%203D/README.md)
- [CLAUDE.md](file:///e:/WebSpider%203D/CLAUDE.md)
- [AUTHORS](file:///e:/WebSpider%203D/AUTHORS)
- [CODE_OF_CONDUCT.md](file:///e:/WebSpider%203D/CODE_OF_CONDUCT.md)
- [CONTRIBUTING.md](file:///e:/WebSpider%203D/CONTRIBUTING.md)
- [MAINTAINERS.md](file:///e:/WebSpider%203D/MAINTAINERS.md)
- [NOTICE.md](file:///e:/WebSpider%203D/NOTICE.md)
- [SECURITY.md](file:///e:/WebSpider%203D/SECURITY.md)
- [SUPPORT.md](file:///e:/WebSpider%203D/SUPPORT.md)
- [TRADEMARKS.md](file:///e:/WebSpider%203D/TRADEMARKS.md)

---

## Verification Plan

### Automated Verification
- Run `python -m pytest -q` to verify Python test suite passes with updated module imports.
- Run git grep search to verify zero occurrences of `WebSpider 3D`, `webspider3d`, `WebSpider AI`, or `webspider_ai` remain in active codebase paths (excluding external third-party licenses where original authorship notice is required by GPL/SPDX).

### Manual Verification
- Inspect generated configuration files (`webspider.json`, `webspider_env_config.h`).
- Verify directory structure under `src/scripts/webspider` and `src/source/blender/editors/space_webspider_*`.
