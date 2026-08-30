"""API entry point for skill registry and orchestrator integration."""

from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec

_mod_path = Path(__file__).parent / "hla_typing.py"
_spec = spec_from_file_location("hla_typing", _mod_path)
_mod = module_from_spec(_spec)
_spec.loader.exec_module(_mod)


def run(input_path: str, output_dir: str = "/tmp/hla-typing") -> dict:
    """Raises NotImplementedError — hla-typing has no HLA calling implementation."""
    data = _mod.validate_input(Path(input_path))
    result = _mod.run_analysis(data)
    _mod.write_report(result, Path(output_dir))
    return result
