from typing import TYPE_CHECKING
from typing import Any

import dramatiq
from django.utils.timezone import now

from app.models import BackgroundTask
from app.models import BackgroundTaskEvent
from app.models import BackgroundTaskFile
from app.models import EventType
from app.models import TaskStatus

if TYPE_CHECKING:
    from dramatiq.broker import Broker
    from dramatiq.broker import MessageProxy
    from dramatiq.message import Message

    from django.core.files import File


def attach_file_to_task(
    task_id: str,
    file_obj: "File[Any]",
    description: str = "",
) -> None:
    try:
        task = BackgroundTask.objects.get(task_id=task_id)
        BackgroundTaskFile.objects.create(
            task=task,
            file=file_obj,
            description=description,
        )
    except BackgroundTask.DoesNotExist:
        pass


def log_progress(task_id: str, message: str) -> None:
    try:
        task = BackgroundTask.objects.get(task_id=task_id)
        BackgroundTaskEvent.objects.create(
            task=task,
            event=EventType.PROGRESS,
            message=message,
        )
    except BackgroundTask.DoesNotExist:
        pass


def log_task_event(
    task_id: str,
    name: str,
    event: EventType,
    message: str | None = None,
    **defaults: Any,
) -> None:
    task, _ = BackgroundTask.objects.get_or_create(
        task_id=task_id,
        defaults={
            "name": name,
            **defaults,
        },
    )
    BackgroundTaskEvent.objects.create(task=task, event=event, message=message)


def update_status(task_id: str, status: TaskStatus, **kwargs: Any) -> None:
    BackgroundTask.objects.filter(task_id=task_id).update(status=status, **kwargs)


class BackgroundTaskMiddleware(dramatiq.Middleware):
    """Keeps BackgroundTask/BackgroundTaskEvent in sync with actor runs.

    Registered on the broker in config/dramatiq.py. This is Dramatiq's
    equivalent of what used to be five `@signal.connect` handlers on
    Celery's task_received/task_prerun/task_success/task_failure/
    task_revoked - Dramatiq exposes the same kind of lifecycle events, but
    as hooks on a single Middleware subclass instead of standalone
    signals, and the hooks themselves don't line up one-to-one:

    - There's no worker-side "received but not yet running" moment
      distinct from "about to run" the way Celery split task_received
      from task_prerun - before_process_message already covers both.
      RECEIVED is logged from after_enqueue instead, which fires in
      whichever process calls `.send()` (a view, another task, or
      Dramatiq's own Retries middleware scheduling a retry) the moment
      the message is handed to the broker - the closest equivalent this
      side of the queue has to offer, and it fires again on every retry.
    - task_success/task_failure become one hook, after_process_message,
      distinguished by whether `exception` is set.
    - task_revoked has no equivalent at all: Dramatiq has no built-in way
      to cancel a pending or in-flight message. TaskStatus.REVOKED/
      EventType.REVOKED are left on the model for a project that adds
      https://pypi.org/project/dramatiq-abort/ to get that back.
    """

    def after_enqueue(
        self,
        broker: "Broker",
        message: "Message[Any]",
        delay: int | None,
    ) -> None:
        log_task_event(
            message.message_id,
            message.actor_name,
            event=EventType.RECEIVED,
            message="Task received",
        )
        update_status(message.message_id, TaskStatus.RECEIVED)

    def before_process_message(
        self,
        broker: "Broker",
        message: "MessageProxy",
    ) -> None:
        log_task_event(
            message.message_id,
            message.actor_name,
            event=EventType.STARTED,
            message="Task started",
        )
        update_status(message.message_id, TaskStatus.STARTED, started_at=now())

    def after_process_message(
        self,
        broker: "Broker",
        message: "MessageProxy",
        *,
        result: Any = None,
        exception: BaseException | None = None,
    ) -> None:
        if exception is None:
            log_task_event(
                message.message_id,
                message.actor_name,
                event=EventType.SUCCEEDED,
                message="Task succeeded",
            )
            update_status(message.message_id, TaskStatus.SUCCESS, finished_at=now())
        else:
            log_task_event(
                message.message_id,
                message.actor_name,
                event=EventType.FAILED,
                message=f"Task failed: {exception}",
            )
            update_status(
                message.message_id,
                TaskStatus.FAILURE,
                finished_at=now(),
                exception=str(exception),
            )
