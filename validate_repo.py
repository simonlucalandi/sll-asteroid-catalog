#!/usr/bin/env python3
"""validate_repo.py -- integrity check for this catalog.

Verifies that the per-object files under objects/ and the published catalog can never
silently drift: every objects/<n>.md must match a catalog (or rejected) row on period,
shape, and status; filenames must match their frontmatter; there must be no orphan files;
and every rejected object should have a file explaining why. Self-contained -- reads only
catalog/catalog.csv, catalog/rejected.csv, and objects/*.md.

Run from anywhere:  python3 validate_repo.py   (exit 0 = clean, 1 = mismatches).
"""
from __future__ import annotations
import csv, glob, os, re, sys

REPO = os.path.dirname(os.path.abspath(__file__))


def load_catalog():
    """num -> dict(P_rot_h, shape, status) from catalog.csv + rejected.csv."""
    ref = {}
    with open(os.path.join(REPO, "catalog", "catalog.csv")) as f:
        for r in csv.DictReader(f):
            ref[r["number"].strip()] = dict(P_rot_h=r["P_rot_h"].strip(),
                                            shape=r["shape"].strip(), status=r["status"].strip().upper())
    rej = os.path.join(REPO, "catalog", "rejected.csv")
    if os.path.exists(rej):
        with open(rej) as f:
            for r in csv.DictReader(f):
                ref.setdefault(r["number"].strip(), dict(P_rot_h="", shape="", status="KILLED"))
    return ref


def parse_frontmatter(path):
    txt = open(path).read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def approx_equal(a, b, tol=0.02):
    try:
        a, b = float(a), float(b)
    except (ValueError, TypeError):
        return str(a).strip() == str(b).strip()
    if b == 0:
        return abs(a) < 1e-9
    return abs(a - b) / abs(b) <= tol


def main():
    ref = load_catalog()
    errors, warnings, seen = [], [], set()
    for path in sorted(glob.glob(os.path.join(REPO, "objects", "*.md"))):
        base = os.path.basename(path)
        if base == "README.md":
            continue
        fname_num = base[:-3]
        fm = parse_frontmatter(path)
        if fm is None:
            errors.append(f"{base}: no YAML frontmatter")
            continue
        num = str(fm.get("number", "")).strip()
        seen.add(num)
        if num != fname_num:
            errors.append(f"{base}: frontmatter number '{num}' != filename '{fname_num}'")
        if num not in ref:
            errors.append(f"{base}: number {num} not in catalog.csv or rejected.csv (orphan)")
            continue
        c = ref[num]
        if (c["status"] or "").upper() != (fm.get("status", "") or "").upper():
            errors.append(f"{base}: status '{fm.get('status')}' != catalog '{c['status']}'")
        if c["status"] != "KILLED":
            if not approx_equal(fm.get("P_rot_h"), c["P_rot_h"]):
                errors.append(f"{base}: P_rot_h '{fm.get('P_rot_h')}' != catalog '{c['P_rot_h']}'")
            if (fm.get("shape", "") or "").strip() != (c["shape"] or "").strip():
                errors.append(f"{base}: shape '{fm.get('shape')}' != catalog '{c['shape']}'")

    for num, c in ref.items():
        if num not in seen and c["status"] == "KILLED":
            warnings.append(f"({num}) is KILLED but has no objects/{num}.md explaining why")

    print(f"checked {len(seen)} object files against {len(ref)} catalog/rejected rows")
    for w in warnings:
        print(f"  WARN: {w}")
    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        print(f"FAIL: {len(errors)} mismatch(es)")
        return 1
    print("OK: all object files match the catalog (period, shape, status, filename)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
