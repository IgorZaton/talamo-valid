from talamo_valid.constraints import get_talamo_constraints


def test_constraints_are_c1_only() -> None:
    constraints = get_talamo_constraints()

    assert constraints["scope"]["supported_targets"] == ["C1"]
    assert "T1" in constraints["scope"]["out_of_scope_targets"]
    assert constraints["mapper"]["supported_arch_codes"] == ["C1"]
    assert "IFEncoder" in constraints["c1"]["encoders"]
    assert "DigitalNeuron" in constraints["c1"]["neurons"]
    assert "DigitalSynapse" in constraints["c1"]["synapses"]
