#!/usr/bin/env python3
"""Conservative static preflight for Chinese fiction proofreading."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TEXT_SUFFIXES = {".md", ".txt"}
SKIP_DIRS = {".git", "归档", "大纲", "设定", "追踪", "拆文库", "reports", "node_modules"}
PAIRS = {"（": "）", "[": "]", "【": "】", "《": "》", "〈": "〉"}
REVERSE = {value: key for key, value in PAIRS.items()}


def iter_files(paths: list[Path]):
    for path in paths:
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path
        elif path.is_dir():
            for item in sorted(path.rglob("*")):
                if any(part in SKIP_DIRS for part in item.parts):
                    continue
                if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES:
                    yield item


def add(findings, path, line, column, code, message, excerpt):
    findings.append({
        "file": str(path), "line": line, "column": column,
        "code": code, "message": message, "excerpt": excerpt.strip()[:160],
    })


def check_file(path: Path):
    findings = []
    text = path.read_text(encoding="utf-8-sig")
    stack: list[tuple[str, int, int]] = []
    in_fence = False

    for line_no, raw in enumerate(text.splitlines(), 1):
        if raw.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        line = raw.rstrip("\n")
        for col, char in enumerate(line, 1):
            if char in PAIRS:
                stack.append((char, line_no, col))
            elif char in REVERSE:
                expected = REVERSE[char]
                if stack and stack[-1][0] == expected:
                    stack.pop()
                else:
                    add(findings, path, line_no, col, "UNMATCHED_CLOSE", f"未找到与 {char} 配对的 {expected}", line)

        for match in re.finditer(r"[ \t]+[，。！？；：、]", line):
            add(findings, path, line_no, match.start() + 1, "SPACE_BEFORE_PUNCT", "中文标点前有多余空白", line)
        for match in re.finditer(r"[。！？；：、]{3,}", line):
            add(findings, path, line_no, match.start() + 1, "PUNCT_RUN", "连续中文标点较多，请确认是否有意", line)
        for match in re.finditer(r"(?<!\.)\.\.\.(?!\.)", line):
            add(findings, path, line_no, match.start() + 1, "ASCII_ELLIPSIS", "中文正文出现三个英文句点，可确认是否应为省略号", line)
        for match in re.finditer(r"([\u4e00-\u9fff])\1{2,}", line):
            add(findings, path, line_no, match.start() + 1, "REPEATED_HAN", "汉字连续重复三次以上，请确认是否为口吃或拟声", line)
        if "\u3000" in line:
            add(findings, path, line_no, line.index("\u3000") + 1, "IDEOGRAPHIC_SPACE", "正文含全角空格", line)

    for opener, line_no, col in stack:
        add(findings, path, line_no, col, "UNCLOSED_PAIR", f"{opener} 缺少配对的 {PAIRS[opener]}", "")
    return findings


def main():
    parser = argparse.ArgumentParser(description="保守检查中文小说中的配对符号、异常空白和可疑重复。")
    parser.add_argument("paths", nargs="+", type=Path, help="待检查的 .md/.txt 文件或目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    files = list(dict.fromkeys(iter_files(args.paths)))
    findings = [item for path in files for item in check_file(path)]
    if args.json:
        print(json.dumps({"files_checked": len(files), "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print(f"Checked {len(files)} file(s); found {len(findings)} candidate(s).")
        for item in findings:
            print(f"{item['file']}:{item['line']}:{item['column']} [{item['code']}] {item['message']}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
