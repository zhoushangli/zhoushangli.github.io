"""Validate independent scorecards and publish the local comparison report."""
from __future__ import annotations

import argparse
import json
import re
import sys
from itertools import combinations
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "src" / "data" / "preview-audit"
SCORES = {"aesthetics":25,"reading":25,"structure":20,"diversity":15,"mobile":15}
MINIMUMS = {"aesthetics":20,"reading":20,"diversity":12,"mobile":12}
AXES = {"imagery","layout","typography","accent","mechanism","rhythm"}
GATES = {"routesLoaded","noErrors","localAssets","noBrokenImages","linksValid","noHorizontalOverflow","darkSurface","bodyContrast","smallTextContrast","readingMetrics","mobileGutters","touchTargets","focusVisible","interactions","growthStress","wideContent","noindex","reducedMotion","categoryRedirect"}
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=REPO / "artifacts" / "preview-audit")
    args = parser.parse_args()
    public = REPO / "public" / "previews-audit"
    public.mkdir(parents=True, exist_ok=True)
    comparison = load(AUDIT / "comparison.json")
    slots = {}
    errors = []
    for letter in "abcdef":
        design = "design-" + letter
        source = (REPO / "src" / "data" / "designs" / (design + ".ts")).read_text(encoding="utf-8")
        record = json.loads(re.search(r"const design: DesignRecord = (.*?);", source, re.S).group(1))
        gates = load(AUDIT / (design + ".gates.json"))
        score = load(AUDIT / (design + ".score.json"))
        scores = score.get("scores", {})
        valid = set(scores) == set(SCORES) and all(type(scores[k]) is int and 0 <= scores[k] <= SCORES[k] for k in SCORES)
        total = sum(scores.values()) if valid else 0
        gate_pass = set(gates.get("gates", {})) == GATES and all(v is True for v in gates["gates"].values())
        current = bool(score) and score.get("round") == gates.get("round")
        pairs = [pair for pair in comparison.get("pairs",[]) if design in (pair.get("left"),pair.get("right"))]
        cross = len(pairs) == 5 and all(
            pair.get("layoutDifferent") is True and pair.get("interactionDifferent") is True
            and set(pair.get("differentAxes",[])).issubset(AXES)
            and len(set(pair.get("differentAxes",[]))) >= 4
            and {"layout","mechanism"}.issubset(pair.get("differentAxes",[]))
            and bool(pair.get("evidence"))
            and pair.get("rounds",{}).get(design) == gates.get("round")
            for pair in pairs
        )
        passed = valid and total >= 80 and all(scores[k] >= v for k,v in MINIMUMS.items()) and gate_pass and current and cross and score.get("verdict") == "pass"
        if not passed:
            errors.append(design + ": " + ", ".join(reason for reason,ok in {
                "score format":valid,"score >=80":total >= 80,"minimums":valid and all(scores.get(k,0) >= v for k,v in MINIMUMS.items()),
                "technical gates":gate_pass,"current independent review":current,"pairwise differences":cross,"review verdict":score.get("verdict") == "pass"
            }.items() if not ok))
        slots[design] = {"name":record["name"],"round":gates.get("round"),"total":total if valid else None,"scores":scores,"passed":passed,"gatesPass":gate_pass,"crossPass":cross,"score":score}
        bundle = {"design":design,"name":record["name"],"passed":passed,"gates":gates,"review":score,"comparisonPairs":pairs}
        (public / (design + "-review.json")).write_text(json.dumps(bundle,ensure_ascii=False,indent=2),encoding="utf-8")
    expected = {tuple(pair) for pair in combinations(slots,2)}
    actual = [tuple(sorted((pair.get("left",""),pair.get("right","")))) for pair in comparison.get("pairs",[])]
    if len(actual) != 15 or set(actual) != expected:
        errors.append("Comparison must contain all 15 unique pairs.")
    if comparison.get("verdict") != "pass":
        errors.append("Independent pairwise verdict is not pass.")
    qualified = sum(slot["passed"] for slot in slots.values())
    lines = ["# 六套暗色古典博客 · 独立评审汇总","",f"合格：{qualified}/6。证据包括三个视图、1440/1024/390px，以及每案实际交互。","",
      "| 方案 | 轮次 | 美术 /25 | 阅读 /25 | 结构 /20 | 差异 /15 | 移动交互 /15 | 总分 | 技术 | 横向差异 | 结论 |",
      "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for design,slot in slots.items():
        values = [slot["scores"].get(k,"—") for k in SCORES]
        lines.append("| " + " | ".join(map(str,[design + " " + slot["name"],slot["round"],*values,slot["total"] or "—","通过" if slot["gatesPass"] else "待修复","通过" if slot["crossPass"] else "待评审","合格" if slot["passed"] else "未合格"])) + " |")
    for design,slot in slots.items():
        lines.extend(["","## " + design + " · " + slot["name"],"",slot["score"].get("summary","待独立评审"),""])
        lines.extend("- " + item for item in slot["score"].get("defects",[]))
        lines.extend(["","评审依据："])
        lines.extend("- " + item for item in slot["score"].get("evidence",[]))
    if comparison:
        lines.extend(["","## 六案横向比较","",comparison.get("summary","")])
        for pair in comparison.get("pairs",[]):
            lines.append("- " + pair["left"] + " / " + pair["right"] + "：" + "; ".join(pair.get("evidence",[])))
    if errors:
        lines.extend(["","## 未完成项目","",*("- " + error for error in errors)])
    text = "\n".join(lines) + "\n"
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out / "summary.md").write_text(text,encoding="utf-8")
    (public / "summary.md").write_text(text,encoding="utf-8")
    if comparison:
        (public / "comparison.json").write_text(json.dumps(comparison,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"qualified={qualified}/6; uniquePairs={len(set(actual))}/15")
    for design,slot in slots.items():
        print(design + " " + str(slot["total"]) + " " + ("PASS" if slot["passed"] else "FAIL"))
    for error in errors:
        print(error)
    return 0 if not errors and qualified == 6 else 1

if __name__ == "__main__":
    raise SystemExit(main())
