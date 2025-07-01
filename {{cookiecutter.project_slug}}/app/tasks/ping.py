import tempfile
from pathlib import Path
from celery import shared_task
from django.core.files import File
from app.domain.background_task import attach_file_to_task, log_progress

@shared_task(bind=True)
def ping(self):
    log_progress(self.request.id, "Sending Pong")
    return "pong"

@shared_task(bind=True)
def generate_report(self):
    log_progress(self.request.id, "Starting PDF generation")

    temp_dir = Path(tempfile.gettempdir())
    report_path = temp_dir / "sample_report.txt"
    report_path.write_text("This is a test report")
    log_progress(self.request.id, "PDF generation complete")

    try:
        with report_path.open("rb") as f:
            django_file = File(f, name="sample_report.txt")
            attach_file_to_task(
                self.request.id,
                django_file,
                description="Sample report output",
            )
    finally:
        report_path.unlink(missing_ok=True)

    log_progress(self.request.id, "Sending report via email")
    return "Report Created"
