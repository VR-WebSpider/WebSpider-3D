# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Moodboard Pie Menu

Pie menu for quick access to moodboard features (Tab key).
"""

import bpy
from bpy.types import Menu, Operator


from webspider.modules.common.utils.webspider_ai_space_utils import WEBSPIDER_AI_SPACE_AVAILABLE


class WEBSPIDER_AI_MT_moodboard_pie_menu(Menu):
    """Pie menu for moodboard features"""
    bl_idname = "WEBSPIDER_AI_MT_moodboard_pie_menu"
    bl_label = "Moodboard Features"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        # Pie menu positions (in order):
        # 4(W), 6(E), 2(S), 8(N), 7(NW), 9(NE), 1(SW), 3(SE)

        # West (4) - Mesh Segment
        pie.operator("webspider_ai.mesh_segment_popup", text="Mesh Segment", icon='MESH_GRID')

        # East (6) - From Depth (formerly Lookdev)
        pie.operator("webspider_ai.lookdev_popup", text="From Depth", icon='SHADING_RENDERED')

        # South (2) - ImageGen
        pie.operator("webspider_ai.imagegen_popup", text="ImageGen", icon='IMAGE_DATA')

        # North (8) - Lookdev360
        pie.operator("webspider_ai.lookdev360_popup", text="Generate PBR Maps", icon='SPHERE')

        # Northwest (7) - Segment to 3D
        pie.operator("webspider_ai.segment_to_3d_popup", text="Segment to 3D", icon='MOD_MASK')

        # Northeast (9) - Image to 3D
        pie.operator("webspider_ai.image_to_3d_popup", text="Image to 3D", icon='VIEW3D')

        # Southwest (1) - Scene Reconstruction
        pie.operator("webspider_ai.scene_recon_popup", text="Generate Scene", icon='SCENE_DATA')

        # Southeast (3) - Empty slot (8th position required for proper pie menu layout)
        pie.separator()


class WEBSPIDER_AI_OT_moodboard_pie_menu_call(Operator):
    """Call the moodboard pie menu"""
    bl_idname = "webspider_ai.moodboard_pie_menu_call"
    bl_label = "Moodboard Pie Menu"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        if not WEBSPIDER_AI_SPACE_AVAILABLE:
            return False
        return context.space_data and context.space_data.type == 'WEBSPIDER_AI'

    def execute(self, context):
        bpy.ops.wm.call_menu_pie(name="WEBSPIDER_AI_MT_moodboard_pie_menu")
        return {'FINISHED'}


# Only include classes if WEBSPIDER_AI space is available
classes = (
    WEBSPIDER_AI_MT_moodboard_pie_menu,
    WEBSPIDER_AI_OT_moodboard_pie_menu_call,
) if WEBSPIDER_AI_SPACE_AVAILABLE else ()
