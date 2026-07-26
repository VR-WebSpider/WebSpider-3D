# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Transform Module

Contains panels and operators for UV transform/snapping operations.
Note: The main Transform panel is implemented in C++ (space_webspider3d_uv_properties.cc).
"""

from . import panels
from . import operators


classes = (
    *panels.classes,
    *operators.classes,
)
