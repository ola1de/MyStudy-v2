"""Hausa, Igbo, Yoruba pools — written in the language, covering WAEC syllabus topics
(sound system, grammar, oral/written literature, customs, greetings).
Only vocabulary, grammar, numbers, greetings and literature facts the generator is confident about are used;
no English questions are passed off as language questions."""
import random
from core import mk, uniq_pool
from facts1 import _facts_pool

def _vocab_pool(year, seed, lang_name, q_en_to_lang, q_lang_to_en, vocab, extra_facts):
    """vocab = list of (english, lang_word, category). Two question forms per entry."""
    rng = random.Random(f"{seed}-{year}")
    P = []
    words = [w for _, w, _ in vocab]
    for en, lw, _cat in vocab:
        ds = [w for w in words if w != lw]
        rng.shuffle(ds)
        P.append(mk(q_en_to_lang.format(en=en), lw, ds[:3],
                    f"'{lw}' ita ce kalmar {lang_name} ta '{en}'.", year, "Vocabulary"))
        ens = [e for e, _, _ in vocab]
        ds2 = [e for e in ens if e != en]
        rng.shuffle(ds2)
        P.append(mk(q_lang_to_en.format(lw=lw), en, ds2[:3],
                    f"'{lw}' na nufin '{en}' da Turanci.", year, "Vocabulary"))
    for q, c, ds, e, t in extra_facts:
        ds2 = list(ds); rng.shuffle(ds2)
        P.append(mk(q, c, ds2, e, year, t))
    return uniq_pool(P)

