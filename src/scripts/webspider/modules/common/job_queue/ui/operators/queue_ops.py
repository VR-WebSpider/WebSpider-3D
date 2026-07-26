# SPDX-FileCopyrightText: 2026 WebSpider Studios
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Operators for the job queue UIList."""

from bpy.props import StringProperty
from bpy.types import Operator

from webspider.modules.common.job_queue.core.queue_manager import get_queue
from webspider.modules.common.utils.webspider_ai_space_utils import WEBSPIDER_AI_SPACE_AVAILABLE


class WEBSPIDER_AI_OT_queue_cancel_job(Operator):
    """Cancel a single queued or running job."""

    bl_idname = "webspider_ai.queue_cancel_job"
    bl_label = "Cancel Job"
    bl_options = {'REGISTER'}

    feature_key: StringProperty(default="")
    job_id: StringProperty(default="")

    def execute(self, context):
        if not self.feature_key or not self.job_id:
            return {'CANCELLED'}
        get_queue(self.feature_key).cancel(self.job_id)
        return {'FINISHED'}


class WEBSPIDER_AI_OT_queue_copy_error(Operator):
    """Copy the full error details to clipboard"""

    bl_idname = "webspider_ai.queue_copy_error"
    bl_label = "Copy Error"
    bl_description = "Copy full error details to clipboard"
    bl_options = {'REGISTER'}

    feature_key: StringProperty(default="")
    job_id: StringProperty(default="")

    def execute(self, context):
        if not self.feature_key or not self.job_id:
            return {'CANCELLED'}
        queue = get_queue(self.feature_key)
        for job in queue.snapshot():
            if job.id == self.job_id:
                context.window_manager.clipboard = job.error or "Unknown error"
                self.report({'INFO'}, "Error copied to clipboard")
                return {'FINISHED'}
        self.report({'WARNING'}, "Job not found in queue")
        return {'CANCELLED'}


class WEBSPIDER_AI_OT_queue_cancel_all(Operator):
    """Cancel every non-terminal job in the queue."""

    bl_idname = "webspider_ai.queue_cancel_all"
    bl_label = "Cancel All"
    bl_options = {'REGISTER'}

    feature_key: StringProperty(default="")

    def execute(self, context):
        if not self.feature_key:
            return {'CANCELLED'}
        get_queue(self.feature_key).cancel_all()
        return {'FINISHED'}


class WEBSPIDER_AI_OT_queue_clear_completed(Operator):
    """Remove all terminal (success/failed/cancelled) jobs from the queue."""

    bl_idname = "webspider_ai.queue_clear_completed"
    bl_label = "Clear Completed"
    bl_options = {'REGISTER'}

    feature_key: StringProperty(default="")

    def execute(self, context):
        if not self.feature_key:
            return {'CANCELLED'}
        get_queue(self.feature_key).clear_completed()
        return {'FINISHED'}


class WEBSPIDER_AI_OT_queue_clear_all_completed(Operator):
    """Remove all terminal jobs from every feature queue."""

    bl_idname = "webspider_ai.queue_clear_all_completed"
    bl_label = "Clear All Completed"
    bl_options = {'REGISTER'}

    def execute(self, context):
        from webspider.modules.common.job_queue.core.queue_manager import all_queues
        for q in all_queues():
            q.clear_completed()
        return {'FINISHED'}


# The unified Queue panel registers under bl_space_type WEBSPIDER_AI when the
# WebSpider 3D space exists (moodboard_sidebar_panels.py) — the "Queue" sidebar
# category does NOT exist in plain VIEW_3D areas, so the operator must
# target the same space type the panels registered in.
QUEUE_AREA_TYPE = 'WEBSPIDER_AI' if WEBSPIDER_AI_SPACE_AVAILABLE else 'VIEW_3D'


def find_largest_queue_area(context):
    """Return the biggest area hosting the Queue panel's space type, or None.

    Fallback target for callers whose context can't reach the Queue tab —
    toast action buttons fire from a ``bpy.app.timers`` callback where
    ``context.area`` is None, and a toast clicked in a 3D viewport still
    needs the WEBSPIDER_AI sidebar.
    """
    wm = getattr(context, "window_manager", None)
    best = None
    best_size = -1
    for window in getattr(wm, "windows", None) or []:
        screen = getattr(window, "screen", None)
        for area in getattr(screen, "areas", None) or []:
            if area.type == QUEUE_AREA_TYPE:
                size = area.width * area.height
                if size > best_size:
                    best, best_size = area, size
    return best


class WEBSPIDER_AI_OT_queue_view(Operator):
    """Switch sidebar to the Queue panel."""

    bl_idname = "webspider_ai.queue_view"
    bl_label = "View Queue"
    bl_options = {'REGISTER'}

    def execute(self, context):
        area = getattr(context, "area", None)
        if area is None or area.type != QUEUE_AREA_TYPE:
            area = find_largest_queue_area(context)
        if area is None:
            return {'CANCELLED'}
        space = area.spaces.active
        if hasattr(space, 'show_region_ui'):
            space.show_region_ui = True
        # Switch sidebar category to Queue
        region = next(
            (r for r in area.regions if r.type == 'UI'), None,
        )
        try:
            if region and hasattr(region, 'active_panel_category'):
                region.active_panel_category = "Queue"
        except Exception:
            pass  # sidebar just opened — category list not built yet
        area.tag_redraw()
        return {'FINISHED'}


classes = (
    WEBSPIDER_AI_OT_queue_cancel_job,
    WEBSPIDER_AI_OT_queue_copy_error,
    WEBSPIDER_AI_OT_queue_cancel_all,
    WEBSPIDER_AI_OT_queue_clear_completed,
    WEBSPIDER_AI_OT_queue_clear_all_completed,
    WEBSPIDER_AI_OT_queue_view,
)
