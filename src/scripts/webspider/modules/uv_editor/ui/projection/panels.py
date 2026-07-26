# SPDX-FileCopyrightText: 2025 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""
WebSpider 3D UV Projection Panels

The standalone Projection panel was merged into WEBSPIDER_UV_PT_unwrap, which
now hosts both the Unwrap and Project sub-sections. This file remains so
the projection package keeps a stable shape for the bootstrap loader; the
projection operators continue to live in projection/operators.py.
"""

# No panel classes — the Project section is rendered inside the Unwrap panel
# (see ../unwrap/panels.py).
classes = ()
