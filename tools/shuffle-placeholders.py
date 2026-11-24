#!/usr/bin/env python3
"""Deterministic answer-position shuffle for MyStudy filled placeholder files.

Seed: base string "mystudy-shuffle-v1" + per-file SHA-256 of the filename.
Only files where at least one real question has practice:true are touched.
Only `opts` order and `ans` change; q text, explanation, source, practice,
type and passage content are untouched.

Per file, target answer counts are as equal as possible (n=40 -> 10/10/10/10,
n=50 -> 13/13/12/12 with the +1s going to the two indices first in a seeded
order, n=60 -> 15/15/15/15). Target positions are assigned to questions in
seeded-shuffled order, then each question's options are permuted with the
correct option swapped into its assigned position.
"""
import hashlib
import json
import pathlib
import random

BASE_SEED = "mystudy-shuffle-v1"
BASE = pathlib.Path.home() / "workspace/mystudy/data-repos/Exam-Questions-Data/json"


def real_questions(items):
    """Yield (container, index, question) so nested passage/poem questions
    are shuffled individually but stay attached to their container."""
    for i, it in enumerate(items):
        if isinstance(it, dict) and isinstance(it.get("questions"), list):
            for j, q in enumerate(it["questions"]):
                yield (it["questions"], j, q)
        elif isinstance(it, dict):
            yield (items, i, it)


def shuffle_file(path: pathlib.Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    qs = list(real_questions(data))
    practice = [q for _, _, q in qs if q.get("practice") is True]
    if not practice:
        return None
    assert len(practice) == len(qs), f"{path.name}: non-practice question in placeholder file"
    n = len(qs)
    # Per-file deterministic RNG: SHA-256 of base seed + filename (stable across runs)
    seed_int = int(hashlib.sha256(f"{BASE_SEED}:{path.name}".encode()).hexdigest()[:16], 16)
    rng = random.Random(seed_int)
    # Target counts as equal as possible; remainder goes to indices first in seeded order
    counts = [n // 4] * 4
    order = list(range(4))
    rng.shuffle(order)
    for k in range(n % 4):
        counts[order[k]] += 1
    targets = []
    for idx, c in enumerate(counts):
        targets.extend([idx] * c)
    rng.shuffle(targets)
    assert len(targets) == n
    for (container, idx, q), target in zip(qs, targets):
        opts = list(q["opts"])
        assert len(opts) == 4 and len(set(map(str, opts))) == 4
        correct = opts[q["ans"]]
        distractors = [o for i, o in enumerate(opts) if i != q["ans"]]
        rng.shuffle(distractors)
        # Build a permutation: place distractors in random order, correct at target
        new_opts = [None] * 4
        new_opts[target] = correct
        di = 0
        for i in range(4):
            if new_opts[i] is None:
                new_opts[i] = distractors[di]
                di += 1
        assert sorted(map(str, new_opts)) == sorted(map(str, opts))
        q["opts"] = new_opts
        q["ans"] = target
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"file": path.name, "n": n, "counts": counts, "seed": f"{BASE_SEED}:{path.name}"}


def main():
    changed = []
    for path in sorted(BASE.glob("*.json")):
        result = shuffle_file(path)
        if result:
            changed.append(result)
    print(f"shuffled {len(changed)} files, {sum(r['n'] for r in changed)} questions")
    for r in changed:
        print(r["file"], r["n"], r["counts"])


if __name__ == "__main__":
    main()
