#!/usr/bin/env python3
"""Find exact normalized character n-gram overlap between a manuscript and sources."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt"}


def read_path(path: Path):
    if path.is_file():
        return [(path, path.read_text(encoding="utf-8-sig"))]
    return [(item, item.read_text(encoding="utf-8-sig")) for item in sorted(path.rglob("*")) if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES and ".git" not in item.parts]


def normalize(text: str):
    return re.sub(r"[^\u3400-\u9fffA-Za-z0-9]", "", text).lower()


def ngrams(text: str, width: int):
    return {text[index:index + width] for index in range(max(0, len(text) - width + 1))}


def main():
    parser = argparse.ArgumentParser(description="比较稿件与已知来源的规范化字符片段重合，仅生成审计候选。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument("--ngram", type=int, default=16, help="字符片段长度，默认 16")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.ngram < 8:
        raise SystemExit("--ngram 不应小于 8，过短会产生大量无意义重合")

    manuscript_files = read_path(args.manuscript)
    source_files = [entry for path in args.sources for entry in read_path(path)]
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
        print("候选重合需要人工判断；零结果不代表绝对原创。")


if __name__ == "__main__":
    main()
