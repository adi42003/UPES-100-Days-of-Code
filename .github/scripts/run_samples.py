import json
import pathlib
import re
import subprocess
import urllib.request

ROOT = pathlib.Path(".")
BANK_URL = "https://raw.githubusercontent.com/maitysoumik/basic-coding-with-c/main/questions2.json"

def norm(value):
    return " ".join(value.split())

def usable_input(value):
    if value is None:
        return False
    s = str(value).strip()
    if s.lower() in {"", "no input"}:
        return True
    # The source bank mixes actual stdin with human descriptions and
    # judge-style assignments. Only run cases that look like literal stdin.
    if any(token in s for token in ("File:", "Content:", "nums", "arr[]", "Student", "Details of", "Employee:", "Gender=", "Name:", "Roll:", "Joining Date:", "User Input:", "Input File", "Existing File", "Source File", "Filename:", "3 students:", "Student 1", "Student2", "Student:", "Student allocated", "No solution")):
        return False
    if any(ch in s for ch in "=[]{}"):
        return False
    if re.search(r"\b(input|output|content|file exists)\s*:", s, re.I):
        return False
    return True

def source_path(qid):
    if qid <= 100:
        day = (qid + 1) // 2
        problem = 1 if qid % 2 else 2
    else:
        day = qid - 50
        problem = 1
    return ROOT / f"Day-{day:03d}" / f"problem-{problem}.c"

with urllib.request.urlopen(BANK_URL, timeout=30) as response:
    bank = json.load(response)

questions = {}
for section in bank.get("questionBank", []):
    for q in section.get("questions", []):
        qid = int(q["id"])
        if qid <= 146:
            questions[qid] = q

# The upstream bank contains several incorrect expected values. Keep the
# programs mathematically correct and validate against independently computed
# results for those cases.
EXPECTED_OVERRIDES = {
    (4, "7"): "Area=153.94, Circumference=43.98",
    (9, "5000 7 3"): "Simple Interest=1050, Compound Interest=1125.22",
    (17, "1 -3 2"): "Roots are real and different: 2.00, 1.00",
    (17, "1 -2 1"): "Roots are real and same: 1.00",
    (44, "3"): "Approximate sum: 2.6",
    (44, "5"): "Approximate sum: 4.4",
    (45, "3"): "Approximate sum: 1.78",
    (45, "5"): "Approximate sum: 2.84",
    (123, "File: sample.txt (Content: Hello world\nThis is C programming)"):
        "Characters: 33 Words: 6 Lines: 2",
}

results = []
for qid in range(1, 147):
    q = questions.get(qid)
    src = source_path(qid)
    if not q or not src.exists():
        results.append((qid, "MISSING", str(src)))
        continue

    exe = pathlib.Path("/tmp") / f"upes-q{qid}"
    comp = subprocess.run(
        ["gcc", "-std=c11", "-Wall", "-Wextra", "-pedantic", str(src), "-lm", "-o", str(exe)],
        text=True, capture_output=True, timeout=15
    )
    if comp.returncode:
        results.append((qid, "COMPILE_FAIL", comp.stderr[-500:]))
        continue

    cases = q.get("testCases", [])
    runnable = [c for c in cases if (usable_input(c.get("input")) or qid == 123) and isinstance(c.get("output"), str)]
    ran = 0
    passed = 0
    failures = []
    for case in runnable:
        raw_input = str(case.get("input", ""))
        if raw_input.strip().lower() == "no input":
            raw_input = ""
        expected = norm(EXPECTED_OVERRIDES.get((qid, raw_input.replace("\\n", "\n")), case["output"]))
        # Prose-only expected outputs are not executable assertions.
        if expected.startswith(("Pattern with ", "Note:", "Tabular list", "Displays file content")):
            continue
        try:
            if qid == 123:
                import tempfile
                with tempfile.TemporaryDirectory(prefix="upes-q123-") as temp_dir:
                    pathlib.Path(temp_dir, "sample.txt").write_text(
                        "Hello world\nThis is C programming", encoding="utf-8"
                    )
                    run = subprocess.run(
                        [str(exe)], input="", text=True, capture_output=True,
                        timeout=3, cwd=temp_dir
                    )
            else:
                run = subprocess.run(
                    [str(exe)], input=raw_input + ("\n" if raw_input and not raw_input.endswith("\n") else ""),
                    text=True, capture_output=True, timeout=3
                )
            ran += 1
            actual = norm(run.stdout)
            if run.returncode == 0 and expected and expected in actual:
                passed += 1
            elif run.returncode == 0 and not expected and not actual:
                passed += 1
            else:
                failures.append({
                    "input": raw_input[:120],
                    "expected": expected[:180],
                    "actual": actual[:220],
                    "exit": run.returncode,
                    "stderr": norm(run.stderr)[:180]
                })
        except subprocess.TimeoutExpired:
            ran += 1
            failures.append({"input": raw_input[:120], "error": "Timed out after 3 seconds"})
    if ran == 0:
        results.append((qid, "NO_RUNNABLE_SAMPLE", "Sample inputs require file setup or are descriptive"))
    elif failures:
        results.append((qid, f"FAIL {passed}/{ran}", json.dumps(failures[:3], ensure_ascii=False)))
    else:
        results.append((qid, f"PASS {passed}/{ran}", ""))

with open("sample-test-report.txt", "w", encoding="utf-8") as report:
    for qid, status, detail in results:
        report.write(f"Q{qid:03d}: {status}\n")
        if detail:
            report.write(f"  {detail}\n")

counts = {}
for _, status, _ in results:
    key = status.split()[0]
    counts[key] = counts.get(key, 0) + 1
print("Question-level sample test summary:")
for key in ("PASS", "FAIL", "COMPILE_FAIL", "MISSING", "NO_RUNNABLE_SAMPLE"):
    print(f"{key}: {counts.get(key, 0)}")
print("Question-level failures:")
for qid, status, detail in results:
    if status.startswith(("FAIL", "COMPILE_FAIL", "MISSING")):
        print(f"Q{qid:03d}: {status} :: {detail}")
print("Full details saved to sample-test-report.txt")
