# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Moodboard Context Menus

Right-click context menu for moodboard operations.
"""

import bpy
from bpy.types import Menu

from webspider.modules.common.utils.webspider_ai_space_utils import (
    WEBSPIDER_AI_SPACE_AVAILABLE,
    get_selected_moodboard_items,
)


class WEBSPIDER_AI_MT_moodboard_context_menu(Menu):
    """Right-click context menu for moodboard"""
    bl_label = "Moodboard"
    bl_idname = "WEBSPIDER_AI_MT_moodboard_context_menu"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Check selection state
        selected_images, selected_textboxes, selected_groups = (
            get_selected_moodboard_items(scene)
        )
        total_items_selected = selected_images + selected_textboxes

        # Check if any selected images belong to a group
        has_grouped_selection = any(
            img.selected and img.group_index >= 0
            for img in scene.webspider_ai_moodboard_images
        )

        # Group operations - show contextually
        if selected_groups > 0 or has_grouped_selection:
            layout.operator("webspider_ai.ungroup", text="Ungroup", icon='UGLYPACKAGE')
            layout.separator()
        elif total_items_selected >= 2:
            layout.operator("webspider_ai.create_group", text="Group", icon='GROUP')
            layout.separator()

        # Add content
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("webspider_ai.moodboard_add_existing_image", text="Add Existing Image", icon='TRIA_DOWN')
        layout.operator("webspider_ai.moodboard_add_image", text="Open Image", icon='FILE_FOLDER')
        layout.operator("webspider_ai.moodboard_paste_image", text="Paste from Clipboard", icon='PASTEDOWN')
        layout.operator("webspider_ai.moodboard_add_textbox", text="Add Text", icon='FONT_DATA')

        layout.separator()

        # Text box editing (only shown when exactly one text box is selected)
        if selected_textboxes == 1:
            for i, tb in enumerate(scene.webspider_ai_moodboard_textboxes):
                if tb.selected:
                    layout.operator_context = 'INVOKE_DEFAULT'
                    op = layout.operator(
                        "webspider_ai.moodboard_edit_textbox",
                        text="Edit Text Content",
                        icon='GREASEPENCIL',
                    )
                    op.index = i

                    op2 = layout.operator(
                        "webspider_ai.moodboard_update_textbox_properties",
                        text="Edit Text Properties",
                        icon='PROPERTIES',
                    )
                    op2.index = i
                    break
            layout.separator()

        # Transform operations (only enabled when images are selected)
        row = layout.row()
        row.enabled = selected_images > 0
        row.operator("webspider_ai.moodboard_crop_tool", text="Crop", icon='FULLSCREEN_EXIT')

        row = layout.row()
        row.enabled = selected_images > 0
        row.operator("webspider_ai.rotate_images", text="Rotate 90°", icon='LOOP_FORWARDS').angle = 90.0

        row = layout.row()
        row.enabled = selected_images > 0
        row.operator("webspider_ai.flip_horizontal", text="Flip Horizontal", icon='ARROW_LEFTRIGHT')

        row = layout.row()
        row.enabled = selected_images > 0
        row.operator("webspider_ai.flip_vertical", text="Flip Vertical", icon='EMPTY_SINGLE_ARROW')

        row = layout.row()
        row.enabled = total_items_selected > 0
        row.operator("webspider_ai.moodboard_duplicate", text="Duplicate", icon='DUPLICATE')

        layout.separator()

        # Selection
        layout.operator("webspider_ai.moodboard_select_all", text="Select All", icon='CHECKBOX_HLT')
        layout.operator("webspider_ai.moodboard_deselect_all", text="Deselect All", icon='CHECKBOX_DEHLT')

        layout.separator()

        # Export (only enabled when images are selected)
        row = layout.row()
        row.enabled = selected_images > 0
        row.operator("webspider_ai.moodboard_export_images", text="Export", icon='EXPORT')

        layout.separator()

        # Delete (only enabled when something is selected)
        row = layout.row()
        row.enabled = (total_items_selected + selected_groups) > 0
        row.operator("webspider_ai.moodboard_delete", text="Delete", icon='TRASH')


# Only include menu if WEBSPIDER_AI space is available
classes = (
    WEBSPIDER_AI_MT_moodboard_context_menu,
) if WEBSPIDER_AI_SPACE_AVAILABLE else ()
