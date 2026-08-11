from talamo_valid.architecture import check_architecture, check_pipeline_config


def test_valid_c1_architecture_passes_with_scope_info() -> None:
    report = check_architecture(
        {
            "target": "C1",
            "mapper_arch": "C1",
            "encoder": "IFEncoder",
            "layers": [
                {
                    "type": "Dense",
                    "neuron": "DigitalNeuron",
                    "synapse": "DigitalSynapse",
                }
            ],
            "quantization": {"strategy": "qat"},
        }
    )

    assert report.passed
    assert [finding.code for finding in report.findings] == ["RUNTIME_OUT_OF_SCOPE"]


def test_t1_target_fails_as_out_of_scope() -> None:
    report = check_architecture(
        {
            "target": "T1",
            "mapper_arch": "T1",
            "layers": [{"neuron": "DigitalNeuron", "synapse": "DigitalSynapse"}],
            "quantized": True,
        }
    )

    assert not report.passed
    assert {finding.code for finding in report.errors} == {
        "TARGET_OUT_OF_SCOPE",
        "UNSUPPORTED_MAPPER_ARCH",
    }


def test_unknown_component_names_fail() -> None:
    report = check_architecture(
        {
            "target": "C1",
            "mapper_arch": "C1",
            "encoder": "UnsupportedEncoder",
            "layers": [{"neuron": "LIF", "synapse": "DenseSynapse"}],
            "quantized": True,
        }
    )

    assert not report.passed
    assert {finding.code for finding in report.errors} == {
        "UNSUPPORTED_ENCODER",
        "UNSUPPORTED_NEURON",
        "UNSUPPORTED_SYNAPSE",
    }


def test_missing_quantization_warns() -> None:
    report = check_architecture(
        {
            "target": "C1",
            "mapper_arch": "C1",
            "layers": [{"neuron": "DigitalNeuron", "synapse": "DigitalSynapse"}],
        }
    )

    assert report.passed
    assert {finding.code for finding in report.warnings} == {"MISSING_QUANTIZATION"}


def test_pipeline_config_validates_data_constraints() -> None:
    report = check_pipeline_config(
        {
            "target": "C1",
            "mapper_arch": "C1",
            "encoder": "PeriodicRateEncoder",
            "data_constraints": ["DenseDataConstraint", "UnknownConstraint"],
            "quantized": True,
        }
    )

    assert not report.passed
    assert {finding.code for finding in report.errors} == {"UNSUPPORTED_DATA_CONSTRAINT"}
