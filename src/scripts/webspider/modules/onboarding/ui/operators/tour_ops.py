# SPDX-FileCopyrightText: 2026 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Onboarding Tour Operators

Three operators that drive transitions during the tour itself:

* ``WEBSPIDER_OT_onboarding_advance`` — wired to every tour toast's
  primary "Continue" button. Looks up the current step's declared
  next step and transitions there.
* ``WEBSPIDER_OT_onboarding_skip_tour`` — wired to every tour toast's
  secondary "Skip tour" button. Marks the session opted-out and
  parks the state at DONE.
* ``WEBSPIDER_OT_onboarding_restart`` — explicit reset entry point.
  Currently unused by any UI, but exposed for dev panels and a
  future "Restart tour" affordance.
"""

import bpy
from bpy.types import Operator

from webspider.config.logging_config import get_logger
from webspider.modules.onboarding.constants import (
    OP_ADVANCE,
    OP_RESTART,
    OP_SKIP_TOUR,
    OP_WELCOME,
)

logger = get_logger(__name__)


class WEBSPIDER_OT_onboarding_advance(Operator):
    """Move the onboarding flow to the next step."""

    bl_idname = OP_ADVANCE
    bl_label = "Continue"
    bl_description = "Advance the WebSpider 3D onboarding flow to the next step"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        state.advance(context)
        return {"FINISHED"}


class WEBSPIDER_OT_onboarding_skip_tour(Operator):
    """Skip the onboarding tour for this session."""

    bl_idname = OP_SKIP_TOUR
    bl_label = "Skip tour"
    bl_description = "Skip the rest of the onboarding tour"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        state.skip_tour(context)
        return {"FINISHED"}


class WEBSPIDER_OT_onboarding_restart(Operator):
    """Reset onboarding state and re-open the welcome dialog."""

    bl_idname = OP_RESTART
    bl_label = "Restart Onboarding"
    bl_description = "Reset onboarding state and reopen the welcome dialog"
    bl_options = {"REGISTER", "INTERNAL"}

    def execute(self, context):
        from webspider.modules.onboarding.core import state
        state.reset(context)
        namespace, name = OP_WELCOME.split(".", 1)
        try:
            getattr(getattr(bpy.ops, namespace), name)("INVOKE_DEFAULT")
        except Exception as exc:
            logger.warning("Onboarding: restart failed to reopen welcome: %s", exc)
            return {"CANCELLED"}
        return {"FINISHED"}


classes = (
    WEBSPIDER_OT_onboarding_advance,
    WEBSPIDER_OT_onboarding_skip_tour,
    WEBSPIDER_OT_onboarding_restart,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
