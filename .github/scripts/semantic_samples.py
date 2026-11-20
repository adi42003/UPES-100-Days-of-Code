#!/usr/bin/env python3
"""Semantic tests for source-bank exercises whose examples use descriptive input."""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(".")
BANK_URL = "https://raw.githubusercontent.com/maitysoumik/basic-coding-with-c/main/questions2.json"

def path_for(qid: int) -> pathlib.Path:
    day = qid - 50
    return ROOT / f"Day-{day:03d}" / "problem-1.c"

def array_values(raw: str, index: int = 0) -> list[int]:
    groups = [group for group in re.findall(r"\[([^\]]*)\]", raw)
              if re.search(r"-?\d+", group)]
    if index >= len(groups):
        raise ValueError(f"Missing array in {raw!r}")
    return [int(x) for x in re.findall(r"-?\d+", groups[index])]

def make_cases(qid: int, question: dict) -> list[tuple[str, dict[str, str], str, dict[str, str]]]:
    """Return stdin, fixture files, expected stdout substring, expected output files."""
    cases = []
    for case in question.get("testCases", []):
        raw = str(case.get("input", ""))
        expected = str(case.get("output", ""))
        fixtures: dict[str, str] = {}
        output_files: dict[str, str] = {}
        if 101 <= qid <= 120:
            if qid == 101:
                a = array_values(raw); target = int(re.search(r"target\s*=\s*(-?\d+)", raw).group(1))
                data = f"{len(a)}\n{' '.join(map(str,a))}\n{target}\n"
            elif qid == 102:
                a = array_values(raw); x = int(re.search(r"x\s*=\s*(-?\d+)", raw).group(1))
                data = f"{len(a)}\n{' '.join(map(str,a))}\n{x}\n"
            elif qid in (103, 105, 106, 107, 108, 112, 118, 119):
                a = array_values(raw); data = f"{len(a)}\n{' '.join(map(str,a))}\n"
            elif qid == 104:
                n = int(re.search(r"n\s*=\s*(\d+)", raw).group(1)); data = f"{n}\n"
            elif qid in (109, 110, 111, 113):
                a = array_values(raw); k = int(re.search(r"k\s*=\s*(\d+)", raw).group(1))
                data = f"{len(a)}\n{' '.join(map(str,a))}\n{k}\n"
            elif qid == 114:
                value = re.search(r'"(.*)"', raw).group(1); data = value + "\n"
            elif qid == 115:
                values = re.findall(r'"([^"]*)"', raw); data = "\n".join(values[:2]) + "\n"
            elif qid == 116:
                a = array_values(raw); target = int(re.search(r"target\s*=\s*(-?\d+)", raw).group(1))
                data = f"{len(a)}\n{' '.join(map(str,a))}\n{target}\n"
            elif qid == 117:
                a = array_values(raw,0); b = array_values(raw,1)
                data = f"{len(a)}\n{' '.join(map(str,a))}\n{len(b)}\n{' '.join(map(str,b))}\n"
            elif qid == 120:
                value = re.sub(r"^\s*str\s*=\s*", "", raw)
                data = value + "\n"
            else:
                raise ValueError(f"No adapter for Q{qid}")
        elif qid == 121:
            match = re.search(r"Name:\s*([^,]+),\s*Age:\s*(\d+)", raw)
            data = f"{match.group(1).strip()} {match.group(2)}\n"
            expected = "File created successfully! Data written to info.txt"
            output_files["info.txt"] = f"Name: {match.group(1).strip()}\nAge: {match.group(2)}\n"
        elif qid == 122:
            fixtures["info.txt"] = "Name: Rahul\nAge: 23\n"
            data = "info.txt\n"
        elif qid == 123:
            fixtures["sample.txt"] = "Hello world\nThis is C programming"
            data = ""
            expected = "Characters: 33\nWords: 6\nLines: 2"
        elif qid == 124:
            fixtures["source.txt"] = "Learning C File Handling"
            data = "source.txt destination.txt\n"
            expected = "File copied successfully to destination.txt"
            output_files["destination.txt"] = fixtures["source.txt"]
        elif qid == 125:
            fixtures["data.txt"] = "Hello world"
            data = "This is appended text.\n"
            expected = "File updated successfully with appended text."
            output_files["data.txt"] = "Hello world\nThis is appended text.\n"
        elif qid == 126:
            fixtures["sample.txt"] = "Sample file contents\n"
            data = raw.split("Filename:")[1].split("(")[0].strip() + "\n"
            if "File Exists: Yes" in raw:
                expected = "File opened successfully. Sample file contents"
            else:
                expected = "Error: File does not exist!"
        elif qid == 127:
            fixtures["input.txt"] = "Hello World\nC programming"
            data = ""
            expected = "Conversion completed. Output written to output.txt"
            output_files["output.txt"] = "HELLO WORLD\nC PROGRAMMING"
        elif qid == 128:
            fixtures["text.txt"] = "Welcome to C language"
            data = ""
            expected = "Vowels: 8\nConsonants: 10"
        elif qid == 129:
            fixtures["numbers.txt"] = "10 20 30 40 50"
            data = ""
            expected = "Sum = 150\nAverage = 30.00"
        elif qid == 130:
            data = "2\nAsha 101 85\nRavi 102 92\n"
            expected = "Name: Asha | Roll: 101 | Marks: 85.00\nName: Ravi | Roll: 102 | Marks: 92.00"
        elif qid == 140:
            data = "MALE\n"; expected = "Male"
        elif qid == 141:
            data = "Asha 101 90\n"; expected = "Name: Asha | Roll: 101 | Marks: 90.00"
        elif qid == 142:
            data = "Asha 101 85\nRavi 102 92\nMina 103 88\nDev 104 76\nIra 105 91\n"
            expected = "Asha\t101\t85.00"
        elif qid == 143:
            data = "3\nRavi 101 95\nSita 102 85\nAman 103 88\n"
            expected = "Topper: Ravi (Marks: 95.00)"
        elif qid == 144:
            data = "Neha 104 92\n"; expected = "Name: Neha | Roll: 104 | Marks: 92.00"
        elif qid == 145:
            data = "3\nRiya 101 89\nKaran 102 96\nMeena 103 92\n"
            expected = "Top Student: Karan | Roll: 102 | Marks: 96.00"
        elif qid == 146:
            data = "Employee: Raj | ID: 11 | Joining Date: 12 05 2020\n"
            expected = "Name: Raj | ID: 11 | Joining Date: 12/05/2020"
        else:
            raise ValueError(f"No adapter for Q{qid}")
        cases.append((data, fixtures, expected, output_files))
    return cases

