#!/usr/bin/env python3
"""Read-only audit of /tmp/mystudy-repos/vocabulary-database/
Writes /tmp/vocab_audit.json + prints summary. Persisted copy:
~/workspace/mystudy/tools/vocab_audit.py
"""
import json, os, re, collections, sys

BASE = "/tmp/mystudy-repos/vocabulary-database"
files = sorted(f for f in os.listdir(BASE) if f.endswith(".json") and f != "index.json")

STOP = set("""a an the of to be one ones do not it its in on for and or who will can more than you your
is are was were has have had he she they we i me him her his their our this that these those with by at from as
""".split())
PLACEHOLDER = re.compile(r"\b(todo|lorem|placeholder|tbd|xxx)\b|\?\?\?", re.I)

def _toks(text):
    """Unicode-aware word tokens; an apostrophe-joined match also yields its
    parts (Igbo "n'ụlọ" -> "n'ụlọ", "n", "ụlọ"), so a word can match either
    the joined form or a part, while "someone's" stays intact for the
    possessive-placeholder check."""
    out = []
    for m in re.findall(r"(?:[^\W\d_]|')+", str(text or "").lower()):
        out.append(m)
        if "'" in m:
            out.extend(p for p in m.split("'") if p)
    return out

def base_tokens(word):
    """Content tokens of a word, parenthetical qualifiers stripped."""
    w = re.sub(r"\(.*?\)", " ", str(word or ""))
    toks = _toks(w)
    return [t for t in toks if t not in STOP and len(t) > 1]

IRREG = {"get": {"got", "gets", "getting"}, "go": {"went", "goes", "going"},
         "bite": {"bit", "bitten", "biting"}, "take": {"took", "taken", "taking"}}
POSSESSIVES = {"my", "your", "his", "her", "its", "our", "their"}

def example_ok(word, example):
    """True if every content token of word appears in example allowing
    3-letter stem match (covers inflections: bit/bite, burned/burn,
    contemporaries/contemporary, polytheistic/polytheism, estuaries/estuary),
    irregular pasts (get/got, go/went), and pronoun placeholders
    (someone's/one's satisfied by any possessive pronoun)."""
    toks = base_tokens(word)
    if not toks:
        return True, []
    ex_toks = _toks(example)
    missing = []
    for t in toks:
        if t in ("someone's", "one's", "someone", "one") and any(e in POSSESSIVES for e in ex_toks):
            continue
        stem = t[:3]
        if any(e[:3] == stem or e.startswith(t) or t.startswith(e) for e in ex_toks):
            continue
        if t in IRREG and any(e in IRREG[t] for e in ex_toks):
            continue
        missing.append(t)
    return (not missing), missing

report = {"files": {}}
all_words = []
all_ids = collections.Counter()
defects = []
quiz_defects = []
word_by_file = {}
quiz_by_file = {}

