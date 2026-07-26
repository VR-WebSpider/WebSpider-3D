# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Transform/Snapping Panels

Snapping panel for the WebSpider 3D UV Properties space.
"""

import bpy
from bpy.types import Panel

from webspider.modules.uv_editor.ui.base.panels import snap_base_applies


def draw_collapsible_header(layout, ui_state, prop_name, label, icon='NONE'):
    """Draw a collapsible section header with arrow toggle."""
    is_expanded = getattr(ui_state, prop_name)
    header_row = layout.row(align=True)
    header_row.scale_y = 1.3
    collapse_icon = 'DOWNARROW_HLT' if is_expanded else 'RIGHTARROW'
    header_row.prop(ui_state, prop_name, text="", icon=collapse_icon, emboss=False)
    header_row.label(text=label, icon=icon)
    return is_expanded


class WEBSPIDER_UV_PT_snapping(Panel):
    """Snapping panel for WebSpider 3D UV Properties space"""
    bl_label = "Snapping"
    bl_idname = "WEBSPIDER_UV_PT_snapping"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'CHANNELS'
    bl_options = set()

    @classmethod
    def poll(cls, context):
        sima = context.space_data
        if not (sima and sima.mode == 'WEBSPIDER_UV'):
            return False
        wm = context.window_manager
        if not hasattr(wm, 'webspider3d_uv_ui'):
            return False
        return wm.webspider3d_uv_ui.active_panel == 'TRANSFORM'

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.separator(factor=0.5)

        layout.use_property_split = True
        layout.use_property_decorate = False

        # Get UI state for collapsible sections
        uv_ui = wm.webspider3d_uv_ui

        # ========== SNAPPING OPTIONS SECTION ==========
        box = layout.box()
        if draw_collapsible_header(box, uv_ui, "expand_snapping_options", "Snapping Options", icon='SNAP_ON'):
            col = box.column(align=True)
            col.separator(factor=0.5)

            tool_settings = context.tool_settings
            col.prop(tool_settings, "use_snap_uv", text="Enable Snapping")
            col.separator()
            col.label(text="Snap Target")
            col.prop(tool_settings, "snap_uv_element", expand=True)
            col.separator()
            col.label(text="Snap Base")
            row = col.row(align=True)
            row.active = snap_base_applies(tool_settings.snap_uv_element)
            row.prop(tool_settings, "snap_target", expand=True)
            col.separator()
            col.label(text="Affect")
            row = col.row(align=False)
            row.prop(tool_settings, "use_snap_translate", text="Move", toggle=True)
            row.prop(tool_settings, "use_snap_rotate", text="Rotate", toggle=True)
            row.prop(tool_settings, "use_snap_scale", text="Scale", toggle=True)
            col.separator()
            col.label(text="Rotation Increment")
            row = col.row(align=True)
            row.prop(tool_settings, "snap_angle_increment_2d", text="")
            row.prop(tool_settings, "snap_angle_increment_2d_precision", text="")

        layout.separator(factor=0.5)

        # ========== SNAP OPERATIONS SECTION ==========
        box = layout.box()
        if draw_collapsible_header(box, uv_ui, "expand_snap_operations", "Snap Operations", icon='SNAP_GRID'):
            col = box.column(align=True)
            col.separator(factor=0.5)
            col.label(text="Selection")
            col.operator("webspider.snap_selected", text="Selected to Pixels").target = 'PIXELS'
            col.operator("webspider.snap_selected", text="Selected to Cursor").target = 'CURSOR'
            col.operator("webspider.snap_selected", text="Selected to Cursor (Offset)").target = 'CURSOR_OFFSET'
            col.operator("webspider.snap_selected", text="Selected to Adjacent Unselected").target = 'ADJACENT_UNSELECTED'
            col.separator()
            col.label(text="Cursor")
            col.operator("webspider.snap_cursor", text="Cursor to Pixels").target = 'PIXELS'
            col.operator("webspider.snap_cursor", text="Cursor to Selected").target = 'SELECTED'
            col.operator("webspider.snap_cursor", text="Cursor to Origin").target = 'ORIGIN'


classes = (
    WEBSPIDER_UV_PT_snapping,
)
