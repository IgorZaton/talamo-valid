"""Serialize Talamo C1 constraints for agents and docs consumers."""

from __future__ import annotations

from typing import Any

from talamo_valid import requirements as req


def get_talamo_constraints() -> dict[str, Any]:
    """Return Talamo C1 design-time compatibility metadata."""
    return {
        "docs": {
            "version": req.DOCS_VERSION,
            "root": req.DOCS_ROOT,
            "citations": req.DOC_CITATIONS,
        },
        "scope": {
            "supported_targets": [req.SUPPORTED_TARGET],
            "out_of_scope_targets": sorted(req.OUT_OF_SCOPE_TARGETS),
            "runtime_execution": False,
            "simulator_execution": False,
            "notes": [
                "Initial talamo-valid release is C1-only.",
                "T1/T1_Digital are rejected as out of scope for this package version.",
                "Simulator and hardware execution should live in a future talamo-run package.",
            ],
        },
        "mapper": {
            "supported_arch_codes": sorted(req.SUPPORTED_MAPPER_ARCH_CODES),
            "required_arch_code": req.SUPPORTED_TARGET,
        },
        "c1": {
            "device": "talamo.device.C1",
            "hardware": "talamo.hardware.C1Hardware",
            "encoders": sorted(req.C1_ENCODERS),
            "neurons": sorted(req.C1_NEURONS),
            "synapses": sorted(req.C1_SYNAPSES),
        },
        "pipeline": {
            "data_constraints": sorted(req.PIPELINE_DATA_CONSTRAINTS),
            "input_spike_constraints": "talamo.encoders.InputSpikeConstraints",
        },
        "quantization": {
            "apis": sorted(req.QUANTIZATION_APIS),
            "guidance": (
                "Hardware deployment should include explicit quantization or "
                "quantization-aware training decisions."
            ),
        },
        "finding_codes": {
            "TARGET_OUT_OF_SCOPE": "T1/T1_Digital requested in the C1-only initial release.",
            "UNKNOWN_TARGET": "Target is not recognized.",
            "UNSUPPORTED_MAPPER_ARCH": "Mapper arch code is not supported by this release.",
            "UNSUPPORTED_ENCODER": "Encoder is not in the C1 docs-derived allowlist.",
            "UNSUPPORTED_NEURON": "Neuron is not in the C1 docs-derived allowlist.",
            "UNSUPPORTED_SYNAPSE": "Synapse is not in the C1 docs-derived allowlist.",
            "MISSING_QUANTIZATION": "No quantization/deployment quantization guidance was supplied.",
            "RUNTIME_OUT_OF_SCOPE": "Runtime/simulator checks are intentionally not performed.",
        },
    }
