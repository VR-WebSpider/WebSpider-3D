# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Set Operators

Operators for UV set operations (UDIM tiles) in the WebSpider 3D UV Editor.
"""

import bpy
from bpy.types import Operator

from webspider.modules.uv_editor.common.uv_utils import (
    get_webspider3d_uv_image_editor,
)


class WEBSPIDER_OT_image_new(Operator):
    """Create a new image (Tiled enabled by default)

    Wrapper around `image.new` that pre-sets `tiled=True` on the
    operator's property dialog. Used as the `new=` operator for
    `template_ID` in WebSpider 3D UV panels so the dialog opens with the
    Tiled checkbox already checked. The underlying `image.new` does
    the actual creation and ID assignment.
    """
    bl_idname = "webspider.image_new"
    bl_label = "New Image"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return bpy.ops.image.new('INVOKE_DEFAULT', tiled=True)

    def execute(self, context):
        return bpy.ops.image.new(tiled=True)


class WEBSPIDER_OT_tile_add(Operator):
    """Add UDIM tile"""
    bl_idname = "webspider.tile_add"
    bl_label = "Add Tile"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        area = get_webspider3d_uv_image_editor(context)
        if not area:
            return False
        sima = area.spaces.active
        return sima and sima.image and sima.image.source == 'TILED'

    def execute(self, context):
        area = get_webspider3d_uv_image_editor(context)
        if not area:
            return {'CANCELLED'}
        with context.temp_override(area=area, space_data=area.spaces.active):
            bpy.ops.image.tile_add('INVOKE_DEFAULT')
        return {'FINISHED'}


class WEBSPIDER_OT_tile_remove(Operator):
    """Remove UDIM tile"""
    bl_idname = "webspider.tile_remove"
    bl_label = "Remove Tile"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        area = get_webspider3d_uv_image_editor(context)
        if not area:
            return False
        sima = area.spaces.active
        if not (sima and sima.image and sima.image.source == 'TILED'):
            return False
        # Check if there's an active tile to remove
        return sima.image.tiles and len(sima.image.tiles) > 0

    def execute(self, context):
        area = get_webspider3d_uv_image_editor(context)
        if not area:
            return {'CANCELLED'}
        with context.temp_override(area=area, space_data=area.spaces.active):
            bpy.ops.image.tile_remove()
        return {'FINISHED'}


class WEBSPIDER_OT_tile_fill(Operator):
    """Fill UDIM tile"""
    bl_idname = "webspider.tile_fill"
    bl_label = "Fill Tile"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        area = get_webspider3d_uv_image_editor(context)
        if not area:
            return False
        sima = area.spaces.active
        if not (sima and sima.image and sima.image.source == 'TILED'):
            return False
        # Check if there's an active tile
        return sima.image.tiles and sima.image.tiles.active

    def execute(self, context):
        area = get_webspider3d_uv_image_editor(context)
        if not area:
            return {'CANCELLED'}
        with context.temp_override(area=area, space_data=area.spaces.active):
            bpy.ops.image.tile_fill('INVOKE_DEFAULT')
        return {'FINISHED'}


classes = (
    WEBSPIDER_OT_image_new,
    WEBSPIDER_OT_tile_add,
    WEBSPIDER_OT_tile_remove,
    WEBSPIDER_OT_tile_fill,
)
