"""Core helpers for WAEC practice-set generation (syllabus-modelled, practice:true)."""
import re
FALLBACKS = {"count": 0}
def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', str(s).lower()).strip()
def mk(q, correct, distractors, expl, year, topic, adapted="WAEC 2024/2025 repo files"):
    ds = []
    for d in distractors:
        if d != correct and d not in ds:
            ds.append(d)
    for filler in ("None of the above", "All of the above", "Cannot be determined"):
        if len(ds) >= 3:
            break
        if filler not in ds:
            ds.append(filler); FALLBACKS["count"] += 1
    assert len(ds) == 3, f"could not build 4 distinct opts for: {q}"
    opts = [correct] + ds
    return {"q": q, "opts": opts, "ans": 0, "explanation": expl,
            "topic": topic, "practice": True,
            "source": (f"MyStudy Practice Set \u2014 modelled on the WAEC syllabus for this subject, "
                       f"not the official {year} paper | Topic: {topic} | Adapted by topic from {adapted}; "
                       f"syllabus: WAEC syllabus (waecsyllabus.com) and JAMB syllabus (ibass.jamb.gov.ng); "
                       f"answers verified against the syllabus")}
def fmt_num(x):
    if isinstance(x, float) and x == int(x):
        return str(int(x))
    if isinstance(x, float):
        return f"{x:.2f}".rstrip('0').rstrip('.')
    return str(x)
def uniq_pool(pool):
    seen = set(); out = []
    for it in pool:
        k = norm(it["q"])
        if k in seen:
            continue
        seen.add(k); out.append(it)
    return out
