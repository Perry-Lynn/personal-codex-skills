#!/usr/bin/env python3
"""Measure prose-style fingerprints and compare targets with stable samples.

Metrics are descriptive signals, not quality scores. The script scans canonical
prose only and intentionally excludes outlines, settings, trackers and archives.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt"}
SKIP_DIRS = {
    ".git",
    ".story-pipeline",
    "node_modules",
    "归档",
    "追踪",
    "设定",
    "大纲",
    "参考资料",
    "对标",
    "拆文库",
}
SENTENCE_RE = re.compile(r"[^。！？!?\n]+[。！？!?]?", re.MULTILINE)
DIALOGUE_RE = re.compile(r"[“\"]([^”\"\n]+)[”\"]")
SPACE_RE = re.compile(r"\s+")
MARKDOWN_PREFIX_RE = re.compile(r"^\s*(?:#{1,6}\s|>\s|[-*+]\s|\|)")
RISK_PATTERNS = {
    "not-a-but-b": re.compile(r"不是[^。！？\n]{1,40}(?:而是|只是)"),
    "quiet-voice-contrast": re.compile(r"声音不(?:大|高)[^。！？\n]{0,20}(?:却|但)"),
    "gaze-template": re.compile(r"(?:目光|视线)(?:落在|停在|移向)"),
    "smile-template": re.compile(r"嘴角(?:勾起|扬起)"),
    "author-summary": re.compile(r"(?:这意味着|他终于明白|真正重要的是|这一刻他才明白)"),
    "forecast-ending": re.compile(r"(?:没人知道|才刚刚开始|命运的齿轮|拉开序幕)"),
    "soft-adverbs": re.compile(r"(?:微微|淡淡|似乎|仿佛)"),
    "engineering-metadata": re.compile(
        r"(?:本章|上一章|前一章|细纲|读者|爽点|伏笔|任务卡|章节定位)"
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile fiction prose style or compare it with a stable baseline."
    )
    parser.add_argument("targets", nargs="+", help="Target prose files or directories")
    parser.add_argument(
        "--baseline",
        action="append",
        default=[],
        help="Stable sample file or directory; repeat for multiple samples",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def canonical_root(path: Path) -> Path:
    if path.is_dir() and (path / "正文").is_dir():
        return path / "正文"
    return path


def collect_files(raw_paths: list[str]) -> list[Path]:
    files: set[Path] = set()
    for raw in raw_paths:
        path = canonical_root(Path(raw).expanduser())
        if not path.exists():
            raise FileNotFoundError(raw)
        if path.is_file():
            if path.suffix.lower() in TEXT_SUFFIXES:
                files.add(path.resolve())
            continue
        for candidate in path.rglob("*"):
            if not candidate.is_file() or candidate.suffix.lower() not in TEXT_SUFFIXES:
                continue
            relative_parts = candidate.relative_to(path).parts[:-1]
            if any(part.startswith(".") or part in SKIP_DIRS for part in relative_parts):
                continue
            files.add(candidate.resolve())
    return sorted(files)


def clean_markdown(text: str) -> str:
    kept: list[str] = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not stripped or stripped.startswith("<!--"):
            kept.append("")
            continue
        if MARKDOWN_PREFIX_RE.match(line):
            continue
        kept.append(line)
    return "\n".join(kept)


def sentence_lengths(text: str) -> list[int]:
    lengths: list[int] = []
    for match in SENTENCE_RE.finditer(text):
        sentence = SPACE_RE.sub("", match.group(0)).strip("。！？!?“”\"' ")
        if sentence:
            lengths.append(len(sentence))
    return lengths


def paragraphs(text: str) -> list[str]:
    return [SPACE_RE.sub("", part) for part in re.split(r"\n\s*\n", text) if part.strip()]


def round_ratio(value: float) -> float:
    return round(value, 4)


def profile(paths: list[Path]) -> dict:
    texts: list[str] = []
    for path in paths:
        texts.append(clean_markdown(path.read_text(encoding="utf-8")))
    text = "\n\n".join(texts)
    compact = SPACE_RE.sub("", text)
    char_count = len(compact)
    lengths = sentence_lengths(text)
    paras = paragraphs(text)
    dialogue_chars = sum(len(SPACE_RE.sub("", item)) for item in DIALOGUE_RE.findall(text))
    sentence_count = len(lengths)
    bucket_counts = {
        "1_8": sum(1 for length in lengths if length <= 8),
        "9_15": sum(1 for length in lengths if 9 <= length <= 15),
        "16_25": sum(1 for length in lengths if 16 <= length <= 25),
        "26_plus": sum(1 for length in lengths if length >= 26),
    }
    bucket_share = {
        key: round_ratio(value / sentence_count) if sentence_count else 0.0
        for key, value in bucket_counts.items()
    }
    single_sentence = sum(1 for para in paras if len(sentence_lengths(para)) == 1)
    punctuation = Counter(char for char in text if char in "。！？，；：……—!?；：")
    risk_counts = {name: len(pattern.findall(text)) for name, pattern in RISK_PATTERNS.items()}
    per_1000 = {
        "exclamation": round((punctuation["！"] + punctuation["!"]) * 1000 / char_count, 2)
        if char_count
        else 0.0,
        "ellipsis": round(text.count("……") * 1000 / char_count, 2) if char_count else 0.0,
        "dash": round(text.count("——") * 1000 / char_count, 2) if char_count else 0.0,
    }
    return {
        "files": [str(path) for path in paths],
        "file_count": len(paths),
        "characters": char_count,
        "sentence_count": sentence_count,
        "average_sentence_length": round(sum(lengths) / sentence_count, 2)
        if sentence_count
        else 0.0,
        "sentence_length_share": bucket_share,
        "paragraph_count": len(paras),
        "average_paragraph_characters": round(
            sum(len(para) for para in paras) / len(paras), 2
        )
        if paras
        else 0.0,
        "single_sentence_paragraph_share": round_ratio(single_sentence / len(paras))
        if paras
        else 0.0,
        "dialogue_character_share": round_ratio(dialogue_chars / char_count) if char_count else 0.0,
        "punctuation_per_1000_characters": per_1000,
        "risk_pattern_counts": risk_counts,
    }


def compare(baseline: dict, target: dict) -> dict:
    metrics = {
        "average_sentence_length": round(
            target["average_sentence_length"] - baseline["average_sentence_length"], 2
        ),
        "dialogue_character_share": round_ratio(
            target["dialogue_character_share"] - baseline["dialogue_character_share"]
        ),
        "single_sentence_paragraph_share": round_ratio(
            target["single_sentence_paragraph_share"]
            - baseline["single_sentence_paragraph_share"]
        ),
        "short_sentence_share_1_15": round_ratio(
            target["sentence_length_share"]["1_8"]
            + target["sentence_length_share"]["9_15"]
            - baseline["sentence_length_share"]["1_8"]
            - baseline["sentence_length_share"]["9_15"]
        ),
    }
    flags: list[dict] = []

    def flag(metric: str, delta: float, threshold: float, message: str) -> None:
        if abs(delta) >= threshold:
            flags.append({"metric": metric, "delta": delta, "message": message})

    flag(
        "average_sentence_length",
        metrics["average_sentence_length"],
        4.0,
        "平均句长与稳定样本差异较大，需结合章节类型人工复核。",
    )
    flag(
        "dialogue_character_share",
        metrics["dialogue_character_share"],
        0.15,
        "对白占比与稳定样本差异较大，先确认是否由章节类型造成。",
    )
    flag(
        "single_sentence_paragraph_share",
        metrics["single_sentence_paragraph_share"],
        0.20,
        "单句段比例明显偏移，检查电报体或段落变厚。",
    )
    flag(
        "short_sentence_share_1_15",
        metrics["short_sentence_share_1_15"],
        0.20,
        "短句占比明显偏移，检查节奏是否失真。",
    )
    return {"metric_deltas": metrics, "review_flags": flags}


def print_profile(label: str, data: dict) -> None:
    print(f"{label}: {data['file_count']} file(s), {data['characters']} characters")
    print(
        f"  sentence avg={data['average_sentence_length']}, "
        f"dialogue={data['dialogue_character_share']:.1%}, "
        f"single-paragraph={data['single_sentence_paragraph_share']:.1%}"
    )
    shares = data["sentence_length_share"]
    print(
        "  sentence share: "
        f"1-8={shares['1_8']:.1%}, 9-15={shares['9_15']:.1%}, "
        f"16-25={shares['16_25']:.1%}, 26+={shares['26_plus']:.1%}"
    )
    nonzero = {key: value for key, value in data["risk_pattern_counts"].items() if value}
    print(f"  risk patterns: {nonzero or 'none'}")


def main() -> int:
    args = parse_args()
    try:
        target_files = collect_files(args.targets)
        baseline_files = collect_files(args.baseline) if args.baseline else []
        if not target_files:
            raise ValueError("no target .md or .txt prose files found")
        if args.baseline and not baseline_files:
            raise ValueError("no baseline .md or .txt prose files found")
        target = profile(target_files)
        baseline = profile(baseline_files) if baseline_files else None
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    result = {"target": target, "manual_review_required": True}
    if baseline:
        result["baseline"] = baseline
        result["comparison"] = compare(baseline, target)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if baseline:
            print_profile("Baseline", baseline)
        print_profile("Target", target)
        if baseline:
            comparison = result["comparison"]
            print(f"Comparison deltas: {comparison['metric_deltas']}")
            if comparison["review_flags"]:
                for item in comparison["review_flags"]:
                    print(f"[REVIEW] {item['metric']}: {item['message']}")
            else:
                print("No large mechanical drift flags.")
        print("Manual style review is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
