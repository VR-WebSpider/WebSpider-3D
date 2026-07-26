/* SPDX-FileCopyrightText: 2025 Blender Authors
 * SPDX-FileCopyrightText: 2026 WebSpider Studios
 *
 * SPDX-License-Identifier: GPL-3.0-or-later */

/** \file
 * \ingroup spwebspiderproperties
 *
 * WebSpider 3D Properties Space - Layer and texture properties.
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

static SpaceLink *webspider_properties_create(const ScrArea * /*area*/, const Scene * /*scene*/)
{
  SpaceWebSpider 3DProperties *sprops = MEM_callocN<SpaceWebSpider 3DProperties>("initwebspiderproperties");
  sprops->spacetype = SPACE_WEBSPIDER_PROPERTIES;

  /* Header (hosts the editor-type switch dropdown) */
  ARegion *region = BKE_area_region_new();
  BLI_addtail(&sprops->regionbase, region);
  region->regiontype = RGN_TYPE_HEADER;
  region->alignment = (U.uiflag & USER_HEADER_BOTTOM) ? RGN_ALIGN_BOTTOM : RGN_ALIGN_TOP;

  /* Main region */
  region = BKE_area_region_new();
  BLI_addtail(&sprops->regionbase, region);
  region->regiontype = RGN_TYPE_WINDOW;

  return (SpaceLink *)sprops;
}

static void webspider_properties_free(SpaceLink * /*sl*/) {}

static void webspider_properties_init(wmWindowManager * /*wm*/, ScrArea * /*area*/) {}

static SpaceLink *webspider_properties_duplicate(SpaceLink *sl)
{
  return (SpaceLink *)MEM_dupallocN(sl);
}

static void webspider_properties_main_region_init(wmWindowManager *wm, ARegion *region)
{
  ED_region_panels_init(wm, region);
}

static void webspider_properties_main_region_draw(const bContext *C, ARegion *region)
{
  ED_region_panels(C, region);
}

static void webspider_properties_main_region_listener(const wmRegionListenerParams *params)
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

/* Header region uses the standard header draw so Python `Header` classes
 * (and the editor-type switch dropdown) are rendered. */
static void webspider_properties_header_region_init(wmWindowManager * /*wm*/, ARegion *region)
{
  ED_region_header_init(region);
}

static void webspider_properties_header_region_draw(const bContext *C, ARegion *region)
{
  ED_region_header(C, region);
}

static void webspider_properties_header_region_listener(const wmRegionListenerParams *params)
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

static void webspider_properties_blend_write(BlendWriter *writer, SpaceLink *sl)
{
  BLO_write_struct(writer, SpaceWebSpider 3DProperties, sl);
}

void ED_spacetype_webspider_properties()
{
  std::unique_ptr<SpaceType> st = std::make_unique<SpaceType>();

  st->spaceid = SPACE_WEBSPIDER_PROPERTIES;
  STRNCPY_UTF8(st->name, "Texturing Properties");
  st->iconid = ICON_PROPERTIES;

  st->create = webspider_properties_create;
  st->free = webspider_properties_free;
  st->init = webspider_properties_init;
  st->duplicate = webspider_properties_duplicate;
  st->blend_write = webspider_properties_blend_write;

  /* Main region */
  ARegionType *art = MEM_callocN<ARegionType>("spacetype webspider_properties main");
  art->regionid = RGN_TYPE_WINDOW;
  art->keymapflag = ED_KEYMAP_UI;
  art->init = webspider_properties_main_region_init;
  art->layout = ED_region_panels_layout;
  art->draw = webspider_properties_main_region_draw;
  art->listener = webspider_properties_main_region_listener;
  BLI_addhead(&st->regiontypes, art);

  /* Header region */
  art = MEM_callocN<ARegionType>("spacetype webspider_properties header");
  art->regionid = RGN_TYPE_HEADER;
  art->prefsizey = HEADERY;
  art->keymapflag = ED_KEYMAP_UI | ED_KEYMAP_HEADER;
  art->init = webspider_properties_header_region_init;
  art->draw = webspider_properties_header_region_draw;
  art->listener = webspider_properties_header_region_listener;
  BLI_addhead(&st->regiontypes, art);

  BKE_spacetype_register(std::move(st));
}
