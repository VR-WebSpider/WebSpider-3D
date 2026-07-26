/* SPDX-FileCopyrightText: 2025 Blender Authors
 * SPDX-FileCopyrightText: 2026 WebSpider Studios
 *
 * SPDX-License-Identifier: GPL-3.0-or-later */

/** \file
 * \ingroup spwebspider_aichat
 */

#pragma once

#include "BLI_rect.h"

#include "webspider_ai_chat_layout_data.hh"
#include "webspider_ai_chat_ui_types.hh"

struct ARegion;
struct bContext;
struct Main;
struct PointerRNA;
struct PropertyRNA;
struct ScrArea;
struct wmEvent;
struct wmOperatorType;
struct wmRegionListenerParams;
struct wmWindow;
struct wmWindowManager;

namespace blender::gpu {
class Texture;
}

/* -------------------------------------------------------------------- */
/** \name Region Callbacks
 * \{ */

/* Header region callbacks */
void webspider_ai_chat_header_region_init(wmWindowManager *wm, ARegion *region);
void webspider_ai_chat_header_region_draw(const bContext *C, ARegion *region);

/* Footer region callbacks */
void webspider_ai_chat_footer_region_init(wmWindowManager *wm, ARegion *region);
void webspider_ai_chat_footer_region_layout(const bContext *C, ARegion *region);
void webspider_ai_chat_footer_region_draw(const bContext *C, ARegion *region);

/* Main region callbacks (webspider_ai_chat_main_region.cc) */
void webspider_ai_chat_main_region_cursor(wmWindow *win, ScrArea *area, ARegion *region);
void webspider_ai_chat_main_region_init(wmWindowManager *wm, ARegion *region);
void webspider_ai_chat_main_region_draw(const bContext *C, ARegion *region);
void webspider_ai_chat_main_region_exit(wmWindowManager *wm, ARegion *region);
void webspider_ai_chat_main_region_listener(const wmRegionListenerParams *params);
void webspider_ai_chat_main_region_layout(const bContext *C, ARegion *region);

/* Animation frame pump (webspider_ai_chat_main_region.cc): a TIMERNOTIFIER wmTimer
 * that keeps chat redraws coming at animation rate while any draw-side
 * animation (slide-in, spinner/loader, scroll bounce) is live. Request from
 * the messages draw every frame; shutdown removes the timer outright. */
void webspider_ai_chat_anim_pump_request(const bContext *C, bool anim_active);
void webspider_ai_chat_anim_pump_shutdown(wmWindowManager *wm);

/* Main region custom drawing */
void webspider_ai_chat_draw_messages(const bContext *C, ARegion *region);

/* Optional per-frame background colour override.  When set, the
 * region draw functions use this RGBA colour instead of TH_BACK.
 * The flag is automatically cleared after each draw call so callers
 * must set it every frame (from a wrapper draw callback). */
void webspider_ai_chat_set_bg_override(const float rgba[4]);
void webspider_ai_chat_clear_bg_override();
bool webspider_ai_chat_has_bg_override();
void webspider_ai_chat_get_bg_override(float r_rgba[4]);

/* Animation types for chat UI elements */
enum ChatAnimationType {
  CHAT_ANIM_SPINNER = 0, /* ◐ ◓ ◑ ◒  (loader spinner) */
  CHAT_ANIM_PULSE_DOT,   /* ● ○      (active/in-progress indicator) */
  CHAT_ANIM_COUNT,
};
const char *chat_anim_frame(ChatAnimationType type, int frame_index);

/* Wall-clock-derived spinner frame (0-3). All C++ spinner draw sites use
 * this instead of the Python-advanced RNA index: the Python timer only
 * ticks at 0.5s (2 fps — visibly choppy), while the clock advances the
 * glyph whenever a redraw happens, so the spinner is exactly as smooth as
 * the frames the animation pump delivers. */
int chat_ui_spinner_frame();

/* Empty state drawing (webspider_ai_chat_empty_state.cc) */
void webspider_ai_chat_draw_empty_state(const bContext *C,
                                  ARegion *region,
                                  struct SpaceWebSpider AIChat *swebspider_ai,
                                  const ChatLayoutMetrics &metrics,
                                  int winx,
                                  int winy);

/* Message content rendering (webspider_ai_chat_messages_content.cc) */
void webspider_ai_chat_render_message_content(const MessageLayoutData &layout,
                                        PointerRNA *msg_ptr,
                                        int text_len,
                                        const char *display_text);

