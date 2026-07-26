# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Moodboard Scene-Level Property Registration

Registers PropertyGroup classes and attaches collection/pointer properties
to bpy.types.Scene and bpy.types.WindowManager.

Architecture notes
------------------
This module has explicit register()/unregister() functions (rather than
relying solely on bootstrap auto-discovery) because it must wire up
bpy.types.Scene and bpy.types.WindowManager properties *after* the
PropertyGroup classes they reference have been registered. The bootstrap
auto-discovery system in ``startup/bootstrap/__init__.py`` excludes classes
that are already registered here, so there is no double-registration.

The ``try: register_class(cls) / except ValueError`` pattern inside
register() guards against hot-reloads (F8 or script re-run): Blender
raises ``ValueError`` when a class is already registered, which we catch
and silently skip so the rest of the property setup can proceed.
"""

import bpy
from bpy.props import (
    PointerProperty,
    CollectionProperty,
    FloatProperty,
    IntProperty,
    BoolProperty,
    StringProperty,
)

from webspider.config.logging_config import get_logger

from .moodboard_properties import (
    WebSpiderAIMoodboardSegment,
    WebSpiderAIMoodboardImage,
    WebSpiderAIMoodboardGroup,
    WebSpiderAIMoodboardTextBox,
)
from .moodboard_tab_properties import (
    WebSpiderAIMoodboardReferenceImage,
    WebSpiderAIMoodboardTabAIRenderProps,
    WebSpiderAIMoodboardTabImageGenProps,
    WebSpiderAIMoodboardTabLookdevProps,
    WebSpiderAIMoodboardTabLookdev360Props,
    WebSpiderAIMoodboardTabImageTo3DProps,
    WebSpiderAIMoodboardTabSegmentTo3DProps,
    WebSpiderAIMoodboardTabMeshSegmentProps,
    WebSpiderAIMoodboardTabSceneReconProps,
    WebSpiderAIMoodboardTabAnimateProps,
    WebSpiderAIMoodboardTabRetopologyProps,
    WebSpiderAIMoodboardTabUVUnwrapProps,
    # Scene Gen Experimental disabled
    # WebSpiderAISceneGenExpBBox,
    # WebSpiderAISceneGenExpLabelObject,
    # WebSpiderAIMoodboardTabSceneGenExpProps,
    WebSpiderAIMoodboardSidebarProperties,
)

logger = get_logger(__name__)

classes = (
    WebSpiderAIMoodboardSegment,
    WebSpiderAIMoodboardImage,
    WebSpiderAIMoodboardGroup,
    WebSpiderAIMoodboardReferenceImage,
    WebSpiderAIMoodboardTabAIRenderProps,
    WebSpiderAIMoodboardTabImageGenProps,
    WebSpiderAIMoodboardTabLookdevProps,
    WebSpiderAIMoodboardTabLookdev360Props,
    WebSpiderAIMoodboardTabImageTo3DProps,
    WebSpiderAIMoodboardTabSegmentTo3DProps,
    WebSpiderAIMoodboardTabMeshSegmentProps,
    WebSpiderAIMoodboardTabSceneReconProps,
    WebSpiderAIMoodboardTabAnimateProps,
    WebSpiderAIMoodboardTabRetopologyProps,
    WebSpiderAIMoodboardTabUVUnwrapProps,
    # Scene Gen Experimental disabled
    # WebSpiderAISceneGenExpBBox,
    # WebSpiderAISceneGenExpLabelObject,
    # WebSpiderAIMoodboardTabSceneGenExpProps,
    WebSpiderAIMoodboardSidebarProperties,
    WebSpiderAIMoodboardTextBox,
)


def register():
    """Register moodboard property classes and scene-level properties."""
    from bpy.utils import register_class

    for cls in classes:
        try:
            register_class(cls)
        except ValueError:
            logger.debug("Class %s already registered", cls.__name__)
        except Exception as e:
            logger.error("Failed to register class %s: %s", cls.__name__, e)

    # Scene collection properties
    _safe_scene_prop(
        'webspider_ai_moodboard_images',
        CollectionProperty(
            type=WebSpiderAIMoodboardImage,
            name="WebSpider AI Moodboard Images",
            description="Collection of reference images in Moodboard mode",
        ),
    )
    _safe_scene_prop(
        'webspider_ai_moodboard_textboxes',
        CollectionProperty(
            type=WebSpiderAIMoodboardTextBox,
            name="WebSpider AI Moodboard Text Boxes",
            description="Collection of text boxes in Moodboard mode",
        ),
    )
    _safe_scene_prop(
        'webspider_ai_moodboard_groups',
        CollectionProperty(
            type=WebSpiderAIMoodboardGroup,
            name="WebSpider AI Moodboard Groups",
            description="Collection of image groups",
        ),
    )
    _safe_scene_prop(
        'webspider_ai_moodboard_selected_index',
        IntProperty(
            name="Selected Moodboard Image Index",
            description="Index of the currently selected moodboard image",
            default=-1,
        ),
    )
    _safe_scene_prop(
        'webspider_ai_moodboard_sidebar',
        PointerProperty(
            type=WebSpiderAIMoodboardSidebarProperties,
            name="Moodboard Sidebar Properties",
            description="Properties for moodboard sidebar state",
        ),
    )

    # Edit tool state
    try:
        from .moodboard_edit_state import MoodboardEditToolState
        try:
            register_class(MoodboardEditToolState)
        except ValueError:
            pass  # already registered
        _safe_scene_prop(
            'webspider_ai_edit_tool_state',
            PointerProperty(type=MoodboardEditToolState),
        )
    except Exception as e:
        logger.error("Failed to register webspider_ai_edit_tool_state: %s", e)

    # Generation state flags (SKIP_SAVE so undo doesn't restore stale generating state)
    _safe_scene_prop(
        'webspider_ai_scene_recon_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether scene reconstruction is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_scene_recon_error',
        StringProperty(
            name="Error Message",
            description="Last error message from scene reconstruction",
            default="",
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_segment_to_3d_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether segment to 3D generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_imagegen_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether image generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_lookdev_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether lookdev generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_lookdev360_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether lookdev360 generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_image_to_3d_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether image to 3D generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    # Scene Gen Experimental disabled — flags intentionally not registered.
    _safe_scene_prop(
        'webspider_ai_retopology_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether retopology generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )
    _safe_scene_prop(
        'webspider_ai_animate_is_generating',
        BoolProperty(
            name="Is Generating",
            description="Whether rig/animate generation is in progress",
            default=False,
            options={'SKIP_SAVE'},
        ),
    )

    # Generation progress floats (session-only)
    for prefix in ('imagegen', 'lookdev', 'lookdev360', 'image_to_3d', 'scene_recon',
                    'segment_to_3d', 'mesh_segment', 'retopology', 'animate'):
        # Scene Gen Experimental ('scene_gen_hp', 'scene_gen_lp') intentionally omitted.
        _safe_wm_prop(
            f'webspider_ai_{prefix}_generate_progress',
            FloatProperty(
                name="Generate Progress",
                description=f"Generation progress for {prefix}",
                default=0.0, min=0.0, max=1.0,
                subtype='FACTOR',
                options={'SKIP_SAVE'},
            ),
        )


def unregister():
    """Unregister moodboard property classes and scene-level properties."""
    from bpy.utils import unregister_class

    # Scene properties (reverse of registration order)
    for attr in (
        # Scene Gen Experimental flags were not registered; nothing to remove.
        'webspider_ai_animate_is_generating',
        'webspider_ai_retopology_is_generating',
        'webspider_ai_image_to_3d_is_generating',
        'webspider_ai_lookdev360_is_generating',
        'webspider_ai_lookdev_is_generating',
        'webspider_ai_imagegen_is_generating',
        'webspider_ai_scene_recon_error',
        'webspider_ai_scene_recon_is_generating',
        'webspider_ai_segment_to_3d_is_generating',
        'webspider_ai_edit_tool_state',
        'webspider_ai_moodboard_sidebar',
        'webspider_ai_moodboard_selected_index',
        'webspider_ai_moodboard_groups',
        'webspider_ai_moodboard_textboxes',
        'webspider_ai_moodboard_images',
    ):
        try:
            delattr(bpy.types.Scene, attr)
        except AttributeError:
            pass

    # WindowManager properties
    wm_attrs = []
    for prefix in ('imagegen', 'lookdev', 'lookdev360', 'image_to_3d', 'scene_recon',
                    'segment_to_3d', 'mesh_segment', 'retopology', 'animate'):
        wm_attrs.append(f'webspider_ai_{prefix}_generate_progress')
    for attr in wm_attrs:
        try:
            delattr(bpy.types.WindowManager, attr)
        except AttributeError:
            pass

    # Classes (reverse order)
    for cls in reversed(classes):
        try:
            unregister_class(cls)
        except RuntimeError:
            pass

    # Unregister lazily-registered edit state class
    try:
        from bpy.utils import unregister_class
        from .moodboard_edit_state import MoodboardEditToolState
        try:
            unregister_class(MoodboardEditToolState)
        except RuntimeError:
            pass
    except Exception:
        pass


# -- helpers ----------------------------------------------------------------

def _safe_scene_prop(name, prop):
    try:
        setattr(bpy.types.Scene, name, prop)
    except Exception as e:
        logger.error("Failed to register Scene.%s: %s", name, e)


def _safe_wm_prop(name, prop):
    try:
        setattr(bpy.types.WindowManager, name, prop)
    except Exception as e:
        logger.error("Failed to register WindowManager.%s: %s", name, e)
