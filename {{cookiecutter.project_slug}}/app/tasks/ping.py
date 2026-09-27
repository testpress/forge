import tempfile
from pathlib import Path

import dramatiq
from dramatiq.middleware import CurrentMessage
from django.core.files import File

from app.domain.background_task import attach_file_to_task
from app.domain.background_task import log_progress


def _current_task_id() -> str:
    # Only unset outside of an actor, which shouldn't happen here - these
    # functions are only ever invoked by a Dramatiq worker.
    message = CurrentMessage.get_current_message()
    if message is None:
        msg = "no current Dramatiq message - called outside of an actor?"
        raise RuntimeError(msg)
    return message.message_id


# max_retries=0 keeps this actor's behavior identical to the Celery task it
# replaces - Celery's plain @shared_task does not retry on failure, unlike
# a Dramatiq actor's default of up to 20 retries with backoff. Drop this
# option (or raise the limit) to opt into Dramatiq's retries.
#
# Neither actor returns a value: nothing here consumes one (no Results
# middleware/backend is configured - BackgroundTask/BackgroundTaskEvent,
# via log_progress below, are this template's result store), and
# returning one anyway makes Dramatiq log a "result discarded" warning on
# every run.
@dramatiq.actor(max_retries=0)
def ping() -> None:
    log_progress(_current_task_id(), "Sending Pong")


@dramatiq.actor(max_retries=0)
def generate_report() -> None:
    task_id = _current_task_id()
    log_progress(task_id, "Starting PDF generation")

    temp_dir = Path(tempfile.gettempdir())
    report_path = temp_dir / "sample_report.txt"
    report_path.write_text("This is a test report")
    log_progress(task_id, "PDF generation complete")

    try:
        with report_path.open("rb") as f:
            django_file = File(f, name="sample_report.txt")
            attach_file_to_task(
                task_id,
                django_file,
                description="Sample report output",
            )
    finally:
        report_path.unlink(missing_ok=True)

    log_progress(task_id, "Sending report via email")