/** Join todo items into one "icon text" line per item, overflow-safe.
 * `in_progress_icon` is the icon for status 1 (call sites differ: animated
 * pulse frame vs static dot for clipboard copies). Truncates — never
 * overflows — when the combined text exceeds `buf_maxncpy`; size buffers
 * with `SLOT_TODO_COMBINED_MAX` to fit the worst case. Returns
 * `strlen(buf)`. (webspider_ai_chat_messages_layout.cc) */
size_t webspider_ai_chat_build_todo_text(const TodoItemSlotData *items,
                                  int count,
                                  const char *in_progress_icon,
                                  char *buf,
                                  size_t buf_maxncpy);

/* Layout cache builder and message renderer (split from webspider_ai_chat_messages.cc) */
float webspider_ai_chat_build_layout_cache(struct SpaceWebSpider AIChat *swebspider_ai,
                                    Main *bmain,
                                    PointerRNA *scene_ptr,
                                    PropertyRNA *prop,
                                    const ChatLayoutMetrics &metrics,
                                    const ChatImageStyle &image_style,
                                    int winx,
                                    int msg_count);
void webspider_ai_chat_render_messages(const bContext *C,
                                ARegion *region,
                                struct SpaceWebSpider AIChat *swebspider_ai,
                                Main *bmain,
                                PointerRNA *scene_ptr,
                                PropertyRNA *prop,
                                const ChatLayoutMetrics &metrics,
                                const ChatImageStyle &image_style);
void webspider_ai_chat_render_feedback(const bContext *C,
                                ARegion *region,
                                PointerRNA *msg_ptr,
                                const ChatLayoutMetrics &metrics,
                                const MessageLayoutData &layout);
/* Vertical gap between the message's last content row and the feedback stars.
 * Shared by the layout pass and the render pass so they always agree. */
float chat_ui_get_feedback_top_gap(const ChatLayoutMetrics &metrics);
/* Pixel height for the in-progress feedback comment input, wrap-measured with
 * the exact widget_draw_text_multiline() font and line-height math so the
 * button grows one widget line at a time (Shift+Enter multi-line). Clamped to
 * FEEDBACK_COMMENT_MAX_LINES. */
float webspider_ai_chat_feedback_comment_input_height(PointerRNA *msg_ptr, float input_width);

/** \} */

/* -------------------------------------------------------------------- */
/** \name UI Primitives (webspider_ai_chat_ui_primitives.cc)
 * \{ */

/* Rounded rectangle drawing */
void chat_ui_draw_rounded_rect(const rctf *rect, float radius, const float color[4]);
void chat_ui_draw_rounded_rect_outline(const rctf *rect,
                                       float radius,
                                       const float color[4],
                                       float line_width);
void chat_ui_draw_rounded_rect_bordered(const rctf *rect,
                                        float radius,
                                        const float fill_color[4],
                                        const float border_color[4],
                                        float border_width);

/* Thin colored vertical accent bar at the left edge of a block (Plan / steps /
 * thinking), so the three section types are differentiated while staying flat.
 * Drawn in the block's existing left padding — no layout change. */
void chat_ui_draw_accent_bar(float x,
                             float y_bottom,
                             float height,
                             const float color[4],
                             float scale);

/* Text drawing and measurement */
void chat_ui_calc_text_bounds(const char *text,
                              float max_width,
                              int font_size,
                              int flags,
                              float *out_width,
                              float *out_height);

float chat_ui_draw_text_wrapped(const char *text,
                                const rctf *rect,
                                int font_size,
                                int flags,
                                const float color[4]);

/* Font-parameterized variants — pass a specific BLF font id (e.g.
 * chat_ui_mono_font() for code). The plain variants above wrap these with
 * BLF_default(). */
void chat_ui_calc_text_bounds_font(const char *text,
                                   float max_width,
                                   int font_size,
                                   int flags,
                                   int font_id,
                                   float *out_width,
                                   float *out_height);

float chat_ui_draw_text_wrapped_font(const char *text,
                                     const rctf *rect,
                                     int font_size,
                                     int flags,
                                     int font_id,
                                     const float color[4]);

/* Lazily-loaded monospace font id for code rendering. */
int chat_ui_mono_font();

/* Rich inline-markdown text: renders **bold**, *italic* and `code` runs with
 * word-wrapping and a monospace inline-code style. base_flags (BLF_BOLD /
 * BLF_ITALIC) applies to every run — used for headings/quotes. When do_draw is
 * false only measurement happens. Returns the total height; out_max_width
 * (nullable) receives the widest rendered line. Both the layout and draw passes
 * call this so they agree exactly. */
