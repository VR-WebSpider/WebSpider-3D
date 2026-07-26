# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Panel Toggle Operators

Operators for toggling panel visibility in the WebSpider AI space sidebar.
These create mutually exclusive toggle button behavior.
"""

import bpy
from bpy.types import Operator


class WEBSPIDER_AI_OT_toggle_mesh_segment_panel(Operator):
    """Toggle Mesh Segment panel visibility"""
    bl_idname = "webspider_ai.toggle_mesh_segment_panel"
    bl_label = "Toggle Mesh Segment Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        # Toggle: if already MESH_SEGMENT, set to NONE; otherwise set to MESH_SEGMENT
        if scene.webspider_ai_active_panel == 'MESH_SEGMENT':
            scene.webspider_ai_active_panel = 'NONE'
        else:
            scene.webspider_ai_active_panel = 'MESH_SEGMENT'

        # Force UI region to redraw immediately
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()
        return {'FINISHED'}


class WEBSPIDER_AI_OT_toggle_lookdev_panel(Operator):
    """Toggle Lookdev panel visibility"""
    bl_idname = "webspider_ai.toggle_lookdev_panel"
    bl_label = "Toggle Lookdev Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        # Toggle: if already LOOKDEV, set to NONE; otherwise set to LOOKDEV
        if scene.webspider_ai_active_panel == 'LOOKDEV':
            scene.webspider_ai_active_panel = 'NONE'
        else:
            scene.webspider_ai_active_panel = 'LOOKDEV'

        # Force UI region to redraw immediately
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()
        return {'FINISHED'}


class WEBSPIDER_AI_OT_toggle_lookdev360_panel(Operator):
    """Toggle Lookdev360 panel visibility"""
    bl_idname = "webspider_ai.toggle_lookdev360_panel"
    bl_label = "Toggle Lookdev360 Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        # Toggle: if already LOOKDEV360, set to NONE; otherwise set to LOOKDEV360
        if scene.webspider_ai_active_panel == 'LOOKDEV360':
            scene.webspider_ai_active_panel = 'NONE'
        else:
            scene.webspider_ai_active_panel = 'LOOKDEV360'

        # Force UI region to redraw immediately
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()
        return {'FINISHED'}


class WEBSPIDER_AI_OT_toggle_imagegen_panel(Operator):
    """Toggle Image Gen panel visibility"""
    bl_idname = "webspider_ai.toggle_imagegen_panel"
    bl_label = "Toggle Image Gen Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        # Toggle: if already IMAGEGEN, set to NONE; otherwise set to IMAGEGEN
        if scene.webspider_ai_active_panel == 'IMAGEGEN':
            scene.webspider_ai_active_panel = 'NONE'
        else:
            scene.webspider_ai_active_panel = 'IMAGEGEN'

        # Force UI region to redraw immediately
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()
        return {'FINISHED'}


class WEBSPIDER_AI_OT_toggle_image_to_3d_panel(Operator):
    """Toggle Image to 3D panel visibility"""
    bl_idname = "webspider_ai.toggle_image_to_3d_panel"
    bl_label = "Toggle Image to 3D Panel"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        # Toggle: if already IMAGE_TO_3D, set to NONE; otherwise set to IMAGE_TO_3D
        if scene.webspider_ai_active_panel == 'IMAGE_TO_3D':
            scene.webspider_ai_active_panel = 'NONE'
        else:
            scene.webspider_ai_active_panel = 'IMAGE_TO_3D'

        # Force UI region to redraw immediately
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()
        return {'FINISHED'}


classes = (
    WEBSPIDER_AI_OT_toggle_mesh_segment_panel,
    WEBSPIDER_AI_OT_toggle_lookdev_panel,
    WEBSPIDER_AI_OT_toggle_lookdev360_panel,
    WEBSPIDER_AI_OT_toggle_imagegen_panel,
    WEBSPIDER_AI_OT_toggle_image_to_3d_panel,
)
