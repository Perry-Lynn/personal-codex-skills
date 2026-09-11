#!/usr/bin/env python3
"""Transparent descriptive metrics for chapter-level serial-fiction CSV data."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path


class InputError(ValueError):
    """Raised when the CSV or metric specification cannot be analyzed."""


def number(value: str | None) -> tuple[float | None, str | None]:
    """Parse a finite number and return a diagnostic for non-empty bad input."""
    if value is None or not value.strip():
        return None, "missing value"
    token = value.strip().replace(",", "")
    is_percent = token.endswith("%")
    if is_percent:
        token = token[:-1].strip()
    if not token or "%" in token:
        return None, f"invalid numeric value: {value!r}"
    try:
        parsed = float(token)
    except ValueError:
        return None, f"invalid numeric value: {value!r}"
    if not math.isfinite(parsed):
        return None, f"non-finite numeric value: {value!r}"
    return (parsed / 100 if is_percent else parsed), None


OUTPUT_RESERVED_FIELDS = {"chapter", "diagnostics", "source", "row_count", "summaries", "rows"}


def validate_input_headers(headers: list[str], chapter_col: str) -> None:
    conflicts = [
        header
        for header in headers
        if header != chapter_col and (header in OUTPUT_RESERVED_FIELDS or header.endswith("_change"))
    ]
    if conflicts:
        raise InputError(f"CSV 输入字段使用输出保留名或派生字段名: {', '.join(conflicts)}")


def parse_ratio_specs(
    specs: list[str], headers: list[str], explicit_values: list[str], chapter_col: str
) -> list[tuple[str, str, str]]:
    parsed: list[tuple[str, str, str]] = []
    names: set[str] = set()
    reserved = OUTPUT_RESERVED_FIELDS | {chapter_col, *explicit_values}
    for spec in specs:
        if spec.count("=") != 1:
            raise InputError(f"无效比率定义: {spec}")
        name, expression = (part.strip() for part in spec.split("=", 1))
        if expression.count("/") != 1:
            raise InputError(f"无效比率定义: {spec}")
        numerator, denominator = (part.strip() for part in expression.split("/", 1))
        if not name or not numerator or not denominator:
            raise InputError(f"无效比率定义: {spec}")
        if name in names or name in headers or name in reserved or name.endswith("_change"):
            raise InputError(f"比率名称重名或覆盖保留字段: {name}")
        if numerator not in headers or denominator not in headers:
            missing = numerator if numerator not in headers else denominator
            raise InputError(f"比率引用未知列: {missing}")
        names.add(name)
        parsed.append((name, numerator, denominator))
    return parsed


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str | None]]]:
    if not path.exists():
        raise InputError(f"CSV 不存在: {path}")
    if not path.is_file():
        raise InputError(f"CSV 不是文件: {path}")
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = reader.fieldnames or []
            rows = list(reader)
    except (OSError, UnicodeError, csv.Error) as exc:
        raise InputError(f"无法读取 CSV {path}: {exc}") from exc
    if not headers or any(not header or not header.strip() for header in headers):
        raise InputError("CSV 缺少有效表头")
    if len(set(headers)) != len(headers):
        raise InputError("CSV 表头存在重名列")
    if not rows:
        raise InputError("CSV 没有数据行")
    return headers, rows


def add_diagnostic(item: dict, field: str, diagnostic: str) -> None:
    item.setdefault("diagnostics", []).append(f"{field}: {diagnostic}")


def main() -> int:
    parser = argparse.ArgumentParser(description="计算连载小说章节 CSV 的描述性变化和可选比率。")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--chapter-col", default="chapter")
    parser.add_argument("--value", action="append", default=[], help="要分析的数值列，可重复")
    parser.add_argument("--ratio", action="append", default=[], metavar="NAME=NUM/DEN", help="定义比率，可重复")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        headers, rows = read_csv(args.csv_file)
        if args.chapter_col not in headers:
            raise InputError(f"缺少章节列: {args.chapter_col}")
        validate_input_headers(headers, args.chapter_col)

        if len(set(args.value)) != len(args.value):
            raise InputError("--value 存在重名列")
        if any(field not in headers or field == args.chapter_col for field in args.value):
            unknown = next(field for field in args.value if field not in headers or field == args.chapter_col)
            raise InputError(f"--value 引用未知或非法列: {unknown}")
        ratio_specs = parse_ratio_specs(args.ratio, headers, args.value, args.chapter_col)

        if args.value:
            fields = list(args.value)
        else:
            fields = []
            for key in headers:
                if key == args.chapter_col:
                    continue
                if any(number(row.get(key))[0] is not None for row in rows):
                    fields.append(key)
        if not fields and not ratio_specs:
            raise InputError("CSV 没有可分析的数值列或比率")

        output_rows = []
        previous: dict[str, float | None] = {}
        ratio_names = [name for name, _, _ in ratio_specs]
        for row_number, row in enumerate(rows, start=2):
            item: dict[str, object] = {"chapter": row.get(args.chapter_col, "") or ""}
            if not item["chapter"].strip():
                add_diagnostic(item, args.chapter_col, f"row {row_number}: missing chapter")

            for field in fields:
                value, diagnostic = number(row.get(field))
                item[field] = value
                prior = previous.get(field)
                change = None if value is None or prior in (None, 0) else (value - prior) / prior
                item[f"{field}_change"] = change if change is None or math.isfinite(change) else None
                if diagnostic:
                    add_diagnostic(item, field, diagnostic)
                if change is not None and not math.isfinite(change):
                    add_diagnostic(item, f"{field}_change", "non-finite derived value")
                # A missing or invalid row breaks adjacency; never compare across it.
                previous[field] = value

            for name, numerator, denominator in ratio_specs:
                num, num_diagnostic = number(row.get(numerator))
                den, den_diagnostic = number(row.get(denominator))
                ratio = None if num is None or den in (None, 0) else num / den
                item[name] = ratio if ratio is None or math.isfinite(ratio) else None
                if num_diagnostic:
                    add_diagnostic(item, numerator, num_diagnostic)
                if den_diagnostic:
                    add_diagnostic(item, denominator, den_diagnostic)
                if den == 0:
                    add_diagnostic(item, name, "zero denominator")
                if ratio is not None and not math.isfinite(ratio):
                    add_diagnostic(item, name, "non-finite derived value")

            if "diagnostics" not in item:
                item["diagnostics"] = []
            output_rows.append(item)

        summaries: dict[str, dict[str, float | int | None]] = {}
        for field in [*fields, *ratio_names]:
            values = [
                row[field]
                for row in output_rows
                if isinstance(row.get(field), (int, float)) and math.isfinite(row[field])
            ]
            summaries[field] = {
                "count": len(values),
                "min": min(values) if values else None,
                "max": max(values) if values else None,
                # Scale before summing so two finite 1e308 values do not
                # overflow merely because the arithmetic is computing a mean.
                "mean": math.fsum(value / len(values) for value in values) if values else None,
            }
        result = {"source": str(args.csv_file), "row_count": len(rows), "summaries": summaries, "rows": output_rows}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
        else:
            print(f"Rows: {len(rows)}")
            print(json.dumps(summaries, ensure_ascii=False, indent=2, allow_nan=False))
            for item in output_rows:
                print(json.dumps(item, ensure_ascii=False, allow_nan=False))
        return 0
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
