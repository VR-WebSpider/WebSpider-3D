# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Floating agent chat bubble overlaid on the active Blender window.

Architecture (Phase 1):
- C++ side (src/source/blender/editors/space_webspider_chat/
  webspider_chat_agent_bubble.cc) registers WEBSPIDER_AI_CHAT_OT_agent_bubble_show,
  which uses UI_popup_block_invoke + UI_BLOCK_KEEP_OPEN to draw a
  persistent popup over every editor in the active window — no
  per-region clipping.
- Python side (this module) defines the popup's body via the
  WEBSPIDER_AI_CHAT_MT_agent_bubble menu type, so the layout is authored with
  the same UILayout API used everywhere else and reuses
  draw_multiline_text_input from common.utils.ui_utils — the very same
  widget the chat editor's footer uses for its input field.
- Send / receive go through scene.webspider_chat_input +
  webspider_ai_chat.send_message, so the optimistic UI update + SSE pipeline
  is shared with the chat editor.

Phase 2 (not yet shipped) adds drag-to-move, drag-to-resize, and a
distinct status pill rendered above the composer.
"""
