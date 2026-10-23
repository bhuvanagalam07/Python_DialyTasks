import json
from weather_processor.main import main


def test_cli_end_to_end_with_sample_data(tmp_path):
    input_file = tmp_path / "weather.json"
    input_file.write_text(json.dumps([
        {"city": "A", "temperature": 10},
        {"city": "B", "temperature": 20},
    ]), encoding="utf-8")
    output = tmp_path / "reports"
    assert main(["--input", str(input_file), "--output-dir", str(output)]) == 0
    payload = json.loads((output / "weather_report.json").read_text(encoding="utf-8"))
    assert payload["total_cities"] == 2
    assert payload["average_temperature"] == 15.0
    assert payload["data_source"] == "sample_file"


def test_missing_input_returns_nonzero_without_traceback(tmp_path, capsys):
    result = main(["--input", str(tmp_path / "missing.json"), "--output-dir", str(tmp_path / "out")])
    captured = capsys.readouterr()
    assert result == 1
    assert "Input file not found" in captured.err
