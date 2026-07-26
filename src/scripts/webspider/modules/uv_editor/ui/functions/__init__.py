# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Functions Module

Contains panels and operators for UV functions (seam, pin, merge, split, hide, copy/paste).
"""

from . import panels
from . import operators


classes = (
    *panels.classes,
    *operators.classes,
)
