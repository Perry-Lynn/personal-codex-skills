#!/usr/bin/env python3
"""Find exact normalized character n-gram overlap between a manuscript and sources."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt"}
SKIP_DIRS = {".git", "node_modules"}


class InputError(ValueError):
    """Raised when the requested comparison scope cannot be checked."""


def read_path(path: Path):
    if not path.exists():
        raise InputError(f"路径不存在: {path}")
    if path.is_file():
        if path.suffix.lower() not in TEXT_SUFFIXES:
            raise InputError(f"不支持的文件扩展名: {path}")
        candidates = [path.resolve()]
    elif path.is_dir():
        candidates = [
            item.resolve()
            for item in sorted(path.rglob("*"))
            if item.is_file()
            and item.suffix.lower() in TEXT_SUFFIXES
            and not any(part in SKIP_DIRS or part.startswith(".") for part in item.relative_to(path).parts[:-1])
        ]
        if not candidates:
            raise InputError(f"路径中没有可比较的 .md/.txt 文件: {path}")
    else:
        raise InputError(f"不是文件或目录: {path}")

    entries = []
    for candidate in candidates:
        try:
            text = candidate.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as exc:
            raise InputError(f"无法读取 {candidate}: {exc}") from exc
        if not text.strip():
            raise InputError(f"输入为空白: {candidate}")
        entries.append((candidate, text))
    return entries


def normalize(text: str):
    return re.sub(r"[^\u3400-\u9fffA-Za-z0-9]", "", text).lower()


def ngrams(text: str, width: int):
    return {text[index:index + width] for index in range(len(text) - width + 1)}


def main():
    parser = argparse.ArgumentParser(description="比较稿件与已知来源的规范化字符片段重合，仅生成审计候选。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--ngram", type=int, default=16, help="字符片段长度，默认 16")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.ngram < 8:
        print("ERROR: --ngram 不应小于 8，过短会产生大量无意义重合", file=sys.stderr)
        return 2
    if args.limit <= 0:
        print("ERROR: --limit 必须为正数", file=sys.stderr)
        return 2

    try:
        manuscript_files = read_path(args.manuscript)
        source_files = [entry for path in args.sources for entry in read_path(path)]
        for path, text in [*manuscript_files, *source_files]:
            if len(normalize(text)) < args.ngram:
                raise InputError(f"规范化文本短于 --ngram={args.ngram}: {path}")
    except (InputError, OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    findings = []
    for manuscript_path, manuscript_text in manuscript_files:
        manuscript_norm = normalize(manuscript_text)
        manuscript_grams = ngrams(manuscript_norm, args.ngram)
        for source_path, source_text in source_files:
            source_norm = normalize(source_text)
            shared = sorted(manuscript_grams & ngrams(source_norm, args.ngram))
            if shared:
                findings.append({
                    "manuscript": str(manuscript_path),
                    "source": str(source_path),
                    "ngram": args.ngram,
                    "shared_count": len(shared),
                    "examples": shared[:args.limit],
                })
    result = {
        "scope": "exact normalized character n-grams against provided sources only",
        "manuscript_files": len(manuscript_files),
        "source_files": len(source_files),
        "comparisons_with_matches": len(findings),
        "findings": findings,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Compared {len(manuscript_files)} manuscript file(s) with {len(source_files)} source file(s).")
        for finding in findings:
            print(f"{finding['manuscript']} <> {finding['source']}: {finding['shared_count']} shared candidate(s)")
            for example in finding["examples"]:
                print(f"  {example}")
        print("候选重合需要人工判断；比较完成但零候选不代表绝对原创。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
