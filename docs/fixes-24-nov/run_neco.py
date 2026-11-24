#!/usr/bin/env python3
"""Generate the 84 NECO placeholder files (2020-2023 x 21 subjects) in the durable clone.

Steps: verify the 84 placeholders -> back up originals -> build pools
(base + expansion + topup) -> dedupe by normalised text -> drop any item
whose normalised text matches a real NECO 2024/2025 question -> split into
4 distinct yearly sets -> write JSON -> validate every file.

Run from ~/workspace/mystudy/docs/fixes-24-nov/ :  python3 run_neco.py
Writes only the 84 files in BASE. Never touches corrupt files or WAEC/JAMB.
"""
import importlib.util
import json
import pathlib
import random
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
BASE = pathlib.Path("/home/hatch/workspace/mystudy/data-repos/Exam-Questions-Data/json")
BACKUP = HERE / "orig-placeholders-neco"
REPORT = HERE / "validation-neco-24-nov.json"

YEARS = [2020, 2021, 2022, 2023]
SUBJECTS = ["Accounting", "Agric", "Biology", "CRS", "Chemistry", "Civic", "Commerce",
            "Computer", "Economics", "English", "FurtherMath", "Geography", "Government",
            "Hausa", "History", "IRS", "Igbo", "Literature", "Mathematics", "Physics", "Yoruba"]

# per-year standard-question counts; passages add the remainder
STD_PER_YEAR = {"English": 50, "Literature": 35}
DEFAULT_STD = 40


def load_pools():
    spec = importlib.util.spec_from_file_location("gb", HERE / "gen_base.py")
    gb = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gb)
    ns = dict(vars(gb))
    ns["__name__"] = "gn"
    exec(open(HERE / "gen_neco.py").read(), ns)
    exec(open(HERE / "gen_topup.py").read(), ns)
    return gb, ns


def real_question_hashes(gb):
    """Normalised question texts from every real NECO 2024/2025 file that parses."""
    hashes = set()
    files = 0
    for path in sorted(BASE.glob("NECO_*.json")):
        if not (path.name.endswith("_2024.json") or path.name.endswith("_2025.json")):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue  # corrupt file - not ours
        files += 1
        for item in data:
            if isinstance(item, dict) and item.get("type") == "std":
                hashes.add(gb.norm(item.get("q", "")))
            elif isinstance(item, dict) and item.get("type") == "passage":
                for q in item.get("questions", []):
                    hashes.add(gb.norm(q.get("q", "")))
    return hashes, files


