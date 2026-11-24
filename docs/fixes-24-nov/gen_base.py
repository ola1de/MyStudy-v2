# Base pools for NECO placeholder generator (rebuilt 24 Nov 2026 after /tmp wipe lost the
# first version; expansion pools in gen_neco.py survived and are appended after this file).
# Sources (fetched 24 Nov 2026): JAMB official syllabus PDFs via IBASS https://ibass.jamb.gov.ng
# and byte-for-byte mirror https://jambsyllabus.com/ (checked 21 Nov 2026); WAEC syllabuses
# https://lekkiheadmaster.com/waec-syllabus/ ; JAMB topics https://allschool.ng/jamb-topics-for-all-subjects/ ;
# NECO syllabus via https://www.neco.gov.ng (Examinations > SSCE > Syllabuses; no direct PDF URL fetchable,
# summaries at https://myuniguide.com/neco-syllabus/ and https://masterneco.com.ng/neco-syllabus-2026-2027-is-out-for-all-subjects/);
# past questions online: JAMB Master https://jamb-master.web.app/ (12,166 real JAMB Qs 1983-2020, free);
# MySchoolGist JAMB PDFs; 9japastquestions.com (NECO needs free account - not used);
# ExamPadi/ExamCoach/TestaCBT (free tier capped - not used). No free downloadable NECO 2020-2023 PDF
# was found, so files are modelled on the repo's own real past questions (JAMB 2021-2025 and
# NECO 2024-2025 in ~/workspace/mystudy/data-repos/Exam-Questions-Data/json/) for topic coverage
# and style, ADAPTED (reworded, new numbers/names/option sets) - never copied verbatim
# (checked by normalised-text hash). Every question carries a "topic" syllabus field.
import json, math, random, re, pathlib
from fractions import Fraction

BASE = pathlib.Path('/home/hatch/workspace/mystudy/data-repos/Exam-Questions-Data/json')
YEARS = [2020, 2021, 2022, 2023]
SUBJECTS = ["Accounting","Agric","Biology","CRS","Chemistry","Civic","Commerce","Computer",
            "Economics","English","FurtherMath","Geography","Government","Hausa","History","IRS",
            "Igbo","Literature","Mathematics","Physics","Yoruba"]

SYLLABUS_URLS = ("JAMB IBASS https://ibass.jamb.gov.ng / mirror https://jambsyllabus.com/ ; "
                 "WAEC https://lekkiheadmaster.com/waec-syllabus/ ; NECO syllabus via https://www.neco.gov.ng "
                 "(Examinations > SSCE > Syllabuses)")

def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', str(s).lower()).strip()

def mk(year, subj, topic, q, correct, distractors, expl, adapted=""):
    return {"topic": topic, "q": q, "correct": correct, "distractors": list(distractors),
            "expl": expl, "year": year, "subj": subj,
            "adapted_from": adapted or (f"Repo JAMB_{subj}_2024.json / NECO_{subj}_2024.json "
                                         f"(topic coverage & style; adapted, not verbatim) | Syllabus: {SYLLABUS_URLS}")}

def finalise(raw, year, subj, seed):
    rng = random.Random(seed)
    opts = [raw["correct"]] + list(raw["distractors"])
    seen, uniq = set(), []
    for o in opts:
        if str(o) not in seen:
            seen.add(str(o)); uniq.append(o)
    assert len(uniq) == 4, f"bad options for {raw['q']!r}: {uniq}"
    rng.shuffle(uniq)
    ans = uniq.index(raw["correct"])
    return {"type": "std", "q": raw["q"], "opts": [str(o) for o in uniq], "ans": ans,
            "explanation": raw["expl"], "practice": True,
            "source": f"MyStudy Practice Set \u2014 modelled on the NECO syllabus for this subject, not the official {year} paper",
            "topic": raw["topic"], "adapted_from": raw["adapted_from"]}

def fmt_num(x):
    if isinstance(x, Fraction):
        if x.denominator == 1: return str(x.numerator)
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9: return str(int(round(x)))
        return f"{x:.2f}".rstrip('0').rstrip('.')
    return str(x)

