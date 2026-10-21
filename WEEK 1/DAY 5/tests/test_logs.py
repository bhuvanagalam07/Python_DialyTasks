import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from log_analyzer import LogAnalyzer


def test_read_logs(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        "2026-10-09 09:00:00 INFO Application started\n"
        "2026-10-09 09:01:00 ERROR Database failed\n",
        encoding="utf-8",
    )

    analyzer = LogAnalyzer(log_file)

    lines = analyzer.read_logs()

    assert len(lines) == 2
    assert "INFO Application started" in lines[0]


def test_analyze_counts_log_levels(tmp_path):
    log_file = tmp_path / "app.log"
    log_file.write_text(
        "2026-10-09 09:00:00 INFO Started\n"
        "2026-10-09 09:01:00 WARNING High memory\n"
        "2026-10-09 09:02:00 ERROR Database failed\n",
        encoding="utf-8",
    )

    report = LogAnalyzer(log_file).analyze()

    assert report["total_lines"] == 3
    assert report["counts"]["INFO"] == 1
    assert report["counts"]["WARNING"] == 1
    assert report["counts"]["ERROR"] == 1
    assert len(report["errors"]) == 1
    assert len(report["warnings"]) == 1


def test_missing_log_file(tmp_path):
    log_file = tmp_path / "missing.log"
    analyzer = LogAnalyzer(log_file)

    try:
        analyzer.read_logs()
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        assert True


if __name__ == "__main__":
    import pytest

    sys.exit(pytest.main([__file__, "-v"]))
