# SPDX-FileCopyrightText: 2024 WebSpider 3D Authors
# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Layer and mask merging operations

This module re-exports the merge operators for backward compatibility.
The actual implementations are in:
- merge_layer_operator.py: MMergeLayer class
- merge_mask_operator.py: MMergeMask class
"""

from ..merge.merge_layer_operator import MMergeLayer
from ..merge.merge_mask_operator import MMergeMask

# Re-export all classes for backward compatibility
__all__ = [
    "MMergeLayer",
    "MMergeMask",
    "classes",
]

classes = (
    MMergeLayer,
    MMergeMask,
)
