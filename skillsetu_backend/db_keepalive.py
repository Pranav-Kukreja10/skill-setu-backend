"""
Database Keep-Alive Daemon & Activity Window Manager for Neon Serverless PostgreSQL.

Architecture:
1. Smart Activity Window:
   - When a user or evaluator visits the platform, activity is recorded.
   - Neon is kept active and warm (pinged every 150s with 'SELECT 1') for 45 minutes
     following the last user interaction.
   - If no requests occur for 45 minutes, the daemon stops pinging, allowing Neon to
     scale to zero and safely conserve the 100 CU-hour monthly free-tier quota.
2. Lightweight Middleware:
   - DatabaseActivityMiddleware detects incoming API / page requests and updates
     the activity window automatically.
   - Excludes external uptime pings (/ping) so automated Render monitors keep Render
     awake 24/7 without consuming Neon database hours.
"""

import os
import sys
import time
import logging
import threading
from typing import Tuple

logger = logging.getLogger("skillsetu.db_keepalive")

# Thread synchronization
_lock = threading.Lock()
_stop_event = threading.Event()
_keepalive_thread: threading.Thread = None

# Activity tracking (initialized to server start time so initial boot gives a warm window)
_last_activity_time: float = time.time()

# Configuration (overridable via environment variables)
# Default window: 45 minutes (2700 seconds) of continuous keepalive after last request
ACTIVITY_WINDOW_SECONDS = int(os.getenv("DB_ACTIVITY_WINDOW_SECONDS", "2700"))
# Ping interval: 150 seconds (safely under Neon's 300s / 5min scale-to-zero suspension)
PING_INTERVAL_SECONDS = int(os.getenv("DB_KEEPALIVE_INTERVAL", "150"))
# Global master switch
KEEPALIVE_ENABLED = os.getenv("DB_KEEPALIVE_ENABLED", "True").lower() in ("true", "1")


def record_activity(source: str = "request") -> None:
    """Record user activity to keep the database awake for the active window."""
    global _last_activity_time
    with _lock:
        _last_activity_time = time.time()
    logger.debug(f"Activity recorded from '{source}'. DB active window refreshed.")


def get_last_activity_timestamp() -> float:
    """Return the timestamp of the last recorded activity."""
    with _lock:
        return _last_activity_time


def is_within_activity_window() -> bool:
    """Check whether we are currently within the active evaluation window."""
    with _lock:
        elapsed = time.time() - _last_activity_time
    return elapsed < ACTIVITY_WINDOW_SECONDS


def get_window_status() -> dict:
    """Return a diagnostic dictionary describing the keepalive status."""
    with _lock:
        elapsed = time.time() - _last_activity_time
    remaining = max(0, int(ACTIVITY_WINDOW_SECONDS - elapsed))
    is_active = remaining > 0
    return {
        "enabled": KEEPALIVE_ENABLED,
        "is_active_window": is_active,
        "seconds_since_last_activity": int(elapsed),
        "seconds_remaining_in_window": remaining,
        "activity_window_total_seconds": ACTIVITY_WINDOW_SECONDS,
        "ping_interval_seconds": PING_INTERVAL_SECONDS,
        "daemon_alive": _keepalive_thread.is_alive() if _keepalive_thread else False,
    }


def ping_database() -> Tuple[bool, float, str]:
    """
    Execute a lightweight 'SELECT 1;' query on the default database.
    Returns: (success: bool, latency_ms: float, message: str)
    """
    from django.db import connection, connections

    start = time.perf_counter()
    try:
        # Close any stale connections before checking
        connections.close_all()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
        latency_ms = (time.perf_counter() - start) * 1000.0

        # Close the connection immediately so PgBouncer / Neon connection pools
        # are not held open with idle locks
        connections.close_all()

        if row and row[0] == 1:
            return True, round(latency_ms, 2), "OK"
        return False, round(latency_ms, 2), f"Unexpected response: {row}"
    except Exception as exc:
        latency_ms = (time.perf_counter() - start) * 1000.0
        try:
            connections.close_all()
        except Exception:
            pass
        return False, round(latency_ms, 2), str(exc)


def _keepalive_worker() -> None:
    """Background daemon loop that periodically pings Neon while inside an active window."""
    logger.info(
        f"Neon DB Keep-Alive daemon started (Interval: {PING_INTERVAL_SECONDS}s, "
        f"Window: {ACTIVITY_WINDOW_SECONDS // 60} min)."
    )

    while not _stop_event.is_set():
        # Wait for the next ping interval or stop event
        if _stop_event.wait(PING_INTERVAL_SECONDS):
            break

        if not is_within_activity_window():
            logger.debug(
                "Keep-alive: Outside active evaluation window. Letting database idle/sleep to conserve CU-hours."
            )
            continue

        # We are within the active evaluation window: ping to keep Neon awake
        success, latency_ms, msg = ping_database()
        status = get_window_status()
        remaining_min = status["seconds_remaining_in_window"] // 60

        if success:
            logger.info(
                f"[Neon KeepAlive] Ping successful ({latency_ms}ms). "
                f"Neon kept awake (~{remaining_min}m left in active window)."
            )
        else:
            logger.warning(
                f"[Neon KeepAlive] Ping failed ({latency_ms}ms): {msg}. Retrying next cycle."
            )


def start_db_keepalive() -> None:
    """Start the background keep-alive daemon if not already running."""
    global _keepalive_thread

    if not KEEPALIVE_ENABLED:
        logger.info("Neon DB Keep-Alive disabled by configuration (DB_KEEPALIVE_ENABLED=False).")
        return

    # Avoid duplicate threads in Django development reloader (runserver)
    if os.environ.get("RUN_MAIN") == "false":
        return

    with _lock:
        if _keepalive_thread is not None and _keepalive_thread.is_alive():
            return

        _stop_event.clear()
        _keepalive_thread = threading.Thread(
            target=_keepalive_worker,
            name="NeonKeepAliveDaemon",
            daemon=True,
        )
        _keepalive_thread.start()


def stop_db_keepalive() -> None:
    """Signal the background keep-alive daemon to terminate."""
    _stop_event.set()


class DatabaseActivityMiddleware:
    """
    Django middleware that refreshes the database activity window on every user request.
    Pings to '/api/v1/ping' or '/ping' are ignored so external Render monitors can keep
    the web server awake without forcing Neon to stay awake 24/7.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        # Skip uptime ping endpoints
        if not (path.endswith("/ping") or path.endswith("/ping/")):
            record_activity(source=path)
        return self.get_response(request)
