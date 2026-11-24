"""Parametric generators: Mathematics, FurtherMath, Physics.
Every answer is computed in code. Topics = WAEC/JAMB syllabus topics (waecsyllabus.com topic lists;
JAMB syllabus PDFs at ibass.jamb.gov.ng)."""
import random, math
from fractions import Fraction as Fr
from core import mk, fmt_num, uniq_pool

def _dist(rng, correct, spread, fmt=fmt_num, lo=None):
    vals = set(); tries = 0
    while len(vals) < 3 and tries < 60:
        tries += 1
        d = correct + rng.choice([-1, 1]) * rng.randint(1, max(1, spread)) * rng.choice([1, 2, 5, 10])
        if lo is not None and d < lo:
            continue
        s = fmt(d)
        if s != fmt(correct) and s not in vals:
            vals.add(s)
    k = 1
    while len(vals) < 3:
        for d in (correct + k, correct - k, correct + 2 * k):
            s = fmt(d)
            if s != fmt(correct) and s not in vals:
                vals.add(s)
            if len(vals) == 3:
                break
        k += 1
    return list(vals)

def _pick(rng, correct, pool):
    seen = set(); ds = []
    for x in pool:
        if x != correct and x not in seen:
            seen.add(x); ds.append(x)
    rng.shuffle(ds)
    return ds[:3]

