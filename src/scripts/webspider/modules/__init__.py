# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D Modules

Contains feature modules for the WebSpider 3D application.

Available modules:
- common: Shared components (mode selector, utilities)
- moodboard: Moodboard mode for image collection and AI generation
- space_webspider_ai: WebSpider AI space with segmentation, lookdev, and image generation
- paint: Texture painting backend (layer system, nodes, baking, texturing workspace)
- testing: Testing utilities and test files

Registration is handled by bootstrap/__init__.py which auto-discovers
and registers all files in modules/**/ui/ directories.
Paint module registration is handled by bootstrap/paint_module.py.
Do NOT import moodboard or space_webspider_ai here - it causes double registration.
"""

from . import common

# Testing module is only imported when explicitly requested
# to avoid import errors during addon startup
TESTING_MODULE_AVAILABLE = False