def hausa_pool(year):
    vocab = [("dog", "kare", "animal"), ("cat", "kyanwa", "animal"), ("cow", "saniya", "animal"),
             ("goat", "akuya", "animal"), ("hen", "kaza", "animal"), ("horse", "doki", "animal"),
             ("lion", "zaki", "animal"), ("elephant", "giwa", "animal"),
             ("head", "kai", "body"), ("eye", "ido", "body"), ("nose", "hanci", "body"),
             ("mouth", "baki", "body"), ("hand", "hannu", "body"), ("leg", "kafa", "body"),
             ("father", "uba", "family"), ("mother", "uwa", "family"), ("boy", "yaro", "family"),
             ("girl", "yarinya", "family"), ("man", "namiji", "family"), ("woman", "mace", "family"),
             ("white", "fari", "colour"), ("black", "baki", "colour"), ("red", "ja", "colour"),
             ("green", "kore", "colour"), ("blue", "shuɗi", "colour"), ("yellow", "rawaya", "colour"),
             ("water", "ruwa", "nature"), ("sun", "rana", "nature")]
    nums = [("one", "ɗaya"), ("two", "biyu"), ("three", "uku"), ("four", "hudu"), ("five", "biyar"),
            ("six", "shida"), ("seven", "bakwai"), ("eight", "takwas"), ("nine", "tara"), ("ten", "goma"),
            ("eleven", "goma sha ɗaya"), ("twelve", "goma sha biyu"), ("twenty", "ashirin")]
    extra = []
    for en, hw in nums:
        others = [x for _, x in nums if x != hw]
        random.Random(f"hausa-num-{year}-{en}").shuffle(others)
        extra.append((f"Menene '{en}' da Hausa?", hw, others[:3],
                      f"'{en}' da Hausa shi ne '{hw}'.", "Numbers"))
    extra += [
        ("Wanne ne cikin wadannan wakilin suna ne na nuni (demonstrative pronoun)?", "Wannan", ["Su", "Mu", "Kai"], "'Wannan' (this) is used for pointing at a specific noun.", "Grammar (Nahawu)"),
        ("Wasulan Hausa guda nawa ne a tsaye (standard vowels)?", "Biyar", ["Bakwai", "Goma", "Sha biyu"], "Standard Hausa has five basic vowels: a, e, i, o, u.", "Sound system (Tsarin Sauti)"),
        ("Menene 'noun' da Hausa?", "Suna", ["Aikatau", "Sifa", "Bayanau"], "'Suna' means noun in Hausa.", "Grammar (Nahawu)"),
        ("Menene 'verb' da Hausa?", "Aikatau", ["Suna", "Sifa", "Wakilin suna"], "'Aikatau' means verb in Hausa.", "Grammar (Nahawu)"),
        ("Menene 'adjective' da Hausa?", "Sifa", ["Suna", "Aikatau", "Bayanau"], "'Sifa' means adjective in Hausa.", "Grammar (Nahawu)"),
        ("Wanene ya rubuta littafin 'Magana Jari Ce'?", "Abubakar Imam", ["Aminu Kano", "Tafawa Balewa", "Cyprian Ekwensi"], "'Magana Jari Ce' was written by Abubakar Imam.", "Written literature"),
        ("Wanene ya rubuta littafin 'Ruwan Bagaja'?", "Abubakar Imam", ["Aminu Kano", "Bello Kagara", "Tafawa Balewa"], "'Ruwan Bagaja' was written by Abubakar Imam.", "Written literature"),
        ("Menene gaisuwa da safe da Hausa?", "Ina kwana", ["Ina wuni", "Ina yini", "Sai anjima"], "'Ina kwana' is the morning greeting in Hausa.", "Greeting"),
        ("Menene gaisuwa da rana da Hausa?", "Ina wuni", ["Ina kwana", "Ina yini", "Sai anjima"], "'Ina wuni' is the afternoon greeting in Hausa.", "Greeting"),
        ("Menene gaisuwa da yamma da Hausa?", "Ina yini", ["Ina kwana", "Ina wuni", "Sai anjima"], "'Ina yini' is the evening greeting in Hausa.", "Greeting"),
        ("Menene amsar 'Ina kwana'?", "Lafiya lau", ["Na gode", "Sai anjima", "Barka"], "The reply to 'Ina kwana' is 'Lafiya lau'.", "Greeting"),
        ("Wanne ne daga cikin wadannan baƙaƙen Hausa ne na gaskiya?", "B", ["Q", "X", "V"], "Hausa uses the letter B; Q, X and V are not standard Hausa letters.", "Sound system (Tsarin Sauti)"),
        ("Karin magana 'Abin da ka shuka, shi za ka girba' na nufin", "Za ka girbi abin da ka shuka", ["Ka yi aiki tukuru", "Ka yi hakuri", "Ka yi addu'a"], "The proverb means you reap what you sow.", "Oral literature"),
        ("Wanne ne daga cikin wadannan suna ne na mace?", "Maryam", ["Musa", "Ibrahim", "Yusuf"], "Maryam is a female name.", "Grammar (Nahawu)"),
        ("Menene 'school' da Hausa?", "Makaranta", ["Kasuwanci", "Gida", "Asibiti"], "'Makaranta' means school in Hausa.", "Vocabulary"),
        ("Menene 'book' da Hausa?", "Littafi", ["Takarda", "Alƙalami", "Tebur"], "'Littafi' means book in Hausa.", "Vocabulary"),
        ("Menene 'house' da Hausa?", "Gida", ["Makaranta", "Kasuwanci", "Asibiti"], "'Gida' means house in Hausa.", "Vocabulary"),
        ("Menene 'market' da Hausa?", "Kasuwanci", ["Gida", "Makaranta", "Asibiti"], "'Kasuwanci' means market in Hausa.", "Vocabulary"),
        ("Wace rana ce ta farko a mako da Hausa?", "Lahadi", ["Litinin", "Talata", "Juma'a"], "The week in Hausa begins with Lahadi (Sunday).", "Vocabulary"),
        ("Menene 'Monday' da Hausa?", "Litinin", ["Talata", "Laraba", "Alhamis"], "'Litinin' is Monday in Hausa.", "Vocabulary"),
        ("Menene 'Friday' da Hausa?", "Juma'a", ["Asabar", "Lahadi", "Litinin"], "'Juma'a' is Friday in Hausa.", "Vocabulary"),
    ]
    return _vocab_pool(year, "hausa", "Hausa",
                       "Menene '{en}' da Hausa?", "Menene ma'anar '{lw}' da Turanci?",
                       vocab, extra)

