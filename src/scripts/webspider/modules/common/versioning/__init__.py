# SPDX-FileCopyrightText: 2024 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""WebSpider 3D file versioning and migration system."""

from .registry import (
    WEBSPIDER_PY_VERSION,
    register_migration,
    get_file_version,
    set_file_version,
    run_migrations,
)

# Import migration modules so they self-register via register_migration() at module level.
# Each migrations_vN.py file calls register_migration() during import.
from . import migrations_v1  # noqa: F401

__all__ = [
    "WEBSPIDER_PY_VERSION",
    "register_migration",
    "get_file_version",
    "set_file_version",
    "run_migrations",
]
