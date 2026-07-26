<!-- SPDX-FileCopyrightText: 2026 WebSpider Studios -->
<!-- SPDX-License-Identifier: GPL-3.0-or-later -->

# Notices

WebSpider 3D App is a project of WebSpider Studios, built on top of Blender.

## Corporate Structure

The WebSpider 3D product is developed and operated by:

- **WebSpider Studios** — a company incorporated in India. Current copyright holder of the WebSpider 3D source code and brand assets.
- **WebSpider 3D Inc** — a company incorporated in the United States. Operates WebSpider 3D's hosted backend services and US-facing commercial operations.

Copyright in this repository is currently held by WebSpider Studios. An intra-group assignment of intellectual property to WebSpider 3D Inc is planned; copyright notices in this repository will be updated to reflect WebSpider 3D Inc at that time. The assignment will not affect the GPL-3.0-or-later license under which this source is published, nor users' rights under that license.

Blender is free software. Blender-derived files and upstream materials retain their own notices and licenses. File-level SPDX metadata and [REUSE.toml](REUSE.toml) are the authoritative source for per-file licensing in this repository.

The WebSpider 3D name, WebSpider 3D logo, WebSpider AI name, and related brand assets are trademarks or pending trademarks of WebSpider Studios. The source code license does not grant trademark rights, and WebSpider 3D brand-asset files (logos, icons, wordmarks) are governed separately by [LICENSES/LicenseRef-WebSpider-Brand.txt](LICENSES/LicenseRef-WebSpider-Brand.txt) — not by GPL-3.0-or-later. See [TRADEMARKS.md](TRADEMARKS.md).

WebSpider 3D hosted backend services are not included in this public source repository.

## Third-Party Software Acknowledgements

### ucupaint

WebSpider 3D's texture painting module builds on the open-source [ucupaint](https://github.com/ucupumar/ucupaint) addon by [ucupumar](https://github.com/ucupumar), used under the terms of the GNU General Public License version 3 or later.

Specifically:

- **Asset library** — `src/scripts/webspider/modules/paint/core/lib/lib.blend` is a modified version of ucupaint's `lib_281.blend`, containing layer/channel node groups derived from the original.
- **Layer and channel architecture** — files under `src/scripts/webspider/modules/paint/core/io/connections/`, `src/scripts/webspider/modules/paint/core/layer/create_channels.py`, and parts of the UI under `src/scripts/webspider/modules/paint/ui/` adapt ucupaint's patterns for channel handling, normal/height layer composition, and connection topology. WebSpider 3D's adaptations have been substantially modified and integrated with WebSpider 3D's wider feature set, but the design lineage is ucupaint's.

ucupaint's license is GPL-3.0-or-later (see [LICENSES/GPL-3.0-or-later.txt](LICENSES/GPL-3.0-or-later.txt)). WebSpider 3D's adaptations of ucupaint code are also distributed under GPL-3.0-or-later, consistent with the original license. Per-file SPDX metadata and [REUSE.toml](REUSE.toml) record per-file copyright attribution.

We thank ucupumar for the open-source work that made WebSpider 3D's texture-painting module possible.
