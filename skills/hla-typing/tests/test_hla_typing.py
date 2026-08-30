"""Tests for hla-typing.

Red/green TDD: the capability tests are `xfail(strict=True)` while
`run_analysis` is unimplemented. They fail today, and they turn XPASS — which
fails the suite — the moment a real HLA caller lands, forcing whoever
implements it to unmark them rather than inherit a falsely-green suite.
"""

import json
import subprocess
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

unimplemented = pytest.mark.xfail(
    strict=True,
    reason="hla-typing has no HLA calling implementation; run_analysis raises",
)

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "hla_typing.py"
DEMO_INPUT = SKILL_DIR / "demo_input.txt"


class TestCLI:
    """CLI interface tests."""

    def test_no_args_exits_nonzero(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            capture_output=True, text=True
        )
        assert result.returncode != 0

    @unimplemented
    def test_demo_mode_produces_output(self, tmp_path):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--demo", "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert (tmp_path / "report.md").exists()
        assert (tmp_path / "result.json").exists()

    @unimplemented
    def test_input_mode_produces_output(self, tmp_path):
        result = subprocess.run(
            [sys.executable, str(SCRIPT),
             "--input", str(DEMO_INPUT),
             "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert (tmp_path / "report.md").exists()

    def test_missing_input_exits_nonzero(self, tmp_path):
        result = subprocess.run(
            [sys.executable, str(SCRIPT),
             "--input", str(tmp_path / "nonexistent.txt"),
             "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        assert result.returncode != 0


class TestOutputFormat:
    """Output format validation."""

    @unimplemented
    def test_result_json_is_valid(self, tmp_path):
        subprocess.run(
            [sys.executable, str(SCRIPT), "--demo", "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        result = json.loads((tmp_path / "result.json").read_text())
        assert isinstance(result, dict)
        assert "skill" in result
        assert result["skill"] == "hla-typing"

    @unimplemented
    def test_report_contains_disclaimer(self, tmp_path):
        subprocess.run(
            [sys.executable, str(SCRIPT), "--demo", "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        report = (tmp_path / "report.md").read_text()
        assert "not a medical device" in report.lower()

    @unimplemented
    def test_result_has_variants_count(self, tmp_path):
        subprocess.run(
            [sys.executable, str(SCRIPT), "--demo", "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        result = json.loads((tmp_path / "result.json").read_text())
        assert "variants_processed" in result
        assert result["variants_processed"] > 0


class TestUnimplemented:
    """The skill must fail loudly rather than return an empty finding set."""

    def test_run_analysis_raises(self):
        spec = spec_from_file_location("hla_typing", SCRIPT)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        with pytest.raises(NotImplementedError, match="no HLA calling"):
            mod.run_analysis({"lines": ["chr6\t29910247\t.\tA\tG"], "source": "x"})

    def test_demo_exits_nonzero_and_writes_nothing(self, tmp_path):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--demo", "--output", str(tmp_path)],
            capture_output=True, text=True
        )
        assert result.returncode != 0
        assert "no HLA calling implementation" in result.stderr
        assert not (tmp_path / "report.md").exists()
        assert not (tmp_path / "result.json").exists()


class TestDemoData:
    """Demo data integrity."""

    def test_demo_input_exists(self):
        assert DEMO_INPUT.exists(), f"Demo data missing: {DEMO_INPUT}"

    def test_demo_input_has_content(self):
        content = DEMO_INPUT.read_text()
        lines = [l for l in content.splitlines() if l.strip() and not l.startswith("#")]
        assert len(lines) > 0, "Demo input has no data lines"
