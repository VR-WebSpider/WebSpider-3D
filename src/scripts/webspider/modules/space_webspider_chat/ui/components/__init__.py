# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Reusable UI components for WebSpider Chat.
"""

from .status_indicator import (
    draw_connection_status,
    draw_error_box,
    draw_status_message,
)

__all__ = [
    "draw_connection_status",
    "draw_error_box",
    "draw_status_message",
]
