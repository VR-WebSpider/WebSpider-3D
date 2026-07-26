# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider Chat Login Panel

Login panel for user authentication via browser SSO.
"""

import bpy
from bpy.types import Panel


class WEBSPIDER_AI_CHAT_PT_login(Panel):
    """Login panel for WebSpider Chat"""
    bl_label = "Login"
    bl_idname = "WEBSPIDER_AI_CHAT_PT_login"
    bl_space_type = 'WEBSPIDER_AI_CHAT'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(cls, context):
        """Only show when not logged in"""
        wm = context.window_manager
        return not wm.webspider_chat_is_logged_in

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        col = layout.column(align=True)

        # Session expired message
        if getattr(wm, 'webspider_chat_session_expired', False):
            box = col.box()
            box.alert = True
            box.label(text="Session expired", icon='ERROR')
            box.label(text="Please log in again.")
            col.separator()

        # Show error if present (non-expired errors)
        elif wm.webspider_chat_login_error:
            error_box = col.box()
            error_box.alert = True
            error_col = error_box.column(align=True)
            error_col.label(text="Login Failed", icon='ERROR')
            # Word wrap error message (max ~30 chars per line)
            words = wm.webspider_chat_login_error.split()
            line = ""
            for word in words:
                if len(line) + len(word) + 1 > 30:
                    error_col.label(text=line)
                    line = word
                else:
                    line = f"{line} {word}".strip()
            if line:
                error_col.label(text=line)
            col.separator()

        col.label(text="Sign in with your WebSpider 3D account", icon='USER')
        col.separator()

        # SSO Login button
        if wm.webspider_chat_is_logging_in:
            row = col.row()
            row.enabled = False
            row.operator("webspider_ai_chat.login", text="Waiting for browser...", icon='SORTTIME')
        else:
            col.operator("webspider_ai_chat.login", text="Login with Browser", icon='URL')


classes = (
    WEBSPIDER_AI_CHAT_PT_login,
)