float chat_ui_rich_text(const char *text,
                        const rctf *rect,
                        int font_size,
                        int base_flags,
                        const float color[4],
                        float scale_factor,
                        bool do_draw,
                        float *out_max_width);

void chat_ui_draw_label(const char *text,
                        float x,
                        float y,
                        int font_size,
                        int flags,
                        const float color[4],
                        bool right_align);

/* Image drawing */
void chat_ui_draw_image(blender::gpu::Texture *tex, const rctf *rect, float corner_radius);
void chat_ui_calc_image_bounds(int tex_width,
                               int tex_height,
                               float max_width,
                               float max_height,
                               float *out_width,
                               float *out_height);

/* Layout metrics */
ChatLayoutMetrics chat_ui_get_layout_metrics();
ChatBubbleStyle chat_ui_get_user_bubble_style(const ChatLayoutMetrics *metrics);
ChatBubbleStyle chat_ui_get_agent_bubble_style(const ChatLayoutMetrics *metrics);
ChatImageStyle chat_ui_get_image_style(const ChatLayoutMetrics *metrics);

/* Theme accessor functions */
float chat_ui_get_font_size();
float chat_ui_get_label_font_size();
float chat_ui_get_padding();
float chat_ui_get_bubble_spacing();
float chat_ui_get_bubble_h_padding();
float chat_ui_get_bubble_v_padding();
float chat_ui_get_corner_radius();
float chat_ui_get_label_height();
float chat_ui_get_image_max_width();
float chat_ui_get_image_max_height();
float chat_ui_get_image_margin();
float chat_ui_get_image_corner_radius();
float chat_ui_get_action_button_height();
float chat_ui_get_action_button_padding();
float chat_ui_get_action_button_spacing();
float chat_ui_get_action_button_corner_radius();
float chat_ui_get_footer_general_padding();
float chat_ui_get_main_footer_gap();
float chat_ui_get_send_button_size();
float chat_ui_get_attach_button_size();
float chat_ui_get_footer_button_row_height();
float chat_ui_get_thumbnail_border_radius();
float chat_ui_get_thumbnail_padding();
void chat_ui_get_thumbnail_border_color(float out_color[4]);
void chat_ui_get_button_hover_color(float out_color[4]);
void chat_ui_get_history_row_hover_color(float out_color[4]);
void chat_ui_get_placeholder_text_color(float out_color[4]);
void chat_ui_get_prompt_button_color(float out_color[4]);

/* Toggle switch theme colors */
void chat_ui_get_toggle_on_color(float out_color[4]);
void chat_ui_get_toggle_off_color(float out_color[4]);
void chat_ui_get_toggle_knob_color(float out_color[4]);
void chat_ui_get_toggle_label_color(float out_color[4]);

/** \} */

/* -------------------------------------------------------------------- */
/** \name UI Widgets (webspider_ai_chat_ui_widgets.cc)
 * \{ */

/* Chat bubble */
float chat_ui_calc_bubble_height(const ChatBubbleStyle *style,
                                 const char *text,
                                 float max_width,
                                 float attachments_height);
float chat_ui_draw_bubble(const ChatBubbleStyle *style,
                          const char *text,
                          float x,
                          float y,
                          float bubble_width,
                          float bubble_height,
                          float content_width,
                          float attachments_height = 0.0f);

/* Ephemeral bubble with FIFO line limiting (webspider_ai_chat_thinking.cc) */
/* Current loader status string, or `fallback` when the loader has no valid
 * text. Shared by the layout (height) and render (draw) passes so both size
 * and draw the SAME status line. */
const char *chat_ui_loader_status_text(const LoaderSlotData *loader,
                                       bool has_loader,
                                       const char *fallback);
float chat_ui_calc_ephemeral_bubble_height(const ChatBubbleStyle *style,
                                           const char *status_text,
                                           float content_width);
void chat_ui_draw_ephemeral_bubble(const ChatBubbleStyle *style,
                                   const char *ephemeral_text,
                                   const LoaderSlotData *loader,
                                   bool has_loader,
                                   float x,
                                   float y,
                                   float bubble_width,
                                   float bubble_height,
                                   float content_width);

/* Live thinking line: a compact "◐ <status>" indicator that updates as the
 * agent narrates. Wraps at content_width (never truncates), so the height
 * depends on the status text. */