# ---------------- MATHEMATICS ----------------
def maths_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Mathematics", t, q, c, d, e))
    for n, b in [(231,4),(1011,2),(342,5),(123,6),(210,3),(1101,2),(432,5),(101,7),(213,4),(321,5),
                 (10010,2),(122,3),(241,6),(110,8),(201,3),(314,5),(1001,2),(222,4),(135,6),(10101,2)]:
        v = int(str(n), b)
        add("Number Bases", f"Convert ${n}_{{{b}}}$ to base 10.", str(v),
            [str(v+1), str(v-1), str(v+2)], f"{n} in base {b} = {v} in base 10.")
    for p, amt in [(20,500),(15,800),(25,1200),(10,2500),(30,600),(12,1500),(5,4000),(40,750)]:
        v = p*amt//100
        add("Fractions, Decimals and Percentages", f"Find {p}% of \u20a6{amt:,}.", f"\u20a6{v:,}",
            [f"\u20a6{v+50:,}", f"\u20a6{v-50:,}", f"\u20a6{v*2:,}"], f"{p}% of {amt} = {p}/100 x {amt} = {v}.")
    for cp, sp in [(800,1000),(1200,900),(500,650),(2000,2400),(750,600),(1500,1800)]:
        pct = abs(sp-cp)*100//cp; kind = "profit" if sp > cp else "loss"
        add("Fractions, Decimals and Percentages", f"A trader bought an article for \u20a6{cp:,} and sold it for \u20a6{sp:,}. Find the percentage {kind}.", f"{pct}%",
            [f"{pct+5}%", f"{pct-5}%", f"{pct+10}%"], f"{kind.title()} = {abs(sp-cp)}, as a percentage of cost price {cp} = {pct}%.")
    for pr, r, t in [(5000,10,2),(8000,5,3),(12000,8,2),(20000,6,4),(4000,12,3),(15000,4,5)]:
        si = pr*r*t//100
        add("Fractions, Decimals and Percentages", f"Find the simple interest on \u20a6{pr:,} at {r}% per annum for {t} years.", f"\u20a6{si:,}",
            [f"\u20a6{si+200:,}", f"\u20a6{si-200:,}", f"\u20a6{si*2:,}"], f"I = PRT/100 = {pr} x {r} x {t} / 100 = {si}.")
    for a,b in [(2,3),(3,2),(5,2),(2,5),(4,2),(10,2)]:
        add("Indices, Logarithms and Surds", f"Evaluate: ${a}^{{{b}}}$.", str(a**b),
            [str(a**b+1), str(a*b), str(a**b-1)], f"{a} raised to power {b} = {a**b}.")
    add("Indices, Logarithms and Surds", "Simplify: $\\sqrt{98} - \\sqrt{50} + \\sqrt{32}$.", "$6\\sqrt{2}$",
        ["$4\\sqrt{2}$", "$8\\sqrt{2}$", "$10\\sqrt{2}$"], "7\u221a2 - 5\u221a2 + 4\u221a2 = 6\u221a2.")
    add("Indices, Logarithms and Surds", "If $\\log_{10} 2 = 0.3010$ and $\\log_{10} 3 = 0.4771$, find $\\log_{10} 18$.", "1.2552",
        ["0.7781", "1.0791", "1.3010"], "log 18 = log(2 x 3^2) = 0.3010 + 2(0.4771) = 1.2552.")
    add("Indices, Logarithms and Surds", "Evaluate: $(0.008)^{-1/3}$.", "5", ["0.2", "0.5", "2"],
        "(8/1000)^(-1/3) = (1000/8)^(1/3) = 10/2 = 5.")
    for n in [16,25,36,49,64,81]:
        add("Indices, Logarithms and Surds", f"Simplify: $\\sqrt{{{n}}} \\times \\sqrt{{2}} \\div \\sqrt{{2}}$.", str(int(math.isqrt(n))),
            [str(int(math.isqrt(n))+1), str(int(math.isqrt(n))-1), str(int(math.isqrt(n))*2)], f"\u221a{n} = {int(math.isqrt(n))}.")
    for a,b,c in [(2,3,11),(3,4,19),(5,2,27),(4,7,39),(2,9,25),(3,5,32),(6,1,25),(4,3,27)]:
        x = (c-b)//a
        add("Algebra", f"Solve for x: ${a}x + {b} = {c}$.", str(x), [str(x+1), str(x-1), str(x+2)],
            f"{a}x = {c-b}, so x = {x}.")
    for r1,r2 in [(2,3),(1,5),(2,4),(3,4),(1,6),(2,5),(3,5),(4,5)]:
        s, p = r1+r2, r1*r2
        add("Algebra", f"Find the roots of $x^2 - {s}x + {p} = 0$.", f"x = {r1} or x = {r2}",
            [f"x = {r1} or x = {r2+1}", f"x = -{r1} or x = -{r2}", f"x = {r1+1} or x = {r2}"], f"(x-{r1})(x-{r2}) = 0, so x = {r1} or {r2}.")
    for x,y in [(3,2),(4,1),(2,5),(5,3),(1,4),(3,4)]:
        s, d = x+y, x-y
        add("Algebra", f"Solve simultaneously: x + y = {s} and x - y = {d}.", f"x = {x}, y = {y}",
            [f"x = {x+1}, y = {y}", f"x = {x}, y = {y+1}", f"x = {y}, y = {x}"], f"Adding: 2x = {s+d}, x = {x}; then y = {y}.")
    for a,d,n in [(2,3,5),(5,2,6),(1,4,5),(3,3,4),(10,5,4),(4,6,5)]:
        v = a+(n-1)*d
        add("Sequences and Series", f"The {n}th term of an arithmetic progression with first term {a} and common difference {d} is:", str(v),
            [str(v+d), str(v-d), str(v+1)], f"Tn = a + (n-1)d = {a} + {n-1} x {d} = {v}.")
    for a,r,n in [(2,2,4),(3,2,3),(1,3,4),(2,3,3),(5,2,3),(4,2,4)]:
        v = a*(r**(n-1))
        add("Sequences and Series", f"The {n}th term of a geometric progression with first term {a} and common ratio {r} is:", str(v),
            [str(v*r), str(v//r if v//r else v+1), str(v+2)], f"Tn = ar^(n-1) = {a} x {r}^{n-1} = {v}.")
    for opp,hyp in [(3,5),(5,13),(8,10),(6,10),(9,15),(12,13)]:
        adj = int(math.isqrt(hyp*hyp-opp*opp))
        add("Geometry and Trigonometry", f"In a right-angled triangle with opposite side {opp} and hypotenuse {hyp}, find the adjacent side.", str(adj),
            [str(adj+1), str(adj-1), str(adj+2)], f"By Pythagoras, adjacent = \u221a({hyp}\u00b2 - {opp}\u00b2) = {adj}.")
    for r in [7,14,21,3,5,10]:
        area = 22*r*r//7
        add("Geometry and Trigonometry", f"Find the area of a circle of radius {r} cm. (Take \u03c0 = 22/7)", f"{area} cm\u00b2",
            [f"{area+22} cm\u00b2", f"{area-22} cm\u00b2", f"{2*22*r//7} cm\u00b2"], f"Area = \u03c0r\u00b2 = 22/7 x {r}\u00b2 = {area} cm\u00b2.")
    for l,w in [(12,8),(15,10),(20,6),(9,7),(18,5),(14,11)]:
        add("Geometry and Trigonometry", f"Find the area of a rectangle {l} cm long and {w} cm wide.", f"{l*w} cm\u00b2",
            [f"{l*w+10} cm\u00b2", f"{l+w} cm\u00b2", f"{2*(l+w)} cm\u00b2"], f"Area = length x width = {l} x {w} = {l*w} cm\u00b2.")
    for b,h in [(10,6),(8,5),(12,9),(20,7),(14,4),(16,10)]:
        add("Geometry and Trigonometry", f"Find the area of a triangle of base {b} cm and height {h} cm.", f"{b*h//2} cm\u00b2",
            [f"{b*h} cm\u00b2", f"{b*h//2+5} cm\u00b2", f"{b+h} cm\u00b2"], f"Area = 1/2 x base x height = {b*h//2} cm\u00b2.")
    for s in [4,5,6,8,10,12]:
        add("Geometry and Trigonometry", f"Find the volume of a cube of side {s} cm.", f"{s**3} cm\u00b3",
            [f"{s**2} cm\u00b3", f"{s*s+s} cm\u00b3", f"{s**3+10} cm\u00b3"], f"Volume = s\u00b3 = {s}\u00b3 = {s**3} cm\u00b3.")
    for data in [[2,4,6,8,10],[5,10,15,20],[3,6,9,12,15],[10,20,30,40],[4,8,12,16,20,24],[1,3,5,7,9,11]]:
        m = sum(data)/len(data)
        add("Statistics and Probability", f"Find the mean of {', '.join(map(str,data))}.", fmt_num(m),
            [fmt_num(m+1), fmt_num(m-1), fmt_num(m+2)], f"Mean = sum/count = {sum(data)}/{len(data)} = {fmt_num(m)}.")
    add("Statistics and Probability", "A fair die is thrown once. What is the probability of getting an even number?", "1/2",
        ["1/3", "1/6", "2/3"], "Even numbers are 2, 4, 6 out of 6 outcomes: 3/6 = 1/2.")
    add("Algebra", "If y varies directly as x and y = 12 when x = 3, find y when x = 7.", "28",
        ["21", "24", "36"], "y = kx, k = 4, so y = 4 x 7 = 28.")
    add("Algebra", "Solve the inequality: 2x - 3 > 7.", "x > 5", ["x < 5", "x > 2", "x < 2"], "2x > 10, so x > 5.")
    add("Algebra", "If U = {1,2,3,4,5,6} and A = {2,4,6}, find A'.", "{1,3,5}", ["{2,4,6}", "{1,2,3}", "{4,5,6}"],
        "The complement of A contains the elements of U not in A.")
    add("Number Bases", "Convert 45 to base 2.", "101101", ["101011", "110101", "101110"],
        "45 = 32+8+4+1 = 101101 in base 2.")
    add("Geometry and Trigonometry", "The sum of the interior angles of a pentagon is:", "540\u00b0",
        ["360\u00b0", "720\u00b0", "180\u00b0"], "(n-2) x 180\u00b0 = 3 x 180\u00b0 = 540\u00b0.")
    add("Geometry and Trigonometry", "sin 30\u00b0 is equal to:", "1/2", ["\u221a3/2", "1", "0"], "sin 30\u00b0 = 1/2.")
    add("Geometry and Trigonometry", "cos 60\u00b0 is equal to:", "1/2", ["\u221a3/2", "1", "0"], "cos 60\u00b0 = 1/2.")
    add("Geometry and Trigonometry", "tan 45\u00b0 is equal to:", "1", ["0", "1/2", "\u221a3"], "tan 45\u00b0 = 1.")
    add("Statistics and Probability", "The median of 3, 7, 5, 9, 11 is:", "7", ["5", "9", "3"],
        "Ordered: 3, 5, 7, 9, 11; the middle value is 7.")
    add("Statistics and Probability", "The mode of 2, 3, 3, 5, 7, 3, 8 is:", "3", ["2", "5", "7"],
        "3 occurs most often (three times).")
    add("Algebra", "Factorise: x\u00b2 - 9.", "(x - 3)(x + 3)", ["(x - 9)(x + 1)", "(x - 3)(x - 3)", "(x + 9)(x - 1)"],
        "Difference of two squares: a\u00b2 - b\u00b2 = (a-b)(a+b).")
    add("Algebra", "Expand: (x + 2)(x + 3).", "x\u00b2 + 5x + 6", ["x\u00b2 + 6x + 5", "x\u00b2 + 5x + 5", "x\u00b2 + 6x + 6"],
        "(x+2)(x+3) = x\u00b2 + 3x + 2x + 6 = x\u00b2 + 5x + 6.")
    return P

# ---------------- FURTHER MATHEMATICS ----------------
def furthermath_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "FurtherMath", t, q, c, d, e))
    for a,n in [(3,2),(2,3),(4,2),(5,2),(2,4),(3,3)]:
        add("Calculus", f"Differentiate y = {a}x^{n} with respect to x.", f"{a*n}x^{n-1}",
            [f"{a}x^{n-1}", f"{a*n}x^{n}", f"{a}x^{n}"], f"dy/dx = {a} x {n} x^{n-1} = {a*n}x^{n-1}.")
    for a,n in [(2,3),(3,2),(4,3),(1,4),(5,2),(2,2)]:
        coeff = Fraction(a, n+1)
        add("Calculus", f"Integrate {a}x^{n} dx.", f"{fmt_num(coeff)}x^{n+1} + C",
            [f"{a}x^{n+1} + C", f"{fmt_num(coeff)}x^{n} + C", f"{a*n}x^{n-1} + C"],
            f"\u222b {a}x^{n} dx = {a}/(n+1) x^{n+1} + C.")
    for a,b,c,d in [(1,2,3,4),(2,1,1,3),(3,2,1,2),(1,3,2,5),(2,2,3,1),(4,1,2,3)]:
        det = a*d-b*c
        add("Matrices", f"Find the determinant of the matrix [[{a}, {b}], [{c}, {d}]].", str(det),
            [str(det+1), str(det-1), str(a*d+b*c)], f"det = ad - bc = {a}x{d} - {b}x{c} = {det}.")
    for n in [5,6,7,8,4,9]:
        add("Combinatorics", f"Evaluate {n}! / ({n-2})!.", str(n*(n-1)),
            [str(n*(n-1)+1), str(n), str((n-1)*(n-2))], f"{n}!/({n-2})! = {n} x {n-1} = {n*(n-1)}.")
    for n,r in [(5,2),(6,2),(7,3),(5,3),(8,2),(6,3)]:
        v = math.comb(n, r)
        add("Combinatorics", f"Evaluate C({n}, {r}).", str(v),
            [str(v+1), str(v-1), str(math.perm(n, r))], f"C({n},{r}) = {n}!/({r}!({n-r})!) = {v}.")
    for n,r in [(5,2),(6,3),(4,2),(7,2),(5,3),(6,2)]:
        v = math.perm(n, r)
        add("Combinatorics", f"Evaluate P({n}, {r}).", str(v),
            [str(v+1), str(v-1), str(math.comb(n, r))], f"P({n},{r}) = {n}!/({n-r})! = {v}.")
    for a,b in [(3,4),(5,12),(8,15),(6,8),(9,12),(20,21)]:
        mod = int(math.isqrt(a*a+b*b))
        add("Vectors and Complex Numbers", f"Find the magnitude of the vector ({a}, {b}).", str(mod),
            [str(mod+1), str(mod-1), str(a+b)], f"|v| = \u221a({a}\u00b2 + {b}\u00b2) = {mod}.")
    for a,b in [(2,3),(3,4),(1,5),(4,3),(2,1),(5,2)]:
        add("Vectors and Complex Numbers", f"Find the modulus of the complex number {a} + {b}i.", f"\u221a{a*a+b*b}",
            [f"\u221a{a*a+b*b-1}", f"{a+b}", f"\u221a{a*a-b*b}"], f"|z| = \u221a(a\u00b2 + b\u00b2) = \u221a{a*a+b*b}.")
    _sin_dis = {0: ["1/2", "1", "-1"], 30: ["0", "1", "\u221a3/2"], 45: ["0", "1/2", "1"],
                60: ["0", "1/2", "1"], 90: ["0", "1/2", "\u221a3/2"]}
    for x in [0,30,45,60,90]:
        add("Trigonometry", f"Find sin {x}\u00b0.", {0:"0",30:"1/2",45:"\u221a2/2",60:"\u221a3/2",90:"1"}[x],
            _sin_dis[x], "Standard trigonometric value.")
    for a in [2,3,4,5,6,8]:
        add("Indices and Logarithms", f"Solve for x: 2^x = {2**a}.", str(a), [str(a+1), str(a-1), str(2*a)],
            f"2^x = 2^{a}, so x = {a}.")
    for a,b in [(10,5),(12,3),(15,5),(20,4)]:
        add("Algebra", f"Find the sum of the first {b} terms of an AP with first term {a} and common difference {a}.",
            str(b*(2*a+(b-1)*a)//2), [str(b*a), str(b*(2*a+(b-1)*a)//2+10), str(b*(2*a+(b-1)*a)//2-10)],
            f"Sn = n/2[2a + (n-1)d] = {b*(2*a+(b-1)*a)//2}.")
    add("Calculus", "The derivative of sin x with respect to x is:", "cos x", ["-sin x", "-cos x", "tan x"],
        "d/dx(sin x) = cos x.")
    add("Calculus", "The derivative of cos x with respect to x is:", "-sin x", ["sin x", "cos x", "-cos x"],
        "d/dx(cos x) = -sin x.")
    add("Calculus", "The integral of 1/x dx is:", "ln|x| + C", ["x + C", "e^x + C", "1/x\u00b2 + C"],
        "\u222b 1/x dx = ln|x| + C.")
    add("Calculus", "Find the gradient of y = x\u00b2 at x = 3.", "6", ["3", "9", "12"], "dy/dx = 2x = 6 at x = 3.")
    add("Calculus", "Find the stationary point of y = x\u00b2 - 4x + 3.", "x = 2", ["x = 4", "x = 1", "x = 3"],
        "dy/dx = 2x - 4 = 0 gives x = 2.")
    add("Matrices", "A matrix with the same number of rows and columns is called a:", "square matrix",
        ["rectangular matrix", "column matrix", "row matrix"], "Equal rows and columns define a square matrix.")
    add("Matrices", "The identity matrix I satisfies:", "AI = A", ["AI = 0", "AI = I", "AI = -A"],
        "Multiplying by the identity matrix leaves a matrix unchanged.")
    add("Vectors and Complex Numbers", "The conjugate of 3 + 4i is:", "3 - 4i", ["-3 + 4i", "3 + 4i", "-3 - 4i"],
        "The conjugate changes the sign of the imaginary part.")
    add("Vectors and Complex Numbers", "i\u00b2 is equal to:", "-1", ["1", "0", "i"], "By definition i = \u221a(-1), so i\u00b2 = -1.")
    add("Trigonometry", "sin\u00b2\u03b8 + cos\u00b2\u03b8 equals:", "1", ["0", "2", "tan\u00b2\u03b8"],
        "The fundamental Pythagorean identity.")
    add("Trigonometry", "The period of sin x is:", "2\u03c0", ["\u03c0", "4\u03c0", "\u03c0/2"], "sin x repeats every 2\u03c0 radians.")
    add("Algebra", "The sum of the roots of x\u00b2 - 5x + 6 = 0 is:", "5", ["6", "-5", "2"], "Sum of roots = -b/a = 5.")
    add("Algebra", "The product of the roots of x\u00b2 - 5x + 6 = 0 is:", "6", ["5", "-6", "2"], "Product of roots = c/a = 6.")
    add("Combinatorics", "In how many ways can 4 books be arranged on a shelf?", "24", ["12", "16", "8"], "4! = 24.")
    add("Combinatorics", "The binomial expansion of (1 + x)\u00b2 is:", "1 + 2x + x\u00b2", ["1 + x + x\u00b2", "1 + 2x + 2x\u00b2", "1 + x\u00b2"],
        "(1+x)\u00b2 = 1 + 2x + x\u00b2.")
    add("Statistics", "The variance of 2, 4, 6 is:", "8/3", ["2", "4", "16/3"],
        "Mean = 4; squared deviations 4, 0, 4; variance = 8/3.")
    add("Statistics", "If the mean of 5 numbers is 12, their sum is:", "60", ["17", "24", "7"],
        "Sum = mean x count = 12 x 5 = 60.")
    return P

# ---------------- PHYSICS ----------------
def physics_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Physics", t, q, c, d, e))
    for u,a,t in [(0,2,5),(10,2,4),(5,3,3),(20,4,2),(0,10,3),(15,5,4)]:
        v = u+a*t
        add("Motion", f"A body starts with velocity {u} m/s and accelerates at {a} m/s\u00b2 for {t} s. Find its final velocity.", f"{v} m/s",
            [f"{v+2} m/s", f"{v-2} m/s", f"{u+a} m/s"], f"v = u + at = {u} + {a}x{t} = {v} m/s.")
    for m,a in [(5,2),(10,3),(4,5),(20,2),(8,4),(15,2)]:
        add("Motion", f"Find the force needed to accelerate a {m} kg mass at {a} m/s\u00b2.", f"{m*a} N",
            [f"{m*a+5} N", f"{m+a} N", f"{m*a-5} N"], f"F = ma = {m} x {a} = {m*a} N.")
    for m,h in [(10,5),(5,10),(20,3),(2,20),(4,15),(50,2)]:
        add("Work, Energy and Power", f"Find the potential energy of a {m} kg mass at a height of {h} m. (g = 10 m/s\u00b2)", f"{m*h*10} J",
            [f"{m*h*5} J", f"{m*h*10+100} J", f"{m+h} J"], f"PE = mgh = {m} x 10 x {h} = {m*h*10} J.")
    for m,v in [(2,10),(4,5),(10,4),(5,6),(8,3),(20,2)]:
        ke = Fraction(m*v*v, 2)
        add("Work, Energy and Power", f"Find the kinetic energy of a {m} kg body moving at {v} m/s.", f"{fmt_num(ke)} J",
            [f"{m*v+5} J", f"{fmt_num(ke*2)} J", f"{fmt_num(ke+10)} J"], f"KE = 1/2 mv\u00b2 = 1/2 x {m} x {v}\u00b2 = {fmt_num(ke)} J.")
    for w,t in [(100,10),(200,20),(500,25),(120,12),(300,15),(60,6)]:
        add("Work, Energy and Power", f"A machine does {w} J of work in {t} s. Find its power.", f"{w//t} W",
            [f"{w//t+5} W", f"{w*t} W", f"{w//t-2} W"], f"Power = work/time = {w}/{t} = {w//t} W.")
    for v,i in [(12,2),(24,3),(10,5),(20,4),(6,3),(30,5)]:
        add("Electricity", f"Find the resistance of a conductor when a potential difference of {v} V drives a current of {i} A through it.", f"{v//i} \u03a9",
            [f"{v*i} \u03a9", f"{v//i+1} \u03a9", f"{v+i} \u03a9"], f"R = V/I = {v}/{i} = {v//i} \u03a9.")
    for v,i in [(12,2),(24,4),(10,2),(20,5),(6,2),(30,6)]:
        add("Electricity", f"Find the power dissipated when {v} V drives {i} A through a resistor.", f"{v*i} W",
            [f"{v+i} W", f"{v*i+10} W", f"{v//i} W"], f"P = VI = {v} x {i} = {v*i} W.")
    for f,l in [(50,2),(100,3),(20,5),(200,1),(25,4),(10,10)]:
        add("Waves", f"A wave of frequency {f} Hz has wavelength {l} m. Find its speed.", f"{f*l} m/s",
            [f"{f+l} m/s", f"{f//l+10 if f>=l else f*l+10} m/s", f"{f*l+50} m/s"], f"v = f\u03bb = {f} x {l} = {f*l} m/s.")
    for m,v in [(10,2),(5,4),(20,1),(4,5),(8,2),(2,10)]:
        add("Motion", f"Find the density of a body of mass {m} kg and volume {v} m\u00b3.", f"{fmt_num(m/v)} kg/m\u00b3",
            [f"{m*v+2} kg/m\u00b3", f"{fmt_num(m/v+3)} kg/m\u00b3", f"{v+1} kg/m\u00b3"], f"Density = mass/volume = {m}/{v} = {fmt_num(m/v)} kg/m\u00b3.")
    for f,a in [(100,10),(200,20),(50,5),(150,15),(80,8),(120,12)]:
        add("Pressure", f"A force of {f} N acts on an area of {a} m\u00b2. Find the pressure.", f"{f//a} Pa",
            [f"{f*a} Pa", f"{f//a+5} Pa", f"{f//a+2} Pa"], f"Pressure = force/area = {f}/{a} = {f//a} Pa.")
    for c in [10,20,30,40,50,60]:
        add("Heat", f"Find the heat required to raise {c} g of water by 1\u00b0C. (Specific heat capacity of water = 4.2 J/g\u00b0C)", f"{c*42//10} J",
            [f"{c*2} J", f"{c*42//10+50} J", f"{c} J"], f"Q = mc\u0394\u03b8 = {c} x 4.2 x 1 = {c*42//10} J.")
    facts = [
        ("Measurements and Units", "The SI unit of force is the:", "newton", ["joule", "watt", "pascal"], "Force is measured in newtons (N)."),
        ("Measurements and Units", "The SI unit of energy is the:", "joule", ["newton", "watt", "volt"], "Energy is measured in joules (J)."),
        ("Measurements and Units", "The SI unit of power is the:", "watt", ["joule", "newton", "ohm"], "Power is measured in watts (W)."),
        ("Measurements and Units", "The SI unit of electric current is the:", "ampere", ["volt", "ohm", "watt"], "Current is measured in amperes (A)."),
        ("Measurements and Units", "Which of these is a vector quantity?", "velocity", ["speed", "distance", "mass"], "Velocity has both magnitude and direction."),
        ("Measurements and Units", "Which of these is a scalar quantity?", "speed", ["velocity", "force", "acceleration"], "Speed has magnitude only."),
        ("Motion", "Newton's first law of motion is also called the law of:", "inertia", ["gravitation", "action and reaction", "conservation of energy"], "A body remains at rest or in uniform motion unless acted on by a force."),
        ("Motion", "The acceleration due to gravity on Earth is approximately:", "10 m/s\u00b2", ["5 m/s\u00b2", "20 m/s\u00b2", "100 m/s\u00b2"], "g \u2248 9.8 m/s\u00b2, taken as 10 m/s\u00b2 in school work."),
        ("Motion", "A body falling freely under gravity has:", "constant acceleration", ["constant velocity", "zero acceleration", "decreasing acceleration"], "Free fall is uniformly accelerated motion."),
        ("Waves", "Sound waves are:", "longitudinal waves", ["transverse waves", "electromagnetic waves", "stationary waves"], "Sound travels as compressions and rarefactions in the medium."),
        ("Waves", "Light waves are:", "transverse electromagnetic waves", ["longitudinal waves", "sound waves", "mechanical waves"], "Light is a transverse electromagnetic wave and needs no medium."),
        ("Waves", "The speed of light in a vacuum is approximately:", "3 x 10^8 m/s", ["3 x 10^6 m/s", "3 x 10^5 m/s", "3 x 10^10 m/s"], "c \u2248 3.0 x 10^8 m/s."),
        ("Waves", "The unit of frequency is the:", "hertz", ["watt", "tesla", "weber"], "Frequency is measured in hertz (Hz)."),
        ("Electricity", "An instrument used to measure electric current is the:", "ammeter", ["voltmeter", "ohmmeter", "galvanometer"], "An ammeter is connected in series to measure current."),
        ("Electricity", "An instrument used to measure potential difference is the:", "voltmeter", ["ammeter", "ohmmeter", "barometer"], "A voltmeter is connected in parallel across the component."),
        ("Electricity", "In a series circuit, the current is:", "the same everywhere", ["greatest at the battery", "least at the battery", "different in each resistor"], "Series components carry the same current."),
        ("Electricity", "The resistance of a wire increases when its:", "length increases", ["cross-sectional area increases", "temperature decreases", "length decreases"], "R = \u03c1L/A, so longer wire means greater resistance."),
        ("Heat", "Heat is transferred through a vacuum by:", "radiation", ["conduction", "convection", "evaporation"], "Radiation needs no medium; the Sun's heat reaches Earth this way."),
        ("Heat", "The instrument used to measure temperature is the:", "thermometer", ["barometer", "hygrometer", "manometer"], "A thermometer measures temperature."),
        ("Optics", "The image formed by a plane mirror is:", "virtual and laterally inverted", ["real and inverted", "real and upright", "virtual and magnified"], "A plane mirror forms a virtual image the same size as the object, with left-right reversal."),
        ("Optics", "The angle of incidence equals the angle of reflection. This is the law of:", "reflection", ["refraction", "diffraction", "interference"], "The first law of reflection."),
        ("Modern Physics", "The particle that carries electric charge in a metal is the:", "electron", ["proton", "neutron", "photon"], "Free electrons carry current in metals."),
        ("Modern Physics", "The nucleus of an atom contains:", "protons and neutrons", ["electrons and protons", "electrons only", "protons only"], "Protons and neutrons make up the nucleus."),
        ("Pressure", "Atmospheric pressure is measured with a:", "barometer", ["thermometer", "manometer", "hydrometer"], "A barometer measures air pressure."),
        ("Pressure", "The pressure in a liquid increases with:", "depth", ["surface area", "volume", "temperature"], "P = \u03c1gh, so pressure grows with depth."),
        ("Simple Machines", "The mechanical advantage of a machine is:", "load/effort", ["effort/load", "load x effort", "effort - load"], "MA = load divided by effort."),
        ("Elasticity", "Hooke's law states that extension is proportional to:", "the applied force", ["the original length", "the cross-sectional area", "the temperature"], "Within the elastic limit, extension \u221d load."),
        ("Gravitational Field", "The force of attraction between two masses depends on:", "their masses and the distance between them", ["their colours", "their temperatures", "their volumes only"], "Newton's law of universal gravitation."),
        ("Equilibrium of Forces", "A body is in equilibrium when the resultant force on it is:", "zero", ["maximum", "equal to its weight", "equal to its mass"], "Equilibrium means no net force and no net moment."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- CHEMISTRY ----------------
def chemistry_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Chemistry", t, q, c, d, e))
    elements = [("Hydrogen","H"),("Helium","He"),("Carbon","C"),("Nitrogen","N"),("Oxygen","O"),
                ("Fluorine","F"),("Sodium","Na"),("Magnesium","Mg"),("Aluminium","Al"),("Silicon","Si"),
                ("Phosphorus","P"),("Sulphur","S"),("Chlorine","Cl"),("Potassium","K"),("Calcium","Ca"),
                ("Iron","Fe"),("Copper","Cu"),("Zinc","Zn"),("Silver","Ag"),("Gold","Au"),
                ("Lead","Pb"),("Tin","Sn"),("Mercury","Hg"),("Iodine","I"),("Bromine","Br")]
    for name, sym in elements:
        others = [s for n, s in elements if s != sym][:3]
        add("Atomic Structure and Periodicity", f"What is the chemical symbol for {name}?", sym, others,
            f"The symbol for {name} is {sym}.")
    compounds = [("water, H\u2082O", 18), ("carbon dioxide, CO\u2082", 44), ("sodium chloride, NaCl", 58.5),
                 ("sulphuric acid, H\u2082SO\u2084", 98), ("ammonia, NH\u2083", 17), ("methane, CH\u2084", 16),
                 ("calcium carbonate, CaCO\u2083", 100), ("nitric acid, HNO\u2083", 63),
                 ("sodium hydroxide, NaOH", 40), ("hydrochloric acid, HCl", 36.5)]
    for name, mm in compounds:
        add("Chemical Combination", f"What is the molar mass of {name}?", f"{fmt_num(mm)} g/mol",
            [f"{fmt_num(mm+10)} g/mol", f"{fmt_num(mm-5)} g/mol", f"{fmt_num(mm*2)} g/mol"],
            f"Adding the atomic masses gives {fmt_num(mm)} g/mol.")
    for mass, mm, name in [(36,18,"water"),(88,44,"carbon dioxide"),(117,58.5,"sodium chloride"),
                           (34,17,"ammonia"),(32,16,"methane"),(80,40,"sodium hydroxide"),
                           (196,98,"sulphuric acid"),(200,100,"calcium carbonate")]:
        moles = mass/mm
        add("Chemical Combination", f"How many moles are in {fmt_num(mass)} g of {name}?", f"{fmt_num(moles)} mol",
            [f"{fmt_num(moles+1)} mol", f"{fmt_num(moles*2)} mol", f"{fmt_num(moles/2)} mol"],
            f"Moles = mass/molar mass = {fmt_num(mass)}/{fmt_num(mm)} = {fmt_num(moles)} mol.")
    for p1,v1,p2 in [(100,2,200),(50,4,100),(200,3,300),(80,5,200),(120,6,240),(60,10,300)]:
        v2 = p1*v1//p2
        add("Kinetic Theory and Gas Laws", f"A gas at {p1} kPa occupies {v1} dm\u00b3. At constant temperature, what volume will it occupy at {p2} kPa?", f"{v2} dm\u00b3",
            [f"{v2+1} dm\u00b3", f"{v2+3} dm\u00b3", f"{p1*v1} dm\u00b3"], f"Boyle's law: P1V1 = P2V2, so V2 = {p1}x{v1}/{p2} = {v2} dm\u00b3.")
    facts = [
        ("Atomic Structure and Periodicity", "The atomic number of an element is the number of:", "protons", ["neutrons", "electrons and neutrons", "nucleons"], "Atomic number = number of protons in the nucleus."),
        ("Atomic Structure and Periodicity", "Isotopes of an element have the same number of protons but different numbers of:", "neutrons", ["protons", "electrons", "shells"], "Isotopes differ in neutron number, hence in mass number."),
        ("Atomic Structure and Periodicity", "The vertical columns of the periodic table are called:", "groups", ["periods", "blocks", "series"], "Groups run vertically; periods run horizontally."),
        ("Atomic Structure and Periodicity", "Elements in the same group have the same number of:", "valence electrons", ["protons", "neutrons", "shells"], "Group number gives the number of outer-shell electrons."),
        ("Chemical Bonding", "A covalent bond is formed by:", "sharing of electrons", ["transfer of electrons", "sharing of protons", "transfer of protons"], "Covalent bonding is electron sharing."),
        ("Chemical Bonding", "An ionic bond is formed by:", "transfer of electrons", ["sharing of electrons", "sharing of neutrons", "transfer of neutrons"], "Ionic bonding is electron transfer between metal and non-metal."),
        ("Chemical Bonding", "Which of these is an ionic compound?", "sodium chloride", ["methane", "carbon dioxide", "water"], "NaCl is held together by ionic bonds."),
        ("Acids, Bases and Salts", "The pH of a neutral solution at 25\u00b0C is:", "7", ["0", "14", "1"], "Neutral solutions have pH 7."),
        ("Acids, Bases and Salts", "An acid turns blue litmus paper:", "red", ["green", "blue", "yellow"], "Acids turn blue litmus red; alkalis turn red litmus blue."),
        ("Acids, Bases and Salts", "The reaction between an acid and a base produces:", "salt and water", ["hydrogen only", "oxygen only", "salt only"], "Neutralisation gives salt + water."),
        ("Acids, Bases and Salts", "Which of these is a strong acid?", "hydrochloric acid", ["ethanoic acid", "carbonic acid", "citric acid"], "HCl ionises completely in water."),
        ("Acids, Bases and Salts", "A substance that changes colour in acids and alkalis is called an:", "indicator", ["catalyst", "inhibitor", "electrolyte"], "Indicators such as litmus show whether a solution is acidic or alkaline."),
        ("Separation of Mixtures", "The best method to obtain pure water from salty water is:", "distillation", ["filtration", "evaporation", "decantation"], "Distillation separates a liquid from dissolved solids by boiling and condensing."),
        ("Separation of Mixtures", "Filtration is used to separate:", "an insoluble solid from a liquid", ["two miscible liquids", "a soluble solid from a liquid", "two gases"], "The solid stays on the filter paper while the liquid passes through."),
        ("Separation of Mixtures", "A mixture of iron filings and sulphur can be separated using a:", "magnet", ["filter paper", "distillation flask", "separating funnel"], "Iron is magnetic; sulphur is not."),
        ("Organic Chemistry", "The general formula of alkanes is:", "C\u2099H\u2082\u2099\u208a\u2082", ["C\u2099H\u2082\u2099", "C\u2099H\u2082\u2099\u208b\u2082", "C\u2099H\u2082\u2099\u208a\u2081"], "Alkanes are saturated hydrocarbons, C\u2099H\u2082\u2099\u208a\u2082."),
        ("Organic Chemistry", "Methane belongs to the homologous series of:", "alkanes", ["alkenes", "alkynes", "alcohols"], "Methane, CH\u2084, is the first alkane."),
        ("Organic Chemistry", "Ethene is an example of an:", "alkene", ["alkane", "alkyne", "alcohol"], "Ethene has a carbon-carbon double bond."),
        ("Organic Chemistry", "The functional group of alcohols is:", "-OH", ["-COOH", "-CHO", "-NH\u2082"], "Alcohols contain the hydroxyl group -OH."),
        ("Organic Chemistry", "The functional group of carboxylic acids is:", "-COOH", ["-OH", "-CHO", "-CO-"], "Carboxylic acids contain -COOH."),
        ("Chemical Reactions", "A reaction in which heat is given out is called:", "exothermic", ["endothermic", "reversible", "catalytic"], "Exothermic reactions release heat to the surroundings."),
        ("Chemical Reactions", "A catalyst is a substance that:", "speeds up a reaction without being used up", ["slows down all reactions", "is used up in a reaction", "changes the products of a reaction"], "A catalyst increases the rate but is not consumed."),
        ("Electrolysis", "During electrolysis, the positive electrode is the:", "anode", ["cathode", "electrolyte", "salt bridge"], "The anode is positive; anions move towards it."),
        ("Electrolysis", "At the cathode during electrolysis, the process is:", "reduction", ["oxidation", "neutralisation", "combustion"], "Reduction (gain of electrons) occurs at the cathode."),
        ("Non-Metals and Their Compounds", "The gas released when dilute hydrochloric acid reacts with zinc is:", "hydrogen", ["oxygen", "carbon dioxide", "chlorine"], "Metal + acid gives salt + hydrogen."),
        ("Non-Metals and Their Compounds", "Limestone is mainly:", "calcium carbonate", ["calcium oxide", "sodium carbonate", "calcium chloride"], "Limestone is CaCO\u2083."),
        ("Metals and Their Compounds", "The most reactive metal among sodium, zinc, copper and iron is:", "sodium", ["zinc", "copper", "iron"], "Sodium is at the top of the reactivity series among these."),
        ("Metals and Their Compounds", "Rusting of iron requires:", "oxygen and water", ["oxygen only", "water only", "carbon dioxide only"], "Iron rusts only when both air (oxygen) and water are present."),
        ("Chemical Combination", "Avogadro's number is approximately:", "6.02 x 10\u00b2\u00b3", ["6.02 x 10\u00b2\u00b2", "3.01 x 10\u00b2\u00b3", "6.02 x 10\u00b2\u2074"], "One mole contains 6.02 x 10\u00b2\u00b3 particles."),
        ("Chemical Combination", "The relative atomic mass of carbon-12 is:", "12", ["6", "14", "1"], "Carbon-12 is the standard, with relative atomic mass 12."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- BIOLOGY ----------------
def biology_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Biology", t, q, c, d, e))
    organelles = [("powerhouse of the cell", "mitochondrion", ["ribosome", "nucleus", "Golgi body"]),
                  ("site of photosynthesis", "chloroplast", ["mitochondrion", "vacuole", "nucleus"]),
                  ("controls all cell activities", "nucleus", ["cytoplasm", "ribosome", "cell membrane"]),
                  ("site of protein synthesis", "ribosome", ["lysosome", "chloroplast", "vacuole"]),
                  ("controls what enters and leaves the cell", "cell membrane", ["cell wall", "cytoplasm", "nucleus"]),
                  ("stores water and food in plant cells", "vacuole", ["ribosome", "mitochondrion", "lysosome"]),
                  ("packages and distributes proteins", "Golgi body", ["ribosome", "nucleus", "vacuole"]),
                  ("digests worn-out cell parts", "lysosome", ["ribosome", "chloroplast", "Golgi body"])]
    for role, ans, dis in organelles:
        add("Cell Biology", f"Which organelle is the {role}?", ans, dis, f"The {ans} is the {role}.")
    vitamins = [("Vitamin A", "night blindness"), ("Vitamin B1", "beriberi"), ("Vitamin C", "scurvy"),
                ("Vitamin D", "rickets"), ("Vitamin B3 (niacin)", "pellagra"), ("Iodine", "goitre"),
                ("Iron", "anaemia"), ("Vitamin K", "poor blood clotting")]
    for nut, disease in vitamins:
        others = [d for n, d in vitamins if d != disease][:3]
        add("Nutrition", f"Deficiency of {nut} causes:", disease, others, f"Lack of {nut} leads to {disease}.")
    hormones = [("insulin", "pancreas", "lowers blood sugar"), ("adrenaline", "adrenal gland", "prepares the body for emergency"),
                ("thyroxine", "thyroid gland", "controls metabolic rate"), ("growth hormone", "pituitary gland", "stimulates growth"),
                ("oestrogen", "ovary", "develops female secondary sexual characteristics"),
                ("testosterone", "testis", "develops male secondary sexual characteristics"),
                ("glucagon", "pancreas", "raises blood sugar")]
    for h, gland, fn in hormones:
        add("Coordination and Control", f"The hormone {h} is produced by the {gland} and {fn}. Which hormone is described?", h,
            [x[0] for x in hormones if x[0] != h][:3], f"{h} is produced by the {gland}; it {fn}.")
    diseases = [("malaria", "Plasmodium (a protozoan)"), ("cholera", "Vibrio cholerae (a bacterium)"),
                ("tuberculosis", "Mycobacterium tuberculosis (a bacterium)"), ("HIV/AIDS", "human immunodeficiency virus"),
                ("ringworm", "a fungus"), ("sleeping sickness", "Trypanosoma (a protozoan)"),
                ("measles", "a virus"), ("typhoid", "Salmonella typhi (a bacterium)")]
    for dis_name, cause in diseases:
        others = [c for n, c in diseases if c != cause][:3]
        add("Health and Disease", f"{dis_name.capitalize()} is caused by:", cause, others,
            f"{dis_name.capitalize()} is caused by {cause}.")
    facts = [
        ("Cell Biology", "The basic unit of life is the:", "cell", ["tissue", "organ", "system"], "All living things are made of cells."),
        ("Cell Biology", "Mitosis produces:", "two identical daughter cells", ["four different cells", "two different cells", "one cell"], "Mitosis gives two genetically identical diploid cells."),
        ("Cell Biology", "Meiosis produces:", "four haploid cells", ["two diploid cells", "four diploid cells", "two haploid cells"], "Meiosis gives four genetically different haploid gametes."),
        ("Cell Biology", "Osmosis is the movement of water molecules:", "from a dilute to a concentrated solution through a semi-permeable membrane", ["from a concentrated to a dilute solution", "through a fully permeable membrane", "against a concentration gradient by active transport"], "Osmosis moves water down its concentration gradient across a semi-permeable membrane."),
        ("Cell Biology", "Diffusion is the movement of molecules from a region of:", "higher to lower concentration", ["lower to higher concentration", "equal concentration", "no concentration"], "Diffusion is down the concentration gradient."),
        ("Classification", "The scientific name of humans is:", "Homo sapiens", ["Homo erectus", "Pan troglodytes", "Gorilla gorilla"], "Humans are Homo sapiens."),
        ("Classification", "Which of these is a monocotyledonous plant?", "maize", ["beans", "groundnut", "mango"], "Maize has one cotyledon; beans, groundnut and mango are dicots."),
        ("Classification", "Which of these is a dicotyledonous plant?", "beans", ["maize", "rice", "palm tree"], "Beans have two cotyledons."),
        ("Classification", "A mammal is distinguished from other vertebrates by:", "mammary glands and hair", ["scales", "feathers", "laying eggs in water"], "Mammals have hair and feed their young with milk."),
        ("Classification", "The human chromosome number is:", "46", ["23", "44", "48"], "Humans have 46 chromosomes (23 pairs) in body cells."),
        ("Genetics", "The genotype of a homozygous dominant tall pea plant is:", "TT", ["Tt", "tt", "tT"], "Homozygous dominant means two dominant alleles, TT."),
        ("Genetics", "A cross between Tt and tt gives a phenotypic ratio of:", "1:1", ["3:1", "1:2:1", "2:1"], "Half the offspring are Tt (tall) and half tt (short)."),
        ("Genetics", "The gene for a trait is carried on a:", "chromosome", ["ribosome", "mitochondrion", "vacuole"], "Genes are sections of DNA on chromosomes."),
        ("Genetics", "DNA is found mainly in the:", "nucleus", ["cytoplasm", "ribosome", "cell wall"], "Most DNA is in the nucleus."),
        ("Ecology", "The organisms that produce food in an ecosystem are the:", "producers", ["consumers", "decomposers", "scavengers"], "Producers (green plants) make food by photosynthesis."),
        ("Ecology", "A food chain always begins with a:", "producer", ["herbivore", "carnivore", "decomposer"], "Producers capture energy from sunlight first."),
        ("Ecology", "The relationship in which both organisms benefit is:", "mutualism", ["parasitism", "commensalism", "predation"], "In mutualism both partners gain."),
        ("Ecology", "The relationship in which one organism benefits and the other is harmed is:", "parasitism", ["mutualism", "commensalism", "competition"], "A parasite gains at its host's expense."),
        ("Ecology", "The gradual change in a community over time is called:", "succession", ["evolution", "adaptation", "migration"], "Succession is the orderly replacement of communities."),
        ("Physiology", "The organ that pumps blood around the body is the:", "heart", ["liver", "kidney", "lung"], "The heart pumps blood through the circulatory system."),
        ("Physiology", "Gaseous exchange in humans takes place in the:", "alveoli", ["bronchi", "trachea", "diaphragm"], "Alveoli are the air sacs where oxygen and carbon dioxide are exchanged."),
        ("Physiology", "The functional unit of the kidney is the:", "nephron", ["neuron", "alveolus", "villus"], "Nephrons filter blood and form urine."),
        ("Physiology", "The part of the flower that produces pollen is the:", "anther", ["stigma", "ovary", "petal"], "Anthers produce pollen grains."),
        ("Physiology", "Photosynthesis takes place mainly in the:", "leaf", ["root", "stem", "flower"], "Leaves contain chlorophyll in chloroplasts."),
        ("Physiology", "The raw materials for photosynthesis are:", "carbon dioxide and water", ["oxygen and glucose", "nitrogen and water", "carbon dioxide and oxygen"], "6CO\u2082 + 6H\u2082O -> C\u2086H\u2081\u2082O\u2086 + 6O\u2082."),
        ("Physiology", "The green pigment in plants is:", "chlorophyll", ["haemoglobin", "melanin", "carotene"], "Chlorophyll absorbs light for photosynthesis."),
        ("Physiology", "The enzyme that digests starch in the mouth is:", "ptyalin (salivary amylase)", ["pepsin", "lipase", "trypsin"], "Ptyalin in saliva begins starch digestion."),
        ("Physiology", "Bile is produced by the:", "liver", ["pancreas", "gall bladder", "stomach"], "The liver makes bile, which is stored in the gall bladder."),
        ("Physiology", "The part of the brain that controls balance is the:", "cerebellum", ["cerebrum", "medulla", "hypothalamus"], "The cerebellum coordinates movement and balance."),
        ("Physiology", "The part of the eye that focuses light is the:", "lens", ["iris", "retina", "cornea"], "The lens focuses light onto the retina."),
        ("Reproduction", "Fertilisation in humans takes place in the:", "fallopian tube", ["uterus", "ovary", "vagina"], "The sperm meets the egg in the fallopian tube."),
        ("Reproduction", "The male reproductive cell is the:", "sperm", ["ovum", "zygote", "embryo"], "The sperm is the male gamete."),
        ("Reproduction", "Pollination is the transfer of pollen from the anther to the:", "stigma", ["ovary", "petal", "sepal"], "Pollen lands on the stigma."),
        ("Evolution", "The scientist associated with the theory of evolution by natural selection is:", "Charles Darwin", ["Gregor Mendel", "Louis Pasteur", "Robert Hooke"], "Darwin proposed natural selection."),
        ("Evolution", "The scientist associated with the laws of inheritance is:", "Gregor Mendel", ["Charles Darwin", "Jean Lamarck", "Alexander Fleming"], "Mendel worked out inheritance from pea plants."),
        ("Nutrition", "The food test for starch uses:", "iodine solution", ["Benedict's solution", "biuret solution", "Sudan III"], "Iodine turns blue-black with starch."),
        ("Nutrition", "Benedict's solution is used to test for:", "reducing sugars", ["starch", "protein", "fats"], "Benedict's solution turns brick-red with reducing sugars on heating."),
        ("Transport", "The tissue that transports water in plants is the:", "xylem", ["phloem", "cambium", "epidermis"], "Xylem carries water and mineral salts upward."),
        ("Transport", "The tissue that transports food in plants is the:", "phloem", ["xylem", "cambium", "epidermis"], "Phloem carries manufactured food around the plant."),
        ("Transport", "Red blood cells carry:", "oxygen", ["carbon dioxide only", "nutrients only", "hormones only"], "Haemoglobin in red blood cells binds oxygen."),
        ("Transport", "White blood cells defend the body against:", "disease-causing organisms", ["oxygen loss", "blood loss", "dehydration"], "White blood cells fight infection."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- ACCOUNTING ----------------
def accounting_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Accounting", t, q, c, d, e))
    for sales, cogs in [(10000,6000),(20000,12000),(15000,9000),(50000,30000),(8000,5000),(12000,7000)]:
        gp = sales-cogs
        add("Final Accounts", f"A trader had sales of \u20a6{sales:,} and cost of goods sold of \u20a6{cogs:,}. Find the gross profit.", f"\u20a6{gp:,}",
            [f"\u20a6{gp+1000:,}", f"\u20a6{sales+cogs:,}", f"\u20a6{gp-1000:,}"], f"Gross profit = sales - cost of goods sold = {gp}.")
    for cost, rate, yrs in [(10000,10,2),(20000,5,3),(50000,10,1),(12000,20,2),(8000,25,2),(40000,5,4)]:
        dep = cost*rate*yrs//100
        add("Depreciation", f"A machine costing \u20a6{cost:,} is depreciated at {rate}% per annum on a straight-line basis. Find the total depreciation after {yrs} year(s).", f"\u20a6{dep:,}",
            [f"\u20a6{dep+500:,}", f"\u20a6{dep*2:,}", f"\u20a6{dep+1000:,}"], f"Annual depreciation = {cost} x {rate}% = {cost*rate//100}; over {yrs} year(s) = {dep}.")
    for amt, rate in [(1000,5),(2000,10),(5000,2),(4000,5),(10000,10),(3000,5)]:
        disc = amt*rate//100
        add("Cash Book", f"A cash discount of {rate}% is allowed on \u20a6{amt:,}. Find the discount.", f"\u20a6{disc:,}",
            [f"\u20a6{disc+50:,}", f"\u20a6{amt-disc:,}", f"\u20a6{disc+100:,}"], f"Discount = {rate}% of {amt} = {disc}.")
    for op, cl in [(5000,7000),(10000,12000),(2000,5000),(15000,18000)]:
        add("Final Accounts", f"Opening stock was \u20a6{op:,} and closing stock was \u20a6{cl:,}. If purchases were \u20a6{20000:,}, find the cost of goods sold.", f"\u20a6{op+20000-cl:,}",
            [f"\u20a6{op+20000:,}", f"\u20a6{cl:,}", f"\u20a6{op+20000+cl:,}"], f"COGS = opening stock + purchases - closing stock = {op+20000-cl}.")
    facts = [
        ("Nature of Accounting", "The accounting equation is:", "Assets = Capital + Liabilities", ["Assets = Capital - Liabilities", "Capital = Assets + Liabilities", "Liabilities = Assets + Capital"], "A = C + L is the fundamental accounting equation."),
        ("Double Entry", "The rule of double entry for a real account is:", "Debit the receiver, credit the giver", ["Debit the giver, credit the receiver", "Debit all accounts", "Credit all accounts"], "In double entry, every debit has an equal credit."),
        ("Double Entry", "An account that records assets is called a:", "real account", ["personal account", "nominal account", "impersonal account"], "Real accounts record assets."),
        ("Double Entry", "An account that records persons is called a:", "personal account", ["real account", "nominal account", "valuation account"], "Personal accounts record debtors and creditors."),
        ("Double Entry", "Expenses and incomes are recorded in:", "nominal accounts", ["real accounts", "personal accounts", "control accounts"], "Nominal accounts record expenses, losses, incomes and gains."),
        ("Trial Balance", "The trial balance is prepared to check the:", "arithmetical accuracy of the ledger", ["profit of the business", "cash position", "value of stock"], "It tests whether total debits equal total credits."),
        ("Trial Balance", "If total debits exceed total credits in a trial balance, the difference is:", "an error", ["profit", "a loss", "capital"], "Debits must equal credits; a difference means an error exists."),
        ("Final Accounts", "The trading account is prepared to find the:", "gross profit", ["net profit", "capital", "total assets"], "Gross profit = sales - cost of goods sold."),
        ("Final Accounts", "The profit and loss account shows the:", "net profit or net loss", ["gross profit", "total assets", "cash balance"], "It deducts expenses from gross profit."),
        ("Final Accounts", "The balance sheet shows the:", "financial position of a business at a date", ["profit over a period", "cash flow over a period", "sales over a period"], "The balance sheet lists assets, liabilities and capital at a point in time."),
        ("Cash Book", "The imprest system is used for:", "petty cash", ["bank overdraft", "sales ledger", "fixed assets"], "Petty cash is kept on an imprest (fixed float) system."),
        ("Bank Reconciliation", "A cheque not yet presented for payment is called an:", "unpresented cheque", ["uncredited cheque", "dishonoured cheque", "standing order"], "Unpresented cheques reduce the bank statement balance."),
        ("Bank Reconciliation", "A bank reconciliation statement is prepared to agree the:", "cash book balance with the bank statement balance", ["trial balance with the ledger", "sales ledger with the purchases ledger", "profit with the cash balance"], "It explains differences between the cash book and the bank statement."),
        ("Partnership Accounts", "In a partnership, the agreement between partners is called the:", "partnership deed", ["memorandum of association", "articles of association", "prospectus"], "The deed sets out capital, profit sharing and duties."),
        ("Company Accounts", "The capital of a company is divided into:", "shares", ["debentures", "bonds", "loans"], "Company capital is divided into shares owned by shareholders."),
        ("Company Accounts", "A dividend is:", "a share of company profit paid to shareholders", ["interest on a loan", "a tax on profit", "a director's salary"], "Dividends are paid out of profit to shareholders."),
        ("Stock Valuation", "The FIFO method of stock valuation assumes that:", "the oldest stock is issued first", ["the newest stock is issued first", "stock is valued at selling price", "stock is never valued"], "FIFO = First In, First Out."),
        ("Control Accounts", "A sales ledger control account is used to check the accuracy of the:", "debtors' ledger", ["creditors' ledger", "cash book", "fixed asset register"], "It summarises total debtors."),
        ("Errors", "An error of omission is:", "a transaction completely left out of the books", ["a transaction entered in the wrong account", "a transaction with the wrong amount", "a transaction entered twice"], "Omission means the entry was never made."),
        ("Errors", "An error of commission is:", "an entry made in the wrong personal account", ["an entry completely omitted", "an entry with figures transposed", "an entry made twice"], "Commission is posting to the wrong account of the same class."),
        ("Ethics", "One quality of a good accountant is:", "integrity", ["secrecy", "partiality", "negligence"], "Accountants must be honest and act with integrity."),
        ("Information Technology", "A computerised accounting system stores records:", "electronically", ["only on paper", "only in the cash book", "in the trial balance only"], "Computerised systems keep records in electronic form."),
        ("Final Accounts", "Drawings are:", "goods or cash taken by the owner for personal use", ["expenses of the business", "income of the business", "loans from the bank"], "Drawings reduce the owner's capital."),
        ("Final Accounts", "Capital is the:", "owner's claim on the assets of the business", ["total assets of the business", "total liabilities", "cash in the bank"], "Capital = assets - liabilities."),
        ("Final Accounts", "Accrued expenses are expenses:", "incurred but not yet paid", ["paid in advance", "paid in full", "never incurred"], "Accrued expenses are owed at the period end."),
        ("Final Accounts", "Prepaid expenses are expenses:", "paid in advance", ["incurred but not paid", "written off", "owed to creditors"], "Prepaid expenses are paid before they are used up."),
        ("Branch Accounts", "A branch account is prepared to show the:", "profit or loss of a branch", ["profit of the head office only", "total cash of the business", "capital of the branch only"], "Branch accounts measure each branch's performance."),
        ("Departmental Accounts", "Departmental accounts are prepared to find the profit of each:", "department", ["customer", "supplier", "employee"], "Each department's trading result is shown separately."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- ECONOMICS ----------------
def economics_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Economics", t, q, c, d, e))
    for p1,q1,p2,q2 in [(10,100,20,80),(5,200,10,150),(20,50,25,40),(8,120,12,90)]:
        ed = abs((q2-q1)/q1) / abs((p2-p1)/p1)
        add("Demand and Supply", f"When price rises from \u20a6{p1} to \u20a6{p2}, quantity demanded falls from {q1} to {q2} units. Find the price elasticity of demand.", fmt_num(ed),
            [fmt_num(ed+0.3), fmt_num(ed+1), fmt_num(ed+2)], f"Ed = % change in quantity / % change in price = {fmt_num(ed)}.")
    facts = [
        ("Economics as a Science", "Economics is the study of:", "how people use scarce resources to satisfy unlimited wants", ["how money is printed", "how banks make profit", "how governments collect tax"], "Scarcity and choice are the core of economics."),
        ("Economics as a Science", "The opportunity cost of a choice is:", "the next best alternative forgone", ["the money spent", "the total cost", "the profit made"], "Opportunity cost is what you give up."),
        ("Economics as a Science", "A scale of preference shows:", "the order in which wants are satisfied", ["the price of goods", "the income of consumers", "the cost of production"], "Wants are ranked by importance on a scale of preference."),
        ("Demand and Supply", "The law of demand states that, other things being equal:", "quantity demanded falls as price rises", ["quantity demanded rises as price rises", "demand is constant", "price falls as demand rises"], "Demand curves slope downward."),
        ("Demand and Supply", "The law of supply states that, other things being equal:", "quantity supplied rises as price rises", ["quantity supplied falls as price rises", "supply is constant", "price rises as supply rises"], "Supply curves slope upward."),
        ("Demand and Supply", "Equilibrium price is the price at which:", "quantity demanded equals quantity supplied", ["demand is zero", "supply is zero", "price is highest"], "At equilibrium the market clears."),
        ("Demand and Supply", "An increase in the price of a substitute good will:", "increase the demand for the good", ["decrease the demand for the good", "not affect demand", "decrease the supply of the good"], "Consumers switch to the relatively cheaper good."),
        ("Demand and Supply", "An increase in consumers' income will increase the demand for a:", "normal good", ["inferior good", "Giffen good", "free good"], "Demand for normal goods rises with income."),
        ("Production", "The factors of production are:", "land, labour, capital and entrepreneur", ["land, labour, money and time", "land, capital, profit and rent", "labour, wages, interest and profit"], "The four factors are land, labour, capital and entrepreneurship."),
        ("Production", "The reward for land is:", "rent", ["wages", "interest", "profit"], "Land earns rent."),
        ("Production", "The reward for labour is:", "wages", ["rent", "interest", "profit"], "Labour earns wages or salaries."),
        ("Production", "The reward for capital is:", "interest", ["rent", "wages", "profit"], "Capital earns interest."),
        ("Production", "The reward for entrepreneurship is:", "profit", ["rent", "wages", "interest"], "The entrepreneur bears risk and earns profit."),
        ("Production", "Division of labour leads to:", "increased output and specialisation", ["lower output", "higher cost per unit", "less skill"], "Specialisation raises productivity."),
        ("Market Structures", "A market with many sellers of identical products is:", "perfect competition", ["monopoly", "oligopoly", "monopolistic competition"], "Perfect competition has many sellers and homogeneous products."),
        ("Market Structures", "A market with only one seller is a:", "monopoly", ["duopoly", "oligopoly", "monopsony"], "A monopoly has a single seller."),
        ("Market Structures", "A market with a few large sellers is an:", "oligopoly", ["monopoly", "perfect competition", "monopsony"], "Oligopoly has few dominant firms."),
        ("National Income", "Gross Domestic Product (GDP) measures:", "the total value of goods and services produced within a country in a year", ["the total income of citizens abroad", "the total exports of a country", "the total money in circulation"], "GDP is production within the country's borders."),
        ("National Income", "National income can be measured by the:", "output, income and expenditure methods", ["demand method only", "supply method only", "price method only"], "The three approaches should give the same total."),
        ("Money and Banking", "The main function of money is as a:", "medium of exchange", ["store of value only", "measure of inflation", "source of profit"], "Money is first a medium of exchange."),
        ("Money and Banking", "The central bank of Nigeria is the:", "Central Bank of Nigeria", ["First Bank of Nigeria", "Bank of Industry", "Nigerian Deposit Insurance Corporation"], "The CBN is Nigeria's central bank."),
        ("Money and Banking", "A commercial bank accepts deposits and:", "lends money to customers", ["prints currency", "sets monetary policy", "collects taxes"], "Commercial banks take deposits and make loans."),
        ("Money and Banking", "Inflation is a:", "general and sustained rise in prices", ["fall in prices", "rise in one price", "fall in money supply"], "Inflation is a persistent rise in the general price level."),
        ("Money and Banking", "Deflation is a:", "general fall in prices", ["rise in prices", "rise in money supply", "fall in output only"], "Deflation is a sustained fall in the general price level."),
        ("International Trade", "The difference between a country's exports and imports is its:", "balance of trade", ["balance of payments", "national debt", "foreign reserves"], "Balance of trade = exports - imports of goods."),
        ("International Trade", "A country gains from trade by:", "specialising in goods it produces at lower cost", ["producing everything itself", "banning imports", "fixing all prices"], "Comparative advantage is the basis of trade."),
        ("International Trade", "A tariff is a:", "tax on imported goods", ["subsidy on exports", "ban on imports", "quota on exports"], "Tariffs raise the price of imports."),
        ("Public Finance", "Government revenue from taxes is used to:", "provide public goods and services", ["pay dividends", "make private profit", "buy shares only"], "Taxes fund roads, schools, hospitals and defence."),
        ("Public Finance", "A budget deficit occurs when government expenditure exceeds:", "government revenue", ["exports", "imports", "savings"], "Deficit = spending greater than revenue."),
        ("Economic Systems", "In a free-market economy, resources are allocated mainly by the:", "price mechanism", ["government plan", "traditional custom", "central committee"], "Prices guide buyers and sellers in a market economy."),
        ("Economic Systems", "In a centrally planned economy, resources are allocated by the:", "government", ["price mechanism", "market forces", "consumers only"], "The state plans production and distribution."),
        ("Economic Development", "One characteristic of a developing economy is:", "low per-capita income", ["high per-capita income", "full industrialisation", "low population growth"], "Developing economies typically have low income per head."),
        ("Business Organisations", "A sole proprietorship is owned by:", "one person", ["two or more partners", "shareholders", "the government"], "One person owns and controls it."),
        ("Business Organisations", "The liability of shareholders in a limited company is limited to their:", "share capital", ["personal property", "total debts", "salary"], "Shareholders lose only what they invested."),
        ("Tools of Analysis", "The mean of 10, 20 and 30 is:", "20", ["15", "25", "30"], "Mean = (10+20+30)/3 = 20."),
        ("Tools of Analysis", "The range of 5, 12, 8, 20, 3 is:", "17", ["20", "15", "12"], "Range = highest - lowest = 20 - 3 = 17."),
        ("Tools of Analysis", "The median of 4, 8, 6, 10, 2 is:", "6", ["4", "8", "10"], "Ordered: 2, 4, 6, 8, 10; middle is 6."),
        ("Tools of Analysis", "The mode of 1, 2, 2, 3, 4, 2, 5 is:", "2", ["1", "3", "5"], "2 occurs three times, more than any other value."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- COMMERCE ----------------
def commerce_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Commerce", t, q, c, d, e))
    for price, rate in [(2000,10),(5000,5),(10000,20),(4000,25),(8000,10),(3000,15)]:
        disc = price*rate//100
        add("Finance", f"A trader gives a {rate}% trade discount on goods priced at \u20a6{price:,}. Find the discount.", f"\u20a6{disc:,}",
            [f"\u20a6{disc+100:,}", f"\u20a6{price-disc:,}", f"\u20a6{disc*2:,}"], f"Discount = {rate}% of {price} = {disc}.")
    for amt, rate in [(10000,10),(20000,5),(5000,20),(15000,10)]:
        comm = amt*rate//100
        add("Finance", f"A salesman earns {rate}% commission on sales of \u20a6{amt:,}. Find his commission.", f"\u20a6{comm:,}",
            [f"\u20a6{comm+200:,}", f"\u20a6{amt-comm:,}", f"\u20a6{comm*2:,}"], f"Commission = {rate}% of {amt} = {comm}.")
    facts = [
        ("Commerce", "Commerce is concerned with:", "the distribution of goods and services", ["the production of goods only", "the consumption of goods only", "the storage of goods only"], "Commerce covers trade and aids to trade that move goods from producers to consumers."),
        ("Commerce", "Trade is the:", "buying and selling of goods", ["production of goods", "storage of goods", "transport of goods"], "Trade is exchange by buying and selling."),
        ("Commerce", "Home trade is trade carried on:", "within a country", ["between countries", "between continents", "online only"], "Home (internal) trade takes place inside one country."),
        ("Commerce", "Foreign trade is trade between:", "two or more countries", ["two towns", "two states", "two villages"], "Foreign (international) trade crosses national borders."),
        ("Occupation", "An occupation in which goods are produced is:", "industrial occupation", ["commercial occupation", "service occupation", "direct service"], "Industrial occupations extract or manufacture goods."),
        ("Production", "The primary stage of production includes:", "farming and mining", ["manufacturing", "retailing", "banking"], "Primary production extracts raw materials from nature."),
        ("Production", "The secondary stage of production is:", "manufacturing", ["farming", "retailing", "transport"], "Secondary production turns raw materials into finished goods."),
        ("Production", "The tertiary stage of production covers:", "services such as transport and banking", ["farming", "mining", "manufacturing"], "Tertiary production provides services."),
        ("Business Organisations", "A sole trader's business is owned by:", "one person", ["the government", "shareholders", "partners"], "A sole trader owns the business alone."),
        ("Business Organisations", "A partnership has a minimum of:", "two partners", ["one partner", "seven partners", "twenty partners"], "A partnership needs at least two people."),
        ("Business Organisations", "A public limited company can offer its shares to the:", "general public", ["directors only", "employees only", "government only"], "Plc shares are offered to the public."),
        ("Business Organisations", "A cooperative society is formed mainly to:", "serve the common interest of its members", ["make profit for shareholders", "avoid tax", "employ civil servants"], "Cooperatives exist for members' mutual benefit."),
        ("Trade", "A wholesaler buys goods in bulk from the manufacturer and sells to the:", "retailer", ["final consumer only", "producer", "government"], "The wholesaler links manufacturer and retailer."),
        ("Trade", "A retailer sells goods directly to the:", "final consumer", ["wholesaler", "manufacturer", "importer"], "Retailers are the last link to the consumer."),
        ("Trade", "A document used to request goods from a supplier is a:", "purchase order", ["invoice", "receipt", "credit note"], "The buyer sends an order stating what is wanted."),
        ("Trade", "An invoice is sent by the:", "seller to the buyer", ["buyer to the seller", "bank to the buyer", "government to the seller"], "The invoice states the goods supplied and the amount due."),
        ("Trade", "A receipt is evidence of:", "payment made", ["goods ordered", "goods returned", "credit given"], "A receipt acknowledges money received."),
        ("Trade", "A credit note is issued when goods are:", "returned by the buyer", ["ordered by the buyer", "paid for in cash", "delivered correctly"], "It reduces the amount the buyer owes."),
        ("Aids to Trade", "Transport is an aid to trade because it:", "moves goods from producers to consumers", ["stores goods", "advertises goods", "insures goods"], "Transport overcomes the barrier of distance."),
        ("Aids to Trade", "Warehousing helps trade by:", "storing goods until they are needed", ["moving goods", "advertising goods", "paying for goods"], "Warehouses store goods and protect them."),
        ("Aids to Trade", "Insurance is an aid to trade because it:", "covers the risk of loss or damage", ["moves goods", "stores goods", "sells goods"], "Insurance compensates for loss in transit or storage."),
        ("Aids to Trade", "Advertising helps trade by:", "informing and persuading consumers", ["transporting goods", "storing goods", "insuring goods"], "Advertising creates awareness and demand."),
        ("Aids to Trade", "Banking aids trade by:", "providing money transfer and credit facilities", ["moving goods", "storing goods", "advertising goods"], "Banks handle payments and lend to traders."),
        ("Aids to Trade", "Communication aids trade by:", "passing information between buyers and sellers", ["storing goods", "moving goods", "insuring goods"], "Phones, email and post speed up business dealings."),
        ("Finance", "The money used to start a business is called:", "capital", ["profit", "revenue", "turnover"], "Capital is the money invested in the business."),
        ("Finance", "A bank overdraft is:", "permission to withdraw more than the account balance", ["a long-term loan", "a savings account", "a fixed deposit"], "An overdraft is short-term borrowing from the bank."),
        ("Finance", "A cheque is an instruction to a bank to:", "pay a stated sum to a named person", ["lend money", "open an account", "close an account"], "A cheque orders the bank to pay."),
        ("Finance", "The Central Bank of Nigeria is the:", "bankers' bank", ["commercial bank", "merchant bank", "development bank"], "The CBN is the bank of banks and the government."),
        ("Marketing", "The four elements of the marketing mix are product, price, place and:", "promotion", ["people", "profit", "packaging"], "The 4 Ps are product, price, place and promotion."),
        ("Marketing", "Market segmentation means dividing a market into:", "groups of similar buyers", ["countries", "shops", "products only"], "Segments are groups with similar needs."),
        ("Consumer Protection", "A consumer's right to safety means goods sold should be:", "safe for use", ["cheap", "imported", "advertised"], "Consumers have the right to safe products."),
        ("Consumer Protection", "In Nigeria, the agency that protects consumers is the:", "Federal Competition and Consumer Protection Commission (FCCPC)", ["Central Bank of Nigeria", "Nigerian Stock Exchange", "Corporate Affairs Commission"], "The FCCPC protects consumer rights."),
        ("International Trade", "Exports are goods:", "sold to other countries", ["bought from other countries", "produced for home use", "stored in warehouses"], "Exports leave the country; imports enter it."),
        ("International Trade", "A country that sells more than it buys has a:", "favourable balance of trade", ["unfavourable balance of trade", "budget deficit", "trade deficit"], "Exports greater than imports is favourable."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- COMPUTER ----------------
def computer_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Computer", t, q, c, d, e))
    for n in [5,9,13,17,21,25,29,33,42,50]:
        b = bin(n)[2:]
        add("Number Systems", f"Convert {n} to binary.", b,
            [bin(n+2)[2:], bin(n+1)[2:], bin(n-1)[2:]], f"{n} in binary is {b}.")
    for b in ["101","110","1010","1111","1001","1100","10101","1110"]:
        v = int(b, 2)
        add("Number Systems", f"Convert binary {b} to decimal.", str(v),
            [str(v+1), str(v-1), str(v*2)], f"Binary {b} = {v} in decimal.")
    for n in [10,15,16,255,26,31]:
        add("Number Systems", f"Convert {n} to hexadecimal.", hex(n)[2:].upper(),
            [hex(n+1)[2:].upper(), hex(n-1)[2:].upper(), str(n)], f"{n} in hexadecimal is {hex(n)[2:].upper()}.")
    facts = [
        ("Evolution of Computing", "The first electronic computer was the:", "ENIAC", ["UNIVAC", "EDVAC", "IBM PC"], "ENIAC (1946) was the first general-purpose electronic computer."),
        ("Evolution of Computing", "Charles Babbage is known as the father of the:", "computer", ["internet", "telephone", "television"], "Babbage designed the Analytical Engine."),
        ("Evolution of Computing", "The Analytical Engine was designed by:", "Charles Babbage", ["Alan Turing", "John von Neumann", "Bill Gates"], "Babbage's Analytical Engine was the first programmable computer design."),
        ("Fundamentals", "The two main parts of a computer system are:", "hardware and software", ["input and output", "CPU and monitor", "data and information"], "Hardware is the physical parts; software is the programs."),
        ("Fundamentals", "Data that has been processed into a useful form is called:", "information", ["data", "knowledge", "input"], "Information is processed data."),
        ("Fundamentals", "The smallest unit of data in a computer is the:", "bit", ["byte", "kilobyte", "megabyte"], "A bit is a single 0 or 1."),
        ("Fundamentals", "One byte is made up of:", "8 bits", ["4 bits", "16 bits", "2 bits"], "1 byte = 8 bits."),
        ("Fundamentals", "1024 bytes make:", "1 kilobyte", ["1 megabyte", "1 gigabyte", "1 terabyte"], "1024 bytes = 1 KB."),
        ("Hardware", "The CPU is also called the:", "brain of the computer", ["heart of the computer", "memory of the computer", "eye of the computer"], "The CPU controls and processes everything."),
        ("Hardware", "CPU stands for:", "Central Processing Unit", ["Central Program Unit", "Computer Processing Unit", "Central Power Unit"], "CPU = Central Processing Unit."),
        ("Hardware", "The part of the CPU that carries out calculations is the:", "Arithmetic and Logic Unit (ALU)", ["Control Unit", "Memory Unit", "Input Unit"], "The ALU does arithmetic and logic operations."),
        ("Hardware", "The part of the CPU that directs operations is the:", "Control Unit", ["Arithmetic and Logic Unit", "Memory Unit", "Output Unit"], "The Control Unit fetches and decodes instructions."),
        ("Hardware", "Which of these is an input device?", "keyboard", ["monitor", "printer", "speaker"], "The keyboard enters data into the computer."),
        ("Hardware", "Which of these is an output device?", "monitor", ["keyboard", "mouse", "scanner"], "The monitor displays results."),
        ("Hardware", "Which of these is a storage device?", "hard disk", ["keyboard", "monitor", "printer"], "The hard disk stores data permanently."),
        ("Hardware", "RAM stands for:", "Random Access Memory", ["Read And Modify", "Rapid Access Memory", "Read Access Memory"], "RAM is the temporary working memory."),
        ("Hardware", "ROM stands for:", "Read Only Memory", ["Random Only Memory", "Read On Memory", "Rapid Only Memory"], "ROM holds permanent start-up instructions."),
        ("Hardware", "The main memory that loses its contents when power is off is:", "RAM", ["ROM", "hard disk", "flash drive"], "RAM is volatile memory."),
        ("Software", "The software that manages the computer hardware is the:", "operating system", ["application software", "utility software", "word processor"], "The OS controls hardware and runs programs."),
        ("Software", "Which of these is an operating system?", "Windows", ["Microsoft Word", "Excel", "PowerPoint"], "Windows is an operating system; the others are applications."),
        ("Software", "Microsoft Word is an example of:", "application software", ["system software", "operating system", "utility software"], "Word is an application for word processing."),
        ("Software", "A program designed to harm a computer is called:", "malware", ["freeware", "shareware", "firmware"], "Malware includes viruses, worms and trojans."),
        ("Software", "Antivirus software is used to:", "detect and remove malware", ["increase speed", "store data", "print documents"], "Antivirus protects against malicious programs."),
        ("Number Systems", "The binary number system uses base:", "2", ["8", "10", "16"], "Binary uses digits 0 and 1, base 2."),
        ("Number Systems", "The hexadecimal system uses base:", "16", ["2", "8", "10"], "Hexadecimal is base 16."),
        ("Data Processing", "The stages of data processing are input, processing, storage and:", "output", ["input", "deletion", "formatting"], "IPO cycle: input, process, output (with storage)."),
        ("ICT", "ICT stands for:", "Information and Communication Technology", ["Information and Computer Technology", "Internet and Communication Technology", "Information and Control Technology"], "ICT = Information and Communication Technology."),
        ("ICT", "The internet is a:", "global network of computers", ["single computer", "type of software", "storage device"], "The internet links computers worldwide."),
        ("ICT", "A web browser is used to:", "access websites", ["write programs", "store files", "print documents"], "Browsers display web pages."),
        ("ICT", "An email address must contain the symbol:", "@", ["#", "$", "%"], "The @ separates the user name from the domain."),
        ("Files", "A file extension that indicates a Word document is:", ".docx", [".xlsx", ".pptx", ".mp3"], ".docx is the Word document extension."),
        ("Files", "A folder is used to:", "organise files", ["delete files only", "print files", "scan files"], "Folders group related files together."),
        ("Ethics", "Using another person's work without permission is:", "plagiarism", ["copyright", "licensing", "encryption"], "Plagiarism is presenting others' work as your own."),
        ("Ethics", "A password should be kept:", "secret", ["shared with friends", "written on the monitor", "easy to guess"], "Passwords protect accounts and must stay secret."),
        ("Problem Solving", "A step-by-step procedure for solving a problem is called an:", "algorithm", ["flowchart", "program", "variable"], "An algorithm lists the steps in order."),
        ("Problem Solving", "A diagram that shows the steps of an algorithm is a:", "flowchart", ["algorithm", "pseudocode", "variable"], "Flowcharts use symbols to show process steps."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- AGRIC ----------------
def agric_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Agric", t, q, c, d, e))
    crops = [("maize", "cereal"), ("yam", "root/tuber"), ("cassava", "root/tuber"), ("rice", "cereal"),
             ("groundnut", "legume"), ("cowpea", "legume"), ("cotton", "fibre crop"), ("cocoa", "beverage/tree crop"),
             ("oil palm", "oil crop"), ("sorghum", "cereal"), ("millet", "cereal"), ("plantain", "fruit crop")]
    for crop, group in crops:
        others = list(dict.fromkeys(g for c, g in crops if g != group))[:3]
        add("Agronomy", f"{crop.capitalize()} is an example of a {group.split('/')[0]} crop. Which group does {crop} belong to?", group,
            others, f"{crop.capitalize()} is classified as a {group}.")
    facts = [
        ("General Agriculture", "Agriculture is the art and science of:", "cultivating crops and rearing animals", ["mining minerals", "manufacturing goods", "fishing only"], "Agriculture covers crop and animal production."),
        ("General Agriculture", "One importance of agriculture is that it provides:", "food for the population", ["cars for transport", "houses for shelter", "clothes for export only"], "Agriculture feeds the nation."),
        ("General Agriculture", "A farm manager is responsible for:", "planning and supervising farm operations", ["selling farm land", "buying tractors only", "counting animals only"], "The manager plans, organises and controls the farm."),
        ("Agronomy", "The best soil for most crops is:", "loamy soil", ["sandy soil", "clay soil", "gravelly soil"], "Loam holds water and nutrients well and drains adequately."),
        ("Agronomy", "Which soil type holds the most water?", "clay soil", ["sandy soil", "loamy soil", "gravelly soil"], "Clay has tiny particles and holds water strongly."),
        ("Agronomy", "Which soil type drains fastest?", "sandy soil", ["clay soil", "loamy soil", "silty soil"], "Sand has large particles and large air spaces, so water drains quickly."),
        ("Agronomy", "Humus in the soil improves its:", "fertility and water-holding capacity", ["acidity", "temperature", "colour only"], "Humus adds nutrients and improves soil structure."),
        ("Agronomy", "The process of breaking up soil before planting is:", "tillage", ["irrigation", "mulching", "pruning"], "Tillage loosens the soil for planting."),
        ("Agronomy", "Irrigation is the:", "artificial application of water to crops", ["removal of weeds", "application of fertiliser", "harvesting of crops"], "Irrigation supplies water when rainfall is inadequate."),
        ("Agronomy", "Mulching is the covering of soil with:", "plant materials to conserve moisture", ["fertiliser", "pesticides", "stones only"], "Mulch reduces evaporation and weed growth."),
        ("Agronomy", "Crop rotation is the practice of growing:", "different crops on the same land in sequence", ["the same crop every year", "crops and animals together", "only one crop"], "Rotation maintains soil fertility and breaks pest cycles."),
        ("Agronomy", "A leguminous crop enriches the soil with:", "nitrogen", ["phosphorus", "potassium", "calcium"], "Legumes fix atmospheric nitrogen through root nodules."),
        ("Agronomy", "NPK fertiliser supplies:", "nitrogen, phosphorus and potassium", ["nitrogen only", "calcium, magnesium and sulphur", "iron, zinc and boron"], "NPK stands for nitrogen, phosphorus and potassium."),
        ("Agronomy", "The practice of growing two or more crops on the same land at the same time is:", "mixed cropping", ["mono-cropping", "crop rotation", "shifting cultivation"], "Mixed cropping grows several crops together."),
        ("Agronomy", "Weeds are harmful to crops because they:", "compete for water, nutrients and light", ["add nutrients to the soil", "attract pollinators", "improve soil structure"], "Weeds compete with crops and reduce yield."),
        ("Animal Production", "The young of a cow is called a:", "calf", ["lamb", "kid", "piglet"], "A young cow is a calf."),
        ("Animal Production", "The young of a sheep is called a:", "lamb", ["calf", "kid", "chick"], "A young sheep is a lamb."),
        ("Animal Production", "The young of a goat is called a:", "kid", ["calf", "lamb", "piglet"], "A young goat is a kid."),
        ("Animal Production", "The young of a pig is called a:", "piglet", ["calf", "lamb", "kid"], "A young pig is a piglet."),
        ("Animal Production", "The young of a hen is called a:", "chick", ["duckling", "gosling", "poult"], "A young hen is a chick."),
        ("Animal Production", "Poultry kept for egg production are called:", "layers", ["broilers", "cockerels", "capons"], "Layers produce eggs; broilers are raised for meat."),
        ("Animal Production", "Poultry kept for meat production are called:", "broilers", ["layers", "pullets", "cockerels"], "Broilers grow fast for meat."),
        ("Animal Production", "The process of giving birth in cattle is called:", "calving", ["lambing", "kidding", "farrowing"], "Calving is birth in cattle."),
        ("Animal Production", "The process of giving birth in pigs is called:", "farrowing", ["calving", "lambing", "kidding"], "Farrowing is birth in pigs."),
        ("Animal Production", "The process of giving birth in sheep is called:", "lambing", ["calving", "farrowing", "kidding"], "Lambing is birth in sheep."),
        ("Animal Production", "The gestation period of a cow is about:", "283 days", ["114 days", "150 days", "365 days"], "A cow carries its calf for about 9 months (283 days)."),
        ("Animal Production", "The gestation period of a sow is about:", "114 days", ["283 days", "150 days", "60 days"], "A sow's gestation is about 3 months, 3 weeks and 3 days (114 days)."),
        ("Animal Production", "Ruminant animals have:", "a four-chambered stomach", ["a single stomach", "no stomach", "a beak"], "Cattle, sheep and goats are ruminants."),
        ("Animal Production", "Which of these is a ruminant?", "cow", ["pig", "dog", "horse"], "Cattle chew the cud; pigs, dogs and horses are not ruminants in the strict sense used here."),
        ("Animal Production", "The disease Newcastle disease affects:", "poultry", ["cattle", "sheep", "goats"], "Newcastle disease is a viral disease of birds."),
        ("Animal Production", "Foot-and-mouth disease affects:", "cattle", ["poultry", "fish", "bees"], "Foot-and-mouth disease affects cloven-hoofed animals such as cattle."),
        ("Animal Production", "Trypanosomiasis in cattle is transmitted by the:", "tsetse fly", ["housefly", "mosquito", "tick"], "The tsetse fly spreads trypanosomiasis (sleeping sickness in animals)."),
        ("Agricultural Economics", "The law of diminishing returns states that as more of a variable input is added:", "output increases at a decreasing rate", ["output increases at an increasing rate", "output stays constant", "output falls immediately"], "After a point, extra input adds less and less output."),
        ("Agricultural Economics", "Land, labour, capital and management are the:", "factors of production in agriculture", ["types of crops", "types of animals", "forms of credit"], "These are the resources used in farming."),
        ("Agricultural Economics", "Agricultural extension teaches farmers:", "improved farming practices", ["how to sell land", "how to avoid tax", "how to build houses"], "Extension passes research findings to farmers."),
        ("Agricultural Technology", "A tractor is used mainly for:", "tillage and haulage", ["planting seeds by hand", "watering crops", "storing grain"], "Tractors pull ploughs and trailers."),
        ("Agricultural Technology", "The implement used to turn over soil is the:", "plough", ["harrow", "planter", "sprayer"], "The plough inverts the soil."),
        ("Agricultural Technology", "The implement used to break soil clods after ploughing is the:", "harrow", ["plough", "ridger", "planter"], "Harrowing breaks clods and levels the soil."),
        ("Agricultural Technology", "A knapsack sprayer is used to apply:", "pesticides", ["fertiliser", "water for irrigation", "seeds"], "Sprayers apply chemicals to crops."),
        ("Forestry", "Afforestation is the:", "planting of trees where there were none", ["cutting down of trees", "burning of forests", "clearing of land"], "Afforestation creates new forest."),
        ("Forestry", "Deforestation leads to:", "soil erosion and loss of wildlife habitat", ["increased rainfall", "better soil", "more timber forever"], "Removing trees exposes soil and destroys habitats."),
        ("Fisheries", "Fish farming is also called:", "aquaculture", ["apiculture", "sericulture", "horticulture"], "Aquaculture is the farming of fish and other aquatic animals."),
        ("Fisheries", "The rearing of bees is called:", "apiculture", ["aquaculture", "sericulture", "horticulture"], "Apiculture is beekeeping."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- GEOGRAPHY ----------------
def geography_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Geography", t, q, c, d, e))
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
        others = [c for co, c in capitals if c != cap][:3]
        add("Regional Geography", f"What is the capital of {country}?", cap, others,
            f"The capital of {country} is {cap}.")
    for scale, cm in [(50000,2),(100000,3),(25000,4),(50000,4)]:
        ground = scale*cm//100000
        add("Map Work", f"On a map of scale 1:{scale:,}, a distance of {cm} cm represents how many kilometres on the ground?", f"{ground} km",
            [f"{ground+1} km", f"{ground+2} km", f"{ground+3} km"],
            f"Ground distance = {cm} x {scale:,} cm = {scale*cm//100000} km.")
    facts = [
        ("Physical Geography", "The longest river in the world is the:", "Nile", ["Amazon", "Niger", "Congo"], "The Nile is about 6,650 km long."),
        ("Physical Geography", "The longest river in Nigeria is the:", "Niger", ["Benue", "Cross River", "Ogun"], "The River Niger is Nigeria's longest river."),
        ("Physical Geography", "The highest mountain in Africa is:", "Mount Kilimanjaro", ["Mount Kenya", "Mount Cameroon", "Mount Everest"], "Kilimanjaro (5,895 m) is Africa's highest peak."),
        ("Physical Geography", "The largest desert in the world is the:", "Sahara", ["Kalahari", "Gobi", "Arabian"], "The Sahara is the world's largest hot desert."),
        ("Physical Geography", "The instrument used to measure rainfall is the:", "rain gauge", ["barometer", "thermometer", "anemometer"], "A rain gauge collects and measures rainfall."),
        ("Physical Geography", "The instrument used to measure wind speed is the:", "anemometer", ["barometer", "rain gauge", "hygrometer"], "An anemometer measures wind speed."),
        ("Physical Geography", "The instrument used to measure atmospheric pressure is the:", "barometer", ["anemometer", "rain gauge", "thermometer"], "A barometer measures air pressure."),
        ("Physical Geography", "The instrument used to measure humidity is the:", "hygrometer", ["barometer", "anemometer", "rain gauge"], "A hygrometer measures air humidity."),
        ("Physical Geography", "The lines joining places of equal temperature on a map are:", "isotherms", ["isobars", "isohyets", "contours"], "Isotherms join places of equal temperature."),
        ("Physical Geography", "The lines joining places of equal rainfall are:", "isohyets", ["isotherms", "isobars", "contours"], "Isohyets join places of equal rainfall."),
        ("Physical Geography", "The lines joining places of equal pressure are:", "isobars", ["isotherms", "isohyets", "contours"], "Isobars join places of equal pressure."),
        ("Physical Geography", "Lines joining places of equal height are called:", "contours", ["isobars", "isotherms", "isohyets"], "Contours show height above sea level."),
        ("Physical Geography", "The equator is at latitude:", "0\u00b0", ["90\u00b0N", "23.5\u00b0N", "66.5\u00b0S"], "The equator is 0\u00b0 latitude."),
        ("Physical Geography", "The Tropic of Cancer is at latitude:", "23.5\u00b0N", ["23.5\u00b0S", "66.5\u00b0N", "0\u00b0"], "The Tropic of Cancer lies at 23.5\u00b0 north."),
        ("Physical Geography", "The Tropic of Capricorn is at latitude:", "23.5\u00b0S", ["23.5\u00b0N", "66.5\u00b0S", "0\u00b0"], "The Tropic of Capricorn lies at 23.5\u00b0 south."),
        ("Physical Geography", "The Earth rotates on its axis once in:", "24 hours", ["12 hours", "365 days", "30 days"], "One rotation takes about 24 hours, giving day and night."),
        ("Physical Geography", "The Earth revolves around the Sun once in:", "365 days", ["24 hours", "30 days", "12 hours"], "One revolution takes about 365 days, giving the year."),
        ("Physical Geography", "The seasons are caused by the:", "tilt of the Earth's axis and its revolution", ["rotation of the Earth only", "distance from the Moon", "shape of the Earth"], "The 23.5\u00b0 tilt plus revolution produces seasons."),
        ("Map Work", "On a map, the north is usually indicated by:", "an arrow pointing up", ["a scale bar", "a legend", "a contour"], "The north arrow shows direction."),
        ("Map Work", "The ratio 1:50,000 on a map means 1 cm on the map represents:", "50,000 cm on the ground", ["50 cm on the ground", "500 cm on the ground", "5,000 cm on the ground"], "The representative fraction gives ground distance per map unit."),
        ("Human Geography", "The movement of people from rural to urban areas is called:", "rural-urban migration", ["urban-rural migration", "emigration", "immigration"], "Rural-urban migration moves people into towns."),
        ("Human Geography", "A settlement with a large population and many services is a:", "town or city", ["hamlet", "village", "farmstead"], "Towns and cities have large populations and varied functions."),
        ("Human Geography", "The most populous country in Africa is:", "Nigeria", ["Egypt", "Ethiopia", "South Africa"], "Nigeria has Africa's largest population."),
        ("Human Geography", "The main occupation in rural Nigeria is:", "farming", ["manufacturing", "banking", "mining"], "Most rural Nigerians farm."),
        ("Economic Geography", "The main export of Nigeria is:", "crude oil", ["cocoa", "groundnut", "timber"], "Crude oil dominates Nigeria's exports."),
        ("Economic Geography", "The headquarters of ECOWAS is in:", "Abuja, Nigeria", ["Accra, Ghana", "Lagos, Nigeria", "Abidjan, Cote d'Ivoire"], "ECOWAS headquarters is in Abuja."),
        ("Economic Geography", "The headquarters of the African Union is in:", "Addis Ababa, Ethiopia", ["Cairo, Egypt", "Nairobi, Kenya", "Pretoria, South Africa"], "The AU headquarters is in Addis Ababa."),
        ("Economic Geography", "The headquarters of the United Nations is in:", "New York, USA", ["Geneva, Switzerland", "London, UK", "Paris, France"], "The UN headquarters is in New York."),
        ("Environmental Geography", "The cutting down of trees on a large scale is called:", "deforestation", ["afforestation", "reforestation", "desertification"], "Deforestation removes forest cover."),
        ("Environmental Geography", "The gradual change of fertile land into desert is:", "desertification", ["deforestation", "erosion", "flooding"], "Desertification is land degradation in dry areas."),
        ("Environmental Geography", "Soil erosion is mainly caused by:", "running water and wind", ["planting trees", "terracing", "mulching"], "Water and wind remove topsoil."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- GOVERNMENT ----------------
def government_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Government", t, q, c, d, e))
    facts = [
        ("Basic Concepts", "Government as an institution refers to:", "the machinery through which the state is governed", ["the people of a country", "the political party in power", "the armed forces"], "Government is the institution that makes and enforces rules."),
        ("Basic Concepts", "Sovereignty means:", "supreme and independent power of the state", ["rule by the military", "rule by the people", "freedom of speech"], "A sovereign state answers to no higher authority."),
        ("Basic Concepts", "Legitimacy is:", "the acceptance of a government by the people", ["the use of force", "the wealth of a ruler", "the age of a constitution"], "A legitimate government is accepted as rightful."),
        ("Basic Concepts", "Authority is:", "the right to exercise power", ["the use of force", "the power of the military", "the wealth of a state"], "Authority is power recognised as legitimate."),
        ("Basic Concepts", "A state is made up of population, territory, government and:", "sovereignty", ["army", "wealth", "language"], "The four elements of a state are population, territory, government and sovereignty."),
        ("Forms of Government", "Democracy is government by:", "the people", ["one person", "a few rich people", "the military"], "Democracy means rule by the people."),
        ("Forms of Government", "A monarchy is rule by a:", "king or queen", ["president", "general", "prime minister"], "Monarchy is rule by a hereditary king or queen."),
        ("Forms of Government", "An oligarchy is rule by a:", "small group of people", ["single person", "whole population", "religious leader"], "Oligarchy is rule by a few."),
        ("Forms of Government", "An autocracy is rule by:", "one person with absolute power", ["the people", "a parliament", "a council of elders"], "Autocracy concentrates power in one ruler."),
        ("Arms of Government", "The three arms of government are the legislature, executive and:", "judiciary", ["police", "army", "civil service"], "The three arms are legislature, executive and judiciary."),
        ("Arms of Government", "The main function of the legislature is to:", "make laws", ["interpret laws", "enforce laws", "collect taxes"], "The legislature makes laws."),
        ("Arms of Government", "The main function of the judiciary is to:", "interpret laws", ["make laws", "enforce laws", "collect taxes"], "The judiciary interprets laws and settles disputes."),
        ("Arms of Government", "The main function of the executive is to:", "implement and enforce laws", ["make laws", "interpret laws", "amend the constitution"], "The executive carries out the laws."),
        ("Arms of Government", "The head of the executive in Nigeria is the:", "President", ["Senate President", "Chief Justice", "Speaker"], "The President heads the executive arm."),
        ("Arms of Government", "Nigeria's legislature is called the:", "National Assembly", ["Supreme Court", "Federal Executive Council", "National Council of State"], "The National Assembly is made up of the Senate and the House of Representatives."),
        ("Arms of Government", "The upper house of Nigeria's National Assembly is the:", "Senate", ["House of Representatives", "House of Assembly", "Supreme Court"], "The Senate is the upper chamber."),
        ("Arms of Government", "The lower house of Nigeria's National Assembly is the:", "House of Representatives", ["Senate", "Supreme Court", "House of Chiefs"], "The House of Representatives is the lower chamber."),
        ("Structures of Governance", "In a federal system, power is shared between the:", "central government and the component units", ["president and the governor", "army and the police", "rich and the poor"], "Federalism divides power between the centre and the states."),
        ("Structures of Governance", "In a unitary system, power is concentrated in the:", "central government", ["state governments", "local governments", "traditional rulers"], "Unitary government keeps power at the centre."),
        ("Systems of Governance", "In a presidential system, the president is:", "both head of state and head of government", ["head of state only", "head of government only", "ceremonial only"], "Nigeria's presidential system combines both roles in the President."),
        ("Systems of Governance", "In a parliamentary system, the head of government is the:", "prime minister", ["president", "king", "chief justice"], "The prime minister leads the government in a parliamentary system."),
        ("Constitution", "A constitution is:", "the fundamental law of a state", ["an ordinary law", "a military decree", "a party manifesto"], "The constitution is the supreme law."),
        ("Constitution", "Nigeria's current constitution is the:", "1999 Constitution", ["1979 Constitution", "1989 Constitution", "1963 Constitution"], "The 1999 Constitution (as amended) is in force."),
        ("Constitution", "The supremacy of the constitution means it is:", "above all other laws", ["below ordinary laws", "equal to decrees", "only advisory"], "Any law inconsistent with the constitution is void."),
        ("Democratic Principles", "Separation of powers means each arm of government:", "exercises only its own functions", ["controls the other arms", "shares all powers", "answers to the military"], "Powers are divided among legislature, executive and judiciary."),
        ("Democratic Principles", "Checks and balances ensure that:", "no arm of government abuses its power", ["the executive controls all", "the judiciary makes laws", "the legislature enforces laws"], "Each arm checks the others."),
        ("Democratic Principles", "The rule of law means:", "everyone, including leaders, is subject to the law", ["leaders are above the law", "laws apply only to the poor", "custom is above the law"], "Under the rule of law, no one is above the law."),
        ("Citizenship", "A person becomes a citizen of Nigeria by:", "birth, registration or naturalisation", ["birth only", "wealth only", "marriage only"], "The constitution provides these three ways."),
        ("Citizenship", "One duty of a citizen is to:", "pay taxes", ["avoid voting", "disobey laws", "evade tax"], "Citizens must obey laws and pay taxes."),
        ("Citizenship", "One right of a citizen is the right to:", "vote", ["steal", "break laws", "avoid tax"], "Voting is a political right of citizens."),
        ("Political Parties", "The main function of a political party is to:", "contest elections and form government", ["make laws", "interpret laws", "collect taxes"], "Parties seek power through elections."),
        ("Political Parties", "A one-party system has:", "only one political party", ["two parties", "many parties", "no parties"], "Only one party is allowed."),
        ("Political Parties", "A two-party system has:", "two major political parties", ["one party", "many equal parties", "no parties"], "Two parties dominate politics."),
        ("Nigerian Government", "Nigeria became independent on:", "1 October 1960", ["1 October 1963", "1 January 1960", "1 October 1979"], "Nigeria gained independence on 1 October 1960."),
        ("Nigerian Government", "Nigeria became a republic on:", "1 October 1963", ["1 October 1960", "1 October 1979", "29 May 1999"], "Nigeria became a republic on 1 October 1963."),
        ("Nigerian Government", "The first Prime Minister of Nigeria was:", "Sir Abubakar Tafawa Balewa", ["Dr Nnamdi Azikiwe", "Chief Obafemi Awolowo", "Sir Ahmadu Bello"], "Tafawa Balewa was Nigeria's first Prime Minister."),
        ("Nigerian Government", "The first President of Nigeria was:", "Dr Nnamdi Azikiwe", ["Sir Abubakar Tafawa Balewa", "General Yakubu Gowon", "Alhaji Shehu Shagari"], "Azikiwe became President when Nigeria became a republic in 1963."),
        ("Nigerian Government", "Nigeria returned to civilian rule in:", "1999", ["1979", "1983", "1993"], "The Fourth Republic began on 29 May 1999."),
        ("Nigerian Government", "The 1999 Constitution provides for:", "three tiers of government", ["two tiers of government", "four tiers of government", "one tier of government"], "Federal, state and local governments."),
        ("Nigerian Government", "The local government is the:", "third tier of government", ["first tier", "second tier", "fourth tier"], "Local government is the grassroots tier."),
        ("Foreign Policy", "Nigeria's foreign policy is guided by the promotion of:", "African unity and interests", ["European interests", "Asian interests", "American interests"], "Africa is the centrepiece of Nigeria's foreign policy."),
        ("Foreign Policy", "ECOWAS stands for:", "Economic Community of West African States", ["Economic Council of West African States", "Economic Community of West African Societies", "Economic Commission of West Africa"], "ECOWAS is the West African regional body."),
        ("Foreign Policy", "The AU stands for:", "African Union", ["Asian Union", "American Union", "Arab Union"], "The African Union succeeded the OAU in 2002."),
        ("Foreign Policy", "The UN was founded in:", "1945", ["1919", "1939", "1960"], "The United Nations was founded in 1945 after the Second World War."),
        ("Pre-colonial Polities", "The pre-colonial Yoruba political system was headed by the:", "Oba", ["Emir", "Obong", "Eze"], "The Oba headed Yoruba kingdoms such as Oyo."),
        ("Pre-colonial Polities", "The pre-colonial Hausa/Fulani political system was headed by the:", "Emir", ["Oba", "Eze", "Obong"], "Emirs headed the Hausa/Fulani emirates."),
        ("Pre-colonial Polities", "The pre-colonial Igbo political system was:", "largely republican and acephalous", ["highly centralised under a king", "ruled by an emir", "ruled by an oba"], "Igbo communities were governed by councils and age grades rather than a single king."),
        ("Pre-colonial Polities", "The Sokoto Jihad was led by:", "Usman dan Fodio", ["Ahmadu Bello", "Muhammed Bello", "Nana Asma'u"], "Usman dan Fodio led the jihad of 1804."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- HISTORY ----------------
def history_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "History", t, q, c, d, e))
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
              ("Mungo Park reached the River Niger", 1796), ("The Scramble for Africa began in earnest", 1884),
              ("Nigeria's first military coup", 1966), ("The June 12 election was annulled", 1993),
              ("Nigeria returned to civilian rule (Fourth Republic)", 1999),
              ("The Lagos colony was annexed by Britain", 1861),
              ("The British conquest of Benin", 1897), ("The Aba Women's Riot", 1929),
              ("The Egba United Government was formed", 1865), ("The Kano Chronicle was written", 1890),
              ("Usman dan Fodio founded the Sokoto Caliphate", 1804),
              ("The Yoruba civil wars ended with the Kiriji War", 1886),
              ("The first Nigerian newspaper, Iwe Irohin, was founded", 1859),
              ("The Richards Constitution was introduced", 1946),
              ("The Macpherson Constitution was introduced", 1951),
              ("The Lyttleton Constitution was introduced", 1954),
              ("The independence Constitution came into force", 1960),
              ("The first republican Constitution came into force", 1963),
              ("General Gowon was overthrown", 1975), ("General Murtala Mohammed was assassinated", 1976),
              ("The Second Republic began", 1979), ("The Second Republic was overthrown", 1983),
              ("The Berlin Wall fell", 1989), ("The slave trade was abolished in the USA", 1865)]
    for name, yr in events:
        others = list(dict.fromkeys([str(y) for n, y in events if y != yr]))[:3]
        while len(others) < 3: others.append(str(yr+10+len(others)))
        add("Nigerian and World History", f"In which year did the following happen: {name}?", str(yr), others,
            f"{name} happened in {yr}.")
    pairs = [(("Nigeria gained independence", 1960), ("Nigeria became a republic", 1963)),
             (("The Sokoto Jihad began", 1804), ("Nigeria gained independence", 1960)),
             (("The First World War began", 1914), ("The Second World War began", 1939)),
             (("The amalgamation of Nigeria", 1914), ("Nigeria gained independence", 1960)),
             (("The Nigerian Civil War began", 1967), ("The Nigerian Civil War ended", 1970)),
             (("The OAU was founded", 1963), ("The African Union replaced the OAU", 2002)),
             (("The Berlin Conference", 1884), ("Nigeria gained independence", 1960)),
             (("The Second World War ended", 1945), ("Nigeria gained independence", 1960)),
             (("Ghana gained independence", 1957), ("Nigeria gained independence", 1960)),
             (("The Aba Women's Riot", 1929), ("Nigeria gained independence", 1960))]
    for (n1, y1), (n2, y2) in pairs:
        gap = y2-y1
        add("Nigerian and World History", f"How many years after {n1} ({y1}) did {n2} ({y2}) happen?", f"{gap} years",
            [f"{gap+5} years", f"{gap-5} years", f"{gap+10} years"], f"{y2} - {y1} = {gap} years.")
    facts = [
        ("Early Civilisations", "The Nok culture is famous for its:", "terracotta sculptures", ["bronze plaques", "stone castles", "gold mines"], "Nok terracotta figures are among Africa's oldest art."),
        ("Early Civilisations", "The Benin Kingdom is famous for its:", "bronze plaques and ivory carvings", ["terracotta heads", "stone walls", "gold coins"], "Benin bronzes are world-famous."),
        ("Early Civilisations", "Ife is famous for its:", "naturalistic bronze and terracotta heads", ["stone castles", "gold mines", "iron bridges"], "Ife art is noted for its naturalism."),
        ("Early Civilisations", "The Kanem-Bornu Empire was located around:", "Lake Chad", ["the River Niger", "the Atlantic coast", "the Jos Plateau"], "Kanem-Bornu grew around Lake Chad."),
        ("The Sokoto Caliphate", "The Sokoto Caliphate was founded after the jihad of:", "1804", ["1807", "1814", "1900"], "Usman dan Fodio's jihad began in 1804."),
        ("Colonial Nigeria", "The British administrator who amalgamated Nigeria in 1914 was:", "Lord Lugard", ["Lord Macaulay", "Sir Hugh Clifford", "Sir Arthur Richards"], "Frederick Lugard amalgamated the protectorates in 1914."),
        ("Colonial Nigeria", "Indirect rule in Northern Nigeria was introduced by:", "Lord Lugard", ["Sir Hugh Clifford", "Sir Arthur Richards", "Lord Macpherson"], "Lugard used existing emirs under indirect rule."),
        ("Colonial Nigeria", "The Aba Women's Riot of 1929 protested against:", "taxation of women", ["forced labour", "land seizure", "school fees"], "Women protested against proposed taxation."),
        ("Nationalism", "The first Nigerian political party, the NNDP, was founded by:", "Herbert Macaulay", ["Nnamdi Azikiwe", "Obafemi Awolowo", "Ahmadu Bello"], "Herbert Macaulay founded the NNDP in 1923."),
        ("Nationalism", "The NCNC was led by:", "Nnamdi Azikiwe", ["Obafemi Awolowo", "Ahmadu Bello", "Herbert Macaulay"], "Azikiwe led the National Council of Nigeria and the Cameroons."),
        ("Nationalism", "The Action Group was led by:", "Obafemi Awolowo", ["Nnamdi Azikiwe", "Ahmadu Bello", "Tafawa Balewa"], "Awolowo led the Action Group in the Western Region."),
        ("Nationalism", "The NPC was led by:", "Ahmadu Bello", ["Obafemi Awolowo", "Nnamdi Azikiwe", "Herbert Macaulay"], "Ahmadu Bello, the Sardauna of Sokoto, led the Northern People's Congress."),
        ("Military Rule", "Nigeria's first military Head of State was:", "General Aguiyi-Ironsi", ["General Yakubu Gowon", "General Murtala Mohammed", "General Olusegun Obasanjo"], "Aguiyi-Ironsi took power after the January 1966 coup."),
        ("Military Rule", "The Nigerian Civil War was fought between:", "the Federal Government and Biafra", ["Nigeria and Ghana", "Nigeria and Cameroon", "the North and the West"], "Biafra, led by Ojukwu, seceded in 1967."),
        ("Military Rule", "The leader of Biafra during the Civil War was:", "Odumegwu Ojukwu", ["Yakubu Gowon", "Nnamdi Azikiwe", "Obafemi Awolowo"], "Ojukwu declared the Republic of Biafra."),
        ("Post-Independence", "Nigeria's capital was moved from Lagos to Abuja in:", "1991", ["1979", "1983", "1999"], "The seat of government moved to Abuja in December 1991."),
        ("African History", "The first African country to gain independence from colonial rule was:", "Ghana (1957)", ["Nigeria (1960)", "Kenya (1963)", "Egypt (1922)"], "Ghana, under Nkrumah, led sub-Saharan independence in 1957."),
        ("African History", "The apartheid system was practised in:", "South Africa", ["Ghana", "Kenya", "Egypt"], "Apartheid was racial segregation in South Africa."),
        ("African History", "The leader of the anti-apartheid struggle who became South Africa's first democratic president was:", "Nelson Mandela", ["Robert Mugabe", "Kwame Nkrumah", "Julius Nyerere"], "Mandela was elected president in 1994."),
        ("World History", "The Second World War ended in:", "1945", ["1918", "1939", "1950"], "The war ended in 1945."),
        ("World History", "The League of Nations was replaced by the:", "United Nations", ["African Union", "European Union", "Commonwealth"], "The UN was founded in 1945 to replace the League."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- CRS ----------------
def crs_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "CRS", t, q, c, d, e))
    facts = [
        ("Sovereignty of God", "In the beginning, God created:", "the heaven and the earth", ["man only", "the angels only", "the sea only"], "Genesis 1:1 - 'In the beginning God created the heaven and the earth.'"),
        ("Sovereignty of God", "God created man on the:", "sixth day", ["first day", "third day", "seventh day"], "Man was created on the sixth day (Genesis 1:26-31)."),
        ("Sovereignty of God", "God rested on the:", "seventh day", ["sixth day", "first day", "third day"], "God rested on the seventh day (Genesis 2:2)."),
        ("The Covenant", "God's covenant with Noah was sealed with the:", "rainbow", ["dove", "olive branch", "ark"], "The rainbow was the sign of the covenant with Noah (Genesis 9:13)."),
        ("The Covenant", "God promised Abraham that his descendants would be as many as the:", "stars of heaven", ["grains of sand only", "leaves of trees", "fish of the sea"], "God promised Abraham descendants as numerous as the stars (Genesis 15:5)."),
        ("The Covenant", "The sign of the covenant with Abraham was:", "circumcision", ["baptism", "sacrifice", "fasting"], "Circumcision was the sign of the Abrahamic covenant (Genesis 17:10-11)."),
        ("The Covenant", "The Ten Commandments were given to Moses on Mount:", "Sinai", ["Zion", "Carmel", "Nebo"], "Moses received the Law on Mount Sinai (Exodus 20)."),
        ("The Covenant", "The first commandment is:", "You shall have no other gods before me", ["You shall not steal", "You shall not kill", "Honour your father and mother"], "Exodus 20:3 - the first commandment forbids other gods."),
        ("Leadership Qualities", "Joseph was sold into slavery by his:", "brothers", ["father", "master", "friends"], "Joseph's brothers sold him to Ishmaelite traders (Genesis 37)."),
        ("Leadership Qualities", "Joseph became a ruler in:", "Egypt", ["Canaan", "Babylon", "Assyria"], "Joseph rose to become governor of Egypt under Pharaoh."),
        ("Leadership Qualities", "Moses led the Israelites out of:", "Egypt", ["Babylon", "Canaan", "Assyria"], "The Exodus was the deliverance from Egypt."),
        ("Leadership Qualities", "The Red Sea was parted by:", "Moses", ["Aaron", "Joshua", "David"], "Moses stretched out his hand and the Red Sea parted (Exodus 14)."),
        ("Leadership Qualities", "Joshua led the Israelites across the:", "River Jordan", ["Red Sea", "River Nile", "River Euphrates"], "Joshua led the crossing of the Jordan into Canaan."),
        ("Leadership Qualities", "Deborah was a:", "judge and prophetess", ["queen", "priestess only", "king"], "Deborah judged Israel and prophesied (Judges 4)."),
        ("Leadership Qualities", "Samson's strength lay in his:", "hair", ["arms", "eyes", "feet"], "Samson's strength was tied to his uncut hair (Judges 16)."),
        ("Leadership Qualities", "Gideon defeated the Midianites with:", "300 men", ["3,000 men", "30,000 men", "100 men"], "Gideon won with 300 men (Judges 7)."),
        ("The Monarchy", "The first king of Israel was:", "Saul", ["David", "Solomon", "Samuel"], "Saul was anointed as Israel's first king."),
        ("The Monarchy", "David defeated Goliath with a:", "sling and stone", ["sword", "spear", "bow"], "David killed Goliath with a sling and a stone (1 Samuel 17)."),
        ("The Monarchy", "Solomon was known for his:", "wisdom", ["strength", "wealth only", "speed"], "Solomon asked God for wisdom (1 Kings 3)."),
        ("The Monarchy", "Solomon built the:", "Temple in Jerusalem", ["Ark of the Covenant", "Tower of Babel", "Tabernacle"], "Solomon built the first Temple in Jerusalem."),
        ("The Prophets", "The prophet who was swallowed by a great fish was:", "Jonah", ["Elijah", "Elisha", "Isaiah"], "Jonah was in the fish for three days (Jonah 1:17)."),
        ("The Prophets", "Elijah challenged the prophets of Baal on Mount:", "Carmel", ["Sinai", "Zion", "Nebo"], "The contest took place on Mount Carmel (1 Kings 18)."),
        ("The Prophets", "Isaiah prophesied the birth of:", "Emmanuel (the Messiah)", ["Moses", "David", "Solomon"], "Isaiah 7:14 speaks of Emmanuel."),
        ("The Prophets", "Amos was a prophet from:", "Tekoa", ["Jerusalem", "Bethlehem", "Nazareth"], "Amos was a herdsman from Tekoa."),
        ("The Prophets", "Hosea's message centred on God's:", "love and faithfulness", ["anger only", "judgement only", "silence"], "Hosea pictures God's faithful love for unfaithful Israel."),
        ("The Birth of Jesus", "Jesus was born in:", "Bethlehem", ["Nazareth", "Jerusalem", "Capernaum"], "Jesus was born in Bethlehem (Matthew 2:1)."),
        ("The Birth of Jesus", "The mother of Jesus was:", "Mary", ["Elizabeth", "Martha", "Salome"], "Mary was the mother of Jesus."),
        ("The Birth of Jesus", "The angel who announced Jesus' birth to Mary was:", "Gabriel", ["Michael", "Raphael", "Uriel"], "Gabriel announced the birth (Luke 1:26)."),
        ("The Birth of Jesus", "The wise men followed a:", "star", ["cloud", "comet", "moon"], "A star guided the wise men to Bethlehem."),
        ("The Birth of Jesus", "Jesus was baptised by:", "John the Baptist", ["Peter", "James", "Andrew"], "John baptised Jesus in the Jordan."),
        ("The Ministry of Jesus", "The first miracle of Jesus was turning water into wine at:", "Cana", ["Capernaum", "Jerusalem", "Bethsaida"], "The wedding at Cana (John 2)."),
        ("The Ministry of Jesus", "Jesus fed five thousand people with:", "five loaves and two fish", ["seven loaves and three fish", "two loaves and five fish", "ten loaves and ten fish"], "Five loaves and two fish fed the multitude (John 6)."),
        ("The Ministry of Jesus", "The parable of the Good Samaritan teaches:", "love for one's neighbour", ["the need for wealth", "the value of fasting", "the duty of prayer"], "The Samaritan helped the wounded man (Luke 10)."),
        ("The Ministry of Jesus", "The parable of the Prodigal Son teaches God's:", "forgiveness and mercy", ["anger", "indifference", "partiality"], "The father welcomed the returning son (Luke 15)."),
        ("The Ministry of Jesus", "The parable of the Sower teaches about:", "responses to God's word", ["farming methods", "the value of money", "the need for rest"], "The soils picture different responses to the word (Matthew 13)."),
        ("The Ministry of Jesus", "Jesus calmed the storm on the:", "Sea of Galilee", ["Red Sea", "Dead Sea", "River Jordan"], "Jesus calmed the wind and waves on the Sea of Galilee."),
        ("The Passion", "Jesus was betrayed by:", "Judas Iscariot", ["Peter", "Thomas", "Matthew"], "Judas betrayed Jesus for thirty pieces of silver."),
        ("The Passion", "Jesus was crucified on:", "the cross at Golgotha", ["Mount Sinai", "Mount Carmel", "the Temple"], "Jesus was crucified at Golgotha."),
        ("The Passion", "Jesus rose from the dead on the:", "third day", ["second day", "seventh day", "first day of the week only"], "He rose on the third day, the first day of the week."),
        ("The Passion", "The Last Supper was shared by Jesus with his:", "disciples", ["Pharisees", "Sadducees", "family only"], "Jesus shared the Passover meal with his disciples."),
        ("The Early Church", "The Holy Spirit came upon the disciples on the day of:", "Pentecost", ["Passover", "Atonement", "Tabernacles"], "Pentecost was the outpouring of the Spirit (Acts 2)."),
        ("The Early Church", "The first Christian martyr was:", "Stephen", ["Peter", "Paul", "James"], "Stephen was stoned (Acts 7)."),
        ("The Early Church", "Saul was converted on the road to:", "Damascus", ["Jerusalem", "Antioch", "Rome"], "Saul met the risen Jesus on the Damascus road (Acts 9)."),
        ("The Early Church", "The apostle to the Gentiles was:", "Paul", ["Peter", "John", "James"], "Paul was called to take the gospel to the Gentiles."),
        ("Christian Ethics", "The Golden Rule teaches us to do to others as we would have them do to:", "us", ["the rich", "the poor", "our friends only"], "Matthew 7:12 - do to others as you would have them do to you."),
        ("Christian Ethics", "The greatest commandment is to love:", "God and one's neighbour", ["oneself only", "one's family only", "one's country only"], "Love God and love your neighbour (Matthew 22:37-39)."),
        ("Christian Ethics", "The fruit of the Spirit includes love, joy and:", "peace", ["anger", "envy", "pride"], "Galatians 5:22 lists love, joy, peace, patience and more."),
        ("Christian Ethics", "Faith without works is:", "dead", ["alive", "perfect", "enough"], "James 2:26 - faith without works is dead."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- IRS ----------------
def irs_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "IRS", t, q, c, d, e))
    facts = [
        ("The Qur'an", "The Qur'an was revealed to Prophet Muhammad (SAW) through Angel:", "Jibril (Gabriel)", ["Mikail", "Israfil", "Malik"], "Jibril brought the revelation to the Prophet."),
        ("The Qur'an", "The first revelation came in the month of:", "Ramadan", ["Shawwal", "Dhul-Hijjah", "Muharram"], "The Qur'an began to be revealed in Ramadan."),
        ("The Qur'an", "The first revealed words were:", "'Iqra' (Read)", ["'Pray'", "'Fast'", "'Give'"], "The first revelation began 'Iqra bismi Rabbik' (Q 96:1)."),
        ("The Qur'an", "The Qur'an has:", "114 chapters (surahs)", ["100 chapters", "120 chapters", "99 chapters"], "The Qur'an contains 114 surahs."),
        ("The Qur'an", "The longest chapter of the Qur'an is:", "Surah Al-Baqarah", ["Surah Al-Ikhlas", "Surah Al-Fatihah", "Surah Ya-Sin"], "Al-Baqarah is the longest surah."),
        ("The Qur'an", "The opening chapter of the Qur'an is:", "Surah Al-Fatihah", ["Surah Al-Baqarah", "Surah Al-Ikhlas", "Surah An-Nas"], "Al-Fatihah opens the Qur'an."),
        ("The Qur'an", "Surah Al-Ikhlas teaches the:", "oneness of Allah (Tawhid)", ["story of Moses", "rules of fasting", "laws of inheritance"], "Al-Ikhlas (Q 112) affirms Allah's oneness."),
        ("Tawhid", "Tawhid means the:", "oneness of Allah", ["plurality of gods", "worship of angels", "belief in fate only"], "Tawhid is belief in the absolute oneness of Allah."),
        ("Tawhid", "Shirk is the sin of:", "associating partners with Allah", ["disbelieving in angels", "missing prayers", "eating pork"], "Shirk is the greatest sin in Islam."),
        ("The Five Pillars", "The first pillar of Islam is the:", "Shahadah (declaration of faith)", ["Salat", "Zakat", "Sawm"], "The Shahadah is the testimony of faith."),
        ("The Five Pillars", "Salat is the:", "five daily prayers", ["annual fast", "pilgrimage", "alms tax"], "Salat is prayer, performed five times daily."),
        ("The Five Pillars", "Zakat is:", "obligatory almsgiving", ["voluntary charity", "fasting", "pilgrimage"], "Zakat is the compulsory giving of a portion of wealth."),
        ("The Five Pillars", "Sawm is fasting in the month of:", "Ramadan", ["Shawwal", "Muharram", "Dhul-Hijjah"], "Muslims fast in Ramadan."),
        ("The Five Pillars", "Hajj is the pilgrimage to:", "Makkah", ["Madinah", "Jerusalem", "Cairo"], "Hajj is the pilgrimage to Makkah."),
        ("The Five Pillars", "The daily prayers are:", "five", ["three", "four", "seven"], "Fajr, Zuhr, Asr, Maghrib and Isha make five daily prayers."),
        ("The Five Pillars", "The morning prayer is:", "Fajr", ["Zuhr", "Asr", "Isha"], "Fajr is the dawn prayer."),
        ("The Five Pillars", "The night prayer is:", "Isha", ["Fajr", "Zuhr", "Maghrib"], "Isha is the night prayer."),
        ("The Prophets", "The first prophet of Islam was:", "Adam (AS)", ["Nuh", "Ibrahim", "Musa"], "Adam was the first prophet and the first man."),
        ("The Prophets", "The prophet who built the Ark was:", "Nuh (Noah)", ["Ibrahim", "Musa", "Isa"], "Nuh built the Ark at Allah's command."),
        ("The Prophets", "The prophet who was thrown into the fire but was saved was:", "Ibrahim (Abraham)", ["Musa", "Yusuf", "Ayyub"], "Ibrahim was saved from the fire by Allah."),
        ("The Prophets", "The prophet who received the Tawrah was:", "Musa (Moses)", ["Isa", "Dawud", "Ibrahim"], "Musa received the Tawrah."),
        ("The Prophets", "The prophet who received the Injil was:", "Isa (Jesus)", ["Musa", "Dawud", "Muhammad"], "Isa received the Injil."),
        ("The Prophets", "The prophet who received the Zabur was:", "Dawud (David)", ["Musa", "Isa", "Sulayman"], "Dawud received the Zabur (Psalms)."),
        ("The Prophets", "Prophet Muhammad (SAW) was born in:", "Makkah", ["Madinah", "Taif", "Jerusalem"], "The Prophet was born in Makkah in 570 CE."),
        ("The Prophets", "Prophet Muhammad (SAW) migrated to Madinah in:", "622 CE", ["570 CE", "610 CE", "632 CE"], "The Hijrah to Madinah took place in 622 CE."),
        ("The Prophets", "Prophet Muhammad (SAW) died in:", "632 CE", ["622 CE", "610 CE", "570 CE"], "The Prophet died in Madinah in 632 CE (11 AH)."),
        ("The Prophets", "The mother of Prophet Muhammad (SAW) was:", "Aminah", ["Khadijah", "Aisha", "Fatimah"], "Aminah was the Prophet's mother."),
        ("The Prophets", "The first wife of Prophet Muhammad (SAW) was:", "Khadijah", ["Aisha", "Hafsah", "Fatimah"], "Khadijah was his first wife."),
        ("Hadith", "Hadith refers to the:", "sayings and actions of Prophet Muhammad (SAW)", ["words of the Qur'an only", "laws of the caliphs", "stories of the companions only"], "Hadith records the Sunnah of the Prophet."),
        ("Hadith", "The most authentic collection of Hadith is:", "Sahih al-Bukhari", ["Sunan Ibn Majah only", "Muwatta only", "Musnad Ahmad only"], "Sahih al-Bukhari is regarded as the most authentic collection."),
        ("Fiqh", "Wudu is the:", "ablution before prayer", ["full bath", "dry ablution", "call to prayer"], "Wudu is ritual washing before Salat."),
        ("Fiqh", "Tayammum is ablution using:", "clean earth/dust", ["water", "oil", "sand only when wet"], "Tayammum is dry ablution with clean earth when water is unavailable."),
        ("Fiqh", "The call to prayer is the:", "Adhan", ["Iqamah", "Khutbah", "Tasbih"], "The Adhan calls Muslims to prayer."),
        ("Fiqh", "The Friday congregational prayer is:", "Jumu'ah", ["Taraweeh", "Tahajjud", "Eid"], "Jumu'ah is the Friday prayer."),
        ("Islamic History", "The first Caliph after Prophet Muhammad (SAW) was:", "Abu Bakr", ["Umar", "Uthman", "Ali"], "Abu Bakr was the first of the Rightly Guided Caliphs."),
        ("Islamic History", "The second Caliph was:", "Umar ibn al-Khattab", ["Abu Bakr", "Uthman", "Ali"], "Umar succeeded Abu Bakr."),
        ("Islamic History", "The third Caliph was:", "Uthman ibn Affan", ["Ali", "Umar", "Abu Bakr"], "Uthman was the third Caliph."),
        ("Islamic History", "The fourth Caliph was:", "Ali ibn Abi Talib", ["Uthman", "Umar", "Abu Bakr"], "Ali was the fourth Caliph."),
        ("Islamic History", "The Qur'an was compiled into a single book during the caliphate of:", "Abu Bakr", ["Umar", "Uthman", "Ali"], "The compilation began under Abu Bakr and was standardised under Uthman."),
        ("Islamic History", "The Sokoto Caliphate was founded by:", "Usman dan Fodio", ["Ahmadu Bello", "Muhammed Bello", "Nana Asma'u"], "Usman dan Fodio founded the Sokoto Caliphate after the 1804 jihad."),
        ("Islamic History", "The first mosque built in Islam was:", "Quba Mosque", ["the Prophet's Mosque", "Al-Aqsa", "the Ka'bah"], "Quba was the first mosque built by the Prophet on arrival in Madinah."),
        ("Islamic Morality", "Honesty in Islam is called:", "Sidq", ["Amanah", "Ihsan", "Taqwa"], "Sidq means truthfulness."),
        ("Islamic Morality", "Trustworthiness in Islam is called:", "Amanah", ["Sidq", "Ihsan", "Sabr"], "Amanah is keeping trust."),
        ("Islamic Morality", "Patience in Islam is called:", "Sabr", ["Shukr", "Taqwa", "Ihsan"], "Sabr is patience in hardship and obedience."),
        ("Islamic Morality", "God-consciousness in Islam is called:", "Taqwa", ["Sabr", "Shukr", "Sidq"], "Taqwa is consciousness of Allah."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- CIVIC ----------------
def civic_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Civic", t, q, c, d, e))
    facts = [
        ("Values", "Values are:", "beliefs and standards that guide behaviour", ["laws of the country", "religious rules only", "school rules only"], "Values shape what people consider right and important."),
        ("Values", "Honesty as a value means:", "telling the truth", ["keeping secrets", "avoiding people", "being rich"], "An honest person is truthful."),
        ("Values", "One importance of values in society is that they:", "promote order and good conduct", ["cause conflict", "encourage crime", "divide people"], "Shared values hold society together."),
        ("Citizenship", "A citizen is a:", "legal member of a state", ["visitor to a state", "foreigner in a state", "refugee in a state"], "Citizenship is legal membership of a state."),
        ("Citizenship", "Citizenship education teaches people their:", "rights and duties", ["wealth and power", "history only", "religion only"], "It prepares citizens to participate responsibly."),
        ("Citizenship", "National consciousness means:", "awareness of belonging to one nation", ["loyalty to one's village only", "hatred of other nations", "ignorance of history"], "It is the sense of shared national identity."),
        ("Human Rights", "Human rights are rights that belong to every person by virtue of being:", "human", ["rich", "educated", "a citizen only"], "Human rights are universal."),
        ("Human Rights", "The right to life is a:", "fundamental human right", ["political privilege", "economic benefit", "social favour"], "The right to life is in the constitution and the UDHR."),
        ("Human Rights", "The Universal Declaration of Human Rights was adopted in:", "1948", ["1919", "1945", "1960"], "The UDHR was adopted by the UN in 1948."),
        ("Human Rights", "Freedom of speech is a:", "civil right", ["economic right", "social right", "cultural right"], "It is a civil and political right."),
        ("Human Rights", "One limitation of human rights is:", "the rights of others", ["wealth", "education", "age only"], "Rights are limited where they infringe others' rights."),
        ("Law and Order", "Law is a:", "set of rules that guide behaviour in society", ["suggestion", "custom only", "religious teaching only"], "Laws are binding rules enforced by the state."),
        ("Law and Order", "Constituted authority is authority that is:", "established by law", ["seized by force", "inherited only", "bought with money"], "It is power given by the constitution or law."),
        ("Law and Order", "One type of constituted authority is:", "traditional authority", ["military authority", "rebel authority", "gang authority"], "Traditional, political and religious authorities are constituted authorities."),
        ("Responsible Parenthood", "Responsible parenthood means:", "caring properly for one's children", ["having many children", "leaving children alone", "sending children to work"], "Responsible parents provide food, education, love and guidance."),
        ("Responsible Parenthood", "One role of responsible parents is to:", "provide education for their children", ["ignore their children", "force children to work", "abandon their children"], "Parents must educate and nurture their children."),
        ("Traffic Rules", "A red traffic light means:", "stop", ["go", "slow down", "turn left"], "Red means stop."),
        ("Traffic Rules", "A green traffic light means:", "go", ["stop", "wait", "turn back"], "Green means go when the way is clear."),
        ("Traffic Rules", "A yellow (amber) traffic light means:", "get ready to stop or go", ["go at full speed", "stop at once always", "reverse"], "Amber means prepare to stop (or proceed with caution where allowed)."),
        ("Traffic Rules", "The agency that manages road safety in Nigeria is the:", "Federal Road Safety Corps (FRSC)", ["Nigeria Police Force", "Nigerian Army", "Civil Defence"], "The FRSC enforces road safety."),
        ("Interpersonal Relations", "Good interpersonal relations require:", "respect and tolerance", ["arrogance", "selfishness", "dishonesty"], "Respect and tolerance build good relationships."),
        ("Interpersonal Relations", "Tolerance means:", "accepting people with different views", ["agreeing with everyone", "ignoring everyone", "fighting others"], "Tolerance is respecting differences."),
        ("Interpersonal Relations", "Dialogue is important in resolving conflict because it:", "allows parties to talk and understand each other", ["increases fighting", "wastes time", "favours the strong"], "Dialogue is a peaceful way to settle disputes."),
        ("Interpersonal Relations", "One cause of conflict in society is:", "competition over scarce resources", ["tolerance", "dialogue", "cooperation"], "Scarcity breeds competition and conflict."),
        ("Interpersonal Relations", "Conflict can be resolved peacefully through:", "mediation", ["violence", "revenge", "avoidance only"], "Mediation uses a neutral third party."),
        ("National Identity", "The Nigerian national anthem begins with:", "'Arise, O compatriots'", ["'Nigeria, we hail thee'", "'God bless Nigeria'", "'O God of creation'"], "The anthem adopted in 1978 begins 'Arise, O compatriots'."),
        ("National Identity", "The colours of the Nigerian flag are:", "green, white and green", ["green, white and red", "red, white and blue", "green and yellow"], "The flag is green-white-green."),
        ("National Identity", "The green in the Nigerian flag represents:", "agriculture and the land", ["peace", "the rivers", "the sky"], "Green stands for agriculture; white for peace and unity."),
        ("National Identity", "The white in the Nigerian flag represents:", "peace and unity", ["agriculture", "the rivers", "strength"], "White stands for peace and unity."),
        ("National Identity", "Nigeria's coat of arms has the motto:", "Unity and Faith, Peace and Progress", ["Peace and Unity", "Strength and Honour", "Faith and Courage"], "The motto is 'Unity and Faith, Peace and Progress'."),
        ("National Identity", "The eagle on Nigeria's coat of arms represents:", "strength", ["peace", "agriculture", "unity"], "The eagle symbolises strength."),
        ("Structure of Government", "The three tiers of government in Nigeria are federal, state and:", "local", ["regional", "traditional", "military"], "Nigeria has federal, state and local tiers."),
        ("Structure of Government", "The head of a local government is the:", "chairman", ["governor", "president", "senator"], "The chairman heads the local government council."),
        ("Structure of Government", "The head of a state government is the:", "governor", ["president", "chairman", "minister"], "The governor heads the state executive."),
        ("Democracy", "Democracy is government by the:", "people", ["military", "king", "few rich"], "Democracy means rule by the people."),
        ("Democracy", "One feature of democracy is:", "free and fair elections", ["one-party rule", "censorship", "military rule"], "Elections let the people choose leaders."),
        ("Democracy", "One pillar of democracy is the:", "rule of law", ["rule of the military", "rule of the rich", "rule of tradition only"], "The rule of law is a pillar of democracy."),
        ("Democracy", "The rule of law means:", "all persons are equal before the law", ["leaders are above the law", "the rich are above the law", "laws apply only to the poor"], "No one is above the law."),
        ("Democracy", "A problem of democracy in Nigeria is:", "electoral malpractice", ["free elections", "rule of law", "press freedom"], "Rigging and violence weaken democracy."),
        ("National Development", "National development means:", "improvement in the lives of citizens and the economy", ["building stadiums only", "increasing taxes", "reducing population"], "Development raises living standards and economic capacity."),
        ("National Development", "Corruption hinders national development because it:", "wastes public resources", ["increases honesty", "builds trust", "creates jobs fairly"], "Corruption diverts money meant for development."),
        ("Drug Abuse", "Drug abuse is the:", "use of drugs in a harmful way", ["use of prescribed drugs", "use of herbal drugs", "use of drugs by doctors"], "Abuse is taking drugs without medical need or in excess."),
        ("Drug Abuse", "One effect of drug abuse is:", "damage to health and behaviour", ["better health", "improved studies", "stronger family"], "Drugs harm health, judgement and relationships."),
        ("Drug Abuse", "The agency that fights drug trafficking in Nigeria is the:", "NDLEA", ["FRSC", "NAPTIP", "EFCC"], "The National Drug Law Enforcement Agency fights drug abuse and trafficking."),
        ("Human Trafficking", "Human trafficking is:", "the illegal trade in people for exploitation", ["legal migration", "voluntary travel", "tourism"], "Trafficking exploits victims for labour or sex."),
        ("Human Trafficking", "The agency that fights human trafficking in Nigeria is:", "NAPTIP", ["NDLEA", "FRSC", "EFCC"], "NAPTIP is the National Agency for the Prohibition of Trafficking in Persons."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
    return P

# ---------------- LITERATURE ----------------
def literature_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Literature", t, q, c, d, e))
    facts = [
        ("Literary Terms", "A poem of 14 lines with a specific rhyme scheme is a:", "sonnet", ["ballad", "ode", "elegy"], "A sonnet has 14 lines."),
        ("Literary Terms", "The central idea or message in a literary work is the:", "theme", ["plot", "setting", "style"], "Theme is the main idea."),
        ("Literary Terms", "The sequence of events in a story is the:", "plot", ["theme", "setting", "character"], "Plot is the arrangement of events."),
        ("Literary Terms", "The time and place of a story is its:", "setting", ["plot", "theme", "style"], "Setting is time and place."),
        ("Literary Terms", "A comparison using 'like' or 'as' is a:", "simile", ["metaphor", "personification", "hyperbole"], "Simile uses 'like' or 'as'."),
        ("Literary Terms", "A direct comparison without 'like' or 'as' is a:", "metaphor", ["simile", "irony", "alliteration"], "Metaphor says one thing is another."),
        ("Literary Terms", "Giving human qualities to non-human things is:", "personification", ["simile", "metaphor", "irony"], "Personification gives human traits to objects or animals."),
        ("Literary Terms", "An exaggeration for effect is:", "hyperbole", ["irony", "litotes", "euphemism"], "Hyperbole is deliberate exaggeration."),
        ("Literary Terms", "The repetition of initial consonant sounds is:", "alliteration", ["assonance", "onomatopoeia", "rhyme"], "Alliteration repeats beginning sounds."),
        ("Literary Terms", "Words that imitate sounds, like 'buzz' or 'bang', are:", "onomatopoeia", ["alliteration", "assonance", "metaphor"], "Onomatopoeia imitates the sound it names."),
        ("Literary Terms", "A statement that means the opposite of what it says is:", "irony", ["simile", "metaphor", "hyperbole"], "Irony is a contrast between expectation and reality."),
        ("Literary Terms", "The main character of a story is the:", "protagonist", ["antagonist", "foil", "narrator"], "The protagonist is the central character."),
        ("Literary Terms", "The character who opposes the protagonist is the:", "antagonist", ["protagonist", "hero", "narrator"], "The antagonist creates conflict."),
        ("Literary Terms", "A play that ends sadly for the hero is a:", "tragedy", ["comedy", "farce", "melodrama"], "Tragedy ends in the hero's downfall."),
        ("Literary Terms", "A play meant to make the audience laugh is a:", "comedy", ["tragedy", "elegy", "epic"], "Comedy is humorous drama."),
        ("Literary Terms", "A long narrative poem about heroic deeds is an:", "epic", ["sonnet", "ballad", "ode"], "Epics tell heroic stories."),
        ("Literary Terms", "A poem mourning the dead is an:", "elegy", ["ode", "sonnet", "ballad"], "An elegy is a lament for the dead."),
        ("Literary Terms", "A poem of praise is an:", "ode", ["elegy", "sonnet", "epic"], "An ode praises its subject."),
        ("Literary Terms", "A story that teaches a moral, often with animals, is a:", "fable", ["myth", "legend", "epic"], "Fables teach morals through animal characters."),
        ("Literary Terms", "The voice that tells a story is the:", "narrator", ["author", "protagonist", "reader"], "The narrator tells the story."),
        ("Literary Terms", "A story told by a character using 'I' is in the:", "first person", ["second person", "third person", "omniscient"], "First-person narration uses 'I'."),
        ("Literary Terms", "The feeling a literary work creates in the reader is its:", "mood", ["theme", "tone", "plot"], "Mood is the atmosphere the work creates."),
        ("Literary Terms", "The writer's attitude towards the subject is the:", "tone", ["mood", "theme", "setting"], "Tone is the author's attitude."),
        ("Literary Terms", "A hint of what will happen later in a story is:", "foreshadowing", ["flashback", "irony", "suspense"], "Foreshadowing hints at future events."),
        ("Literary Terms", "A scene from an earlier time in a story is a:", "flashback", ["foreshadowing", "climax", "denouement"], "A flashback returns to the past."),
        ("Literary Terms", "The turning point of a story is the:", "climax", ["exposition", "resolution", "rising action"], "The climax is the highest point of tension."),
        ("Drama", "A person who writes plays is a:", "playwright", ["novelist", "poet", "critic"], "A playwright writes drama."),
        ("Drama", "The spoken words of characters in a play are called:", "dialogue", ["soliloquy", "monologue", "aside"], "Dialogue is conversation between characters."),
        ("Drama", "A long speech by one character alone on stage is a:", "soliloquy", ["dialogue", "aside", "chorus"], "A soliloquy is a character thinking aloud alone."),
        ("Drama", "Stage directions in a play tell actors:", "what to do and how to move", ["what to wear only", "what the audience thinks", "what the author feels"], "Stage directions guide performance."),
        ("Poetry", "A stanza is a:", "group of lines in a poem", ["single line", "single word", "single rhyme"], "Stanzas are verse paragraphs."),
        ("Poetry", "The pattern of stressed and unstressed syllables in a poem is its:", "rhythm", ["rhyme", "tone", "theme"], "Rhythm is the beat of the poem."),
        ("Poetry", "Words at the ends of lines that sound alike form a:", "rhyme", ["rhythm", "stanza", "meter"], "Rhyme is similarity of sound at line ends."),
        ("Poetry", "The speaker in a poem is the:", "persona", ["poet", "reader", "critic"], "The persona is the voice speaking in the poem."),
        ("Prose", "A long fictional narrative is a:", "novel", ["short story", "essay", "play"], "A novel is a long work of fiction."),
        ("Prose", "A short fictional narrative is a:", "short story", ["novel", "epic", "drama"], "A short story is brief fiction."),
        ("Prose", "A true story of a person's life written by another person is a:", "biography", ["autobiography", "memoir", "novel"], "Biography is written by someone else; autobiography by the subject."),
        ("Prose", "A true story of a person's life written by the person is an:", "autobiography", ["biography", "novel", "fable"], "Autobiography is self-written life story."),
    ]
    for t, q, c, d, e in facts: add(t, q, c, d, e)
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
        others = list(dict.fromkeys(a for t, a in works if a != author))[:3]
        add("African and World Literature", f"Who wrote '{title}'?", author, others,
            f"'{title}' was written by {author}.")
    return P

# Poems for Literature passages (original, written for this practice set)
LITERATURE_POEMS = [
    ("The Silent Drum",
     "<b>The Silent Drum</b><br><br>The drum hangs silent on the wall,<br>No hands to make its rhythm call.<br>Dust settles on its tautened skin,<br>Where once the spirit danced within.<br>The dancers' feet are cold and still,<br>The songbirds left the grassy hill.<br>A silence heavy, thick, and deep,<br>Has lulled the village into sleep.<br>We wait for dawn to break the spell,<br>And drink from memory's deep well.",
     [("The 'silent drum' is a symbol of:", "a lost tradition / cultural silence", ["a musical instrument for sale", "a new festival", "a rainy season"], "The drum's silence stands for a tradition that has fallen quiet."),
      ("The mood of the poem is:", "sad and reflective", ["joyful and loud", "angry and bitter", "playful and light"], "The imagery of silence, dust and sleep creates a sad, reflective mood."),
      ("'Dust settles on its tautened skin' suggests the drum has:", "not been used for a long time", ["just been made", "been painted", "been sold"], "Dust settling means it has lain unused."),
      ("The phrase 'drink from memory's deep well' means the people:", "remember the past", ["fetch water", "dig a well", "forget the past"], "Memory's well is a metaphor for remembering."),
      ("The poem is written mainly in:", "rhymed couplets", ["free verse", "blank verse", "prose"], "The lines rhyme in pairs (wall/call, skin/within).")]),
    ("The Road Home",
     "<b>The Road Home</b><br><br>The road runs red beneath my feet,<br>Past farms where maize and millet meet.<br>The sun sinks low, the evening calls,<br>And shadows climb the village walls.<br>I hear the drums, I smell the rain,<br>I am a child of this soil again.<br>Though cities called with lights so bright,<br>Home is the lamp that burns tonight.",
     [("The persona in the poem is:", "returning home", ["leaving home forever", "lost in a city", "going to war"], "The persona walks the road home and feels like a child of the soil again."),
      ("'The road runs red' refers to the:", "laterite soil of the road", ["blood on the road", "a red carpet", "sunset only"], "Red laterite earth is common on Nigerian village roads."),
      ("The image of home as 'the lamp that burns tonight' suggests home is:", "a source of light and comfort", ["a place of darkness", "a market", "a school"], "The lamp metaphor makes home a light in the dark."),
      ("The poem's setting is:", "a village at evening", ["a city at noon", "a forest at dawn", "a beach at night"], "Farms, village walls and evening point to a village at dusk."),
      ("The dominant feeling in the poem is:", "nostalgia / longing for home", ["fear", "anger", "boredom"], "The persona longs for home and feels joy at returning.")]),
    ("The Weaver",
     "<b>The Weaver</b><br><br>Her fingers fly, her shuttle sings,<br>Thread over thread, the pattern springs.<br>Red as the dawn, and black as night,<br>She weaves the cloth in morning light.<br>Each knot a story, each line a song,<br>The cloth will last when she is gone.<br>What hands have made, no time can break,<br>For love is woven, not just made.",
     [("The weaver's work is described as:", "an art that preserves stories", ["a waste of time", "a machine process", "a child's play"], "Each knot is a story; the cloth outlasts the weaver."),
      ("'Her shuttle sings' is an example of:", "personification", ["simile", "irony", "hyperbole"], "The shuttle is given the human quality of singing."),
      ("The line 'What hands have made, no time can break' suggests:", "craftsmanship endures", ["cloth is fragile", "time destroys all", "weaving is easy"], "Handmade work lasts beyond the maker's life."),
      ("The colours mentioned in the poem are:", "red and black", ["blue and green", "white and gold", "yellow and purple"], "Red as the dawn, and black as night."),
      ("The theme of the poem is:", "the value of traditional craft", ["the danger of weaving", "the cost of cloth", "the noise of the loom"], "The poem celebrates weaving as lasting art.")]),
    ("Rain",
     "<b>Rain</b><br><br>It came at last, the longed-for rain,<br>It washed the dust from roof and lane.<br>It drummed a rhythm on the zinc,<br>It made the thirsty gardens drink.<br>The children danced with joy and glee,<br>Beneath the mango, fig and tree.<br>The earth, so dry, so cracked, so worn,<br>Was washed, and made, and born anew.",
     [("The rain is presented as:", "a blessing after drought", ["a punishment", "a nuisance", "a danger"], "The longed-for rain brings joy and renewal."),
      ("'It drummed a rhythm on the zinc' uses:", "onomatopoeia / sound imagery", ["simile", "irony", "hyperbole"], "Drumming evokes the sound of rain on zinc roofs."),
      ("The children danced because they were:", "happy the rain had come", ["afraid of the rain", "going to school", "leaving home"], "They danced with joy and glee."),
      ("The earth is described as 'born anew' because the rain:", "renewed it", ["destroyed it", "dried it", "froze it"], "The dry earth was washed and renewed."),
      ("The poem's tone is:", "joyful", ["mournful", "angry", "fearful"], "Joy, dancing and renewal set a joyful tone.")]),
]

# ---------------- ENGLISH ----------------
ENGLISH_PASSAGES = [
    ("The Market Day",
     "Every Saturday, the market in the town square came alive before sunrise. Traders arrived with baskets of yams, tomatoes and peppers, and set up their stalls under colourful umbrellas. Buyers moved from stall to stall, haggling over prices and greeting old friends. The air was filled with the smell of roasted corn and the sound of bargaining. By noon, the market was crowded, and the traders counted their money with smiles. For many families, market day was not only a time to buy and sell, but also a time to meet, share news and strengthen the bonds of the community.",
     [("The market came alive:", "before sunrise", ["at noon", "in the evening", "at midnight"], "The passage says the market came alive before sunrise."),
      ("The traders sold:", "yams, tomatoes and peppers", ["rice and beans only", "clothes and shoes", "books and pens"], "The traders brought baskets of yams, tomatoes and peppers."),
      ("Market day was important because it:", "allowed people to trade and meet", ["was a public holiday", "closed all schools", "stopped all work"], "It was a time to buy, sell, meet and share news."),
      ("The word 'haggling' in the passage means:", "bargaining over prices", ["fighting", "singing", "cooking"], "Haggling is bargaining over a price."),
      ("By noon, the traders:", "counted their money with smiles", ["closed their stalls", "went home hungry", "refused to sell"], "By noon the traders counted their money with smiles.")]),
    ("The River",
     "The river was the lifeblood of the village. Women fetched water from it at dawn, children swam in its shallow parts, and fishermen cast their nets at dusk. When the rains came, the river swelled and flooded the farms near its banks, leaving rich soil behind. The elders warned the young ones never to swim in the deep part, where the current was strong. Yet the river was loved by all, for it gave the village water, fish and fertile land.",
     [("The river provided the village with:", "water, fish and fertile land", ["gold and silver", "timber only", "roads and bridges"], "The passage says the river gave water, fish and fertile land."),
      ("The elders warned the children against swimming in the:", "deep part", ["shallow part", "bank", "village well"], "The deep part had a strong current."),
      ("When the rains came, the river:", "swelled and flooded nearby farms", ["dried up completely", "stopped flowing", "turned salty"], "The river swelled and flooded the farms."),
      ("The fishermen cast their nets at:", "dusk", ["dawn", "noon", "midnight"], "Fishermen cast their nets at dusk."),
      ("The word 'lifeblood' suggests the river was:", "essential to the village", ["dangerous to all", "owned by the elders", "full of blood"], "Lifeblood means something essential to life.")]),
    ("Amina's Dream",
     "Amina had always wanted to become a doctor. As a child, she watched her mother walk long distances to the nearest clinic, and she promised herself that one day she would bring healthcare to her village. She studied hard, often reading by the light of a kerosene lamp when the power failed. Her teachers noticed her determination and encouraged her. Years later, Amina returned to her village as a qualified doctor and opened a small clinic. The villagers celebrated, for their daughter had kept her promise.",
     [("Amina wanted to become a:", "doctor", ["teacher", "nurse", "lawyer"], "Amina wanted to become a doctor."),
      ("She studied by the light of a:", "kerosene lamp", ["candle", "torch", "moon"], "She read by a kerosene lamp when power failed."),
      ("Amina returned to her village as a:", "qualified doctor", ["student", "teacher", "visitor"], "She returned as a qualified doctor."),
      ("Her teachers encouraged her because of her:", "determination", ["wealth", "beauty", "age"], "Her teachers noticed her determination."),
      ("The villagers celebrated because Amina had:", "kept her promise", ["left the village", "become rich", "travelled abroad"], "She had promised to bring healthcare and did so.")]),
    ("The Old Library",
     "The old library stood at the end of the street, its walls covered in creeping plants. Inside, shelves of books reached to the ceiling, and the smell of old paper filled the air. Mr. Okafor, the librarian, knew every book by heart and could find any title in minutes. Children came after school to read and do their homework, and on rainy days the library was full. Though the building was old, it was the heart of learning in the town, and everyone agreed it must be protected.",
     [("The library was located:", "at the end of the street", ["in the market", "near the river", "on a hill"], "It stood at the end of the street."),
      ("Mr. Okafor was the:", "librarian", ["teacher", "mayor", "author"], "Mr. Okafor was the librarian."),
      ("Children came to the library to:", "read and do homework", ["play games", "watch films", "eat lunch"], "Children came to read and do homework."),
      ("The library was described as the heart of:", "learning in the town", ["trade in the town", "politics in the town", "sports in the town"], "It was the heart of learning."),
      ("The word 'creeping' describes plants that:", "spread along surfaces", ["grow tall quickly", "bear fruit", "have thorns"], "Creeping plants spread along walls and ground.")]),
    ("The Football Match",
     "The final match of the inter-house competition was played on a hot afternoon. The crowd cheered as the two teams ran onto the field. In the first half, neither team could score, and the goalkeepers made brilliant saves. After the break, the blue team scored a fine goal, and their supporters erupted in joy. The red team fought back, but the match ended one goal to nothing. The blue team lifted the trophy, and the captain thanked his teammates for their hard work.",
     [("The match was played on a:", "hot afternoon", ["cold morning", "rainy evening", "windy night"], "It was played on a hot afternoon."),
      ("In the first half, the score was:", "goalless", ["1-0", "2-0", "1-1"], "Neither team could score in the first half."),
      ("The blue team won by:", "one goal to nothing", ["two goals to nothing", "three goals to one", "a penalty shoot-out"], "The match ended one goal to nothing."),
      ("The supporters erupted in joy when:", "the blue team scored", ["the match ended", "it rained", "the referee arrived"], "They erupted when the blue team scored."),
      ("The captain thanked his:", "teammates", ["opponents", "teachers", "parents"], "He thanked his teammates.")]),
    ("The Drought",
     "For three years, no rain fell on the land. The wells dried up, the crops withered, and the cattle grew thin. People walked long distances in search of water, and many left their villages for the towns. Then one evening, dark clouds gathered, and rain fell heavily through the night. By morning, the fields were wet, and the people danced with joy. The drought had taught them the value of water, and they began to dig wells and store rainwater for the future.",
     [("The drought lasted for:", "three years", ["one year", "five years", "ten years"], "No rain fell for three years."),
      ("During the drought, the crops:", "withered", ["grew well", "were harvested early", "were sold cheaply"], "The crops withered."),
      ("The rain finally came:", "one evening", ["at noon", "in the morning", "at midnight"], "Dark clouds gathered one evening and rain fell."),
      ("After the drought, the people began to:", "dig wells and store rainwater", ["leave the villages", "sell their cattle", "stop farming"], "They dug wells and stored rainwater."),
      ("The drought taught the people the value of:", "water", ["money", "land", "cattle"], "It taught them the value of water.")]),
    ("The Young Farmer",
     "Tunde was the youngest farmer in his village, but he was also the most hardworking. While others planted the same crops every year, Tunde tried new methods he had learned from agricultural extension officers. He planted maize and beans together, used compost to enrich the soil, and dug a small channel to bring water to his farm. At harvest time, his yield was the best in the village. The elders praised him, and many young people began to follow his example.",
     [("Tunde was known as the:", "youngest farmer", ["oldest farmer", "richest farmer", "tallest farmer"], "Tunde was the youngest farmer."),
      ("He learned new methods from:", "agricultural extension officers", ["his father only", "the market women", "the internet"], "He learned from agricultural extension officers."),
      ("Tunde planted maize and beans:", "together", ["in different villages", "in different years", "for sale only"], "He planted maize and beans together."),
      ("At harvest, his yield was:", "the best in the village", ["the worst in the village", "average", "not measured"], "His yield was the best in the village."),
      ("The elders praised Tunde because he was:", "hardworking and innovative", ["rich", "old", "famous"], "He was hardworking and tried new methods.")]),
    ("The Letter",
     "When Ada received the letter, her hands shook. She had waited months for news of her scholarship application, and now the envelope lay before her. She opened it slowly and read the first line: 'We are pleased to inform you...' Tears of joy filled her eyes. She ran to tell her mother, who embraced her and thanked God. That evening, the whole family gathered to celebrate, and Ada promised to work hard and make them proud.",
     [("Ada had waited for news about her:", "scholarship application", ["job application", "exam result", "travel visa"], "She waited for news of her scholarship application."),
      ("The letter began with the words:", "'We are pleased to inform you...'", ["'We regret to inform you...'", "'Your application failed...'", "'Please try again...'"], "The first line said they were pleased to inform her."),
      ("Ada's reaction was one of:", "joy", ["anger", "fear", "disappointment"], "Tears of joy filled her eyes."),
      ("Ada ran to tell her:", "mother", ["father", "teacher", "friend"], "She ran to tell her mother."),
      ("Ada promised to:", "work hard and make her family proud", ["travel abroad at once", "quit her studies", "forget the village"], "She promised to work hard and make them proud.")]),
]

def english_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "English", t, q, c, d, e))
    synonyms = [("happy","joyful"),("sad","unhappy"),("brave","courageous"),("fast","quick"),
                ("big","large"),("small","tiny"),("rich","wealthy"),("poor","needy"),
                ("angry","furious"),("calm","peaceful"),("bright","shining"),("dark","dim"),
                ("strong","powerful"),("weak","feeble"),("kind","generous"),("cruel","wicked"),
                ("honest","truthful"),("lazy","idle"),("clever","intelligent"),("beautiful","lovely"),
                ("begin","start"),("end","finish"),("ask","inquire"),("answer","reply"),
                ("difficult","hard"),("easy","simple"),("ancient","old"),("modern","new"),
                ("silent","quiet"),("loud","noisy")]
    for w, syn in synonyms:
        others = [s for x, s in synonyms if s != syn][:3]
        add("Lexis: Synonyms", f"Choose the word nearest in meaning to: {w.upper()}", syn, others,
            f"{syn} is the closest synonym of {w}.")
    antonyms = [("happy","sad"),("brave","cowardly"),("fast","slow"),("big","small"),
                ("rich","poor"),("angry","calm"),("bright","dark"),("strong","weak"),
                ("kind","cruel"),("honest","dishonest"),("clever","foolish"),("begin","end"),
                ("difficult","easy"),("ancient","modern"),("silent","noisy"),("love","hate"),
                ("arrive","depart"),("accept","reject"),("victory","defeat"),("truth","falsehood")]
    for w, ant in antonyms:
        others = [a for x, a in antonyms if a != ant][:3]
        add("Lexis: Antonyms", f"Choose the word opposite in meaning to: {w.upper()}", ant, others,
            f"{ant} is the opposite of {w}.")
    idioms = [("to hit the nail on the head", "to say exactly the right thing"),
              ("to beat about the bush", "to avoid saying what one means"),
              ("to let the cat out of the bag", "to reveal a secret"),
              ("a blessing in disguise", "a good thing that first seemed bad"),
              ("to break the ice", "to start a conversation in a friendly way"),
              ("once in a blue moon", "very rarely"), ("to bite the dust", "to fail or be defeated"),
              ("to burn the midnight oil", "to work late into the night"),
              ("a piece of cake", "something very easy"),
              ("to cost an arm and a leg", "to be very expensive"),
              ("to spill the beans", "to reveal secret information"),
              ("to hit the books", "to begin studying seriously"),
              ("under the weather", "slightly ill"), ("to cut corners", "to do something cheaply and badly"),
              ("the ball is in your court", "it is your turn to act")]
    for idiom, meaning in idioms:
        others = [m for i, m in idioms if m != meaning][:3]
        add("Lexis: Idioms", f"What does the idiom '{idiom}' mean?", meaning, others,
            f"'{idiom}' means: {meaning}.")
    grammar = [
        ("Lexis and Structure", "Neither the players nor their coach _____ happy with the decision.", "was", ["were", "are", "is"], "The verb agrees with the nearer subject, 'coach' (singular)."),
        ("Lexis and Structure", "The principal congratulated the students _____ their performance.", "on", ["for", "at", "about"], "'Congratulate' is followed by 'on'."),
        ("Lexis and Structure", "The principal, as well as the teachers, _____ present.", "is", ["are", "were", "have"], "'As well as' does not change the singular subject 'principal'."),
        ("Lexis and Structure", "Each of the boys _____ a prize.", "has", ["have", "are", "were"], "'Each' is singular, so the verb is 'has'."),
        ("Lexis and Structure", "One of the students _____ absent today.", "is", ["are", "were", "have"], "'One' is singular."),
        ("Lexis and Structure", "The committee _____ reached a decision.", "has", ["have", "are", "were"], "The committee acts as one body here, so the singular verb is used."),
        ("Lexis and Structure", "She _____ to school every day.", "goes", ["go", "going", "gone"], "Third-person singular present takes '-es'."),
        ("Lexis and Structure", "They _____ playing football now.", "are", ["is", "was", "has"], "Present continuous with 'they' uses 'are'."),
        ("Lexis and Structure", "I have lived here _____ ten years.", "for", ["since", "from", "by"], "'For' is used with a period of time."),
        ("Lexis and Structure", "I have lived here _____ 2015.", "since", ["for", "from", "by"], "'Since' is used with a point in time."),
        ("Lexis and Structure", "She is good _____ Mathematics.", "at", ["in", "on", "for"], "'Good at' is the correct collocation."),
        ("Lexis and Structure", "He is afraid _____ dogs.", "of", ["from", "by", "with"], "'Afraid of' is the correct collocation."),
        ("Lexis and Structure", "The book is _____ the table.", "on", ["in", "at", "by"], "The book rests on the table."),
        ("Lexis and Structure", "Choose the correctly spelt word:", "accommodation", ["accomodation", "acommodation", "accomodationn"], "'Accommodation' has double 'c' and double 'm'."),
        ("Lexis and Structure", "Choose the correctly spelt word:", "separate", ["seperate", "separete", "seperete"], "'Separate' is spelt with 'a' after 'p'."),
        ("Lexis and Structure", "Choose the correctly spelt word:", "occurrence", ["occurence", "occurrance", "ocurrence"], "'Occurrence' has double 'c' and double 'r'."),
        ("Lexis and Structure", "The past tense of 'go' is:", "went", ["goed", "gone", "going"], "'Went' is the past tense of 'go'."),
        ("Lexis and Structure", "The past participle of 'write' is:", "written", ["wrote", "writing", "writed"], "'Written' is the past participle of 'write'."),
        ("Lexis and Structure", "The plural of 'child' is:", "children", ["childs", "childes", "childrens"], "'Children' is the irregular plural of 'child'."),
        ("Lexis and Structure", "The plural of 'woman' is:", "women", ["womans", "womens", "womanes"], "'Women' is the plural of 'woman'."),
        ("Lexis and Structure", "The comparative form of 'good' is:", "better", ["gooder", "best", "more good"], "'Better' is the comparative of 'good'."),
        ("Lexis and Structure", "The superlative form of 'bad' is:", "worst", ["worser", "baddest", "worse"], "'Worst' is the superlative of 'bad'."),
        ("Lexis and Structure", "Choose the correct question tag: She is a teacher, _____?", "isn't she", ["is she", "doesn't she", "aren't she"], "A positive statement takes a negative tag."),
        ("Lexis and Structure", "Choose the correct question tag: They are not late, _____?", "are they", ["aren't they", "are they not", "is they"], "A negative statement takes a positive tag."),
        ("Lexis and Structure", "The passive form of 'The boy kicked the ball' is:", "The ball was kicked by the boy", ["The ball is kicked by the boy", "The boy was kicked by the ball", "The ball kicked the boy"], "Past simple passive: was + past participle."),
        ("Lexis and Structure", "The active form of 'The letter was written by Ada' is:", "Ada wrote the letter", ["Ada writes the letter", "The letter wrote Ada", "Ada is writing the letter"], "Active: subject + past tense verb + object."),
        ("Lexis and Structure", "He said, 'I am hungry.' The reported speech is: He said that he _____ hungry.", "was", ["is", "are", "were"], "In reported speech the present tense shifts to the past."),
        ("Lexis and Structure", "A word that describes a noun is a/an:", "adjective", ["adverb", "verb", "pronoun"], "Adjectives describe nouns."),
        ("Lexis and Structure", "A word that describes a verb is a/an:", "adverb", ["adjective", "noun", "pronoun"], "Adverbs describe verbs, adjectives or other adverbs."),
        ("Lexis and Structure", "The word 'quickly' is a/an:", "adverb", ["adjective", "noun", "verb"], "'Quickly' describes how an action is done."),
        ("Lexis and Structure", "The word 'happiness' is a/an:", "noun", ["verb", "adjective", "adverb"], "'Happiness' names a thing (a state)."),
        ("Lexis and Structure", "Which sentence is correctly punctuated?", "Ada, who is my friend, came yesterday.", ["Ada who is my friend came yesterday", "Ada, who is my friend came yesterday.", "Ada who is my friend, came yesterday."], "The non-defining clause is set off by commas."),
        ("Oral English", "The vowel sound in 'seat' is the same as in:", "feet", ["set", "sit", "sat"], "'Seat' and 'feet' share the /i:/ sound."),
        ("Oral English", "The vowel sound in 'cat' is the same as in:", "hat", ["cart", "cut", "cot"], "'Cat' and 'hat' share the /ae/ sound."),
        ("Oral English", "Which word has a different vowel sound: bat, cat, hat, ball?", "ball", ["bat", "cat", "hat"], "Bat, cat and hat have /ae/; ball has /o:/."),
        ("Oral English", "The word 'photograph' is stressed on the:", "first syllable", ["second syllable", "third syllable", "last syllable"], "PHO-to-graph: stress on the first syllable."),
        ("Oral English", "The word 'important' is stressed on the:", "second syllable", ["first syllable", "third syllable", "last syllable"], "im-POR-tant: stress on the second syllable."),
        ("Oral English", "Words that sound alike but have different meanings are:", "homophones", ["synonyms", "antonyms", "homographs"], "Homophones sound the same, e.g. 'sea' and 'see'."),
        ("Oral English", "The pair 'right' and 'write' are:", "homophones", ["synonyms", "antonyms", "homonyms"], "They sound the same but are spelt differently."),
    ]
    for t, q, c, d, e in grammar:
        add(t, q, c, d, e)
    add("Comprehension", "A summary should be written:", "in the writer's own words, briefly",
        ["by copying the passage", "at the same length", "with new ideas"],
        "A summary condenses the passage in your own words.")
    return P

# ---------------- HAUSA ----------------
HAUSA_VOCAB = [("water","ruwa"),("house","gida"),("food","abinci"),("book","littafi"),("school","makaranta"),
    ("teacher","malam"),("money","kudi"),("car","mota"),("road","hanya"),("sun","rana"),("moon","wata"),
    ("night","dare"),("morning","safe"),("dog","kare"),("cat","mage"),("fish","kifi"),("bird","tsuntsu"),
    ("tree","itace"),("stone","dutse"),("fire","wuta"),("land","kasa"),("sky","sama"),("head","kai"),
    ("eye","ido"),("leg","kafa"),("mouth","baki"),("nose","hanci"),("ear","kunne"),("tooth","hakori"),
    ("tongue","harshe"),("heart","zuciya"),("blood","jini"),("mother","uwa"),("father","uba"),
    ("friend","aboki"),("child","yaro"),("man","namiji"),("woman","mace"),("king","sarki"),
    ("market","kasuwa"),("farm","gona"),("river","kogi"),("rice","shinkafa"),("yam","doya"),
    ("cassava","rogo"),("maize","masara"),("beans","wake"),("meat","nama"),("milk","nono"),
    ("bread","burodi"),("salt","gishiri"),("sugar","sukari"),("oil","mai"),("egg","kwai"),
    ("cloth","tufafi"),("shoe","takalmi"),("shirt","riga"),("trousers","wando"),("cap","hula"),
    ("window","taga"),("chair","kujera"),("table","tebur"),("bed","gado"),("room","daki"),
    ("village","kauye"),("town","gari"),("rain","ruwan sama"),("horse","doki"),("goat","akuya"),
    ("cow","saniya"),("sheep","tunkiya"),("chicken","kaza"),("lion","zaki"),("snake","maciji")]
HAUSA_NUMBERS = [("one","daya"),("two","biyu"),("three","uku"),("four","hudu"),("five","biyar"),
    ("six","shida"),("seven","bakwai"),("eight","takwas"),("nine","tara"),("ten","goma"),
    ("twenty","ashirin"),("thirty","talatin"),("forty","arba'in"),("fifty","hamsin"),("hundred","dari")]

def hausa_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Hausa", t, q, c, d, e))
    for eng, hau in HAUSA_VOCAB:
        others = [h for e, h in HAUSA_VOCAB if h != hau][:3]
        add("Kalmomi (Vocabulary)", f"Menene '{eng}' a Hausa?", hau, others, f"'{eng}' a Hausa shi ne '{hau}'.")
        others2 = [e for e, h in HAUSA_VOCAB if e != eng][:3]
        add("Kalmomi (Vocabulary)", f"Menene ma'anar '{hau}' a Turanci?", eng, others2, f"'{hau}' a Turanci shi ne '{eng}'.")
    for eng, hau in HAUSA_NUMBERS:
        others = [h for e, h in HAUSA_NUMBERS if h != hau][:3]
        add("Lambobi (Numbers)", f"Menene '{eng}' a Hausa?", hau, others, f"'{eng}' a Hausa shi ne '{hau}'.")
    greet = [("Sannu", "hello"), ("Na gode", "thank you"), ("Don Allah", "please"),
             ("Yi hakuri", "sorry / excuse me"), ("Sai anjima", "see you later"),
             ("Ina kwana", "good morning"), ("Barka da rana", "good afternoon"), ("Lafiya", "peace / good health")]
    for hau, eng in greet:
        others = [e for h, e in greet if e != eng][:3]
        add("Gaisuwa (Greetings)", f"Menene ma'anar '{hau}'?", eng, others, f"'{hau}' na nufin '{eng}'.")
    plurals = [("doki","dokuna"),("gida","gidaje"),("littafi","littattafai"),("yaro","yara"),
               ("kare","karnuka"),("mota","motoci"),("hanya","hanyoyi"),("riga","riguna"),
               ("kujera","kujeru"),("tebur","tebura")]
    for sing, plu in plurals:
        others = [p for s, p in plurals if p != plu][:3]
        add("Nahawu (Grammar)", f"Menene jam'in '{sing}'?", plu, others, f"Jam'in '{sing}' shi ne '{plu}'.")
    add("Nahawu (Grammar)", "Menene 'Noun' a Hausa?", "Suna", ["Aikatau", "Sifa", "Bayanau"], "'Noun' a Hausa shi ne 'Suna'.")
    add("Nahawu (Grammar)", "Menene 'Verb' a Hausa?", "Aikatau", ["Suna", "Sifa", "Bayanau"], "'Verb' a Hausa shi ne 'Aikatau'.")
    add("Nahawu (Grammar)", "Menene 'Adjective' a Hausa?", "Sifa", ["Suna", "Aikatau", "Bayanau"], "'Adjective' a Hausa shi ne 'Sifa'.")
    add("Adabi (Literature)", "Wanene ya rubuta 'Magana Jari Ce'?", "Abubakar Imam", ["Aminu Kano", "Balewa", "Ekwensi"], "'Magana Jari Ce' ta Abubakar Imam ce.")
    add("Adabi (Literature)", "Wanene ya rubuta 'Ruwan Bagaja'?", "Abubakar Imam", ["Aminu Kano", "Wole Soyinka", "Chinua Achebe"], "'Ruwan Bagaja' ta Abubakar Imam ce.")
    add("Al'ada (Culture)", "Sarkin Musulmi yana zaune a:", "Sokoto", ["Kano", "Zaria", "Kaduna"], "Sarkin Musulmi yana Sokoto.")
    add("Al'ada (Culture)", "Babban birnin Kano na da tarihi a matsayin cibiyar:", "kasuwanci", ["noma kadai", "kamun kifi", "ma'adinai"], "Kano cibiyar kasuwanci ce ta tarihi.")
    add("Karin Magana (Proverbs)", "Karin magana 'Magana jari ce' na nufin:", "magana tana da amfani kamar jari", ["magana ba ta da amfani", "kudi ne kawai", "shiru ya fi magana"], "'Magana jari ce' na nufin magana tana da amfani.")
    add("Nahawu (Grammar)", "Wane ne sarki a Hausa?", "Sarki", ["Sarauniya", "Yaro", "Malam"], "Sarki shi ne mai mulki.")
    add("Nahawu (Grammar)", "Menene 'Hello' a Hausa?", "Sannu", ["Na gode", "Sai anjima", "Don Allah"], "'Hello' a Hausa shi ne 'Sannu'.")
    return P

# ---------------- IGBO ----------------
IGBO_VOCAB = [("water","mmiri"),("house","ulo"),("food","nri"),("book","akwukwo"),("school","ulo akwukwo"),
    ("teacher","onye nkuzi"),("money","ego"),("car","ugboala"),("road","uzo"),("sun","anyanwu"),("moon","onwa"),
    ("night","abali"),("morning","ututu"),("dog","nkita"),("cat","nwamba"),("fish","azu"),("bird","nnunu"),
    ("tree","osisi"),("stone","nkume"),("fire","oku"),("land","ala"),("sky","igwe"),("head","isi"),
    ("eye","anya"),("leg","ukwu"),("mouth","onu"),("nose","imi"),("ear","nti"),
    ("tongue","ire"),("heart","obi"),("blood","obara"),("mother","nne"),("father","nna"),
    ("friend","enyi"),("child","nwa"),("man","nwoke"),("woman","nwanyi"),("king","eze"),
    ("market","ahia"),("farm","ugbo"),("river","osimiri"),("rice","osikapa"),("yam","ji"),
    ("cassava","akpu"),("maize","oka"),("beans","agwa"),("meat","anu"),("milk","mmiri ara ehi"),
    ("bread","achicha"),("salt","nnu"),("sugar","shuga"),("oil","mmanu"),("cloth","uwe"),
    ("shoe","akpukpoukwu"),("cap","okpu"),("chair","oche"),("table","tebulu"),("village","obodo"),
    ("rain","mmiri ozuzo"),("horse","inyinya"),("goat","ewu"),("cow","ehi"),
    ("sheep","aturu"),("chicken","okuko"),("lion","odum"),("snake","agwo"),("egg","akwa")]
IGBO_NUMBERS = [("one","otu"),("two","abuo"),("three","ato"),("four","ano"),("five","ise"),
    ("six","isii"),("seven","asaa"),("eight","asato"),("nine","itoolu"),("ten","iri"),
    ("twenty","iri abuo"),("thirty","iri ato"),("forty","iri ano"),("fifty","iri ise"),("hundred","otu nari")]

def igbo_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Igbo", t, q, c, d, e))
    for eng, ig in IGBO_VOCAB:
        others = [h for e, h in IGBO_VOCAB if h != ig][:3]
        add("Okwu (Vocabulary)", f"G\u1ecbn\u1ecb b\u1ee5 '{eng}' n'as\u1ee5s\u1ee5 Igbo?", ig, others,
            f"'{eng}' n'as\u1ee5s\u1ee5 Igbo b\u1ee5 '{ig}'.")
        others2 = [e for e, h in IGBO_VOCAB if e != eng][:3]
        add("Okwu (Vocabulary)", f"G\u1ecbn\u1ecb b\u1ee5 '{ig}' n'as\u1ee5s\u1ee5 Bekee?", eng, others2,
            f"'{ig}' n'as\u1ee5s\u1ee5 Bekee b\u1ee5 '{eng}'.")
    for eng, ig in IGBO_NUMBERS:
        others = [h for e, h in IGBO_NUMBERS if h != ig][:3]
        add("Onuogugu (Numbers)", f"G\u1ecbn\u1ecb b\u1ee5 '{eng}' n'as\u1ee5s\u1ee5 Igbo?", ig, others,
            f"'{eng}' n'as\u1ee5s\u1ee5 Igbo b\u1ee5 '{ig}'.")
    greet = [("Ndewo", "hello"), ("Daalu", "thank you"), ("Biko", "please"), ("Ndo", "sorry"),
             ("Ututu oma", "good morning"), ("Ehihie oma", "good afternoon"), ("Abali oma", "good night"),
             ("Ka emesia", "see you later")]
    for ig, eng in greet:
        others = [e for h, e in greet if e != eng][:3]
        add("Ekele (Greetings)", f"G\u1ecbn\u1ecb b\u1ee5 '{ig}' n'as\u1ee5s\u1ee5 Bekee?", eng, others,
            f"'{ig}' n'as\u1ee5s\u1ee5 Bekee b\u1ee5 '{eng}'.")
    add("Utoasusu (Grammar)", "G\u1ecbn\u1ecb b\u1ee5 'Noun' n'as\u1ee5s\u1ee5 Igbo?", "Nkeaha",
        ["Ngwaa", "Nkowa", "Nnochiha"], "'Noun' n'as\u1ee5s\u1ee5 Igbo b\u1ee5 'Nkeaha'.")
    add("Utoasusu (Grammar)", "G\u1ecbn\u1ecb b\u1ee5 'Verb' n'as\u1ee5s\u1ee5 Igbo?", "Ngwaa",
        ["Nkeaha", "Nkowa", "Mbukumba"], "'Verb' n'as\u1ee5s\u1ee5 Igbo b\u1ee5 'Ngwaa'.")
    add("Utoasusu (Grammar)", "G\u1ecbn\u1ecb b\u1ee5 otutu nke 'nwa'?", "umuaka", ["umunwoke", "umunwanyi", "umuada"],
        "Otutu nke 'nwa' b\u1ee5 'umuaka' (umuaka = children).")
    add("Akwukwo (Literature)", "Onye dere 'Omenuko'?", "Pita Nwana",
        ["Chinua Achebe", "F.C. Ogbalu", "Tony Ubesie"], "'Omenuko' bu akwukwo Pita Nwana dere.")
    add("Akwukwo (Literature)", "Onye dere 'Things Fall Apart'?", "Chinua Achebe",
        ["Pita Nwana", "Cyprian Ekwensi", "Flora Nwapa"], "'Things Fall Apart' bu akwukwo Chinua Achebe dere.")
    add("Akwukwo (Literature)", "Onye dere 'Efuru'?", "Flora Nwapa",
        ["Chinua Achebe", "Buchi Emecheta", "Pita Nwana"], "'Efuru' bu akwukwo Flora Nwapa dere.")
    add("Omenala (Culture)", "Eze n'ala Igbo bu:", "Igwe/Eze", ["Oba", "Emir", "Obong"],
        "Eze n'ala Igbo bu Igwe ma obu Eze.")
    add("Omenala (Culture)", "Nri kacha ewu ewu n'ala Igbo bu:", "ji (yam)",
        ["osikapa", "oka", "akpu"], "Ji bu nri a ma ama n'ala Igbo.")
    add("Omenala (Culture)", "Iri ji ohuru bu emume nke:", "owuwe ihe ubi (New Yam Festival)",
        ["agbamakwukwo", "olili ozu", "alumin di na nwunye"], "Iri ji ohuru bu emume owuwe ihe ubi.")
    add("Utoasusu (Grammar)", "G\u1ecbn\u1ecb b\u1ee5 'Hello' n'as\u1ee5s\u1ee5 Igbo?", "Ndewo",
        ["Daalu", "Biko", "Ndo"], "'Hello' n'as\u1ee5s\u1ee5 Igbo b\u1ee5 'Ndewo'.")
    return P

# ---------------- YORUBA ----------------
YORUBA_VOCAB = [("water","omi"),("house","ile"),("food","ounje"),("book","iwe"),("school","ile-iwe"),
    ("teacher","oluko"),("money","owo"),("car","moto"),("road","ona"),("sun","oorun"),("moon","osu"),
    ("night","oru"),("morning","owuro"),("dog","aja"),("cat","ologbo"),("fish","eja"),("bird","eye"),
    ("tree","igi"),("stone","okuta"),("fire","ina"),("sky","orun"),("head","ori"),("eye","oju"),
    ("leg","ese"),("mouth","enu"),("nose","imu"),("ear","eti"),("tooth","eyin"),("tongue","ahon"),
    ("heart","okan"),("blood","eje"),("mother","iya"),("father","baba"),("brother","arakunrin"),
    ("sister","arabinrin"),("friend","ore"),("child","omo"),("man","okunrin"),("woman","obinrin"),
    ("king","oba"),("market","oja"),("farm","oko"),("river","odo"),("rice","iresi"),("yam","isu"),
    ("cassava","ege"),("maize","agbado"),("beans","ewa"),("meat","eran"),("milk","wara"),
    ("bread","buredi"),("salt","iyo"),("sugar","suga"),("oil","epo"),("cloth","aso"),
    ("shoe","bata"),("cap","fila"),("door","ilekun"),("window","ferese"),("chair","aga"),
    ("table","tabili"),("bed","ibusun"),("room","yara"),("village","abule"),("town","ilu"),
    ("rain","ojo"),("horse","esin"),("goat","ewure"),("cow","malu"),("sheep","agutan"),
    ("chicken","adie"),("lion","kinniun"),("snake","ejo")]
YORUBA_NUMBERS = [("one","okan"),("two","meji"),("three","meta"),("four","merin"),("five","marun"),
    ("six","mefa"),("seven","meje"),("eight","mejo"),("nine","mesan"),("ten","mewa"),
    ("twenty","ogun"),("thirty","ogbon"),("forty","ogoji"),("fifty","aadota"),("hundred","ogorun")]

def yoruba_pool():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "Yoruba", t, q, c, d, e))
    for eng, yo in YORUBA_VOCAB:
        others = [h for e, h in YORUBA_VOCAB if h != yo][:3]
        add("Oro (Vocabulary)", f"Ki ni '{eng}' ni ede Yoruba?", yo, others,
            f"'{eng}' ni ede Yoruba ni '{yo}'.")
        others2 = [e for e, h in YORUBA_VOCAB if e != eng][:3]
        add("Oro (Vocabulary)", f"Ki ni itumo '{yo}' ni ede Geesi?", eng, others2,
            f"'{yo}' ni ede Geesi ni '{eng}'.")
    for eng, yo in YORUBA_NUMBERS:
        others = [h for e, h in YORUBA_NUMBERS if h != yo][:3]
        add("Nomba (Numbers)", f"Ki ni '{eng}' ni ede Yoruba?", yo, others,
            f"'{eng}' ni ede Yoruba ni '{yo}'.")
    greet = [("Bawo ni", "hello / how are you"), ("E se", "thank you"), ("E jowo", "please"),
             ("E ma binu", "sorry"), ("O daabo", "goodbye"), ("E kaaro", "good morning"),
             ("E kaasan", "good afternoon"), ("E kaale", "good evening")]
    for yo, eng in greet:
        others = [e for h, e in greet if e != eng][:3]
        add("Ikini (Greetings)", f"Ki ni itumo '{yo}' ni ede Geesi?", eng, others,
            f"'{yo}' ni ede Geesi ni '{eng}'.")
    add("Girama (Grammar)", "Ami ohun meloo lo wa ni ede Yoruba?", "Meta",
        ["Meji", "Merin", "Marun"], "Ami ohun meta ni o wa: ami oke, ami isale, ati ami arin.")
    add("Girama (Grammar)", "Ewo ni faweli aranmu?", "an", ["e", "o", "a"], "'an' ni faweli aranmu.")
    add("Girama (Grammar)", "Ki ni oruko oye Oba ilu Oyo?", "Alaafin", ["Ooni", "Awujale", "Olubadan"], "Oba ilu Oyo ni Alaafin.")
    add("Girama (Grammar)", "Ki ni oruko oye Oba ilu Ife?", "Ooni", ["Alaafin", "Awujale", "Olubadan"], "Oba ilu Ife ni Ooni.")
    add("Girama (Grammar)", "Ki ni oruko oye Oba ilu Ijebu?", "Awujale", ["Ooni", "Alaafin", "Olubadan"], "Oba ilu Ijebu ni Awujale.")
    add("Girama (Grammar)", "Ki ni oruko oye Oba ilu Ibadan?", "Olubadan", ["Ooni", "Alaafin", "Awujale"], "Oba ilu Ibadan ni Olubadan.")
    add("Litireso (Literature)", "Ta ni o ko iwe 'O le ku'?", "Kola Akinlade",
        ["Akinwumi Isola", "Adebayo Faleti", "Olatubosun Oladapo"], "'O le ku' ni iwe Kola Akinlade ko.")
    add("Litireso (Literature)", "Ta ni o ko 'Ogbori Elemoso'?", "Akinwumi Isola",
        ["Kola Akinlade", "Adebayo Faleti", "D.O. Fagunwa"], "'Ogbori Elemoso' ni iwe Akinwumi Isola ko.")
    add("Litireso (Literature)", "Ta ni o ko 'Ogboju Ode Ninu Igbo Irunmole'?", "D.O. Fagunwa",
        ["Akinwumi Isola", "Kola Akinlade", "Wole Soyinka"], "'Ogboju Ode Ninu Igbo Irunmole' ni iwe D.O. Fagunwa ko.")
    add("Asa (Culture)", "Ere wo ni o je ere ibile Yoruba?", "Ayo", ["Football", "Tennis", "Golf"], "Ayo ni ere ibile Yoruba.")
    add("Asa (Culture)", "Orisa wo ni o ni ibatan pelu imole ati ojo?", "Sango", ["Ogun", "Osun", "Yemoja"], "Sango ni orisa imole ati ojo.")
    add("Asa (Culture)", "Orisa wo ni o ni ibatan pelu irin?", "Ogun", ["Sango", "Osun", "Yemoja"], "Ogun ni orisa irin.")
    add("Girama (Grammar)", "Ki ni 'Hello' ni ede Yoruba?", "Bawo ni", ["E se", "O daabo", "E jowo"], "'Hello' ni ede Yoruba ni 'Bawo ni'.")
    return P
