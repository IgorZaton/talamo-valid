"""talamo-valid MCP server: C1 design-time constraints and checks."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from talamo_valid.architecture import check_architecture, check_pipeline_config
from talamo_valid.constraints import get_talamo_constraints

mcp = FastMCP(
    "talamo-valid",
    instructions=(
        "Talamo C1 compatibility helper. Use get_talamo_constraints before "
        "designing a Talamo SNN, check_architecture to validate planned C1 "
        "layer/neuron/synapse choices, and check_pipeline_config to validate "
        "high-level C1 pipeline metadata. T1/T1_Digital and simulator execution "
        "are out of scope for this initial release."
    ),
)


@mcp.tool(name="get_talamo_constraints")
def get_talamo_constraints_tool() -> dict[str, Any]:
    """Return Talamo C1 design-time constraints and known caveats."""
    return get_talamo_constraints()


@mcp.tool(name="check_architecture")
def check_architecture_tool(architecture: dict[str, Any]) -> dict[str, Any]:
    """Validate a planned Talamo C1 SNN architecture.

    Args:
        architecture: Architecture JSON object with target, mapper_arch, encoder,
            layers, and optional quantization metadata.
    """
    return check_architecture(architecture).to_dict()


@mcp.tool(name="check_pipeline_config")
def check_pipeline_config_tool(config: dict[str, Any]) -> dict[str, Any]:
    """Validate a planned Talamo C1 pipeline config.

    Args:
        config: Pipeline JSON object with target, mapper_arch, encoder,
            data_constraints, and optional quantization metadata.
    """
    return check_pipeline_config(config).to_dict()


def main() -> None:
    """Run the MCP server."""
    mcp.run()
