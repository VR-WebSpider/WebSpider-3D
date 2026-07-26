# SPDX-FileCopyrightText: 2025 Blender Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Base Panels

Empty state panel shown when no UV properties are available.
"""

from bpy.types import Panel
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper

# Enum panels that always show when selected (no extra requirements)
_ALWAYS_VISIBLE_PANELS = ('UV_SET', 'PACK_ISLANDS', 'IMAGE', 'MATERIAL_SLOT', 'TRANSFORM')

# Enum panels requiring edit mode
_EDIT_MODE_PANELS = ('UNWRAP', 'EXPORT')

# Tools that have their own dedicated sidebar panel. When the active
# workspace tool is one of these, the matching tool panel takes priority
# over any selected header tab — the header tab stays visually selected
# in the IMAGE_HT_header, but its panel hides so only the tool panel
# shows in the sidebar.
TOOL_PANEL_BY_TOOL = {
    'builtin.select_box': 'WEBSPIDER_UV_PT_selection',
    'builtin.select_circle': 'WEBSPIDER_UV_PT_selection',
    'builtin.select_lasso': 'WEBSPIDER_UV_PT_selection',
    'sculpt.uv_sculpt_grab': 'WEBSPIDER_UV_PT_tools',
    'sculpt.uv_sculpt_relax': 'WEBSPIDER_UV_PT_tools',
    'sculpt.uv_sculpt_pinch': 'WEBSPIDER_UV_PT_tools',
    'builtin.rip_region': 'WEBSPIDER_UV_PT_tools',
    'builtin.transform': 'WEBSPIDER_UV_PT_transform',
    'builtin.uv_tool': 'WEBSPIDER_UV_PT_uv_tool',
    'builtin.uv_functions': 'WEBSPIDER_UV_PT_functions',
    'builtin.annotate': 'WEBSPIDER_UV_PT_annotate',
    'builtin.annotate_line': 'WEBSPIDER_UV_PT_annotate',
    'builtin.annotate_polygon': 'WEBSPIDER_UV_PT_annotate',
    'builtin.annotate_eraser': 'WEBSPIDER_UV_PT_annotate',
}

TOOL_BASED_TOOLS = tuple(TOOL_PANEL_BY_TOOL)


def snap_base_applies(snap_uv_element):
    """Return whether Snap Base controls apply for a snap target value."""
    disabled = {'INCREMENT', 'GRID'}
    if isinstance(snap_uv_element, str):
        return snap_uv_element not in disabled
    return bool(set(snap_uv_element).difference(disabled))


def tool_panel_is_active(context):
    """Return True if the active workspace tool has a dedicated WebSpider 3D
    UV sidebar panel.

    Used by the seven header-tab panel polls so the header panel hides
    when a tool-bound panel (Selection / Transform / UV Sculpt Tools /
    Tools / Functions / Annotate) is about to show — giving the
    toolbar selection priority over the header selection in the
    sidebar without having to forcibly deselect the header tab itself.
    """
    area = context.area
    if area is None:
        return False
    with context.temp_override(area=area):
        tool = ToolSelectPanelHelper.tool_active_from_context(context)
        return tool is not None and tool.idname in TOOL_BASED_TOOLS


def poll_header_panel(context, panel_name, requires_edit=False,
                      requires_mesh_data=False):
    """Shared poll for header-tab panels in the WebSpider 3D UV sidebar."""
    sima = context.space_data
    if not (sima and sima.mode == 'WEBSPIDER_UV'):
        return False
    wm = context.window_manager
    if not hasattr(wm, 'webspider3d_uv_ui'):
        return False
    if wm.webspider3d_uv_ui.active_panel != panel_name:
        return False

    obj = context.active_object
    if requires_edit:
        if not (obj and obj.type == 'MESH' and obj.mode == 'EDIT'):
            return False
    elif requires_mesh_data:
        if not (obj and obj.type == 'MESH' and obj.data):
            return False

    return not tool_panel_is_active(context)


def _any_panel_would_show(context):
    """Check if any UV property panel would be visible."""
    wm = context.window_manager
    if not hasattr(wm, 'webspider3d_uv_ui'):
        return False

    active = wm.webspider3d_uv_ui.active_panel
    obj = context.active_object
    in_edit = obj and obj.type == 'MESH' and obj.mode == 'EDIT'

    if active in _ALWAYS_VISIBLE_PANELS:
        return True

    if active in _EDIT_MODE_PANELS:
        return in_edit

    if active == 'TEXEL_DENSITY':
        return obj and obj.type == 'MESH' and obj.data is not None

    # active_panel == 'NONE': tool-based panels need edit mode + matching tool
    if not in_edit:
        return False

    area = context.area
    if area:
        with context.temp_override(area=area):
            tool = ToolSelectPanelHelper.tool_active_from_context(context)
            if tool and tool.idname in TOOL_BASED_TOOLS:
                return True

    return False


class WEBSPIDER_UV_PT_empty_state(Panel):
    """Empty state shown when no UV properties are available"""
    bl_label = ""
    bl_idname = "WEBSPIDER_UV_PT_empty_state"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'CHANNELS'
    bl_options = {'HIDE_HEADER'}

    @classmethod
    def poll(cls, context):
        sima = context.space_data
        if not (sima and sima.mode == 'WEBSPIDER_UV'):
            return False
        return not _any_panel_would_show(context)

    def draw(self, context):
        layout = self.layout
        layout.separator(factor=1.0)

        box = layout.box()
        col = box.column(align=True)
        col.separator(factor=0.5)

        obj = context.active_object
        in_edit = obj and obj.type == 'MESH' and obj.mode == 'EDIT'

        if in_edit:
            row = col.row()
            row.label(text="No properties available", icon='INFO')
            col.separator(factor=0.3)
            col.label(text="Select a panel from the header.")
        else:
            row = col.row()
            row.label(text="No properties available", icon='INFO')
            col.separator(factor=0.3)
            col.label(text="Select a mesh and enter Edit Mode")
            col.label(text="to access UV properties.")

        col.separator(factor=0.5)


classes = (
    WEBSPIDER_UV_PT_empty_state,
)
