/* SPDX-FileCopyrightText: 2024 WebSpider 3D Authors
 * SPDX-FileCopyrightText: 2026 WebSpider Studios
 *
 * SPDX-License-Identifier: GPL-3.0-or-later */

/** \file
 * \ingroup blenloader
 *
 * WebSpider 3D-specific versioning declarations.
 */

#pragma once

struct Main;

/**
 * Run WebSpider 3D-specific versioning on file load.
 * Called from blo_do_versions_500() in versioning_500.cc.
 */
void blo_do_versions_webspider(Main *bmain);
