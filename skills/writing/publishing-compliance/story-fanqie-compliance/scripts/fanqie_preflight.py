#!/usr/bin/env python3
"""Deterministic preflight checks for Fanqie-bound fiction text.

This scanner only reports mechanical signals. It does not determine legal or
platform compliance and intentionally avoids broad sensitive-word blocking.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt"}
ENGINEERING_RE = re.compile(
    r"(?:第[一二三四五六七八九十百千万两0-9]+章|上一章|上章|前一章|本章|这一章|"
    r"前文|后文|细纲|读者|爽点|伏笔|任务卡|章节定位)"
)
CONTACT_RE = re.compile(
    r"(?:加(?:微信|V|v|QQ)|微信号|QQ(?:群|号)|私信我|扫码(?:进群|购买|联系)|"
    r"购买链接|返利群|投资群|联系(?:客服|作者)购买)"
)
BYPASS_RE = re.compile(
    r"(?:绕过审核|规避审核|躲过审核|卡审核|利用平台漏洞|平台漏洞教程|封号规避|养号教程)"
)
TITLE_RE = re.compile(r"^\s*#{1,6}\s+第[一二三四五六七八九十百千万两0-9]+章")
SPACE_RE = re.compile(r"\s+")
WORDISH_RE = re.compile(r"[\u4e00-\u9fffA-Za-z0-9]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan fiction files for deterministic Fanqie preflight signals."
    )
    parser.add_argument("paths", nargs="+", help="Markdown/text files or directories")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def collect_files(raw_paths: list[str]) -> list[Path]:
    files: set[Path] = set()
    for raw in raw_paths:
        path = Path(raw).expanduser()
        if not path.exists():
            raise FileNotFoundError(raw)
        if path.is_file():
            if path.suffix.lower() in TEXT_SUFFIXES:
                files.add(path.resolve())
            continue
        for candidate in path.rglob("*"):
            if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES:
                files.add(candidate.resolve())
    return sorted(files)


def normalized_paragraph(text: str) -> str:
    return SPACE_RE.sub("", text).strip()


def scan_file(path: Path) -> tuple[list[dict], dict]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    findings: list[dict] = []
    paragraphs: dict[str, list[int]] = defaultdict(list)
    current: list[str] = []
    start_line = 1

    def add(kind: str, severity: str, line: int, message: str, excerpt: str) -> None:
        findings.append(
            {
                "file": str(path),
                "line": line,
                "kind": kind,
                "severity": severity,
                "message": message,
                "excerpt": excerpt[:120],
            }
        )

    def flush_paragraph() -> None:
        nonlocal current, start_line
        if not current:
            return
        paragraph = normalized_paragraph("\n".join(current))
        if len(paragraph) >= 24:
            paragraphs[paragraph].append(start_line)
        current = []

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped:
            flush_paragraph()
            start_line = number + 1
            continue
        if not current:
            start_line = number
        current.append(line)

        is_title = number <= 3 and TITLE_RE.search(line)
        if not is_title and ENGINEERING_RE.search(line):
            add(
                "engineering-metadata",
                "BLOCK",
                number,
                "正文疑似泄漏写作工程词；故事内真实讨论章节文本时人工豁免。",
                stripped,
            )
        if CONTACT_RE.search(line):
            add(
                "contact-or-transaction",
                "REVIEW",
                number,
                "疑似现实联系方式或交易引流；故事内情节需人工判断。",
                stripped,
            )
        if BYPASS_RE.search(line):
            add(
                "platform-bypass",
                "REVIEW",
                number,
                "疑似平台漏洞、绕审或违规经验表达。",
                stripped,
            )
        visible = [char for char in stripped if not char.isspace()]
        if len(visible) >= 16:
            wordish = sum(1 for char in visible if WORDISH_RE.match(char))
            if wordish / len(visible) < 0.25:
                add(
                    "symbol-heavy-line",
                    "BLOCK",
                    number,
                    "该行以符号、表情或非文字内容为主，疑似无意义填充。",
                    stripped,
                )
    flush_paragraph()

    for paragraph, locations in paragraphs.items():
        if len(locations) < 2:
            continue
        add(
            "duplicate-paragraph",
            "BLOCK",
            locations[1],
            f"发现重复段落，共出现 {len(locations)} 次，行号 {locations}。",
            paragraph,
        )

    stats = {
        "file": str(path),
        "characters": len(normalized_paragraph(text)),
        "lines": len(lines),
        "findings": len(findings),
    }
    return findings, stats


def main() -> int:
    args = parse_args()
    try:
        files = collect_files(args.paths)
    except (OSError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not files:
        print("ERROR: no .md or .txt files found", file=sys.stderr)
        return 2

    findings: list[dict] = []
    stats: list[dict] = []
    for path in files:
        try:
            file_findings, file_stats = scan_file(path)
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: {path}: {exc}", file=sys.stderr)
            return 2
        findings.extend(file_findings)
        stats.append(file_stats)

    blockers = [item for item in findings if item["severity"] == "BLOCK"]
    advisories = [item for item in findings if item["severity"] != "BLOCK"]
    result = {
        "summary": {
            "files": len(files),
            "blockers": len(blockers),
            "advisories": len(advisories),
            "manual_semantic_review_required": True,
        },
        "findings": findings,
        "stats": stats,
    }

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(
            f"Scanned {len(files)} file(s): "
            f"{len(blockers)} blocker(s), {len(advisories)} advisory item(s)."
        )
        for item in findings:
            print(
                f"[{item['severity']}] {item['file']}:{item['line']} "
                f"{item['kind']} - {item['message']}"
            )
            print(f"  {item['excerpt']}")
        print("Manual semantic review is still required.")

    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
