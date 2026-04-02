from validator.reporter import format_human, format_json

SAMPLE = [
    {"release": "jammy", "version": "20240101", "arch": "amd64",
     "ftype": "disk1.img", "cloud": "aws", "sha256": "abc123", "size": 500000000}
]

def test_human_report_contains_release():
    output = format_human(SAMPLE)
    assert "jammy" in output

def test_human_report_shows_total():
    output = format_human(SAMPLE)
    assert "Total images found: 1" in output

def test_human_empty_list():
    output = format_human([])
    assert "No images found" in output

def test_json_output_is_valid():
    import json
    output = format_json(SAMPLE)
    parsed = json.loads(output)
    assert parsed[0]["release"] == "jammy"