float chat_ui_calc_live_thinking_height(const ChatBubbleStyle *style,
                                        const char *status_text,
                                        float content_width);
void chat_ui_draw_live_thinking(const ChatBubbleStyle *style,
                                const char *thinking_text,
                                int spinner_frame,
                                float x,
                                float y,
                                float bubble_width,
                                float bubble_height,
                                float content_width);

/* Collapse chevron shared by the steps block + thinking dropdown
 * (webspider_ai_chat_steps.cc). Drawn as a tinted mono icon (ICON_TRIA_*) so it
 * stays crisp at any UI scale, vertically centered on `center_y`. */
float chat_ui_chevron_indent();
void chat_ui_draw_chevron(float x, float center_y, bool collapsed, const float color[4]);

/* Visual center of the FIRST line of `text` as chat_ui_draw_text_wrapped
 * will actually place it in a rect whose bottom is `rect_ymin`: the text
 * draw bottom-aligns the wrapped INK box, so the first-line baseline is
 * rect_ymin - ink_bbox.ymin, and the visual center sits half a cap height
 * above it. Anchor glyphs/chevrons here, NOT on the geometric line box —
 * the line-box center reads high and shifts with descender depth. */
float chat_ui_wrapped_first_line_center(int font_size,
                                        const char *text,
                                        float wrap_width,
                                        float rect_ymin);

/* Agent steps block (webspider_ai_chat_steps.cc) */
float chat_ui_calc_steps_block_height(const ChatBubbleStyle *style,
                                      const MessageLayoutData *layout,
                                      float content_width);
void chat_ui_draw_steps_block(const ChatBubbleStyle *style,
                              MessageLayoutData *layout,
                              float x,
                              float y,
                              float bubble_width,
                              float content_width);

/* Finalized thinking dropdown (webspider_ai_chat_thinking.cc) */
float chat_ui_calc_thinking_dropdown_height(const ChatBubbleStyle *style,
                                            const char *thinking_text,
                                            bool collapsed,
                                            float content_width);
void chat_ui_draw_thinking_dropdown(const ChatBubbleStyle *style,
                                    const char *thinking_text,
                                    bool collapsed,
                                    int duration_ms,
                                    float x,
                                    float y,
                                    float bubble_width,
                                    float bubble_height,
                                    float content_width,
                                    rctf *out_header_bounds);

/* Markdown rendering (webspider_ai_chat_markdown.cc) */
bool chat_ui_has_markdown_segments(const char *metadata_json);
float chat_ui_calc_markdown_height(const char *metadata_json,
                                   const ChatBubbleStyle *style,
                                   float content_width,
                                   float scale_factor);
void chat_ui_draw_markdown(const char *metadata_json,
                           float x,
                           float y,
                           float content_width,
                           const ChatBubbleStyle *style,
                           float scale_factor);

/* Image attachment */
float chat_ui_calc_image_attachment_height(Main *bmain,
                                           const char *image_path,
                                           int image_source,
                                           const ChatImageStyle *style);
float chat_ui_draw_image_attachment(Main *bmain,
                                    const char *image_path,
                                    int image_source,
                                    float x,
                                    float y,
                                    float max_width,
                                    const ChatImageStyle *style);

/* Action buttons */
void chat_ui_draw_action_buttons(float bubble_x,
                                 float bubble_y,
                                 float bubble_width,
                                 float bubble_height,
                                 bool show_retry,
                                 float scale_factor,
                                 ChatActionButton *out_buttons,
                                 int *out_button_count,
                                 bool align_right = false,
                                 bool show_copied = false,
                                 float alpha = 1.0f);
int chat_ui_handle_action_click(float mouse_x,
                                float mouse_y,
                                const ChatActionButton *buttons,
                                int button_count);
float chat_ui_get_action_buttons_height(float scale_factor);

/* Sender label */
void chat_ui_draw_sender_label(const char *label,
                               float x,
                               float y,
                               const ChatLayoutMetrics *metrics,
                               bool is_user);

/** \} */

/* -------------------------------------------------------------------- */
/** \name Text Selection (webspider_ai_chat_selection.cc)
 * \{ */

/* Selection operators */
void WEBSPIDER_AI_CHAT_OT_select_text(wmOperatorType *ot);
void WEBSPIDER_AI_CHAT_OT_copy(wmOperatorType *ot);

/* Text selection helper - converts mouse position to message index and character offset */
bool webspider_ai_chat_pos_to_text(const bContext *C,
                            ARegion *region,
                            const int mval[2],
                            int *r_message_index,
                            int *r_char_offset);

