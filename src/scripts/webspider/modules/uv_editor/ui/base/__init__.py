# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Base Module

Contains utility operators and base panels for the WebSpider 3D UV Properties space.
"""

from . import operators
from . import panels


classes = (
    *operators.classes,
    *panels.classes,
)
