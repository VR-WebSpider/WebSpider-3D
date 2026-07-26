# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Base Operators

Utility operators for managing the WebSpider 3D UV sidebar in IMAGE_EDITOR.
"""

import bpy
from bpy.types import Operator


class WEBSPIDER_OT_toggle_uv_sidebar(Operator):
    """Toggle the WebSpider 3D UV sidebar in the Image Editor"""
    bl_idname = "webspider.toggle_uv_sidebar"
    bl_label = "Toggle UV Sidebar"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if context.area is None:
            return False
        # Must be in IMAGE_EDITOR in WEBSPIDER_UV mode
        if context.area.type != 'IMAGE_EDITOR':
            return False
        sima = context.space_data
        return sima and sima.mode == 'WEBSPIDER_UV'

    def execute(self, context):
        bpy.ops.screen.region_toggle(region_type='CHANNELS')
        return {'FINISHED'}


class WEBSPIDER_OT_open_uv_sidebar(Operator):
    """Open the WebSpider 3D UV sidebar if hidden"""
    bl_idname = "webspider.open_uv_sidebar"
    bl_label = "Open UV Sidebar"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if context.area is None:
            return False
        if context.area.type != 'IMAGE_EDITOR':
            return False
        sima = context.space_data
        return sima and sima.mode == 'WEBSPIDER_UV'

    def execute(self, context):
        # Check if CHANNELS region is already visible
        for region in context.area.regions:
            if region.type == 'CHANNELS':
                if region.width <= 1:
                    bpy.ops.screen.region_toggle(region_type='CHANNELS')
                break
        return {'FINISHED'}


classes = (
    WEBSPIDER_OT_toggle_uv_sidebar,
    WEBSPIDER_OT_open_uv_sidebar,
)
