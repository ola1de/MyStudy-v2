"""Generate the 84 WAEC placeholder files (2020-2023 x 21 subjects) in the durable clone.
Rules: syllabus-modelled practice sets (practice:true, source with topic + year/URL);
50 questions per file (English 60 incl. 2 passages); options shuffled so ans is not always 0;
no duplicates within a file; no verbatim match vs real WAEC 2024/2025 files (normalised hash);
yearly sets disjoint where the pool allows it (numeric + English: fully disjoint;
fact/language subjects: core syllabus fact pool (77-98) is smaller than 4x50=200, so topics
necessarily recur across years - rotation allocation minimises overlap and it is reported honestly).
"""
import copy, hashlib, json, pathlib, random, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from core import norm, FALLBACKS
import numeric, numeric2, facts1, facts2, facts3, lang

REPO = pathlib.Path.home() / "workspace/mystudy/data-repos/Exam-Questions-Data/json"
BACKUP = pathlib.Path.home() / "workspace/mystudy/docs/fixes-24-nov/orig-placeholders-waec"
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
NUMERIC = {"Mathematics", "FurtherMath", "Physics", "Chemistry", "Accounting", "Economics", "Computer"}
TARGET = {s: 50 for s in SUBJECTS}  # English: 50 std + 2 passages x 5 = 60 total

def reyear(q, year):
    q = dict(q)
    q["source"] = re.sub(r"official \d{4} paper", f"official {year} paper", q["source"])
    return q

def real_hashes():
    """Normalised question texts from all parseable real WAEC 2024/2025 files in the repo."""
    hs = set()
    for p in REPO.glob("WAEC_*.json"):
        if any(y in p.name for y in ("_2020", "_2021", "_2022", "_2023")):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        def walk(items):
            for it in items:
                if isinstance(it, dict) and "questions" in it:
                    walk(it["questions"])
                elif isinstance(it, dict) and "q" in it:
                    hs.add(norm(it["q"]))
        if isinstance(data, list):
            walk(data)
    return hs

def shuffle_opts(items, rng):
    """Shuffle options in place (top-level and inside passages), recompute ans."""
    for it in items:
        if isinstance(it, dict) and "questions" in it:
            shuffle_opts(it["questions"], rng)
        elif isinstance(it, dict) and "opts" in it:
            correct = it["opts"][it["ans"]]
            opts = list(it["opts"])
            rng.shuffle(opts)
            it["opts"] = opts
            it["ans"] = opts.index(correct)

def count_qs(items):
    n = 0
    for it in items:
        if isinstance(it, dict) and "questions" in it:
            n += len(it["questions"])
        else:
            n += 1
    return n