def main():
    gb, ns = load_pools()
    norm = gb.norm
    finalise = gb.finalise
    mk = gb.mk

    # ---- 1. verify the 84 placeholders -------------------------------------
    placeholders = sorted(
        p for p in BASE.glob("NECO_*.json")
        if "Question Content Here" in p.read_text(errors="ignore"))
    expected = {f"NECO_{s}_{y}.json" for s in SUBJECTS for y in YEARS}
    found = {p.name for p in placeholders}
    assert found == expected, (
        f"placeholder set mismatch: missing={sorted(expected - found)} "
        f"extra={sorted(found - expected)}")
    print(f"Verified {len(placeholders)} NECO placeholders.")

    # ---- 2. back up originals ----------------------------------------------
    BACKUP.mkdir(parents=True, exist_ok=True)
    backed = 0
    for p in placeholders:
        dest = BACKUP / p.name
        if dest.exists():
            assert dest.read_text(encoding="utf-8") == p.read_text(encoding="utf-8"), \
                f"backup {p.name} differs from current original - refusing to overwrite backup"
        else:
            shutil.copy2(p, dest)
            backed += 1
    print(f"Backed up {backed} originals to {BACKUP} "
          f"({len(list(BACKUP.glob('*.json')))} files now in backup dir).")

    # ---- 3. real-file hash set ----------------------------------------------
    real_hashes, real_files = real_question_hashes(gb)
    print(f"Real NECO 2024/2025 hash set: {len(real_hashes)} questions from {real_files} files.")

    base_fns = {"Mathematics": gb.maths_pool, "FurtherMath": gb.furthermath_pool,
                "Physics": gb.physics_pool, "Chemistry": gb.chemistry_pool,
                "Biology": gb.biology_pool, "Accounting": gb.accounting_pool,
                "Economics": gb.economics_pool, "Commerce": gb.commerce_pool,
                "Computer": gb.computer_pool, "Agric": gb.agric_pool,
                "Geography": gb.geography_pool, "Government": gb.government_pool,
                "History": gb.history_pool, "CRS": gb.crs_pool, "IRS": gb.irs_pool,
                "Civic": gb.civic_pool, "Literature": gb.literature_pool,
                "English": gb.english_pool, "Hausa": gb.hausa_pool,
                "Igbo": gb.igbo_pool, "Yoruba": gb.yoruba_pool}

    # ---- 4. build, dedupe, filter, split (all in memory; nothing written yet) --
    report = {"files": {}, "subjects": {}}
    total_questions = 0
    built = {}
    for subj in SUBJECTS:
        raw = list(base_fns[subj]())
        for ep in ["extra_pool", "extra_pool2", "extra_pool3", "extra_pool4", "extra_pool5"]:
            raw += list(ns[ep](subj))
        raw += list(ns["topup_pool"](subj))
        # dedupe by normalised question text (keep first occurrence)
        seen, uniq = set(), []
        dupes = 0
        for item in raw:
            n = norm(item["q"])
            if n in seen:
                dupes += 1
                continue
            seen.add(n)
            uniq.append(item)
        # drop anything matching a real 2024/2025 question verbatim (normalised)
        kept, dropped_real = [], 0
        for item in uniq:
            if norm(item["q"]) in real_hashes:
                dropped_real += 1
                continue
            kept.append(item)
        need = STD_PER_YEAR.get(subj, DEFAULT_STD) * 4
        assert len(kept) >= need, (
            f"{subj}: only {len(kept)} unique questions after filtering, need {need}")
        rng = random.Random(f"NECO-{subj}-2026")
        rng.shuffle(kept)
        chunks = [kept[i * need // 4:(i + 1) * need // 4] for i in range(4)]

        # passages
        if subj == "English":
            passages = list(gb.ENGLISH_PASSAGES)
            rng.shuffle(passages)
            passage_pairs = [passages[0:2], passages[2:4], passages[4:6], passages[6:8]]
        elif subj == "Literature":
            poems = list(gb.LITERATURE_POEMS)
            rng.shuffle(poems)
            passage_pairs = [[p] for p in poems]
        else:
            passage_pairs = [[] for _ in range(4)]

        subj_q_total = 0
        for yi, year in enumerate(YEARS):
            items = []
            std_items = chunks[yi]
            for idx, raw_item in enumerate(std_items):
                items.append(finalise(raw_item, year, subj, seed=year * 10000 + idx))
            # insert passages: English after 25 std then at end; Literature in the middle
            built_passages = []
            for title, content, qs in passage_pairs[yi]:
                pqs = []
                for qi, (pq, pc, pd, pe) in enumerate(qs):
                    raw_q = mk(year, subj, "Comprehension" if subj == "English" else "Poetry Analysis",
                               pq, pc, pd, pe)
                    pqs.append(finalise(raw_q, year, subj, seed=year * 10000 + 500 + qi))
                built_passages.append({
                    "type": "passage", "content": content, "questions": pqs,
                    "practice": True,
                    "source": f"MyStudy Practice Set \u2014 modelled on the NECO syllabus "
                              f"for this subject, not the official {year} paper",
                    "topic": "Comprehension" if subj == "English" else "Poetry Analysis",
                })
            if subj == "English":
                items = items[:25] + built_passages[:1] + items[25:] + built_passages[1:]
            elif subj == "Literature":
                items = items[:20] + built_passages + items[20:]
            q_count = sum(len(it["questions"]) if it["type"] == "passage" else 1 for it in items)
            subj_q_total += q_count
            fname = f"NECO_{subj}_{year}.json"
            built[fname] = items
            report["files"][fname] = {
                "subject": subj, "year": year, "items": len(items),
                "questions": q_count,
                "passages": len(built_passages),
            }
        report["subjects"][subj] = {
            "pool_total": len(raw), "duplicates_removed": dupes,
            "dropped_real_match": dropped_real, "unique_kept": len(kept),
            "questions_written": subj_q_total,
        }
        total_questions += subj_q_total
        print(f"{subj:12s} pool={len(raw):4d} dupes={dupes:3d} real_match_dropped={dropped_real:3d} "
              f"kept={len(kept):4d} questions={subj_q_total}")

    # ---- 4b. write files (only reached if the whole in-memory build succeeded)
    for fname, items in built.items():
        with open(BASE / fname, "w", encoding="utf-8") as fh:
            json.dump(items, fh, ensure_ascii=False, indent=2)
    print(f"Wrote {len(built)} files to {BASE}.")

    # ---- 5. validate every written file --------------------------------------
    print("\nValidating...")
    errors = []
    year_sets = {subj: [] for subj in SUBJECTS}
    for fname, meta in sorted(report["files"].items()):
        path = BASE / fname
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{fname}: JSON parse failed: {e}")
            continue
        assert isinstance(data, list), f"{fname}: not a list"
        if len(data) != meta["items"]:
            errors.append(f"{fname}: item count {len(data)} != {meta['items']}")
        qs = []
        for it in data:
            if it.get("type") == "std":
                qs.append(it)
            elif it.get("type") == "passage":
                qs.extend(it.get("questions", []))
                if not it.get("content"):
                    errors.append(f"{fname}: passage with empty content")
            else:
                errors.append(f"{fname}: unknown item type {it.get('type')!r}")
        if len(qs) != meta["questions"]:
            errors.append(f"{fname}: question count {len(qs)} != {meta['questions']}")
        norms = [norm(q["q"]) for q in qs]
        if len(set(norms)) != len(norms):
            errors.append(f"{fname}: duplicate questions within file")
        if set(norms) & real_hashes:
            errors.append(f"{fname}: {len(set(norms) & real_hashes)} questions match real 2024/2025 files")
        year_sets[meta["subject"]].append(set(norms))
        for q in qs:
            opts = q.get("opts", [])
            if len(opts) != 4 or len({str(o) for o in opts}) != 4:
                errors.append(f"{fname}: question {q.get('q','')[:40]!r} does not have 4 distinct options")
            ans = q.get("ans")
            if not isinstance(ans, int) or not (0 <= ans <= 3):
                errors.append(f"{fname}: question {q.get('q','')[:40]!r} bad ans {ans!r}")
            if q.get("practice") is not True:
                errors.append(f"{fname}: question missing practice:true")
            if str(meta["year"]) not in str(q.get("source", "")):
                errors.append(f"{fname}: question source missing year")
            if not q.get("topic"):
                errors.append(f"{fname}: question missing topic")
            if not q.get("explanation"):
                errors.append(f"{fname}: question missing explanation")
            if not q.get("adapted_from"):
                errors.append(f"{fname}: question missing adapted_from")
        # spot-check: ans option must be a non-empty string
        for q in qs:
            if not str(q["opts"][q["ans"]]).strip():
                errors.append(f"{fname}: empty correct option")
    # cross-year overlap within each subject
    for subj, sets in year_sets.items():
        for i in range(4):
            for j in range(i + 1, 4):
                overlap = sets[i] & sets[j]
                if overlap:
                    errors.append(f"{subj}: years {YEARS[i]}/{YEARS[j]} share {len(overlap)} questions")

    report["total_files"] = len(report["files"])
    report["total_questions"] = total_questions
    report["validation_errors"] = errors
    report["real_files_hashed"] = real_files
    report["real_questions_hashed"] = len(real_hashes)
    with open(REPORT, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)

    print(f"\nFiles written: {len(report['files'])}, total questions: {total_questions}")
    if errors:
        print(f"VALIDATION ERRORS ({len(errors)}):")
        for e in errors[:50]:
            print("  -", e)
        sys.exit(1)
    print("Validation passed: all files parse, counts match, no duplicates, "
          "no cross-year overlap, no real-file matches, every question has "
          "4 distinct options, practice:true, source, topic, explanation, adapted_from.")
    print(f"Report: {REPORT}")


if __name__ == "__main__":
    main()
