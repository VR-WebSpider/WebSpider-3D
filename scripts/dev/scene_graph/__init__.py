# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Layered, agent-readable scene graph for WebSpider 3D.

One shared node registry (built from a single scene walk) feeds multiple
pluggable relation layers. The spatial layer is implemented end-to-end here;
geometry/semantic layers plug in later behind the same RelationLayer contract.

Entry point for running inside WebSpider 3D: ../run_scene_graph.py
"""
