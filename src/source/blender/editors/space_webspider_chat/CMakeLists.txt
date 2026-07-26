# SPDX-FileCopyrightText: 2025 Blender Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

set(INC
  ../include
  ../../makesrna

  # RNA_prototypes.hh
  ${CMAKE_BINARY_DIR}/source/blender/makesrna
)

set(INC_SYS
)

set(SRC
  webspider_ai_chat_action_buttons.cc
  webspider_ai_chat_agent_bubble.cc
  webspider_ai_chat_dragdrop.cc
  webspider_ai_chat_footer.cc
  webspider_ai_chat_footer_cache.cc
  webspider_ai_chat_footer_draw.cc
  webspider_ai_chat_footer_layout.cc
  webspider_ai_chat_footer_thumbnails.cc
  webspider_ai_chat_header.cc
  webspider_ai_chat_history_events.cc
  webspider_ai_chat_history_overlay.cc
  webspider_ai_chat_history_util.cc
  webspider_ai_chat_hit_testing.cc
  webspider_ai_chat_main_region.cc
  webspider_ai_chat_markdown.cc
  webspider_ai_chat_markdown_parse.cc
  webspider_ai_chat_mention.cc
  webspider_ai_chat_table.cc
  webspider_ai_chat_empty_state.cc
  webspider_ai_chat_feedback.cc
  webspider_ai_chat_messages.cc
  webspider_ai_chat_messages_content.cc
  webspider_ai_chat_messages_layout.cc
  webspider_ai_chat_messages_render.cc
  webspider_ai_chat_props.cc
  webspider_ai_chat_rules_events.cc
  webspider_ai_chat_rules_overlay.cc
  webspider_ai_chat_rules_util.cc
  webspider_ai_chat_scroll_indicator.cc
  webspider_ai_chat_selection.cc
  webspider_ai_chat_slots.cc
  webspider_ai_chat_steps.cc
  webspider_ai_chat_thinking.cc
  webspider_ai_chat_ui_primitives.cc
  webspider_ai_chat_ui_theme.cc
  webspider_ai_chat_ui_widgets.cc
  space_webspider_chat.cc

  webspider_ai_chat_footer_constants.hh
  webspider_ai_chat_footer_intern.hh
  webspider_ai_chat_history_intern.hh
  webspider_ai_chat_intern.hh
  webspider_ai_chat_layout_data.hh
  webspider_ai_chat_markdown_intern.hh
  webspider_ai_chat_rules_intern.hh
  webspider_ai_chat_ui_types.hh
)

set(LIB
  PRIVATE bf::blenfont
  PRIVATE bf::blenkernel
  PRIVATE bf::blenlib
  PRIVATE bf::blenloader
  PRIVATE bf::blentranslation
  PRIVATE bf::dna
  PRIVATE bf::gpu
  PRIVATE bf::imbuf
  PRIVATE bf::intern::guardedalloc
  PRIVATE bf::windowmanager
  bf_editor_interface
)

blender_add_lib(bf_editor_space_webspider_ai_chat "${SRC}" "${INC}" "${INC_SYS}" "${LIB}")

# RNA_prototypes.hh dna_type_offsets.h
add_dependencies(bf_editor_space_webspider_ai_chat bf_rna)
