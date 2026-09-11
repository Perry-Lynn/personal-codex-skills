from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, str(ROOT / script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


class ProofreadScriptTests(unittest.TestCase):
    SCRIPT = "skills/writing/language-quality/story-chinese-proofreading/scripts/chinese_proofread.py"

    def test_valid_clean_and_candidate_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            clean = root / "clean.md"
            clean.write_text("这是一个干净的句子。", encoding="utf-8")
            result = run(self.SCRIPT, str(clean), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["files_checked"], 1)

            candidate = root / "candidate.md"
            candidate.write_text("他说……\u3000等等", encoding="utf-8")
            result = run(self.SCRIPT, str(candidate), "--json")
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertTrue(json.loads(result.stdout)["findings"])

    def test_invalid_scope_and_encoding_return_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            empty = root / "empty"
            empty.mkdir()
            blank = root / "blank.md"
            blank.write_text(" \n", encoding="utf-8")
            unsupported = root / "image.csv"
            unsupported.write_text("x", encoding="utf-8")
            bad_encoding = root / "bad.md"
            bad_encoding.write_bytes(b"\xff")
            valid = root / "valid.md"
            valid.write_text("有效正文。", encoding="utf-8-sig")
            for target in (root / "missing.md", empty, blank, unsupported, bad_encoding):
                result = run(self.SCRIPT, str(target))
                self.assertEqual(result.returncode, 2, (target, result.stderr))
                self.assertIn("ERROR", result.stderr)
            result = run(self.SCRIPT, str(valid), str(root / "missing.md"))
            self.assertEqual(result.returncode, 2)


class OverlapScriptTests(unittest.TestCase):
    SCRIPT = "skills/writing/originality/story-originality-audit/scripts/text_overlap.py"

    def test_zero_and_nonzero_candidates_are_successful(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manuscript = root / "manuscript.md"
            source = root / "source.md"
            manuscript.write_text("甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未", encoding="utf-8")
            source.write_text("天南海北春夏秋冬风雨雷电山川湖泊", encoding="utf-8")
            result = run(self.SCRIPT, str(manuscript), str(source), "--json")
            payload = json.loads(result.stdout)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertGreater(payload["manuscript_files"], 0)
            self.assertEqual(payload["findings"], [])

            source.write_text("甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未", encoding="utf-8")
            result = run(self.SCRIPT, str(manuscript), str(source), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["findings"])

    def test_bad_paths_parameters_and_short_material_return_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manuscript = root / "manuscript.md"
            source = root / "source.md"
            manuscript.write_text("这是一段足够长度的稿件内容用于比较。", encoding="utf-8")
            source.write_text("这是一段足够长度的来源内容用于比较。", encoding="utf-8")
            empty_source = root / "empty-source"
            empty_source.mkdir()
            cases = (
                (str(root / "missing.md"), str(source)),
                (str(manuscript), str(root / "missing-source.md")),
                (str(manuscript), str(empty_source)),
                (str(manuscript), str(source), "--ngram", "7"),
                (str(manuscript), str(source), "--limit", "0"),
            )
            for args in cases:
                result = run(self.SCRIPT, *args)
                self.assertEqual(result.returncode, 2, (args, result.stderr))
            short = root / "short.md"
            short.write_text("短文本", encoding="utf-8")
            result = run(self.SCRIPT, str(short), str(source))
            self.assertEqual(result.returncode, 2)


class MetricsScriptTests(unittest.TestCase):
    SCRIPT = "skills/writing/performance-diagnostics/story-serial-performance-diagnostics/scripts/serial_metrics.py"

    def test_percent_finite_values_adjacency_and_ratio_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_file = Path(tmp) / "metrics.csv"
            csv_file.write_text(
                "chapter,metric,percent,decimal,num,den\n"
                "1,100,50%,0.5,1,2\n"
                "2,,bad,NaN,2,0\n"
                "3,120,100%,0.5,3,3\n"
                "4,60,Infinity,0.5,4,2\n",
                encoding="utf-8",
            )
            result = run(
                self.SCRIPT,
                str(csv_file),
                "--value",
                "metric",
                "--value",
                "percent",
                "--value",
                "decimal",
                "--ratio",
                "rate=num/den",
                "--json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            rows = payload["rows"]
            self.assertEqual(rows[0]["percent"], 0.5)
            self.assertEqual(rows[0]["decimal"], 0.5)
            self.assertEqual([rows[i]["metric_change"] for i in range(4)], [None, None, None, -0.5])
            self.assertIsNone(rows[1]["rate"])
            self.assertTrue(rows[1]["diagnostics"])
            self.assertIsNone(rows[1]["decimal"])
            self.assertIsNone(rows[3]["percent"])
            self.assertTrue(any("NaN" in diagnostic for diagnostic in rows[1]["diagnostics"]))

    def test_metric_contract_errors_return_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            no_analysis = root / "no-analysis.csv"
            no_analysis.write_text("chapter,note\n1,hello\n", encoding="utf-8")
            for extra in ((), ("--value", "unknown"), ("--ratio", "bad=unknown/den"), ("--ratio", "same=chapter/den")):
                result = run(self.SCRIPT, str(no_analysis), *extra)
                self.assertEqual(result.returncode, 2, (extra, result.stderr))
            data = root / "data.csv"
            data.write_text("chapter,value,den\n1,1,1\n", encoding="utf-8")
            for extra in (("--ratio", "x=value"), ("--ratio", "value=value/den"), ("--ratio", "x=value/den/den")):
                result = run(self.SCRIPT, str(data), *extra)
                self.assertEqual(result.returncode, 2, (extra, result.stderr))

    def test_derived_non_finite_values_are_null(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            csv_file = Path(tmp) / "overflow.csv"
            csv_file.write_text("chapter,value,num,den\n1,1e308,1e308,1e-308\n2,-1e308,1,1\n", encoding="utf-8")
            result = run(self.SCRIPT, str(csv_file), "--value", "value", "--ratio", "rate=num/den", "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(result.stdout)["rows"][1]
            self.assertIsNone(row["value_change"])
            self.assertTrue(any("non-finite" in diagnostic for diagnostic in row["diagnostics"]))
            self.assertIsNone(json.loads(result.stdout)["rows"][0]["rate"])


class FanqieScriptTests(unittest.TestCase):
    SCRIPT = "skills/writing/publishing-compliance/story-fanqie-compliance/scripts/fanqie_preflight.py"

    def test正文_subtree_wins_and_explicit_excluded_file_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            (root / "正文").mkdir(parents=True)
            (root / "设定").mkdir()
            (root / "追踪").mkdir()
            (root / "正文" / "01.md").write_text("这是正文内容，没有工程词。", encoding="utf-8")
            trigger = "第十章 这是追踪文件中的工程词"
            tracked = root / "追踪" / "notes.md"
            tracked.write_text(trigger, encoding="utf-8")
            result = run(self.SCRIPT, str(root), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["summary"]["files"], 1)
            result = run(self.SCRIPT, str(tracked), "--json")
            self.assertEqual(result.returncode, 1)

    def test_fallback_filter_empty_and_ancestor_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            archive = Path(tmp) / "归档"
            project = archive / "project"
            (project / "设定").mkdir(parents=True)
            (project / "设定" / "setting.md").write_text("第十章", encoding="utf-8")
            result = run(self.SCRIPT, str(project), "--json")
            self.assertEqual(result.returncode, 2)
            (project / "story.md").write_text("正文没有工程词。", encoding="utf-8")
            result = run(self.SCRIPT, str(project), "--json")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["summary"]["files"], 1)


if __name__ == "__main__":
    unittest.main()
