# SPDX-FileCopyrightText: 2026 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Welcome / Skip Operators

Thin shims around the unified ``WEBSPIDER_OT_onboarding_card`` modal:

* :class:`WEBSPIDER_OT_onboarding_welcome` — entry point used by
  Bootstrap (and Help → Welcome). Begins the tour state and routes
  to the card modal with ``step_id = STEP_WELCOME``.

* :class:`WEBSPIDER_OT_onboarding_pick_skip` — kept for backwards
  compatibility with menus / other call sites that still invoke
  the old "skip from welcome" idname.
"""

import bpy
from bpy.types import Operator

from webspider.config.logging_config import get_logger
from webspider.modules.onboarding.constants import (
    OP_CARD_MODAL,
    OP_PICK_SKIP,
    OP_WELCOME,
    STEP_WELCOME,
)

logger = get_logger(__name__)


class WEBSPIDER_OT_onboarding_welcome(Operator):
    """Show the WebSpider 3D welcome card."""

    bl_idname = OP_WELCOME
    bl_label = "Welcome to WebSpider 3D"
    bl_description = "Open the WebSpider 3D welcome card"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        from webspider.modules.onboarding.ui.operators.card_modal_op import (
            is_card_active,
        )

        # Guard against duplicate welcome cards: several triggers (auth
        # hook, mode-pick nudge, dev fallback) can each fire the welcome
        # near session start. If a card is already on screen, this call is
        # a no-op — otherwise a second modal stacks and the first stays
        # stuck behind the tour.
        if is_card_active():
            logger.debug("Onboarding welcome: a card is already active; skip")
            return {"FINISHED"}

        if state.is_opted_out(context):
            state.reset(context)
        else:
            state.begin(context)
        # Route directly into the welcome step. transition_to runs
        # the tour driver, which invokes the card modal — same path
        # every other step uses.
        state.transition_to(STEP_WELCOME)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class WEBSPIDER_OT_onboarding_pick_skip(Operator):
    """Skip onboarding for this session."""

    bl_idname = OP_PICK_SKIP
    bl_label = "I'll figure it out myself"
    bl_description = "Skip the welcome flow and go straight to the editor"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        state.skip_tour(context)
        return {"FINISHED"}


classes = (
    WEBSPIDER_OT_onboarding_welcome,
    WEBSPIDER_OT_onboarding_pick_skip,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
