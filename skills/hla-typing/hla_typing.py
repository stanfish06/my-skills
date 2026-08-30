#!/usr/bin/env python3
"""Hla Typing - HLA allele typing from WGS/WES VCF data."""

import argparse
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
DISCLAIMER = ("ClawBio is a research and educational tool. It is not a medical device and does not provide clinical diagnoses. Consult a healthcare professional before making any medical decisions.")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, dest="input_file", help="Input file path")
    parser.add_argument("--output", type=Path, help="Output directory")
    parser.add_argument("--demo", action="store_true", help="Run with synthetic demo data")
    return parser.parse_args()


def validate_input(input_path: Path) -> dict:
    """Validate and parse the input file. Returns parsed data dict."""
    if not input_path.exists():
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    lines = []
    with open(input_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return {"lines": lines, "source": str(input_path)}


NOT_IMPLEMENTED_MSG = (
    "hla-typing has no HLA calling implementation. Zero findings would be "
    "indistinguishable from a true negative, and a negative HLA-B*57:01 or "
    "HLA-B*15:02 call gates a drug decision, so this fails instead of "
    "returning an empty success. Allele calls cannot be derived from a chr6 "
    "position list against a linear reference: wiring this up needs a real "
    "caller (OptiType, HLA*LA, arcasHLA, T1K) for sequence data, or a "
    "validated tag-SNP imputation panel for array data. Use pharmgx-reporter "
    "for the pharmacogenomic calls that are implemented."
)


def run_analysis(data: dict) -> dict:
    """Not implemented. Raises NotImplementedError."""
    raise NotImplementedError(NOT_IMPLEMENTED_MSG)


def write_report(result: dict, output_dir: Path) -> None:
    """Write report.md and result.json to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # result.json
    with open(output_dir / "result.json", "w") as f:
        json.dump(result, f, indent=2)

    # report.md
    n = result.get("variants_processed", 0)
    findings = result.get("findings", [])
    report = [
        "# Hla Typing Report",
        "",
        f"**Input**: {result.get('source', 'unknown')}",
        f"**Variants processed**: {n}",
        f"**Findings**: {len(findings)}",
        "",
        "## Results",
        "",
        "| Locus | Finding | Confidence |",
        "|-------|---------|------------|",
    ]
    for f_ in findings:
        report.append(f"| {f_.get('locus', '-')} | {f_.get('finding', '-')} | {f_.get('confidence', '-')} |")
    if not findings:
        report.append("| - | No findings (skeleton implementation) | - |")
    report.extend([
        "",
        "## Summary",
        "",
        f"Analysis completed on {n} variants. {len(findings)} findings reported.",
        "",
        f"*{DISCLAIMER}*",
        "",
    ])
    with open(output_dir / "report.md", "w") as f:
        f.write("\n".join(report))

    print(f"Report written to {output_dir / 'report.md'}")
    print(f"Results written to {output_dir / 'result.json'}")


def run_demo(output_dir: Path) -> None:
    """Run with built-in synthetic demo data."""
    demo_input = SKILL_DIR / "demo_input.txt"
    if not demo_input.exists():
        print("Error: demo data not found", file=sys.stderr)
        sys.exit(1)
    data = validate_input(demo_input)
    result = run_analysis(data)
    write_report(result, output_dir)


def main():
    args = parse_args()
    try:
        _dispatch(args)
    except NotImplementedError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)


def _dispatch(args) -> None:
    if args.demo:
        output = args.output or Path("/tmp") / "hla_typing" / "demo"
        run_demo(output)
    elif args.input_file:
        data = validate_input(args.input_file)
        result = run_analysis(data)
        output = args.output or args.input_file.parent / "output"
        write_report(result, output)
    else:
        print("Error: provide --input <file> or --demo", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