for fn in files:
    with open(os.path.join(BASE, fn)) as f:
        data = json.load(f)
    words = data.get("words", [])
    quiz = data.get("quiz", [])
    # Nigerian-language categories carry one-word English glosses
    # ("Tea.", "Who.") — complete and correct; 4-char minimum applies
    min_def = 4 if data.get("category") in ("hausa", "igbo", "yoruba") else 10
    word_by_file[fn] = words
    quiz_by_file[fn] = quiz
    id_prefixes = collections.Counter()
    for w in words:
        m = re.match(r"^([a-z]+)-", w.get("id", ""))
        id_prefixes[m.group(1) if m else "?"] += 1
    qid_prefixes = collections.Counter()
    for q in quiz:
        m = re.match(r"^([a-z]+)-", q.get("id", ""))
        qid_prefixes[m.group(1) if m else "?"] += 1
    wid_counts = collections.Counter(w.get("id") for w in words)
    dup_ids = {k: v for k, v in wid_counts.items() if v > 1}
    qid_counts = collections.Counter(q.get("id") for q in quiz)
    dup_qids = {k: v for k, v in qid_counts.items() if v > 1}
    w_exact = collections.Counter(w.get("word", "") for w in words)
    dup_exact = {k: v for k, v in w_exact.items() if v > 1}
    w_ci = collections.Counter((w.get("word", "") or "").strip().lower() for w in words)
    dup_ci = {k: v for k, v in w_ci.items() if v > 1}
    # duplicate definitions (normalised)
    dnorm = collections.Counter(re.sub(r"\s+", " ", str(w.get("definition", "")).strip().lower().rstrip(".")) for w in words)
    dup_defs = {k: v for k, v in dnorm.items() if v > 1}
    # quiz id number format
    qid_nums = [re.match(r"^[a-z]+-q(\d+)$", q.get("id", "")) for q in quiz]
    report["files"][fn] = {
        "category": data.get("category"), "title": data.get("title"),
        "n_words": len(words), "n_quiz": len(quiz),
        "word_keys": sorted({tuple(sorted(w.keys())) for w in words}),
        "quiz_keys": sorted({tuple(sorted(q.keys())) for q in quiz}),
        "word_id_prefixes": dict(id_prefixes), "quiz_id_prefixes": dict(qid_prefixes),
        "dup_word_ids": dup_ids, "dup_quiz_ids": dup_qids,
        "dup_words_exact": dup_exact, "dup_words_ci": dup_ci,
        "dup_definitions": dup_defs,
        "extra_top_keys": sorted(set(data.keys()) - {"category", "title", "words", "quiz"}),
        "quiz_id_numbered": all(bool(m) for m in qid_nums),
    }
    for w in words:
        all_ids[w.get("id")] += 1
        all_words.append((fn, w))
        wid, word, pos = w.get("id", "?"), w.get("word"), w.get("pos")
        defin, ex = w.get("definition"), w.get("example")
        if not word or not str(word).strip():
            defects.append((fn, wid, word, "missing/empty word"))
        if not pos or not str(pos).strip():
            defects.append((fn, wid, word, "missing/empty pos"))
        if not defin or not str(defin).strip():
            defects.append((fn, wid, word, "missing/empty definition"))
        else:
            d = str(defin).strip()
            if len(d) < min_def:
                defects.append((fn, wid, word, f"definition too short ({len(d)} chars): {d!r}"))
            if PLACEHOLDER.search(d):
                defects.append((fn, wid, word, f"placeholder definition: {d!r}"))
            if word and d.lower().rstrip(".") == str(word).lower().strip():
                defects.append((fn, wid, word, "circular definition (definition == word)"))
        if not ex or not str(ex).strip():
            defects.append((fn, wid, word, "missing/empty example"))
        elif word:
            ok, missing = example_ok(word, ex)
            if not ok:
                defects.append((fn, wid, word, f"example lacks word part(s) {missing}: {str(ex)!r}"))
    stems = collections.Counter()
    for idx, q in enumerate(quiz):
        qid = q.get("id", f"index-{idx}")
        stem, opts, ans, expl = q.get("question"), q.get("options"), q.get("answer"), q.get("explanation")
        if not stem or not str(stem).strip():
            quiz_defects.append((fn, qid, idx, "broken/empty stem"))
        else:
            stems[str(stem).strip()] += 1
        if not isinstance(opts, list):
            quiz_defects.append((fn, qid, idx, "options missing/not a list"))
            opts = []
        else:
            if len(opts) != 4:
                quiz_defects.append((fn, qid, idx, f"options count = {len(opts)} (expected 4)"))
            if len(set(str(o).strip().lower() for o in opts)) != len(opts):
                quiz_defects.append((fn, qid, idx, f"duplicate options: {opts}"))
            if any(not str(o).strip() for o in opts):
                quiz_defects.append((fn, qid, idx, "empty option present"))
        if ans is None:
            quiz_defects.append((fn, qid, idx, "missing answer"))
        elif not isinstance(ans, int) or isinstance(ans, bool):
            quiz_defects.append((fn, qid, idx, f"answer not an integer: {ans!r}"))
        elif not opts or not (0 <= ans < len(opts)):
            quiz_defects.append((fn, qid, idx, f"answer out of range: {ans} (options={len(opts)})"))
        if stem and isinstance(opts, list) and isinstance(ans, int) and 0 <= ans < len(opts):
            m = re.search(r'Which word means:\s*"(.*?)"\?', str(stem))
            if m:
                defin = m.group(1).strip()
                match_words = [w.get("word") for w in words
                               if str(w.get("definition", "")).strip().rstrip(".") == defin.rstrip(".")
                               or str(w.get("definition", "")).strip() == defin]
                if match_words:
                    expected = match_words[0]
                    if str(opts[ans]).strip() != str(expected).strip():
                        quiz_defects.append((fn, qid, idx,
                            f"answer mismatch: stem is definition of {expected!r} but answer index {ans} points to {opts[ans]!r}"))
                    if str(expected).strip() not in [str(o).strip() for o in opts]:
                        quiz_defects.append((fn, qid, idx,
                            f"correct word {expected!r} not among options"))
                else:
                    quiz_defects.append((fn, qid, idx,
                        f"stem definition matches no word in this file: {defin!r}"))
            else:
                quiz_defects.append((fn, qid, idx, f"stem does not match 'Which word means: ...?' pattern: {str(stem)[:80]!r}"))
        if not expl or not str(expl).strip():
            quiz_defects.append((fn, qid, idx, "missing/empty explanation"))
    for stem, c in stems.items():
        if c > 1:
            quiz_defects.append((fn, "dup-stem", -1, f"duplicate stem x{c}: {stem[:100]!r}"))

