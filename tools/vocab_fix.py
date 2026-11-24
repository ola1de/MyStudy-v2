#!/usr/bin/env python3
"""Fix the 24 existing vocabulary files in /tmp/mystudy-repos/vocabulary-database/.

Applies: duplicate-word replacements, wrong-definition fixes, the
baby-animals restructure (full-sentence definitions), duplicate-definition
disambiguation, fragment-definition expansion, phobias id rename
(ph-01..50 -> pho-01..50, fixing the global id collision), and full quiz
regeneration (stem = definition, 3 distractors, seeded shuffle).
Writes files back in the repo's own format (indent=2, ensure_ascii=False,
no trailing newline). Run AFTER reading the audit; run the validator after.
"""
import json, os, re, random, collections, sys

BASE = "/tmp/mystudy-repos/vocabulary-database"

def load(fn):
    with open(os.path.join(BASE, fn)) as f:
        return json.load(f)

def save(fn, data):
    with open(os.path.join(BASE, fn), "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def quiz_prefix(data):
    m = re.match(r"^([a-z]+)-q\d+$", data["quiz"][0]["id"])
    return m.group(1)

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

# ---------------------------------------------------------------- fixes
# file -> id -> fields to set (word/pos/definition/example)
FIXES = {
"animal-habitats.json": {
    "ah-012": {"definition": "A shed or building where cows are kept."},
    "ah-057": {"definition": "A mound or nest built by termites."},
    "ah-063": {"definition": "The burrow of a badger."},
    "ah-071": {"example": "The squirrel's drey sat high in the oak's crown."},
    "ah-072": {"definition": "The nest of a squirrel, built high in a tree."},
    "ah-095": {"definition": "The den of an otter, usually by a riverbank."},
},
"branches-of-study.json": {
    "bos-056": {"definition": "The scientific study of bees."},
    "bos-058": {"definition": "The scientific study of Mars and its surface."},
    "bos-067": {"definition": "The scientific study of dogs."},
    "bos-069": {"definition": "The branch of medicine that studies the skin."},
},
"capability-adjectives.json": {
    "ca-003": {"definition": "Safe to drink; fit for human consumption."},
    "ca-004": {"definition": "Suitable to drink, especially pleasant in taste."},
    "ca-035": {"word": "Ignitable", "pos": "adjective",
               "definition": "Capable of being set on fire.",
               "example": "The ignitable vapour needed careful handling."},
},
"collective-nouns.json": {
    "cn-22": {"definition": "A group of eagles; also called an aerie."},
    "cn-27": {"definition": "A group of bears; also called a sloth."},
    "cn-28": {"definition": "A group of foxes; also called a leash."},
    "cn-30": {"definition": "A group of hedgehogs; also called an array."},
    "cn-37": {"definition": "A group of zebras; also called a dazzle."},
    "cn-38": {"definition": "A group of zebras; also called a zeal."},
    "cn-39": {"definition": "A group of tigers; also called a streak."},
    "cn-40": {"definition": "A group of tigers; also called an ambush."},
    "cn-061": {"definition": "A group of ants living together in a nest."},
    "cn-068": {"definition": "A group of otters; also called a romp."},
    "cn-073": {"definition": "A group of cats, especially when staring together."},
    "cn-076": {"definition": "A group of bees living in a hive."},
    "cn-086": {"definition": "A group of elephants on the move; a parade."},
},
"dietary-habits.json": {
    "dh-36": {"word": "Faster", "pos": "noun",
               "definition": "One who abstains from food, especially for religious reasons.",
               "example": "The faster broke the fast at sunset."},
    "dh-067": {"word": "Algivore", "pos": "noun",
               "definition": "One who feeds mainly on algae.",
               "example": "Algivores graze on the algae coating the rocks."},
    "dh-070": {"definition": "A person who eats poultry but no other meat."},
    "dh-071": {"definition": "An animal that eats fish."},
    "dh-079": {"definition": "Feeding on meat; meat-eating."},
    "dh-080": {"definition": "Feeding on plants; plant-eating."},
    "dh-082": {"definition": "Feeding on insects; insect-eating."},
    "dh-083": {"definition": "Feeding on fish; fish-eating."},
    "dh-084": {"word": "Planktivore", "pos": "noun",
               "definition": "One who feeds on plankton.",
               "example": "Planktivores drift through the water filtering plankton."},
    "dh-085": {"definition": "Feeding on grain and seeds."},
    "dh-086": {"word": "Vermivore", "pos": "noun",
               "definition": "One who eats worms.",
               "example": "Vermivores probe the soil for worms."},
    "dh-087": {"word": "Pantophagist", "pos": "noun",
               "definition": "One who eats all kinds of food.",
               "example": "The pantophagist sampled every dish on the menu."},
    "dh-088": {"word": "Florivore", "pos": "noun",
               "definition": "One who eats flowers.",
               "example": "Florivores nibble the petals of wildflowers."},
    "dh-089": {"word": "Omophagist", "pos": "noun",
               "definition": "One who eats raw flesh.",
               "example": "The omophagist tore at the raw meat."},
    "dh-090": {"word": "Gummivore", "pos": "noun",
               "definition": "One who feeds on tree gum and sap.",
               "example": "Gummivores lick the sap oozing from the bark."},
    "dh-091": {"word": "Baccivore", "pos": "noun",
               "definition": "One who eats berries.",
               "example": "Baccivores strip the bushes of berries."},
    "dh-092": {"word": "Graminivore", "pos": "noun",
               "definition": "One who eats grass.",
               "example": "Graminivores graze the open savanna."},
    "dh-094": {"word": "Ophiophagist", "pos": "noun",
               "definition": "One who eats snakes.",
               "example": "The ophiophagist swallowed the snake whole."},
},
"forms-of-government.json": {
    "fog-061": {"word": "Tetrarchy", "pos": "noun",
                "definition": "Rule by four people.",
                "example": "The Roman tetrarchy divided the empire among four rulers."},
    "fog-062": {"definition": "Rule by three people acting jointly."},
    "fog-065": {"definition": "Government based on the rule of law."},
    "fog-096": {"word": "Transitional government", "pos": "noun",
                "definition": "A temporary government that rules during a change from one system to another.",
                "example": "The transitional government prepared the country for elections."},
},
"idioms.json": {
    "id-007": {"definition": "Very rarely; almost never."},
    "id-028": {"definition": "To go to bed and sleep."},
    "id-029": {"definition": "In trouble or in a difficult situation."},
    "id-080": {"definition": "To begin studying seriously."},
},
"measurement-instruments.json": {
    "mi-053": {"example": "The ampere-hour meter tracked battery use."},
    "mi-054": {"definition": "An instrument that measures radiant energy by detecting tiny temperature changes."},
    "mi-070": {"example": "The laser rangefinder measured 500 metres."},
    "mi-077": {"definition": "An instrument that counts the steps a person takes."},
    "mi-084": {"definition": "An instrument that measures the intensity of radiant energy."},
},
"medical-specialists.json": {
    "ms-052": {"definition": "A specialist who tests and treats hearing and balance."},
    "ms-053": {"example": "The cardiac electrophysiologist implanted a pacemaker."},
    "ms-060": {"definition": "A specialist in the treatment of diabetes."},
    "ms-061": {"definition": "A surgeon who treats the ear, nose and throat."},
    "ms-064": {"example": "The gastroenterological surgeon operated on the stomach."},
    "ms-065": {"example": "See your general practitioner for a referral."},
    "ms-082": {"definition": "A surgeon who treats bones and joints."},
    "ms-084": {"definition": "A surgeon who operates on children."},
    "ms-091": {"example": "The reproductive endocrinologist began the IVF programme."},
    "ms-094": {"example": "The speech-language pathologist began stroke rehab."},
    "ms-095": {"example": "The sports medicine physician cleared him to play."},
    "ms-096": {"definition": "A surgeon who operates inside the chest."},
},
"obsessions.json": {
    "o-061": {"word": "Oniomania", "pos": "noun",
              "definition": "A compulsive urge to buy things; compulsive shopping.",
              "example": "Oniomania left her with debts and unworn clothes."},
    "o-066": {"word": "Phonomania", "pos": "noun",
              "definition": "An obsession with sounds or noise.",
              "example": "Phonomania made him collect every recording he could find."},
    "o-067": {"word": "Numismatomania", "pos": "noun",
              "definition": "An obsession with coins or money.",
              "example": "Numismatomania filled his house with rare coins."},
    "o-070": {"word": "Dinomania", "pos": "noun",
              "definition": "An excessive fascination with dinosaurs.",
              "example": "Dinomania filled his shelves with dinosaur models."},
    "o-071": {"word": "Pteridomania", "pos": "noun",
              "definition": "An obsessive craze for collecting ferns.",
              "example": "Victorian pteridomania filled parlours with ferns."},
    "o-072": {"word": "Ecdemomania", "pos": "noun",
              "definition": "An obsessive urge to wander away from home.",
              "example": "Ecdemomania drove him to leave home again and again."},
    "o-073": {"word": "Thanatomania", "pos": "noun",
              "definition": "A morbid obsession with death.",
              "example": "Thanatomania coloured all his writing."},
    "o-074": {"word": "Potomania", "pos": "noun",
              "definition": "An excessive craving for alcoholic drink.",
              "example": "Potomania ruined his health and career."},
    "o-075": {"definition": "An obsessive, compulsive drive to keep working."},
    "o-077": {"word": "Morphinomania", "pos": "noun",
              "definition": "A craving for morphine.",
              "example": "Morphinomania followed his injury and treatment."},
    "o-079": {"word": "Philomania", "pos": "noun",
              "definition": "An excessive, obsessive love.",
              "example": "Philomania made every friendship feel like romance."},
    "o-080": {"word": "Lexomania", "pos": "noun",
              "definition": "An obsession with words.",
              "example": "Lexomania filled his notebooks with word lists."},
    "o-082": {"definition": "An obsessive craving to travel and wander."},
    "o-084": {"word": "Polymania", "pos": "noun",
              "definition": "Mania directed at many things at once.",
              "example": "Polymania left him starting ten projects a day."},
    "o-085": {"word": "Hippomania", "pos": "noun",
              "definition": "An obsession with horses.",
              "example": "Hippomania made her spend every weekend at the stables."},
    "o-092": {"word": "Verbomania", "pos": "noun",
              "definition": "An obsession with words and talk.",
              "example": "Verbomania kept him talking long after midnight."},
    "o-094": {"word": "Audiomania", "pos": "noun",
              "definition": "An obsession with music and sound.",
              "example": "Audiomania filled his rooms with speakers."},
    "o-098": {"word": "Nomomania", "pos": "noun",
              "definition": "An obsession with names.",
              "example": "Nomomania made him memorise the name of everyone he met."},
},
"one-word-substitutions.json": {
    "ows-069": {"definition": "A person who walks in their sleep."},
},
"personality-types.json": {
    "pt-065": {"definition": "Eager to know or learn something."},
    "pt-067": {"word": "Dutiful", "pos": "adj",
               "definition": "Conscientious in doing one's duty.",
               "example": "The dutiful clerk filed every report on time."},
    "pt-084": {"definition": "Not depending on others; self-reliant."},
    "pt-091": {"definition": "Not boastful about one's abilities; humble."},
},
"philosophical-stances.json": {
    "ph-04": {"definition": "The belief that there is only one god."},
    "ph-05": {"definition": "The belief in many gods."},
    "ps-051": {"word": "Pessimism", "pos": "noun",
               "definition": "The belief that life is fundamentally bad, or that things will turn out badly.",
               "example": "Philosophical pessimism doubts that progress makes life better."},
    "ps-068": {"definition": "The view that free will and determinism can both be true."},
    "ps-085": {"definition": "An ethics based on reason and human welfare, without a deity."},
    "ps-088": {"definition": "The view that meaning and knowledge depend on what is in the mind."},
},
"phobias.json": {
    "ph-11": {"definition": "Fear of being alone or of oneself."},
    "p-054": {"word": "Didaskaleinophobia", "pos": "noun",
              "definition": "Fear of going to school.",
              "example": "Didaskaleinophobia kept the boy home on Mondays."},
    "p-055": {"word": "Athazagoraphobia", "pos": "noun",
              "definition": "Fear of being forgotten or of forgetting.",
              "example": "Athazagoraphobia made her call her mother daily."},
    "p-073": {"definition": "Fear of crowds and public gatherings."},
    "p-088": {"definition": "Fear of being alone; also called autophobia."},
    "p-098": {"definition": "Fear of falling asleep."},
},
"proverbs.json": {
    "pv-049": {"example": "It's better to be safe than sorry, so wear a helmet."},
    "pv-058": {"example": "People who live in glass houses shouldn't throw stones, so she should not judge."},
    "pv-037": {"definition": "Putting off today's work only makes tomorrow harder."},
    "pv-044": {"definition": "Waiting patiently is often rewarded in the end."},
    "pv-087": {"definition": "Keeping clean is almost as important as being good."},
    "pv-093": {"word": "No pain, no gain",
               "definition": "Suffering or hard effort is needed to achieve something worthwhile.",
               "example": "Training hurt, but no pain, no gain."},
},
"time-and-frequency.json": {
    "tf-12": {"definition": "Lasting only for a short time; not permanent."},
    "tf-13": {"definition": "Passing swiftly; here one moment and gone the next."},
    "tf-32": {"word": "Unremitting", "pos": "adj",
              "definition": "Never stopping or slackening.",
              "example": "The unremitting rain flooded the streets."},
    "taf-061": {"definition": "Occurring every six months."},
    "taf-071": {"definition": "The cycle of activity and rest over a single day."},
    "taf-087": {"definition": "Done in turn by different people or things."},
    "taf-096": {"word": "Evanescent", "pos": "adj",
                "definition": "Quickly fading from sight or memory.",
                "example": "Evanescent mist rose from the river."},
},
"words-for-killing.json": {
    "kl-43": {"example": "The hero will slay the dragon."},
    "wfk-077": {"word": "Avunculicide", "pos": "noun",
                "definition": "The killing of one's uncle.",
                "example": "Avunculicide appears in medieval chronicles."},
    "wfk-078": {"word": "Androcide", "pos": "noun",
                "definition": "The systematic killing of men.",
                "example": "Androcide has been documented in wartime."},
    "wfk-079": {"word": "Vitricide", "pos": "noun",
                "definition": "The killing of one's stepfather.",
                "example": "Vitricide is recorded in old legal codes."},
    "wfk-080": {"word": "Libericide", "pos": "noun",
                "definition": "The killing of one's children.",
                "example": "Libericide is a rare charge in criminal law."},
    "wfk-084": {"definition": "A person who kills, especially violently."},
    "wfk-086": {"definition": "A person who attacks another violently."},
    "wfk-099": {"word": "Decimation", "pos": "noun",
                "definition": "The killing of one in every ten people, or a drastic reduction in numbers.",
                "example": "The decimation of the legion was a Roman punishment."},
    "wfk-100": {"word": "Pogrom", "pos": "noun",
                "definition": "An organised massacre of a particular ethnic group.",
                "example": "The pogrom forced thousands to flee."},
},
"baby-animals.json": {
    "ba-39": {"word": "Cria"},
    "ba-051": {"word": "Alevin", "pos": "noun",
               "definition": "A newly hatched fish, still carrying its yolk sac.",
               "example": "The alevins hid among the gravel."},
    "ba-052": {"definition": "A young ant."},
},
}

# baby-animals ba-053..ba-100: animal -> term phrase (with article)
BABY_TERMS = {
    "ba-053": ("beaver", "a kit"), "ba-054": ("bear", "a cub"),
    "ba-055": ("camel", "a calf"), "ba-056": ("chimp", "an infant"),
    "ba-057": ("coyote", "a pup"), "ba-058": ("crocodile", "a hatchling"),
    "ba-059": ("dolphin", "a calf"), "ba-060": ("dove", "a squab"),
    "ba-061": ("eel", "an elver"), "ba-062": ("ferret", "a kit"),
    "ba-063": ("fox", "a kit or a cub"), "ba-064": ("giraffe", "a calf"),
    "ba-065": ("goat", "a kid"), "ba-066": ("gorilla", "an infant"),
    "ba-067": ("grouse", "a cheeper"), "ba-068": ("hare", "a leveret"),
    "ba-069": ("hedgehog", "a hoglet"), "ba-070": ("heron", "a chick"),
    "ba-071": ("hyena", "a cub"), "ba-072": ("jellyfish", "an ephyra"),
    "ba-073": ("kangaroo", "a joey"), "ba-074": ("koala", "a joey"),
    "ba-075": ("leopard", "a cub"), "ba-076": ("lion", "a cub"),
    "ba-077": ("llama", "a cria"), "ba-078": ("monkey", "an infant"),
    "ba-079": ("ostrich", "a chick"), "ba-080": ("otter", "a pup"),
    "ba-081": ("oyster", "a spat"), "ba-082": ("panda", "a cub"),
    "ba-083": ("parrot", "a chick"), "ba-084": ("peacock", "a peachick"),
    "ba-085": ("penguin", "a chick"), "ba-086": ("pigeon", "a squab"),
    "ba-087": ("platypus", "a puggle"), "ba-088": ("porcupine", "a porcupette"),
    "ba-089": ("quail", "a chick"), "ba-090": ("rat", "a pup or a kitten"),
    "ba-091": ("reindeer", "a calf"), "ba-092": ("rhinoceros", "a calf"),
    "ba-093": ("seal", "a pup"), "ba-094": ("shark", "a pup"),
    "ba-095": ("skunk", "a kit"), "ba-096": ("squirrel", "a kit or a kitten"),
    "ba-097": ("swan", "a cygnet"), "ba-098": ("tiger", "a cub"),
    "ba-099": ("wolf", "a pup or a whelp"), "ba-100": ("zebra", "a foal"),
}
# examples for the baby-animals entries whose old example did not use "baby X"
BABY_EXAMPLES = {
    "ba-061": "The baby eel migrated upriver as an elver.",
    "ba-067": "The baby grouse hid in the bracken.",
    "ba-068": "The baby hare froze in the grass.",
    "ba-069": "The baby hedgehog curled into a ball.",
    "ba-070": "The baby heron opened its beak.",
    "ba-071": "The baby hyena whined for food.",
    "ba-072": "The baby jellyfish drifted on the tide.",
    "ba-073": "The baby kangaroo peered from the pouch.",
    "ba-074": "The baby koala clung to its mother.",
    "ba-075": "The baby leopard practised pouncing.",
    "ba-076": "The baby lion batted at grass.",
    "ba-077": "The baby llama bleated for its mother.",
    "ba-078": "The baby monkey rode on its mother's back.",
    "ba-079": "The baby ostrich sprinted after ants.",
    "ba-080": "The baby otter learned to dive.",
    "ba-081": "The baby oyster settled on the reef.",
    "ba-082": "The baby panda napped in the tree.",
    "ba-083": "The baby parrot opened its beak.",
    "ba-084": "The baby peacock followed the hen.",
    "ba-085": "The baby penguin huddled for warmth.",
    "ba-086": "The baby pigeon was fed crop milk.",
    "ba-087": "The baby platypus wriggled in the burrow.",
    "ba-088": "The baby porcupine's quills were still soft.",
    "ba-089": "The baby quail scampered after its mother.",
    "ba-090": "The baby rat was pink and blind.",
    "ba-091": "The baby reindeer followed the herd.",
    "ba-092": "The baby rhinoceros stayed close to its mother.",
    "ba-093": "The baby seal basked on the ice.",
    "ba-094": "The baby shark was already a hunter.",
    "ba-095": "The baby skunk trailed its mother.",
    "ba-096": "The baby squirrel peered from the drey.",
    "ba-097": "The baby swan paddled after its parents.",
    "ba-098": "The baby tiger pounced on a leaf.",
    "ba-099": "The baby wolf joined the pack.",
    "ba-100": "The baby zebra stood within minutes.",
}

def main():
    files = sorted(f for f in os.listdir(BASE) if f.endswith(".json") and f != "index.json")
    changes = collections.Counter()
    for fn in files:
        data = load(fn)
        words = data["words"]
        by_id = {w["id"]: w for w in words}
        # explicit fixes
        for wid, fields in FIXES.get(fn, {}).items():
            # idempotent re-run: phobias word ids were renamed ph-XX -> pho-XX
            if wid not in by_id and fn == "phobias.json" and wid.startswith("ph-"):
                wid = "pho-" + wid[3:]
            assert wid in by_id, f"{fn}: unknown id {wid}"
            by_id[wid].update(fields)
            changes[fn] += 1
        # baby-animals restructure
        if fn == "baby-animals.json":
            for wid, (animal, term) in BABY_TERMS.items():
                w = by_id[wid]
                assert w["word"] == f"Baby {animal}", (wid, w["word"])
                w["definition"] = f"A baby {animal} is called {term}."
                if wid in BABY_EXAMPLES:
                    w["example"] = BABY_EXAMPLES[wid]
                changes[fn] += 1
        # phobias: expand short "Fear of X." definitions + rename ph-01..50 ids
        if fn == "phobias.json":
            explicit = set(FIXES.get(fn, {}))
            for w in words:
                if w["id"] in explicit:
                    continue
                d = w["definition"]
                if re.match(r"^Fear of [^.]{1,30}\.$", d) and len(d) < 20:
                    w["definition"] = d.replace("Fear of ", "An intense fear of ", 1)
                    changes[fn] += 1
            for w in words:
                m = re.match(r"^ph-(\d+)$", w["id"])
                if m:
                    w["id"] = f"pho-{m.group(1)}"
                    changes[fn] += 1
        # invariants before quiz regen
        wlow = [w["word"].strip().lower() for w in words]
        assert len(set(wlow)) == len(wlow), f"{fn}: duplicate words remain"
        dnorm = [re.sub(r"\s+", " ", w["definition"].strip().lower().rstrip(".")) for w in words]
        dup_defs = [k for k, v in collections.Counter(dnorm).items() if v > 1]
        assert not dup_defs, f"{fn}: duplicate definitions remain: {dup_defs}"
        ids = [w["id"] for w in words]
        assert len(set(ids)) == len(ids), f"{fn}: duplicate word ids"
        for w in words:
            for k in ("id", "word", "pos", "definition", "example"):
                assert w.get(k) and str(w[k]).strip(), f"{fn} {w.get('id')}: empty {k}"
            assert len(w["definition"].strip()) >= 10, f"{fn} {w['id']}: definition <10 chars"
        # regenerate quiz, preserving existing quiz-id prefix
        prefix = quiz_prefix(data)
        data["quiz"] = build_quiz(words, prefix, seed=data["category"])
        save(fn, data)
        print(f"{fn}: {changes[fn]} entry changes, quiz regenerated ({prefix}-q1..q100)")
    print("DONE. Changed entries total:", sum(changes.values()))

if __name__ == "__main__":
    main()
