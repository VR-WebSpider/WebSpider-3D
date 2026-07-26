/* SPDX-FileCopyrightText: 2025 Blender Authors
 * SPDX-FileCopyrightText: 2026 WebSpider Studios
 *
 * SPDX-License-Identifier: GPL-3.0-or-later */

/** \file
 * \ingroup spwebspider_aichat
 */

#include "BKE_screen.hh"

#include "ED_screen.hh"

#include "WM_api.hh"

#include "webspider_ai_chat_intern.hh"

void webspider_ai_chat_header_region_init(wmWindowManager * /*wm*/, ARegion *region)
{
  ED_region_header_init(region);
}

void webspider_ai_chat_header_region_draw(const bContext *C, ARegion *region)
{
  ED_region_header(C, region);
}
