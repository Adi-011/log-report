import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")
REQUIRED_KEYS = {"total_requests", "unique_ips", "top_path"}


def _compute_ground_truth():
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    top_paths = {p for p, c in paths.items() if c == max(paths.values())}
    return total, len(ips), top_paths


def test_report_exists_and_is_valid_json():
    """Criterion 1: /app/report.json exists and contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    try:
        json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")


def test_report_has_exactly_required_keys():
    """Criterion 2: report.json has exactly total_requests, unique_ips, top_path — no extras."""
    report = json.loads(REPORT_PATH.read_text())
    assert set(report.keys()) == REQUIRED_KEYS, (
        f"expected keys {REQUIRED_KEYS}, got {set(report.keys())}"
    )


def test_total_requests_is_correct():
    """Criterion 3: total_requests matches the actual number of requests in access.log."""
    report = json.loads(REPORT_PATH.read_text())
    expected_total, _, _ = _compute_ground_truth()
    assert report["total_requests"] == expected_total, (
        f"total_requests: expected {expected_total}, got {report['total_requests']!r}"
    )


def test_unique_ips_is_correct():
    """Criterion 4: unique_ips matches the actual number of distinct client IPs in access.log."""
    report = json.loads(REPORT_PATH.read_text())
    _, expected_unique_ips, _ = _compute_ground_truth()
    assert report["unique_ips"] == expected_unique_ips, (
        f"unique_ips: expected {expected_unique_ips}, got {report['unique_ips']!r}"
    )


def test_top_path_is_correct():
    """Criterion 5: top_path matches the actual most-requested path in access.log."""
    report = json.loads(REPORT_PATH.read_text())
    _, _, expected_top_paths = _compute_ground_truth()
    assert report["top_path"] in expected_top_paths, (
        f"top_path: expected one of {sorted(expected_top_paths)}, got {report['top_path']!r}"
    )