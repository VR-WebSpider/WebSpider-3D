# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Moodboard Chat Integration Operators

Thin wrappers around ``moodboard.core.chat_sync``. Auto-sync now
mirrors selected moodboard images into the chat composer's pending
attachments on a polling tick — this operator used to do that work
manually (file picker, duplicate checks, attachment cap, etc.) and
those code paths have been retired. The operator is kept so the
existing toolbar entry and ``P`` keymap binding stay functional;
hitting it just nudges the sync to run immediately, useful as a
"force refresh" if anything ever desynchronises.
"""

from bpy.types import Operator

from ....common.utils.platform_utils import format_shortcut


def get_all_image_indices_to_send(scene):
    """
    Get all image indices that should be sent to chat.
    This includes directly selected images and images from selected groups.

    Kept as a public helper because other moodboard ops (image-to-3D,
    lookdev, etc.) call it to know which images the user has staged.
    """
    image_indices = set()

    # Get selected group indices
    selected_group_indices = set()
    for i, group in enumerate(scene.webspider_ai_moodboard_groups):
        if group.selected:
            selected_group_indices.add(i)

    # Get group indices from selected images (group cohesion)
    for img in scene.webspider_ai_moodboard_images:
        if img.selected and img.group_index >= 0:
            selected_group_indices.add(img.group_index)

    # Collect images
    for i, img in enumerate(scene.webspider_ai_moodboard_images):
        if img.selected:
            image_indices.add(i)
        elif img.group_index in selected_group_indices:
            # Image belongs to a group being sent
            image_indices.add(i)

    return image_indices


class WEBSPIDER_AI_OT_moodboard_send_to_chat(Operator):
    """Force the moodboard→chat sync to run immediately.

    Retained for the existing toolbar entry and ``P`` keymap. The
    sync runs automatically every ~200 ms whenever selection changes;
    this operator is just a manual refresh.
    """
    bl_idname = "webspider_ai.moodboard_send_to_chat"
    bl_label = "Refresh Chat Attachments"
    bl_description = f"Refresh moodboard→chat attachment sync ({format_shortcut('P')})"
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        scene = context.scene
        if scene is None:
            return False
        if not hasattr(scene, 'webspider_ai_moodboard_images'):
            return False
        if not hasattr(scene, 'webspider_chat_pending_attachments'):
            return False
        return True

    def execute(self, context):
        scene = context.scene
        try:
            from webspider.modules.moodboard.core.chat_sync import (
                force_resync,
                _reconcile_attachments,
                _collect_selected_image_names,
            )
            force_resync(scene)
            _reconcile_attachments(scene, _collect_selected_image_names(scene))
        except Exception as e:  # noqa: BLE001 — keep the keymap functional
            self.report({'WARNING'}, f"Sync failed: {e}")
            return {'CANCELLED'}

        selected_count = sum(
            1 for att in scene.webspider_chat_pending_attachments
            if getattr(att, "is_moodboard", False)
        )
        if selected_count == 0:
            self.report({'INFO'}, "No moodboard images selected")
        else:
            self.report(
                {'INFO'},
                f"Synced {selected_count} moodboard image"
                f"{'s' if selected_count != 1 else ''}",
            )
        return {'FINISHED'}


class WEBSPIDER_AI_CHAT_OT_attach_moodboard_image(Operator):
    """Force a moodboard→chat sync — wrapper used in the chat footer so
    the tooltip reads "Attach Selected Moodboard Image" while the
    moodboard toolbar keeps the original label."""
    bl_idname = "webspider_ai_chat.attach_moodboard_image"
    bl_label = "Attach Selected Moodboard Image"
    bl_description = (
        f"Refresh moodboard→chat attachment sync ({format_shortcut('P')})"
    )
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return WEBSPIDER_AI_OT_moodboard_send_to_chat.poll(context)

    def execute(self, context):
        import bpy
        return bpy.ops.webspider_ai.moodboard_send_to_chat()


classes = (
    WEBSPIDER_AI_OT_moodboard_send_to_chat,
    WEBSPIDER_AI_CHAT_OT_attach_moodboard_image,
)
