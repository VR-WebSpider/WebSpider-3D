# SPDX-FileCopyrightText: 2024 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Handlers module for paint system."""

from .decal_handlers import (
    mpaint_decal_constraint_update,
    register_decal_handlers,
    unregister_decal_handlers,
)

__all__ = [
    'mpaint_decal_constraint_update',
    'register_decal_handlers',
    'unregister_decal_handlers',
]