def igbo_pool(year):
    vocab = [("dog", "nkịta", "animal"), ("cat", "nwamba", "animal"), ("cow", "ehi", "animal"),
             ("goat", "ewu", "animal"), ("hen", "ọkụkọ", "animal"), ("horse", "ịnyịnya", "animal"),
             ("lion", "ọdụm", "animal"), ("elephant", "enyi", "animal"),
             ("head", "isi", "body"), ("eye", "anya", "body"), ("nose", "imi", "body"),
             ("mouth", "ọnụ", "body"), ("hand", "aka", "body"), ("leg", "ụkwụ", "body"),
             ("father", "nna", "family"), ("mother", "nne", "family"), ("boy", "nwoke", "family"),
             ("girl", "nwanyị", "family"), ("man", "nwoke", "family"), ("woman", "nwanyị", "family"),
             ("white", "ọcha", "colour"), ("black", "ojii", "colour"), ("red", "uhie", "colour"),
             ("green", "akwụkwọ ndụ", "colour"), ("yellow", "edo", "colour"),
             ("water", "mmiri", "nature"), ("sun", "anwụ", "nature")]
    nums = [("one", "otu"), ("two", "abụọ"), ("three", "atọ"), ("four", "anọ"), ("five", "ise"),
            ("six", "isii"), ("seven", "asaa"), ("eight", "asatọ"), ("nine", "iteghete"), ("ten", "iri"),
            ("eleven", "iri na otu"), ("twelve", "iri na abụọ"), ("twenty", "ogwu")]
    extra = []
    for en, iw in nums:
        others = [x for _, x in nums if x != iw]
        random.Random(f"igbo-num-{year}-{en}").shuffle(others)
        extra.append((f"Gịnị bụ '{en}' n'asụsụ Igbo?", iw, others[:3],
                      f"'{en}' n'asụsụ Igbo bụ '{iw}'.", "Numbers"))
    extra += [
        ("Gịnị bụ 'noun' n'asụsụ Igbo?", "Aha", ["Ngwaa", "Nkọwa", "Nnọchiaha"], "'Aha' pụtara noun n'asụsụ Igbo.", "Grammar"),
        ("Gịnị bụ 'verb' n'asụsụ Igbo?", "Ngwaa", ["Aha", "Nkọwa", "Nnọchiaha"], "'Ngwaa' pụtara verb n'asụsụ Igbo.", "Grammar"),
        ("Ònye dere akwụkwọ 'Omenuko'?", "Pita Nwana", ["Chinua Achebe", "F. C. Ogbalu", "Tony Ubesie"], "'Omenuko' bụ akwụkwọ Pita Nwana dere.", "Written literature"),
        ("Ònye dere akwụkwọ 'Things Fall Apart'?", "Chinua Achebe", ["Pita Nwana", "Wole Soyinka", "Ngugi wa Thiong'o"], "'Things Fall Apart' bụ akwụkwọ Chinua Achebe dere.", "Written literature"),
        ("Gịnị bụ ekele ụtụtụ n'asụsụ Igbo?", "Ụtụtụ ọma", ["Ehihie ọma", "Mgbede ọma", "Ka ọ mesịa"], "'Ụtụtụ ọma' bụ ekele ụtụtụ n'asụsụ Igbo.", "Greeting"),
        ("Gịnị bụ ekele ehihie n'asụsụ Igbo?", "Ehihie ọma", ["Ụtụtụ ọma", "Mgbede ọma", "Ka ọ mesịa"], "'Ehihie ọma' bụ ekele ehihie n'asụsụ Igbo.", "Greeting"),
        ("Gịnị bụ ekele mgbede n'asụsụ Igbo?", "Mgbede ọma", ["Ụtụtụ ọma", "Ehihie ọma", "Ka ọ mesịa"], "'Mgbede ọma' bụ ekele mgbede n'asụsụ Igbo.", "Greeting"),
        ("Ilu Igbo 'Egbe bere ugo bere' pụtara na", "Onye ọ bụla nwere ikike ịdị ndụ", ["Nnụnụ na-efe efe", "Ugo ka egbe ike", "Egbe na-eri ugo"], "Ilu ahụ pụtara na onye ọ bụla nwere ikike ịdị ndụ.", "Oral literature"),
        ("Ilu Igbo 'Onye ajụrụ aju anaghị aju onwe ya' pụtara na", "Onye a jụrụ ekwesịghị ịjụ onwe ya", ["Onye a jụrụ ga-anwụ", "Onye a jụrụ bụ onye ọjọọ", "Onye a jụrụ enweghị uru"], "Ilu ahụ na-akụzi na onye a jụrụ ekwesịghị ịjụ onwe ya.", "Oral literature"),
        ("Ụdaume Igbo ole ka ha dị?", "Asatọ", ["Ise", "Iri", "Itoolu"], "Asụsụ Igbo nwere ụdaume asatọ: a, e, i, o, u, ọ, ụ na ị.", "Sound system"),
        ("Gịnị bụ 'school' n'asụsụ Igbo?", "Ụlọ akwụkwọ", ["Ụlọ ahịa", "Ụlọ ọgwụ", "Ụlọ ekpere"], "'Ụlọ akwụkwọ' pụtara school n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'book' n'asụsụ Igbo?", "Akwụkwọ", ["Mkpịsị odee", "Tebulu", "Oche"], "'Akwụkwọ' pụtara book n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'house' n'asụsụ Igbo?", "Ụlọ", ["Ụlọ akwụkwọ", "Ụlọ ahịa", "Ụlọ ọgwụ"], "'Ụlọ' pụtara house n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'market' n'asụsụ Igbo?", "Ahịa", ["Ụlọ", "Ụlọ akwụkwọ", "Ụlọ ọgwụ"], "'Ahịa' pụtara market n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'Monday' n'asụsụ Igbo?", "Mọnde", ["Tuzde", "Wednesde", "Sọnde"], "'Mọnde' bụ Monday n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'Sunday' n'asụsụ Igbo?", "Sọnde", ["Mọnde", "Tuzde", "Fraịde"], "'Sọnde' bụ Sunday n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'yam' n'asụsụ Igbo?", "Ji", ["Akwụ", "Ọka", "Ede"], "'Ji' pụtara yam n'asụsụ Igbo.", "Vocabulary"),
        ("Gịnị bụ 'kola nut' n'asụsụ Igbo?", "Ọjị", ["Ji", "Akwụ", "Ọka"], "'Ọjị' pụtara kola nut n'asụsụ Igbo.", "Customs (Omenala)"),
        ("Emume Iri Ji bụ emume", "Iri ji ọhụrụ", ["Ọmụmụ nwa", "Alụmdi na nwunye", "Olili ozu"], "Emume Iri Ji bụ emume iri ji ọhụrụ.", "Customs (Omenala)"),
        ("Mmanwu bụ", "Masquerade", ["Egwuregwu", "Abụ", "Ịgba egwu"], "Mmanwu bụ masquerade n'ala Igbo.", "Customs (Omenala)"),
    ]
    return _vocab_pool(year, "igbo", "Igbo",
                       "Gịnị bụ '{en}' n'asụsụ Igbo?", "Gịnị ka '{lw}' pụtara n'asụsụ Bekee?",
                       vocab, extra)

