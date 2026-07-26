/* SPDX-FileCopyrightText: 2025 Blender Authors
 * SPDX-FileCopyrightText: 2026 WebSpider Studios
 *
 * SPDX-License-Identifier: GPL-3.0-or-later */

/** \file
 * \ingroup spwebspiderassets
 *
 * WebSpider 3D Assets Space - Smart materials, brushes, textures library.
 */

#include <cstring>

#include "MEM_guardedalloc.h"

#include "BLI_listbase.h"
#include "BLI_string_utf8.h"

#include "BKE_context.hh"
#include "BKE_screen.hh"

#include "ED_screen.hh"
#include "ED_space_api.hh"

#include "WM_api.hh"

#include "UI_interface.hh"
#include "UI_resources.hh"

#include "BLO_read_write.hh"

#include "DNA_screen_types.h"
#include "DNA_space_types.h"
#include "DNA_userdef_types.h"

static SpaceLink *webspider_assets_create(const ScrArea * /*area*/, const Scene * /*scene*/)
{
  SpaceWebSpider 3DAssets *sassets = MEM_callocN<SpaceWebSpider 3DAssets>("initwebspiderassets");
  sassets->spacetype = SPACE_WEBSPIDER_ASSETS;

  /* Header (hosts the editor-type switch dropdown) */
  ARegion *region = BKE_area_region_new();
  BLI_addtail(&sassets->regionbase, region);
  region->regiontype = RGN_TYPE_HEADER;
  region->alignment = (U.uiflag & USER_HEADER_BOTTOM) ? RGN_ALIGN_BOTTOM : RGN_ALIGN_TOP;

  /* Main region */
  region = BKE_area_region_new();
  BLI_addtail(&sassets->regionbase, region);
  region->regiontype = RGN_TYPE_WINDOW;

  return (SpaceLink *)sassets;
}

static void webspider_assets_free(SpaceLink * /*sl*/) {}

static void webspider_assets_init(wmWindowManager * /*wm*/, ScrArea * /*area*/) {}

static SpaceLink *webspider_assets_duplicate(SpaceLink *sl)
{
  return (SpaceLink *)MEM_dupallocN(sl);
}

static void webspider_assets_main_region_init(wmWindowManager *wm, ARegion *region)
{
  ED_region_panels_init(wm, region);
}

static void webspider_assets_main_region_draw(const bContext *C, ARegion *region)
{
  ED_region_panels(C, region);
}

static void webspider_assets_main_region_listener(const wmRegionListenerParams *params)
{
  ARegion *region = params->region;
  const wmNotifier *wmn = params->notifier;

  switch (wmn->category) {
    case NC_SPACE:
      ED_region_tag_redraw(region);
      break;
  }
}

/* Header region uses the standard header draw so Python `Header` classes
 * (and the editor-type switch dropdown) are rendered. */
static void webspider_assets_header_region_init(wmWindowManager * /*wm*/, ARegion *region)
{
  ED_region_header_init(region);
}

static void webspider_assets_header_region_draw(const bContext *C, ARegion *region)
{
  ED_region_header(C, region);
}

static void webspider_assets_header_region_listener(const wmRegionListenerParams *params)
{
  ARegion *region = params->region;
  const wmNotifier *wmn = params->notifier;

  switch (wmn->category) {
    case NC_MATERIAL:
    case NC_OBJECT:
    case NC_SPACE:
      ED_region_tag_redraw(region);
      break;
  }
}

static void webspider_assets_blend_write(BlendWriter *writer, SpaceLink *sl)
{
  BLO_write_struct(writer, SpaceWebSpider 3DAssets, sl);
}

void ED_spacetype_webspider_assets()
{
  std::unique_ptr<SpaceType> st = std::make_unique<SpaceType>();

  st->spaceid = SPACE_WEBSPIDER_ASSETS;
  STRNCPY_UTF8(st->name, "Texturing Assets");
  st->iconid = ICON_ASSET_MANAGER;

  st->create = webspider_assets_create;
  st->free = webspider_assets_free;
  st->init = webspider_assets_init;
  st->duplicate = webspider_assets_duplicate;
  st->blend_write = webspider_assets_blend_write;

  /* Main region */
  ARegionType *art = MEM_callocN<ARegionType>("spacetype webspider_assets main");
  art->regionid = RGN_TYPE_WINDOW;
  art->keymapflag = ED_KEYMAP_UI;
  art->init = webspider_assets_main_region_init;
  art->layout = ED_region_panels_layout;
  art->draw = webspider_assets_main_region_draw;
  art->listener = webspider_assets_main_region_listener;
  BLI_addhead(&st->regiontypes, art);

  /* Header region */
  art = MEM_callocN<ARegionType>("spacetype webspider_assets header");
  art->regionid = RGN_TYPE_HEADER;
  art->prefsizey = HEADERY;
  art->keymapflag = ED_KEYMAP_UI | ED_KEYMAP_HEADER;
  art->init = webspider_assets_header_region_init;
  art->draw = webspider_assets_header_region_draw;
  art->listener = webspider_assets_header_region_listener;
  BLI_addhead(&st->regiontypes, art);

  BKE_spacetype_register(std::move(st));
}
