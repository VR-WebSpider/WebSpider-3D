# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider AI Common Module

Shared components for WebSpider AI space including mode selector and utilities.
"""

import bpy
from bpy.types import Panel, Operator
from bpy.props import StringProperty


# ============================================================================
# Mode Selector Panel
# ============================================================================

class WEBSPIDER_AI_PT_mode_selector(Panel):
    """Mode selector panel shown at top of sidebar"""
    bl_label = "Mode"
    bl_idname = "WEBSPIDER_AI_PT_mode_selector"
    bl_space_type = 'WEBSPIDER_AI'
    bl_region_type = 'UI'
    bl_category = "WebSpider AI"

    def draw(self, context):
        layout = self.layout
        swebspider_ai = context.space_data

        # Create a column of mode buttons
        col = layout.column(align=True)

        # Moodboard button
        row = col.row()
        row.scale_y = 1.2
        op = row.operator("webspider_ai.set_mode", text="Moodboard",
                         icon='IMAGE_PLANE',
                         depress=(swebspider_ai.webspider_ai_mode == 'MOODBOARD'))
        op.mode = 'MOODBOARD'



# ============================================================================
# Mode Switching Operator
# ============================================================================

class WEBSPIDER_AI_OT_set_mode(Operator):
    """Switch to a specific WebSpider AI mode"""
    bl_idname = "webspider_ai.set_mode"
    bl_label = "Set WebSpider AI Mode"
    bl_description = "Switch to a specific WebSpider AI mode"
    bl_options = {'REGISTER', 'UNDO'}

    mode: StringProperty(
        name="Mode",
        description="Mode to switch to",
        default="MOODBOARD"
    )

    def execute(self, context):
        swebspider_ai = context.space_data
        if swebspider_ai and swebspider_ai.bl_rna.identifier == "SpaceWebSpider AI":
            swebspider_ai.webspider_ai_mode = self.mode
            # Trigger redraw
            for area in context.screen.areas:
                if area.type == 'WEBSPIDER_AI':
                    area.tag_redraw()
            return {'FINISHED'}
        return {'CANCELLED'}


# ============================================================================
# Placeholder Operator (for incomplete features)
# ============================================================================

class WEBSPIDER_AI_OT_placeholder(Operator):
    """Placeholder action for features in development"""
    bl_idname = "webspider_ai.placeholder"
    bl_label = "Placeholder Action"
    bl_description = "This is a placeholder button"

    def execute(self, context):
        self.report({'INFO'}, "Placeholder button clicked")
        return {'FINISHED'}


# ============================================================================
# Registration
# ============================================================================

classes = (
    WEBSPIDER_AI_PT_mode_selector,
    WEBSPIDER_AI_OT_set_mode,
    WEBSPIDER_AI_OT_placeholder,
)


def register():
    """Register shared WebSpider AI components"""
    from bpy.utils import register_class
    for cls in classes:
        try:
            register_class(cls)
        except ValueError:
            pass


def unregister():
    """Unregister shared WebSpider AI components"""
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        try:
            unregister_class(cls)
        except RuntimeError:
            pass
