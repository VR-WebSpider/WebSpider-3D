# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Texel Density Panel

Texel density panel wrapper for the WebSpider 3D UV Properties space.
Delegates drawing to the texel_density module.
"""

from bpy.types import Panel

from webspider.modules.uv_editor.ui.base.panels import poll_header_panel
from webspider.modules.texel_density.texel.ui import panel_draw


class WEBSPIDER_UV_PT_texel_density(Panel):
    """Texel Density panel for WebSpider 3D UV Properties space"""
    bl_label = "Texel Density"
    bl_idname = "WEBSPIDER_UV_PT_texel_density"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'CHANNELS'
    bl_options = set()
    # Header-driven panels sort in the middle band (above Selection /
    # UV Tool / Functions / Transform = 100, below UV Sculpt Tools /
    # Annotate = -10).
    bl_order = 50

    @classmethod
    def poll(cls, context):
        return poll_header_panel(
            context, 'TEXEL_DENSITY', requires_mesh_data=True)

    def draw(self, context):
        layout = self.layout

        # Top padding for parent panel
        layout.separator(factor=0.5)

        layout.use_property_split = True
        layout.use_property_decorate = False

        panel_draw(layout, context)


classes = (
    WEBSPIDER_UV_PT_texel_density,
)
