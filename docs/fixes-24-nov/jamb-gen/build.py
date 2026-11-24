"""Build all 22 JAMB placeholder files from gen1-gen8, validate, write."""
import sys, json, os
sys.path.insert(0, "/home/hatch/workspace/mystudy/docs/fixes-24-nov/jamb-gen")
from common import build, build_passage, build_poem, count_questions, validate, load_real_hashes, write_file, SRC2020, SRC2023
import gen1, gen2, gen3, gen4, gen5, gen6, gen7, gen8

OUT = "/home/hatch/workspace/mystudy/data-repos/Exam-Questions-Data/json"
real_hashes = load_real_hashes(OUT)
print(f"real-file question hashes loaded: {len(real_hashes)}")

files = {}
files["JAMB_Accounting_2020.json"] = build(gen1.ACCOUNTING, SRC2020)
files["JAMB_Agric_2020.json"] = build(gen1.AGRIC, SRC2020)
files["JAMB_Biology_2020.json"] = build(gen1.BIOLOGY, SRC2020)
files["JAMB_CRS_2020.json"] = build(gen2.CRS, SRC2020)
files["JAMB_Chemistry_2020.json"] = build(gen2.CHEMISTRY, SRC2020)
files["JAMB_Civic_2020.json"] = build(gen2.CIVIC, SRC2020)
files["JAMB_Commerce_2020.json"] = build(gen3.COMMERCE, SRC2020)
files["JAMB_Computer_2020.json"] = build(gen3.COMPUTER, SRC2020)
files["JAMB_Economics_2020.json"] = build(gen3.ECONOMICS, SRC2020)
files["JAMB_English_2020.json"] = [
    build_passage(*gen4.ENG_PASSAGE_COMP, SRC2020),
    build_passage(*gen4.ENG_PASSAGE_SUMMARY, SRC2020),
    build_passage(*gen4.ENG_PASSAGE_CLOZE, SRC2020),
] + build(gen4.ENGLISH_STD, SRC2020)
files["JAMB_FurtherMath_2020.json"] = build(gen5.FURTHERMATH, SRC2020)
files["JAMB_Geography_2020.json"] = build(gen5.GEOGRAPHY, SRC2020)
files["JAMB_Government_2020.json"] = build(gen5.GOVERNMENT, SRC2020)
files["JAMB_Hausa_2020.json"] = build(gen6.HAUSA_2020, SRC2020)
files["JAMB_Hausa_2023.json"] = build(gen6.HAUSA_2023, SRC2023)
files["JAMB_History_2020.json"] = build(gen6.HISTORY, SRC2020)
files["JAMB_IRS_2020.json"] = build(gen7.IRS, SRC2020)
files["JAMB_Igbo_2020.json"] = build(gen7.IGBO, SRC2020)
files["JAMB_Literature_2020.json"] = [
    build_poem(*gen4.LIT_POEM, SRC2020),
    build_passage(*gen4.LIT_PASSAGE, SRC2020),
] + build(gen4.LITERATURE_STD, SRC2020)
files["JAMB_Mathematics_2020.json"] = build(gen7.MATHEMATICS, SRC2020)
files["JAMB_Physics_2020.json"] = build(gen8.PHYSICS, SRC2020)
files["JAMB_Yoruba_2020.json"] = build(gen8.YORUBA, SRC2020)

report = []
total = 0
all_ok = True
for name, data in files.items():
    n = count_questions(data)
    errors, nq = validate(data, real_hashes)
    assert n == nq
    total += n
    status = "OK" if not errors else "FAIL"
    if errors:
        all_ok = False
    report.append((name, n, errors))
    print(f"{name}: {n} questions — {status}")
    for e in errors:
        print("   ERROR:", e)
print(f"TOTAL questions: {total}")
print("ALL VALID" if all_ok else "ERRORS PRESENT — not writing")
if all_ok:
    for name, data in files.items():
        write_file(os.path.join(OUT, name), data)
    print("Wrote all 22 files.")
json.dump({"total": total, "files": [{"name": n, "questions": q, "errors": e} for n, q, e in report]},
          open("/home/hatch/workspace/mystudy/docs/fixes-24-nov/jamb-gen/build-report.json", "w"), ensure_ascii=False, indent=2)
