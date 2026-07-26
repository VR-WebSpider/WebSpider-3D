<!-- SPDX-FileCopyrightText: 2026 WebSpider Studios -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

<div align="center">

  <img src="https://github.com/VR-WebSpider/webspider-assets/raw/main/branding/WebSpider%20Studios%20Official%20Logo%20Color.png" alt="WebSpider Studios Logo" width="480" />

  # WebSpider 3D Suite

  **AI-Powered 3D Content Creation Software by WebSpider Studios (Built on Blender 5.0)**

  [![Studio: WebSpider Studios](https://img.shields.io/badge/Studio-WebSpider_Studios-00b894.svg?style=for-the-badge)](https://github.com/VR-WebSpider)
  [![Engine: Blender 5.0](https://img.shields.io/badge/Engine-Blender_5.0-E87D0D.svg?style=for-the-badge)](https://www.blender.org)
  [![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-emerald.svg?style=for-the-badge)](https://www.gnu.org/licenses/gpl-3.0)
  [![Release: v3.1.49](https://img.shields.io/badge/Release-v3.1.49-723EC3.svg?style=for-the-badge)](https://github.com/VR-WebSpider/WebSpider-3D/releases)

</div>

---

## 🚀 Download & Quick Links

- 💻 **Windows Setup (.exe)**: [<kbd>⬇️ Download WebSpider 3D Setup Installer</kbd>](https://github.com/VR-WebSpider/webspider-assets/raw/main/WebSpider3D_Setup_3.1.49.exe)
- 🌐 **WebSpider Studios Official Website**: [webspiderstudios.com](https://github.com/VR-WebSpider/WebSpider-Studios)
- 🏢 **Central Asset Hub**: [github.com/VR-WebSpider/webspider-assets](https://github.com/VR-WebSpider/webspider-assets)

---

## ✨ Key Features of WebSpider 3D

WebSpider 3D retains 100% of Blender's core engine (sculpting, animation, rendering, simulation, Python API) while integrating WebSpider Studios' AI creation tools:

* 🤖 **In-Viewport AI Agent Chat**: Meet **WebSpider AI**—an interactive assistant inside Blender viewports that autonomously executes scene modeling, UV unwrapping, material node setup, texture generation, and lookdev.
* 🎨 **Layered Texture Painting System**: A stacked, Photoshop-style node-driven texture painter featuring procedural materials, masks, modifiers, baking, UDIM support, and direct asset export.
* 🧊 **AI 3D Mesh Generation**: Neural text-to-3D and image-to-3D generation powered by advanced AI models, with automatic retopology and UV unwrapping.
* 🦴 **Automated Auto-Rig & Retopology**: Convert high-poly sculpted models into clean, game-ready quad meshes with automatic skeletal rigging for instant game engine integration.
* 🔑 **Bring Your Own Key (BYOK)**: Connect your own OpenAI, Anthropic, or local model API keys for total privacy and zero credit limits.
* 🎛️ **WebSpider 3D Native Spaces**: Custom-engineered editor spaces (**Layers**, **Properties**, **Assets**, **WebSpider AI Chat**) built directly into the Blender interface.

---

## 🏗️ Architecture & Overlay Flow

WebSpider 3D uses a clean overlay architecture built on Blender 5.0:

```text
upstream/               Blender 5.0 source (git submodule)
src/                    WebSpider 3D's overlay source — Python addon + C++ additions
source/                 Generated working tree: upstream/ copied here, then src/ rsync'd on top
build/<env>/            CMake build directory
```

---

## 🛠️ Building WebSpider 3D from Source

### Prerequisites

1. **System Build Tools**: Everything required to build Blender 5.0 (C++20 compiler, CMake 3.22+, Ninja / Visual Studio, Python 3.11+).
2. **Platform Setup**: Follow Blender's developer documentation: <https://developer.blender.org/docs/handbook/building_blender/>.

### Build Commands

```bash
# 1. Clone repo recursively with submodules
git clone --recursive https://github.com/VR-WebSpider/WebSpider-3D.git
cd WebSpider-3D

# 2. Initialize submodules
make init

# 3. Configure runtime settings
cp .env.example .env

# 4. Build executable
make build
```

Built executables land in `build/<WEBSPIDER_ENV>/bin/`.

---

## ⚖️ Licensing & Trademarks

- **Source Code**: Published under the **GNU General Public License v3.0 or later (GPL-3.0-or-later)**.
- **Trademarks & Branding**: The WebSpider 3D name, WebSpider Studios name, logos, and brand assets are trademarks of **WebSpider Studios** governed under [`LICENSES/LicenseRef-WebSpider-Brand.txt`](LICENSES/LicenseRef-WebSpider-Brand.txt).
- **Upstream Attribution**: WebSpider 3D is derived from Blender (GNU GPL) and incorporates ucupaint (GNU GPL-3.0). See [NOTICE.md](NOTICE.md).

---

<div align="center">
  <sub>Developed by <strong>WebSpider Studios</strong>. All Rights Reserved.</sub>
</div>
