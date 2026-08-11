"""Talamo C1 architecture and pipeline validation."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from talamo_valid import requirements as req
from talamo_valid.model import CompatibilityReport, Finding, Severity


def check_architecture(architecture: Mapping[str, Any]) -> CompatibilityReport:
    """Validate a planned Talamo C1 SNN architecture."""
    findings: list[Finding] = []
    target = _string_value(architecture.get("target"), default=req.SUPPORTED_TARGET)
    mapper_arch = _string_value(architecture.get("mapper_arch"), default=target)

    _validate_target(target, findings, "target")
    _validate_mapper_arch(mapper_arch, findings, "mapper_arch")
    _validate_named_component(
        architecture.get("encoder"),
        req.C1_ENCODERS,
        findings,
        code="UNSUPPORTED_ENCODER",
        path="encoder",
        component_name="encoder",
        required=False,
    )
    _validate_layers(architecture.get("layers", []), findings)
    _validate_quantization(architecture, findings)
    _add_runtime_scope_note(findings)
    return CompatibilityReport(tuple(findings))


def check_pipeline_config(config: Mapping[str, Any]) -> CompatibilityReport:
    """Validate a high-level Talamo C1 pipeline configuration."""
    findings: list[Finding] = []
    target = _string_value(config.get("target"), default=req.SUPPORTED_TARGET)
    mapper_arch = _string_value(config.get("mapper_arch"), default=target)

    _validate_target(target, findings, "target")
    _validate_mapper_arch(mapper_arch, findings, "mapper_arch")
    _validate_named_component(
        config.get("encoder"),
        req.C1_ENCODERS,
        findings,
        code="UNSUPPORTED_ENCODER",
        path="encoder",
        component_name="encoder",
        required=False,
    )
    _validate_data_constraints(config.get("data_constraints", []), findings)
    _validate_quantization(config, findings)
    _add_runtime_scope_note(findings)
    return CompatibilityReport(tuple(findings))


def _validate_layers(value: Any, findings: list[Finding]) -> None:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        findings.append(
            Finding(
                Severity.ERROR,
                "INVALID_LAYERS",
                "layers must be a list of layer objects",
                path="layers",
                value=value,
            )
        )
        return

    for index, layer in enumerate(value):
        if not isinstance(layer, Mapping):
            findings.append(
                Finding(
                    Severity.ERROR,
                    "INVALID_LAYER",
                    "layer entries must be objects",
                    path=f"layers[{index}]",
                    value=layer,
                )
            )
            continue
        _validate_named_component(
            layer.get("neuron"),
            req.C1_NEURONS,
            findings,
            code="UNSUPPORTED_NEURON",
            path=f"layers[{index}].neuron",
            component_name="neuron",
            required=True,
        )
        _validate_named_component(
            layer.get("synapse"),
            req.C1_SYNAPSES,
            findings,
            code="UNSUPPORTED_SYNAPSE",
            path=f"layers[{index}].synapse",
            component_name="synapse",
            required=True,
        )


def _validate_target(target: str, findings: list[Finding], path: str) -> None:
    if target in req.OUT_OF_SCOPE_TARGETS:
        findings.append(
            Finding(
                Severity.ERROR,
                "TARGET_OUT_OF_SCOPE",
                "initial talamo-valid release supports C1 only",
                path=path,
                value=target,
            )
        )
        return
    if target != req.SUPPORTED_TARGET:
        findings.append(
            Finding(
                Severity.ERROR,
                "UNKNOWN_TARGET",
                "target must be C1 for this release",
                path=path,
                value=target,
            )
        )


def _validate_mapper_arch(mapper_arch: str, findings: list[Finding], path: str) -> None:
    if mapper_arch not in req.SUPPORTED_MAPPER_ARCH_CODES:
        findings.append(
            Finding(
                Severity.ERROR,
                "UNSUPPORTED_MAPPER_ARCH",
                "mapper_arch must be C1 for this release",
                path=path,
                value=mapper_arch,
            )
        )


def _validate_named_component(
    value: Any,
    allowed: frozenset[str],
    findings: list[Finding],
    *,
    code: str,
    path: str,
    component_name: str,
    required: bool,
) -> None:
    if value is None:
        if required:
            findings.append(
                Finding(
                    Severity.ERROR,
                    f"MISSING_{component_name.upper()}",
                    f"layer {component_name} is required",
                    path=path,
                )
            )
        return

    name = _string_value(value)
    if name not in allowed:
        findings.append(
            Finding(
                Severity.ERROR,
                code,
                f"{component_name} is not in the C1 allowlist",
                path=path,
                value=value,
            )
        )


def _validate_data_constraints(value: Any, findings: list[Finding]) -> None:
    if value in (None, []):
        return
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        findings.append(
            Finding(
                Severity.ERROR,
                "INVALID_DATA_CONSTRAINTS",
                "data_constraints must be a list of constraint names",
                path="data_constraints",
                value=value,
            )
        )
        return
    for index, item in enumerate(value):
        name = _string_value(item)
        if name not in req.PIPELINE_DATA_CONSTRAINTS:
            findings.append(
                Finding(
                    Severity.ERROR,
                    "UNSUPPORTED_DATA_CONSTRAINT",
                    "data constraint is not in the C1 pipeline allowlist",
                    path=f"data_constraints[{index}]",
                    value=item,
                )
            )


def _validate_quantization(payload: Mapping[str, Any], findings: list[Finding]) -> None:
    quantization = payload.get("quantization")
    quantized = payload.get("quantized")
    if quantization is None and quantized is not True:
        findings.append(
            Finding(
                Severity.WARNING,
                "MISSING_QUANTIZATION",
                "hardware deployment should include explicit quantization guidance",
                path="quantization",
            )
        )


def _add_runtime_scope_note(findings: list[Finding]) -> None:
    findings.append(
        Finding(
            Severity.INFO,
            "RUNTIME_OUT_OF_SCOPE",
            "talamo-valid performs static checks only; simulator/hardware execution is out of scope",
        )
    )


def _string_value(value: Any, default: str | None = None) -> str:
    if value is None:
        if default is None:
            return ""
        return default
    return str(value)