# ---------------- MATHEMATICS ----------------
def math_pool(year):
    rng = random.Random(f"math-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    for _ in range(14):
        a = rng.randint(2, 9); b = rng.randint(2, 20); x = rng.randint(2, 12)
        c = a * x + b
        add(f"If {a}x + {b} = {c}, find the value of x.", str(x), _dist(rng, x, 3, lo=0),
            f"{a}x = {c} - {b} = {c - b}, so x = {c - b}/{a} = {x}.", "Algebra: linear equations")
    for _ in range(12):
        r1, r2 = rng.sample(range(-6, 7), 2)
        if r1 == 0 or r2 == 0:
            continue
        b = -(r1 + r2); c = r1 * r2
        add(f"Solve the equation x\u00b2 {'+' if b >= 0 else '-'} {abs(b)}x {'+' if c >= 0 else '-'} {abs(c)} = 0.",
            f"x = {r1} or x = {r2}", [f"x = {-r1} or x = {r2}", f"x = {r1} or x = {-r2}", f"x = {-r1} or x = {-r2}"],
            f"Factorising: (x - {r1})(x - {r2}) = 0, so x = {r1} or x = {r2}.", "Algebra: quadratic equations")
    for _ in range(10):
        n = rng.randint(5, 40); base = rng.choice([2, 5, 8])
        s = ""; m = n
        while m > 0:
            s = str(m % base) + s; m //= base
        add(f"Convert {n} to base {base}.", s,
            _pick(rng, s, [str(n + 1), str(n - 1), str(n + 2), str(n * 2), "101", "110", "1001", "111"]),
            f"{n} in base {base} is {s}.", "Number and numeration: number bases")
    for _ in range(10):
        a = rng.randint(2, 9); b = rng.randint(2, 9); m = rng.randint(3, 9)
        v = (a * b) % m
        add(f"Evaluate ({a} \u00d7 {b}) mod {m}.", str(v), _dist(rng, v, 2, lo=0),
            f"{a} \u00d7 {b} = {a * b}; {a * b} \u00f7 {m} leaves remainder {v}.", "Number and numeration: modular arithmetic")
    for _ in range(10):
        a = rng.randint(2, 5); p = rng.randint(2, 4)
        v = a ** p
        add(f"Evaluate {a}^{p}.", str(v), _dist(rng, v, 5, lo=0),
            f"{a}^{p} = {a} \u00d7 " + " \u00d7 ".join([str(a)] * (p - 1)) + f" = {v}.", "Algebra: indices")
    for _ in range(12):
        cp = rng.choice([200, 400, 500, 800, 1000, 1500, 2000, 2500, 4000])
        pct = rng.choice([5, 10, 15, 20, 25, 30])
        sp = cp * (100 + pct) // 100; prof = cp * pct // 100
        add(f"A trader bought an article for \u20a6{cp} and sold it at a profit of {pct}%. Find the selling price.",
            f"\u20a6{sp}", _pick(rng, f"\u20a6{sp}", [f"\u20a6{cp}", f"\u20a6{cp + prof * 2}", f"\u20a6{cp - prof}", f"\u20a6{cp + prof // 2}", f"\u20a6{sp + 100}"]),
            f"Profit = {pct}% of \u20a6{cp} = \u20a6{prof}; selling price = \u20a6{cp} + \u20a6{prof} = \u20a6{sp}.",
            "Financial arithmetic: profit and loss")
    for _ in range(8):
        pr = rng.choice([1000, 2000, 5000, 10000]); r = rng.choice([5, 8, 10, 12]); t = rng.randint(2, 5)
        si = pr * r * t // 100
        add(f"Find the simple interest on \u20a6{pr} at {r}% per annum for {t} years.", f"\u20a6{si}",
            _pick(rng, f"\u20a6{si}", [f"\u20a6{si + 100}", f"\u20a6{si - 100}", f"\u20a6{pr * r // 100}", f"\u20a6{si * 2}", f"\u20a6{si // 2}", f"\u20a6{pr + si}"]),
            f"I = PRT/100 = {pr} \u00d7 {r} \u00d7 {t}/100 = \u20a6{si}.", "Financial arithmetic: simple interest")
    for _ in range(10):
        xs = [rng.randint(1, 20) for _ in range(5)]
        while sum(xs) % 5 != 0:
            xs = [rng.randint(1, 20) for _ in range(5)]
        mean = sum(xs) // 5
        add(f"Find the mean of {', '.join(map(str, xs))}.", str(mean), _dist(rng, mean, 3, lo=0),
            f"Sum = {sum(xs)}; mean = {sum(xs)}/5 = {mean}.", "Statistics: measures of central tendency")
    for _ in range(8):
        u = rng.choice([40, 48, 50, 60]); a = rng.randint(15, 30); b = rng.randint(15, 30)
        inter = rng.randint(5, min(a, b) - 2); union = a + b - inter
        add(f"In a universal set with n(U) = {u}, n(A) = {a}, n(B) = {b} and n(A \u222a B) = {union}, find n(A \u2229 B).",
            str(inter), _dist(rng, inter, 3, lo=0),
            f"n(A \u222a B) = n(A) + n(B) - n(A \u2229 B), so {union} = {a} + {b} - n(A \u2229 B); n(A \u2229 B) = {inter}.", "Sets")
    for _ in range(10):
        a = rng.randint(1, 9); d = rng.randint(2, 6); n = rng.randint(5, 12)
        v = a + (n - 1) * d
        add(f"Find the {n}th term of the arithmetic progression {a}, {a + d}, {a + 2 * d}, ...", str(v),
            _dist(rng, v, 4, lo=0), f"Tn = a + (n-1)d = {a} + {n - 1} \u00d7 {d} = {v}.", "Sequences and series: arithmetic progression")
    for _ in range(8):
        r = rng.choice([7, 14, 21, 28]); area = 22 * r * r // 7
        add(f"Find the area of a circle of radius {r} cm. [Take \u03c0 = 22/7]", f"{area} cm\u00b2",
            [f"{22 * r // 7} cm\u00b2", f"{area + 44} cm\u00b2", f"{area - 22} cm\u00b2"],
            f"Area = \u03c0r\u00b2 = 22/7 \u00d7 {r} \u00d7 {r} = {area} cm\u00b2.", "Mensuration: circles")
    for _ in range(10):
        x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
        x2 = x1 + rng.choice([3, 4, 5]); y2 = y1 + rng.choice([0, 3, 4])
        d = math.hypot(x2 - x1, y2 - y1)
        if d != int(d):
            continue
        add(f"Find the distance between the points ({x1}, {y1}) and ({x2}, {y2}).", f"{int(d)} units",
            [f"{int(d) + 1} units", f"{int(d) + 2} units", f"{int(d) - 1 if d > 1 else 1} units"],
            f"Distance = \u221a[({x2}-{x1})\u00b2 + ({y2}-{y1})\u00b2] = \u221a{int(d * d)} = {int(d)} units.", "Coordinate geometry: distance between points")
    for _ in range(10):
        tot = rng.choice([10, 12, 15, 20]); fav = rng.randint(2, tot - 2)
        f = Fr(fav, tot)
        add(f"A bag contains {tot} balls of which {fav} are red. Find the probability of picking a red ball at random.",
            str(f), _pick(rng, str(f), [str(Fr(fav + 1, tot)), str(Fr(tot - fav, tot)), str(Fr(fav, tot + 5)), str(Fr(1, tot)), str(Fr(fav, tot - 1)), str(Fr(2, tot))]),
            f"Probability = favourable/total = {fav}/{tot} = {f}.", "Probability")
    for _ in range(10):
        x, y = rng.randint(1, 9), rng.randint(1, 9)
        s = x + y; d = x - y
        add(f"If x + y = {s} and x - y = {d}, find the value of x.", str(x), _dist(rng, x, 2, lo=0),
            f"Adding: 2x = {s + d}, so x = {x}.", "Algebra: simultaneous equations")
    for _ in range(8):
        a, b = rng.sample(range(2, 7), 2); tot = rng.choice([300, 400, 500, 600, 900])
        if tot % (a + b):
            continue
        share = tot * a // (a + b)
        correct = f"\u20a6{tot * max(a, b) // (a + b)}" if a < b else f"\u20a6{tot * min(a, b) // (a + b)}"
        add(f"Share \u20a6{tot} in the ratio {a}:{b}. Find the larger share." if a < b else f"Share \u20a6{tot} in the ratio {a}:{b}. Find the smaller share.",
            correct, _pick(rng, correct, [f"\u20a6{share}", f"\u20a6{tot // 2}", f"\u20a6{tot * 2 // (a + b)}", f"\u20a6{tot // (a + b)}", f"\u20a6{tot - share}", f"\u20a6{share + 50}"]),
            f"Total parts = {a + b}; each part = \u20a6{tot // (a + b)}.", "Ratio, proportion and rate")
    for _ in range(8):
        b = rng.choice([2, 3, 5]); e = rng.randint(2, 4); v = b ** e
        add(f"Solve for x: log{v} = {e} (base {b}).", str(v), _dist(rng, v, 4, lo=0),
            f"x = {b}^{e} = {v}.", "Algebra: logarithms")
    for _ in range(8):
        a = rng.randint(2, 9)
        add(f"Simplify \u221a{a * a}.", str(a), _dist(rng, a, 2, lo=0),
            f"\u221a{a * a} = {a} since {a} \u00d7 {a} = {a * a}.", "Number and numeration: surds")
    for _ in range(8):
        k = rng.randint(2, 12); x = rng.randint(2, 6)
        add(f"y varies directly as the square of x. If y = {k} when x = 1, find y when x = {x}.", str(k * x * x),
            _dist(rng, k * x * x, 5, lo=0), f"y = {k}x\u00b2, so when x = {x}, y = {k} \u00d7 {x}\u00b2 = {k * x * x}.", "Algebra: variation")
    for _ in range(8):
        ang = rng.choice([30, 45, 60, 0, 90]); fn = rng.choice(["sin", "cos"])
        table = {"sin": {"30": "1/2", "45": "\u221a2/2", "60": "\u221a3/2", "0": "0", "90": "1"},
                 "cos": {"30": "\u221a3/2", "45": "\u221a2/2", "60": "1/2", "0": "1", "90": "0"}}
        correct = table[fn][str(ang)]
        add(f"Evaluate {fn} {ang}\u00b0.", correct, _pick(rng, correct, ["1/2", "\u221a2/2", "\u221a3/2", "0", "1", "2"]),
            f"{fn} {ang}\u00b0 = {correct} (standard trigonometric ratio).", "Trigonometry")
    for _ in range(8):
        r = rng.choice([7, 14]); h = rng.choice([5, 10, 15]); v = 22 * r * r * h // 7
        add(f"Find the volume of a cylinder of radius {r} cm and height {h} cm. [Take \u03c0 = 22/7]", f"{v} cm\u00b3",
            [f"{v + 154} cm\u00b3", f"{v - 154} cm\u00b3", f"{22 * r * h // 7} cm\u00b3"],
            f"V = \u03c0r\u00b2h = 22/7 \u00d7 {r}\u00b2 \u00d7 {h} = {v} cm\u00b3.", "Mensuration: volumes")
    for _ in range(10):
        a = rng.randint(2, 9); b = a * rng.randint(2, 4)
        h = math.gcd(a, b)
        add(f"Find the highest common factor (HCF) of {a} and {b}.", str(h), _dist(rng, h, 2, lo=1),
            f"The common factors of {a} and {b} are greatest at {h}.", "Number and numeration: HCF and LCM")
    for _ in range(10):
        a = rng.randint(30, 80); b = rng.randint(30, 80)
        while a + b >= 170:
            a = rng.randint(30, 80); b = rng.randint(30, 80)
        c = 180 - a - b
        add(f"Two angles of a triangle are {a}\u00b0 and {b}\u00b0. Find the third angle.", f"{c}\u00b0",
            _dist(rng, c, 5, lo=1), f"Angles in a triangle sum to 180\u00b0: 180 - {a} - {b} = {c}\u00b0.", "Geometry: angles in a triangle")
    for _ in range(10):
        d = rng.choice([120, 150, 180, 240]); t2 = rng.choice([2, 3, 4, 6])
        if d % t2:
            continue
        add(f"A car travels {d} km in {t2} hours. Find its average speed.", f"{d // t2} km/h",
            _dist(rng, d // t2, 5, lo=1), f"Speed = distance/time = {d}/{t2} = {d // t2} km/h.", "Ratio, proportion and rate: speed")
    for _ in range(8):
        a = rng.randint(4, 10); b = rng.randint(4, 10); h = rng.randint(2, 6)
        if (a + b) * h % 2:
            continue
        area = (a + b) * h // 2
        add(f"Find the area of a trapezium with parallel sides {a} cm and {b} cm and height {h} cm.", f"{area} cm\u00b2",
            _pick(rng, f"{area} cm\u00b2", [f"{area + 5} cm\u00b2", f"{a * b} cm\u00b2", f"{area - 5} cm\u00b2", f"{area + 10} cm\u00b2", f"{area - 10} cm\u00b2", f"{a * h} cm\u00b2"]),
            f"Area = \u00bd(a + b)h = \u00bd({a} + {b}) \u00d7 {h} = {area} cm\u00b2.", "Mensuration: areas")
    for _ in range(10):
        n = rng.randint(3, 12)
        if rng.random() < 0.5:
            add(f"Evaluate {n}\u00b2.", str(n * n), _dist(rng, n * n, 5, lo=0),
                f"{n}\u00b2 = {n} \u00d7 {n} = {n * n}.", "Number and numeration: squares and square roots")
        else:
            add(f"Evaluate {n}\u00b3.", str(n ** 3), _dist(rng, n ** 3, 10, lo=0),
                f"{n}\u00b3 = {n} \u00d7 {n} \u00d7 {n} = {n ** 3}.", "Number and numeration: cubes")
    for _ in range(8):
        a = rng.randint(2, 9)
        add(f"Factorise x\u00b2 - {a * a}.", f"(x - {a})(x + {a})",
            [f"(x - {a})(x - {a})", f"(x + {a})(x + {a})", f"x(x - {a * a})"],
            f"x\u00b2 - {a * a} = (x - {a})(x + {a}) by difference of two squares.", "Algebra: factorisation")
    for _ in range(8):
        frac = rng.choice([4, 5, 6, 8, 10]); ang = 360 // frac
        add(f"In a pie chart, a sector represents 1/{frac} of the whole. Find the angle of the sector.", f"{ang}\u00b0",
            _dist(rng, ang, 5, lo=1), f"Angle = (1/{frac}) \u00d7 360\u00b0 = {ang}\u00b0.", "Statistics: pie charts")
    for _ in range(8):
        xs = sorted(rng.sample(range(1, 30), 5)); rg = xs[-1] - xs[0]
        add(f"Find the range of {', '.join(map(str, xs))}.", str(rg), _dist(rng, rg, 3, lo=0),
            f"Range = highest - lowest = {xs[-1]} - {xs[0]} = {rg}.", "Statistics: measures of dispersion")
    for _ in range(8):
        a = rng.randint(1, 4); r = rng.choice([2, 3]); n = rng.randint(3, 5)
        v = a * r ** (n - 1)
        add(f"Find the {n}th term of the geometric progression {a}, {a * r}, {a * r * r}, ...", str(v),
            _dist(rng, v, 5, lo=0), f"Tn = ar^(n-1) = {a} \u00d7 {r}^{n - 1} = {v}.", "Sequences and series: geometric progression")
    for _ in range(8):
        a = rng.randint(2, 6); c = rng.randint(10, 40); b = rng.randint(2, 9)
        y = a * b + c
        add(f"If y = {a}x + {c} and y = {y}, find x.", str(b), _dist(rng, b, 2, lo=0),
            f"{a}x = {y} - {c} = {y - c}, so x = {b}.", "Algebra: change of subject")
    return uniq_pool(P)

# ---------------- FURTHER MATHEMATICS ----------------
def furthermath_pool(year):
    rng = random.Random(f"fm-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    for _ in range(16):
        a = rng.randint(2, 6); n = rng.randint(2, 4); x0 = rng.randint(1, 3)
        v = a * n * x0 ** (n - 1)
        add(f"If f(x) = {a}x^{n}, find f'({x0}).", str(v), _dist(rng, v, 4, lo=0),
            f"f'(x) = {a * n}x^{n - 1}; f'({x0}) = {a * n} \u00d7 {x0}^{n - 1} = {v}.", "Calculus: differentiation")
    for _ in range(12):
        a = rng.randint(2, 5); n = rng.randint(1, 3)
        v = Fr(a, n + 1)
        add(f"Evaluate \u222b\u2080\u00b9 {a}x^{n} dx.", str(v),
            [str(Fr(a + 1, n + 1)), str(Fr(a, n + 2)), str(a)],
            f"\u222b {a}x^{n} dx = {a}x^{n + 1}/{n + 1}; from 0 to 1 this is {a}/{n + 1} = {v}.", "Calculus: integration")
    for _ in range(10):
        k = rng.randint(2, 9)
        add(f"Evaluate lim(x\u21920) sin {k}x / x.", str(k), _dist(rng, k, 2, lo=0),
            f"lim(x\u21920) sin {k}x / x = {k} (standard limit).", "Calculus: limits")
    for _ in range(10):
        n = rng.randint(4, 8); r = rng.randint(2, 3)
        v = math.comb(n, r)
        add(f"Find the coefficient of x^{r} in the binomial expansion of (1 + x)^{n}.", str(v), _dist(rng, v, 5, lo=0),
            f"C({n}, {r}) = {n}!/({r}!{n - r}!) = {v}.", "Algebra: binomial theorem")
    for _ in range(10):
        a = rng.choice([3, 6, 8, 5]); b = rng.choice([4, 8, 6, 12])
        mod = math.hypot(a, b)
        if mod != int(mod):
            continue
        add(f"Find the modulus of {a} + {b}i.", str(int(mod)), _dist(rng, int(mod), 3, lo=0),
            f"|{a} + {b}i| = \u221a({a}\u00b2 + {b}\u00b2) = \u221a{int(mod * mod)} = {int(mod)}.", "Complex numbers")
    for _ in range(12):
        a, b, c, d = [rng.randint(1, 6) for _ in range(4)]
        det = a * d - b * c
        add(f"Find the determinant of the matrix [[{a}, {b}], [{c}, {d}]].", str(det), _dist(rng, det, 4),
            f"det = {a}\u00d7{d} - {b}\u00d7{c} = {a * d} - {b * c} = {det}.", "Matrices")
    for _ in range(10):
        a = rng.choice([3, 6]); b = rng.choice([4, 8])
        mod = int(math.hypot(a, b))
        add(f"Find the magnitude of the vector ({a}, {b}).", str(mod), _dist(rng, mod, 3, lo=0),
            f"|v| = \u221a({a}\u00b2 + {b}\u00b2) = {mod}.", "Vectors")
    for _ in range(10):
        a = rng.randint(1, 4); r = 2; n = rng.randint(3, 5)
        s = a * (r ** n - 1) // (r - 1)
        add(f"Find the sum of the first {n} terms of the geometric progression {a}, {a * 2}, {a * 4}, ...", str(s),
            _dist(rng, s, 5, lo=0), f"S{n} = a(r^n - 1)/(r - 1) = {a}(2^{n} - 1) = {s}.", "Sequences and series: geometric progression")
    for _ in range(8):
        add("Simplify sin\u00b2\u03b8 + cos\u00b2\u03b8.", "1", ["0", "2", "sin 2\u03b8"],
            "The Pythagorean identity: sin\u00b2\u03b8 + cos\u00b2\u03b8 = 1.", "Trigonometry: identities")
    for _ in range(12):
        r1, r2 = rng.sample(range(1, 8), 2)
        ssum = r1 + r2; prod = r1 * r2
        if rng.random() < 0.5:
            add(f"If \u03b1 and \u03b2 are the roots of x\u00b2 - {ssum}x + {prod} = 0, find \u03b1 + \u03b2.", str(ssum),
                _dist(rng, ssum, 3, lo=0), f"For x\u00b2 - Sx + P = 0, sum of roots = S = {ssum}.", "Algebra: roots of equations")
        else:
            add(f"If \u03b1 and \u03b2 are the roots of x\u00b2 - {ssum}x + {prod} = 0, find \u03b1\u03b2.", str(prod),
                _dist(rng, prod, 4, lo=0), f"For x\u00b2 - Sx + P = 0, product of roots = P = {prod}.", "Algebra: roots of equations")
    for _ in range(10):
        a = rng.choice([2, 3, 4]); e = rng.randint(2, 4)
        add(f"Evaluate log_{a} {a ** e}.", str(e), _dist(rng, e, 2, lo=0),
            f"log_{a} {a ** e} = {e} because {a}^{e} = {a ** e}.", "Algebra: logarithms")
    for _ in range(10):
        n = rng.randint(5, 8)
        v = math.perm(n, 2)
        add(f"In how many ways can 2 officers be chosen in order from {n} candidates?", str(v),
            _dist(rng, v, 6, lo=0), f"Permutations: P({n}, 2) = {n}!/{n - 2}! = {v}.", "Probability: permutations")
    for _ in range(10):
        a = rng.randint(1, 5); b = rng.randint(1, 5)
        add(f"If f(x) = x\u00b2 + {a}x + {b}, find f(1).", str(1 + a + b), _dist(rng, 1 + a + b, 3, lo=0),
            f"f(1) = 1 + {a} + {b} = {1 + a + b}.", "Algebra: functions")
    for _ in range(10):
        a = rng.randint(2, 5); x0 = rng.randint(1, 3)
        add(f"Find the gradient of the curve y = {a}x\u00b2 at x = {x0}.", str(2 * a * x0), _dist(rng, 2 * a * x0, 4, lo=0),
            f"dy/dx = {2 * a}x; at x = {x0}, dy/dx = {2 * a} \u00d7 {x0} = {2 * a * x0}.", "Calculus: differentiation")
    return uniq_pool(P)

# ---------------- PHYSICS ----------------
def physics_pool(year):
    rng = random.Random(f"phys-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    facts = [
        ("Which of the following is a fundamental quantity?", "Length", ["Force", "Velocity", "Power"], "Length is one of the seven fundamental quantities in the SI system.", "Fundamental and derived quantities"),
        ("The SI unit of force is the", "Newton", ["Joule", "Watt", "Pascal"], "Force is measured in newtons (N).", "Fundamental and derived quantities"),
        ("The SI unit of energy is the", "Joule", ["Newton", "Watt", "Volt"], "Energy and work are measured in joules (J).", "Work, energy and power"),
        ("Which of the following is a vector quantity?", "Velocity", ["Speed", "Distance", "Mass"], "Velocity has both magnitude and direction, so it is a vector.", "Scalars and vectors"),
        ("Which of the following is a scalar quantity?", "Speed", ["Velocity", "Force", "Acceleration"], "Speed has magnitude only, so it is a scalar.", "Scalars and vectors"),
        ("The instrument used to measure current is the", "Ammeter", ["Voltmeter", "Ohmmeter", "Galvanometer"], "An ammeter measures electric current in amperes.", "Current electricity"),
        ("The instrument used to measure potential difference is the", "Voltmeter", ["Ammeter", "Ohmmeter", "Barometer"], "A voltmeter measures potential difference in volts.", "Current electricity"),
        ("Which of the following is a good conductor of electricity?", "Copper", ["Wood", "Rubber", "Glass"], "Copper has free electrons and conducts electricity well.", "Current electricity"),
        ("The speed of light in a vacuum is approximately", "3.0 \u00d7 10\u2078 m/s", ["3.0 \u00d7 10\u2076 m/s", "3.0 \u00d7 10\u2077 m/s", "3.0 \u00d7 10\u2079 m/s"], "Light travels at about 3.0 \u00d7 10\u2078 m/s in a vacuum.", "Waves: light"),
        ("The SI unit of frequency is the", "Hertz", ["Metre", "Second", "Decibel"], "Frequency is measured in hertz (Hz).", "Waves"),
        ("Sound travels fastest in", "Solids", ["Vacuum", "Gases", "Liquids"], "Particles are closest in solids, so sound travels fastest there.", "Waves: sound"),
        ("Which colour of light has the longest wavelength?", "Red", ["Blue", "Green", "Violet"], "Red light has the longest wavelength in the visible spectrum.", "Waves: light"),
        ("The process by which a liquid changes to vapour at any temperature is", "Evaporation", ["Condensation", "Sublimation", "Fusion"], "Evaporation is the change from liquid to vapour at the surface, at any temperature.", "Heat: change of state"),
        ("The boiling point of pure water at standard atmospheric pressure is", "100\u00b0C", ["90\u00b0C", "80\u00b0C", "120\u00b0C"], "Pure water boils at 100\u00b0C at standard atmospheric pressure.", "Heat"),
        ("Which of these is a renewable source of energy?", "Solar energy", ["Coal", "Petroleum", "Natural gas"], "Solar energy is replenished naturally, unlike fossil fuels.", "Energy"),
        ("The acceleration due to gravity on Earth is approximately", "10 m/s\u00b2", ["1 m/s\u00b2", "5 m/s\u00b2", "100 m/s\u00b2"], "g is approximately 9.8 m/s\u00b2, taken as 10 m/s\u00b2 in school calculations.", "Motion"),
        ("A body at rest has", "Zero velocity", ["Maximum velocity", "Constant acceleration", "Zero mass"], "A body at rest is not moving, so its velocity is zero.", "Motion"),
        ("Which mirror is used as a driving mirror in vehicles?", "Convex mirror", ["Concave mirror", "Plane mirror", "Parabolic mirror"], "A convex mirror gives a wide field of view and diminished images.", "Light: reflection"),
        ("The image formed by a plane mirror is", "Virtual, erect and same size", ["Real, inverted and magnified", "Virtual, inverted and diminished", "Real, erect and same size"], "A plane mirror forms a virtual, erect image the same size as the object.", "Light: reflection"),
        ("Ohm's law states that current is", "Directly proportional to voltage", ["Inversely proportional to voltage", "Independent of voltage", "Equal to voltage"], "V = IR, so at constant resistance current is directly proportional to voltage.", "Current electricity"),
        ("Which of the following is an insulator?", "Rubber", ["Copper", "Aluminium", "Iron"], "Rubber does not conduct electricity.", "Current electricity"),
        ("The SI unit of pressure is the", "Pascal", ["Newton", "Joule", "Watt"], "Pressure is measured in pascals (Pa).", "Fluids at rest: pressure"),
        ("The density of a substance is defined as its", "Mass per unit volume", ["Weight per unit volume", "Mass per unit area", "Volume per unit mass"], "Density = mass/volume.", "Matter: density"),
        ("Which of the following is a derived unit?", "Newton", ["Metre", "Kilogram", "Second"], "The newton is derived from kg\u00b7m/s\u00b2.", "Fundamental and derived quantities"),
        ("The force that opposes motion between two surfaces in contact is", "Friction", ["Tension", "Gravity", "Upthrust"], "Friction opposes relative motion between surfaces.", "Friction"),
        ("The centre of gravity of a uniform rod is at its", "Midpoint", ["End", "Quarter point", "Centre of mass only if loaded"], "For a uniform rod the centre of gravity is at its midpoint.", "Equilibrium"),
        ("Which of these is a magnetic material?", "Iron", ["Copper", "Aluminium", "Wood"], "Iron is ferromagnetic.", "Magnetism"),
        ("The north pole of a magnet repels the", "North pole of another magnet", ["South pole of another magnet", "Iron filings", "Earth's north pole"], "Like poles repel.", "Magnetism"),
        ("In a series circuit, the same quantity flows through all components: it is the", "Current", ["Voltage", "Resistance", "Power"], "In series, current is the same everywhere.", "Current electricity"),
        ("The main function of a fuse in a circuit is to", "Protect the circuit from excess current", ["Increase the voltage", "Store charge", "Reduce resistance"], "A fuse melts and breaks the circuit when current exceeds its rating.", "Current electricity"),
        ("Which of the following waves is electromagnetic?", "X-rays", ["Sound waves", "Water waves", "Seismic waves"], "X-rays are electromagnetic waves; sound and water waves are mechanical.", "Waves"),
        ("The phenomenon of light bending as it passes from one medium to another is", "Refraction", ["Reflection", "Diffraction", "Dispersion"], "Refraction is the bending of light at a boundary between media.", "Light: refraction"),
        ("The splitting of white light into its colours is called", "Dispersion", ["Diffraction", "Interference", "Polarisation"], "Dispersion separates white light into its spectrum.", "Light"),
        ("The SI unit of electric charge is the", "Coulomb", ["Ampere", "Volt", "Ohm"], "Charge is measured in coulombs (C).", "Electrostatics"),
        ("A machine with efficiency less than 100% loses energy mainly as", "Heat", ["Light", "Sound only", "Chemical energy"], "Friction in a machine converts useful energy to heat.", "Machines and efficiency"),
        ("The period of a simple pendulum depends on its", "Length", ["Mass of the bob", "Amplitude", "Material of the bob"], "T = 2\u03c0\u221a(l/g); period depends on length and g, not mass.", "Simple harmonic motion"),
        ("Which of the following is a unit of power?", "Watt", ["Joule", "Newton", "Pascal"], "Power is measured in watts (W).", "Work, energy and power"),
        ("Momentum is defined as", "Mass \u00d7 velocity", ["Mass \u00d7 acceleration", "Force \u00d7 time", "Mass \u00f7 velocity"], "Momentum p = mv.", "Motion: momentum"),
        ("The principle of conservation of energy states that energy", "Cannot be created or destroyed, only transformed", ["Can be created in machines", "Decreases with time", "Is always lost as heat"], "Energy is conserved; it only changes form.", "Work, energy and power"),
        ("Which of the following is a source of e.m.f.?", "A battery", ["A resistor", "A capacitor", "A switch"], "A battery supplies electromotive force.", "Current electricity"),
        ("The image formed in a pinhole camera is", "Inverted", ["Erect", "Virtual", "Magnified only"], "A pinhole camera forms a real inverted image.", "Light"),
        ("A transformer works on the principle of", "Electromagnetic induction", ["Electrolysis", "Thermionic emission", "Photoelectric effect"], "A transformer transfers energy by mutual electromagnetic induction.", "Electromagnetic induction"),
        ("The refractive index of a medium is the ratio of the speed of light in vacuum to its speed in the", "Medium", ["Air", "Glass", "Water"], "n = c/v, where v is the speed in the medium.", "Light: refraction"),
        ("Which gas law relates pressure and volume at constant temperature?", "Boyle's law", ["Charles' law", "Pressure law", "Avogadro's law"], "Boyle's law: P \u221d 1/V at constant temperature.", "Gas laws"),
        ("The temperature at which a gas has zero volume in Charles' law is", "Absolute zero (-273\u00b0C)", ["0\u00b0C", "100\u00b0C", "-100\u00b0C"], "Absolute zero is -273\u00b0C (0 K).", "Gas laws"),
        ("A concave mirror can form a real image when the object is", "Beyond the focal point", ["At the mirror surface", "Between the mirror and the focus only", "At infinity only"], "A concave mirror forms a real image when the object is beyond F.", "Light: reflection"),
        ("The phenomenon of echo is due to", "Reflection of sound", ["Refraction of sound", "Diffraction of sound", "Interference of sound"], "An echo is a reflected sound wave.", "Waves: sound"),
        ("Which of these is a semiconductor?", "Silicon", ["Copper", "Glass", "Iron"], "Silicon is a semiconductor used in electronics.", "Electronics"),
        ("The half-life of a radioactive substance is the time taken for", "Half of the atoms to decay", ["All atoms to decay", "The mass to double", "The activity to double"], "Half-life is the time for half the nuclei to decay.", "Atomic and nuclear physics"),
        ("Alpha particles are", "Helium nuclei", ["Electrons", "Protons", "Neutrons"], "An alpha particle is a helium-4 nucleus.", "Atomic and nuclear physics"),
        ("The SI unit of capacitance is the", "Farad", ["Henry", "Tesla", "Weber"], "Capacitance is measured in farads (F).", "Capacitance"),
        ("Which instrument measures atmospheric pressure?", "Barometer", ["Thermometer", "Hygrometer", "Altimeter"], "A barometer measures atmospheric pressure.", "Fluids at rest: pressure"),
        ("The weight of a body is greatest at the", "Poles of the Earth", ["Equator", "Centre of the Earth", "Moon"], "g is slightly greater at the poles, so weight is greatest there.", "Gravitation"),
        ("A body moving with uniform velocity has", "Zero acceleration", ["Maximum acceleration", "Constant non-zero acceleration", "Increasing velocity"], "Uniform velocity means no change in velocity, so acceleration is zero.", "Motion"),
        ("The unit of moment of a force is the", "Newton-metre", ["Newton per metre", "Joule per second", "Kilogram-metre"], "Moment = force \u00d7 distance, in N\u00b7m.", "Moments"),
    ]
    for q, c, ds, e, t in facts:
        add(q, c, ds, e, t)
    for _ in range(30):
        kind = rng.choice(["v", "F", "W", "KE", "P", "V", "R", "Q", "rho", "p", "f", "I"])
        if kind == "v":
            u = rng.randint(0, 10); a = rng.randint(1, 5); t = rng.randint(2, 6)
            v = u + a * t
            add(f"A car accelerates from {u} m/s at {a} m/s\u00b2 for {t} s. Find its final velocity.", f"{v} m/s",
                _pick(rng, f"{v} m/s", [f"{v + a} m/s", f"{v - a} m/s", f"{u + a} m/s", f"{v + 2 * a} m/s", f"{u} m/s", f"{v + 5} m/s"]), f"v = u + at = {u} + {a} \u00d7 {t} = {v} m/s.", "Motion: equations of motion")
        elif kind == "F":
            m = rng.randint(2, 20); a = rng.randint(2, 10)
            add(f"Find the force needed to accelerate a mass of {m} kg at {a} m/s\u00b2.", f"{m * a} N",
                [f"{m + a} N", f"{m * a + 5} N", f"{m * a - 5} N"], f"F = ma = {m} \u00d7 {a} = {m * a} N.", "Motion: Newton's laws")
        elif kind == "W":
            m = rng.randint(2, 20)
            add(f"Find the weight of a {m} kg mass. [Take g = 10 m/s\u00b2]", f"{m * 10} N",
                [f"{m} N", f"{m * 10 + 10} N", f"{m * 5} N"], f"W = mg = {m} \u00d7 10 = {m * 10} N.", "Mass and weight")
        elif kind == "KE":
            m = rng.choice([2, 4, 5, 10]); v = rng.choice([2, 4, 6, 10])
            ke = m * v * v // 2
            add(f"Find the kinetic energy of a {m} kg body moving at {v} m/s.", f"{ke} J",
                _pick(rng, f"{ke} J", [f"{ke + 10} J", f"{m * v} J", f"{ke - 10} J", f"{ke * 2} J", f"{m * v * v} J"]), f"KE = \u00bdmv\u00b2 = \u00bd \u00d7 {m} \u00d7 {v}\u00b2 = {ke} J.", "Work, energy and power")
        elif kind == "P":
            w = rng.choice([100, 200, 500, 1000]); t = rng.choice([5, 10, 20])
            add(f"Find the power of a machine that does {w} J of work in {t} s.", f"{w // t} W",
                [f"{w // t + 5} W", f"{w * t} W", f"{w // (t + 5)} W"], f"P = W/t = {w}/{t} = {w // t} W.", "Work, energy and power")
        elif kind == "V":
            i = rng.choice([2, 4, 5]); r = rng.choice([3, 5, 10])
            add(f"Find the potential difference across a {r} \u03a9 resistor carrying {i} A.", f"{i * r} V",
                _pick(rng, f"{i * r} V", [f"{i + r} V", f"{i * r + 2} V", f"{i * r - 2} V", f"{r} V"]), f"V = IR = {i} \u00d7 {r} = {i * r} V.", "Current electricity: Ohm's law")
        elif kind == "R":
            v = rng.choice([12, 24, 20]); i = rng.choice([2, 4, 5])
            if v % i:
                continue
            add(f"A {v} V supply drives a current of {i} A through a resistor. Find its resistance.", f"{v // i} \u03a9",
                [f"{v + i} \u03a9", f"{v // i + 1} \u03a9", f"{v * i} \u03a9"], f"R = V/I = {v}/{i} = {v // i} \u03a9.", "Current electricity: Ohm's law")
        elif kind == "Q":
            i = rng.choice([2, 3, 5]); t = rng.choice([10, 20, 30])
            add(f"Find the charge that flows when a current of {i} A flows for {t} s.", f"{i * t} C",
                [f"{i + t} C", f"{i * t + 5} C", f"{i * t - 5} C"], f"Q = It = {i} \u00d7 {t} = {i * t} C.", "Current electricity")
        elif kind == "rho":
            m = rng.choice([20, 40, 50, 100]); v = rng.choice([5, 10, 20])
            if m % v:
                continue
            add(f"Find the density of a body of mass {m} kg and volume {v} m\u00b3.", f"{m // v} kg/m\u00b3",
                [f"{m + v} kg/m\u00b3", f"{m // v + 1} kg/m\u00b3", f"{m * v} kg/m\u00b3"], f"\u03c1 = m/V = {m}/{v} = {m // v} kg/m\u00b3.", "Matter: density")
        elif kind == "p":
            m = rng.randint(2, 10); v = rng.randint(2, 10)
            add(f"Find the momentum of a {m} kg body moving at {v} m/s.", f"{m * v} kg m/s",
                [f"{m + v} kg m/s", f"{m * v + 2} kg m/s", f"{m * v - 2} kg m/s"], f"p = mv = {m} \u00d7 {v} = {m * v} kg m/s.", "Motion: momentum")
        elif kind == "f":
            lam = rng.choice([2, 5, 10]); v = lam * rng.choice([2, 3, 5])
            f = v // lam
            add(f"A wave travels at {v} m/s with wavelength {lam} m. Find its frequency.", f"{f} Hz",
                [f"{f + 1} Hz", f"{f + 2} Hz", f"{v} Hz"], f"v = f\u03bb, so f = v/\u03bb = {v}/{lam} = {f} Hz.", "Waves")
        elif kind == "I":
            p = rng.choice([100, 200, 500]); v = rng.choice([100, 200, 250])
            if p % v:
                continue
            add(f"An appliance rated {p} W is connected to a {v} V supply. Find the current it draws.", f"{p // v} A",
                [f"{p // v + 1} A", f"{p} A", f"{v // 10} A"], f"I = P/V = {p}/{v} = {p // v} A.", "Current electricity: power")
    facts2 = [
        ("The time taken for one complete oscillation is called the", "Period", ["Frequency", "Amplitude", "Wavelength"], "Period is the time for one complete cycle.", "Simple harmonic motion"),
        ("Frequency is the reciprocal of the", "Period", ["Amplitude", "Wavelength", "Velocity"], "f = 1/T.", "Waves"),
        ("The distance between two successive crests of a wave is its", "Wavelength", ["Amplitude", "Frequency", "Period"], "Wavelength is the distance between identical points on successive waves.", "Waves"),
        ("Which of the following is used to measure temperature?", "Thermometer", ["Barometer", "Ammeter", "Hygrometer"], "A thermometer measures temperature.", "Heat: thermometry"),
        ("Heat is transferred through a vacuum by", "Radiation", ["Conduction", "Convection", "Evaporation"], "Radiation needs no medium.", "Heat transfer"),
        ("Heat is transferred through a metal rod mainly by", "Conduction", ["Convection", "Radiation", "Evaporation"], "Conduction transfers heat through solids by particle vibration.", "Heat transfer"),
        ("The sea breeze is caused by", "Convection", ["Conduction", "Radiation", "Reflection"], "Unequal heating of land and sea sets up convection currents.", "Heat transfer"),
        ("The fixed points on the Celsius scale are", "0\u00b0C and 100\u00b0C", ["0\u00b0C and 50\u00b0C", "32\u00b0C and 212\u00b0C", "-273\u00b0C and 0\u00b0C"], "Ice point is 0\u00b0C and steam point is 100\u00b0C.", "Heat: thermometry"),
        ("Which of the following has the highest specific heat capacity?", "Water", ["Iron", "Copper", "Aluminium"], "Water has a specific heat capacity of about 4200 J/kg\u00b7K.", "Heat"),
        ("The process of a solid changing directly to gas is", "Sublimation", ["Evaporation", "Condensation", "Melting"], "Sublimation is solid to gas without melting.", "Heat: change of state"),
        ("A converging lens is", "Thicker in the middle than at the edges", ["Thinner in the middle", "Uniform in thickness", "Always made of glass"], "A convex (converging) lens is thicker at the centre.", "Light: lenses"),
        ("A diverging lens is also called a", "Concave lens", ["Convex lens", "Cylindrical lens", "Plano lens"], "A concave lens diverges parallel rays.", "Light: lenses"),
        ("Short sight (myopia) is corrected with a", "Concave lens", ["Convex lens", "Bifocal lens", "Plane lens"], "A concave lens diverges light so the image forms on the retina.", "Light: the eye"),
        ("Long sight (hypermetropia) is corrected with a", "Convex lens", ["Concave lens", "Cylindrical lens", "Plane lens"], "A convex lens converges light onto the retina.", "Light: the eye"),
        ("The speed of sound in air at room temperature is about", "340 m/s", ["150 m/s", "1500 m/s", "3000 m/s"], "Sound travels at about 340 m/s in air.", "Waves: sound"),
        ("The pitch of a sound depends on its", "Frequency", ["Amplitude", "Wavelength", "Speed"], "Higher frequency gives higher pitch.", "Waves: sound"),
        ("The loudness of a sound depends on its", "Amplitude", ["Frequency", "Wavelength", "Speed"], "Greater amplitude gives louder sound.", "Waves: sound"),
        ("The phenomenon where a wave bends around an obstacle is", "Diffraction", ["Reflection", "Refraction", "Interference"], "Diffraction is the spreading of waves around obstacles.", "Waves"),
        ("The resistance of a wire increases when its", "Length increases", ["Length decreases", "Cross-sectional area increases", "Temperature decreases"], "R = \u03c1l/A: longer wire means more resistance.", "Current electricity: resistance"),
        ("In a parallel circuit, the quantity that is the same across each branch is the", "Voltage", ["Current", "Resistance", "Power"], "In parallel, voltage is the same across branches.", "Current electricity"),
        ("The total resistance of resistors in series is", "The sum of the resistances", ["The product of the resistances", "Less than the smallest resistance", "The reciprocal of the sum"], "R = R1 + R2 + ... in series.", "Current electricity"),
        ("The total resistance of resistors in parallel is", "Less than the smallest resistance", ["The sum of the resistances", "Greater than the largest resistance", "Equal to the largest resistance"], "1/R = 1/R1 + 1/R2 + ..., so total is less than the smallest.", "Current electricity"),
        ("An electric motor converts", "Electrical energy to mechanical energy", ["Mechanical energy to electrical energy", "Chemical energy to heat", "Light to electrical energy"], "A motor converts electrical energy into motion.", "Electromagnetism"),
        ("A generator converts", "Mechanical energy to electrical energy", ["Electrical energy to mechanical energy", "Heat to light", "Chemical energy to sound"], "A generator converts motion into electrical energy.", "Electromagnetism"),
        ("The SI unit of magnetic flux density is the", "Tesla", ["Weber", "Henry", "Ampere"], "Magnetic flux density is measured in tesla (T).", "Magnetism"),
        ("The photoelectric effect is the emission of electrons when", "Light falls on a metal surface", ["A metal is heated", "A metal is cooled", "A current flows"], "Light of sufficient frequency ejects electrons from a metal.", "Atomic physics"),
        ("Cathode rays are streams of", "Electrons", ["Protons", "Neutrons", "Alpha particles"], "Cathode rays are electrons emitted from the cathode.", "Atomic physics"),
        ("The nucleus of an atom contains", "Protons and neutrons", ["Electrons and protons", "Electrons only", "Protons only"], "The nucleus contains protons and neutrons.", "Atomic structure"),
        ("The atomic number of an element is the number of", "Protons", ["Neutrons", "Electrons and neutrons", "Nucleons"], "Atomic number Z equals the number of protons.", "Atomic structure"),
        ("Isotopes of an element have the same number of", "Protons", ["Neutrons", "Nucleons", "Electrons only"], "Isotopes differ in neutron number but have the same protons.", "Atomic structure"),
        ("Beta particles are", "Fast-moving electrons", ["Helium nuclei", "Protons", "Gamma rays"], "Beta radiation consists of high-speed electrons.", "Atomic and nuclear physics"),
        ("Gamma rays are", "Electromagnetic waves", ["Helium nuclei", "Electrons", "Neutrons"], "Gamma rays are high-energy electromagnetic radiation.", "Atomic and nuclear physics"),
        ("Which radiation has the greatest penetrating power?", "Gamma rays", ["Alpha particles", "Beta particles", "Infrared rays"], "Gamma rays penetrate furthest.", "Atomic and nuclear physics"),
        ("Which radiation has the least penetrating power?", "Alpha particles", ["Beta particles", "Gamma rays", "X-rays"], "Alpha particles are stopped by paper.", "Atomic and nuclear physics"),
        ("Nuclear fission is the splitting of a", "Heavy nucleus", ["Light nucleus", "Atom into electrons", "Molecule"], "Fission splits a heavy nucleus into lighter ones.", "Atomic and nuclear physics"),
        ("Nuclear fusion is the joining of", "Light nuclei", ["Heavy nuclei", "Atoms and molecules", "Electrons and protons"], "Fusion joins light nuclei, as in the Sun.", "Atomic and nuclear physics"),
        ("The main energy source of the Sun is", "Nuclear fusion", ["Nuclear fission", "Chemical burning", "Gravitational collapse"], "The Sun's energy comes from hydrogen fusion.", "Atomic and nuclear physics"),
        ("A semiconductor diode allows current to flow", "In one direction only", ["In both directions equally", "Only at high voltage", "Only in alternating current"], "A diode conducts in the forward direction only.", "Electronics"),
        ("The device used to step up or step down alternating voltage is the", "Transformer", ["Rectifier", "Capacitor", "Inductor"], "A transformer changes AC voltage levels.", "Electromagnetic induction"),
        ("One kilowatt-hour is equal to", "3.6 \u00d7 10\u2076 J", ["3.6 \u00d7 10\u00b3 J", "1000 J", "360 J"], "1 kWh = 1000 W \u00d7 3600 s = 3.6 \u00d7 10\u2076 J.", "Current electricity: power"),
        ("The centre of gravity of a body is the point where", "Its whole weight acts", ["Its mass is zero", "It balances on a knife edge only", "Friction acts"], "Weight is taken to act at the centre of gravity.", "Equilibrium"),
        ("The principle of moments states that for a body in equilibrium, the sum of clockwise moments equals the", "Sum of anticlockwise moments", ["Total force", "Total weight", "Sum of masses"], "Clockwise moments = anticlockwise moments in equilibrium.", "Moments"),
        ("Hooke's law states that extension is proportional to the", "Applied force", ["Mass of the spring", "Length of the spring", "Temperature"], "F = kx: extension is proportional to force within the elastic limit.", "Elasticity"),
        ("Potential energy of a body depends on its", "Height above a reference level", ["Speed", "Temperature", "Volume"], "PE = mgh depends on height.", "Work, energy and power"),
        ("The angle of incidence equals the angle of reflection. This is the law of", "Reflection", ["Refraction", "Dispersion", "Diffraction"], "The first law of reflection states the angles are equal.", "Light: reflection"),
        ("Total internal reflection occurs when light travels from a", "Denser to a less dense medium", ["Less dense to a denser medium", "Vacuum to air", "Glass to water only"], "Total internal reflection needs denser to rarer medium beyond the critical angle.", "Light: refraction"),
        ("The critical angle is the angle of incidence in the denser medium for which the angle of refraction is", "90\u00b0", ["0\u00b0", "45\u00b0", "180\u00b0"], "At the critical angle the refracted ray grazes the boundary at 90\u00b0.", "Light: refraction"),
        ("An optical fibre works on the principle of", "Total internal reflection", ["Refraction only", "Dispersion", "Interference"], "Light is guided along a fibre by total internal reflection.", "Light: refraction"),
        ("Which of the following is a luminous body?", "The Sun", ["The Moon", "A mirror", "A book"], "The Sun produces its own light; the Moon only reflects it.", "Light"),
        ("A voltmeter is connected in a circuit in", "Parallel", ["Series", "Either way", "Across the battery only"], "A voltmeter is connected across (in parallel with) a component.", "Current electricity"),
        ("An ammeter is connected in a circuit in", "Series", ["Parallel", "Either way", "Across the battery only"], "An ammeter is connected in series with the circuit.", "Current electricity"),
        ("The colour of light with the shortest wavelength in the visible spectrum is", "Violet", ["Red", "Yellow", "Green"], "Violet has the shortest visible wavelength.", "Waves: light"),
        ("The speed of a wave is the product of its frequency and its", "Wavelength", ["Amplitude", "Period", "Energy"], "v = f\u03bb.", "Waves"),
        ("A wave in which particles vibrate parallel to the direction of travel is a", "Longitudinal wave", ["Transverse wave", "Electromagnetic wave", "Standing wave"], "In a longitudinal wave, vibration is along the direction of travel.", "Waves"),
        ("Sound is an example of a", "Longitudinal wave", ["Transverse wave", "Electromagnetic wave", "Surface wave"], "Sound travels as a longitudinal wave.", "Waves: sound"),
        ("Light is an example of a", "Transverse wave", ["Longitudinal wave", "Sound wave", "Pressure wave"], "Light is a transverse electromagnetic wave.", "Waves: light"),
    ]
    for q, c, ds, e, t2 in facts2:
        add(q, c, ds, e, t2)
    for _ in range(30):
        kind = rng.choice(["s", "work", "pe", "eff", "press", "series", "parallel", "heat", "T", "hooke"])
        if kind == "s":
            u = rng.randint(0, 5); a = rng.randint(1, 4); t3 = rng.randint(2, 5)
            s = u * t3 + a * t3 * t3 // 2
            add(f"A body starts with velocity {u} m/s and accelerates at {a} m/s\u00b2 for {t3} s. Find the distance covered.", f"{s} m",
                _pick(rng, f"{s} m", [f"{s + 5} m", f"{u * t3} m", f"{s - 5} m", f"{a * t3} m"]), f"s = ut + \u00bdat\u00b2 = {u}\u00d7{t3} + \u00bd\u00d7{a}\u00d7{t3}\u00b2 = {s} m.", "Motion: equations of motion")
        elif kind == "work":
            f = rng.choice([10, 20, 25, 50]); d = rng.choice([2, 4, 5, 10])
            add(f"Find the work done when a force of {f} N moves a body {d} m in the direction of the force.", f"{f * d} J",
                _pick(rng, f"{f * d} J", [f"{f + d} J", f"{f * d + 10} J", f"{f * d - 10} J"]), f"W = Fd = {f} \u00d7 {d} = {f * d} J.", "Work, energy and power")
        elif kind == "pe":
            m = rng.choice([2, 5, 10]); h = rng.choice([2, 5, 10])
            add(f"Find the potential energy of a {m} kg body at a height of {h} m above the ground. [Take g = 10 m/s\u00b2]", f"{m * 10 * h} J",
                _pick(rng, f"{m * 10 * h} J", [f"{m * h} J", f"{m * 10 * h + 50} J", f"{m * 10} J"]), f"PE = mgh = {m} \u00d7 10 \u00d7 {h} = {m * 10 * h} J.", "Work, energy and power")
        elif kind == "eff":
            out = rng.choice([80, 100, 150, 200]); inp = out + rng.choice([20, 50, 100])
            if out * 100 % inp:
                continue
            eff = out * 100 // inp
            add(f"A machine does {out} J of useful work from {inp} J of input energy. Find its efficiency.", f"{eff}%",
                _pick(rng, f"{eff}%", [f"{eff + 5}%", f"{100 - eff}%", f"{eff - 5}%"]), f"Efficiency = (useful output/input) \u00d7 100% = {out}/{inp} \u00d7 100% = {eff}%.", "Machines and efficiency")
        elif kind == "press":
            f = rng.choice([100, 200, 400]); a = rng.choice([2, 4, 5, 10])
            if f % a:
                continue
            add(f"Find the pressure exerted by a force of {f} N on an area of {a} m\u00b2.", f"{f // a} Pa",
                _pick(rng, f"{f // a} Pa", [f"{f * a} Pa", f"{f // a + 5} Pa", f"{a} Pa"]), f"P = F/A = {f}/{a} = {f // a} Pa.", "Fluids at rest: pressure")
        elif kind == "series":
            r1 = rng.choice([2, 3, 4, 5]); r2 = rng.choice([2, 3, 4, 5])
            add(f"Two resistors of {r1} \u03a9 and {r2} \u03a9 are connected in series. Find the total resistance.", f"{r1 + r2} \u03a9",
                _pick(rng, f"{r1 + r2} \u03a9", [f"{r1 * r2} \u03a9", f"{abs(r1 - r2)} \u03a9", f"{r1 + r2 + 1} \u03a9"]), f"In series R = R1 + R2 = {r1} + {r2} = {r1 + r2} \u03a9.", "Current electricity")
        elif kind == "parallel":
            r1 = rng.choice([4, 6]); r2 = rng.choice([4, 6, 12])
            tot = Fr(1, 1) / (Fr(1, r1) + Fr(1, r2))
            add(f"Two resistors of {r1} \u03a9 and {r2} \u03a9 are connected in parallel. Find the total resistance.", f"{tot} \u03a9",
                _pick(rng, f"{tot} \u03a9", [f"{r1 + r2} \u03a9", f"{r1 * r2} \u03a9", f"{max(r1, r2)} \u03a9"]), f"1/R = 1/{r1} + 1/{r2}, so R = {tot} \u03a9.", "Current electricity")
        elif kind == "heat":
            m = rng.choice([2, 4, 5]); dt = rng.choice([5, 10, 20])
            q = m * 4200 * dt
            add(f"Find the heat required to raise {m} kg of water by {dt}\u00b0C. [Specific heat capacity of water = 4200 J/kg\u00b7K]", f"{q} J",
                _pick(rng, f"{q} J", [f"{q + 1000} J", f"{m * dt} J", f"{q // 2} J"]), f"Q = mc\u0394T = {m} \u00d7 4200 \u00d7 {dt} = {q} J.", "Heat: specific heat capacity")
        elif kind == "T":
            f = rng.choice([2, 5, 10, 20])
            add(f"A wave has frequency {f} Hz. Find its period.", f"{Fr(1, f)} s",
                _pick(rng, f"{Fr(1, f)} s", [f"{f} s", f"{Fr(1, f + 1)} s", f"{Fr(2, f)} s"]), f"T = 1/f = 1/{f} = {Fr(1, f)} s.", "Waves")
        elif kind == "hooke":
            k = rng.choice([10, 20, 25, 50]); x = rng.choice([2, 4, 5])
            add(f"A spring of force constant {k} N/m is extended by {x} cm. Find the force applied. [Use x in metres: {x} cm = {x / 100} m]",
                f"{k * x / 100} N",
                _pick(rng, f"{k * x / 100} N", [f"{k * x} N", f"{k + x} N", f"{k * x / 10} N"]), f"F = kx = {k} \u00d7 {x / 100} = {k * x / 100} N.", "Elasticity: Hooke's law")
    return uniq_pool(P)
