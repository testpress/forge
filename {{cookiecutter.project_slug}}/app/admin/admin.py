from django.contrib import admin

from app.models import BackgroundTask
from app.models import BackgroundTaskEvent
from app.models import BackgroundTaskFile


class BackgroundTaskEventInline(
    admin.TabularInline[BackgroundTaskEvent, BackgroundTask]
):
    model = BackgroundTaskEvent
    fields = ("event", "message", "created")
    readonly_fields = ("event", "message", "created")
    extra = 0
    can_delete = False
    show_change_link = False


@admin.register(BackgroundTask)
class BackgroundTaskAdmin(admin.ModelAdmin[BackgroundTask]):
    list_display = ("name", "task_id", "status", "started_at", "finished_at")
    search_fields = ("task_id", "name")
    list_filter = ("status",)
    inlines = (BackgroundTaskEventInline,)


@admin.register(BackgroundTaskEvent)
class BackgroundTaskEventAdmin(admin.ModelAdmin[BackgroundTaskEvent]):
    list_display = ("task", "event", "created")
    list_filter = ("event",)


@admin.register(BackgroundTaskFile)
class BackgroundTaskFileAdmin(admin.ModelAdmin[BackgroundTaskFile]):
    list_display = ("task", "file", "description")
