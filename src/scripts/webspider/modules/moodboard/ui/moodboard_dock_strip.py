# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Moodboard Dock Strip

Bottom footer bar showing active job progress.
Feature buttons have moved to the right Generate panel (N-panel, UI region).
"""

import bpy
from bpy.types import Header


from webspider.modules.common.utils.webspider_ai_space_utils import WEBSPIDER_AI_SPACE_AVAILABLE


if WEBSPIDER_AI_SPACE_AVAILABLE:

    class WEBSPIDER_AI_HT_dock_strip(Header):
        """Dock strip with feature buttons"""
        bl_space_type = 'WEBSPIDER_AI'
        bl_region_type = 'FOOTER'

        def draw(self, context):
            layout = self.layout
            layout.template_running_jobs()


    classes = (
        WEBSPIDER_AI_HT_dock_strip,
    )

else:
    classes = ()
