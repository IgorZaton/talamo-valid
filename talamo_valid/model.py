"""Structured compatibility report models."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Severity(str, Enum):
    """Compatibility finding severity."""

    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass(frozen=True)
class Finding:
    """A machine-readable validation finding."""

    severity: Severity
    code: str
    message: str
    path: str | None = None
    value: Any | None = None

    def format(self) -> str:
        """Return a compact human-readable finding string."""
        location = f" at {self.path}" if self.path else ""
        value = f" (value={self.value!r})" if self.value is not None else ""
        return f"{self.severity.value}: [{self.code}]{location} {self.message}{value}"

    def to_dict(self) -> dict[str, Any]:
        """Serialize the finding for CLI and MCP clients."""
        return {
            "severity": self.severity.value,
            "code": self.code,
            "message": self.message,
            "path": self.path,
            "value": self.value,
            "text": self.format(),
        }


@dataclass(frozen=True)
class CompatibilityReport:
    """Validation result payload shared by CLI and MCP."""

    findings: tuple[Finding, ...] = field(default_factory=tuple)

    @property
    def errors(self) -> tuple[Finding, ...]:
        """Return error findings."""
        return tuple(finding for finding in self.findings if finding.severity == Severity.ERROR)

    @property
    def warnings(self) -> tuple[Finding, ...]:
        """Return warning findings."""
        return tuple(finding for finding in self.findings if finding.severity == Severity.WARNING)

    @property
    def passed(self) -> bool:
        """Whether no error findings were reported."""
        return not self.errors

    def summary(self) -> str:
        """Return a one-line report summary."""
        if self.passed:
            if self.warnings:
                return f"PASS with {len(self.warnings)} warning(s)"
            return "PASS: Talamo C1 compatibility checks passed"
        return f"FAIL: {len(self.errors)} error(s), {len(self.warnings)} warning(s)"

    def to_dict(self) -> dict[str, Any]:
        """Serialize the report for CLI and MCP clients."""
        return {
            "passed": self.passed,
            "status": "PASS" if self.passed else "FAIL",
            "summary": self.summary(),
            "findings": [finding.to_dict() for finding in self.findings],
            "errors": [finding.to_dict() for finding in self.errors],
            "warnings": [finding.to_dict() for finding in self.warnings],
        }
