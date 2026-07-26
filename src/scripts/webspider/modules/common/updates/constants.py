# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Auto-Update System Constants

Configuration values, enums, and file paths for the update checker.
Updating is browser-based: the client only detects that a newer version
exists and points the user at the downloads page — there is no in-app
download or installer launch.
"""

from enum import Enum

# ============================================================================
# PLATFORM MAPPING
# ============================================================================

PLATFORM_MAP = {
    "darwin": "mac",
    "win32": "windows",
    "win": "windows",
    "linux": "linux",
}

# ============================================================================
# FILE / DIRECTORY NAMES
# ============================================================================

INSTALL_ID_FILENAME = ".webspider3d_install_id"
SKIPPED_VERSION_FILENAME = ".webspider3d_skipped_version"

# ============================================================================
# NOTIFICATION
# ============================================================================

UPDATE_NOTIFICATION_ID = "webspider3d-update"

# ============================================================================
# OPERATORS
# ============================================================================

OP_CHECK_FOR_UPDATES = "webspider.check_for_updates"

# ============================================================================
# URLS
# ============================================================================

# Public downloads page — where the update toast's [Download] button goes
# when the backend doesn't supply a per-release browser URL.
# Overridable at runtime via webspider.json ("updates" -> "downloads_url").
DOWNLOADS_PAGE_URL = "https://www.webspider3d.com/downloads"

# ============================================================================
# STATE MACHINE
# ============================================================================


class UpdateState(Enum):
    """Lifecycle states for the update checker."""

    IDLE = "idle"
    CHECKING = "checking"
    AVAILABLE = "available"
    ERROR = "error"