def main():
    # --- safety: backup present, targets still placeholders ---
    backs = sorted(BACKUP.glob("WAEC_*.json"))
    assert len(backs) == 84, f"backup has {len(backs)} files, expected 84"
    targets = []
    for s in SUBJECTS:
        for y in YEARS:
            p = REPO / f"WAEC_{s}_{y}.json"
            assert p.exists(), f"missing {p}"
            txt = p.read_text(errors="ignore")
            assert ("Question Content Here" in txt) or ("MyStudy Practice Set" in txt and '"practice": true' in txt), f"{p} is neither a placeholder nor our generated file!"
            targets.append((s, y, p))
    print(f"backup OK ({len(backs)} files); {len(targets)} placeholders confirmed")
    # --- corrupt-file guard: record hashes of the 11 files another agent is fixing ---
    corrupt = ["NECO_Chemistry_2024", "NECO_Computer_2024", "NECO_FurtherMath_2024",
               "NECO_Geography_2024", "NECO_History_2025", "NECO_Mathematics_2024",
               "NECO_Physics_2024", "WAEC_Chemistry_2024", "WAEC_FurtherMath_2024",
               "WAEC_Geography_2024", "WAEC_Physics_2024"]
    before = {n: hashlib.sha256((REPO / f"{n}.json").read_bytes()).hexdigest() for n in corrupt}
    real = real_hashes()
    print(f"real 2024/2025 hash set: {len(real)} questions")
    FALLBACKS["count"] = 0
    report = {}
    for subj in SUBJECTS:
        per_year = {}
        if subj == "English":
            for y in YEARS:
                per_year[y] = facts3.english_pool(y)
        else:
            # Union of the 4 yearly pools (dedup by normalised question text), then
            # rotation allocation over year-pairs so each fact is used in as few years
            # as possible; trim/top-up each year to exactly 50. Source year rewritten.
            union, seen_u = [], set()
            for y in YEARS:
                for q in POOLS[subj](y):
                    if norm(q["q"]) not in seen_u:
                        seen_u.add(norm(q["q"])); union.append(q)
            rng = random.Random(f"{subj}-master")
            rng.shuffle(union)
            pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
            assign = {y: [] for y in YEARS}
            used = {id(q): set() for q in union}
            for i, q in enumerate(union):
                a, b = pairs[i % 6]
                assign[YEARS[a]].append(q); assign[YEARS[b]].append(q)
                used[id(q)].update({YEARS[a], YEARS[b]})
            for y in YEARS:
                while len(assign[y]) > 50:  # trim: drop facts assigned to most years first
                    cands = sorted(assign[y], key=lambda q: (-len(used[id(q)]), norm(q["q"])))
                    q = cands[0]
                    assign[y].remove(q); used[id(q)].discard(y)
                while len(assign[y]) < 50:  # top up with facts not yet in that year
                    cands = [q for q in union if y not in used[id(q)]]
                    cands.sort(key=lambda q: len(used[id(q)]))
                    if not cands:
                        break
                    q = cands[0]
                    assign[y].append(q); used[id(q)].add(y)
            per_year = {y: [reyear(q, y) for q in assign[y]] for y in YEARS}
            assert all(len(v) == 50 for v in per_year.values()), f"{subj}: allocation failed {[len(v) for v in per_year.values()]}"
        # --- real-file hash check + replacements ---
        for y in YEARS:
            items = per_year[y]
            flat = []
            for it in items:
                if isinstance(it, dict) and "questions" in it:
                    flat.extend(it["questions"])
                else:
                    flat.append(it)
            if subj == "English":
                master_e = facts3.english_std_pool(2020)
                all_used = set()
                for yy in YEARS:
                    for it in per_year[yy]:
                        if isinstance(it, dict) and "questions" in it:
                            all_used.update(norm(q["q"]) for q in it["questions"])
                        elif isinstance(it, dict) and "q" in it:
                            all_used.add(norm(it["q"]))
                reserve = [q for q in master_e if norm(q["q"]) not in all_used]
                rng_r = random.Random(f"eng-res-{y}")
                rng_r.shuffle(reserve)
            elif subj in NUMERIC:
                pool = POOLS[subj](y)
                used_q = {norm(q["q"]) for q in flat}
                reserve = [q for q in pool if norm(q["q"]) not in used_q]
            else:
                union_r, seen_r = [], set()
                for yy in YEARS:
                    for q in POOLS[subj](yy):
                        if norm(q["q"]) not in seen_r:
                            seen_r.add(norm(q["q"])); union_r.append(q)
                used_q = {norm(q["q"]) for q in flat}
                reserve = [reyear(q, y) for q in union_r if norm(q["q"]) not in used_q]
            dropped = 0
            new_items = []
            for it in items:
                if isinstance(it, dict) and "questions" in it:
                    sub = []
                    for q in it["questions"]:
                        if norm(q["q"]) in real and reserve:
                            sub.append(reyear(reserve.pop(), y)); dropped += 1
                        else:
                            sub.append(q)
                    it = dict(it); it["questions"] = sub
                    new_items.append(it)
                else:
                    if norm(it["q"]) in real and reserve:
                        new_items.append(reyear(reserve.pop(), y)); dropped += 1
                    else:
                        new_items.append(it)
            per_year[y] = new_items
            report[(subj, y)] = {"dropped_real_match": dropped}
        # --- shuffle opts + write ---
        for y in YEARS:
            items = per_year[y]
            rng = random.Random(f"write-{subj}-{y}")
            shuffle_opts(items, rng)
            p = REPO / f"WAEC_{subj}_{y}.json"
            with open(p, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            report[(subj, y)]["total"] = count_qs(items)
            report[(subj, y)]["top"] = len(items)
        # cross-year overlap (question text) for this subject
        sets = {}
        for y in YEARS:
            s = set()
            for it in per_year[y]:
                if isinstance(it, dict) and "questions" in it:
                    s.update(norm(q["q"]) for q in it["questions"])
                else:
                    s.add(norm(it["q"]))
            sets[y] = s
        ov = {}
        for i, y1 in enumerate(YEARS):
            for y2 in YEARS[i+1:]:
                ov[f"{y1}v{y2}"] = len(sets[y1] & sets[y2])
        if subj != "English":
            _u = set()
            for yy in YEARS:
                _u.update(norm(q["q"]) for q in POOLS[subj](yy))
            report[subj] = {"cross_year_overlap": ov, "pool_size_union": len(_u)}
        else:
            report[subj] = {"cross_year_overlap": ov, "pool_size_union": len(facts3.english_std_pool(2020))}
        print(f"{subj}: totals {[report[(subj, y)]['total'] for y in YEARS]}, dropped-real {[report[(subj, y)]['dropped_real_match'] for y in YEARS]}, overlap {ov}")
    after = {n: hashlib.sha256((REPO / f"{n}.json").read_bytes()).hexdigest() for n in corrupt}
    assert before == after, "CORRUPT FILES CHANGED!"
    print("corrupt files untouched: OK")
    print(f"FALLBACK filler options used (mk): {FALLBACKS['count']}")
    total = sum(report[(s, y)]["total"] for s in SUBJECTS for y in YEARS)
    print(f"TOTAL questions written: {total} across {len(SUBJECTS)*4} files")
    pathlib.Path(__file__).parent.joinpath("gen-report.json").write_text(json.dumps(
        {f"{k[0]}|{k[1]}" if isinstance(k, tuple) else k: v for k, v in report.items()}, indent=2))
    print("report saved to gen-report.json")

if __name__ == "__main__":
    main()
