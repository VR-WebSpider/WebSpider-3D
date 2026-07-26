# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Lookdev 360 Reference Image Operators

Operators for managing reference/style images and restoring materials
in the Lookdev 360 workflow.
"""

import bpy
from bpy.types import Operator
import os

from webspider.config.logging_config import get_logger
from ....common.utils.file_select_utils import file_select_guard, mark_file_select_executed
from ...core.lookdev360_utils import restore_material_checkpoint
from ...core.image_lifecycle import remove_image_safely

logger = get_logger(__name__)


def _get_lookdev360_props(scene):
    """Get lookdev360 tab properties from sidebar."""
    if hasattr(scene, 'webspider_ai_moodboard_sidebar') and scene.webspider_ai_moodboard_sidebar:
        sidebar = scene.webspider_ai_moodboard_sidebar
        if hasattr(sidebar, 'tab_lookdev360'):
            return sidebar.tab_lookdev360
    return None


class WEBSPIDER_AI_OT_lookdev360_upload_reference(Operator):
    """Upload a reference image for style transfer"""

    bl_idname = "webspider_ai.lookdev360_upload_reference"
    bl_label = "Upload Reference Image"
    bl_description = "Upload an image for PBR texture generation"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to the reference image file",
        subtype='FILE_PATH'
    )

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.jpg;*.jpeg;*.bmp;*.tga;*.tiff;*.webp",
        options={'HIDDEN'}
    )

    def invoke(self, context, event):
        if not file_select_guard(self, context):
            return {'FINISHED'}
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.filepath:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}

        # Validate path
        try:
            filepath = os.path.abspath(os.path.realpath(self.filepath))
        except (OSError, ValueError) as e:
            self.report({'ERROR'}, f"Invalid file path: {e}")
            return {'CANCELLED'}

        if not os.path.isfile(filepath):
            self.report({'ERROR'}, f"File not found: {filepath}")
            return {'CANCELLED'}

        # Load the image
        try:
            img = bpy.data.images.load(filepath, check_existing=True)
            img.pack()
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load image: {e}")
            return {'CANCELLED'}

        # Set as reference image in sidebar properties
        props = _get_lookdev360_props(context.scene)
        if props:
            props.reference_image = img
            # Switch to uploaded-image mode so the info card is visible
            props.use_selected_image = False

        # Redraw UI
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()

        self.report({'INFO'}, f"Added '{img.name}' as reference image")
        mark_file_select_executed(self)
        return {'FINISHED'}


class WEBSPIDER_AI_OT_lookdev360_remove_reference(Operator):
    """Remove the reference image"""

    bl_idname = "webspider_ai.lookdev360_remove_reference"
    bl_label = "Remove Reference Image"
    bl_description = "Remove the style reference image"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = _get_lookdev360_props(context.scene)
        if props:
            old_img = getattr(props, 'reference_image', None)
            props.reference_image = None
            remove_image_safely(old_img)

        # Redraw UI
        for area in context.screen.areas:
            if area.type == 'WEBSPIDER_AI':
                area.tag_redraw()

        self.report({'INFO'}, "Reference image removed")
        return {'FINISHED'}


class WEBSPIDER_AI_OT_lookdev360_pick_style_image(Operator):
    """Pick a style image file for Lookdev 360"""

    bl_idname = "webspider_ai.lookdev360_pick_style_image"
    bl_label = "Pick Style Image"
    bl_description = "Select a style reference image file"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Path to the style image file",
        subtype='FILE_PATH'
    )

    filter_glob: bpy.props.StringProperty(
        default="*.png;*.jpg;*.jpeg;*.bmp;*.tga;*.tiff;*.webp",
        options={'HIDDEN'}
    )

    def invoke(self, context, event):
        if not file_select_guard(self, context):
            return {'FINISHED'}
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.filepath:
            self.report({'WARNING'}, "No file selected")
            return {'CANCELLED'}

        # Validate path
        try:
            filepath = os.path.abspath(os.path.realpath(self.filepath))
        except (OSError, ValueError) as e:
            self.report({'ERROR'}, f"Invalid file path: {e}")
            return {'CANCELLED'}

        if not os.path.isfile(filepath):
            self.report({'ERROR'}, f"File not found: {filepath}")
            return {'CANCELLED'}

        # Load the image
        try:
            img = bpy.data.images.load(filepath, check_existing=True)
            img.pack()
        except Exception as e:
            self.report({'ERROR'}, f"Failed to load image: {e}")
            return {'CANCELLED'}

        # Set as style image
        context.scene.webspider_ai_lookdev360_style_image = img

        self.report({'INFO'}, f"Selected '{img.name}' as style image")
        mark_file_select_executed(self)
        return {'FINISHED'}


class WEBSPIDER_AI_OT_lookdev360_restore_materials(Operator):
    """Restore original materials from checkpoint"""

    bl_idname = "webspider_ai.lookdev360_restore_materials"
    bl_label = "Restore Materials"
    bl_description = "Restore original materials from before Lookdev 360 generation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        checkpoint = getattr(scene, 'webspider_ai_lookdev360_checkpoint', '')

        if not checkpoint:
            self.report({'WARNING'}, "No material checkpoint found")
            return {'CANCELLED'}

        success = restore_material_checkpoint(checkpoint)

        if success:
            # Clear checkpoint and reset flags
            if hasattr(scene, 'webspider_ai_lookdev360_checkpoint'):
                scene.webspider_ai_lookdev360_checkpoint = ""
            if hasattr(scene, 'webspider_ai_lookdev360_has_applied'):
                scene.webspider_ai_lookdev360_has_applied = False

            # Also reset sidebar property
            props = _get_lookdev360_props(scene)
            if props and hasattr(props, 'has_applied_materials'):
                props.has_applied_materials = False

            # Redraw UI
            for area in context.screen.areas:
                if area.type == 'WEBSPIDER_AI':
                    area.tag_redraw()

            self.report({'INFO'}, "Materials restored successfully")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Failed to restore materials")
            return {'CANCELLED'}


# Keep old name for backwards compatibility
class WEBSPIDER_AI_OT_lookdev360_restore(WEBSPIDER_AI_OT_lookdev360_restore_materials):
    """Alias for restore_materials (backwards compatibility)"""
    bl_idname = "webspider_ai.lookdev360_restore"


classes = (
    WEBSPIDER_AI_OT_lookdev360_upload_reference,
    WEBSPIDER_AI_OT_lookdev360_remove_reference,
    WEBSPIDER_AI_OT_lookdev360_pick_style_image,
    WEBSPIDER_AI_OT_lookdev360_restore_materials,
    WEBSPIDER_AI_OT_lookdev360_restore,
)


def register():
    """Register operator classes"""
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    """Unregister operator classes"""
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
