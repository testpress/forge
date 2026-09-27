"""Dramatiq broker setup.

This is what actually wires up the task queue - not a Django app config -
mirroring the role config/celery.py used to play for Celery. Run a worker
with:

    uv run dramatiq config.dramatiq

(see docker-compose.yml's `worker` service, which does exactly that).

This module is imported from two different places, which need two
different amounts of Django bootstrapping:

- The `dramatiq` CLI above imports it directly, into a bare Python
  process where nothing has touched Django yet. Dramatiq has no
  Celery-style automatic Django integration ("fixup") that notices
  DJANGO_SETTINGS_MODULE and calls django.setup() for you, so this
  module has to call it explicitly, before anything below it touches
  Django models - app.domain.background_task does, and so does anything
  imported from app.tasks.
- app/apps.py's AppConfig.ready() also imports it, so that every other
  process - a view handling a request, a shell session, a test - gets
  the same configured broker rather than Dramatiq's own unconfigured
  default. But ready() itself runs *during* django.setup()'s call to
  apps.populate(), so calling django.setup() again here would hit
  Django's own "populate() isn't reentrant" guard. apps.loading is True
  for exactly that window (see django.apps.registry.Apps.populate), so
  it's used below to skip the redundant, unsafe second call - by the
  time ready() runs, settings and models are already loaded regardless.
"""

import os
from typing import TYPE_CHECKING

import django
from django.apps import apps as django_apps

if django_apps.loading:
    pass
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.base")
    django.setup()

import dramatiq  # noqa: E402
from dramatiq.brokers.redis import RedisBroker  # noqa: E402
from dramatiq.middleware import CurrentMessage  # noqa: E402
from django.conf import settings  # noqa: E402
from django.db import close_old_connections  # noqa: E402

from app.domain.background_task import BackgroundTaskMiddleware  # noqa: E402

if TYPE_CHECKING:
    from dramatiq.broker import Broker
    from dramatiq.broker import MessageProxy


class DjangoDBMiddleware(dramatiq.Middleware):
    """Releases Django's DB connections after each task.

    Worker threads are long-lived, unlike Django's own per-request
    lifecycle, so without this a connection can go stale (timed out,
    dropped by the DB) and every task after that fails until the worker
    is restarted. Django already handles exactly this for HTTP requests
    by calling close_old_connections() on the request_started/
    request_finished signals; after_process_message is the Dramatiq
    equivalent of that boundary.
    """

    def after_process_message(
        self,
        broker: "Broker",
        message: "MessageProxy",
        *,
        result: object = None,
        exception: BaseException | None = None,
    ) -> None:
        close_old_connections()


# dramatiq ships py.typed, but RedisBroker.__init__ itself has no
# parameter annotations (it's `def __init__(self, *, url=None, ...)`),
# which mypy's strict mode still treats as an untyped call.
redis_broker = RedisBroker(  # type: ignore[no-untyped-call]
    url=settings.DRAMATIQ_BROKER_URL,
)
redis_broker.add_middleware(DjangoDBMiddleware())
# Exposes CurrentMessage.get_current_message() inside an actor - the
# Dramatiq equivalent of Celery's `self.request` on a bound task. Not
# enabled by default, unlike the two middlewares above it.
redis_broker.add_middleware(CurrentMessage())
redis_broker.add_middleware(BackgroundTaskMiddleware())
dramatiq.set_broker(redis_broker)

# Import every actor module so its @dramatiq.actor-decorated functions
# register with the broker above - the Dramatiq equivalent of Celery's
# app.autodiscover_tasks(["app.tasks"]).
from app import tasks  # noqa: E402,F401
