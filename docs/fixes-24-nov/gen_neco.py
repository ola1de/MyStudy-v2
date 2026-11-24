
# ---------------- EXPANSION POOLS ----------------
# Second wave: reverse-direction questions (capital->country, symbol->element, author->work,
# year->event, disease->nutrient, etc.) + new parametric sets + new factual tables.
# Every item is a distinct question text from the first wave; together the two waves give
# >=160 distinct items per subject (40 per year x 4 years), English >=200 std + 8 passages.
def extra_pool(subj):
    E = []
    def a(t, q, c, d, e): E.append(mk(0, subj, t, q, c, d, e))
    if subj == "Mathematics":
        for x, y in [(7,8),(9,6),(11,4),(13,5),(15,3),(17,2),(6,9),(8,7),(12,11),(14,6)]:
            add = x+y
            a("Algebra", f"Find the sum of {x} and {y}.", str(add), [str(add+1), str(add-1), str(add+2)],
              f"{x} + {y} = {add}.")
        for x, y in [(9,4),(12,3),(15,5),(18,6),(20,4),(16,8),(21,7),(24,6),(27,9),(30,5)]:
            a("Algebra", f"Find the value of {x} divided by {y}.", str(x//y), [str(x//y+1), str(x//y-1), str(x*y)],
              f"{x} / {y} = {x//y}.")
        for n in [2,3,4,5,6,7,8,9,10,11]:
            a("Algebra", f"Find the square of {n}.", str(n*n), [str(n*n+1), str(n*n-1), str(n*n+2)],
              f"{n}\u00b2 = {n*n}.")
    if subj == "FurtherMath":
        for k, n in [(2,3),(3,4),(5,3),(4,4),(6,2),(2,5),(3,5),(7,2),(4,5),(5,4)]:
            a("Calculus", f"Find dy/dx if y = {k}x^{n}.", f"{k*n}x^{n-1}",
              [f"{k}x^{n-1}", f"{k*n}x^{n}", f"{k}x^{n}"], f"dy/dx = {k*n}x^{n-1}.")
        for k, n in [(6,2),(12,3),(20,4),(3,3),(8,2),(15,3),(4,4),(10,2),(24,5),(2,4)]:
            coeff = Fraction(k, n+1)
            a("Calculus", f"Find \u222b {k}x^{n} dx.", f"{fmt_num(coeff)}x^{n+1} + C",
              [f"{k}x^{n+1} + C", f"{fmt_num(coeff)}x^{n} + C", f"{k*n}x^{n-1} + C"],
              f"\u222b {k}x^{n} dx = {fmt_num(coeff)}x^{n+1} + C.")
        for p, q_, r, s in [(2,3,1,4),(3,1,2,5),(1,4,3,2),(5,2,1,3),(2,2,4,3),(4,3,2,1),
                            (3,3,1,1),(2,5,3,4),(1,1,2,2),(6,1,1,2)]:
            det = p*s-q_*r
            a("Matrices", f"Find the determinant of [[{p}, {q_}], [{r}, {s}]].", str(det),
              [str(det+1), str(det-1), str(p*s+q_*r)], f"det = {p}x{s} - {q_}x{r} = {det}.")
        for n, r in [(9,2),(10,3),(8,3),(9,3),(10,2),(7,4),(11,2),(12,3)]:
            a("Combinatorics", f"Evaluate C({n}, {r}).", str(math.comb(n, r)),
              [str(math.comb(n, r)+1), str(math.comb(n, r)-1), str(math.perm(n, r))],
              f"C({n},{r}) = {math.comb(n, r)}.")
        for n, r in [(9,2),(8,4),(10,4),(7,3),(11,3),(12,2)]:
            a("Combinatorics", f"Evaluate P({n}, {r}).", str(math.perm(n, r)),
              [str(math.perm(n, r)+1), str(math.perm(n, r)-1), str(math.comb(n, r))],
              f"P({n},{r}) = {math.perm(n, r)}.")
        for k in [2,3,4,5,6]:
            a("Algebra", f"Expand (x + {k})\u00b2.", f"x\u00b2 + {2*k}x + {k*k}",
              [f"x\u00b2 + {k}x + {k*k}", f"x\u00b2 + {2*k}x + {k}", f"x\u00b2 + {k*k}"],
              f"(x+{k})\u00b2 = x\u00b2 + {2*k}x + {k*k}.")
        for k in [2,3,4,5]:
            a("Trigonometry", f"Find the value of tan 45\u00b0 multiplied by {k}.", str(k),
              [str(k+1), str(k-1), "0"], f"tan 45\u00b0 = 1, so 1 x {k} = {k}.")
        a("Calculus", "The derivative of e^x is:", "e^x", ["x e^x", "e^x / x", "ln x"],
          "d/dx(e^x) = e^x.")
        a("Calculus", "The integral of cos x dx is:", "sin x + C", ["-sin x + C", "cos x + C", "-cos x + C"],
          "\u222b cos x dx = sin x + C.")
        a("Calculus", "The integral of sin x dx is:", "-cos x + C", ["cos x + C", "sin x + C", "-sin x + C"],
          "\u222b sin x dx = -cos x + C.")
        a("Vectors and Complex Numbers", "The dot product of (1, 2) and (3, 4) is:", "11",
          ["10", "12", "14"], "(1x3) + (2x4) = 3 + 8 = 11.")
        a("Vectors and Complex Numbers", "The dot product of (2, 3) and (4, 1) is:", "11",
          ["10", "12", "9"], "(2x4) + (3x1) = 8 + 3 = 11.")
        a("Statistics", "The standard deviation of a constant is:", "0", ["1", "the constant", "undefined"],
          "A constant does not vary, so its standard deviation is 0.")
        a("Algebra", "If f(x) = x\u00b2 + 1, find f(3).", "10", ["9", "8", "7"], "f(3) = 9 + 1 = 10.")
        a("Algebra", "If f(x) = 2x + 3, find f(4).", "11", ["10", "12", "9"], "f(4) = 8 + 3 = 11.")
        a("Algebra", "If f(x) = x\u00b3, find f(2).", "8", ["6", "4", "9"], "f(2) = 2\u00b3 = 8.")
    if subj == "Physics":
        for u, a_, t in [(2,3,4),(4,2,6),(8,5,2),(12,3,3),(6,4,5),(3,6,3),(10,10,2),(0,4,6)]:
            v = u+a_*t; s = u*t + a_*t*t//2
            a("Motion", f"A body with initial velocity {u} m/s accelerates at {a_} m/s\u00b2 for {t} s. Find the distance covered.", f"{s} m",
              [f"{s+10} m", f"{v} m", f"{s+20} m"], f"s = ut + 1/2 at\u00b2 = {u}x{t} + 1/2 x {a_} x {t}\u00b2 = {s} m.")
        for m, v in [(3,8),(6,10),(2,12),(10,6),(5,4),(4,20)]:
            p = m*v
            a("Motion", f"Find the momentum of a {m} kg body moving at {v} m/s.", f"{p} kg m/s",
              [f"{p+5} kg m/s", f"{m+v} kg m/s", f"{p-5} kg m/s"], f"Momentum = mv = {m} x {v} = {p} kg m/s.")
        for r, i in [(10,2),(5,4),(20,1),(4,5),(8,3),(15,2)]:
            a("Electricity", f"Find the voltage across a {r} \u03a9 resistor carrying {i} A.", f"{r*i} V",
              [f"{r+i} V", f"{r*i+5} V", f"{r*i-5} V"], f"V = IR = {r} x {i} = {r*i} V.")
        for q_, t in [(20,4),(30,5),(60,10),(12,3),(100,20),(24,6)]:
            a("Electricity", f"A charge of {q_} C flows in {t} s. Find the current.", f"{q_//t} A",
              [f"{q_*t} A", f"{q_//t+1} A", f"{t} A"], f"I = Q/t = {q_}/{t} = {q_//t} A.")
        for l in [1,2,3,4,5]:
            a("Waves", f"The period of a wave of frequency {l*10} Hz is:", f"{fmt_num(Fraction(1,l*10))} s",
              [f"{l*10} s", f"{fmt_num(Fraction(1,l*5))} s", "1 s"], f"T = 1/f = 1/{l*10} s.")
        for m, g in [(2,10),(5,10),(10,10)]:
            a("Work, Energy and Power", f"Find the weight of a {m} kg mass. (g = 10 m/s\u00b2)", f"{m*10} N",
              [f"{m} N", f"{m*5} N", f"{m*20} N"], f"W = mg = {m} x 10 = {m*10} N.")
        for f, d in [(50,4),(100,2),(80,5),(200,3),(60,10),(150,2)]:
            a("Work, Energy and Power", f"Find the work done when a force of {f} N moves a body {d} m.", f"{f*d} J",
              [f"{f+d} J", f"{f*d+50} J", f"{f//d} J"], f"Work = force x distance = {f} x {d} = {f*d} J.")
        for h in [2,5,10,4]:
            a("Pressure", f"Find the pressure at a depth of {h} m in water. (density 1000 kg/m\u00b3, g = 10 m/s\u00b2)", f"{h*10000} Pa",
              [f"{h*1000} Pa", f"{h*10000+1000} Pa", f"{h*100} Pa"], f"P = \u03c1gh = 1000 x 10 x {h} = {h*10000} Pa.")
    if subj == "Chemistry":
        elements = [("Hydrogen","H"),("Helium","He"),("Carbon","C"),("Nitrogen","N"),("Oxygen","O"),
                    ("Fluorine","F"),("Sodium","Na"),("Magnesium","Mg"),("Aluminium","Al"),("Silicon","Si"),
                    ("Phosphorus","P"),("Sulphur","S"),("Chlorine","Cl"),("Potassium","K"),("Calcium","Ca"),
                    ("Iron","Fe"),("Copper","Cu"),("Zinc","Zn"),("Silver","Ag"),("Gold","Au"),
                    ("Lead","Pb"),("Tin","Sn"),("Mercury","Hg"),("Iodine","I"),("Bromine","Br")]
        for name, sym in elements:
            others = [n for n, s in elements if n != name][:3]
            a("Atomic Structure and Periodicity", f"Which element has the chemical symbol {sym}?", name, others,
              f"The symbol {sym} stands for {name}.")
        compounds = [("ammonium chloride, NH\u2084Cl", 53.5), ("potassium chloride, KCl", 74.5),
                     ("magnesium oxide, MgO", 40), ("zinc oxide, ZnO", 81), ("iron(II) oxide, FeO", 72),
                     ("copper(II) sulphate, CuSO\u2084", 160), ("sodium carbonate, Na\u2082CO\u2083", 106),
                     ("calcium hydroxide, Ca(OH)\u2082", 74), ("aluminium oxide, Al\u2082O\u2083", 102),
                     ("glucose, C\u2086H\u2081\u2082O\u2086", 180), ("ethanol, C\u2082H\u2085OH", 46), ("ethanoic acid, CH\u2083COOH", 60)]
        for name, mm in compounds:
            a("Chemical Combination", f"What is the molar mass of {name}?", f"{fmt_num(mm)} g/mol",
              [f"{fmt_num(mm+10)} g/mol", f"{fmt_num(mm-5)} g/mol", f"{fmt_num(mm*2)} g/mol"],
              f"Adding the atomic masses gives {fmt_num(mm)} g/mol.")
        for mass, mm, name in [(54,18,"water"),(132,44,"carbon dioxide"),(85,17,"ammonia"),
                               (48,16,"methane"),(120,40,"sodium hydroxide"),(300,100,"calcium carbonate")]:
            moles = mass/mm
            a("Chemical Combination", f"How many moles are in {fmt_num(mass)} g of {name}?", f"{fmt_num(moles)} mol",
              [f"{fmt_num(moles+1)} mol", f"{fmt_num(moles*2)} mol", f"{fmt_num(moles/2)} mol"],
              f"Moles = mass/molar mass = {fmt_num(moles)} mol.")
        a("Acids, Bases and Salts", "The pH of a strong alkaline solution is close to:", "14",
          ["7", "0", "3"], "Alkaline solutions have pH above 7, up to 14.")
        a("Acids, Bases and Salts", "The pH of a strong acid is close to:", "1", ["7", "14", "10"],
          "Strong acids have pH near 0-1.")
        a("Acids, Bases and Salts", "Methyl orange turns _____ in an acid.", "red", ["yellow", "blue", "green"],
          "Methyl orange is red in acid and yellow in alkali.")
        a("Acids, Bases and Salts", "Phenolphthalein turns _____ in an alkali.", "pink",
          ["red", "blue", "yellow"], "Phenolphthalein is pink in alkali and colourless in acid.")
        a("Organic Chemistry", "The molecular formula of ethane is:", "C\u2082H\u2086",
          ["C\u2082H\u2084", "CH\u2084", "C\u2083H\u2088"], "Ethane is C\u2082H\u2086.")
        a("Organic Chemistry", "The molecular formula of propane is:", "C\u2083H\u2088",
          ["C\u2083H\u2086", "C\u2082H\u2086", "C\u2084H\u208a\u2080"], "Propane is C\u2083H\u2088.")
        a("Organic Chemistry", "The molecular formula of butane is:", "C\u2084H\u208a\u2080",
          ["C\u2084H\u2088", "C\u2083H\u2088", "C\u2085H\u208a\u2082"], "Butane is C\u2084H\u208a\u2080.")
        a("Organic Chemistry", "The functional group of aldehydes is:", "-CHO",
          ["-OH", "-COOH", "-NH\u2082"], "Aldehydes contain -CHO.")
        a("Organic Chemistry", "The functional group of ketones is:", "-CO-",
          ["-OH", "-COOH", "-CHO"], "Ketones contain the carbonyl group -CO-.")
        a("Organic Chemistry", "The functional group of amines is:", "-NH\u2082",
          ["-OH", "-COOH", "-CHO"], "Amines contain -NH\u2082.")
        a("Chemical Reactions", "In a redox reaction, oxidation is:", "loss of electrons",
          ["gain of electrons", "loss of protons", "gain of protons"], "OIL RIG: Oxidation Is Loss of electrons.")
        a("Chemical Reactions", "In a redox reaction, reduction is:", "gain of electrons",
          ["loss of electrons", "loss of neutrons", "gain of protons"], "Reduction is gain of electrons.")
        a("Electrolysis", "The electrolyte in a simple cell is usually a:", "solution that conducts electricity",
          ["metal rod", "plastic cover", "glass tube"], "An electrolyte conducts electricity when molten or in solution.")
        a("Electrolysis", "Electroplating is used to:", "coat a metal with another metal",
          ["melt metals", "separate gases", "make acids"], "Electroplating deposits a thin metal coating.")
        a("Metals and Their Compounds", "The metal used in galvanising iron is:", "zinc",
          ["copper", "tin", "lead"], "Zinc coating protects iron from rusting.")
        a("Metals and Their Compounds", "The ore of iron is:", "haematite",
          ["bauxite", "galena", "cassiterite"], "Haematite (Fe\u2082O\u2083) is the main iron ore.")
        a("Metals and Their Compounds", "The ore of aluminium is:", "bauxite",
          ["haematite", "galena", "cassiterite"], "Bauxite is the ore of aluminium.")
        a("Non-Metals and Their Compounds", "The gas used in balloons because it is light and safe is:", "helium",
          ["hydrogen", "oxygen", "nitrogen"], "Helium is light and does not burn.")
        a("Non-Metals and Their Compounds", "The main gas in the air is:", "nitrogen",
          ["oxygen", "carbon dioxide", "argon"], "Air is about 78% nitrogen.")
        a("Non-Metals and Their Compounds", "The percentage of oxygen in air is about:", "21%",
          ["78%", "1%", "50%"], "Air is about 21% oxygen.")
    if subj == "Biology":
        vitamins = [("Vitamin A", "night blindness"), ("Vitamin B1", "beriberi"), ("Vitamin C", "scurvy"),
                    ("Vitamin D", "rickets"), ("Vitamin B3 (niacin)", "pellagra"), ("Iodine", "goitre"),
                    ("Iron", "anaemia"), ("Vitamin K", "poor blood clotting")]
        for nut, disease in vitamins:
            others = [n for n, d in vitamins if n != nut][:3]
            a("Nutrition", f"Which nutrient deficiency causes {disease}?", nut, others,
              f"{disease} is caused by deficiency of {nut}.")
        diseases = [("malaria", "Plasmodium (a protozoan)"), ("cholera", "Vibrio cholerae (a bacterium)"),
                    ("tuberculosis", "Mycobacterium tuberculosis (a bacterium)"), ("HIV/AIDS", "human immunodeficiency virus"),
                    ("ringworm", "a fungus"), ("sleeping sickness", "Trypanosoma (a protozoan)"),
                    ("measles", "a virus"), ("typhoid", "Salmonella typhi (a bacterium)")]
        for dis_name, cause in diseases:
            others = [n for n, c in diseases if n != dis_name][:3]
            a("Health and Disease", f"Which disease is caused by {cause}?", dis_name, others,
              f"{dis_name.capitalize()} is caused by {cause}.")
        examples = [("mammal", "whale", ["lizard", "eagle", "frog"]),
                    ("bird", "eagle", ["bat", "whale", "lizard"]),
                    ("reptile", "lizard", ["eagle", "whale", "frog"]),
                    ("amphibian", "frog", ["lizard", "eagle", "whale"]),
                    ("fish", "shark", ["whale", "eagle", "frog"]),
                    ("insect", "butterfly", ["spider", "snail", "earthworm"]),
                    ("arachnid", "spider", ["butterfly", "snail", "earthworm"]),
                    ("mollusc", "snail", ["spider", "butterfly", "earthworm"])]
        for group, ex, dis in examples:
            a("Classification", f"Which of these is a {group}?", ex, dis,
              f"The {ex} is a {group}.")
        enzymes = [("amylase", "starch"), ("pepsin", "protein"), ("lipase", "fats (lipids)"),
                   ("trypsin", "protein"), ("maltase", "maltose"), ("sucrase", "sucrose")]
        for enz, sub in enzymes:
            others = list(dict.fromkeys(s for e, s in enzymes if s != sub))[:3]
            a("Physiology", f"The enzyme {enz} digests:", sub, others, f"{enz} acts on {sub}.")
        a("Physiology", "The organ that filters blood and makes urine is the:", "kidney",
          ["liver", "heart", "lung"], "Kidneys filter blood and form urine.")
        a("Physiology", "The organ that stores bile is the:", "gall bladder",
          ["liver", "pancreas", "spleen"], "Bile made by the liver is stored in the gall bladder.")
        a("Physiology", "The part of the plant where photosynthesis is greatest is the:", "leaf blade",
          ["root", "stem", "flower"], "The leaf blade has the most chlorophyll.")
        a("Physiology", "The opening and closing of stomata is controlled by:", "guard cells",
          ["xylem", "phloem", "epidermis"], "Guard cells open and close the stomata.")
        a("Physiology", "Transpiration is the loss of water from a plant through the:", "leaves",
          ["roots", "flowers", "stem only"], "Water vapour leaves through the stomata in leaves.")
        a("Physiology", "The part of a flower that receives pollen is the:", "stigma",
          ["anther", "ovary", "filament"], "Pollen lands on the stigma.")
        a("Physiology", "The female part of a flower is the:", "pistil (carpel)",
          ["stamen", "anther", "petal"], "The pistil contains stigma, style and ovary.")
        a("Physiology", "The male part of a flower is the:", "stamen",
          ["pistil", "ovary", "sepal"], "The stamen is anther plus filament.")
        a("Genetics", "A person with genotype AA is:", "homozygous dominant",
          ["heterozygous", "homozygous recessive", "carrier"], "AA has two identical dominant alleles.")
        a("Genetics", "A person with genotype Aa is:", "heterozygous",
          ["homozygous dominant", "homozygous recessive", "haploid"], "Aa has two different alleles.")
        a("Genetics", "A cross between AA and aa gives offspring that are all:", "Aa",
          ["AA", "aa", "A"], "All offspring receive A from one parent and a from the other.")
        a("Genetics", "The sex chromosomes in a human female are:", "XX",
          ["XY", "YY", "XO"], "Females are XX; males are XY.")
        a("Genetics", "The sex chromosomes in a human male are:", "XY",
          ["XX", "YY", "XO"], "Males are XY.")
        a("Ecology", "The study of the relationships between organisms and their environment is:", "ecology",
          ["genetics", "physiology", "taxonomy"], "Ecology studies organisms and their environment.")
        a("Ecology", "An organism that eats both plants and animals is a:", "omnivore",
          ["herbivore", "carnivore", "decomposer"], "Omnivores eat plants and animals.")
        a("Ecology", "An organism that eats only plants is a:", "herbivore",
          ["carnivore", "omnivore", "scavenger"], "Herbivores eat plants.")
        a("Ecology", "An organism that eats only flesh is a:", "carnivore",
          ["herbivore", "omnivore", "producer"], "Carnivores eat flesh.")
        a("Ecology", "Bacteria and fungi that break down dead matter are:", "decomposers",
          ["producers", "consumers", "parasites"], "Decomposers recycle nutrients.")
        a("Ecology", "The total number of organisms of a species in an area is its:", "population",
          ["community", "habitat", "niche"], "Population is the number of one species in an area.")
        a("Ecology", "The place where an organism lives is its:", "habitat",
          ["niche", "population", "community"], "Habitat is the organism's home.")
        a("Cell Biology", "The jelly-like substance in a cell is the:", "cytoplasm",
          ["nucleus", "vacuole", "cell wall"], "Cytoplasm fills the cell around the nucleus.")
        a("Cell Biology", "The rigid outer layer of a plant cell is the:", "cell wall",
          ["cell membrane", "cytoplasm", "nucleus"], "Plant cells have a cellulose cell wall.")
        a("Cell Biology", "Animal cells do not have a:", "cell wall", ["nucleus", "cytoplasm", "cell membrane"],
          "Animal cells lack a cell wall and chloroplasts.")
        a("Cell Biology", "Chlorophyll is found in the:", "chloroplast",
          ["mitochondrion", "nucleus", "ribosome"], "Chlorophyll sits in chloroplasts.")
        a("Nutrition", "The food test for protein uses:", "biuret solution",
          ["iodine solution", "Benedict's solution", "Sudan III"], "Biuret turns violet with protein.")
        a("Nutrition", "The food test for fats uses:", "Sudan III",
          ["iodine solution", "biuret solution", "Benedict's solution"], "Sudan III stains fats red.")
        a("Nutrition", "The main function of carbohydrates is to provide:", "energy",
          ["growth", "protection", "warmth only"], "Carbohydrates are the main energy food.")
        a("Nutrition", "The main function of proteins is:", "growth and repair",
          ["energy only", "protection from disease", "insulation"], "Proteins build and repair body tissues.")
        a("Nutrition", "The main function of fats is to provide:", "energy and insulation",
          ["growth only", "oxygen", "water"], "Fats give energy and insulate the body.")
        a("Transport", "The blood vessel that carries blood away from the heart is the:", "artery",
          ["vein", "capillary", "lymph vessel"], "Arteries carry blood away from the heart.")
        a("Transport", "The blood vessel that carries blood towards the heart is the:", "vein",
          ["artery", "capillary", "aorta"], "Veins return blood to the heart.")
        a("Transport", "The smallest blood vessels are the:", "capillaries",
          ["arteries", "veins", "aorta"], "Capillaries are tiny vessels where exchange happens.")
        a("Transport", "The liquid part of blood is the:", "plasma",
          ["serum", "haemoglobin", "platelet"], "Plasma is the fluid part of blood.")
        a("Transport", "Blood clotting is helped by the:", "platelets",
          ["red blood cells", "white blood cells", "plasma only"], "Platelets help blood to clot.")
    return E

def extra_pool2(subj):
    E = []
    def a(t, q, c, d, e): E.append(mk(0, subj, t, q, c, d, e))
    if subj == "Accounting":
        for sales, gp, exp in [(20000,8000,5000),(30000,12000,7000),(15000,6000,4000),(50000,20000,12000),
                               (10000,4000,2500),(40000,16000,9000)]:
            np_ = gp-exp
            a("Final Accounts", f"A trader made a gross profit of \u20a6{gp:,} and had expenses of \u20a6{exp:,}. Find the net profit.", f"\u20a6{np_:,}",
              [f"\u20a6{gp+exp:,}", f"\u20a6{gp:,}", f"\u20a6{np_+1000:,}"], f"Net profit = gross profit - expenses = {np_}.")
        for cost, rate in [(20000,10),(30000,5),(15000,20),(40000,10),(25000,8),(60000,5)]:
            dep = cost*rate//100
            a("Depreciation", f"Find the annual depreciation on an asset costing \u20a6{cost:,} at {rate}% per annum (straight line).", f"\u20a6{dep:,}",
              [f"\u20a6{dep+500:,}", f"\u20a6{dep*2:,}", f"\u20a6{cost:,}"], f"Depreciation = {rate}% of {cost} = {dep}.")
        for cost, rate in [(10000,10),(20000,20),(5000,10),(30000,10)]:
            dep = cost*rate//100; nbv = cost-dep
            a("Depreciation", f"An asset costing \u20a6{cost:,} is depreciated at {rate}% on the reducing balance basis. Find its net book value after one year.", f"\u20a6{nbv:,}",
              [f"\u20a6{cost:,}", f"\u20a6{dep:,}", f"\u20a6{nbv-500:,}"], f"Depreciation = {dep}; net book value = {cost} - {dep} = {nbv}.")
        for amt, rate in [(20000,5),(40000,10),(10000,2),(50000,4)]:
            disc = amt*rate//100
            a("Cash Book", f"A trade discount of {rate}% is given on goods worth \u20a6{amt:,}. How much is paid?", f"\u20a6{amt-disc:,}",
              [f"\u20a6{amt:,}", f"\u20a6{disc:,}", f"\u20a6{amt+disc:,}"], f"Amount paid = {amt} - {disc} = {amt-disc}.")
        for ca, cl in [(50000,25000),(80000,40000),(30000,15000),(120000,60000),(60000,20000),(90000,30000)]:
            ratio = ca//cl
            a("Final Accounts", f"A business has current assets of \u20a6{ca:,} and current liabilities of \u20a6{cl:,}. Find the current ratio.", f"{ratio}:1",
              [f"{ratio+1}:1", f"1:{ratio}", f"{cl//1000}:{ca//1000}"], f"Current ratio = current assets / current liabilities = {ratio}:1.")
        for cap, profit in [(100000,20000),(50000,10000),(200000,40000),(80000,16000)]:
            pct = profit*100//cap
            a("Final Accounts", f"A business with capital of \u20a6{cap:,} made a profit of \u20a6{profit:,}. Find the return on capital.", f"{pct}%",
              [f"{pct+5}%", f"{pct-5}%", f"{pct*2}%"], f"Return = profit/capital x 100 = {pct}%.")
        a("Double Entry", "The debit side of an account is the:", "left-hand side",
          ["right-hand side", "top", "bottom"], "Debits are recorded on the left.")
        a("Double Entry", "The credit side of an account is the:", "right-hand side",
          ["left-hand side", "top", "bottom"], "Credits are recorded on the right.")
        a("Double Entry", "To increase an asset account, you:", "debit it", ["credit it", "close it", "ignore it"],
          "Assets increase on the debit side.")
        a("Double Entry", "To increase a liability account, you:", "credit it", ["debit it", "close it", "ignore it"],
          "Liabilities increase on the credit side.")
        a("Double Entry", "To increase capital, you:", "credit the capital account", ["debit the capital account", "close the capital account", "open a new account"],
          "Capital is a credit balance; it increases by crediting.")
        a("Source Documents", "A document that shows goods bought on credit is a:", "purchase invoice",
          ["receipt", "cheque", "pay-in slip"], "The supplier's invoice records a credit purchase.")
        a("Source Documents", "A document that shows money received is a:", "receipt",
          ["invoice", "order", "delivery note"], "A receipt acknowledges payment received.")
        a("Source Documents", "A cheque is a document that instructs a bank to:", "pay money",
          ["receive money", "lend money", "save money"], "A cheque orders the bank to pay.")
        a("Books of Original Entry", "Sales on credit are first recorded in the:", "sales day book",
          ["purchases day book", "cash book", "returns inwards book"], "Credit sales go in the sales day book.")
        a("Books of Original Entry", "Purchases on credit are first recorded in the:", "purchases day book",
          ["sales day book", "cash book", "returns outwards book"], "Credit purchases go in the purchases day book.")
        a("Books of Original Entry", "Goods returned by customers are recorded in the:", "returns inwards book",
          ["returns outwards book", "sales day book", "cash book"], "Returns inwards records goods returned by customers.")
        a("Books of Original Entry", "Goods returned to suppliers are recorded in the:", "returns outwards book",
          ["returns inwards book", "purchases day book", "cash book"], "Returns outwards records goods sent back to suppliers.")
        a("Trial Balance", "A trial balance with equal debit and credit totals proves that:", "the ledger is arithmetically correct",
          ["there are no errors at all", "the business made a profit", "all debts are paid"],
          "It proves arithmetical accuracy only; some errors (e.g. omission) do not affect it.")
        a("Trial Balance", "An error that does not affect the trial balance is an error of:", "omission",
          ["addition", "subtraction", "transposition"], "Omission leaves both sides equally understated.")
        a("Final Accounts", "The cost of goods sold equals opening stock plus purchases minus:", "closing stock",
          ["sales", "gross profit", "expenses"], "COGS = opening stock + purchases - closing stock.")
        a("Final Accounts", "Carriage inwards is added to:", "the cost of goods", ["sales", "expenses", "capital"],
          "Carriage inwards is part of the cost of purchases.")
        a("Final Accounts", "Carriage outwards is treated as a:", "selling expense",
          ["cost of goods", "capital item", "liability"], "Carriage outwards is an expense in the profit and loss account.")
        a("Final Accounts", "Bad debts are:", "debts that will never be paid",
          ["debts paid early", "debts paid in full", "loans from banks"], "Bad debts are written off as an expense.")
        a("Final Accounts", "A provision for doubtful debts is made for debts that:", "may not be paid",
          ["have been paid", "will certainly be paid", "are not yet due"], "It is a prudent estimate of debts at risk.")
        a("Partnership Accounts", "Partners share profits according to the:", "partnership deed",
          ["memorandum", "trial balance", "balance sheet"], "The deed states the profit-sharing ratio.")
        a("Partnership Accounts", "Interest on capital is:", "a reward to partners for capital contributed",
          ["a tax", "a loan", "an expense of the firm only"], "Partners may be paid interest on their capital.")
        a("Partnership Accounts", "A partner's drawings are recorded in the partner's:", "drawings account",
          ["capital account only", "current account only", "loan account"], "Drawings are recorded separately.")
        a("Company Accounts", "The document that states a company's objects is the:", "memorandum of association",
          ["articles of association", "prospectus", "certificate of incorporation"],
          "The memorandum sets out the company's objects and powers.")
        a("Company Accounts", "The document that states a company's internal rules is the:", "articles of association",
          ["memorandum of association", "prospectus", "balance sheet"], "The articles govern internal management.")
        a("Company Accounts", "A debenture is a:", "long-term loan to a company",
          ["share in a company", "dividend", "tax"], "Debenture holders are lenders, not owners.")
        a("Company Accounts", "Debenture interest is paid:", "whether or not the company makes a profit",
          ["only when profit is made", "only to shareholders", "only at year end"], "Interest on debentures must be paid.")
        a("Ethics", "The body that regulates accountants in Nigeria is:", "ICAN (Institute of Chartered Accountants of Nigeria)",
          ["CBN", "SEC", "CAC"], "ICAN is the professional body for chartered accountants in Nigeria.")
        a("Ethics", "ANAN stands for:", "Association of National Accountants of Nigeria",
          ["Association of Nigerian Auditors", "Accounting Network of Nigeria", "Association of National Auditors"],
          "ANAN is the Association of National Accountants of Nigeria.")
        a("Information Technology", "A spreadsheet is useful in accounting for:", "calculations and tables",
          ["writing letters only", "drawing pictures", "playing music"], "Spreadsheets handle figures and formulas.")
        a("Branch Accounts", "Goods sent to a branch are recorded in the head office books as:", "goods sent to branch",
          ["sales", "purchases", "drawings"], "Goods sent to a branch are not sales.")
        a("Departmental Accounts", "Common expenses in departmental accounts are shared on a:", "fair basis such as floor area or sales",
          ["random basis", "equal basis always", "manager's choice only"], "Common costs are apportioned on a reasonable basis.")
    if subj == "Economics":
        for p1, q1, p2, q2 in [(20,200,25,160),(30,150,40,120),(10,500,15,400),(50,80,60,64)]:
            ed = abs((q2-q1)/q1) / abs((p2-p1)/p1)
            a("Demand and Supply", f"Price rises from \u20a6{p1} to \u20a6{p2} and quantity demanded falls from {q1} to {q2}. Find the price elasticity of demand.", fmt_num(ed),
              [fmt_num(ed+0.3), fmt_num(ed+1), fmt_num(ed+2)], f"Ed = %\u0394Q / %\u0394P = {fmt_num(ed)}.")
        for data in [[8,12,16,20,24],[6,9,12,15],[20,40,60],[5,15,25,35,45],[100,200,300]]:
            m = sum(data)/len(data)
            a("Tools of Analysis", f"Find the mean of {', '.join(map(str,data))}.", fmt_num(m),
              [fmt_num(m+1), fmt_num(m-1), fmt_num(m+2)], f"Mean = {sum(data)}/{len(data)} = {fmt_num(m)}.")
        for data in [[3,7,11,15,19],[2,8,14,20],[10,30,50,70]]:
            a("Tools of Analysis", f"Find the range of {', '.join(map(str,data))}.", str(max(data)-min(data)),
              [str(max(data)), str(max(data)-min(data)-2), str(min(data))], f"Range = {max(data)} - {min(data)} = {max(data)-min(data)}.")
        a("Demand and Supply", "A fall in the price of a complementary good will:", "increase the demand for the good",
          ["decrease the demand for the good", "not affect demand", "decrease the supply of the good"],
          "Complements are used together, so cheaper complements raise demand.")
        a("Demand and Supply", "An increase in the price of a good will cause:", "a contraction of demand",
          ["an increase in demand", "a shift in demand", "a fall in supply"], "A price rise moves along the demand curve (contraction).")
        a("Demand and Supply", "A fall in the price of a good will cause:", "an extension of demand",
          ["a contraction of demand", "a fall in demand", "a rise in supply"], "A price fall moves along the demand curve (extension).")
        a("Demand and Supply", "Demand for a good is elastic when a price change causes a:", "more than proportionate change in quantity demanded",
          ["less than proportionate change", "no change", "equal change only"], "Elastic demand responds strongly to price.")
        a("Demand and Supply", "The demand for salt is usually:", "inelastic",
          ["elastic", "perfectly elastic", "unitary"], "Salt has few substitutes and is a small part of spending.")
        a("Production", "The short run is a period in which:", "at least one factor is fixed",
          ["all factors vary", "no output is possible", "prices are fixed"], "In the short run, fixed factors cannot change.")
        a("Production", "The long run is a period in which:", "all factors of production can vary",
          ["no factor can vary", "only labour varies", "only capital varies"], "In the long run all inputs are variable.")
        a("Production", "Total product divided by the number of workers is the:", "average product",
          ["marginal product", "total cost", "marginal cost"], "Average product = total product / units of labour.")
        a("Production", "The extra output from one more worker is the:", "marginal product",
          ["average product", "total product", "fixed product"], "Marginal product is the addition to total product.")
        a("Costs", "Fixed costs are costs that:", "do not change with output",
          ["rise with output", "fall to zero", "are paid only once"], "Fixed costs (rent, salaries) stay the same in the short run.")
        a("Costs", "Variable costs are costs that:", "change with output",
          ["never change", "are always zero", "are paid in advance"], "Variable costs (raw materials) rise with output.")
        a("Costs", "Total cost equals:", "fixed cost plus variable cost",
          ["fixed cost minus variable cost", "average cost times output only", "marginal cost"],
          "TC = FC + VC.")
        a("Costs", "Average cost equals:", "total cost divided by output",
          ["total cost times output", "marginal cost", "fixed cost"], "AC = TC/Q.")
        a("Market Structures", "In perfect competition, firms are:", "price takers",
          ["price makers", "monopolists", "price fixers"], "No single firm can influence the market price.")
        a("Market Structures", "A monopolist is a:", "price maker", ["price taker", "price follower", "price breaker"],
          "A monopolist sets the price.")
        a("Market Structures", "Monopolistic competition has:", "many sellers of differentiated products",
          ["one seller", "few sellers of identical products", "many sellers of identical products"],
          "Products differ (branding, quality) in monopolistic competition.")
        a("Market Structures", "An example of an oligopoly in Nigeria is the:", "cement industry",
          ["street hawking", "subsistence farming", "local market"], "A few large firms dominate cement.")
        a("National Income", "GDP per capita is GDP divided by the:", "population",
          ["number of workers", "land area", "exports"], "Per capita = total divided by population.")
        a("National Income", "GNP equals GDP plus:", "net income from abroad",
          ["exports", "imports", "taxes"], "GNP adds net factor income from abroad.")
        a("National Income", "Transfer payments such as pensions are:", "excluded from national income",
          ["included in national income", "counted as output", "counted as exports"],
          "Transfers are not payments for current production.")
        a("National Income", "Double counting is avoided in national income by counting only:", "value added",
          ["gross output", "total sales", "intermediate goods"], "Value added avoids counting the same output twice.")
        a("Money and Banking", "The money market deals in:", "short-term funds",
          ["long-term funds", "shares only", "land"], "The money market is for short-term borrowing and lending.")
        a("Money and Banking", "The capital market deals in:", "long-term funds",
          ["short-term funds", "cash only", "foreign exchange only"], "The capital market trades shares and bonds.")
        a("Money and Banking", "The Nigerian Stock Exchange trades in:", "shares and bonds",
          ["foodstuffs", "land", "cars"], "The stock market trades securities.")
        a("Money and Banking", "A rise in the bank rate will tend to:", "reduce borrowing",
          ["increase borrowing", "leave borrowing unchanged", "abolish interest"],
          "Higher interest rates discourage borrowing.")
        a("Money and Banking", "Demand-pull inflation is caused by:", "too much money chasing too few goods",
          ["falling demand", "rising output", "falling costs"], "Excess demand pulls prices up.")
        a("Money and Banking", "Cost-push inflation is caused by:", "rising costs of production",
          ["falling costs", "rising demand", "falling wages"], "Higher costs push prices up.")
        a("Money and Banking", "Unemployment in which people lack the skills for available jobs is:", "structural unemployment",
          ["frictional unemployment", "cyclical unemployment", "seasonal unemployment"],
          "Structural unemployment is a mismatch of skills.")
        a("Money and Banking", "Unemployment caused by a fall in demand in a recession is:", "cyclical unemployment",
          ["frictional unemployment", "structural unemployment", "seasonal unemployment"],
          "Cyclical unemployment follows the business cycle.")
        a("Money and Banking", "Unemployment of farm workers between planting and harvest is:", "seasonal unemployment",
          ["structural unemployment", "frictional unemployment", "cyclical unemployment"],
          "Seasonal work ends when the season ends.")
        a("Public Finance", "A progressive tax takes a:", "higher proportion from higher incomes",
          ["higher proportion from lower incomes", "fixed amount from all", "lower proportion from higher incomes"],
          "Progressive taxes rise with income.")
        a("Public Finance", "A regressive tax takes a:", "higher proportion from lower incomes",
          ["higher proportion from higher incomes", "fixed proportion from all", "no tax from the poor"],
          "Regressive taxes burden low incomes more.")
        a("Public Finance", "A proportional tax takes:", "the same proportion from all incomes",
          ["more from the rich", "more from the poor", "nothing from the rich"],
          "Proportional tax is a flat rate.")
        a("Public Finance", "VAT in Nigeria is a tax on:", "consumption of goods and services",
          ["income", "property", "exports"], "Value Added Tax is charged on goods and services.")
        a("Public Finance", "The main source of government revenue in Nigeria is:", "oil revenue",
          ["VAT only", "customs duties only", "personal income tax"], "Oil dominates federal revenue.")
        a("International Trade", "A quota is a:", "limit on the quantity of imports",
          ["tax on imports", "subsidy on exports", "ban on exports"], "Quotas restrict import quantities.")
        a("International Trade", "An embargo is a:", "total ban on trade with a country",
          ["tax on imports", "subsidy", "quota"], "An embargo prohibits trade.")
        a("International Trade", "Dumping is selling goods abroad at:", "below their cost of production",
          ["above cost", "the same price", "a fair price"], "Dumping undercuts foreign producers.")
        a("International Trade", "The balance of payments records:", "all economic transactions with the rest of the world",
          ["only exports", "only imports", "only aid"], "The balance of payments covers trade, services and capital flows.")
        a("Economic Development", "One indicator of development is:", "life expectancy",
          ["population size", "land area", "number of cars only"], "Life expectancy reflects health and living standards.")
        a("Economic Development", "The Human Development Index measures health, education and:", "income",
          ["population", "land area", "exports"], "HDI combines health, education and income.")
        a("Business Organisations", "A public corporation is owned by the:", "government",
          ["shareholders", "partners", "cooperative members"], "Public corporations are state-owned.")
        a("Business Organisations", "One advantage of a sole proprietorship is:", "quick decision-making",
          ["unlimited capital", "limited liability", "continuity after death"],
          "The owner decides alone and quickly.")
        a("Business Organisations", "One disadvantage of a partnership is:", "unlimited liability",
          ["limited liability", "quick decisions", "easy formation"], "Partners are personally liable for the firm's debts.")
    if subj == "Commerce":
        docs = [("invoice", "a bill for goods supplied"), ("receipt", "proof of payment"),
                ("credit note", "a document reducing the amount owed"), ("debit note", "a document increasing the amount owed"),
                ("delivery note", "a document listing goods delivered"), ("purchase order", "a request for goods"),
                ("quotation", "a statement of price for goods"), ("statement of account", "a summary of transactions between buyer and seller")]
        for doc, meaning in docs:
            others = [m for d, m in docs if m != meaning][:3]
            a("Trade", f"An/a {doc} is:", meaning, others, f"A {doc} is {meaning}.")
        a("Trade", "The channel of distribution is the route goods take from the:", "producer to the consumer",
          ["consumer to the producer", "wholesaler to the producer", "retailer to the wholesaler"],
          "Distribution moves goods from producer to final consumer.")
        a("Trade", "A middleman who buys and sells on behalf of others for a commission is a:", "agent",
          ["wholesaler", "retailer", "producer"], "Agents act for principals and earn commission.")
        a("Trade", "A broker is a middleman who:", "brings buyers and sellers together",
          ["buys goods for himself", "stores goods", "transports goods"], "Brokers arrange deals for a fee.")
        a("Trade", "Hire purchase allows a buyer to:", "pay for goods in instalments while using them",
          ["pay cash only", "borrow goods free", "return goods always"], "Hire purchase spreads payment over time.")
        a("Trade", "Cash on delivery means payment is made:", "when the goods are delivered",
          ["before ordering", "after one year", "never"], "COD: pay on delivery.")
        a("Aids to Trade", "The fastest means of transport for perishable goods over long distances is:", "air transport",
          ["road transport", "rail transport", "water transport"], "Air is fastest, though costly.")
        a("Aids to Trade", "The cheapest means of transporting bulky goods is:", "water transport",
          ["air transport", "road transport", "rail transport"], "Ships carry bulky goods cheaply.")
        a("Aids to Trade", "A warehouse that stores goods before duty is paid is a:", "bonded warehouse",
          ["public warehouse", "private warehouse", "cold store"], "Bonded warehouses hold dutiable goods.")
        a("Aids to Trade", "A warehouse owned by a firm for its own goods is a:", "private warehouse",
          ["public warehouse", "bonded warehouse", "cold store"], "Private warehouses serve one firm.")
        a("Aids to Trade", "Marine insurance covers risks in:", "sea transport",
          ["road transport", "air transport", "rail transport"], "Marine insurance covers goods at sea.")
        a("Aids to Trade", "Fire insurance covers loss caused by:", "fire",
          ["theft", "accident", "flood only"], "Fire policies pay for fire damage.")
        a("Aids to Trade", "Life assurance pays a sum on the:", "death of the assured",
          ["birth of a child", "marriage", "retirement only"], "Life assurance pays beneficiaries on death.")
        a("Aids to Trade", "The person who pays the insurance premium is the:", "policy holder",
          ["insurer", "broker", "agent"], "The policy holder pays premiums.")
        a("Aids to Trade", "The company that accepts the risk is the:", "insurer",
          ["policy holder", "broker", "agent"], "The insurer carries the risk.")
        a("Aids to Trade", "Indemnity in insurance means the insured is:", "restored to the position before the loss",
          ["paid double the loss", "paid a profit", "not paid at all"], "Indemnity restores, not enriches.")
        a("Aids to Trade", "Advertising through television is a form of:", "mass media advertising",
          ["personal selling", "sales promotion", "public relations"], "TV reaches a mass audience.")
        a("Aids to Trade", "A poster is an example of:", "outdoor advertising",
          ["personal selling", "direct mail", "television advertising"], "Posters are outdoor ads.")
        a("Aids to Trade", "The main purpose of a trade fair is to:", "display goods to buyers",
          ["sell goods at home", "store goods", "transport goods"], "Trade fairs exhibit products.")
        a("Finance", "A savings account is opened mainly to:", "save money and earn interest",
          ["borrow money", "pay bills only", "trade shares"], "Savings accounts encourage saving.")
        a("Finance", "A current account is used mainly for:", "day-to-day business transactions",
          ["long-term savings", "fixed deposits", "pensions"], "Current accounts handle frequent payments.")
        a("Finance", "A fixed deposit account pays:", "higher interest for money left for a fixed time",
          ["no interest", "lower interest than savings", "interest daily only"], "Fixed deposits lock money for a term at higher interest.")
        a("Finance", "A bank draft is:", "a bank's own cheque",
          ["a personal cheque", "a loan", "a savings book"], "A bank draft is drawn by a bank on itself.")
        a("Finance", "A standing order is an instruction to a bank to:", "pay a fixed sum regularly",
          ["close an account", "open an account", "lend money"], "Standing orders pay regular amounts.")
        a("Finance", "A direct debit allows a firm to:", "collect varying amounts from a customer's account",
          ["pay cash", "close accounts", "issue cheques"], "Direct debits collect amounts that vary.")
        a("Finance", "The stock exchange is a market for:", "shares and other securities",
          ["foodstuffs", "cars", "land"], "Stock exchanges trade securities.")
        a("Finance", "A shareholder is a person who:", "owns shares in a company",
          ["lends to a company", "works for a company", "buys from a company"], "Shareholders own part of the company.")
        a("Marketing", "Branding is giving a product a:", "name or mark that identifies it",
          ["price", "colour only", "package only"], "Brands identify and distinguish products.")
        a("Marketing", "Packaging protects goods and:", "attracts buyers",
          ["increases weight", "reduces quality", "hides the product"], "Good packaging protects and promotes.")
        a("Marketing", "A trademark is a:", "legally protected brand name or symbol",
          ["price tag", "receipt", "invoice"], "Trademarks are registered and protected by law.")
        a("Marketing", "Sales promotion includes:", "free samples and discounts",
          ["transport", "storage", "insurance"], "Promotions encourage quick buying.")
        a("Consumer Protection", "A consumer who buys a faulty product should first complain to the:", "seller",
          ["police", "court", "government"], "The seller should be given a chance to put it right.")
        a("Consumer Protection", "The Standards Organisation of Nigeria (SON) ensures products meet:", "approved standards",
          ["low prices", "foreign tastes", "advertising rules"], "SON sets and enforces standards.")
        a("International Trade", "Imports are goods:", "bought from other countries",
          ["sold to other countries", "made at home", "stored at home"], "Imports enter the country.")
        a("International Trade", "The document that allows goods to leave a country is the:", "export licence",
          ["import licence", "bill of lading", "invoice"], "Export licences permit exports.")
        a("International Trade", "A bill of lading is a document used in:", "sea transport",
          ["road transport", "air transport", "rail transport"], "The bill of lading is the shipping document.")
        a("International Trade", "An airway bill is used in:", "air transport",
          ["sea transport", "road transport", "rail transport"], "Airway bills cover air freight.")
        a("International Trade", "Customs duty is a tax on:", "imported and exported goods",
          ["local goods only", "services only", "land"], "Customs duties are charged at the border.")
    return E

def extra_pool3(subj):
    E = []
    def a(t, q, c, d, e): E.append(mk(0, subj, t, q, c, d, e))
    if subj == "Computer":
        acronyms = [("CPU","Central Processing Unit"),("RAM","Random Access Memory"),
                    ("ROM","Read Only Memory"),("LAN","Local Area Network"),("WAN","Wide Area Network"),
                    ("URL","Uniform Resource Locator"),("HTML","HyperText Markup Language"),
                    ("HTTP","HyperText Transfer Protocol"),("WWW","World Wide Web"),
                    ("ICT","Information and Communication Technology"),("GUI","Graphical User Interface"),
                    ("OS","Operating System"),("USB","Universal Serial Bus"),
                    ("CD","Compact Disc"),("DVD","Digital Versatile Disc"),
                    ("PDF","Portable Document Format"),("SMS","Short Message Service"),
                    ("Wi-Fi","Wireless Fidelity"),("IP","Internet Protocol"),
                    ("DNS","Domain Name System"),("ISP","Internet Service Provider")]
        for ab, full in acronyms:
            others = [f for x, f in acronyms if f != full][:3]
            a("Fundamentals", f"What does {ab} stand for?", full, others, f"{ab} stands for {full}.")
        exts = [(".docx","Word document"),(".xlsx","Excel spreadsheet"),(".pptx","PowerPoint presentation"),
                (".pdf","PDF document"),(".jpg","image file"),(".mp3","audio file"),(".mp4","video file"),
                (".txt","plain text file"),(".zip","compressed file"),(".html","web page file")]
        for ext, meaning in exts:
            others = [m for x, m in exts if m != meaning][:3]
            a("Files", f"A file with the extension {ext} is a:", meaning, others,
              f"{ext} indicates a {meaning}.")
        for kb in [1,2,4,8,10]:
            a("Fundamentals", f"How many bytes are in {kb} kilobyte(s)?", f"{kb*1024} bytes",
              [f"{kb*1000} bytes", f"{kb*1024+100} bytes", f"{kb} bytes"], f"1 KB = 1024 bytes, so {kb} KB = {kb*1024} bytes.")
        for mb in [1,2,5,10]:
            a("Fundamentals", f"How many kilobytes are in {mb} megabyte(s)?", f"{mb*1024} KB",
              [f"{mb*1000} KB", f"{mb*1024+100} KB", f"{mb} KB"], f"1 MB = 1024 KB, so {mb} MB = {mb*1024} KB.")
        devices = [("keyboard","input"),("mouse","input"),("scanner","input"),("microphone","input"),
                   ("monitor","output"),("printer","output"),("speaker","output"),("projector","output"),
                   ("hard disk","storage"),("flash drive","storage"),("CD-ROM","storage"),("memory card","storage")]
        for dev, kind in devices:
            others = [k for k in ["input", "output", "storage", "processing"] if k != kind][:3]
            a("Hardware", f"A {dev} is a/an {kind} device. Which type of device is a {dev}?", kind, others[:3],
              f"The {dev} is a {kind} device.")
        a("Hardware", "The device that prints on paper is the:", "printer",
          ["monitor", "scanner", "speaker"], "A printer produces hard copy.")
        a("Hardware", "The device that captures images from paper is the:", "scanner",
          ["printer", "monitor", "speaker"], "A scanner digitises paper documents.")
        a("Software", "Word processing software is used to:", "create and edit documents",
          ["calculate figures", "browse the internet", "play music"], "Word processors handle text documents.")
        a("Software", "Spreadsheet software is used to:", "work with numbers in tables",
          ["write letters", "browse the internet", "edit photos"], "Spreadsheets organise data in rows and columns.")
        a("Software", "Presentation software is used to:", "create slides for talks",
          ["store data", "browse the internet", "send email"], "Presentation software makes slide shows.")
        a("Software", "Database software is used to:", "store and organise large amounts of data",
          ["draw pictures", "play games", "browse the internet"], "Databases store structured records.")
        a("Software", "An example of a web browser is:", "Google Chrome",
          ["Microsoft Word", "Excel", "Paint"], "Chrome is a browser.")
        a("Software", "An example of a search engine is:", "Google",
          ["Chrome", "Windows", "Word"], "Google is a search engine.")
        a("ICT", "Email is sent over the:", "internet", ["radio", "television", "telephone line only"],
          "Email travels over the internet.")
        a("ICT", "A website address begins with:", "www or http",
          ["@ only", "# only", "file:// only"], "Web addresses start with http/https or www.")
        a("ICT", "Social media platforms are used for:", "sharing information and connecting with people",
          ["storing files only", "printing documents", "scanning images"], "Social media connects people online.")
        a("ICT", "One danger of the internet is:", "cyberbullying and fraud",
          ["faster communication", "online learning", "e-commerce"], "The internet also carries risks such as fraud.")
        a("Ethics", "Copyright protects:", "the rights of creators of original work",
          ["the rights of buyers", "public property", "government secrets"], "Copyright gives creators control over their work.")
        a("Ethics", "A strong password should contain:", "a mix of letters, numbers and symbols",
          ["only your name", "only numbers", "your date of birth"], "Mixed characters make passwords harder to guess.")
        a("Problem Solving", "The first step in problem solving is to:", "identify the problem",
          ["write the program", "test the program", "buy a computer"], "You must understand the problem first.")
        a("Problem Solving", "Pseudocode is:", "a plain-language description of an algorithm",
          ["a programming language", "a flowchart", "a computer program"], "Pseudocode describes steps in words.")
    if subj == "Agric":
        tools = [("cutlass","cutting weeds and clearing bush"),("hoe","tilling and weeding soil"),
                 ("rake","levelling soil and gathering leaves"),("spade","digging soil"),
                 ("sickle","harvesting crops"),("watering can","watering crops"),
                 ("wheelbarrow","carrying loads"),("axe","cutting wood"),
                 ("machete","cutting bush"),("shovel","digging and moving soil")]
        for tool, use in tools:
            others = [u for t, u in tools if u != use][:3]
            a("Agricultural Technology", f"A {tool} is used for:", use, others, f"A {tool} is used for {use}.")
        young = [("cow","calf"),("sheep","lamb"),("goat","kid"),("pig","piglet"),("hen","chick"),
                 ("dog","puppy"),("cat","kitten"),("horse","foal"),("duck","duckling"),("rabbit","kit")]
        for animal, baby in young:
            others = [b for an, b in young if b != baby][:3]
            a("Animal Production", f"The young of a {animal} is called a:", baby, others,
              f"A young {animal} is a {baby}.")
        gest = [("cow",283),("sow",114),("ewe",150),("goat",150),("mare",340)]
        for animal, days in gest:
            others = list(dict.fromkeys(f"{d} days" for an, d in gest if d != days))[:3]
            a("Animal Production", f"The gestation period of a {animal} is about:", f"{days} days", others,
              f"A {animal} carries its young for about {days} days.")
        a("Animal Production", "Castration in farm animals is done to:", "control breeding and improve meat quality",
          ["increase milk", "cure disease", "increase size only"], "Castration removes the testes.")
        a("Animal Production", "Dehorning is the removal of:", "horns", ["tails", "teeth", "hooves"],
          "Dehorning removes horns for safety.")
        a("Animal Production", "Docking in sheep is the removal of the:", "tail",
          ["horn", "ear", "leg"], "Docking shortens the tail.")
        a("Animal Production", "Vaccination protects animals against:", "disease",
          ["hunger", "cold", "thirst"], "Vaccines build immunity to disease.")
        a("Animal Production", "The feed given to poultry for egg laying is called:", "layers' mash",
          ["broiler mash", "creep feed", "hay"], "Layers' mash is formulated for laying hens.")
        a("Animal Production", "Roughage in animal feed provides:", "fibre",
          ["protein only", "vitamins only", "water"], "Roughage is fibrous feed such as grass and hay.")
        a("Animal Production", "Concentrates in animal feed are rich in:", "protein and energy",
          ["fibre only", "water only", "roughage"], "Concentrates are energy- and protein-rich feeds.")
        a("Agronomy", "The planting of seeds at the correct depth helps:", "germination",
          ["flowering only", "harvesting", "storage"], "Correct depth gives good germination.")
        a("Agronomy", "Thinning is the removal of:", "excess seedlings",
          ["weeds only", "old plants", "flowers"], "Thinning leaves the right spacing.")
        a("Agronomy", "Pruning is the removal of:", "unwanted branches",
          ["roots", "fruits", "leaves only"], "Pruning shapes the plant and improves yield.")
        a("Agronomy", "Staking is done to support:", "climbing crops such as yam",
          ["root crops", "cereals", "trees"], "Yam vines are staked for support.")
        a("Agronomy", "The best time to harvest maize for grain is when the:", "grains are dry and hard",
          ["leaves are green", "plant is flowering", "cob is soft"], "Dry, hard grains store well.")
        a("Agronomy", "Yam is propagated by:", "seed yam (setts)", ["seeds", "cuttings", "suckers"],
          "Yam is planted from pieces of tuber called setts.")
        a("Agronomy", "Cassava is propagated by:", "stem cuttings", ["seeds", "tubers", "suckers"],
          "Cassava is planted from stem cuttings.")
        a("Agronomy", "Banana is propagated by:", "suckers", ["seeds", "cuttings", "tubers"],
          "Banana is planted from suckers.")
        a("Agronomy", "A cover crop is grown mainly to:", "protect the soil",
          ["produce food only", "produce timber", "feed animals only"], "Cover crops protect soil from erosion.")
        a("Agronomy", "Green manure is:", "a crop ploughed into the soil to enrich it",
          ["chemical fertiliser", "animal dung only", "compost only"], "Green manure adds organic matter and nitrogen.")
        a("Agronomy", "Compost is made from:", "decayed plant and animal matter",
          ["chemicals only", "sand", "clay"], "Compost is decomposed organic matter.")
        a("Agronomy", "Farmyard manure is:", "animal dung and litter",
          ["chemical fertiliser", "green manure", "compost only"], "Farmyard manure comes from animal waste.")
        a("Agricultural Economics", "The demand for farm produce is affected by:", "price and income",
          ["soil type only", "rainfall only", "farm size only"], "Price and income shift demand.")
        a("Agricultural Economics", "A cooperative helps farmers by:", "buying inputs cheaply and marketing produce together",
          ["lending land", "paying taxes", "building roads"], "Cooperatives give farmers bargaining power.")
        a("Agricultural Economics", "The main source of farm credit in Nigeria is the:", "Bank of Agriculture",
          ["Central Bank only", "commercial banks only", "market women"], "The Bank of Agriculture lends to farmers.")
        a("Agricultural Extension", "The extension worker's main job is to:", "teach farmers new methods",
          ["sell land", "collect tax", "buy produce"], "Extension links research and farmers.")
        a("Forestry", "A tree crop that gives timber is:", "mahogany",
          ["cocoa", "oil palm", "rubber"], "Mahogany is a timber tree.")
        a("Forestry", "Rubber is tapped for its:", "latex", ["timber", "fruit", "leaves"],
          "Rubber trees yield latex.")
        a("Fisheries", "The best water for fish farming is:", "clean, oxygen-rich water",
          ["dirty water", "salty water only", "hot water"], "Fish need clean, oxygenated water.")
        a("Fisheries", "Fish feed mainly on:", "plankton and formulated feed",
          ["grass only", "leaves only", "soil"], "Fish eat plankton and prepared feed.")
        a("General Agriculture", "Shifting cultivation involves:", "farming a plot, then leaving it fallow",
          ["farming the same plot forever", "irrigation only", "terracing only"],
          "Shifting cultivation moves to new land after a few years.")
        a("General Agriculture", "A fallow period allows the soil to:", "regain fertility",
          ["lose fertility", "dry out", "become acidic"], "Fallow lets the soil recover.")
    if subj == "Geography":
        capitals = [("Nigeria","Abuja"),("Ghana","Accra"),("Kenya","Nairobi"),("Egypt","Cairo"),
                    ("South Africa","Pretoria"),("Ethiopia","Addis Ababa"),("France","Paris"),
                    ("Germany","Berlin"),("Italy","Rome"),("Spain","Madrid"),("Portugal","Lisbon"),
                    ("United Kingdom","London"),("Russia","Moscow"),("China","Beijing"),("India","New Delhi"),
                    ("Japan","Tokyo"),("Australia","Canberra"),("Canada","Ottawa"),("Brazil","Brasilia"),
                    ("United States","Washington D.C."),("Mexico","Mexico City"),("Argentina","Buenos Aires"),
                    ("Turkey","Ankara"),("Saudi Arabia","Riyadh"),("Iran","Tehran"),("Iraq","Baghdad"),
                    ("Pakistan","Islamabad"),("Bangladesh","Dhaka"),("Indonesia","Jakarta"),
                    ("Thailand","Bangkok"),("Vietnam","Hanoi"),("South Korea","Seoul"),("Poland","Warsaw"),
                    ("Netherlands","Amsterdam"),("Belgium","Brussels"),("Switzerland","Bern"),
                    ("Austria","Vienna"),("Greece","Athens"),("Morocco","Rabat"),("Algeria","Algiers"),
                    ("Libya","Tripoli"),("Sudan","Khartoum"),("Senegal","Dakar"),("Mali","Bamako"),
                    ("Cote d'Ivoire","Yamoussoukro"),("Cameroon","Yaounde"),("Angola","Luanda"),
                    ("Zambia","Lusaka"),("Zimbabwe","Harare"),("Tanzania","Dodoma")]
        for country, cap in capitals:
            others = [co for co, c in capitals if co != country][:3]
            a("Regional Geography", f"{cap} is the capital of which country?", country, others,
              f"{cap} is the capital of {country}.")
        rivers = [("Niger","Nigeria"),("Benue","Nigeria"),("Nile","Egypt/Sudan"),("Congo","DR Congo"),
                  ("Zambezi","Zambia/Zimbabwe"),("Orange","South Africa"),("Amazon","Brazil"),
                  ("Danube","Europe"),("Thames","England"),("Volga","Russia")]
        for river, place in rivers:
            others = list(dict.fromkeys(p for r, p in rivers if p != place))[:3]
            a("Physical Geography", f"The River {river} is found in:", place, others,
              f"The River {river} flows through {place}.")
        a("Physical Geography", "The largest lake in Africa is:", "Lake Victoria",
          ["Lake Chad", "Lake Tanganyika", "Lake Malawi"], "Lake Victoria is Africa's largest lake.")
        a("Physical Geography", "The deepest lake in the world is:", "Lake Baikal",
          ["Lake Victoria", "Lake Tanganyika", "Lake Chad"], "Lake Baikal in Russia is the deepest.")
        a("Physical Geography", "The longest mountain range in the world is the:", "Andes",
          ["Himalayas", "Alps", "Rockies"], "The Andes run along South America's west coast.")
        a("Physical Geography", "The highest mountain in the world is:", "Mount Everest",
          ["Mount Kilimanjaro", "Mount Kenya", "K2"], "Everest (8,849 m) is the world's highest peak.")
        a("Physical Geography", "The Atlas Mountains are in:", "North Africa",
          ["East Africa", "West Africa", "Southern Africa"], "The Atlas range crosses Morocco, Algeria and Tunisia.")
        a("Physical Geography", "The Jos Plateau is in:", "Nigeria",
          ["Ghana", "Cameroon", "Kenya"], "The Jos Plateau is in Plateau State, Nigeria.")
        a("Physical Geography", "The Mambilla Plateau is in:", "Taraba State, Nigeria",
          ["Plateau State", "Borno State", "Kano State"], "The Mambilla Plateau is in Taraba State.")
        a("Physical Geography", "The climate of southern Nigeria is mainly:", "tropical rainforest",
          ["desert", "Mediterranean", "temperate"], "The south has a wet tropical rainforest climate.")
        a("Physical Geography", "The climate of northern Nigeria is mainly:", "tropical savanna / semi-arid",
          ["rainforest", "Mediterranean", "temperate"], "The north is drier savanna, grading to semi-arid.")
        a("Physical Geography", "The harmattan is a:", "dry, dusty wind from the Sahara",
          ["wet wind from the sea", "cold wind from Europe", "wind from the forest"],
          "The harmattan blows dry dust from the Sahara in the dry season.")
        a("Physical Geography", "The rainy season in southern Nigeria is mainly caused by the:", "south-west monsoon winds",
          ["harmattan", "north-east trade winds", "sea breeze only"], "The moist south-west monsoon brings rain.")
        a("Physical Geography", "The dry season in Nigeria is caused by the:", "north-east trade winds (harmattan)",
          ["south-west monsoon", "sea breeze", "land breeze"], "The dry north-east trades bring the dry season.")
        a("Human Geography", "The largest city in Nigeria is:", "Lagos",
          ["Abuja", "Kano", "Ibadan"], "Lagos is Nigeria's largest city.")
        a("Human Geography", "The capital of Nigeria before Abuja was:", "Lagos",
          ["Ibadan", "Kano", "Enugu"], "Lagos was the capital until 1991.")
        a("Human Geography", "Kano is famous for its:", "groundnut pyramids and trade",
          ["oil wells", "fishing", "timber"], "Kano was famous for groundnut trade.")
        a("Human Geography", "The main seaport of Nigeria is:", "Lagos (Apapa)",
          ["Port Harcourt", "Calabar", "Warri"], "Apapa in Lagos is the main seaport.")
        a("Economic Geography", "Cocoa is mainly grown in:", "south-western Nigeria",
          ["northern Nigeria", "the Niger Delta", "the Jos Plateau"], "Cocoa grows in the south-west rainforest zone.")
        a("Economic Geography", "Groundnut is mainly grown in:", "northern Nigeria",
          ["southern Nigeria", "the Niger Delta", "the coastal zone"], "Groundnut is a northern crop.")
        a("Economic Geography", "Oil palm is mainly grown in:", "south-eastern Nigeria",
          ["northern Nigeria", "the Jos Plateau", "the Sahel"], "Oil palm grows in the south-east rainforest zone.")
        a("Economic Geography", "Tin mining in Nigeria is centred on the:", "Jos Plateau",
          ["Mambilla Plateau", "Obudu Plateau", "Biu Plateau"], "Tin is mined on the Jos Plateau.")
        a("Economic Geography", "Coal mining in Nigeria is centred on:", "Enugu",
          ["Jos", "Kano", "Lagos"], "Coal was mined at Enugu.")
        a("Economic Geography", "Iron ore in Nigeria is found at:", "Itakpe",
          ["Enugu", "Jos", "Kano"], "Itakpe in Kogi State has iron ore.")
        a("Map Work", "A map that shows height uses:", "contours",
          ["isobars", "isotherms", "symbols only"], "Contours show relief.")
        a("Map Work", "The key of a map is also called the:", "legend",
          ["scale", "title", "north arrow"], "The legend explains map symbols.")
        a("Map Work", "The scale of a map shows the relationship between:", "map distance and ground distance",
          ["height and depth", "latitude and longitude", "time and distance"],
          "Scale relates map distance to ground distance.")
        a("Environmental Geography", "Gully erosion is common in:", "south-eastern Nigeria",
          ["the Sahara", "the coast", "the Jos Plateau"], "Gully erosion affects the south-east.")
        a("Environmental Geography", "Flooding in Lagos is worsened by:", "poor drainage and low-lying land",
          ["high mountains", "desert winds", "cold weather"], "Lagos is low-lying with heavy rain and poor drainage.")
        a("Environmental Geography", "Afforestation helps to check:", "desert encroachment",
          ["flooding only", "earthquakes", "volcanoes"], "Planting trees checks desertification.")
    if subj == "Government":
        a("Basic Concepts", "Power is the ability to:", "make others do what you want",
          ["obey laws", "pay taxes", "vote"], "Power is the capacity to influence others.")
        a("Basic Concepts", "A nation is a group of people with a common:", "history, culture and language",
          ["government only", "army", "wealth"], "A nation shares identity; a state adds territory and government.")
        a("Basic Concepts", "A nation-state is a state whose people form:", "one nation",
          ["many nations", "no nation", "two nations"], "A nation-state matches one nation to one state.")
        a("Basic Concepts", "Political socialisation is the process of learning:", "political values and attitudes",
          ["farming", "trading", "reading only"], "People learn political behaviour through family, school and media.")
        a("Basic Concepts", "Political participation includes:", "voting in elections",
          ["paying tax only", "obeying laws only", "watching television"], "Voting is the main form of participation.")
        a("Basic Concepts", "Political culture is the:", "attitudes and beliefs people hold about politics",
          ["law of the land", "party manifesto", "constitution"], "Political culture shapes how people view government.")
        a("Forms of Government", "A republic is a state headed by a:", "president",
          ["king", "queen", "emir"], "A republic has an elected head, not a monarch.")
        a("Forms of Government", "Feudalism was a system based on:", "land ownership and service",
          ["trade", "industry", "democracy"], "Feudal lords held land in return for service.")
        a("Forms of Government", "Capitalism is an economic system based on:", "private ownership of the means of production",
          ["state ownership", "common ownership", "no ownership"], "Capitalism rests on private property and markets.")
        a("Forms of Government", "Socialism is based on:", "collective or state ownership",
          ["private ownership only", "no ownership", "foreign ownership"], "Socialism favours public ownership.")
        a("Forms of Government", "Communism aims for a:", "classless society",
          ["monarchy", "military rule", "theocracy"], "Communism seeks a classless, stateless society.")
        a("Forms of Government", "Totalitarianism is rule with:", "total control over all aspects of life",
          ["limited power", "free press", "free elections"], "Totalitarian regimes control politics, economy and society.")
        a("Forms of Government", "Fascism is a form of:", "extreme nationalism and dictatorship",
          ["democracy", "socialism", "liberalism"], "Fascism is authoritarian and nationalist.")
        a("Arms of Government", "The Senate President presides over the:", "Senate",
          ["House of Representatives", "Supreme Court", "Cabinet"], "The Senate President leads the Senate.")
        a("Arms of Government", "The Speaker presides over the:", "House of Representatives",
          ["Senate", "Supreme Court", "Cabinet"], "The Speaker leads the House of Representatives.")
        a("Arms of Government", "The Chief Justice of Nigeria heads the:", "judiciary",
          ["legislature", "executive", "police"], "The Chief Justice heads the judiciary.")
        a("Arms of Government", "The Supreme Court is the:", "highest court in Nigeria",
          ["lowest court", "court of appeal only", "customary court"], "The Supreme Court is the final court of appeal.")
        a("Arms of Government", "Ministers are appointed by the:", "President",
          ["Senate", "Chief Justice", "Governor"], "The President appoints ministers, subject to Senate confirmation.")
        a("Arms of Government", "Commissioners are appointed by the:", "Governor",
          ["President", "Senate", "Chairman"], "State governors appoint commissioners.")
        a("Constitution", "A written constitution is one that is:", "contained in a single document",
          ["unwritten", "based on custom only", "a military decree"], "Written constitutions are codified in one document.")
        a("Constitution", "An unwritten constitution is based on:", "customs, conventions and statutes",
          ["a single document", "a decree", "a manifesto"], "Britain has an unwritten constitution.")
        a("Constitution", "A rigid constitution is one that is:", "difficult to amend",
          ["easy to amend", "not written", "not supreme"], "Rigid constitutions need special procedures to change.")
        a("Constitution", "A flexible constitution is one that is:", "easy to amend",
          ["difficult to amend", "unwritten always", "supreme always"], "Flexible constitutions can be amended by ordinary law-making.")
        a("Constitution", "The sources of a constitution include:", "history, customs and past constitutions",
          ["party manifestos only", "newspapers", "foreign laws only"], "Constitutions draw on history and custom.")
        a("Democratic Principles", "Accountability means leaders must:", "answer for their actions",
          ["hide their actions", "avoid elections", "rule by decree"], "Accountable leaders explain their use of power.")
        a("Democratic Principles", "Representative government means citizens elect people to:", "represent them",
          ["rule them by force", "collect taxes only", "make laws for them without consent"],
          "Representatives act on behalf of the people.")
        a("Democratic Principles", "Constitutionalism means government is limited by the:", "constitution",
          ["army", "party", "president"], "Constitutionalism is government according to the constitution.")
        a("Citizenship", "Dual citizenship means a person is a citizen of:", "two countries",
          ["one country", "three countries", "no country"], "Dual citizens hold two citizenships.")
        a("Citizenship", "A citizen by birth is one born:", "in the country or to citizen parents, as the constitution provides",
          ["abroad always", "in a hospital", "to foreign parents only"], "Birth citizenship follows the constitutional rules.")
        a("Citizenship", "Naturalisation is citizenship granted to a foreigner who:", "meets the legal conditions",
          ["is rich", "is educated only", "marries a citizen only"], "Naturalisation follows legal requirements.")
        a("Political Parties", "A pressure group differs from a political party because it does not:", "contest elections to form government",
          ["influence government", "have members", "hold meetings"], "Pressure groups influence policy without seeking power.")
        a("Political Parties", "An example of a pressure group in Nigeria is the:", "Nigeria Labour Congress (NLC)",
          ["APC", "PDP", "LP"], "The NLC is a pressure group; APC, PDP and LP are parties.")
        a("Political Parties", "The electoral body in Nigeria is:", "INEC",
          ["ICPC", "EFCC", "NCC"], "The Independent National Electoral Commission conducts elections.")
        a("Political Parties", "INEC stands for:", "Independent National Electoral Commission",
          ["Independent National Election Council", "International Electoral Commission", "Independent Nigerian Electoral Council"],
          "INEC is the Independent National Electoral Commission.")
        a("Political Parties", "Voting in Nigeria is by:", "secret ballot",
          ["open ballot", "show of hands", "voice vote"], "Voters mark ballots in secret.")
        a("Political Parties", "The age for voting in Nigeria is:", "18 years",
          ["16 years", "21 years", "25 years"], "Citizens aged 18 and above may vote.")
        a("Nigerian Government", "The 1979 Constitution introduced the:", "presidential system",
          ["parliamentary system", "military rule", "confederation"], "The Second Republic used the presidential system.")
        a("Nigerian Government", "The 1963 Constitution made Nigeria a:", "republic",
          ["monarchy", "colony", "dominion"], "Nigeria became a republic in 1963.")
        a("Nigerian Government", "The first military coup in Nigeria took place in:", "January 1966",
          ["July 1966", "1975", "1983"], "The first coup was in January 1966.")
        a("Nigerian Government", "The June 12, 1993 election was won by:", "M.K.O. Abiola",
          ["Bashir Tofa", "Olusegun Obasanjo", "Ernest Shonekan"], "Abiola won the annulled June 12 election.")
        a("Nigerian Government", "Democracy Day in Nigeria is marked on:", "June 12",
          ["October 1", "May 29", "January 15"], "Democracy Day is June 12.")
        a("Nigerian Government", "The first Executive President of Nigeria was:", "Alhaji Shehu Shagari",
          ["Dr Nnamdi Azikiwe", "General Obasanjo", "Alhaji Tafawa Balewa"], "Shagari was President of the Second Republic (1979-1983).")
        a("Foreign Policy", "Nigeria played a leading role in the formation of:", "ECOWAS",
          ["the EU", "NATO", "ASEAN"], "Nigeria helped found ECOWAS in 1975.")
        a("Foreign Policy", "The headquarters of the United Nations is in:", "New York",
          ["Geneva", "Paris", "London"], "The UN headquarters is in New York.")
        a("Foreign Policy", "The headquarters of the African Union is in:", "Addis Ababa",
          ["Cairo", "Nairobi", "Abuja"], "The AU headquarters is in Addis Ababa, Ethiopia.")
        a("Foreign Policy", "The OAU was founded in:", "1963", ["1945", "1975", "2002"],
          "The Organisation of African Unity was founded in 1963.")
        a("Pre-colonial Polities", "The Oyo Empire was ruled by the:", "Alaafin",
          ["Ooni", "Oba of Benin", "Emir"], "The Alaafin ruled Oyo.")
        a("Pre-colonial Polities", "The Benin Kingdom was ruled by the:", "Oba",
          ["Alaafin", "Emir", "Eze"], "The Oba ruled Benin.")
        a("Pre-colonial Polities", "The Igbo village assembly was made up of:", "adult males and titled men",
          ["the king only", "the emir only", "women only"], "Igbo decisions were taken in village assemblies.")
        a("Pre-colonial Polities", "The Tiv political system was:", "largely acephalous (without a central king)",
          ["highly centralised", "ruled by an emir", "ruled by an oba"], "Tiv society was organised by kinship, not a central king.")
    return E

def extra_pool4(subj):
    E = []
    def a(t, q, c, d, e): E.append(mk(0, subj, t, q, c, d, e))
    if subj == "History":
        events = [("Nigeria gained independence", 1960), ("Nigeria became a republic", 1963),
                  ("The Sokoto Jihad began", 1804), ("The Berlin Conference partitioned Africa", 1884),
                  ("The First World War began", 1914), ("The First World War ended", 1918),
                  ("The Second World War began", 1939), ("The Second World War ended", 1945),
                  ("The United Nations was founded", 1945), ("Ghana gained independence", 1957),
                  ("The Nigerian Civil War began", 1967), ("The Nigerian Civil War ended", 1970),
                  ("The OAU was founded", 1963), ("The African Union replaced the OAU", 2002),
                  ("South Africa ended apartheid (first democratic elections)", 1994),
                  ("The amalgamation of Northern and Southern Nigeria", 1914),
                  ("The Atlantic slave trade was abolished by Britain", 1807),
                  ("Mungo Park reached the River Niger", 1796),
                  ("Nigeria's first military coup", 1966), ("The June 12 election was annulled", 1993),
                  ("Nigeria returned to civilian rule (Fourth Republic)", 1999),
                  ("The Lagos colony was annexed by Britain", 1861),
                  ("The British conquest of Benin", 1897), ("The Aba Women's Riot", 1929),
                  ("The Richards Constitution was introduced", 1946),
                  ("The Macpherson Constitution was introduced", 1951),
                  ("The Lyttleton Constitution was introduced", 1954),
                  ("The independence Constitution came into force", 1960),
                  ("The first republican Constitution came into force", 1963),
                  ("General Gowon was overthrown", 1975), ("General Murtala Mohammed was assassinated", 1976),
                  ("The Second Republic began", 1979), ("The Second Republic was overthrown", 1983),
                  ("The Berlin Wall fell", 1989), ("The slave trade was abolished in the USA", 1865),
                  ("Usman dan Fodio founded the Sokoto Caliphate", 1804),
                  ("The Yoruba civil wars ended with the Kiriji War", 1886),
                  ("The first Nigerian newspaper, Iwe Irohin, was founded", 1859),
                  ("Nigeria's capital was moved from Lagos to Abuja", 1991)]
        for name, yr in events:
            others = [n for n, y in events if n != name][:3]
            a("Nigerian and World History", f"Which of these events happened in {yr}?", name, others,
              f"{name} happened in {yr}.")
        a("Early Civilisations", "The Nok culture flourished in present-day:", "northern Nigeria",
          ["southern Nigeria", "Ghana", "Mali"], "Nok sites are in the Jos area of northern Nigeria.")
        a("Early Civilisations", "The Igbo-Ukwu bronzes were discovered in present-day:", "Anambra State",
          ["Lagos State", "Kano State", "Oyo State"], "Igbo-Ukwu is in Anambra State.")
        a("Early Civilisations", "The trans-Saharan trade linked West Africa with:", "North Africa",
          ["Europe only", "Asia only", "America"], "Caravans crossed the Sahara between West and North Africa.")
        a("Early Civilisations", "The main goods traded from West Africa across the Sahara were gold and:", "kola nuts and slaves",
          ["iron only", "timber", "fish"], "Gold, kola and slaves went north; salt and cloth came south.")
        a("Early Civilisations", "Salt was important in the trans-Saharan trade because it was:", "scarce in the forest zone and needed to preserve food",
          ["plentiful everywhere", "used as money only", "a luxury for kings only"],
          "Salt was scarce in the south and vital for diet and preservation.")
        a("Colonial Nigeria", "The Royal Niger Company was led by:", "George Goldie",
          ["Lord Lugard", "Mungo Park", "Hugh Clifford"], "Goldie ran the Royal Niger Company.")
        a("Colonial Nigeria", "The first British High Commissioner of Northern Nigeria was:", "Lord Lugard",
          ["George Goldie", "Hugh Clifford", "Arthur Richards"], "Lugard was High Commissioner of the Northern Protectorate.")
        a("Colonial Nigeria", "The Clifford Constitution of 1922 introduced:", "the elective principle",
          ["universal suffrage", "independence", "republicanism"], "The 1922 constitution introduced elected seats in Lagos and Calabar.")
        a("Colonial Nigeria", "The elective principle allowed Nigerians to:", "elect representatives to the Legislative Council",
          ["vote for the governor", "choose the king", "become civil servants only"],
          "Elected members sat in the Legislative Council.")
        a("Nationalism", "The West African Pilot was founded by:", "Nnamdi Azikiwe",
          ["Herbert Macaulay", "Obafemi Awolowo", "Ahmadu Bello"], "Azikiwe founded the West African Pilot in 1937.")
        a("Nationalism", "The Nigerian Youth Movement was formed in:", "1934",
          ["1923", "1944", "1951"], "The Nigerian Youth Movement was formed in 1934.")
        a("Nationalism", "The NCNC was formed in:", "1944", ["1923", "1934", "1951"],
          "The NCNC was formed in 1944.")
        a("Nationalism", "The Action Group was formed in:", "1951", ["1944", "1934", "1923"],
          "The Action Group was formed in 1951.")
        a("Nationalism", "The NPC was formed in:", "1951", ["1944", "1934", "1923"],
          "The Northern People's Congress was formed in 1951.")
        a("Nationalism", "The London Constitutional Conference of 1953 discussed:", "self-government for Nigeria",
          ["independence for Ghana", "the slave trade", "the Second World War"],
          "The 1953 conference discussed self-government.")
        a("Military Rule", "General Yakubu Gowon ruled Nigeria from:", "1966 to 1975",
          ["1960 to 1966", "1975 to 1976", "1976 to 1979"], "Gowon was Head of State from 1966 to 1975.")
        a("Military Rule", "General Murtala Mohammed ruled from:", "1975 to 1976",
          ["1966 to 1975", "1976 to 1979", "1983 to 1985"], "Murtala ruled from July 1975 until his assassination in February 1976.")
        a("Military Rule", "General Olusegun Obasanjo handed power to civilians in:", "1979",
          ["1976", "1983", "1993"], "Obasanjo handed over to Shagari in 1979.")
        a("Military Rule", "The 1983 coup brought to power:", "General Muhammadu Buhari",
          ["General Ibrahim Babangida", "General Sani Abacha", "General Abdulsalami Abubakar"],
          "Buhari took power in December 1983.")
        a("Military Rule", "General Ibrahim Babangida ruled from:", "1985 to 1993",
          ["1983 to 1985", "1993 to 1998", "1979 to 1983"], "Babangida ruled from 1985 to 1993.")
        a("Military Rule", "General Sani Abacha ruled from:", "1993 to 1998",
          ["1985 to 1993", "1998 to 1999", "1979 to 1983"], "Abacha ruled from 1993 until his death in 1998.")
        a("Post-Independence", "Nigeria joined the United Nations in:", "1960",
          ["1963", "1970", "1945"], "Nigeria joined the UN in 1960, the year of independence.")
        a("Post-Independence", "Nigeria joined the Commonwealth in:", "1960",
          ["1963", "1970", "1945"], "Nigeria joined the Commonwealth at independence.")
        a("Post-Independence", "The first Nigerian to become Secretary-General of the Commonwealth was:", "Emeka Anyaoku",
          ["Olusegun Obasanjo", "Yakubu Gowon", "Nnamdi Azikiwe"], "Emeka Anyaoku was Commonwealth Secretary-General (1990-2000).")
        a("African History", "Kwame Nkrumah led the independence of:", "Ghana",
          ["Nigeria", "Kenya", "Tanzania"], "Nkrumah led Ghana to independence in 1957.")
        a("African History", "Jomo Kenyatta was the first President of:", "Kenya",
          ["Tanzania", "Uganda", "Zambia"], "Kenyatta led Kenya after independence in 1963.")
        a("African History", "Julius Nyerere was the first President of:", "Tanzania",
          ["Kenya", "Uganda", "Zambia"], "Nyerere led Tanzania after independence.")
        a("African History", "The Mau Mau uprising took place in:", "Kenya",
          ["Ghana", "Nigeria", "Tanzania"], "The Mau Mau fought British rule in Kenya in the 1950s.")
        a("World History", "The First World War was fought between:", "the Allied and Central Powers",
          ["Britain and France only", "Germany and Russia only", "the USA and Japan"],
          "The Allies fought the Central Powers (1914-1918).")
        a("World History", "The Second World War began when Germany invaded:", "Poland",
          ["France", "Britain", "Russia"], "Germany invaded Poland in September 1939.")
        a("World History", "The Cold War was a rivalry between the USA and the:", "Soviet Union",
          ["United Kingdom", "China", "France"], "The Cold War pitted the USA against the USSR.")
    if subj == "CRS":
        parables = [("the Good Samaritan", "love for one's neighbour"), ("the Prodigal Son", "God's forgiveness"),
                    ("the Sower", "responses to God's word"), ("the Talents", "faithful use of gifts"),
                    ("the Mustard Seed", "the growth of God's kingdom"), ("the Lost Sheep", "God's care for the lost"),
                    ("the Rich Fool", "the danger of greed"), ("the Pharisee and the Tax Collector", "humility in prayer"),
                    ("the Ten Virgins", "readiness for Christ's return"), ("the Good Shepherd", "Christ's care for his flock")]
        for name, lesson in parables:
            others = [l for n, l in parables if l != lesson][:3]
            a("The Ministry of Jesus", f"The parable of {name} teaches:", lesson, others,
              f"The parable of {name} teaches {lesson}.")
        miracles = [("turning water into wine", "Cana"), ("feeding the five thousand", "the wilderness"),
                    ("walking on water", "the Sea of Galilee"), ("healing the blind Bartimaeus", "Jericho"),
                    ("raising Lazarus", "Bethany"), ("calming the storm", "the Sea of Galilee"),
                    ("healing the leper", "Galilee"), ("the catch of fish", "the Lake of Gennesaret")]
        for mir, place in miracles:
            others = [p for m, p in miracles if p != place][:3]
            a("The Ministry of Jesus", f"The miracle of {mir} took place at/in:", place, others,
              f"The miracle of {mir} took place at {place}.")
        a("The Ministry of Jesus", "The first disciples called by Jesus were:", "Peter and Andrew",
          ["James and John", "Matthew and Thomas", "Philip and Bartholomew"],
          "Peter and Andrew were called first (Matthew 4:18-19).")
        a("The Ministry of Jesus", "The disciple who was a tax collector was:", "Matthew",
          ["Peter", "John", "James"], "Matthew (Levi) was a tax collector.")
        a("The Ministry of Jesus", "The disciple who doubted the resurrection was:", "Thomas",
          ["Peter", "John", "Judas"], "Thomas doubted until he saw the risen Jesus.")
        a("The Ministry of Jesus", "The Sermon on the Mount is recorded in:", "Matthew chapters 5-7",
          ["Luke chapter 2", "John chapter 1", "Mark chapter 1"], "The Sermon on the Mount is in Matthew 5-7.")
        a("The Ministry of Jesus", "The Beatitudes begin with: 'Blessed are the poor in spirit, for theirs is the kingdom of:'", "heaven",
          ["earth", "the sea", "the temple"], "Matthew 5:3 - 'Blessed are the poor in spirit, for theirs is the kingdom of heaven.'")
        a("The Passion", "The garden where Jesus prayed before his arrest was:", "Gethsemane",
          ["Eden", "Golgotha", "Bethany"], "Jesus prayed in Gethsemane.")
        a("The Passion", "The disciple who denied Jesus three times was:", "Peter",
          ["John", "James", "Andrew"], "Peter denied Jesus three times before the cock crowed.")
        a("The Passion", "Jesus was tried before the Roman governor:", "Pontius Pilate",
          ["Herod", "Caesar", "Felix"], "Pilate sentenced Jesus to be crucified.")
        a("The Passion", "The inscription on the cross read:", "'Jesus of Nazareth, King of the Jews'",
          ["'King of Israel'", "'Son of David'", "'The Messiah'"], "John 19:19 records the inscription.")
        a("The Passion", "The women who first found the empty tomb included:", "Mary Magdalene",
          ["Martha", "Elizabeth", "Salome only"], "Mary Magdalene was among the first at the tomb.")
        a("The Early Church", "The deacon chosen to serve tables who became the first martyr was:", "Stephen",
          ["Philip", "Barnabas", "Silas"], "Stephen was stoned (Acts 7).")
        a("The Early Church", "Philip preached to the Ethiopian eunuch on the road to:", "Gaza",
          ["Damascus", "Jericho", "Bethlehem"], "Philip met the eunuch on the Gaza road (Acts 8).")
        a("The Early Church", "The first Gentile convert baptised by Peter was:", "Cornelius",
          ["Lydia", "Timothy", "Titus"], "Cornelius, a Roman centurion, was baptised (Acts 10).")
        a("The Early Church", "Paul's companion on his first missionary journey was:", "Barnabas",
          ["Silas", "Timothy", "Luke"], "Paul and Barnabas travelled together.")
        a("The Early Church", "The Council of Jerusalem decided that Gentile converts need not be:", "circumcised",
          ["baptised", "taught", "fed"], "The council (Acts 15) freed Gentiles from circumcision.")
        a("The Early Church", "Paul was imprisoned in:", "Rome", ["Athens", "Corinth", "Ephesus"],
          "Paul was held in Rome, where tradition says he was martyred.")
        a("Old Testament", "The book that tells of the creation is:", "Genesis",
          ["Exodus", "Leviticus", "Numbers"], "Genesis tells of creation.")
        a("Old Testament", "The book that tells of the Exodus from Egypt is:", "Exodus",
          ["Genesis", "Leviticus", "Joshua"], "Exodus tells of the deliverance from Egypt.")
        a("Old Testament", "The book of Psalms is mainly a book of:", "songs and prayers",
          ["laws", "history", "prophecy only"], "Psalms are songs and prayers.")
        a("Old Testament", "The book of Proverbs is mainly a book of:", "wisdom",
          ["law", "history", "prophecy"], "Proverbs gives wise sayings.")
        a("Old Testament", "The shortest book in the Old Testament is:", "Obadiah",
          ["Jonah", "Haggai", "Malachi"], "Obadiah has only one chapter.")
        a("Old Testament", "The longest book in the Bible is:", "Psalms",
          ["Genesis", "Isaiah", "Jeremiah"], "Psalms has 150 chapters.")
        a("Old Testament", "The first five books of the Bible are called the:", "Pentateuch",
          ["Prophets", "Writings", "Gospels"], "The Pentateuch is Genesis to Deuteronomy.")
        a("Old Testament", "The Ten Commandments are recorded in:", "Exodus 20",
          ["Genesis 1", "Leviticus 1", "Numbers 1"], "Exodus 20 gives the Ten Commandments.")
        a("Old Testament", "The man who lived longest in the Bible was:", "Methuselah",
          ["Noah", "Adam", "Enoch"], "Methuselah lived 969 years (Genesis 5:27).")
        a("Old Testament", "The brother who killed Abel was:", "Cain",
          ["Seth", "Esau", "Jacob"], "Cain killed Abel (Genesis 4).")
        a("Old Testament", "Jacob's name was changed to:", "Israel",
          ["Judah", "Joseph", "Benjamin"], "Jacob became Israel (Genesis 32:28).")
        a("Old Testament", "The son of Abraham through Sarah was:", "Isaac",
          ["Ishmael", "Jacob", "Esau"], "Isaac was the son of promise.")
        a("Old Testament", "The son of Abraham through Hagar was:", "Ishmael",
          ["Isaac", "Jacob", "Esau"], "Ishmael was Hagar's son.")
        a("Old Testament", "Esau sold his birthright to Jacob for:", "a meal of stew",
          ["gold", "silver", "land"], "Esau sold his birthright for bread and stew (Genesis 25).")
        a("Old Testament", "The mother of Samuel was:", "Hannah",
          ["Sarah", "Rebekah", "Rachel"], "Hannah prayed for Samuel (1 Samuel 1).")
        a("Old Testament", "The prophet who anointed David as king was:", "Samuel",
          ["Nathan", "Gad", "Elijah"], "Samuel anointed David (1 Samuel 16).")
        a("Old Testament", "The king who built the first Temple was:", "Solomon",
          ["David", "Saul", "Rehoboam"], "Solomon built the Temple.")
        a("Old Testament", "The kingdom of Israel split after the death of:", "Solomon",
          ["David", "Saul", "Rehoboam's father only"], "After Solomon, the kingdom divided under Rehoboam.")
        a("Christian Ethics", "The Bible teaches that Christians should pray:", "without ceasing",
          ["only on Sundays", "only in church", "only when in trouble"], "1 Thessalonians 5:17 - pray without ceasing.")
        a("Christian Ethics", "The Bible teaches that the love of money is the root of:", "all kinds of evil",
          ["all good", "wisdom", "success"], "1 Timothy 6:10.")
        a("Christian Ethics", "Christians are taught to forgive:", "seventy times seven",
          ["once only", "seven times only", "never"], "Matthew 18:22 - forgive seventy times seven.")
        a("Christian Ethics", "The two great commandments are to love God and:", "one's neighbour",
          ["oneself only", "one's enemies only", "one's family only"], "Love God and love your neighbour.")
    if subj == "IRS":
        surahs = [("Al-Fatihah", 1), ("Al-Baqarah", 2), ("Al-Ikhlas", 112), ("An-Nas", 114),
                  ("Al-Falaq", 113), ("Ya-Sin", 36), ("Al-Mulk", 67), ("Ar-Rahman", 55),
                  ("Al-Kahf", 18), ("Maryam", 19), ("Yusuf", 12), ("Al-An'am", 6)]
        for name, num in surahs:
            others = [str(n) for n, x in surahs if x != num][:3]
            a("The Qur'an", f"Surah {name} is chapter number:", str(num), others,
              f"Surah {name} is chapter {num} of the Qur'an.")
        a("The Qur'an", "The Qur'an was revealed over a period of:", "23 years",
          ["10 years", "40 years", "13 years"], "Revelation lasted 23 years (610-632 CE).")
        a("The Qur'an", "The Qur'an was first revealed in the cave of:", "Hira",
          ["Thawr", "Uhud", "Quba"], "The first revelation came in Cave Hira.")
        a("The Qur'an", "The Qur'an is written in:", "Arabic", ["Hebrew", "Persian", "Turkish"],
          "The Qur'an was revealed in Arabic.")
        a("The Qur'an", "A person who has memorised the whole Qur'an is called a:", "Hafiz",
          ["Imam", "Mufti", "Qadi"], "A Hafiz has memorised the Qur'an.")
        a("Tawhid", "The three categories of Tawhid are Rububiyyah, Uluhiyyah and:", "Asma wa Sifat",
          ["Iman", "Islam", "Ihsan"], "Tawhid covers Lordship, Worship and Names/Attributes.")
        a("Tawhid", "The angels were created from:", "light", ["fire", "clay", "water"],
          "Angels were created from light.")
        a("Tawhid", "The jinn were created from:", "smokeless fire", ["light", "clay", "water"],
          "Jinn were created from smokeless fire.")
        a("Tawhid", "The first human was created from:", "clay", ["light", "fire", "water"],
          "Adam was created from clay.")
        a("The Five Pillars", "The Zakat rate on cash savings is:", "2.5%",
          ["5%", "10%", "1%"], "Zakat on money is 2.5%.")
        a("The Five Pillars", "Zakat is due on wealth held for:", "one lunar year",
          ["one month", "one week", "one day"], "Zakat is due after a full lunar year (hawl).")
        a("The Five Pillars", "The fast of Ramadan begins at:", "dawn (Fajr)",
          ["sunrise", "noon", "sunset"], "The fast starts at dawn.")
        a("The Five Pillars", "The fast of Ramadan ends at:", "sunset (Maghrib)",
          ["midnight", "dawn", "noon"], "The fast is broken at sunset.")
        a("The Five Pillars", "The meal taken before dawn in Ramadan is:", "Suhur",
          ["Iftar", "Taraweeh", "Fajr"], "Suhur is the pre-dawn meal.")
        a("The Five Pillars", "The meal taken to break the fast is:", "Iftar",
          ["Suhur", "Taraweeh", "Fajr"], "Iftar breaks the fast at sunset.")
        a("The Five Pillars", "The night prayers in Ramadan are called:", "Taraweeh",
          ["Tahajjud only", "Iftar", "Suhur"], "Taraweeh are the Ramadan night prayers.")
        a("The Five Pillars", "Hajj is obligatory on Muslims who are:", "physically and financially able",
          ["rich only", "old only", "scholars only"], "Hajj is required of those who can afford it and are able.")
        a("The Five Pillars", "The Hajj takes place in the month of:", "Dhul-Hijjah",
          ["Ramadan", "Shawwal", "Muharram"], "Hajj is in Dhul-Hijjah.")
        a("The Five Pillars", "The first month of the Islamic calendar is:", "Muharram",
          ["Ramadan", "Shawwal", "Dhul-Hijjah"], "Muharram opens the Islamic year.")
        a("The Five Pillars", "The Islamic calendar is based on the:", "moon",
          ["sun", "stars", "seasons"], "The Hijri calendar is lunar.")
        a("The Prophets", "The prophet known for his patience in suffering was:", "Ayyub (Job)",
          ["Yusuf", "Musa", "Ibrahim"], "Ayyub is the model of patience.")
        a("The Prophets", "The prophet who interpreted dreams in Egypt was:", "Yusuf (Joseph)",
          ["Musa", "Ibrahim", "Isa"], "Yusuf interpreted dreams and rose in Egypt.")
        a("The Prophets", "The prophet who was given wisdom and a kingdom was:", "Sulayman (Solomon)",
          ["Dawud", "Musa", "Isa"], "Sulayman was given wisdom and dominion.")
        a("The Prophets", "The prophet who spoke to Allah on Mount Sinai was:", "Musa (Moses)",
          ["Ibrahim", "Isa", "Muhammad"], "Musa spoke with Allah on Mount Sinai.")
        a("The Prophets", "The prophet who was born without a father by Allah's will was:", "Isa (Jesus)",
          ["Musa", "Ibrahim", "Adam"], "Isa was born to Maryam without a father.")
        a("The Prophets", "The number of prophets mentioned by name in the Qur'an is:", "25",
          ["10", "40", "124,000"], "Twenty-five prophets are named in the Qur'an.")
        a("Hadith", "The Sunnah is the:", "practice and example of the Prophet",
          ["words of the Qur'an", "laws of the caliphs", "customs of the Arabs only"],
          "The Sunnah is the Prophet's example.")
        a("Hadith", "A Hadith is classified as Sahih when it is:", "authentic",
          ["weak", "fabricated", "abrogated"], "Sahih means authentic.")
        a("Hadith", "The six most authentic Hadith collections are called:", "Kutub al-Sittah",
          ["Sahihayn", "Muwatta", "Musnad"], "Kutub al-Sittah are the six books.")
        a("Fiqh", "The five daily prayers were made obligatory during the:", "Isra and Mi'raj",
          ["Hijrah", "Battle of Badr", "Treaty of Hudaybiyyah"], "The prayers were ordained on the Night Journey.")
        a("Fiqh", "The prayer leader is called the:", "Imam", ["Mu'adhin", "Qadi", "Mufti"],
          "The Imam leads the prayer.")
        a("Fiqh", "The person who calls the Adhan is the:", "Mu'adhin",
          ["Imam", "Qadi", "Mufti"], "The Mu'adhin gives the call to prayer.")
        a("Fiqh", "The Friday sermon is called the:", "Khutbah", ["Adhan", "Iqamah", "Tasbih"],
          "The Khutbah is the sermon before Jumu'ah prayer.")
        a("Fiqh", "The two Eid festivals are Eid al-Fitr and:", "Eid al-Adha",
          ["Eid al-Mawlid", "Eid al-Jumu'ah", "Eid al-Hajj"], "The two Eids are Fitr and Adha.")
        a("Fiqh", "Eid al-Fitr comes after:", "Ramadan", ["Hajj", "Muharram", "Shawwal only"],
          "Eid al-Fitr marks the end of Ramadan.")
        a("Fiqh", "Eid al-Adha comes during:", "Hajj", ["Ramadan", "Muharram", "Rajab"],
          "Eid al-Adha is during the Hajj season.")
        a("Fiqh", "The Islamic law of inheritance is called:", "Mirath",
          ["Zakat", "Sadaqah", "Waqf"], "Mirath governs inheritance.")
        a("Fiqh", "Marriage in Islam is called:", "Nikah", ["Talaq", "Khul", "Mahr"],
          "Nikah is the marriage contract.")
        a("Fiqh", "The bridal gift in Islamic marriage is called:", "Mahr",
          ["Nikah", "Talaq", "Khul"], "Mahr is the gift given to the bride.")
        a("Islamic History", "The Battle of Badr took place in:", "624 CE",
          ["622 CE", "630 CE", "632 CE"], "Badr was fought in 2 AH (624 CE).")
        a("Islamic History", "The Battle of Uhud took place in:", "625 CE",
          ["624 CE", "627 CE", "630 CE"], "Uhud was fought in 3 AH (625 CE).")
        a("Islamic History", "Makkah was conquered peacefully in:", "630 CE",
          ["622 CE", "624 CE", "632 CE"], "The conquest of Makkah was in 630 CE (8 AH).")
        a("Islamic History", "The Treaty of Hudaybiyyah was signed in:", "628 CE",
          ["622 CE", "630 CE", "632 CE"], "Hudaybiyyah was in 6 AH (628 CE).")
        a("Islamic History", "The first mosque in Nigeria was built in:", "Lagos (19th century)",
          ["Kano", "Sokoto", "Ibadan"], "Early mosques in Lagos date to the 19th century.")
        a("Islamic Morality", "Gratitude to Allah is called:", "Shukr",
          ["Sabr", "Taqwa", "Sidq"], "Shukr is thankfulness.")
        a("Islamic Morality", "Excellence in worship as if seeing Allah is:", "Ihsan",
          ["Iman", "Islam", "Taqwa"], "Ihsan is worshipping as though you see Allah.")
        a("Islamic Morality", "Backbiting in Islam is:", "forbidden",
          ["allowed", "encouraged", "obligatory"], "Backbiting is forbidden (Q 49:12).")
        a("Islamic Morality", "The greatest sin in Islam after Shirk is:", "disobedience to parents",
          ["lying", "stealing", "missing prayer"], "After Shirk, disobedience to parents is gravely condemned.")
    return E

def extra_pool5(subj):
    E = []
    def a(t, q, c, d, e): E.append(mk(0, subj, t, q, c, d, e))
    if subj == "Civic":
        agencies = [("EFCC", "Economic and Financial Crimes Commission"),
                    ("ICPC", "Independent Corrupt Practices and Other Related Offences Commission"),
                    ("NDLEA", "National Drug Law Enforcement Agency"),
                    ("NAPTIP", "National Agency for the Prohibition of Trafficking in Persons"),
                    ("FRSC", "Federal Road Safety Corps"),
                    ("FCCPC", "Federal Competition and Consumer Protection Commission"),
                    ("NEMA", "National Emergency Management Agency"),
                    ("NYSC", "National Youth Service Corps"),
                    ("INEC", "Independent National Electoral Commission"),
                    ("SON", "Standards Organisation of Nigeria")]
        for ab, full in agencies:
            others = [f for x, f in agencies if f != full][:3]
            a("National Institutions", f"What does {ab} stand for?", full, others, f"{ab} stands for {full}.")
        a("National Institutions", "The EFCC fights:", "economic and financial crimes",
          ["drug trafficking", "road accidents", "human trafficking"], "The EFCC investigates financial crimes.")
        a("National Institutions", "The ICPC fights:", "corruption in public offices",
          ["drug abuse", "road accidents", "election fraud only"], "The ICPC tackles corrupt practices.")
        a("National Institutions", "NEMA responds to:", "emergencies and disasters",
          ["elections", "taxes", "education"], "NEMA manages disaster response.")
        a("National Institutions", "The NYSC was established in:", "1973",
          ["1960", "1979", "1999"], "The NYSC was created in 1973 to promote national unity.")
        a("National Institutions", "The NYSC scheme is for:", "graduates of tertiary institutions",
          ["secondary school leavers", "civil servants", "soldiers"], "Graduates serve for one year under the NYSC.")
        a("National Identity", "Nigeria's national animal on the coat of arms is the:", "eagle",
          ["lion", "horse", "elephant"], "The eagle stands for strength.")
        a("National Identity", "The two horses on Nigeria's coat of arms represent:", "dignity",
          ["strength", "peace", "agriculture"], "The horses symbolise dignity.")
        a("National Identity", "The black shield on Nigeria's coat of arms represents:", "Nigeria's fertile soil",
          ["the rivers", "the people", "the forests"], "The black shield stands for the fertile soil.")
        a("National Identity", "The 'Y' shape on Nigeria's coat of arms represents the:", "confluence of the Niger and Benue rivers",
          ["roads of Nigeria", "borders of Nigeria", "railways of Nigeria"],
          "The Y shape is the meeting of the Niger and Benue.")
        a("National Identity", "The flower on Nigeria's coat of arms is the:", "Costus spectabilis (national flower)",
          ["hibiscus", "rose", "sunflower"], "The Costus spectabilis is at the base of the coat of arms.")
        a("National Identity", "The old national anthem 'Nigeria, We Hail Thee' was replaced in:", "1978",
          ["1960", "1963", "1999"], "The anthem was changed in 1978; 'Nigeria, We Hail Thee' was restored in 2024.")
        a("Values", "Discipline means:", "obeying rules and controlling behaviour",
          ["doing what one likes", "avoiding work", "breaking rules"], "Discipline is self-control and obedience to rules.")
        a("Values", "Integrity means being:", "honest and morally upright",
          ["rich", "famous", "clever"], "Integrity is honesty and strong moral principles.")
        a("Values", "Diligence means:", "working hard and carefully",
          ["working slowly", "avoiding work", "working carelessly"], "Diligence is steady hard work.")
        a("Values", "Contentment means being:", "satisfied with what one has",
          ["greedy", "envious", "ambitious only"], "Contentment is satisfaction with one's lot.")
        a("Values", "Self-reliance means depending on:", "oneself",
          ["others always", "government only", "parents only"], "Self-reliance is independence.")
        a("Citizenship", "A good citizen should:", "obey the laws of the land",
          ["break laws", "avoid taxes", "ignore elections"], "Good citizens obey laws and pay taxes.")
        a("Citizenship", "Voting is a civic:", "duty and right", ["crime", "privilege for the rich", "waste of time"],
          "Voting is both a right and a duty.")
        a("Citizenship", "The voting age in Nigeria is:", "18 years",
          ["16 years", "21 years", "25 years"], "Citizens aged 18 and above may vote.")
        a("Human Rights", "The right to freedom of movement allows citizens to:", "move freely within the country",
          ["travel without passport", "enter any house", "cross borders freely"], "Citizens may move freely within Nigeria.")
        a("Human Rights", "The right to freedom of association allows citizens to:", "join groups of their choice",
          ["form gangs", "avoid all groups", "join secret cults"], "Citizens may join lawful associations.")
        a("Human Rights", "The right to education means every child should have access to:", "schooling",
          ["wealth", "employment", "land"], "Education is a right of the child.")
        a("Human Rights", "Child labour is:", "a violation of children's rights",
          ["a right of children", "good training", "a duty of children"], "Child labour exploits children.")
        a("Law and Order", "The police force in Nigeria is the:", "Nigeria Police Force",
          ["Nigeria Army", "Civil Defence", "FRSC"], "The Nigeria Police Force maintains law and order.")
        a("Law and Order", "A court is a place where:", "justice is administered",
          ["laws are made", "taxes are collected", "elections are held"], "Courts interpret laws and settle disputes.")
        a("Law and Order", "The lowest court in Nigeria is the:", "customary / magistrate court",
          ["Supreme Court", "Court of Appeal", "Federal High Court"], "Magistrate and customary courts are the lowest.")
        a("Traffic Rules", "Zebra crossings are for:", "pedestrians",
          ["vehicles", "cyclists only", "animals"], "Pedestrians cross at zebra crossings.")
        a("Traffic Rules", "A driver must wear a:", "seat belt",
          ["helmet only", "cap", "glove"], "Seat belts save lives.")
        a("Traffic Rules", "A motorcyclist must wear a:", "helmet",
          ["seat belt", "cap", "glove"], "Helmets protect motorcyclists.")
        a("Traffic Rules", "Driving under the influence of alcohol is:", "an offence",
          ["allowed", "safe", "encouraged"], "Drink-driving is against the law.")
        a("Interpersonal Relations", "Empathy means:", "understanding another person's feelings",
          ["ignoring others", "judging others", "avoiding others"], "Empathy is feeling with others.")
        a("Interpersonal Relations", "Cooperation means:", "working together for a common goal",
          ["working alone", "competing always", "avoiding others"], "Cooperation is joint effort.")
        a("Interpersonal Relations", "A mediator is a person who:", "helps parties settle a dispute",
          ["takes sides", "starts a fight", "avoids disputes"], "Mediators are neutral peacemakers.")
        a("Democracy", "A free press is important in a democracy because it:", "informs the public and checks power",
          ["praises the government", "hides information", "supports one party"], "A free press holds leaders accountable.")
        a("Democracy", "The opposition in a democracy:", "criticises and checks the government",
          ["supports everything", "has no role", "rules the country"], "The opposition provides an alternative.")
        a("Democracy", "A referendum is a:", "direct vote by the people on an issue",
          ["election of a president", "court case", "party meeting"], "Referendums let citizens decide an issue directly.")
        a("National Development", "Education contributes to national development by:", "producing skilled manpower",
          ["increasing population", "reducing taxes", "building roads only"], "Education builds human capital.")
        a("National Development", "Good roads contribute to development by:", "easing transport and trade",
          ["increasing accidents", "wasting money", "reducing farming"], "Roads move goods and people.")
        a("Drug Abuse", "One cause of drug abuse among youths is:", "peer pressure",
          ["good parenting", "education", "employment"], "Peer pressure pushes youths into drug use.")
        a("Drug Abuse", "Drug addiction can be treated through:", "rehabilitation",
          ["punishment only", "isolation only", "ignoring it"], "Rehabilitation helps addicts recover.")
        a("Human Trafficking", "Victims of human trafficking are often lured with promises of:", "jobs abroad",
          ["education", "marriage", "land"], "Traffickers promise jobs and a better life.")
        a("Human Trafficking", "One way to prevent human trafficking is through:", "public awareness",
          ["secrecy", "ignorance", "poverty"], "Awareness helps people recognise traffickers' tricks.")
    if subj == "Literature":
        works = [("Things Fall Apart", "Chinua Achebe"), ("The Lion and the Jewel", "Wole Soyinka"),
                 ("The Trials of Brother Jero", "Wole Soyinka"), ("Purple Hibiscus", "Chimamanda Ngozi Adichie"),
                 ("Half of a Yellow Sun", "Chimamanda Ngozi Adichie"), ("The Concubine", "Elechi Amadi"),
                 ("The Slave", "Elechi Amadi"), ("Joys of Motherhood", "Buchi Emecheta"),
                 ("The Bride Price", "Buchi Emecheta"), ("The African Child", "Camara Laye"),
                 ("Weep Not, Child", "Ngugi wa Thiong'o"), ("The River Between", "Ngugi wa Thiong'o"),
                 ("A Grain of Wheat", "Ngugi wa Thiong'o"), ("Mine Boy", "Peter Abrahams"),
                 ("The Beautyful Ones Are Not Yet Born", "Ayi Kwei Armah"),
                 ("The Dilemma of a Ghost", "Ama Ata Aidoo"), ("Anowa", "Ama Ata Aidoo"),
                 ("The Gods Are Not to Blame", "Ola Rotimi"), ("Our Husband Has Gone Mad Again", "Ola Rotimi"),
                 ("The Passport of Mallam Ilia", "Cyprian Ekwensi"), ("Jagua Nana", "Cyprian Ekwensi"),
                 ("The Blinkards", "Kobina Sekyi"), ("Faceless", "Amma Darko"),
                 ("Harvest of Corruption", "Frank Ogodo Ogbeche"), ("The Merchant of Venice", "William Shakespeare"),
                 ("Romeo and Juliet", "William Shakespeare"), ("Macbeth", "William Shakespeare"),
                 ("A Midsummer Night's Dream", "William Shakespeare"), ("Animal Farm", "George Orwell"),
                 ("Lord of the Flies", "William Golding"), ("The Old Man and the Sea", "Ernest Hemingway"),
                 ("The Famished Road", "Ben Okri"), ("The Interpreters", "Wole Soyinka"),
                 ("Arrow of God", "Chinua Achebe"), ("No Longer at Ease", "Chinua Achebe"),
                 ("The Man Died", "Wole Soyinka"), ("A Dance of the Forests", "Wole Soyinka"),
                 ("The Road", "Wole Soyinka"), ("Death and the King's Horseman", "Wole Soyinka")]
        for title, author in works:
            others = [t for t, a in works if t != title][:3]
            a("African and World Literature", f"Which of these works was written by {author}?", title, others,
              f"'{title}' was written by {author}.")
        devices = [("The wind whispered through the trees.", "personification"),
                   ("He is as brave as a lion.", "simile"),
                   ("The classroom was a zoo.", "metaphor"),
                   ("The bees buzzed in the garden.", "onomatopoeia"),
                   ("She sells sea shells by the sea shore.", "alliteration"),
                   ("I have told you a million times.", "hyperbole"),
                   ("The pen is mightier than the sword.", "metaphor"),
                   ("The sun smiled down on us.", "personification"),
                   ("He is like a rock in a storm.", "simile"),
                   ("The thunder crashed and roared.", "onomatopoeia"),
                   ("Peter Piper picked a peck of pickled peppers.", "alliteration"),
                   ("I am so hungry I could eat a horse.", "hyperbole")]
        for sentence, dev in devices:
            others = [d for s, d in devices if d != dev][:3]
            others = list(dict.fromkeys(others))
            while len(others) < 3: others.append("irony")
            a("Literary Devices", f"Which literary device is used in: '{sentence}'", dev, others[:3],
              f"'{sentence}' uses {dev}.")
        a("Literary Terms", "A play with a happy ending is a:", "comedy",
          ["tragedy", "elegy", "epic"], "Comedy ends happily.")
        a("Literary Terms", "A short poem of 14 lines is a:", "sonnet",
          ["ballad", "ode", "elegy"], "A sonnet has 14 lines.")
        a("Literary Terms", "A narrative poem that tells a story in simple verses is a:", "ballad",
          ["sonnet", "ode", "elegy"], "Ballads tell stories in verse.")
        a("Literary Terms", "A poem written to praise a person or thing is an:", "ode",
          ["elegy", "ballad", "sonnet"], "An ode praises its subject.")
        a("Literary Terms", "The hero of a tragedy who suffers a downfall is called the:", "tragic hero",
          ["comic hero", "villain", "fool"], "The tragic hero falls from greatness.")
        a("Literary Terms", "The flaw that leads to the tragic hero's downfall is called:", "hamartia",
          ["hubris only", "catharsis", "peripeteia"], "Hamartia is the tragic flaw.")
        a("Literary Terms", "The feeling of pity and fear aroused by tragedy is called:", "catharsis",
          ["hamartia", "hubris", "nemesis"], "Catharsis is the purging of pity and fear.")
        a("Literary Terms", "A character who contrasts with another to highlight their qualities is a:", "foil",
          ["protagonist", "antagonist", "narrator"], "A foil highlights another character by contrast.")
        a("Literary Terms", "The use of hints to suggest what will happen later is:", "foreshadowing",
          ["flashback", "irony", "suspense"], "Foreshadowing hints at the future.")
        a("Literary Terms", "A sudden reversal of fortune in a play is called:", "peripeteia",
          ["catharsis", "hamartia", "anagnorisis"], "Peripeteia is a reversal of fortune.")
        a("Literary Terms", "The moment of recognition in a tragedy is called:", "anagnorisis",
          ["peripeteia", "catharsis", "hamartia"], "Anagnorisis is recognition or discovery.")
        a("Literary Terms", "Excessive pride in a tragic hero is called:", "hubris",
          ["hamartia", "catharsis", "nemesis"], "Hubris is overweening pride.")
        a("Drama", "The part of a play between acts is called a:", "scene",
          ["stanza", "chapter", "verse"], "Acts are divided into scenes.")
        a("Drama", "The words spoken by a character to the audience, unheard by other characters, are an:", "aside",
          ["soliloquy", "dialogue", "monologue"], "An aside is spoken to the audience alone.")
        a("Drama", "A speech by one character addressing others on stage is a:", "monologue",
          ["soliloquy", "aside", "dialogue"], "A monologue is a long speech to others present.")
        a("Drama", "The group that comments on the action in Greek drama is the:", "chorus",
          ["audience", "orchestra", "cast"], "The chorus comments on the action.")
        a("Poetry", "A poem with no regular rhyme or metre is written in:", "free verse",
          ["blank verse", "sonnet", "ballad"], "Free verse has no fixed pattern.")
        a("Poetry", "Unrhymed verse in iambic pentameter is:", "blank verse",
          ["free verse", "sonnet", "ode"], "Blank verse is unrhymed iambic pentameter.")
        a("Poetry", "A pair of rhymed lines is a:", "couplet",
          ["quatrain", "stanza", "tercet"], "A couplet is two rhymed lines.")
        a("Poetry", "A group of four lines in a poem is a:", "quatrain",
          ["couplet", "tercet", "octave"], "A quatrain has four lines.")
        a("Poetry", "The repetition of vowel sounds in a poem is:", "assonance",
          ["alliteration", "onomatopoeia", "rhyme"], "Assonance repeats vowel sounds.")
        a("Poetry", "The repetition of a word or phrase for emphasis is:", "repetition",
          ["alliteration", "irony", "metaphor"], "Repetition repeats words for effect.")
        a("Prose", "The main character in a novel is the:", "protagonist",
          ["antagonist", "narrator", "author"], "The protagonist is the central character.")
        a("Prose", "A novel that tells the story of a person's growth from childhood is a:", "bildungsroman",
          ["epistolary novel", "picaresque novel", "gothic novel"], "A bildungsroman follows a character's growth.")
        a("Prose", "A novel written as a series of letters is an:", "epistolary novel",
          ["bildungsroman", "gothic novel", "picaresque novel"], "Epistolary novels are told through letters.")
        a("Prose", "The events in a novel are arranged in a:", "plot",
          ["theme", "setting", "style"], "Plot is the sequence of events.")
        a("African and World Literature", "Wole Soyinka won the Nobel Prize for Literature in:", "1986",
          ["1976", "1996", "2006"], "Soyinka won the Nobel Prize in 1986, the first African to do so.")
        a("African and World Literature", "Chinua Achebe's first novel, 'Things Fall Apart', was published in:", "1958",
          ["1948", "1968", "1978"], "'Things Fall Apart' was published in 1958.")
        a("African and World Literature", "The setting of 'Things Fall Apart' is:", "Umuofia, in Igboland",
          ["Lagos", "Ibadan", "Kano"], "The novel is set in the Igbo village of Umuofia.")
        a("African and World Literature", "The hero of 'Things Fall Apart' is:", "Okonkwo",
          ["Nwoye", "Unoka", "Obierika"], "Okonkwo is the central character.")
        a("African and World Literature", "The hero of 'The Lion and the Jewel' who is the Bale is:", "Baroka",
          ["Lakunle", "Sidi", "Sadiku"], "Baroka, the Bale, is the Lion.")
        a("African and World Literature", "In 'The Lion and the Jewel', Sidi is known as the:", "Jewel",
          ["Lion", "Bale", "Teacher"], "Sidi is the Jewel of the village.")
    if subj == "English":
        synonyms = [("abundant","plentiful"),("scarce","rare"),("generous","kind"),
                    ("frugal","thrifty"),("obvious","clear"),("vague","unclear"),
                    ("prompt","quick"),("delay","postpone"),("ancient","old"),
                    ("fragile","delicate"),("sturdy","strong"),("timid","shy"),
                    ("bold","brave"),("grateful","thankful"),("jealous","envious"),
                    ("loyal","faithful"),("modest","humble"),("proud","arrogant"),
                    ("wise","sensible"),("foolish","silly"),("rapid","fast"),
                    ("gradual","slow"),("crucial","important"),("trivial","unimportant"),
                    ("genuine","real"),("false","untrue"),("vivid","clear"),
                    ("dull","boring"),("keen","eager"),("reluctant","unwilling")]
        for w, syn in synonyms:
            others = [s for x, s in synonyms if s != syn][:3]
            a("Lexis: Synonyms", f"Choose the word nearest in meaning to: {w.upper()}", syn, others,
              f"{syn} is the closest synonym of {w}.")
        antonyms = [("abundant","scarce"),("generous","stingy"),("obvious","hidden"),
                    ("prompt","late"),("fragile","strong"),("timid","bold"),
                    ("grateful","ungrateful"),("loyal","disloyal"),("modest","proud"),
                    ("wise","foolish"),("rapid","slow"),("crucial","trivial"),
                    ("genuine","fake"),("vivid","dull"),("keen","reluctant"),
                    ("ancient","modern"),("brave","cowardly"),("honest","dishonest"),
                    ("rich","poor"),("happy","sad")]
        for w, ant in antonyms:
            others = [x for x, y in antonyms if x != ant][:3]
            a("Lexis: Antonyms", f"Choose the word opposite in meaning to: {w.upper()}", ant, others,
              f"{ant} is the opposite of {w}.")
        idioms = [("to burn one's bridges", "to make retreat impossible"),
                  ("to face the music", "to accept the consequences"),
                  ("to give someone the cold shoulder", "to ignore someone deliberately"),
                  ("to be in hot water", "to be in trouble"),
                  ("to kill two birds with one stone", "to achieve two things with one action"),
                  ("to pull someone's leg", "to joke with someone"),
                  ("to rain cats and dogs", "to rain heavily"),
                  ("to be on cloud nine", "to be very happy"),
                  ("to cry over spilt milk", "to regret something that cannot be undone"),
                  ("to keep an eye on", "to watch carefully"),
                  ("to make ends meet", "to manage on one's income"),
                  ("to sit on the fence", "to avoid taking sides"),
                  ("to take something with a pinch of salt", "to not believe it completely"),
                  ("to throw in the towel", "to give up"),
                  ("to be under the weather", "to feel slightly ill")]
        for idiom, meaning in idioms:
            others = [m for i, m in idioms if m != meaning][:3]
            a("Lexis: Idioms", f"What does the idiom '{idiom}' mean?", meaning, others,
              f"'{idiom}' means: {meaning}.")
        grammar = [
            ("Lexis and Structure", "The teacher, together with her students, _____ arrived.", "has", ["have", "are", "were"],
             "'Together with' does not change the singular subject."),
            ("Lexis and Structure", "Not only the students but also the teacher _____ present.", "was", ["were", "are", "have"],
             "The verb agrees with the nearer subject, 'teacher'."),
            ("Lexis and Structure", "Either the boys or the girl _____ to blame.", "is", ["are", "were", "have"],
             "The verb agrees with the nearer subject, 'girl'."),
            ("Lexis and Structure", "The number of students in the class _____ forty.", "is", ["are", "were", "have"],
             "'The number' is singular."),
            ("Lexis and Structure", "A number of students _____ absent.", "were", ["was", "is", "has"],
             "'A number of' takes a plural verb."),
            ("Lexis and Structure", "She has _____ friends in Lagos.", "many", ["much", "more", "most"],
             "'Many' is used with countable nouns."),
            ("Lexis and Structure", "There is _____ water in the jug.", "little", ["few", "many", "several"],
             "'Little' is used with uncountable nouns."),
            ("Lexis and Structure", "There are _____ books on the shelf.", "few", ["little", "much", "less"],
             "'Few' is used with countable nouns."),
            ("Lexis and Structure", "He is taller _____ his brother.", "than", ["then", "that", "to"],
             "Comparisons use 'than'."),
            ("Lexis and Structure", "She is the _____ girl in the class.", "tallest", ["taller", "tall", "more tall"],
             "Superlative is used when comparing three or more."),
            ("Lexis and Structure", "Choose the correctly spelt word:", "rhythm", ["rythm", "rithm", "rythym"],
             "'Rhythm' is spelt r-h-y-t-h-m."),
            ("Lexis and Structure", "Choose the correctly spelt word:", "embarrass", ["embarass", "embarras", "embarrasss"],
             "'Embarrass' has double 'r' and double 's'."),
            ("Lexis and Structure", "Choose the correctly spelt word:", "necessary", ["neccessary", "necesary", "necessery"],
             "'Necessary' has one 'c' and double 's'."),
            ("Lexis and Structure", "Choose the correctly spelt word:", "tomorrow", ["tommorrow", "tomorow", "tommorow"],
             "'Tomorrow' has double 'm' and single 'r'."),
            ("Lexis and Structure", "The past tense of 'teach' is:", "taught", ["teached", "teaching", "taughted"],
             "'Taught' is the past tense of 'teach'."),
            ("Lexis and Structure", "The past tense of 'buy' is:", "bought", ["buyed", "buying", "boughted"],
             "'Bought' is the past tense of 'buy'."),
            ("Lexis and Structure", "The past tense of 'catch' is:", "caught", ["catched", "catching", "caughted"],
             "'Caught' is the past tense of 'catch'."),
            ("Lexis and Structure", "The plural of 'box' is:", "boxes", ["boxs", "boxies", "boxen"],
             "'Boxes' is the plural of 'box'."),
            ("Lexis and Structure", "The plural of 'baby' is:", "babies", ["babys", "babyes", "babie"],
             "'Babies' is the plural of 'baby'."),
            ("Lexis and Structure", "The plural of 'man' is:", "men", ["mans", "mens", "manes"],
             "'Men' is the plural of 'man'."),
            ("Lexis and Structure", "The comparative of 'big' is:", "bigger", ["big", "biggest", "more big"],
             "'Bigger' is the comparative of 'big'."),
            ("Lexis and Structure", "The superlative of 'happy' is:", "happiest", ["happier", "happyest", "most happy"],
             "'Happiest' is the superlative of 'happy'."),
            ("Lexis and Structure", "He _____ TV when I called.", "was watching", ["is watching", "watches", "watch"],
             "Past continuous is used for an action in progress in the past."),
            ("Lexis and Structure", "By this time tomorrow, I _____ my exams.", "will have finished", ["will finish", "finish", "have finished"],
             "Future perfect is used for an action completed by a future time."),
            ("Lexis and Structure", "If I had money, I _____ a car.", "would buy", ["will buy", "buy", "bought"],
             "Second conditional uses 'would' + verb."),
            ("Lexis and Structure", "The passive form of 'She wrote a letter' is:", "A letter was written by her",
             ["A letter is written by her", "She was written a letter", "A letter wrote her"],
             "Past simple passive: was + past participle."),
            ("Lexis and Structure", "The active form of 'The room was cleaned by the boy' is:", "The boy cleaned the room",
             ["The boy cleans the room", "The room cleaned the boy", "The boy was cleaning the room"],
             "Active: subject + past tense verb + object."),
            ("Lexis and Structure", "He asked, 'Where are you going?' The reported speech is: He asked where I _____ going.", "was",
             ["am", "are", "were"], "In reported speech the present tense shifts to the past."),
            ("Lexis and Structure", "A group of words that makes complete sense is a:", "sentence",
             ["phrase", "clause", "word"], "A sentence expresses a complete thought."),
            ("Lexis and Structure", "A group of words without a finite verb is a:", "phrase",
             ["sentence", "clause", "paragraph"], "A phrase lacks a finite verb."),
            ("Lexis and Structure", "The subject of a sentence is the person or thing that:", "does the action",
             ["receives the action", "describes the action", "ends the sentence"],
             "The subject performs the action."),
            ("Lexis and Structure", "The object of a sentence is the person or thing that:", "receives the action",
             ["does the action", "describes the action", "begins the sentence"],
             "The object receives the action."),
            ("Oral English", "The consonant sound in 'church' is the same as in:", "chair",
             ["school", "character", "chemist"], "'Church' and 'chair' share the /tS/ sound."),
            ("Oral English", "The word 'nation' is stressed on the:", "first syllable",
             ["second syllable", "third syllable", "last syllable"], "NA-tion: stress on the first syllable."),
            ("Oral English", "The word 'examination' is stressed on the:", "fourth syllable",
             ["first syllable", "second syllable", "third syllable"], "ex-am-i-NA-tion: stress on the fourth syllable."),
            ("Oral English", "The pair 'flower' and 'flour' are:", "homophones",
             ["synonyms", "antonyms", "homographs"], "They sound the same but are spelt differently."),
            ("Oral English", "The pair 'lead' (metal) and 'lead' (to guide) are:", "homographs",
             ["homophones", "synonyms", "antonyms"], "Homographs are spelt the same but differ in meaning/pronunciation."),
        ]
        for t, q, c, d, e in grammar:
            a(t, q, c, d, e)
    return E
