# SPDX-FileCopyrightText: 2026 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Completion Operator (compatibility shim)

The completion screen is now rendered by ``WEBSPIDER_OT_onboarding_card``
with ``step_id = STEP_COMPLETION``. This file keeps ``OP_COMPLETION``
registered for backwards compatibility with menus / call sites that
still reference the old idname — it just transitions the state
machine to ``STEP_COMPLETION``, and the tour driver opens the card.
"""

from bpy.types import Operator

from webspider.config.logging_config import get_logger
from webspider.modules.onboarding.constants import (
    OP_COMPLETION,
    STEP_COMPLETION,
)

logger = get_logger(__name__)


class WEBSPIDER_OT_onboarding_completion(Operator):
    """Open the onboarding completion card."""

    bl_idname = OP_COMPLETION
    bl_label = "Done"
    bl_description = "Show the onboarding completion card"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        state.transition_to(STEP_COMPLETION, context)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


classes = (WEBSPIDER_OT_onboarding_completion,)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
