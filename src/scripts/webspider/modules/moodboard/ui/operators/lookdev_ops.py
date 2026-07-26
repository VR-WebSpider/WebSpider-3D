# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Lookdev Operators

Entry-point operator that validates the prompt and delegates to the
scene-based generation operator, plus a utility file-picker operator.
"""

import bpy
from bpy.types import Operator

from ....common.utils.file_select_utils import file_select_guard, mark_file_select_executed
from webspider.config.logging_config import get_logger

logger = get_logger(__name__)


def _get_lookdev_props(scene):
    """Get lookdev tab properties from sidebar."""
    if hasattr(scene, 'webspider_ai_moodboard_sidebar') and scene.webspider_ai_moodboard_sidebar:
        sidebar = scene.webspider_ai_moodboard_sidebar
        if hasattr(sidebar, 'tab_lookdev'):
            return sidebar.tab_lookdev
    return None


class WEBSPIDER_AI_OT_lookdev_generate(Operator):
    """Generate an image from a depth map using the Lookdev API (Flux Depth)"""

    bl_idname = "webspider_ai.lookdev_generate"
    bl_label = "Generate Lookdev"
    bl_description = "Generate an image from a depth map using Flux Depth AI model"
    bl_options = {'REGISTER'}

    def execute(self, context):
        scene = context.scene
        props = _get_lookdev_props(scene)

        if props:
            prompt = props.prompt
            if not prompt or not prompt.strip():
                fallback = getattr(scene, 'webspider_ai_lookdev_prompt', '')
                if fallback and fallback.strip():
                    prompt = fallback
        else:
            prompt = getattr(scene, 'webspider_ai_lookdev_prompt', '')

        if not prompt or not prompt.strip():
            self.report({'WARNING'}, "Please enter a prompt (press Enter to confirm your text)")
            return {'CANCELLED'}

        # Always render depth from the 3D scene
        return bpy.ops.webspider_ai.lookdev_generate_from_scene()


class WEBSPIDER_AI_OT_lookdev_pick_depth_image(Operator):
    """Pick a depth map image file"""

    bl_idname = "webspider_ai.lookdev_pick_depth_image"
    bl_label = "Pick Depth Map"
    bl_description = "Select a depth map image file"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to the depth map image file",
        subtype='FILE_PATH'
    )

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.jpg;*.jpeg;*.bmp;*.tga;*.tiff;*.webp;*.exr",
        options={'HIDDEN'}
    )

    def invoke(self, context, event):
        if not file_select_guard(self, context):
            return {'FINISHED'}
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        import os

        if not self.filepath:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}

        try:
            filepath = os.path.abspath(os.path.realpath(self.filepath))
        except (OSError, ValueError) as e:
            self.report({'ERROR'}, f"Invalid file path: {e}")
            return {'CANCELLED'}

        if not os.path.isfile(filepath):
            self.report({'ERROR'}, f"File not found: {filepath}")
            return {'CANCELLED'}

        try:
            img = bpy.data.images.load(filepath, check_existing=True)
            img.pack()
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load image: {e}")
            return {'CANCELLED'}

        context.scene.webspider_ai_lookdev_depth_image = img
        self.report({'INFO'}, f"Selected '{img.name}' as depth map")
        mark_file_select_executed(self)
        return {'FINISHED'}


classes = (
    WEBSPIDER_AI_OT_lookdev_generate,
    WEBSPIDER_AI_OT_lookdev_pick_depth_image,
)
