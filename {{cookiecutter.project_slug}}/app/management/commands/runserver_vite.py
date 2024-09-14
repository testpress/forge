import logging
import os
import shutil
import subprocess
from pathlib import Path

from django.contrib.staticfiles.management.commands.runserver import (
    Command as RunserverCommand,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Command(RunserverCommand):
    def handle(self, *args, **options):
        # Check if this is the main server process, not the reloader
        if os.environ.get("RUN_MAIN") == "true":
            # If this is the reloader, just run the server without
            # starting Vite
            logging.debug(
                "Reloader process, not starting Vite. PID: %s",
                os.getpid(),
            )
            super().handle(*args, **options)
        else:
            logging.debug("Starting Vite... (PID: %s)", os.getpid())

            # Use shutil.which to get the full path to npm
            npm_path = shutil.which("npm")
            if not npm_path:
                logging.error(
                    "npm executable not found. "
                    "Please ensure npm is installed and available in PATH.",
                )
                return

            vite_process = subprocess.Popen(  # noqa: S603
                [npm_path, "start"],
                cwd=Path.cwd() / "app/static",
            )
            try:
                logging.debug(
                    "Starting Django server... (PID: %s)",
                    os.getpid(),
                )
                super().handle(*args, **options)
            finally:
                logging.debug("Terminating Vite... (PID: %s)", os.getpid())
                vite_process.terminate()
                vite_process.wait()
