"""Docs-derived Talamo C1 compatibility constants."""

from __future__ import annotations

DOCS_ROOT = (
    "/home/igor/Desktop/projects/innatera-t1-evk-lemur/docs/sdk:4.7.1/"
    "talamo_docs_v4.7.1/html"
)

DOCS_VERSION = "4.7.1"
SUPPORTED_TARGET = "C1"
SUPPORTED_MAPPER_ARCH_CODES = frozenset({"C1"})
OUT_OF_SCOPE_TARGETS = frozenset({"T1", "T1_Digital"})

C1_ENCODERS = frozenset(
    {
        "IFEncoder",
        "PeriodicRateEncoder",
        "TemporalContrastEncoder",
    }
)

C1_NEURONS = frozenset(
    {
        "AnalogNeuron",
        "DigitalNeuron",
        "analog_neuron",
        "digital_neuron",
    }
)

C1_SYNAPSES = frozenset(
    {
        "AnalogSynapse",
        "DigitalSynapse",
        "analog_synapse",
        "digital_synapse",
    }
)

PIPELINE_DATA_CONSTRAINTS = frozenset(
    {
        "DataConstraint",
        "DenseDataConstraint",
    }
)

QUANTIZATION_APIS = frozenset(
    {
        "Quantizer",
        "RoundAndClamp",
    }
)

DOC_CITATIONS = {
    "t1_deprecation": "index.html:163",
    "c1_device": "api/device/index.html:196-197",
    "c1_hardware": "api/hardware/index.html:152-153",
    "c1_encoders": "api/encoders/c1.html:148-151",
    "c1_mapper": "api/mapper/index.html:154-165",
    "data_constraints": "api/pipeline/embedded.html:149-152",
    "quantization": "api/quantization/index.html:145-148",
    "input_spike_constraints": "_generated/talamo.encoders.InputSpikeConstraints.html",
}
