# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Functions Operators

Operators for UV functions (seam, pin, merge, split, hide, copy/paste) in the WebSpider 3D UV Editor.
"""

import bpy
from bpy.types import Operator

from webspider.modules.uv_editor.common.uv_utils import (
    poll_webspider3d_uv_edit_mode,
    with_uv_context,
    with_uv_context_and_region,
    get_operator_properties,
)


# =============================================================================
# UV Functions - Seam, Pin, Merge, Split, Hide
# =============================================================================

class WEBSPIDER_OT_mark_seam(Operator):
    """Mark selected edges as seam"""
    bl_idname = "webspider.mark_seam"
    bl_label = "Mark Seam"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.mark_seam(clear=False)
        return {'FINISHED'}


class WEBSPIDER_OT_clear_seam(Operator):
    """Clear seam from selected edges"""
    bl_idname = "webspider.clear_seam"
    bl_label = "Clear Seam"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.mark_seam(clear=True)
        return {'FINISHED'}


class WEBSPIDER_OT_seams_from_islands(Operator):
    """Set seams based on UV islands"""
    bl_idname = "webspider.seams_from_islands"
    bl_label = "Seam from Islands"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.seams_from_islands()
        return {'FINISHED'}


class WEBSPIDER_OT_stitch(Operator):
    """Stitch selected UV vertices by proximity (modal interactive)"""
    bl_idname = "webspider.stitch"
    bl_label = "Stitch"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context_and_region
    def execute(self, context, area, region):
        op_props = get_operator_properties(context, "uv.stitch")
        with context.temp_override(area=area, region=region):
            # Invoke with stored properties for modal interaction
            bpy.ops.uv.stitch(
                'INVOKE_DEFAULT',
                use_limit=op_props.use_limit,
                snap_islands=op_props.snap_islands,
                limit=op_props.limit,
                static_island=op_props.static_island,
                midpoint_snap=op_props.midpoint_snap,
                clear_seams=op_props.clear_seams,
                mode=op_props.mode,
            )
        return {'FINISHED'}


class WEBSPIDER_OT_weld(Operator):
    """Weld selected UVs at center"""
    bl_idname = "webspider.weld"
    bl_label = "Merge at Center"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.weld()
        return {'FINISHED'}


class WEBSPIDER_OT_merge_at_cursor(Operator):
    """Merge selected UVs at cursor"""
    bl_idname = "webspider.merge_at_cursor"
    bl_label = "Merge at Cursor"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.snap_selected(target='CURSOR')
        return {'FINISHED'}


class WEBSPIDER_OT_remove_doubles(Operator):
    """Merge UVs by distance"""
    bl_idname = "webspider.remove_doubles"
    bl_label = "Merge by Distance"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        op_props = get_operator_properties(context, "uv.remove_doubles")
        with context.temp_override(area=area):
            bpy.ops.uv.remove_doubles(threshold=op_props.threshold)
        return {'FINISHED'}


class WEBSPIDER_OT_select_split(Operator):
    """Split selected UVs"""
    bl_idname = "webspider.select_split"
    bl_label = "Split"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.select_split()
        return {'FINISHED'}


class WEBSPIDER_OT_pin(Operator):
    """Pin selected UVs"""
    bl_idname = "webspider.pin"
    bl_label = "Pin"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.pin(clear=False)
        return {'FINISHED'}


class WEBSPIDER_OT_unpin(Operator):
    """Unpin selected UVs"""
    bl_idname = "webspider.unpin"
    bl_label = "Unpin"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.pin(clear=True)
        return {'FINISHED'}


class WEBSPIDER_OT_invert_pin(Operator):
    """Invert pin state of selected UVs"""
    bl_idname = "webspider.invert_pin"
    bl_label = "Invert Pin"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.pin(invert=True)
        return {'FINISHED'}


class WEBSPIDER_OT_hide_selected(Operator):
    """Hide selected UV faces"""
    bl_idname = "webspider.hide_selected"
    bl_label = "Hide Selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.hide(unselected=False)
        return {'FINISHED'}


class WEBSPIDER_OT_reveal(Operator):
    """Reveal hidden UV faces"""
    bl_idname = "webspider.reveal"
    bl_label = "Reveal"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.reveal()
        return {'FINISHED'}


class WEBSPIDER_OT_hide_unselected(Operator):
    """Hide unselected UV faces"""
    bl_idname = "webspider.hide_unselected"
    bl_label = "Hide Unselected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.hide(unselected=True)
        return {'FINISHED'}


class WEBSPIDER_OT_copy_uvs(Operator):
    """Copy selected UVs"""
    bl_idname = "webspider.copy_uvs"
    bl_label = "Copy UVs"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.copy()
        return {'FINISHED'}


class WEBSPIDER_OT_paste_uvs(Operator):
    """Paste UVs"""
    bl_idname = "webspider.paste_uvs"
    bl_label = "Paste UVs"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return poll_webspider3d_uv_edit_mode(context)

    @with_uv_context
    def execute(self, context, area):
        with context.temp_override(area=area):
            bpy.ops.uv.paste()
        return {'FINISHED'}


classes = (
    WEBSPIDER_OT_mark_seam,
    WEBSPIDER_OT_clear_seam,
    WEBSPIDER_OT_seams_from_islands,
    WEBSPIDER_OT_stitch,
    WEBSPIDER_OT_weld,
    WEBSPIDER_OT_merge_at_cursor,
    WEBSPIDER_OT_remove_doubles,
    WEBSPIDER_OT_select_split,
    WEBSPIDER_OT_pin,
    WEBSPIDER_OT_unpin,
    WEBSPIDER_OT_invert_pin,
    WEBSPIDER_OT_hide_selected,
    WEBSPIDER_OT_reveal,
    WEBSPIDER_OT_hide_unselected,
    WEBSPIDER_OT_copy_uvs,
    WEBSPIDER_OT_paste_uvs,
)