/* Get selected text string (must be freed with MEM_freeN) */
char *webspider_ai_chat_get_selected_text(const bContext *C);

/* Draw selection highlight over text */
void chat_ui_draw_text_selection(const rctf *text_rect,
                                 const char *text,
                                 int sel_start,
                                 int sel_end,
                                 int font_size);

/* Scroll-to-bottom indicator (webspider_ai_chat_scroll_indicator.cc) */
void webspider_ai_chat_update_scroll_indicator(struct SpaceWebSpider AIChat *swebspider_ai,
                                        ARegion *region,
                                        int msg_count);
void webspider_ai_chat_draw_scroll_indicator(struct SpaceWebSpider AIChat *swebspider_ai, ARegion *region);
void webspider_ai_chat_trigger_scroll_bounce(struct SpaceWebSpider AIChat *swebspider_ai);
bool webspider_ai_chat_handle_scroll_indicator_click(struct SpaceWebSpider AIChat *swebspider_ai,
                                               ARegion *region,
                                               float mouse_x,
                                               float mouse_y);

/* Button bg/text color getters used by scroll indicator */
void chat_ui_get_button_bg_color(float out_color[4]);
void chat_ui_get_button_text_color(float out_color[4]);
void chat_ui_get_label_color(float out_color[4]);

/* Past-chats overlay (webspider_ai_chat_history_overlay.cc). Drawn screen-space
 * on top of the message area; modal for this region while open (consumes
 * clicks/wheel/ESC via the region UI handler). Visibility comes from the
 * Python-registered WindowManager bool `webspider_ai_chat_history_visible`;
 * rows from `webspider_ai_chat_history_entries`. */
void webspider_ai_chat_draw_history_overlay(const bContext *C, ARegion *region);
bool webspider_ai_chat_history_handle_event(bContext *C, const wmEvent *event);
bool webspider_ai_chat_history_cursor(
    wmWindow *win, WebSpider AIChatRuntime *rt, ARegion *region, float mouse_x, float mouse_y);
void webspider_ai_chat_history_set_visible(bContext *C, bool visible);

/* Project-rules overlay (webspider_ai_chat_rules_overlay.cc). Same modal-overlay
 * pattern and visual family as the past-chats overlay; edits a multiline
 * text buffer written through to `scene.webspider_ai_chat_rules`. Visibility comes
 * from the Python-registered WindowManager bool `webspider_ai_chat_rules_visible`. */
void webspider_ai_chat_draw_rules_overlay(const bContext *C, ARegion *region);
bool webspider_ai_chat_rules_handle_event(bContext *C, const wmEvent *event);
bool webspider_ai_chat_rules_cursor(
    wmWindow *win, WebSpider AIChatRuntime *rt, ARegion *region, float mouse_x, float mouse_y);
void webspider_ai_chat_rules_set_visible(bContext *C, bool visible);

/* Hit testing and click handlers (webspider_ai_chat_hit_testing.cc) */
bool webspider_ai_chat_handle_slot_action_click(bContext *C,
                                          ARegion *region,
                                          float mouse_x,
                                          float mouse_y);
bool webspider_ai_chat_handle_action_button_click(bContext *C,
                                            ARegion *region,
                                            float mouse_x,
                                            float mouse_y);
bool webspider_ai_chat_handle_feedback_click(bContext *C,
                                      ARegion *region,
                                      float mouse_x,
                                      float mouse_y);
bool webspider_ai_chat_handle_empty_prompt_click(bContext *C, float mouse_x, float mouse_y);
bool webspider_ai_chat_handle_steps_click(bContext *C,
                                   ARegion *region,
                                   float mouse_x,
                                   float mouse_y);

/** \} */

/* Drag-and-drop (webspider_ai_chat_dragdrop.cc) */
void WEBSPIDER_AI_CHAT_OT_drop_image(wmOperatorType *ot);
void webspider_ai_chat_dropboxes();

/* Floating agent bubble overlay (webspider_ai_chat_agent_bubble.cc).
 * The status pill is drawn INSIDE this same popup as a top-row boxed
 * label — see src/scripts/webspider/modules/agent_bubble/ui/menus/
 * agent_bubble_menu.py — so it inherits the bubble's position, drag
 * behavior, and ESC dismissal automatically. */
void WEBSPIDER_AI_CHAT_OT_agent_bubble_show(wmOperatorType *ot);

/* Property cache, layout data, runtime state: see webspider_ai_chat_layout_data.hh */

/** \} */
