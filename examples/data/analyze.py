#!/usr/bin/env python3
"""Reproduce observed rates from synthetic cohort counts; no causal estimator."""
import argparse
import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


def analyze(path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    groups = {}
    for row in rows:
        variant, cohort = row["variant"], row["cohort"]
        key = variant, cohort
        if key in groups:
            raise ValueError("duplicate variant/cohort row")
        requests, errors = int(row["requests"]), int(row["errors"])
        if requests <= 0 or not 0 <= errors <= requests:
            raise ValueError("invalid request/error counts")
        groups[key] = {"requests":requests, "errors":errors, "rate_pct":float(Decimal(errors) / requests * 100)}
    variants = sorted({v for v, _ in groups})
    cohorts = sorted({c for _, c in groups})
    if variants != ["A", "B"] or any((v, c) not in groups for v in variants for c in cohorts):
        raise ValueError("paired A/B cohort rows required")
    totals = {}
    for variant in variants:
        requests = sum(groups[variant, c]["requests"] for c in cohorts)
        errors = sum(groups[variant, c]["errors"] for c in cohorts)
        totals[variant] = {"requests":requests, "errors":errors, "rate_pct":float(Decimal(errors) / requests * 100)}
    old, new = (Decimal(str(totals[v]["rate_pct"])) for v in ("A", "B"))
    return {"source_sha256":hashlib.sha256(path.read_bytes()).hexdigest(), "unit":"request error rate (%)", "totals":totals,
            "change_pp":float(new-old), "relative_change_pct":float((new-old)/old*100) if old else None,
            "cohorts":{c:{v:{**groups[v,c], "request_share_pct":groups[v,c]["requests"]/totals[v]["requests"]*100} for v in variants} for c in cohorts}}


def plot(result, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    groups = ["Overall", "Light", "Heavy"]
    a = [result["totals"]["A"]["rate_pct"], *[result["cohorts"][c]["A"]["rate_pct"] for c in ("light", "heavy")]]
    b = [result["totals"]["B"]["rate_pct"], *[result["cohorts"][c]["B"]["rate_pct"] for c in ("light", "heavy")]]
    with plt.rc_context({"svg.hashsalt":"explanation-design-cohorts-v1", "font.family":"DejaVu Sans", "font.size":12}):
        fig, ax = plt.subplots(figsize=(9.6,5.4), layout="constrained")
        for values, offset, label, color, hatch in [(a,-.18,"A","#4f5d75",""),(b,.18,"B","#176b62","//")]:
            bars=ax.bar([i+offset for i in range(3)],values,width=.36,label=label,color=color,hatch=hatch)
            ax.bar_label(bars, labels=[f"{v:g}%" for v in values], padding=5)
        ax.set(xticks=range(3),xticklabels=groups,ylim=(0,12),ylabel="Request error rate (%)",title="Within-cohort rates fall; overall rate rises")
        ax.spines[["top","right"]].set_visible(False)
        ax.legend(frameon=False)
        ax.text(.01,-.18,"Synthetic counts. Heavy-cohort share: A 10% → B 90%. Observational, not randomized.",transform=ax.transAxes,fontsize=10)
        fig.savefig(out/"rates.svg",metadata={"Date":None,"Title":"Observed error rates by variant and cohort","Description":"Overall A 1.9%, B 7.2%; light A 1%, B 0%; heavy A 10%, B 8%. Synthetic counts, no causal estimate."})
        svg_path = out/"rates.svg"
        svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())+"\n", encoding="utf-8")
        fig.savefig(out/"rates.png",dpi=150,metadata={"Software":"Matplotlib"})
        plt.close(fig)


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plot",action="store_true")
    args=parser.parse_args()
    base=Path(__file__).resolve().parent
    result=analyze(base/"input/cohorts.csv")
    out=base/"output"
    out.mkdir(exist_ok=True)
    (out/"results.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.plot:
        plot(result,out)
    print(json.dumps(result,ensure_ascii=False,indent=2))
