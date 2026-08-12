#!/usr/bin/env python3
"""Transparent descriptive metrics for chapter-level serial-fiction CSV data."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


def number(value: str):
    value = value.strip().replace(",", "").replace("%", "")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def main():
    parser = argparse.ArgumentParser(description="计算连载小说章节 CSV 的描述性变化和可选比率。")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--chapter-col", default="chapter")
    parser.add_argument("--value", action="append", default=[], help="要分析的数值列，可重复")
    parser.add_argument("--ratio", action="append", default=[], metavar="NAME=NUM/DEN", help="定义比率，可重复")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    with args.csv_file.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("CSV 没有数据行")
    if args.chapter_col not in rows[0]:
        raise SystemExit(f"缺少章节列: {args.chapter_col}")

    ratio_specs = []
    for spec in args.ratio:
        try:
            name, expression = spec.split("=", 1)
            numerator, denominator = expression.split("/", 1)
        except ValueError as exc:
            raise SystemExit(f"无效比率定义: {spec}") from exc
        ratio_specs.append((name, numerator, denominator))

    fields = args.value or [key for key in rows[0] if key != args.chapter_col and any(number(row.get(key, "")) is not None for row in rows)]
    output_rows = []
    previous = {}
    for row in rows:
        item = {"chapter": row.get(args.chapter_col, "")}
        for field in fields:
            value = number(row.get(field, ""))
            item[field] = value
            prior = previous.get(field)
            item[f"{field}_change"] = None if value is None or prior in (None, 0) else (value - prior) / prior
            if value is not None:
                previous[field] = value
        for name, numerator, denominator in ratio_specs:
            num = number(row.get(numerator, ""))
            den = number(row.get(denominator, ""))
            item[name] = None if num is None or den in (None, 0) else num / den
        output_rows.append(item)

    summaries = {}
    for field in fields:
        values = [row[field] for row in output_rows if row[field] is not None and math.isfinite(row[field])]
        summaries[field] = {
            "count": len(values),
            "min": min(values) if values else None,
            "max": max(values) if values else None,
            "mean": sum(values) / len(values) if values else None,
        }
    result = {"source": str(args.csv_file), "row_count": len(rows), "summaries": summaries, "rows": output_rows}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Rows: {len(rows)}")
        print(json.dumps(summaries, ensure_ascii=False, indent=2))
        for item in output_rows:
            print(json.dumps(item, ensure_ascii=False))


if __name__ == "__main__":
    main()
