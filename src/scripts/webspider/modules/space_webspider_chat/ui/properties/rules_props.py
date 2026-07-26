# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Project Rules Properties

``scene.webspider_chat_rules`` holds the persisted rules store — a compact
JSON list of ``{"text", "enabled"}`` entries (see ``core/rules.py``; a
legacy plain-text value parses as one enabled rule). Enabled rules are
concatenated and prepended to the first message of every new chat
session. The property is deliberately persisted (no SKIP_SAVE): rules
belong to the .webspider3d file and must survive save/reload, but a brand new
file starts with the default empty string.

Chats are per-scene (one agent per scene), while rules are per-FILE — the
update callback mirrors every edit onto all other scenes so each scene's
chat sends the same rules. Scenes created after the last edit start empty;
``core/rules.py:get_raw_rules`` falls back to any non-empty scene for
that case.

The C++ rules overlay never parses the JSON: it reads the
``WindowManager.webspider_chat_rule_entries`` mirror (rebuilt by
``rules_ops.sync_rule_entries`` on overlay open and after every rule
operator), exactly like the history overlay reads its entries mirror.
"""

import bpy
from bpy.props import BoolProperty, CollectionProperty, StringProperty
from bpy.types import PropertyGroup

from webspider.config.logging_config import get_logger
from ...constants import CHAT_RULES_MAXLEN

logger = get_logger(__name__)

# Reentrancy guard: mirroring writes other scenes' webspider_chat_rules, which
# fires this same callback on each of them.
_syncing_rules = False


class WebSpiderAIChatRuleEntry(PropertyGroup):
    """One rule card row for the C++ rules overlay (runtime mirror)."""

    text: StringProperty(
        name="Rule Text",
        description="The rule as typed by the user",
        default="",
        maxlen=CHAT_RULES_MAXLEN,
    )
    enabled: BoolProperty(
        name="Enabled",
        description="Disabled rules stay in the list but are not sent",
        default=True,
    )
    is_global: BoolProperty(
        name="Global",
        description="Global rules apply to every .webspider3d file "
                    "(~/.webspider3d/global_rules.json); others to this file only",
        default=False,
    )


def on_chat_rules_changed(self, context):
    """Mirror the edited rules store onto every other scene in the file."""
    global _syncing_rules
    if _syncing_rules:
        return
    _syncing_rules = True
    try:
        value = self.webspider_chat_rules
        for scn in bpy.data.scenes:
            if scn != self and scn.webspider_chat_rules != value:
                scn.webspider_chat_rules = value
    except Exception:
        logger.debug("rules cross-scene sync failed", exc_info=True)
    finally:
        _syncing_rules = False


classes = (WebSpiderAIChatRuleEntry,)


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass  # already registered (module reload)

    bpy.types.Scene.webspider_chat_rules = StringProperty(
        name="Project Rules",
        description=(
            "Rules the WebSpider AI agent must always follow in this file "
            "(JSON list store; enabled rules are sent along with the "
            "first message of every new chat)"
        ),
        default="",
        maxlen=CHAT_RULES_MAXLEN,
        update=on_chat_rules_changed,
    )

    # Fingerprint of the enabled-rules text last SENT to this scene's
    # session (core/rules.py:mark_rules_sent). compose_wire_message
    # compares it on every continuation send — a mismatch means the user
    # changed the rules mid-session, and the current complete set is
    # re-sent under a strict supersede header. SKIP_SAVE: after a file
    # reload the fingerprint is unknown, so the next send re-states the
    # rules once — harmless, and correct for sessions reopened from
    # history whose rules may have changed since.
    bpy.types.Scene.webspider_chat_rules_sent_hash = StringProperty(
        name="Rules Sent Fingerprint",
        default="",
        maxlen=64,
        options={'SKIP_SAVE', 'HIDDEN'},
    )

    # Runtime mirror of the parsed store, read by the C++ overlay for the
    # rule cards. Session state, never persisted.
    bpy.types.WindowManager.webspider_chat_rule_entries = CollectionProperty(
        type=WebSpiderAIChatRuleEntry,
        name="Project Rule Entries",
        options={'SKIP_SAVE'},
    )

    # Visibility of the C++-drawn rules overlay in the chat main region
    # (webspider_chat_rules_overlay.cc) — written here (header toggle) and by
    # the C++ overlay (ESC / click-away / close X all clear it). Same
    # contract as webspider_chat_history_visible.
    bpy.types.WindowManager.webspider_chat_rules_visible = BoolProperty(
        name="Project Rules Visible",
        description="Whether the project-rules overlay is open",
        default=False,
        options={'SKIP_SAVE'},
    )


def unregister():
    for owner, attr in (
        (bpy.types.Scene, 'webspider_chat_rules'),
        (bpy.types.Scene, 'webspider_chat_rules_sent_hash'),
        (bpy.types.WindowManager, 'webspider_chat_rule_entries'),
        (bpy.types.WindowManager, 'webspider_chat_rules_visible'),
    ):
        if hasattr(owner, attr):
            delattr(owner, attr)
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception:
            pass
