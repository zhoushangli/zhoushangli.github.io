"""Check slot diversity and summarise both gate evidence and review scorecards.

e.g. python scripts/preview-audit/report.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DEFAULT_OUT = Path(
    r"C:\Users\Shangli Zhou\.codex\visualizations\2026\09\28\01a0e9ca-2d3d-73f2-a597-9a367465fd22\blog-designs"
)
AXIS_KEYS = ("imagery", "layout", "typography", "accent", "mechanism", "rhythm")
SCORE_KEYS = ("reading", "structure", "creativity", "darkSystem", "mobile")
MIN_AXIS_DISTANCE = 3
MIN_TOTAL = 80
MIN_READING = 20
MIN_MOBILE = 12

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_slots(design_dir: Path) -> dict[str, dict[str, str]]:
    slots: dict[str, dict[str, str]] = {}
    for path in sorted(design_dir.glob("design-*.ts")):
        text = path.read_text(encoding="utf-8")
        block_match = re.search(r"axes:\s*\{(.*?)\}", text, re.S)
        seed_match = re.search(r"seed:\s*'([^']*)'", text)
        name_match = re.search(r"name:\s*'([^']*)'", text)
        device_match = re.search(r"device:\s*'([^']*)'", text)
        axes: dict[str, str] = {}
        if block_match:
            for key in AXIS_KEYS:
                found = re.search(rf"{key}:\s*'([^']*)'", block_match.group(1))
                axes[key] = found.group(1) if found else "?"
        slots[path.stem] = {
            "seed": seed_match.group(1) if seed_match else "?",
            "name": name_match.group(1) if name_match else "?",
            "device": device_match.group(1) if device_match else "?",
            **axes,
        }
    return slots


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarise preview audit results.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    slots = parse_slots(REPO / "src" / "data" / "designs")
    audit_dir = REPO / "src" / "data" / "preview-audit"

    print(f"slots={len(slots)}")
    distances: list[tuple[str, str, int]] = []
    for left, right in combinations(sorted(slots), 2):
        distance = sum(1 for key in AXIS_KEYS if slots[left][key] != slots[right][key])
        distances.append((left, right, distance))
        flag = "ok  " if distance >= MIN_AXIS_DISTANCE else "FAIL"
        print(f"  {flag} {left} vs {right} -> {distance} axes differ")
    worst = min((d for _, _, d in distances), default=0)
    diversity_ok = bool(distances) and worst >= MIN_AXIS_DISTANCE
    print(f"diversity={'PASS' if diversity_ok else 'FAIL'} worst={worst}")

    rows = []
    for design in sorted(slots):
        gates = load_json(audit_dir / f"{design}.gates.json")
        score = load_json(audit_dir / f"{design}.score.json")
        gate_map = gates.get("gates", {})
        failed_gates = [key for key, value in gate_map.items() if not value]
        scores = score.get("scores", {})
        total = sum(scores.get(key, 0) for key in SCORE_KEYS) if scores else None
        verdict = score.get("verdict")
        rows.append(
            {
                "design": design,
                "label": slots[design].get("name"),
                "seed": slots[design].get("seed"),
                "round": gates.get("round"),
                "gatesPass": bool(gate_map) and not failed_gates,
                "failedGates": failed_gates,
                "rounds": gates.get("round"),
                "scores": scores,
                "total": total,
                "reading": scores.get("reading"),
                "mobile": scores.get("mobile"),
                "verdict": verdict,
                "defects": score.get("defects", []),
                "passed": verdict == "pass"
                and (total or 0) >= MIN_TOTAL
                and (scores.get("reading") or 0) >= MIN_READING
                and (scores.get("mobile") or 0) >= MIN_MOBILE
                and not failed_gates,
            }
        )
        summary = "not scored"
        if scores:
            summary = f"total={total} reading={scores.get('reading')} mobile={scores.get('mobile')} verdict={verdict}"
        print(f"  {design} [{rows[-1]['label']}] gates={'PASS' if rows[-1]['gatesPass'] else 'FAIL'} {summary}")
        if failed_gates:
            print(f"      failed gates: {failed_gates}")

    qualified = [row for row in rows if row["passed"]]
    print(f"qualified={len(qualified)}/6")

    lines = ["# Preview audit summary", "", f"- diversity: {'PASS' if diversity_ok else 'FAIL'} (worst pair {worst} axes)", f"- qualified: {len(qualified)} of {len(rows)}", ""]
    lines.append("| slot | name | seed | total | reading | mobile | gates | verdict | open defects |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        lines.append(
            "| {design} | {label} | `{seed}` | {total} | {reading} | {mobile} | {gates} | {verdict} | {defects} |".format(
                design=row["design"],
                label=row["label"],
                seed=row["seed"],
                total=row["total"] if row["total"] is not None else "-",
                reading=row["reading"] if row["reading"] is not None else "-",
                mobile=row["mobile"] if row["mobile"] is not None else "-",
                gates="PASS" if row["gatesPass"] else "FAIL " + ",".join(row["failedGates"]),
                verdict=row["verdict"] or "-",
                defects=len(row["defects"]),
            )
        )
    lines.append("")
    for row in rows:
        lines.append(f"## {row['design']} · {row['label']}")
        lines.append("")
        lines.append(f"- seed `{row['seed']}` · round {row['round']} · verdict {row['verdict'] or 'pending'}")
        if row["defects"]:
            for defect in row["defects"]:
                lines.append(f"- defect: {defect}")
        lines.append("")
    target = args.out / "summary.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines), encoding="utf-8")
    print(f"summary -> {target}")
    return 0 if diversity_ok and len(qualified) == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
