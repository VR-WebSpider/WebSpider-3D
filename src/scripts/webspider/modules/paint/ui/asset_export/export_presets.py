# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Export preset operators and menus for glTF, OBJ, and FBX formats.

Uses Blender's AddPresetBase machinery to provide:
- Built-in engine presets (Unity, Unreal, Godot) shipped via overlay
- User-saveable presets persisted to the Blender user config directory
"""

import bpy
from bl_operators.presets import AddPresetBase


# ---------------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------------

_SKIP_PROPS = frozenset(('rna_type', 'name'))


def _preset_values_for(pg_type):
    """Return a list of 'varname.prop' strings for every user-facing property."""
    return [
        f"gs.{p.identifier}"
        for p in pg_type.bl_rna.properties
        if p.identifier not in _SKIP_PROPS
    ]


# ---------------------------------------------------------------------------
#  glTF
# ---------------------------------------------------------------------------

class WEBSPIDER_OT_gltf_export_preset_add(AddPresetBase, bpy.types.Operator):
    bl_idname = "webspider.gltf_export_preset_add"
    bl_label = "Add glTF Export Preset"
    preset_menu = "WEBSPIDER_MT_gltf_export_presets"
    preset_subdir = "webspider3d/gltf_export"
    preset_defines = ["gs = bpy.context.window_manager.webspider3d_export_gltf"]

    @property
    def preset_values(self):
        return _preset_values_for(bpy.types.MGltfExportSettings)


class WEBSPIDER_MT_gltf_export_presets(bpy.types.Menu):
    bl_label = "glTF Export Presets"
    preset_subdir = "webspider3d/gltf_export"
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset


# ---------------------------------------------------------------------------
#  OBJ
# ---------------------------------------------------------------------------

class WEBSPIDER_OT_obj_export_preset_add(AddPresetBase, bpy.types.Operator):
    bl_idname = "webspider.obj_export_preset_add"
    bl_label = "Add OBJ Export Preset"
    preset_menu = "WEBSPIDER_MT_obj_export_presets"
    preset_subdir = "webspider3d/obj_export"
    preset_defines = ["gs = bpy.context.window_manager.webspider3d_export_obj"]

    @property
    def preset_values(self):
        return _preset_values_for(bpy.types.MObjExportSettings)


class WEBSPIDER_MT_obj_export_presets(bpy.types.Menu):
    bl_label = "OBJ Export Presets"
    preset_subdir = "webspider3d/obj_export"
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset


# ---------------------------------------------------------------------------
#  FBX
# ---------------------------------------------------------------------------

class WEBSPIDER_OT_fbx_export_preset_add(AddPresetBase, bpy.types.Operator):
    bl_idname = "webspider.fbx_export_preset_add"
    bl_label = "Add FBX Export Preset"
    preset_menu = "WEBSPIDER_MT_fbx_export_presets"
    preset_subdir = "webspider3d/fbx_export"
    preset_defines = ["gs = bpy.context.window_manager.webspider3d_export_fbx"]

    @property
    def preset_values(self):
        return _preset_values_for(bpy.types.MFbxExportSettings)


class WEBSPIDER_MT_fbx_export_presets(bpy.types.Menu):
    bl_label = "FBX Export Presets"
    preset_subdir = "webspider3d/fbx_export"
    preset_operator = "script.execute_preset"
    draw = bpy.types.Menu.draw_preset


# ---------------------------------------------------------------------------
#  Registration (auto-discovered by bootstrap via classes tuple)
# ---------------------------------------------------------------------------

classes = (
    WEBSPIDER_OT_gltf_export_preset_add,
    WEBSPIDER_MT_gltf_export_presets,
    WEBSPIDER_OT_obj_export_preset_add,
    WEBSPIDER_MT_obj_export_presets,
    WEBSPIDER_OT_fbx_export_preset_add,
    WEBSPIDER_MT_fbx_export_presets,
)
