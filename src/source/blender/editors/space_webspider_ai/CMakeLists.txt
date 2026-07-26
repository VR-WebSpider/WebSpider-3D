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
  webspider_ai_dragdrop.cc
  webspider_ai_draw_moodboard.cc
  webspider_ai_draw_moodboard_groups.cc
  webspider_ai_draw_moodboard_images.cc
  webspider_ai_draw_moodboard_textboxes.cc
  webspider_ai_draw_moodboard_tools.cc
  webspider_ai_draw_sam3d.cc
  webspider_ai_header.cc
  webspider_ai_moodboard_ops_box_select.cc
  webspider_ai_moodboard_ops_crop.cc
  webspider_ai_moodboard_ops_drop.cc
  webspider_ai_moodboard_ops_masks.cc
  webspider_ai_moodboard_ops_select.cc
  webspider_ai_moodboard_ops_zoom.cc
  webspider_ai_ops.cc
  webspider_ai_select.cc
  space_webspider_ai.cc

  webspider_ai_draw_moodboard_intern.hh
  webspider_ai_intern.hh
  webspider_ai_moodboard_ops_common.hh
)

set(LIB
  PRIVATE bf::blenfont
  PRIVATE bf::blenkernel
  PRIVATE bf::blenlib
  PRIVATE bf::blenloader
  PRIVATE bf::blentranslation
  PRIVATE bf::depsgraph
  PRIVATE bf::dna
  PRIVATE bf::gpu
  PRIVATE bf::imbuf
  PRIVATE bf::intern::guardedalloc
  PRIVATE bf::extern::fmtlib
  PRIVATE bf::windowmanager
  bf_editor_interface
)


blender_add_lib(bf_editor_space_webspider_ai "${SRC}" "${INC}" "${INC_SYS}" "${LIB}")

# RNA_prototypes.hh dna_type_offsets.h
add_dependencies(bf_editor_space_webspider_ai bf_rna)