def yoruba_pool(year):
    vocab = [("dog", "ajá", "animal"), ("cat", "ológbo", "animal"), ("cow", "màlúù", "animal"),
             ("goat", "ewúré", "animal"), ("hen", "adìẹ", "animal"), ("horse", "ẹṣin", "animal"),
             ("lion", "kìnìún", "animal"), ("elephant", "erin", "animal"),
             ("head", "orí", "body"), ("eye", "ojú", "body"), ("nose", "imú", "body"),
             ("mouth", "ẹnu", "body"), ("hand", "ọwọ́", "body"), ("leg", "ẹsẹ̀", "body"),
             ("father", "bàbá", "family"), ("mother", "màmá", "family"), ("boy", "ọmọkùnrin", "family"),
             ("girl", "ọmọbìnrin", "family"), ("man", "ọkùnrin", "family"), ("woman", "obìnrin", "family"),
             ("white", "fúnfun", "colour"), ("black", "dúdú", "colour"), ("red", "pupa", "colour"),
             ("green", "aláwọ̀ ewé", "colour"), ("blue", "búlù", "colour"), ("yellow", "òfèéfèé", "colour"),
             ("water", "omi", "nature"), ("sun", "oòrùn", "nature")]
    nums = [("one", "òòkan"), ("two", "èèjì"), ("three", "ẹ̀ẹ́ta"), ("four", "ẹ̀ẹ́rin"), ("five", "àárùn"),
            ("six", "ẹ̀ẹ́fà"), ("seven", "èèje"), ("eight", "ẹ̀ẹ́jọ"), ("nine", "ẹ̀ẹ́sàn"), ("ten", "ẹ̀ẹ́wáà"),
            ("eleven", "ọ̀ọ́kanlá"), ("twelve", "èèjìlá"), ("twenty", "ogún")]
    extra = []
    for en, yw in nums:
        others = [x for _, x in nums if x != yw]
        random.Random(f"yor-num-{year}-{en}").shuffle(others)
        extra.append((f"Kí ni '{en}' ní èdè Yorùbá?", yw, others[:3],
                      f"'{en}' ní èdè Yorùbá ni '{yw}'.", "Numbers"))
    extra += [
        ("Irúfẹ́ ọ̀rọ̀-àsọjú-orúkọ wo ni 'Èmi'?", "Adáńdúró", ["Asolù", "Asopọ̀", "Atọ́ka"], "'Èmi' is an independent (emphatic) pronoun.", "Grammar"),
        ("Fáwẹ̀lì Yorùbá mélòó ni?", "Méje", ["Márùn-ún", "Mẹ́jọ", "Mẹ́wàá"], "Yoruba has seven vowels: a, e, ẹ, i, o, ọ, u.", "Sound system"),
        ("Àmì ohun Yorùbá mélòó ni?", "Mẹ́ta", ["Méjì", "Márùn-ún", "Mẹ́rin"], "Yoruba has three tones: low, mid and high.", "Sound system"),
        ("Ta ni ó kọ ìwé 'Ògbójú Ọdẹ Nínú Igbó Irúnmọ̀lẹ̀'?", "D. O. Fagunwa", ["Wole Soyinka", "Akinwumi Isola", "Amos Tutuola"], "'Ògbójú Ọdẹ Nínú Igbó Irúnmọ̀lẹ̀' was written by D. O. Fagunwa.", "Written literature"),
        ("Ta ni ó kọ ìwé 'Olèkù'?", "Akinwumi Isola", ["D. O. Fagunwa", "Wole Soyinka", "Kola Akinlade"], "'Olèkù' was written by Akinwumi Isola.", "Written literature"),
        ("Ta ni ó kọ ìwé 'The Lion and the Jewel'?", "Wole Soyinka", ["Chinua Achebe", "D. O. Fagunwa", "Ola Rotimi"], "'The Lion and the Jewel' was written by Wole Soyinka.", "Written literature"),
        ("Ta ni ó kọ ìwé 'The Palm-Wine Drinkard'?", "Amos Tutuola", ["D. O. Fagunwa", "Wole Soyinka", "Chinua Achebe"], "'The Palm-Wine Drinkard' was written by Amos Tutuola.", "Written literature"),
        ("Kí ni ìkíni òwúrọ̀ ní èdè Yorùbá?", "Ẹ káàrọ̀", ["Ẹ káàsán", "Ẹ kù ìrólẹ̀", "Ẹ n lẹ"], "'Ẹ káàrọ̀' is the morning greeting in Yoruba.", "Greeting"),
        ("Kí ni ìkíni ọ̀sán ní èdè Yorùbá?", "Ẹ káàsán", ["Ẹ káàrọ̀", "Ẹ kù ìrólẹ̀", "Ẹ n lẹ"], "'Ẹ káàsán' is the afternoon greeting in Yoruba.", "Greeting"),
        ("Kí ni ìkíni ìrọ̀lẹ́ ní èdè Yorùbá?", "Ẹ kù ìrólẹ̀", ["Ẹ káàrọ̀", "Ẹ káàsán", "Ẹ n lẹ"], "'Ẹ kù ìrólẹ̀' is the evening greeting in Yoruba.", "Greeting"),
        ("Òwe Yorùbá 'Òwe l'ẹ̀ṣin ọ̀rọ̀' túmọ̀ sí pé", "Òwe ni ẹ̀ṣin ọ̀rọ̀", ["Ọ̀rọ̀ ni ẹ̀ṣin òwe", "Òwe kò ṣe pàtàkì", "Ọ̀rọ̀ kò ní òwe"], "The proverb means 'a proverb is the horse of speech'.", "Oral literature"),
        ("Kí ni 'school' ní èdè Yorùbá?", "Ilé-ẹ̀kọ́", ["Ilé-ìwòsàn", "Ọjà", "Ilé"], "'Ilé-ẹ̀kọ́' means school in Yoruba.", "Vocabulary"),
        ("Kí ni 'book' ní èdè Yorùbá?", "Ìwé", ["Ìkọ̀wé", "Tábìlì", "Àga"], "'Ìwé' means book in Yoruba.", "Vocabulary"),
        ("Kí ni 'house' ní èdè Yorùbá?", "Ilé", ["Ilé-ẹ̀kọ́", "Ọjà", "Ilé-ìwòsàn"], "'Ilé' means house in Yoruba.", "Vocabulary"),
        ("Kí ni 'market' ní èdè Yorùbá?", "Ọjà", ["Ilé", "Ilé-ẹ̀kọ́", "Ilé-ìwòsàn"], "'Ọjà' means market in Yoruba.", "Vocabulary"),
        ("Kí ni 'Monday' ní èdè Yorùbá?", "Ọjọ́ Ajé", ["Ọjọ́ Ìṣẹ́gun", "Ọjọ́rú", "Ọjọ́bọ̀"], "'Ọjọ́ Ajé' is Monday in Yoruba.", "Vocabulary"),
        ("Kí ni 'Sunday' ní èdè Yorùbá?", "Ọjọ́ Ìsinmi", ["Ọjọ́ Ajé", "Ọjọ́ Ìṣẹ́gun", "Ọjọ́rú"], "'Ọjọ́ Ìsinmi' is Sunday in Yoruba.", "Vocabulary"),
        ("Kí ni 'yam' ní èdè Yorùbá?", "Iṣu", ["Àgbàdo", "Ẹ̀gẹ́", "Ọ̀gẹ̀dẹ̀"], "'Iṣu' means yam in Yoruba.", "Vocabulary"),
        ("Kí ni iṣẹ́ 'ẹ̀mí' nínú ìpín mẹ́ta tí Yorùbá pín ènìyàn sí?", "Láti sọ ara di alààyè", ["Láti gbé ara ró", "Láti fún ènìyàn ní ìjìnlẹ̀ òye", "Láti yan orí ní àjálá mọpin"], "In Yoruba thought, ẹ̀mí (breath/soul) animates the body.", "Customs"),
        ("Ẹ̀yà wo ni Yorùbá pín ènìyàn sí?", "Ara, ẹ̀mí àti orí", ["Ara àti ẹ̀mí nìkan", "Orí nìkan", "Ara, ẹ̀jẹ̀ àti egungun"], "Yoruba divides a person into ara (body), ẹ̀mí (soul) and orí (destiny).", "Customs"),
        ("Ọ̀rọ̀ wo ni ó jẹ́ 'noun' ní èdè Yorùbá?", "Ọ̀rọ̀-orúkọ", ["Ọ̀rọ̀-ìṣe", "Àpèjúwe", "Ọ̀rọ̀-àsọjú-orúkọ"], "'Ọ̀rọ̀-orúkọ' is a noun in Yoruba.", "Grammar"),
        ("Ọ̀rọ̀ wo ni ó jẹ́ 'verb' ní èdè Yorùbá?", "Ọ̀rọ̀-ìṣe", ["Ọ̀rọ̀-orúkọ", "Àpèjúwe", "Ọ̀rọ̀-àsọjú-orúkọ"], "'Ọ̀rọ̀-ìṣe' is a verb in Yoruba.", "Grammar"),
    ]
    return _vocab_pool(year, "yoruba", "Yoruba",
                       "Kí ni '{en}' ní èdè Yorùbá?", "Kí ni ìtumọ̀ '{lw}' ní èdè Gẹ̀ẹ́sì?",
                       vocab, extra)
