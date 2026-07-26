# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Auto Rig Tab Drawer — Tripo auto-rigging.

Renders the Auto Rig sidebar tab from the generation catalog's
``animate`` capability (single service ``tripo_rig`` — the Mode dropdown
auto-hides). Catalog-only (like AI Render): the panel's ``poll()`` hides
the tab when the loaded catalog has no animate services, so this drawer
can assume the catalog is loaded.
"""

from webspider.modules.common.job_queue.constants import FEATURE_ANIMATE

from .sidebar_ui_helpers import (
    draw_section_box, draw_section_separator, draw_generate_footer,
    draw_hint, draw_mesh_info,
)


def _draw_animate(layout, context):
    """Draw the catalog-driven Auto Rig tab."""
    scene = context.scene
    sidebar = getattr(scene, "webspider_ai_moodboard_sidebar", None)
    tab = getattr(sidebar, "tab_animate", None) if sidebar else None
    if tab is None:
        draw_hint(layout, "Auto Rig tab not available", icon='ERROR')
        return

    from webspider.modules.common.generation_params import draw_capability_selector

    # --- Mesh info ---
    col = draw_section_box(layout, "Mesh Info", icon='MESH_DATA')
    draw_mesh_info(col, context, max_mb=150)
    draw_hint(layout, "Select the meshes you want to auto-rig", icon='INFO')
    draw_section_separator(layout)

    # --- Settings (Model / schema params from the catalog) ---
    col = draw_section_box(layout, "Settings", icon='SETTINGS')
    col.use_property_split = True
    col.use_property_decorate = False
    draw_capability_selector(col, tab, "animate")

    info = draw_section_box(layout, "About", icon='INFO')
    draw_hint(info, "Auto-detects the skeleton type", icon='DOT')
    draw_hint(info, "Works best on character-like meshes", icon='DOT')
    draw_hint(info, "Max mesh: 150 MB (GLB)", icon='DOT')

    # --- Generate ---
    draw_generate_footer(
        layout, context, "webspider_ai.animate_generate", "animate",
        gen_flag_attr="webspider_ai_animate_is_generating",
        feature_key=FEATURE_ANIMATE,
    )
