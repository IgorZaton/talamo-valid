# talamo-valid

Design-time Talamo C1 compatibility checks for agents and MCP clients.

`talamo-valid` is the static validation peer to a future runtime/simulator
package. It helps an agent choose Talamo C1-compatible SNN components before
training, mapping, or deployment.

## Scope

Initial version:

- supports **C1 only**
- exposes docs-derived constraints for C1 encoders, neurons, synapses, pipeline
  data constraints, and quantization guidance
- validates planned architecture and pipeline JSON payloads
- rejects `T1` and `T1_Digital` as out of scope
- does **not** import Talamo, run the simulator, map networks, or deploy to
  hardware

Runtime execution should live in a later `talamo-run` style package.

## Install

From a clone:

```bash
poetry install
poetry install -E mcp
```

Editable install:

```bash
pip install -e .
pip install -e ".[mcp]"
```

## CLI

Print the C1 constraint payload:

```bash
talamo-valid constraints
```

Validate a planned architecture:

```bash
talamo-valid check-architecture architecture.json
```

Example `architecture.json`:

```json
{
  "target": "C1",
  "mapper_arch": "C1",
  "encoder": "IFEncoder",
  "layers": [
    {
      "type": "Dense",
      "neuron": "DigitalNeuron",
      "synapse": "DigitalSynapse"
    }
  ],
  "quantization": {
    "strategy": "qat"
  }
}
```

Validate a pipeline config:

```bash
talamo-valid check-pipeline pipeline.json
```

## MCP

Run the MCP server:

```bash
poetry run talamo-valid-mcp
```

Tools:

| Tool | Purpose |
| --- | --- |
| `get_talamo_constraints` | Return C1 design-time constraints and caveats |
| `check_architecture` | Validate planned C1 layer/neuron/synapse choices |
| `check_pipeline_config` | Validate high-level C1 pipeline metadata |

## Tests

```bash
poetry run pytest -q
```