def main() -> int:
    import urllib.request
    with urllib.request.urlopen(BANK_URL, timeout=30) as response:
        bank = json.load(response)
    questions = {int(q["id"]): q for section in bank["questionBank"]
                 for q in section["questions"] if int(q["id"]) <= 146}

    test_ids = list(range(101, 121)) + list(range(121, 131)) + [140, 141, 142, 143, 144, 145, 146]
    failures = []
    passed = 0
    total = 0

    for qid in test_ids:
        source = path_for(qid)
        exe = pathlib.Path(tempfile.gettempdir()) / f"upes-semantic-q{qid}"
        compile_result = subprocess.run(
            ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic",
             str(source.resolve()), "-lm", "-o", str(exe)],
            capture_output=True, text=True, timeout=20
        )
        if compile_result.returncode:
            failures.append((qid, "COMPILE", compile_result.stderr[-500:]))
            continue

        for case_index, (stdin, fixtures, expected, output_files) in enumerate(make_cases(qid, questions[qid]), 1):
            total += 1
            with tempfile.TemporaryDirectory(prefix=f"upes-q{qid}-") as tmp:
                work = pathlib.Path(tmp)
                for name, content in fixtures.items():
                    (work / name).write_text(content, encoding="utf-8")
                try:
                    run = subprocess.run([str(exe)], input=stdin, text=True,
                                         capture_output=True, timeout=3, cwd=work)
                except subprocess.TimeoutExpired:
                    failures.append((qid, f"CASE {case_index}", "TIMEOUT"))
                    continue

                normalized = " ".join(run.stdout.split())
                expected_normalized = " ".join(expected.split())
                ok = run.returncode == 0 and expected_normalized in normalized
                for name, content in output_files.items():
                    target = work / name
                    if not target.exists() or target.read_text(encoding="utf-8") != content:
                        ok = False
                        failures.append((qid, f"CASE {case_index}", f"file mismatch: {name}"))
                if ok:
                    passed += 1
                elif not any(x[0] == qid and x[1] == f"CASE {case_index}" for x in failures):
                    failures.append((qid, f"CASE {case_index}",
                                     f"exit={run.returncode}; expected={expected_normalized!r}; actual={normalized!r}; stderr={run.stderr[-200:]!r}"))

    # Regression cases for edge conditions discovered during source review.
    edge_cases = [
        ("Day-009/problem-1.c", "1 0 -2\n",
         "Roots are real and different: 1.41, -1.41", {}),
        ("Day-018/problem-2.c", "-2147483648 0\n", "2147483648", {}),
        ("Day-019/problem-1.c", "-9223372036854775808 1\n",
         "9223372036854775808", {}),
        ("Day-020/problem-1.c", "9999999999\n", "3486784401 (", {}),
        ("Day-021/problem-1.c", "-1234\n", "-4231", {}),
        ("Day-054/problem-1.c", "8\n", "6", {}),
        ("Day-066/problem-1.c", "2\n2147483647 1\n-2147483648\n",
         "-1 -1", {}),
        ("Day-069/problem-1.c", "3\n-2147483648 -1 -2147483648\n",
         "-2147483648", {}),
    ]
    for source_name, stdin, expected, fixtures in edge_cases:
        source = ROOT / source_name
        exe = pathlib.Path(tempfile.gettempdir()) / ("upes-edge-" + source.parent.name + "-" + source.stem)
        compiled = subprocess.run(
            ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic",
             str(source.resolve()), "-lm", "-o", str(exe)],
            capture_output=True, text=True, timeout=20
        )
        total += 1
        if compiled.returncode != 0:
            failures.append((source_name, "EDGE COMPILE", compiled.stderr[-300:]))
            continue
        with tempfile.TemporaryDirectory(prefix="upes-edge-") as tmp:
            work = pathlib.Path(tmp)
            for name, value in fixtures.items():
                (work / name).write_text(value, encoding="utf-8")
            run = subprocess.run([str(exe)], input=stdin, text=True,
                                 capture_output=True, timeout=3, cwd=work)
            actual = " ".join(run.stdout.split())
            wanted = " ".join(expected.split())
            if run.returncode == 0 and wanted in actual:
                passed += 1
            else:
                failures.append((source_name, "EDGE RUN",
                                 f"exit={run.returncode}; expected={wanted!r}; actual={actual!r}"))

    # Copying a file onto itself must fail safely without truncating its content.
    source = ROOT / "Day-074/problem-1.c"
    exe = pathlib.Path(tempfile.gettempdir()) / "upes-edge-copy-self"
    compiled = subprocess.run(
        ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic",
         str(source.resolve()), "-lm", "-o", str(exe)],
        capture_output=True, text=True, timeout=20
    )
    total += 1
    if compiled.returncode != 0:
        failures.append(("Day-074/problem-1.c", "EDGE COMPILE", compiled.stderr[-300:]))
    else:
        with tempfile.TemporaryDirectory(prefix="upes-edge-copy-") as tmp:
            work = pathlib.Path(tmp)
            original = "do not truncate this file"
            (work / "same.txt").write_text(original, encoding="utf-8")
            run = subprocess.run([str(exe)], input="same.txt same.txt\n",
                                 text=True, capture_output=True, timeout=3, cwd=work)
            preserved = (work / "same.txt").read_text(encoding="utf-8")
            if run.returncode != 0 and preserved == original:
                passed += 1
            else:
                failures.append(("Day-074/problem-1.c", "EDGE RUN",
                                 f"exit={run.returncode}; preserved={preserved!r}"))

    print(f"Semantic and regression cases: {passed}/{total} passed")
    for failure in failures:
        print(f"Q{failure[0]} {failure[1]}: {failure[2]}")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
