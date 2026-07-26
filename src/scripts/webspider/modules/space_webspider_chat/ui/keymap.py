# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider Chat Keymap Registration

Registers keyboard shortcuts for the WebSpider Chat space.
"""

import bpy

from webspider.config.logging_config import get_logger

logger = get_logger(__name__)

# Global list to track registered keymaps for cleanup
addon_keymaps = []


def register():
    """Register keymap for WebSpider Chat space."""
    if addon_keymaps:
        return  # Already registered — prevents double-registration on timer retry

    wm = getattr(bpy.context, 'window_manager', None)
    if not wm:
        logger.warning("window_manager not available yet, deferring keymap registration")
        if not bpy.app.timers.is_registered(register):
            bpy.app.timers.register(register, first_interval=0.1)
        return

    kc = wm.keyconfigs.addon

    if kc:
        # Register global shortcut for quick prompt (works in all spaces)
        # Platform-specific: Cmd+Shift+M on macOS, Ctrl+Shift+M on Windows
        import sys
        is_macos = sys.platform == 'darwin'

        km_window = kc.keymaps.new(name='Window', space_type='EMPTY')
        if is_macos:
            # macOS: Cmd+Shift+M
            kmi = km_window.keymap_items.new(
                'webspider_ai_chat.quick_prompt',
                type='M',
                value='PRESS',
                shift=True,
                oskey=True
            )
            logger.debug("Registered global Cmd+Shift+M shortcut for quick prompt (macOS)")
        else:
            # Windows/Linux: Ctrl+Shift+M
            kmi = km_window.keymap_items.new(
                'webspider_ai_chat.quick_prompt',
                type='M',
                value='PRESS',
                shift=True,
                ctrl=True
            )
            logger.debug("Registered global Ctrl+Shift+M shortcut for quick prompt (Windows/Linux)")

        addon_keymaps.append((km_window, kmi))

        # Register WebSpider Chat space-specific shortcuts
        km_webspider_ai = kc.keymaps.new(name='WebSpider Chat', space_type='WEBSPIDER_AI_CHAT', region_type='WINDOW')

        # Paste image from clipboard: Cmd+Shift+V (macOS) or Ctrl+Shift+V (Windows/Linux)
        if is_macos:
            kmi_paste = km_webspider_ai.keymap_items.new(
                'webspider_ai_chat.paste_image',
                type='V',
                value='PRESS',
                shift=True,
                oskey=True
            )
            logger.debug("Registered Cmd+Shift+V shortcut for paste image (macOS)")
        else:
            kmi_paste = km_webspider_ai.keymap_items.new(
                'webspider_ai_chat.paste_image',
                type='V',
                value='PRESS',
                shift=True,
                ctrl=True
            )
            logger.debug("Registered Ctrl+Shift+V shortcut for paste image (Windows/Linux)")

        addon_keymaps.append((km_webspider_ai, kmi_paste))

        # Escape to abort current operation (works when agent is BUSY)
        kmi_abort = km_webspider_ai.keymap_items.new(
            'webspider_ai_chat.abort_session',
            type='ESC',
            value='PRESS',
        )
        addon_keymaps.append((km_webspider_ai, kmi_abort))
        logger.debug("Registered Escape shortcut for abort")


def unregister():
    """Unregister keymap for WebSpider Chat space."""
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    logger.debug("Unregistered keymap")


# Export for bootstrap auto-registration
# Note: This file uses register/unregister functions, not classes list
