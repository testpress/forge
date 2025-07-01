from celery.signals import (
    task_failure,
    task_prerun,
    task_received,
    task_revoked,
    task_success,
)
from django.utils.timezone import now
from app.models import (
    CELERY_STATE_MAP,
    BackgroundTask,
    BackgroundTaskEvent,
    BackgroundTaskFile,
    EventType,
    TaskStatus,
)

def attach_file_to_task(task_id, file_obj, description=""):
    try:
        task = BackgroundTask.objects.get(task_id=task_id)
        BackgroundTaskFile.objects.create(task=task, file=file_obj, description=description)
    except BackgroundTask.DoesNotExist:
        pass

def log_progress(task_id, message):
    try:
        task = BackgroundTask.objects.get(task_id=task_id)
        BackgroundTaskEvent.objects.create(
            task=task,
            event=EventType.PROGRESS,
            message=message,
        )
    except BackgroundTask.DoesNotExist:
        pass

def log_task_event(task_id, name, event, message=None, **defaults):
    task, _ = BackgroundTask.objects.get_or_create(
        task_id=task_id,
        defaults={
            "name": name,
            **defaults,
        },
    )
    BackgroundTaskEvent.objects.create(task=task, event=event, message=message)

def update_status(task_id, celery_state, **kwargs):
    status = CELERY_STATE_MAP.get(celery_state, TaskStatus.PENDING)
    BackgroundTask.objects.filter(task_id=task_id).update(status=status, **kwargs)

@task_received.connect
def task_received_handler(sender, request=None, **kwargs):
    if not request:
        return
    task_id = request.id
    name = request.name
    log_task_event(task_id, name, event=EventType.RECEIVED, message="Task received")
    update_status(task_id, "RECEIVED")

@task_prerun.connect
def task_prerun_handler(task_id, task, **kwargs):
    log_task_event(task_id, task.name, event=EventType.STARTED, message="Task started")
    update_status(task_id, "STARTED", started_at=now())

@task_success.connect
def task_success_handler(sender, result, **kwargs):
    log_task_event(
        sender.request.id,
        sender.name,
        event=EventType.SUCCEEDED,
        message="Task succeeded",
    )
    update_status(sender.request.id, "SUCCESS", finished_at=now())

@task_failure.connect
def task_failure_handler(sender, task_id, exception, **kwargs):
    log_task_event(
        task_id,
        sender.name,
        event=EventType.FAILED,
        message=f"Task failed: {exception}",
    )
    update_status(task_id, "FAILURE", finished_at=now(), exception=str(exception))

@task_revoked.connect
def task_revoked_handler(sender, **kwargs):
    log_task_event(
        sender.request.id,
        sender.name,
        event=EventType.REVOKED,
        message="Task revoked",
    )
    update_status(sender.request.id, "REVOKED", finished_at=now())
