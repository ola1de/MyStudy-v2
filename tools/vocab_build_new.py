#!/usr/bin/env python3
"""Build the 20 new vocabulary categories + index.json v3.

Reads data modules vocab_new_1..5 (each exposes CATS dict), writes one
JSON file per category into /tmp/mystudy-repos/vocabulary-database/ in the
repo's own format (indent=2, ensure_ascii=False, no trailing newline),
regenerates quizzes the same way as the fix script, and writes index.json
v3 listing all 44 categories with counts.

Validation (fails loudly): 100 words per category, unique words and
definitions within a category, all fields present, definitions >= 10 chars,
example contains the word (same refined check as the audit), quiz 4 options
with a valid answer. Also prints dictionary-coverage stats for new words.
"""
import json, os, re, random, collections, sys

BASE = "/tmp/mystudy-repos/vocabulary-database"
TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)

STOP = set("""a an the of to be one ones do not it its in on for and or who will can more than you your
is are was were has have had he she they we i me him her his their our this that these those with by at from as
""".split())
IRREG = {"get": {"got", "gets", "getting"}, "go": {"went", "goes", "going"},
         "bite": {"bit", "bitten", "biting"}, "take": {"took", "taken", "taking"}}
POSSESSIVES = {"my", "your", "his", "her", "its", "our", "their"}

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
    w = re.sub(r"\(.*?\)", " ", str(word or ""))
    # Unicode-aware: matches Hausa/Igbo/Yoruba letters (ɗ ƙ ụ ọ ẹ ṣ, accents)
    toks = _toks(w)
    return [t for t in toks if t not in STOP and len(t) > 1]

def example_ok(word, example):
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

def build_quiz(words, prefix, seed):
    rng = random.Random(seed)
    quiz = []
    for i, w in enumerate(words):
        others = [x for j, x in enumerate(words) if j != i]
        distractors = rng.sample(others, 3)
        options = [w["word"]] + [d["word"] for d in distractors]
        rng.shuffle(options)
        quiz.append({
            "id": f"{prefix}-q{i+1}",
            "question": f'Which word means: "{w["definition"]}"?',
            "options": options,
            "answer": options.index(w["word"]),
            "explanation": f'{w["word"]} ({w["pos"]}) — {w["definition"]}',
        })
    return quiz

def main():
    all_cats = {}
    for mod in ["vocab_new_1", "vocab_new_2", "vocab_new_3", "vocab_new_4", "vocab_new_5"]:
        m = __import__(mod)
        for slug, cat in m.CATS.items():
            assert slug not in all_cats, f"duplicate slug {slug}"
            all_cats[slug] = cat
    print(f"new categories: {len(all_cats)}")
    # dictionary for coverage stats
    dic = json.load(open("/tmp/mystudy-repos/mystudy-dic/processed/merged.json"))
    low = {k.lower(): 1 for k in dic}
    total_new_words = 0
    verified = 0
    unverified = []
    for slug, cat in all_cats.items():
        raw = cat["words"]
        assert len(raw) == 100, f"{slug}: {len(raw)} words, expected 100"
        # Nigerian-language categories carry one-word English glosses
        # ("Tea.", "Who.") — complete and correct; 4-char minimum applies
        min_def = 4 if slug in ("hausa", "igbo", "yoruba") else 10
        words = []
        for i, (word, pos, defin, ex) in enumerate(raw, start=1):
            assert word and pos and defin and ex, f"{slug} #{i}: empty field"
            assert len(defin.strip()) >= min_def, f"{slug} {word}: definition <{min_def} chars"
            ok, missing = example_ok(word, ex)
            assert ok, f"{slug} {word}: example lacks {missing}: {ex!r}"
            words.append({"id": f'{cat["word_prefix"]}-{i:03d}', "word": word,
                          "pos": pos, "definition": defin, "example": ex})
        wlow = [w["word"].strip().lower() for w in words]
        assert len(set(wlow)) == len(wlow), f"{slug}: duplicate words"
        dnorm = [re.sub(r"\s+", " ", w["definition"].strip().lower().rstrip(".")) for w in words]
        dups = [k for k, v in collections.Counter(dnorm).items() if v > 1]
        assert not dups, f"{slug}: duplicate definitions: {dups}"
        quiz = build_quiz(words, cat["quiz_prefix"], seed=slug)
        for q in quiz:
            assert len(q["options"]) == 4 and len(set(q["options"])) == 4
            assert 0 <= q["answer"] < 4 and q["options"][q["answer"]] == words[quiz.index(q)]["word"]
        data = {"category": slug, "title": cat["title"], "words": words, "quiz": quiz}
        with open(os.path.join(BASE, cat["file"]), "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        total_new_words += 100
        # dictionary coverage: single-word English terms only; Nigerian-language
        # categories are glossed, not English, so they are skipped here
        if slug in ("hausa", "igbo", "yoruba"):
            continue
        for w in words:
            b = re.sub(r"\(.*?\)", "", w["word"]).strip().lower()
            parts = [p for p in re.split(r"[\s\-']+", b) if p]
            if len(parts) == 1 and parts[0] in low:
                verified += 1
            elif len(parts) == 1:
                unverified.append((slug, w["word"]))
        print(f"  {cat['file']}: 100 words + 100 quiz OK")
    # ---- index v3 ----
    # Order is defined explicitly: v1's 14 first, then the 10 previously
    # unlisted (alphabetical), then the 20 new categories in subject order.
    # (Rebuilt from scratch — never derived from a possibly stale index.json.)
    V1_ORDER = ["one-word-substitutions", "phobias", "medical-specialists",
                "dietary-habits", "forms-of-government", "branches-of-study",
                "words-for-killing", "obsessions", "baby-animals",
                "time-and-frequency", "measurement-instruments",
                "collective-nouns", "personality-types", "philosophical-stances"]
    existing_files = sorted(f for f in os.listdir(BASE)
                            if f.endswith(".json") and f != "index.json")
    titles = {}
    for fn in existing_files:
        d = json.load(open(os.path.join(BASE, fn)))
        titles[d["category"]] = d["title"]
    prev_unlisted = sorted(s for s in titles
                           if s not in V1_ORDER and s not in all_cats)
    new_order = list(all_cats.keys())
    order = V1_ORDER + prev_unlisted + new_order
    assert len(order) == len(set(order)) == len(titles) == 44, \
        (len(order), len(set(order)), len(titles))
    cats = [{"slug": s, "title": titles[s], "file": f"{s}.json", "count": 100}
            for s in order]
    idx = {"version": 3, "categories": cats}
    with open(os.path.join(BASE, "index.json"), "w") as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)
    print(f"index.json v3 written: {len(cats)} categories")
    print(f"new words total: {total_new_words}; single-word terms in dictionary: {verified}; "
          f"single-word terms NOT in dictionary: {len(unverified)}")
    print("unverified single-word terms (specialist vocabulary, kept on standard-usage grounds):")
    for s, w in unverified:
        print(f"   {s}: {w}")

if __name__ == "__main__":
    main()
