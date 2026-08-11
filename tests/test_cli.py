import json

from talamo_valid.cli import main


def test_constraints_command_prints_json(capsys) -> None:
    assert main(["constraints"]) == 0

    output = json.loads(capsys.readouterr().out)
    assert output["scope"]["supported_targets"] == ["C1"]


def test_check_architecture_returns_nonzero_for_error(tmp_path, capsys) -> None:
    payload = tmp_path / "architecture.json"
    payload.write_text('{"target": "T1", "layers": []}')

    assert main(["check-architecture", str(payload)]) == 1

    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "FAIL"