by_word_ci = collections.defaultdict(list)
for fn, w in all_words:
    by_word_ci[(w.get("word") or "").strip().lower()].append((fn, w.get("id"), w.get("definition")))
shared = {k: v for k, v in by_word_ci.items() if len({f for f, _, _ in v}) > 1}
same_sense, diff_sense = {}, {}
for k, v in shared.items():
    defs = {re.sub(r"\s+", " ", str(d or "").strip().lower().rstrip(".")) for _, _, d in v}
    (same_sense if len(defs) == 1 else diff_sense)[k] = v

# global id collisions: words and quiz separately and combined
all_qids = collections.Counter()
for fn, qs in quiz_by_file.items():
    for q in qs:
        all_qids[q.get("id")] += 1

report["defects"] = defects
report["quiz_defects"] = quiz_defects
report["dup_ids_global_words"] = {k: v for k, v in all_ids.items() if v > 1}
report["dup_ids_global_quiz"] = {k: v for k, v in all_qids.items() if v > 1}
report["shared_words"] = {k: v for k, v in shared.items()}
report["same_sense"] = {k: v for k, v in same_sense.items()}
report["diff_sense"] = {k: v for k, v in diff_sense.items()}
report["total_words"] = len(all_words)
report["total_quiz"] = sum(len(q) for q in quiz_by_file.values())

with open("/tmp/vocab_audit.json", "w") as f:
    json.dump(report, f, indent=2, default=str)

print("FILES:", len(files))
print("TOTAL WORDS:", report["total_words"], "| TOTAL QUIZ:", report["total_quiz"])
print("\n== per-file ==")
for fn, r in report["files"].items():
    print(f"{fn}: words={r['n_words']} quiz={r['n_quiz']} word_pref={r['word_id_prefixes']} quiz_pref={r['quiz_id_prefixes']} "
          f"dup_ids={r['dup_word_ids']} dup_qids={r['dup_quiz_ids']} dup_words={r['dup_words_exact']} "
          f"dup_defs={r['dup_definitions']} quiz_numbered={r['quiz_id_numbered']}")
print("\n== entry defects:", len(defects), "==")
for d in defects:
    print(d)
print("\n== quiz defects:", len(quiz_defects), "==")
for d in quiz_defects:
    print(d)
print("\n== duplicate word ids globally:", report["dup_ids_global_words"])
print("== duplicate quiz ids globally:", report["dup_ids_global_quiz"])
print("\n== shared words cross-category:", len(shared), "| same-sense:", len(same_sense), "| diff-sense:", len(diff_sense))
print("SAME-SENSE:", sorted(same_sense.keys()))
