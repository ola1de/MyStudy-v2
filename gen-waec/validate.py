"""Independent validation of the 84 generated WAEC files (run after gen.py).
Checks: parses; counts incl. passages; 4 distinct opts; ans in range; explanation present;
practice:true + source present on every question incl. passages; no within-file dups;
no normalised-text match vs real WAEC 2024/2025 files; ans option == pool's correct answer
(catches any shuffle/write error); ans distribution; cross-year overlap; changed-files audit.
"""
import hashlib, json, pathlib, random, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from core import norm
import numeric, numeric2, facts1, facts2, facts3, lang

REPO = pathlib.Path.home() / "workspace/mystudy/data-repos/Exam-Questions-Data/json"
YEARS = (2020, 2021, 2022, 2023)
SUBJECTS = ["Accounting", "Agric", "Biology", "CRS", "Chemistry", "Civic", "Commerce",
            "Computer", "Economics", "English", "FurtherMath", "Geography", "Government",
            "Hausa", "History", "IRS", "Igbo", "Literature", "Mathematics", "Physics", "Yoruba"]
POOLS = {
    "Mathematics": numeric.math_pool, "FurtherMath": numeric.furthermath_pool, "Physics": numeric.physics_pool,
    "Chemistry": numeric2.chemistry_pool, "Accounting": numeric2.accounting_pool,
    "Economics": numeric2.economics_pool, "Computer": numeric2.computer_pool,
    "Biology": facts1.biology_pool, "Agric": facts1.agric_pool, "Geography": facts1.geography_pool,
    "Commerce": facts2.commerce_pool, "Civic": facts2.civic_pool,
    "Government": facts2.government_pool, "History": facts2.history_pool,
    "CRS": facts3.crs_pool, "IRS": facts3.irs_pool, "Literature": facts3.literature_pool,
    "Hausa": lang.hausa_pool, "Igbo": lang.igbo_pool, "Yoruba": lang.yoruba_pool,
}

def flat(items):
    out = []
    for it in items:
        if isinstance(it, dict) and "questions" in it:
            out.extend(it["questions"])
        else:
            out.append(it)
    return out

def main():
    # pool correct-answer map: norm(q) -> correct option text
    correct = {}  # (subject, norm(q)) -> correct option text (per-subject: same stem can
    # have different correct completions in different subjects, e.g. Government vs Economics)
    for subj, fn in POOLS.items():
        for y in YEARS:
            for q in fn(y):
                correct.setdefault((subj, norm(q["q"])), q["opts"][q["ans"]])
    for y in YEARS:
        for q in facts3.english_std_pool(y):
            correct.setdefault(("English", norm(q["q"])), q["opts"][q["ans"]])
    for _title, _content, qs in facts3.PASSAGES:
        for q, c, _ds, _e, _t in qs:
            correct.setdefault(("English", norm(q)), c)
    # real 2024/2025 hashes
    real = set()
    for p in REPO.glob("WAEC_*.json"):
        if any(f"_{y}" in p.name for y in YEARS):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, list):
            real.update(norm(q["q"]) for q in flat(data) if isinstance(q, dict) and "q" in q)
    print(f"pool answer map: {len(correct)} questions; real 2024/2025 hash set: {len(real)}")
    problems, rows = [], []
    total = 0
    for subj in SUBJECTS:
        sets = {}
        for y in YEARS:
            p = REPO / f"WAEC_{subj}_{y}.json"
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception as e:
                problems.append(f"{p.name}: JSON PARSE FAIL {e}"); continue
            qs = flat(data)
            total += len(qs)
            seen, dups, ans_bad, missing = set(), 0, 0, []
            ans_dist = {0: 0, 1: 0, 2: 0, 3: 0}
            real_match = 0
            for q in qs:
                k = norm(q.get("q", ""))
                if k in seen: dups += 1
                seen.add(k)
                if k in real: real_match += 1
                opts = q.get("opts", [])
                if len(opts) != 4 or len(set(opts)) != 4:
                    problems.append(f"{p.name}: bad opts {q.get('q','')[:60]!r}"); ans_bad += 1
                a = q.get("ans")
                if not isinstance(a, int) or a not in (0, 1, 2, 3):
                    problems.append(f"{p.name}: bad ans {a} {q.get('q','')[:60]!r}"); ans_bad += 1
                else:
                    ans_dist[a] += 1
                    exp = correct.get((subj, k))
                    if exp is not None and opts[a] != exp:
                        problems.append(f"{p.name}: ans mismatch {q.get('q','')[:60]!r} -> {opts[a]!r} != pool {exp!r}")
                    elif exp is None:
                        missing.append(q.get("q", "")[:60])
                if not q.get("explanation"):
                    problems.append(f"{p.name}: missing explanation {q.get('q','')[:60]!r}")
                if q.get("practice") is not True:
                    problems.append(f"{p.name}: practice!=True {q.get('q','')[:60]!r}")
                src = q.get("source", "")
                if "MyStudy Practice Set" not in src or f"official {y} paper" not in src or "Topic:" not in src:
                    problems.append(f"{p.name}: bad source {q.get('q','')[:60]!r}")
            sets[y] = seen
            rows.append((subj, y, len(data), len(qs), dups, real_match, ans_dist, len(missing)))
            if missing:
                problems.append(f"{p.name}: {len(missing)} questions not found in pool map (first: {missing[0]!r})")
        ov = {f"{a}v{b}": len(sets[a] & sets[b]) for i, a in enumerate(YEARS) for b in YEARS[i+1:]}
        print(f"{subj}: overlap {ov}")
    print("\nper-file: subj year top-level total dups real-match ans-dist not-in-pool")
    for r in rows:
        print(r)
    print(f"\nTOTAL questions: {total}")
    print(f"PROBLEMS: {len(problems)}")
    for pr in problems[:40]:
        print("  !!", pr)
    # changed-files audit vs pre-gen snapshot
    snap = json.loads(pathlib.Path(__file__).parent.joinpath("pre-gen-hashes.json").read_text())
    now = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(REPO.glob("*.json"))}
    changed = sorted(n for n in now if snap.get(n) != now[n])
    new = sorted(n for n in now if n not in snap)
    gone = sorted(n for n in snap if n not in now)
    print(f"\nfiles changed vs pre-gen snapshot: {len(changed)} (snapshot had {len(snap)}, now {len(now)})")
    extra = [c for c in changed if not (c.startswith("WAEC_") and any(f"_{y}.json" in c for y in YEARS))]
    print("changed files NOT among the 84 WAEC 2020-2023 targets:", extra or "none")
    print("new files:", new or "none", "| missing files:", gone or "none")
    pathlib.Path(__file__).parent.joinpath("validate-report.json").write_text(json.dumps(
        {"rows": rows, "problems": problems, "total": total, "changed": changed,
         "extra_changed": extra, "new": new, "gone": gone}, indent=2))
    print("validation report saved to validate-report.json")

if __name__ == "__main__":
    main()
