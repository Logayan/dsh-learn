"""Report local CPU, memory, and disk utilization."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict

import psutil


def collect_status() -> Dict[str, Any]:
    """Collect a point-in-time status snapshot from the local host."""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=0.1),
            "count": psutil.cpu_count(),
        },
        "memory": {
            "total_bytes": memory.total,
            "used_bytes": memory.used,
            "available_bytes": memory.available,
            "percent": memory.percent,
        },
        "disk": {
            "path": "/",
            "total_bytes": disk.total,
            "used_bytes": disk.used,
            "free_bytes": disk.free,
            "percent": disk.percent,
        },
    }


def _bytes_to_gib(value: int) -> str:
    return f"{value / (1024 ** 3):.1f} GiB"


def format_report(status: Dict[str, Any]) -> str:
    """Format a status snapshot for people to read."""
    cpu = status["cpu"]
    memory = status["memory"]
    disk = status["disk"]
    lines = [
        "Server status (local host)",
        f"CPU:    {cpu['percent']:.1f}% ({cpu['count'] or 'unknown'} logical cores)",
        (
            "Memory: "
            f"{_bytes_to_gib(memory['used_bytes'])} used / "
            f"{_bytes_to_gib(memory['total_bytes'])} total ({memory['percent']:.1f}%)"
        ),
        (
            f"Disk {disk['path']}: "
            f"{_bytes_to_gib(disk['used_bytes'])} used / "
            f"{_bytes_to_gib(disk['total_bytes'])} total ({disk['percent']:.1f}%)"
        ),
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Show local CPU, memory, and disk usage.")
    parser.add_argument("--json", action="store_true", help="output the report as JSON")
    args = parser.parse_args()

    status = collect_status()
    if args.json:
        print(json.dumps(status, indent=2, sort_keys=True))
    else:
        print(format_report(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
