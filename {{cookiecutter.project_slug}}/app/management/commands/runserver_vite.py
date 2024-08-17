import logging
import os
import subprocess

from django.core.management.commands.runserver import (
    Command as RunserverCommand,
)

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Command(RunserverCommand):
    def handle(self, *args, **options):
        # Check if this is the main server process, not the reloader
        if os.environ.get("RUN_MAIN") == "true":
            # If this is the reloader, just run the server without
            # starting Vite
            logging.debug(
                f"Reloader process, not starting Vite. PID: {os.getpid()}"
            )
            super().handle(*args, **options)
        else:
            logging.debug(f"Starting Vite... (PID: {os.getpid()})")
            vite_process = subprocess.Popen(
                ["npm", "start"], cwd=os.path.join(os.getcwd(), "app/static")
            )
            try:
                logging.debug(
                    f"Starting Django server... (PID: {os.getpid()})"
                )
                super().handle(*args, **options)
            finally:
                logging.debug(f"Terminating Vite... (PID: {os.getpid()})")
                vite_process.terminate()
                vite_process.wait()
