"""Command-line interface for talamo-valid."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from talamo_valid.architecture import check_architecture, check_pipeline_config
from talamo_valid.constraints import get_talamo_constraints


def main(argv: list[str] | None = None) -> int:
    """Run the talamo-valid CLI."""
    parser = argparse.ArgumentParser(
        prog="talamo-valid",
        description="Talamo C1 design-time compatibility checks",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("constraints", help="Print Talamo C1 constraints as JSON")

    architecture_parser = subparsers.add_parser(
        "check-architecture",
        help="Validate a planned SNN architecture JSON file",
    )
    architecture_parser.add_argument("path", help="Path to architecture JSON")

    pipeline_parser = subparsers.add_parser(
        "check-pipeline",
        help="Validate a planned pipeline config JSON file",
    )
    pipeline_parser.add_argument("path", help="Path to pipeline config JSON")

    args = parser.parse_args(argv)

    if args.command == "constraints":
        print(json.dumps(get_talamo_constraints(), indent=2, sort_keys=True))
        return 0

    if args.command == "check-architecture":
        payload = _load_json(Path(args.path))
        report = check_architecture(payload).to_dict()
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["passed"] else 1

    if args.command == "check-pipeline":
        payload = _load_json(Path(args.path))
        report = check_pipeline_config(payload).to_dict()
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["passed"] else 1

    parser.error(f"unknown command {args.command}")
    return 2


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError as error:
        raise SystemExit(f"{path}: file not found") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"{path}: invalid JSON: {error}") from error

    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected a JSON object")
    return data
