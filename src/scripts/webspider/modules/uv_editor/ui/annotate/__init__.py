# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Annotate Module

Panel that mirrors Blender's Active Tool > Annotate properties for the
WebSpider 3D UV editor's CHANNELS sidebar, so annotate settings live next to
the rest of the WebSpider 3D UV property panels instead of in the floating N
panel.
"""

from . import panels


classes = (
    *panels.classes,
)
