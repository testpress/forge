from typing import Any

import dramatiq
import pytest
from dramatiq.brokers.stub import StubBroker
from dramatiq.middleware import CurrentMessage

from app.domain.background_task import BackgroundTaskMiddleware
from app.domain.background_task import log_progress
from app.models import BackgroundTask
from app.models import EventType
from app.models import TaskStatus


@pytest.fixture
def stub_broker() -> StubBroker:
    """A real Dramatiq broker (in-memory, no Redis) with the same
    middleware config/dramatiq.py attaches to the real one.

    Deliberately does *not* run a real dramatiq.Worker thread: that
    races the test's own DB connection against SQLite's shared
    :memory: database (both the enqueuing thread's after_enqueue and a
    worker thread's before_process_message write concurrently), which
    is genuinely flaky - "database is locked" - not just theoretically.
    _process_synchronously below drives the same before/after hook
    lifecycle a real worker does, single-threaded, so it's
    deterministic while still exercising real Message objects and the
    real middleware.
    """
    broker = StubBroker()
    broker.add_middleware(CurrentMessage())
    broker.add_middleware(BackgroundTaskMiddleware())
    return broker


def _process_synchronously(
    broker: StubBroker,
    message: "dramatiq.Message[Any]",
) -> None:
    """Runs one message through the broker's hook lifecycle in-process.

    Mirrors dramatiq.worker.Worker.process_message (emit_before ->
    call the actor -> emit_after, with the exception - if any - passed
    to emit_after rather than raised) closely enough for testing
    purposes, without needing a second thread.
    """
    broker.emit_before("process_message", message)
    exception: BaseException | None = None
    try:
        actor = broker.get_actor(message.actor_name)
        actor(*message.args, **message.kwargs)
    except BaseException as exc:  # noqa: BLE001
        exception = exc
    broker.emit_after("process_message", message, exception=exception)


@pytest.mark.django_db
def test_successful_task_updates_status_and_events(stub_broker: StubBroker) -> None:
    @dramatiq.actor(broker=stub_broker, max_retries=0)
    def example_success() -> None:
        message = CurrentMessage.get_current_message()
        assert message is not None
        log_progress(message.message_id, "halfway there")

    sent = example_success.send()
    _process_synchronously(stub_broker, sent)

    task = BackgroundTask.objects.get(task_id=sent.message_id)
    assert task.status == TaskStatus.SUCCESS
    assert task.started_at is not None
    assert task.finished_at is not None
    events = list(task.events.order_by("created").values_list("event", flat=True))
    assert events == [
        EventType.RECEIVED,
        EventType.STARTED,
        EventType.PROGRESS,
        EventType.SUCCEEDED,
    ]


@pytest.mark.django_db
def test_failing_task_records_exception(stub_broker: StubBroker) -> None:
    @dramatiq.actor(broker=stub_broker, max_retries=0)
    def example_failure() -> None:
        msg = "boom"
        raise ValueError(msg)

    sent = example_failure.send()
    _process_synchronously(stub_broker, sent)

    task = BackgroundTask.objects.get(task_id=sent.message_id)
    assert task.status == TaskStatus.FAILURE
    assert task.exception == "boom"
    assert task.events.filter(event=EventType.FAILED).exists()
