/* SPDX-FileCopyrightText: 2025 Blender Authors
 * SPDX-FileCopyrightText: 2026 WebSpider Studios
 *
 * SPDX-License-Identifier: GPL-3.0-or-later */

/** \file
 * \ingroup spwebspider_aichat
 *
 * Text selection and copy operators for chat messages.
 * Provides character-level drag selection with Cmd/Ctrl+C copy support.
 */

#include <cstring>

#include "MEM_guardedalloc.h"

#include "BLI_rect.h"
#include "BLI_string_utf8.h"

#include "BLF_api.hh"

#include "BKE_context.hh"

#include "DNA_scene_types.h"
#include "DNA_space_types.h"

#include "RNA_access.hh"

#include "GPU_immediate.hh"
#include "GPU_state.hh"

#include "ED_screen.hh"

#include "UI_interface.hh"
#include "UI_view2d.hh"

#include "WM_api.hh"
#include "WM_types.hh"

#include "webspider_ai_chat_intern.hh"

/* -------------------------------------------------------------------- */
/** \name Selection State Helpers
 * \{ */

static SpaceWebSpider AIChat *get_space_webspider_ai_chat(const bContext *C)
{
  ScrArea *area = CTX_wm_area(C);
  /* SPACE_AGENT_BUBBLE has a layout-compatible spacedata struct
   * (see DNA_space_types.h), so this cast is valid for both. */
  if (area && (area->spacetype == SPACE_WEBSPIDER_CHAT ||
               area->spacetype == SPACE_AGENT_BUBBLE))
  {
    return static_cast<SpaceWebSpider AIChat *>(area->spacedata.first);
  }
  return nullptr;
}

