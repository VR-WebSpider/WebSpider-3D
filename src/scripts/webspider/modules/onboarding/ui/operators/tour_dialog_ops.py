# SPDX-FileCopyrightText: 2026 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Tour Step Operator Shims

The five info-step dialogs used to be standalone
``invoke_props_dialog`` operators. With the GPU-rendered
``WEBSPIDER_OT_onboarding_card`` modal in place, those dialogs no
longer exist — the card modal handles every step in a single
operator. We keep these tiny operators registered so ``OP_STEP_*``
idnames referenced from menus, the StepDef table, or external
keymaps still resolve. Each one just routes back through the
state machine to the matching step.
"""

from bpy.types import Operator

from webspider.modules.onboarding.constants import (
    OP_STEP_INFO_IMAGE_TO_3D,
    OP_STEP_INFO_IMAGEGEN,
    OP_STEP_INFO_WEBSPIDER_AI_CHAT,
    OP_STEP_INFO_MOODBOARD,
    OP_STEP_INFO_RETOPOLOGY,
    STEP_INFO_IMAGE_TO_3D,
    STEP_INFO_IMAGEGEN,
    STEP_INFO_WEBSPIDER_AI_CHAT,
    STEP_INFO_MOODBOARD,
    STEP_INFO_RETOPOLOGY,
)


class _StepShimBase:
    step_id: str = ""

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        state.transition_to(self.step_id, context)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class WEBSPIDER_OT_onboarding_info_moodboard(_StepShimBase, Operator):
    bl_idname = OP_STEP_INFO_MOODBOARD
    bl_label = "Moodboard"
    bl_options = {"REGISTER", "INTERNAL"}
    step_id = STEP_INFO_MOODBOARD


class WEBSPIDER_OT_onboarding_info_imagegen(_StepShimBase, Operator):
    bl_idname = OP_STEP_INFO_IMAGEGEN
    bl_label = "Image Gen"
    bl_options = {"REGISTER", "INTERNAL"}
    step_id = STEP_INFO_IMAGEGEN


class WEBSPIDER_OT_onboarding_info_image_to_3d(_StepShimBase, Operator):
    bl_idname = OP_STEP_INFO_IMAGE_TO_3D
    bl_label = "Image to 3D"
    bl_options = {"REGISTER", "INTERNAL"}
    step_id = STEP_INFO_IMAGE_TO_3D


class WEBSPIDER_OT_onboarding_info_retopology(_StepShimBase, Operator):
    bl_idname = OP_STEP_INFO_RETOPOLOGY
    bl_label = "Retopology"
    bl_options = {"REGISTER", "INTERNAL"}
    step_id = STEP_INFO_RETOPOLOGY


class WEBSPIDER_OT_onboarding_info_webspider_ai_chat(_StepShimBase, Operator):
    bl_idname = OP_STEP_INFO_WEBSPIDER_AI_CHAT
    bl_label = "WebSpider Chat"
    bl_options = {"REGISTER", "INTERNAL"}
    step_id = STEP_INFO_WEBSPIDER_AI_CHAT


classes = (
    WEBSPIDER_OT_onboarding_info_moodboard,
    WEBSPIDER_OT_onboarding_info_imagegen,
    WEBSPIDER_OT_onboarding_info_image_to_3d,
    WEBSPIDER_OT_onboarding_info_retopology,
    WEBSPIDER_OT_onboarding_info_webspider_ai_chat,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
