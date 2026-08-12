"""Heimdall namespace for Talamo design-time validation tools."""

from talamo_valid import (
    check_architecture,
    check_pipeline_config,
    get_talamo_constraints,
)

provider = {
    "vendor": "talamo",
    "kind": "valid",
    "package": "talamo-valid",
    "module": __name__,
    "mcp": "heimdall.talamo.valid.mcp",
}

__all__ = [
    "check_architecture",
    "check_pipeline_config",
    "get_talamo_constraints",
    "provider",
]