static void clear_selection(SpaceWebSpider AIChat *swebspider_ai)
{
  swebspider_ai->sel_message_index = -1;
  swebspider_ai->sel_start = 0;
  swebspider_ai->sel_end = 0;
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Get Selected Text
 * \{ */

char *webspider_ai_chat_get_selected_text(const bContext *C)
{
  SpaceWebSpider AIChat *swebspider_ai = get_space_webspider_ai_chat(C);
  if (!swebspider_ai || swebspider_ai->sel_message_index < 0) {
    return nullptr;
  }

  int sel_start = swebspider_ai->sel_start;
  int sel_end = swebspider_ai->sel_end;

  /* Ensure start < end */
  if (sel_start > sel_end) {
    int tmp = sel_start;
    sel_start = sel_end;
    sel_end = tmp;
  }

  if (sel_start == sel_end) {
    return nullptr;
  }

  Scene *scene = CTX_data_scene(C);
  if (!scene) {
    return nullptr;
  }

  PointerRNA scene_ptr = RNA_id_pointer_create(&scene->id);
  PropertyRNA *prop = RNA_struct_find_property(&scene_ptr, "webspider_ai_chat_messages");
  if (!prop) {
    return nullptr;
  }

  /* Get the message at sel_message_index */
  PointerRNA msg_ptr{};
  if (!RNA_property_collection_lookup_int(&scene_ptr, prop, swebspider_ai->sel_message_index, &msg_ptr)) {
    return nullptr;
  }

  /* Try slot-based 'content' field first, fall back to deprecated 'text' */
  PropertyRNA *text_prop = RNA_struct_find_property(&msg_ptr, "content");
  if (!text_prop) {
    text_prop = RNA_struct_find_property(&msg_ptr, "text");
  }
  if (!text_prop) {
    return nullptr;
  }

  /* Dynamically allocate text buffer based on actual string length */
  int text_len = RNA_property_string_length(&msg_ptr, text_prop);
  char *text_buffer = static_cast<char *>(MEM_mallocN(text_len + 1, "chat_text"));
  RNA_property_string_get(&msg_ptr, text_prop, text_buffer);

  /* If content is empty, try text as fallback */
  if (text_len == 0) {
    MEM_freeN(text_buffer);
    PropertyRNA *fallback_prop = RNA_struct_find_property(&msg_ptr, "text");
    if (fallback_prop) {
      text_len = RNA_property_string_length(&msg_ptr, fallback_prop);
      text_buffer = static_cast<char *>(MEM_mallocN(text_len + 1, "chat_text"));
      RNA_property_string_get(&msg_ptr, fallback_prop, text_buffer);
    }
  }

  /* Clamp offsets */
  if (sel_start < 0) {
    sel_start = 0;
  }
  if (sel_end > int(text_len)) {
    sel_end = int(text_len);
  }

  int sel_len = sel_end - sel_start;
  if (sel_len <= 0) {
    MEM_freeN(text_buffer);
    return nullptr;
  }

  /* Copy selected substring */
  char *selected = static_cast<char *>(MEM_mallocN(sel_len + 1, "chat_selected_text"));
  memcpy(selected, text_buffer + sel_start, sel_len);
  selected[sel_len] = '\0';

  /* Free dynamically allocated text buffer */
  MEM_freeN(text_buffer);

  return selected;
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Selection Highlight Drawing
 * \{ */

void chat_ui_draw_text_selection(const rctf *text_rect,
                                 const char *text,
                                 int sel_start,
                                 int sel_end,
                                 int font_size)
{
  if (sel_start == sel_end || !text || text[0] == '\0') {
    return;
  }

  /* Ensure start < end */
  if (sel_start > sel_end) {
    int tmp = sel_start;
    sel_start = sel_end;
    sel_end = tmp;
  }

  /* Re-clamp against the CURRENT text: the offsets were captured at click
   * time, but a streaming update can replace the message with a shorter
   * string before the next redraw — BLF_width would then read past the NUL.
   * (webspider_ai_chat_get_selected_text re-clamps the same way before its memcpy.) */
  const int text_len = int(strlen(text));
  if (sel_start > text_len) {
    sel_start = text_len;
  }
  if (sel_end > text_len) {
    sel_end = text_len;
  }
  if (sel_start < 0) {
    sel_start = 0;
  }
  if (sel_start == sel_end) {
    return;
  }

  const int font_id = BLF_default();
  BLF_size(font_id, font_size);

  /* Calculate selection bounds */
  float sel_x1 = text_rect->xmin + BLF_width(font_id, text, sel_start);
  float sel_x2 = text_rect->xmin + BLF_width(font_id, text, sel_end);

  /* Clamp to text rect */
  if (sel_x1 < text_rect->xmin) {
    sel_x1 = text_rect->xmin;
  }
  if (sel_x2 > text_rect->xmax) {
    sel_x2 = text_rect->xmax;
  }

  /* Draw selection highlight */
  float sel_color[4] = {0.3f, 0.5f, 0.8f, 0.4f};

  GPU_blend(GPU_BLEND_ALPHA);

  GPUVertFormat *format = immVertexFormat();
  uint pos = GPU_vertformat_attr_add(format, "pos", blender::gpu::VertAttrType::SFLOAT_32_32);

  immBindBuiltinProgram(GPU_SHADER_3D_UNIFORM_COLOR);
  immUniformColor4fv(sel_color);

  immRectf(pos, sel_x1, text_rect->ymin, sel_x2, text_rect->ymax);

  immUnbindProgram();
  GPU_blend(GPU_BLEND_NONE);
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Select Text Operator (Modal)
 * \{ */

struct ChatSelectionData {
  int message_index;
  int start_char;
};

static wmOperatorStatus webspider_ai_chat_select_invoke(bContext *C, wmOperator *op, const wmEvent *event)
{
  SpaceWebSpider AIChat *swebspider_ai = get_space_webspider_ai_chat(C);
  ARegion *region = CTX_wm_region(C);

  if (!swebspider_ai || !region) {
    return OPERATOR_CANCELLED;
  }

  /* Check for scroll-to-bottom indicator click first (screen-space) */
  if (webspider_ai_chat_handle_scroll_indicator_click(
          swebspider_ai, region, float(event->mval[0]), float(event->mval[1])))
  {
    ED_region_tag_redraw(region);
    return OPERATOR_FINISHED;
  }

  /* Check for empty prompt clicks first (when chat is empty) */
  if (webspider_ai_chat_handle_empty_prompt_click(C, float(event->mval[0]), float(event->mval[1]))) {
    return OPERATOR_FINISHED;
  }

  /* Check for action button clicks (copy/retry below agent messages) */
  if (webspider_ai_chat_handle_action_button_click(C, region, event->mval[0], event->mval[1])) {
    return OPERATOR_FINISHED;
  }

  /* Check for steps/thinking collapse toggle clicks */
  if (webspider_ai_chat_handle_steps_click(C, region, event->mval[0], event->mval[1])) {
    return OPERATOR_FINISHED;
  }

  /* Check for slot action button clicks */
  if (webspider_ai_chat_handle_slot_action_click(C, region, event->mval[0], event->mval[1])) {
    return OPERATOR_FINISHED;
  }

  /* Check for feedback star/comment clicks */
  if (webspider_ai_chat_handle_feedback_click(C, region, event->mval[0], event->mval[1])) {
    return OPERATOR_FINISHED;
  }

  /* Convert mouse to text position */
  int msg_idx, char_offset;
  if (!webspider_ai_chat_pos_to_text(C, region, event->mval, &msg_idx, &char_offset)) {
    /* Clicked outside any message - clear selection. Pass the event
     * through so handlers registered after this keymap (View2D
     * scrollbar interaction in particular) still get a chance at the
     * click: plain OPERATOR_CANCELLED would break event handling and
     * eat it. */
    clear_selection(swebspider_ai);
    ED_region_tag_redraw(region);
    return OPERATOR_CANCELLED | OPERATOR_PASS_THROUGH;
  }

  /* Start selection */
  swebspider_ai->sel_message_index = msg_idx;
  swebspider_ai->sel_start = char_offset;
  swebspider_ai->sel_end = char_offset;

  /* Setup modal for drag */
  ChatSelectionData *data = MEM_new<ChatSelectionData>("chat_sel_data");
  data->message_index = msg_idx;
  data->start_char = char_offset;
  op->customdata = data;

  WM_event_add_modal_handler(C, op);
  ED_region_tag_redraw(region);

  return OPERATOR_RUNNING_MODAL;
}

static wmOperatorStatus webspider_ai_chat_select_modal(bContext *C, wmOperator *op, const wmEvent *event)
{
  SpaceWebSpider AIChat *swebspider_ai = get_space_webspider_ai_chat(C);
  ARegion *region = CTX_wm_region(C);
  ChatSelectionData *data = static_cast<ChatSelectionData *>(op->customdata);

  if (!swebspider_ai || !region || !data) {
    if (data) {
      MEM_delete<ChatSelectionData>(data);
    }
    return OPERATOR_CANCELLED;
  }

  switch (event->type) {
    case MOUSEMOVE: {
      int msg_idx, char_offset;
      if (webspider_ai_chat_pos_to_text(C, region, event->mval, &msg_idx, &char_offset)) {
        /* Only allow selection within the same message */
        if (msg_idx == data->message_index) {
          swebspider_ai->sel_end = char_offset;
          ED_region_tag_redraw(region);
        }
      }
      return OPERATOR_RUNNING_MODAL;
    }
    case LEFTMOUSE:
      if (event->val == KM_RELEASE) {
        MEM_delete<ChatSelectionData>(data);
        op->customdata = nullptr;
        return OPERATOR_FINISHED;
      }
      return OPERATOR_RUNNING_MODAL;
    case EVT_ESCKEY:
      clear_selection(swebspider_ai);
      ED_region_tag_redraw(region);
      MEM_delete<ChatSelectionData>(data);
      op->customdata = nullptr;
      return OPERATOR_CANCELLED;
    default:
      break;
  }

  /* Pass through events we don't handle (scroll wheel, middle mouse, etc.)
   * so View2D scrolling still works during text selection drag. */
  return OPERATOR_PASS_THROUGH;
}

static void webspider_ai_chat_select_cancel(bContext *C, wmOperator *op)
{
  SpaceWebSpider AIChat *swebspider_ai = get_space_webspider_ai_chat(C);
  if (swebspider_ai) {
    clear_selection(swebspider_ai);
  }

  if (op->customdata) {
    MEM_delete<ChatSelectionData>(static_cast<ChatSelectionData *>(op->customdata));
    op->customdata = nullptr;
  }
}

void WEBSPIDER_AI_CHAT_OT_select_text(wmOperatorType *ot)
{
  ot->name = "Select Text";
  ot->idname = "WEBSPIDER_AI_CHAT_OT_select_text";
  ot->description = "Select text in chat message by clicking and dragging";

  ot->invoke = webspider_ai_chat_select_invoke;
  ot->modal = webspider_ai_chat_select_modal;
  ot->cancel = webspider_ai_chat_select_cancel;

  ot->poll = ED_operator_areaactive;

  ot->flag = 0;
}

/** \} */

/* -------------------------------------------------------------------- */
/** \name Copy Operator
 * \{ */

static bool webspider_ai_chat_has_selection(bContext *C)
{
  SpaceWebSpider AIChat *swebspider_ai = get_space_webspider_ai_chat(C);
  if (!swebspider_ai) {
    return false;
  }
  return (swebspider_ai->sel_message_index >= 0 && swebspider_ai->sel_start != swebspider_ai->sel_end);
}

static wmOperatorStatus webspider_ai_chat_copy_exec(bContext *C, wmOperator * /*op*/)
{
  char *selected = webspider_ai_chat_get_selected_text(C);
  if (!selected) {
    return OPERATOR_CANCELLED;
  }

  WM_clipboard_text_set(selected, false);
  MEM_freeN(selected);

  return OPERATOR_FINISHED;
}

void WEBSPIDER_AI_CHAT_OT_copy(wmOperatorType *ot)
{
  ot->name = "Copy";
  ot->idname = "WEBSPIDER_AI_CHAT_OT_copy";
  ot->description = "Copy selected chat text to clipboard";

  ot->exec = webspider_ai_chat_copy_exec;
  ot->poll = webspider_ai_chat_has_selection;

  ot->flag = OPTYPE_REGISTER;
}

/** \} */
