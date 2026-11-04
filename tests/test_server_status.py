import io
import json
import unittest
from contextlib import redirect_stdout
from types import SimpleNamespace
from unittest.mock import patch

import server_status


class ServerStatusTests(unittest.TestCase):
    @patch.object(server_status.psutil, "disk_usage")
    @patch.object(server_status.psutil, "virtual_memory")
    @patch.object(server_status.psutil, "cpu_count", return_value=8)
    @patch.object(server_status.psutil, "cpu_percent", return_value=23.5)
    def test_collect_status_contains_resource_values(
        self, cpu_percent, cpu_count, virtual_memory, disk_usage
    ):
        virtual_memory.return_value = SimpleNamespace(
            total=16_000, used=6_000, available=10_000, percent=37.5
        )
        disk_usage.return_value = SimpleNamespace(
            total=100_000, used=40_000, free=60_000, percent=40.0
        )

        status = server_status.collect_status()

        self.assertEqual(status["cpu"], {"percent": 23.5, "count": 8})
        self.assertEqual(status["memory"]["available_bytes"], 10_000)
        self.assertEqual(status["disk"]["free_bytes"], 60_000)
        disk_usage.assert_called_once_with("/")

    def test_format_report_is_readable(self):
        status = {
            "cpu": {"percent": 23.5, "count": 8},
            "memory": {
                "total_bytes": 16 * 1024**3,
                "used_bytes": 6 * 1024**3,
                "available_bytes": 10 * 1024**3,
                "percent": 37.5,
            },
            "disk": {
                "path": "/",
                "total_bytes": 100 * 1024**3,
                "used_bytes": 40 * 1024**3,
                "free_bytes": 60 * 1024**3,
                "percent": 40.0,
            },
        }

        report = server_status.format_report(status)

        self.assertIn("Server status (local host)", report)
        self.assertIn("CPU:    23.5% (8 logical cores)", report)
        self.assertIn("Memory: 6.0 GiB used / 16.0 GiB total (37.5%)", report)
        self.assertIn("Disk /: 40.0 GiB used / 100.0 GiB total (40.0%)", report)

    @patch.object(server_status, "collect_status", return_value={"cpu": {"percent": 1}})
    def test_json_flag_outputs_json(self, collect_status):
        output = io.StringIO()
        with patch("sys.argv", ["server-status", "--json"]), redirect_stdout(output):
            self.assertEqual(server_status.main(), 0)

        self.assertEqual(json.loads(output.getvalue()), {"cpu": {"percent": 1}})
        collect_status.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
