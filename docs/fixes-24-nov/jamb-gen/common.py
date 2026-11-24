"""Shared helpers for JAMB practice-set generation (syllabus-sourced)."""
import json, re, unicodedata, os

SRC2020 = "MyStudy Practice Set — modelled on the JAMB syllabus for this subject, not the official 2020 paper"
SRC2023 = "MyStudy Practice Set — modelled on the JAMB syllabus for this subject, not the official 2023 paper"

# adaptation provenance codes -> note text
ADAPT = {
    "R": "Adapted by topic/pattern from JAMB 2021-2025 past questions in repo (wording changed, not copied verbatim)",
    "M": "Adapted by topic/pattern from JAMB Master archive 1983-2020 (jamb-master.web.app; wording changed, not copied verbatim)",
    "N": "New syllabus-modelled item",
}

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]", "", s.lower())).strip()

def src_str(base, topic, adapt):
    s = base + " | Syllabus topic: " + topic
    if adapt:
        s += " | " + ADAPT.get(adapt, adapt)
    return s

def Q(q, opts, ans, expl, topic, adapt="R"):
    """One question tuple: (q, opts, ans, expl, topic, adapt-code)."""
    return (q, list(opts), ans, expl, topic, adapt)

def build(qs, base):
    """qs: list of Q() tuples. Returns list of std dicts."""
    out = []
    for q, opts, ans, expl, topic, adapt in qs:
        d = {"type": "std", "q": q, "opts": list(opts), "ans": ans,
             "practice": True, "source": src_str(base, topic, adapt)}
        if expl:
            d["explanation"] = expl
        out.append(d)
    return out

def build_passage(content, qs, base):
    return {"type": "passage", "content": content,
            "questions": [{"q": q, "opts": list(o), "ans": a, "practice": True,
                           "source": src_str(base, t, ad),
                           **({"explanation": e} if e else {})}
                          for q, o, a, e, t, ad in qs]}

def build_poem(content, qs, base):
    p = build_passage(content, qs, base)
    p["type"] = "poem"
    return p

def count_questions(data):
    n = 0
    for x in data:
        n += len(x["questions"]) if x.get("type") in ("passage", "poem") else 1
    return n

def validate(data, real_hashes):
    errors = []
    seen = set()
    flat = []
    for x in data:
        qs = x["questions"] if x.get("type") in ("passage", "poem") else [x]
        for q in qs:
            flat.append(q)
            if len(q.get("opts", [])) != 4:
                errors.append(f"opts!=4: {q.get('q','')[:60]}")
            if len(set(q.get("opts", []))) != 4:
                errors.append(f"duplicate opts: {q.get('q','')[:60]}")
            a = q.get("ans")
            if not isinstance(a, int) or a not in (0, 1, 2, 3):
                errors.append(f"bad ans: {q.get('q','')[:60]}")
            if not q.get("practice") or not q.get("source"):
                errors.append(f"missing labelling: {q.get('q','')[:60]}")
            if "Syllabus topic:" not in q.get("source", ""):
                errors.append(f"missing syllabus topic: {q.get('q','')[:60]}")
            h = norm(q.get("q", ""))
            if h in seen:
                errors.append(f"internal duplicate: {q.get('q','')[:60]}")
            seen.add(h)
            if h in real_hashes:
                errors.append(f"VERBATIM MATCH vs real file: {q.get('q','')[:60]}")
    return errors, len(flat)

def load_real_hashes(jsondir):
    import glob
    hs = set()
    for f in glob.glob(os.path.join(jsondir, "JAMB_*_202[1-5].json")):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        for x in d:
            qs = x["questions"] if x.get("type") in ("passage", "poem") else [x]
            for q in qs:
                hs.add(norm(q.get("q", "")))
    return hs

def write_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
