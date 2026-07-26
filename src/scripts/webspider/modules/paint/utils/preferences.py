# SPDX-FileCopyrightText: 2024 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Utility functions for accessing WebSpider 3D Paint preferences"""

import bpy


def get_webspider3d_paint_preferences():
    """Get the WebSpider 3D Paint preferences from the current scene.

    Returns:
        WebSpider 3DPaintPreferences: The preferences property group
    """
    if bpy.context.scene:
        return bpy.context.scene.webspider3d_paint_preferences
    return None
