#!/usr/bin/env python3
# test_converter.py
# Auto-grader for the "Format Conversion" activity.
#
# HOW TO USE:
# 1. Make sure network_config.json and config_converter.py are in the
# SAME folder as this file.
# 2. Run: python3 test_converter.py
# 3. Read the [PASS] / [FAIL] / [ERROR] results. Fix config_converter.py
# and run again until every check passes.
#
# IMPORTANT: do NOT modify this file. It is the checker, not the code
# you fix. You only fix conversion bugs inside config_converter.py.

import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

EXPECTED_DEVICES = ["router-01", "switch-01", "firewall-01"]
SEP = "=" * 60

print(SEP)
print(" Format Conversion Pipeline - Auto-Grader")
print(SEP)
print()

# 0. Clean up any leftover output files from a previous run.
for f in ("config.yaml", "config.xml", "config_backup.json"):
    if os.path.exists(f):
        os.remove(f)

# 1. Run the student's pipeline.
print("[RUN ] Running config_converter.py ...")
try:
    result = subprocess.run(
        [sys.executable, "config_converter.py"],
        capture_output=True,
        text=True,
        timeout=60,
    )
except subprocess.TimeoutExpired:
    print("[ERROR] Your script is running for too long (timeout).")
    sys.exit(1)

print("[RUN ] Exit code:", result.returncode)
if result.stdout:
    print(result.stdout.strip())
if result.returncode != 0:
    print("[ERROR] Your script CRASHED. This is what it printed:")
    print("-" * 30)
    print((result.stderr or result.stdout)[-1500:])
    print("-" * 30)
else:
    print()

results = []
passed = 0
failed = 0
detail_written = False


def show_detail(msg):
    for line in msg.splitlines()[1:]:
        print(" " + line)


# 2. Check 1: config.yaml (JSON -> YAML)
print(" [TEST] Check 1: config.yaml (JSON -> YAML)")
try:
    with open("config.yaml", "r") as f:
        content = f.read().strip()
    if not content:
        raise ValueError("file is empty")
    missing = [d for d in EXPECTED_DEVICES if d not in content]
    if missing:
        raise ValueError(f"missing device(s): {', '.join(missing)}")
    results.append(("PASS", "config.yaml contains all 3 devices (JSON -> YAML works)"))
except Exception as e:
    results.append(("FAIL", f"config.yaml missing or invalid.\n -> {e}"))
print(" [%s] %s" % (results[-1][0], results[-1][1].splitlines()[0]))
show_detail(results[-1][1])
print()

# 3. Check 2: config.xml (YAML -> XML)
print(" [TEST] Check 2: config.xml (YAML -> XML)")
try:
    tree = ET.parse("config.xml")
    devices = [e for e in tree.getroot().findall("device")]
    names = [(e.findtext("name") or "") for e in devices]
    missing = [d for d in EXPECTED_DEVICES if d not in names]
    if len(devices) != 3 or missing:
        raise ValueError(f"found {len(devices)} <device> element(s); missing {', '.join(missing)}")
    results.append(("PASS", "config.xml is valid XML with 3 <device> elements (YAML -> XML works)"))
except Exception as e:
    results.append(("FAIL", f"config.xml missing or invalid.\n -> {e}"))
print(" [%s] %s" % (results[-1][0], results[-1][1].splitlines()[0]))
show_detail(results[-1][1])
print()

# 4. Check 3: config_backup.json (XML -> JSON)
print(" [TEST] Check 3: config_backup.json (XML -> JSON)")
try:
    with open("config_backup.json", "r") as f:
        data = json.load(f)
    devices = data.get("devices", [])
    names = [d.get("name", "") for d in devices]
    missing = [n for n in EXPECTED_DEVICES if n not in names]
    if len(devices) != 3 or missing:
        raise ValueError(f"expected 3 devices, found {len(devices)}; missing {', '.join(missing)}")
    results.append(("PASS", "config_backup.json has all 3 devices (XML -> JSON round-trip works)"))
except Exception as e:
    results.append(("FAIL", f"config_backup.json missing or invalid.\n -> {e}"))
print(" [%s] %s" % (results[-1][0], results[-1][1].splitlines()[0]))
show_detail(results[-1][1])
print()

# 5. Summary
passed = sum(1 for tag, _ in results if tag == "PASS")
failed = len(results) - passed
print(SEP)
tag = "3/3 - GREAT JOB!" if failed == 0 else f"{passed} passed, {failed} failed"
print(f" RESULT: {tag}")
if failed > 0:
    print(" You must fix the bugs in config_converter.py and run this grader again.")
print(SEP)