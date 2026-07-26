# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider AI Space Header

Header definition for the WebSpider AI space.

NOTE: the animated per-generation loading indicator that used to live
here ("Generating Image [□■□□□]" + a 100ms redraw timer) was removed —
the Queue panel is the single place generation progress is shown.
"""

import bpy
from bpy.types import Header, Menu


def _has_moodboard_content(context):
    """Check if there is any content in the moodboard."""
    scene = context.scene
    has_content = False
    if hasattr(scene, 'webspider_ai_moodboard_images') and len(scene.webspider_ai_moodboard_images) > 0:
        has_content = True
    if hasattr(scene, 'webspider_ai_moodboard_textboxes') and len(scene.webspider_ai_moodboard_textboxes) > 0:
        has_content = True
    return has_content


class WEBSPIDER_AI_MT_view(Menu):
    bl_label = "View"

    def draw(self, context):
        layout = self.layout

        # Toggle toolbar visibility
        layout.operator(
            "screen.region_toggle",
            text="Toolbar",
            icon='CHECKBOX_HLT' if WEBSPIDER_AI_HT_header._is_toolbar_visible(context) else 'CHECKBOX_DEHLT'
        ).region_type = 'TOOLS'

        # Toggle sidebar visibility
        layout.operator(
            "screen.region_toggle",
            text="Sidebar",
            icon='CHECKBOX_HLT' if WEBSPIDER_AI_HT_header._is_sidebar_visible(context) else 'CHECKBOX_DEHLT'
        ).region_type = 'UI'


class WEBSPIDER_AI_HT_header(Header):
    bl_space_type = 'WEBSPIDER_AI'

    @staticmethod
    def _is_toolbar_visible(context):
        for region in context.area.regions:
            if region.type == 'TOOLS':
                # Region is visible if it has non-zero width
                return region.width > 0
        return False

    @staticmethod
    def _is_sidebar_visible(context):
        for region in context.area.regions:
            if region.type == 'UI':
                # Region is visible if it has non-zero width
                return region.width > 0
        return False

    def draw(self, context):
        layout = self.layout
        layout.template_header()

        layout.label(text="Moodboard")

        # Add View menu (commented out)
        # layout.menu("WEBSPIDER_AI_MT_view")

        # Show "Clear Moodboard" button when there is content in moodboard
        if _has_moodboard_content(context):
            layout.separator_spacer()
            row = layout.row(align=True)
            row.operator(
                "webspider_ai.clear_moodboard",
                text="Clear Moodboard",
                icon='X'
            )


classes = (
    WEBSPIDER_AI_MT_view,
    WEBSPIDER_AI_HT_header,
)
