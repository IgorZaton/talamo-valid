import pytest

mcp = pytest.importorskip("mcp")
assert mcp

from talamo_valid_mcp.server import (  # noqa: E402
    check_architecture_tool,
    check_pipeline_config_tool,
    get_talamo_constraints_tool,
)


def test_mcp_constraints_tool_payload() -> None:
    payload = get_talamo_constraints_tool()

    assert payload["scope"]["supported_targets"] == ["C1"]


def test_mcp_check_architecture_payload() -> None:
    payload = check_architecture_tool(
        {
            "target": "C1",
            "mapper_arch": "C1",
            "layers": [{"neuron": "DigitalNeuron", "synapse": "DigitalSynapse"}],
            "quantized": True,
        }
    )

    assert payload["status"] == "PASS"


def test_mcp_check_pipeline_config_payload() -> None:
    payload = check_pipeline_config_tool(
        {
            "target": "C1",
            "mapper_arch": "C1",
            "encoder": "IFEncoder",
            "data_constraints": ["DenseDataConstraint"],
            "quantized": True,
        }
    )

    assert payload["status"] == "PASS"
