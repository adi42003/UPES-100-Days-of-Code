#!/usr/bin/env python3
"""Compile and smoke-run every standalone C exercise with generated stdin/file fixtures.

This is a runtime smoke test, not a proof of semantic correctness. The official
sample runner remains responsible for checking expected output where examples
are executable.
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import tempfile

ROOT = pathlib.Path(".")
SOURCES = sorted(ROOT.glob("Day-*/*.c"))
REPORT = ROOT / "runtime-smoke-report.txt"

# Common fixture names used by introductory file-handling exercises.
FIXTURE_TEXT = (
    "1 2 3 4 5\n"
    "10 20 30\n"
    "Alice 101 85\n"
    "Bob 102 90\n"
    "Sample text file for C programming exercises.\n"
)

def decode_c_string(s: str) -> str:
    return bytes(s, "utf-8").decode("unicode_escape")

def scanf_formats(source: str) -> list[str]:
    formats = []
    for match in re.finditer(r"\bscanf\s*\(\s*\"((?:\\.|[^\"\\])*)\"", source):
        formats.append(decode_c_string(match.group(1)))
    return formats

def values_for_format(fmt: str) -> list[str]:
    values = []
    i = 0
    while i < len(fmt):
        if fmt[i] != "%":
            i += 1
            continue
        i += 1
        if i < len(fmt) and fmt[i] == "%":
            i += 1
            continue
        while i < len(fmt) and fmt[i] in "*0123456789.+-hlLjzt":
            i += 1
        if i >= len(fmt):
            break
        conv = fmt[i]
        i += 1
        if conv in "diouxX":
            values.append("2")
        elif conv in "fFeEgGaA":
            values.append("1.5")
        elif conv == "c":
            values.append("a")
        elif conv == "s" or conv == "[":
            if conv == "[":
                while i < len(fmt) and fmt[i] != "]":
                    i += 1
                i += (i < len(fmt))
            values.append("sample.txt")
        elif conv == "p":
            values.append("0")
    return values

def generated_stdin(source: str, path: str) -> str:
    tailored = {
        "Day-021/problem-1.c": "1234\n",
        "Day-074/problem-1.c": "source.txt destination.txt\n",
        "Day-020/problem-1.c": "13579\n",
        "Day-034/problem-2.c": "5\n10 20 30 40 50\n2\n",
        "Day-045/problem-1.c": "banana\na\n",
        "Day-050/problem-1.c": "12/04/2020\n",
        "Day-080/problem-1.c": "2\nAlice 101 85\nBob 102 90\n",
        "Day-093/problem-1.c": "2\nAlice 101 85\nBob 102 90\n",
        "Day-095/problem-1.c": "2\nAlice 101 85\nBob 102 90\n",
        "Day-096/problem-1.c": "Employee: Raj | ID: 11 | Joining Date: 12 05 2020\n",
    }
    if path in tailored:
        return tailored[path]
    tokens = []
    for fmt in scanf_formats(source):
        tokens.extend(values_for_format(fmt))
    # Supply enough values for small arrays and scanf loops; programs stop at EOF.
    if not tokens:
        return "sample.txt\n1\n2\n3\n"
    return " ".join(tokens * 12) + "\n"

def prepare_fixtures(source: str, work: pathlib.Path) -> None:
    names = set(re.findall(r'"([^"]+\.(?:txt|dat|csv|in))"', source, re.I))
    names.update({
        "input.txt", "output.txt", "data.txt", "source.txt",
        "destination.txt", "sample.txt", "file.txt", "numbers.txt",
        "student.txt", "employee.txt", "test.txt"
    })
    for name in names:
        path = work / name
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(FIXTURE_TEXT, encoding="utf-8")
        except (OSError, ValueError):
            pass

def main() -> int:
    if len(SOURCES) != 146:
        print(f"Expected 146 C files; found {len(SOURCES)}")
        return 1

    results = []
    with tempfile.TemporaryDirectory(prefix="upes-runtime-") as temp:
        base = pathlib.Path(temp)
        for index, source_path in enumerate(SOURCES, 1):
            source = source_path.read_text(encoding="utf-8", errors="replace")
            work = base / f"case-{index}"
            work.mkdir()
            prepare_fixtures(source, work)
            binary = work / "program"

            compile_result = subprocess.run(
                ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic",
                 str(source_path.resolve()), "-lm", "-o", str(binary)],
                capture_output=True, text=True, timeout=20
            )
            if compile_result.returncode != 0:
                results.append((source_path.as_posix(), "COMPILE_FAIL",
                                compile_result.stderr[-400:]))
                continue

            try:
                execution = subprocess.run(
                    [str(binary)],
                    input=generated_stdin(source, source_path.as_posix()),
                    capture_output=True,
                    text=True,
                    cwd=work,
                    timeout=3
                )
                if execution.returncode == 0:
                    results.append((source_path.as_posix(), "RAN",
                                    execution.stdout[-160:].replace("\n", " ")))
                else:
                    results.append((source_path.as_posix(),
                                    f"EXIT_{execution.returncode}",
                                    execution.stderr[-300:].replace("\n", " ")))
            except subprocess.TimeoutExpired:
                results.append((source_path.as_posix(), "TIMEOUT",
                                "Exceeded 3-second runtime limit"))
            except Exception as exc:
                results.append((source_path.as_posix(), "RUN_ERROR", str(exc)))

    with REPORT.open("w", encoding="utf-8") as report:
        for path, status, detail in results:
            report.write(f"{path}: {status}\n")
            if detail:
                report.write(f"  {detail}\n")

    counts = {}
    for _, status, _ in results:
        key = "RAN" if status == "RAN" else status
        counts[key] = counts.get(key, 0) + 1

    print("Runtime smoke-test summary")
    for key in ("RAN", "EXIT_1", "EXIT_2", "TIMEOUT", "RUN_ERROR",
                "COMPILE_FAIL"):
        print(f"{key}: {counts.get(key, 0)}")
    print(f"Programs attempted: {len(results)}")
    print(f"Full report: {REPORT}")
    problems = [item for item in results if item[1] != "RAN"]
    for path, status, detail in problems:
        print(f"{path}: {status} {detail}")
    return 1 if problems else 0

if __name__ == "__main__":
    raise SystemExit(main())
