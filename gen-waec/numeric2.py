"""Chemistry, Accounting pools. Topics = WAEC syllabus (waecsyllabus.com) + JAMB syllabus (ibass.jamb.gov.ng)."""
import random
from fractions import Fraction as Fr
from core import mk, fmt_num, uniq_pool
from numeric import _dist, _pick

def chemistry_pool(year):
    rng = random.Random(f"chem-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    facts = [
        ("Which of the following is a physical change?", "Melting of ice", ["Burning of wood", "Rusting of iron", "Souring of milk"], "Melting is reversible and forms no new substance.", "Introduction to chemistry: physical and chemical changes"),
        ("Which of the following is a chemical change?", "Rusting of iron", ["Melting of ice", "Dissolving salt in water", "Boiling of water"], "Rusting forms a new substance, iron(III) oxide.", "Introduction to chemistry: physical and chemical changes"),
        ("The number of protons in the nucleus of an atom is its", "Atomic number", ["Mass number", "Nucleon number", "Isotopic number"], "Atomic number Z equals the number of protons.", "Structure of the atom"),
        ("The sum of protons and neutrons in an atom is its", "Mass number", ["Atomic number", "Charge number", "Valency"], "Mass number A = protons + neutrons.", "Structure of the atom"),
        ("Atoms of the same element with different mass numbers are called", "Isotopes", ["Isomers", "Allotropes", "Isobars"], "Isotopes have the same protons but different neutrons.", "Structure of the atom"),
        ("The chemical symbol for sodium is", "Na", ["So", "Sd", "N"], "Sodium comes from Latin 'natrium', symbol Na.", "Periodic chemistry"),
        ("The chemical symbol for iron is", "Fe", ["Ir", "I", "Fn"], "Iron comes from Latin 'ferrum', symbol Fe.", "Periodic chemistry"),
        ("The chemical symbol for potassium is", "K", ["P", "Po", "Pt"], "Potassium comes from Latin 'kalium', symbol K.", "Periodic chemistry"),
        ("Which of the following is a noble gas?", "Argon", ["Oxygen", "Nitrogen", "Chlorine"], "Argon is in Group 0, the noble gases.", "Periodic chemistry"),
        ("The gas used in the manufacture of ammonia by the Haber process is", "Nitrogen and hydrogen", ["Oxygen and hydrogen", "Nitrogen and oxygen", "Carbon dioxide and hydrogen"], "Ammonia is made from nitrogen and hydrogen.", "Chemical industries"),
        ("The best method of separating a mixture of sand and water is", "Filtration", ["Distillation", "Evaporation", "Sublimation"], "Sand is insoluble, so filtration separates it from water.", "Separation techniques"),
        ("The best method of obtaining pure water from sea water is", "Distillation", ["Filtration", "Decantation", "Evaporation to dryness"], "Distillation boils off water and condenses the vapour, leaving salts behind.", "Separation techniques"),
        ("The separation of a mixture of liquids with different boiling points is done by", "Fractional distillation", ["Filtration", "Sublimation", "Chromatography"], "Fractional distillation separates liquids by boiling point.", "Separation techniques"),
        ("Which of the following is an example of a mixture?", "Air", ["Water", "Common salt", "Iron"], "Air is a mixture of gases.", "Elements, compounds and mixtures"),
        ("The pH of a neutral solution at 25\u00b0C is", "7", ["0", "14", "1"], "Neutral solutions have pH 7 at 25\u00b0C.", "Acids, bases and salts"),
        ("The pH of an acidic solution is", "Less than 7", ["Greater than 7", "Equal to 7", "Equal to 14"], "Acids have pH below 7.", "Acids, bases and salts"),
        ("Which of the following is a strong acid?", "Hydrochloric acid", ["Ethanoic acid", "Carbonic acid", "Citric acid"], "Hydrochloric acid ionises completely in water.", "Acids, bases and salts"),
        ("Which of the following is a base?", "Sodium hydroxide", ["Hydrochloric acid", "Sodium chloride", "Sulphur dioxide"], "Sodium hydroxide is an alkali, a soluble base.", "Acids, bases and salts"),
        ("The salt formed when hydrochloric acid reacts with sodium hydroxide is", "Sodium chloride", ["Sodium sulphate", "Sodium nitrate", "Sodium carbonate"], "HCl + NaOH \u2192 NaCl + H2O.", "Acids, bases and salts"),
        ("The gas released when dilute hydrochloric acid reacts with zinc is", "Hydrogen", ["Oxygen", "Carbon dioxide", "Chlorine"], "Zn + 2HCl \u2192 ZnCl2 + H2.", "Chemical reactions"),
        ("The gas released when dilute hydrochloric acid reacts with calcium carbonate is", "Carbon dioxide", ["Hydrogen", "Oxygen", "Nitrogen"], "CaCO3 + 2HCl \u2192 CaCl2 + H2O + CO2.", "Chemical reactions"),
        ("Which gas turns limewater milky?", "Carbon dioxide", ["Oxygen", "Hydrogen", "Nitrogen"], "CO2 reacts with limewater to form white calcium carbonate.", "Chemical reactions"),
        ("The common name for sodium hydroxide is", "Caustic soda", ["Washing soda", "Baking soda", "Slaked lime"], "Sodium hydroxide is caustic soda.", "Acids, bases and salts"),
        ("The common name for sodium carbonate is", "Washing soda", ["Caustic soda", "Baking soda", "Quicklime"], "Sodium carbonate is washing soda.", "Acids, bases and salts"),
        ("The chemical formula of common salt is", "NaCl", ["KCl", "NaOH", "HCl"], "Common salt is sodium chloride, NaCl.", "Chemical formulae"),
        ("The chemical formula of water is", "H2O", ["CO2", "H2O2", "O2"], "A water molecule has two hydrogen atoms and one oxygen atom.", "Chemical formulae"),
        ("The chemical formula of carbon dioxide is", "CO2", ["CO", "C2O", "CO3"], "Carbon dioxide is CO2.", "Chemical formulae"),
        ("The chemical formula of sulphuric acid is", "H2SO4", ["HCl", "HNO3", "H2SO3"], "Sulphuric acid is H2SO4.", "Chemical formulae"),
        ("The oxidation number of oxygen in most compounds is", "-2", ["-1", "+2", "0"], "Oxygen usually has oxidation number -2.", "Redox reactions"),
        ("The oxidation number of hydrogen in most compounds is", "+1", ["-1", "+2", "0"], "Hydrogen usually has oxidation number +1.", "Redox reactions"),
        ("Which of the following is a reducing agent?", "Carbon monoxide", ["Oxygen", "Chlorine", "Concentrated sulphuric acid"], "Carbon monoxide reduces metal oxides, being itself oxidised.", "Redox reactions"),
        ("Electrolysis of brine produces", "Chlorine, hydrogen and sodium hydroxide", ["Oxygen and hydrogen only", "Sodium and chlorine only", "Hydrogen and oxygen only"], "Brine electrolysis gives Cl2, H2 and NaOH.", "Electrolysis"),
        ("The gas liberated at the anode during the electrolysis of dilute sulphuric acid is", "Oxygen", ["Hydrogen", "Chlorine", "Sulphur dioxide"], "At the anode, hydroxide ions discharge to give oxygen.", "Electrolysis"),
        ("The cathode in an electrolytic cell is the", "Negative electrode", ["Positive electrode", "Neutral electrode", "Salt bridge"], "The cathode is negative in electrolysis.", "Electrolysis"),
        ("Which of the following is a covalent compound?", "Carbon dioxide", ["Sodium chloride", "Magnesium oxide", "Potassium bromide"], "CO2 is formed by sharing electrons.", "Chemical bonds"),
        ("Which of the following is an ionic compound?", "Sodium chloride", ["Carbon dioxide", "Water", "Methane"], "NaCl is held by electrostatic attraction between ions.", "Chemical bonds"),
        ("Diamond is hard because its carbon atoms are", "Held in a strong three-dimensional covalent network", ["Held by weak van der Waals forces", "Held by metallic bonds", "Arranged in layers"], "Diamond is held in a giant covalent structure.", "Chemical bonds"),
        ("Graphite conducts electricity because it has", "Delocalised electrons between its layers", ["Free ions", "Metallic bonds", "Hydrogen bonds"], "Delocalised electrons move between graphite layers.", "Chemical bonds"),
        ("The first element in the periodic table is", "Hydrogen", ["Helium", "Lithium", "Oxygen"], "Hydrogen has atomic number 1.", "Periodic chemistry"),
        ("Elements in the same group of the periodic table have the same number of", "Valence electrons", ["Protons", "Neutrons", "Electron shells"], "Group number reflects the number of outer-shell electrons.", "Periodic chemistry"),
        ("Elements in the same period have the same number of", "Electron shells", ["Valence electrons", "Protons", "Neutrons"], "Period number reflects the number of electron shells.", "Periodic chemistry"),
        ("Which of the following is a transition metal?", "Iron", ["Sodium", "Calcium", "Aluminium"], "Iron is a transition metal.", "Periodic chemistry"),
        ("The most reactive metal in the reactivity series is", "Potassium", ["Sodium", "Calcium", "Zinc"], "Potassium is the most reactive common metal.", "Metals and reactivity"),
        ("Which metal is extracted by electrolysis of its molten ore?", "Aluminium", ["Iron", "Zinc", "Copper"], "Aluminium is extracted by electrolysis of bauxite.", "Metals and reactivity"),
        ("Rusting of iron is prevented by", "Galvanising", ["Heating", "Cooling", "Adding water"], "Galvanising coats iron with zinc, preventing rust.", "Metals and reactivity"),
        ("The main ore of iron is", "Haematite", ["Bauxite", "Galena", "Malachite"], "Haematite (Fe2O3) is the main iron ore.", "Metals and reactivity"),
        ("The main ore of aluminium is", "Bauxite", ["Haematite", "Galena", "Cassiterite"], "Bauxite is the ore of aluminium.", "Metals and reactivity"),
        ("Which of the following is a hydrocarbon?", "Methane", ["Ethanol", "Glucose", "Acetic acid"], "Methane (CH4) contains only carbon and hydrogen.", "Organic chemistry"),
        ("The general formula of alkanes is", "CnH2n+2", ["CnH2n", "CnH2n-2", "CnH2n+1"], "Alkanes follow CnH2n+2.", "Organic chemistry"),
        ("The general formula of alkenes is", "CnH2n", ["CnH2n+2", "CnH2n-2", "CnH2n+1"], "Alkenes follow CnH2n.", "Organic chemistry"),
        ("Ethene is an example of an", "Alkene", ["Alkane", "Alkyne", "Alcohol"], "Ethene (C2H4) has a carbon-carbon double bond.", "Organic chemistry"),
        ("The functional group of alcohols is", "-OH", ["-COOH", "-CHO", "-NH2"], "Alcohols contain the hydroxyl group -OH.", "Organic chemistry"),
        ("The functional group of carboxylic acids is", "-COOH", ["-OH", "-CHO", "-CO-"], "Carboxylic acids contain -COOH.", "Organic chemistry"),
        ("Vinegar contains", "Ethanoic acid", ["Citric acid", "Hydrochloric acid", "Tartaric acid"], "Vinegar is dilute ethanoic acid.", "Organic chemistry"),
        ("The monomer of polythene is", "Ethene", ["Ethane", "Propene", "Benzene"], "Polythene is made by polymerising ethene.", "Organic chemistry"),
        ("Soap is made by the reaction of fats with", "Sodium hydroxide", ["Hydrochloric acid", "Sulphuric acid", "Nitric acid"], "Saponification is fat + alkali \u2192 soap + glycerol.", "Organic chemistry"),
        ("Which of the following is a greenhouse gas?", "Carbon dioxide", ["Oxygen", "Nitrogen", "Argon"], "CO2 traps heat in the atmosphere.", "Chemistry and the environment"),
        ("The gas responsible for the depletion of the ozone layer is", "Chlorofluorocarbon", ["Carbon dioxide", "Methane", "Nitrogen"], "CFCs release chlorine that destroys ozone.", "Chemistry and the environment"),
        ("Hard water contains dissolved salts of", "Calcium and magnesium", ["Sodium and potassium", "Iron and zinc", "Copper and lead"], "Hardness is caused by Ca2+ and Mg2+ ions.", "Water"),
        ("The method used to remove permanent hardness of water is", "Adding washing soda", ["Boiling", "Filtration", "Distillation"], "Boiling removes temporary hardness only; washing soda removes permanent hardness.", "Water"),
        ("Avogadro's number is approximately", "6.02 \u00d7 10\u00b2\u00b3", ["6.02 \u00d7 10\u00b2\u00b2", "6.02 \u00d7 10\u00b2\u2074", "6.02 \u00d7 10\u00b2\u2070"], "One mole contains 6.02 \u00d7 10\u00b2\u00b3 particles.", "Stoichiometry"),
        ("One mole of a gas at s.t.p. occupies", "22.4 dm\u00b3", ["11.2 dm\u00b3", "24.0 dm\u00b3", "2.24 dm\u00b3"], "Molar volume at s.t.p. is 22.4 dm\u00b3.", "Stoichiometry"),
        ("Boyle's law states that at constant temperature, the volume of a fixed mass of gas is", "Inversely proportional to its pressure", ["Directly proportional to its pressure", "Independent of its pressure", "Proportional to its temperature"], "Boyle's law: V \u221d 1/P at constant T.", "Gas laws"),
        ("Charles' law states that at constant pressure, the volume of a fixed mass of gas is", "Directly proportional to its absolute temperature", ["Inversely proportional to its temperature", "Independent of temperature", "Proportional to its pressure"], "Charles' law: V \u221d T at constant P.", "Gas laws"),
        ("The ideal gas equation is", "PV = nRT", ["P = nRT/V only", "PV = nT", "V = nRT"], "The ideal gas equation is PV = nRT.", "Gas laws"),
        ("A catalyst increases the rate of a reaction by", "Lowering the activation energy", ["Raising the activation energy", "Increasing the temperature", "Increasing the concentration"], "A catalyst lowers the activation energy.", "Chemical kinetics"),
        ("The rate of a chemical reaction increases with", "Increase in temperature", ["Decrease in temperature", "Decrease in concentration", "Decrease in surface area"], "Higher temperature increases reaction rate.", "Chemical kinetics"),
        ("Which of the following affects the position of equilibrium?", "Temperature", ["Catalyst", "Pressure only for gases", "Colour of reactants"], "A catalyst does not change equilibrium position; temperature does.", "Chemical equilibrium"),
        ("The pH of a solution with [H+] = 1 \u00d7 10\u207b\u00b3 mol/dm\u00b3 is", "3", ["1", "10", "13"], "pH = -log[H+] = 3.", "Acids, bases and salts"),
    ]
    for q, c, ds, e, t in facts:
        add(q, c, ds, e, t)
    for _ in range(28):
        kind = rng.choice(["neutron", "molar", "moles", "boyle", "charles", "titr", "pct"])
        if kind == "neutron":
            z = rng.randint(6, 20); a = z + rng.randint(6, 20)
            add(f"An atom has atomic number {z} and mass number {a}. How many neutrons does it have?", str(a - z),
                _dist(rng, a - z, 3, lo=0), f"Neutrons = mass number - atomic number = {a} - {z} = {a - z}.", "Structure of the atom")
        elif kind == "molar":
            comp, mm = rng.choice([("H2O", 18), ("CO2", 44), ("NH3", 17), ("CH4", 16), ("O2", 32), ("N2", 28), ("HCl", 36.5)])
            if mm == 36.5:
                add(f"Calculate the relative molecular mass of {comp}. [H = 1, Cl = 35.5]", "36.5",
                    ["35.5", "37.5", "36"], "Mr = 1 + 35.5 = 36.5.", "Stoichiometry")
            else:
                add(f"Calculate the relative molecular mass of {comp}. [H = 1, C = 12, N = 14, O = 16, Na = 23, Cl = 35.5]", str(mm),
                    _dist(rng, mm, 3, lo=0), f"The relative molecular mass of {comp} is {mm}.", "Stoichiometry")
        elif kind == "moles":
            mass = rng.choice([8, 16, 32, 44, 88]); mm = rng.choice([16, 32, 44])
            if mass < mm:
                continue
            moles = mass / mm
            if moles != int(moles):
                continue
            add(f"How many moles are in {mass} g of a substance of molar mass {mm} g/mol?", str(int(moles)),
                _dist(rng, int(moles), 2, lo=0), f"Moles = mass/molar mass = {mass}/{mm} = {int(moles)} mol.", "Stoichiometry")
        elif kind == "boyle":
            p1 = rng.choice([100, 200, 400]); v1 = rng.choice([2, 4, 5]); p2 = p1 * 2
            v2 = v1 * p1 // p2
            add(f"A gas occupies {v1} dm\u00b3 at {p1} kPa. If the pressure is doubled at constant temperature, what is the new volume?", f"{v2} dm\u00b3",
                _pick(rng, f"{v2} dm\u00b3", [f"{v1 * 2} dm\u00b3", f"{v1} dm\u00b3", f"{v2 + 1} dm\u00b3"]), f"Boyle's law: P1V1 = P2V2, so V2 = {p1}\u00d7{v1}/{p2} = {v2} dm\u00b3.", "Gas laws")
        elif kind == "charles":
            v1 = rng.choice([100, 200]); v2 = v1 * 2
            add(f"A gas occupies {v1} cm\u00b3 at 273 K. What volume will it occupy at 546 K at constant pressure?", f"{v2} cm\u00b3",
                _pick(rng, f"{v2} cm\u00b3", [f"{v1} cm\u00b3", f"{v1 // 2} cm\u00b3", f"{v2 + 50} cm\u00b3"]), f"Charles' law: V1/T1 = V2/T2, so V2 = {v1} \u00d7 546/273 = {v2} cm\u00b3.", "Gas laws")
        elif kind == "titr":
            m1 = rng.choice([0.1, 0.2, 0.5]); v1 = rng.choice([20, 25]); v2 = rng.choice([20, 25, 50])
            m2 = m1 * v1 / v2
            add(f"{v1} cm\u00b3 of {m1} mol/dm\u00b3 acid neutralises {v2} cm\u00b3 of alkali of the same concentration ratio (1:1). Find the concentration of the alkali.",
                f"{fmt_num(m2)} mol/dm\u00b3",
                _pick(rng, f"{fmt_num(m2)} mol/dm\u00b3", [f"{fmt_num(m1)} mol/dm\u00b3", f"{fmt_num(m2 * 2)} mol/dm\u00b3", f"{fmt_num(m2 / 2)} mol/dm\u00b3"]),
                f"M1V1 = M2V2, so M2 = {m1} \u00d7 {v1}/{v2} = {fmt_num(m2)} mol/dm\u00b3.", "Stoichiometry: volumetric analysis")
        elif kind == "pct":
            comp, pct = rng.choice([("water, H2O (oxygen)", 88.9), ("methane, CH4 (hydrogen)", 25), ("carbon dioxide, CO2 (carbon)", 27.3)])
            add(f"Calculate the percentage by mass of the named element in {comp}.", f"{pct}%",
                _pick(rng, f"{pct}%", ["50%", "75%", "100%", "10%"]), f"Percentage by mass = (mass of element/molar mass) \u00d7 100% = {pct}%.", "Stoichiometry")
    return uniq_pool(P)

def accounting_pool(year):
    rng = random.Random(f"acct-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    facts = [
        ("The accounting concept which states that for every debit entry there must be a corresponding credit entry is the", "Dual aspect concept", ["Going concern concept", "Accrual concept", "Money measurement concept"], "Dual aspect is the foundation of double entry.", "Introduction to Financial Accounting: concepts"),
        ("Which of the following is an example of a nominal account?", "Wages account", ["Plant and machinery", "Bank account", "Debtors account"], "Nominal accounts record expenses and incomes, e.g. wages.", "Classification of accounts"),
        ("Which of the following is a real account?", "Plant and machinery account", ["Wages account", "Sales account", "Rent account"], "Real accounts record assets.", "Classification of accounts"),
        ("The accounting equation is", "Assets = Capital + Liabilities", ["Assets = Capital - Liabilities", "Capital = Assets + Liabilities", "Liabilities = Assets + Capital"], "Assets = Capital + Liabilities.", "The accounting equation and double entry"),
        ("An increase in assets is recorded on the", "Debit side", ["Credit side", "Trial balance only", "Balance sheet only"], "Assets increase on the debit side.", "The accounting equation and double entry"),
        ("The source document for goods bought on credit is the", "Invoice", ["Receipt", "Cheque", "Pay-in slip"], "An invoice is issued for credit purchases.", "Source documents"),
        ("The source document issued for cash received is the", "Receipt", ["Invoice", "Credit note", "Debit note"], "A receipt acknowledges cash received.", "Source documents"),
        ("A credit note is issued when goods are", "Returned by a customer", ["Sold for cash", "Bought for cash", "Damaged in transit only"], "A credit note records goods returned by a customer.", "Source documents"),
        ("The book of original entry for credit sales is the", "Sales day book", ["Purchases day book", "Cash book", "General journal"], "Credit sales are first recorded in the sales day book.", "Books of original entry"),
        ("The book of original entry for credit purchases is the", "Purchases day book", ["Sales day book", "Cash book", "Returns outwards book"], "Credit purchases are first recorded in the purchases day book.", "Books of original entry"),
        ("The cash book is a book of original entry and also a", "Ledger", ["Journal", "Trial balance", "Balance sheet"], "The cash book serves as both a book of original entry and a ledger.", "Books of original entry"),
        ("A trial balance is prepared to check the", "Arithmetical accuracy of the ledger", ["Profit of the business", "Assets of the business", "Cash position"], "A trial balance checks that total debits equal total credits.", "Trial balance"),
        ("If total debits exceed total credits in a trial balance, the difference is a", "Debit balance", ["Credit balance", "Profit", "Loss"], "Excess debits give a debit balance.", "Trial balance"),
        ("Which of the following is a current asset?", "Stock", ["Land and buildings", "Plant and machinery", "Motor vehicles"], "Stock is a current asset.", "Final accounts"),
        ("Which of the following is a non-current asset?", "Motor vehicles", ["Debtors", "Cash at bank", "Stock"], "Motor vehicles are non-current assets.", "Final accounts"),
        ("Which of the following is a current liability?", "Creditors", ["Bank loan (long term)", "Capital", "Debentures"], "Creditors are current liabilities.", "Final accounts"),
        ("The excess of current assets over current liabilities is", "Working capital", ["Capital employed", "Gross profit", "Net profit"], "Working capital = current assets - current liabilities.", "Final accounts"),
        ("Gross profit is calculated as sales less", "Cost of goods sold", ["Expenses", "Drawings", "Capital"], "Gross profit = sales - cost of goods sold.", "Final accounts of a sole trader"),
        ("Cost of goods sold is opening stock plus purchases less", "Closing stock", ["Sales", "Returns inwards", "Carriage outwards"], "Cost of goods sold = opening stock + purchases - closing stock.", "Final accounts of a sole trader"),
        ("Net profit is gross profit less", "Expenses", ["Sales", "Drawings", "Capital"], "Net profit = gross profit - expenses.", "Final accounts of a sole trader"),
        ("Drawings by the owner reduce the", "Capital", ["Sales", "Purchases", "Liabilities"], "Drawings reduce the owner's capital.", "Final accounts of a sole trader"),
        ("Depreciation is the", "Fall in value of a non-current asset over its useful life", ["Increase in value of an asset", "Cost of repairs", "Selling price of an asset"], "Depreciation spreads the cost of an asset over its useful life.", "Provisions and reserves"),
        ("The straight-line method of depreciation charges", "A fixed amount each year", ["A decreasing amount each year", "An increasing amount each year", "Depreciation only on disposal"], "Straight-line depreciation is a fixed annual charge.", "Provisions and reserves"),
        ("The reducing-balance method of depreciation charges", "A fixed percentage of the diminishing value", ["A fixed amount each year", "Depreciation on cost only", "No depreciation after year one"], "Reducing balance applies a fixed rate to the book value.", "Provisions and reserves"),
        ("A provision for doubtful debts is created to", "Cover debts that may not be collected", ["Increase profit", "Reduce creditors", "Increase capital"], "It anticipates bad debts.", "Provisions and reserves"),
        ("Bad debts are written off in the", "Profit and loss account", ["Trading account", "Balance sheet only", "Cash book"], "Bad debts are an expense in the profit and loss account.", "Provisions and reserves"),
        ("The account used to correct errors in the ledger is the", "Suspense account", ["Control account", "Capital account", "Drawings account"], "A suspense account holds differences pending correction.", "Correction of errors"),
        ("A sales ledger control account is also called the", "Debtors control account", ["Creditors control account", "General ledger", "Cash control account"], "It controls the debtors (sales) ledger.", "Control accounts"),
        ("A purchases ledger control account is also called the", "Creditors control account", ["Debtors control account", "Cash control account", "Nominal ledger"], "It controls the creditors (purchases) ledger.", "Control accounts"),
        ("The main purpose of a bank reconciliation statement is to", "Reconcile the cash book balance with the bank statement", ["Calculate profit", "Prepare the trial balance", "Record cheques"], "It explains differences between the cash book and bank statement.", "Bank reconciliation"),
        ("An unpresented cheque in a bank reconciliation is", "Added to the bank statement balance", ["Deducted from the cash book", "Added to the cash book", "Ignored"], "Unpresented cheques have been recorded in the cash book but not yet by the bank.", "Bank reconciliation"),
        ("A bank overdraft is a", "Current liability", ["Current asset", "Non-current asset", "Revenue"], "An overdraft is money owed to the bank, repayable on demand.", "Bank reconciliation"),
        ("The manufacturing account is prepared to find the", "Cost of production", ["Gross profit", "Net profit", "Selling price"], "It calculates the cost of goods manufactured.", "Manufacturing accounts"),
        ("Prime cost is the sum of direct materials, direct labour and", "Direct expenses", ["Factory overheads", "Administration expenses", "Selling expenses"], "Prime cost = direct materials + direct labour + direct expenses.", "Manufacturing accounts"),
        ("Factory overheads are also called", "Indirect manufacturing costs", ["Direct costs", "Prime costs", "Selling costs"], "Factory overheads are indirect production costs.", "Manufacturing accounts"),
        ("A partnership is a business owned by", "Two or more persons", ["One person", "The government", "Shareholders only"], "A partnership has two or more owners.", "Partnership accounts"),
        ("In a partnership, interest on capital is", "An appropriation of profit", ["An expense", "A liability", "A drawings"], "Interest on capital is shared from profit, not charged as an expense.", "Partnership accounts"),
        ("The document that governs a partnership is the", "Partnership deed", ["Memorandum of association", "Articles of association", "Prospectus"], "The partnership deed sets out the terms of the partnership.", "Partnership accounts"),
        ("A company is owned by its", "Shareholders", ["Directors", "Debenture holders", "Employees"], "Shareholders own a company.", "Company accounts"),
        ("Ordinary shares carry", "Voting rights and variable dividends", ["Fixed dividends only", "No voting rights", "Guaranteed interest"], "Ordinary shareholders vote and receive variable dividends.", "Company accounts"),
        ("Preference shares carry", "A fixed rate of dividend", ["Variable dividends", "No dividend", "Voting rights only"], "Preference shares receive a fixed dividend before ordinary shares.", "Company accounts"),
        ("Debentures are a form of", "Long-term loan to the company", ["Share capital", "Current liability", "Reserve"], "Debentures are long-term borrowing.", "Company accounts"),
        ("The current ratio is current assets divided by", "Current liabilities", ["Non-current assets", "Capital", "Total assets"], "Current ratio = current assets / current liabilities.", "Ratio analysis"),
        ("The acid test ratio excludes", "Stock", ["Debtors", "Cash", "Bank"], "Acid test = (current assets - stock) / current liabilities.", "Ratio analysis"),
        ("A business that sells goods on credit is extending", "Trade credit", ["A loan", "A discount", "An overdraft"], "Credit sales are trade credit to customers.", "Final accounts"),
        ("Carriage inwards is charged to the", "Trading account", ["Profit and loss account", "Balance sheet", "Cash book"], "Carriage inwards is part of the cost of goods sold.", "Final accounts of a sole trader"),
        ("Carriage outwards is charged to the", "Profit and loss account", ["Trading account", "Manufacturing account", "Balance sheet"], "Carriage outwards is a selling expense.", "Final accounts of a sole trader"),
        ("Returns inwards are also called", "Sales returns", ["Purchases returns", "Discount allowed", "Discount received"], "Goods returned by customers are sales returns.", "Final accounts of a sole trader"),
        ("Returns outwards are also called", "Purchases returns", ["Sales returns", "Discount allowed", "Bad debts"], "Goods returned to suppliers are purchases returns.", "Final accounts of a sole trader"),
        ("Discount allowed is", "An expense", ["Income", "An asset", "A liability"], "Discount allowed to customers is an expense.", "Final accounts of a sole trader"),
        ("Discount received is", "Income", ["An expense", "An asset", "A liability"], "Discount received from suppliers is income.", "Final accounts of a sole trader"),
    ]
    for q, c, ds, e, t in facts:
        add(q, c, ds, e, t)
    for _ in range(30):
        kind = rng.choice(["dep", "profit", "cogs", "ratio", "acid", "comm", "workcap", "sales"])
        if kind == "dep":
            cost = rng.choice([10000, 20000, 50000, 100000]); rate = rng.choice([10, 20, 25])
            dep = cost * rate // 100
            add(f"A machine cost \u20a6{cost} and is depreciated at {rate}% per annum on a straight-line basis. Find the annual depreciation.",
                f"\u20a6{dep}", _pick(rng, f"\u20a6{dep}", [f"\u20a6{dep * 2}", f"\u20a6{dep // 2}", f"\u20a6{cost - dep}"]),
                f"Depreciation = {rate}% \u00d7 \u20a6{cost} = \u20a6{dep}.", "Provisions and reserves: depreciation")
        elif kind == "profit":
            sales = rng.choice([50000, 80000, 100000, 200000]); cogs = sales * rng.choice([60, 70, 80]) // 100
            gp = sales - cogs
            add(f"A trader's sales were \u20a6{sales} and cost of goods sold was \u20a6{cogs}. Find the gross profit.",
                f"\u20a6{gp}", _pick(rng, f"\u20a6{gp}", [f"\u20a6{sales + cogs}", f"\u20a6{cogs}", f"\u20a6{gp + 10000}"]),
                f"Gross profit = sales - cost of goods sold = \u20a6{sales} - \u20a6{cogs} = \u20a6{gp}.", "Final accounts of a sole trader")
        elif kind == "cogs":
            op = rng.choice([10000, 20000]); pur = rng.choice([40000, 60000]); cl = rng.choice([5000, 15000])
            cogs = op + pur - cl
            add(f"Opening stock \u20a6{op}, purchases \u20a6{pur} and closing stock \u20a6{cl}. Find the cost of goods sold.",
                f"\u20a6{cogs}", _pick(rng, f"\u20a6{cogs}", [f"\u20a6{op + pur}", f"\u20a6{op + pur + cl}", f"\u20a6{pur - cl}"]),
                f"Cost of goods sold = {op} + {pur} - {cl} = \u20a6{cogs}.", "Final accounts of a sole trader")
        elif kind == "ratio":
            ca = rng.choice([60000, 80000, 100000]); cl = rng.choice([20000, 40000, 50000])
            if ca % cl:
                continue
            add(f"A business has current assets of \u20a6{ca} and current liabilities of \u20a6{cl}. Find the current ratio.",
                f"{ca // cl}:1", _pick(rng, f"{ca // cl}:1", ["1:1", "2:1", f"{ca // cl + 1}:1"]),
                f"Current ratio = {ca}/{cl} = {ca // cl}:1.", "Ratio analysis")
        elif kind == "acid":
            ca = rng.choice([80000, 100000]); stock = rng.choice([20000, 40000]); cl = rng.choice([20000, 40000])
            num = ca - stock
            if num % cl:
                continue
            add(f"Current assets \u20a6{ca} (including stock of \u20a6{stock}) and current liabilities \u20a6{cl}. Find the acid test ratio.",
                f"{num // cl}:1", _pick(rng, f"{num // cl}:1", ["1:1", "2:1", f"{num // cl + 1}:1"]),
                f"Acid test = ({ca} - {stock})/{cl} = {num // cl}:1.", "Ratio analysis")
        elif kind == "comm":
            sales = rng.choice([100000, 200000, 500000]); rate = rng.choice([5, 10])
            comm = sales * rate // 100
            add(f"A salesman earns {rate}% commission on sales of \u20a6{sales}. Find his commission.",
                f"\u20a6{comm}", _pick(rng, f"\u20a6{comm}", [f"\u20a6{comm * 2}", f"\u20a6{sales - comm}", f"\u20a6{comm // 2}"]),
                f"Commission = {rate}% \u00d7 \u20a6{sales} = \u20a6{comm}.", "Final accounts of a sole trader")
        elif kind == "workcap":
            ca = rng.choice([90000, 120000]); cl = rng.choice([30000, 50000])
            add(f"Current assets are \u20a6{ca} and current liabilities are \u20a6{cl}. Find the working capital.",
                f"\u20a6{ca - cl}", _pick(rng, f"\u20a6{ca - cl}", [f"\u20a6{ca + cl}", f"\u20a6{cl}", f"\u20a6{ca - cl + 10000}"]),
                f"Working capital = {ca} - {cl} = \u20a6{ca - cl}.", "Final accounts")
        elif kind == "sales":
            cost = rng.choice([40000, 60000, 80000]); pct = rng.choice([20, 25])
            sp = cost * (100 + pct) // 100
            add(f"Goods costing \u20a6{cost} are sold at a mark-up of {pct}%. Find the selling price.",
                f"\u20a6{sp}", _pick(rng, f"\u20a6{sp}", [f"\u20a6{cost}", f"\u20a6{cost + cost * pct // 200}", f"\u20a6{sp + 5000}"]),
                f"Mark-up = {pct}% of \u20a6{cost} = \u20a6{cost * pct // 100}; selling price = \u20a6{sp}.", "Final accounts of a sole trader")
    return uniq_pool(P)

def economics_pool(year):
    rng = random.Random(f"econ-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    facts = [
        ("Economics is often defined as the study of scarcity and", "Choice", ["Poverty", "Wealth", "Money"], "Scarcity forces choice about how to use limited resources.", "Definition and scope of economics"),
        ("The fundamental economic problem facing every society is", "Scarcity", ["Unemployment", "Inflation", "Poverty"], "Resources are finite while wants are infinite.", "Definition and scope of economics"),
        ("The cost of the next best alternative forgone is called", "Opportunity cost", ["Money cost", "Fixed cost", "Marginal cost"], "Opportunity cost is the alternative given up.", "Definition and scope of economics"),
        ("A scale of preference is a list of wants arranged in order of", "Priority", ["Price", "Quantity", "Time"], "A scale of preference ranks wants by importance.", "Definition and scope of economics"),
        ("Which of the following is a factor of production?", "Land", ["Money", "Goods", "Services"], "The factors are land, labour, capital and entrepreneurship.", "Factors of production"),
        ("The reward for land is", "Rent", ["Wages", "Interest", "Profit"], "Land earns rent.", "Factors of production"),
        ("The reward for labour is", "Wages", ["Rent", "Interest", "Profit"], "Labour earns wages (or salaries).", "Factors of production"),
        ("The reward for capital is", "Interest", ["Rent", "Wages", "Profit"], "Capital earns interest.", "Factors of production"),
        ("The reward for entrepreneurship is", "Profit", ["Rent", "Wages", "Interest"], "The entrepreneur earns profit.", "Factors of production"),
        ("Which economic system is based on private ownership of the means of production?", "Capitalism", ["Socialism", "Communism", "Mixed economy only"], "In capitalism, private individuals own the means of production.", "Types and basic features of economic systems"),
        ("In a socialist economy, the means of production are owned by the", "State", ["Individuals", "Foreigners", "Church"], "In socialism the state owns the means of production.", "Types and basic features of economic systems"),
        ("Nigeria operates a", "Mixed economy", ["Pure capitalist economy", "Pure socialist economy", "Command economy only"], "Nigeria combines private and public ownership.", "Types and basic features of economic systems"),
        ("The law of demand states that, other things being equal, as price rises, quantity demanded", "Falls", ["Rises", "Stays the same", "Doubles"], "Demand curves slope downwards.", "Demand"),
        ("The law of supply states that, other things being equal, as price rises, quantity supplied", "Rises", ["Falls", "Stays the same", "Becomes zero"], "Supply curves slope upwards.", "Supply"),
        ("An increase in the price of a substitute good will", "Increase demand for the good", ["Decrease demand for the good", "Not affect demand", "Decrease supply"], "Consumers switch to the relatively cheaper good.", "Demand"),
        ("An increase in consumers' income will increase demand for a", "Normal good", ["Inferior good", "Giffen good", "Free good"], "Demand for normal goods rises with income.", "Demand"),
        ("An increase in consumers' income will decrease demand for an", "Inferior good", ["Normal good", "Luxury good", "Essential good"], "Consumers buy less of inferior goods as income rises.", "Demand"),
        ("The point where demand equals supply is the", "Equilibrium point", ["Maximum point", "Minimum point", "Break-even point"], "At equilibrium, quantity demanded equals quantity supplied.", "Theory of price determination"),
        ("When price is above equilibrium, there is a", "Surplus", ["Shortage", "Equilibrium", "Deficit"], "Excess supply appears above equilibrium price.", "Theory of price determination"),
        ("When price is below equilibrium, there is a", "Shortage", ["Surplus", "Equilibrium", "Glut"], "Excess demand appears below equilibrium price.", "Theory of price determination"),
        ("Price elasticity of demand measures the responsiveness of quantity demanded to a change in", "Price", ["Income", "Taste", "Supply"], "PED = % change in quantity demanded / % change in price.", "Demand: elasticity"),
        ("If demand is price elastic, a fall in price will", "Increase total revenue", ["Decrease total revenue", "Leave total revenue unchanged", "Reduce quantity demanded"], "With elastic demand, quantity rises proportionally more than price falls.", "Demand: elasticity"),
        ("The total cost of producing a given output is the sum of", "Fixed cost and variable cost", ["Marginal cost and average cost", "Explicit cost only", "Implicit cost only"], "TC = FC + VC.", "Theory of cost and revenue"),
        ("Costs that do not change with output are", "Fixed costs", ["Variable costs", "Marginal costs", "Average costs"], "Fixed costs, e.g. rent, do not vary with output.", "Theory of cost and revenue"),
        ("Costs that change with output are", "Variable costs", ["Fixed costs", "Sunk costs", "Opportunity costs"], "Variable costs, e.g. raw materials, vary with output.", "Theory of cost and revenue"),
        ("Marginal cost is the", "Extra cost of producing one more unit", ["Total cost divided by output", "Cost of fixed inputs", "Average cost of production"], "MC = change in TC / change in output.", "Theory of cost and revenue"),
        ("A firm maximises profit where", "Marginal cost equals marginal revenue", ["Total cost is minimum", "Average cost is minimum", "Price is highest"], "Profit is maximised where MC = MR.", "Theory of cost and revenue"),
        ("In perfect competition, there are", "Many buyers and sellers", ["One seller", "Few sellers", "One buyer"], "Perfect competition has many buyers and sellers of identical products.", "Market structures"),
        ("A market with only one seller is a", "Monopoly", ["Oligopoly", "Monopolistic competition", "Duopoly"], "A monopoly has a single seller.", "Market structures"),
        ("A market with a few large sellers is an", "Oligopoly", ["Monopoly", "Perfect competition", "Monopsony"], "An oligopoly has a few dominant sellers.", "Market structures"),
        ("The main aim of a sole proprietorship is to", "Make profit", ["Provide employment only", "Pay taxes", "Avoid competition"], "A sole trader aims to earn profit.", "Business organisations"),
        ("A major disadvantage of a sole proprietorship is", "Unlimited liability", ["Limited liability", "Difficulty in raising capital only", "Lack of privacy"], "The owner's personal assets are at risk.", "Business organisations"),
        ("A cooperative society is formed mainly to", "Serve the interests of its members", ["Make maximum profit", "Avoid taxes", "Employ the government"], "Cooperatives serve members' common needs.", "Business organisations"),
        ("The middleman between the producer and the retailer is the", "Wholesaler", ["Consumer", "Agent only", "Retailer"], "The wholesaler buys in bulk and sells to retailers.", "Distributive trade"),
        ("The middleman who sells directly to the final consumer is the", "Retailer", ["Wholesaler", "Producer", "Agent"], "The retailer sells to final consumers.", "Distributive trade"),
        ("The central bank of Nigeria is the", "Central Bank of Nigeria", ["First Bank of Nigeria", "Bank of Industry", "Nigeria Deposit Insurance Corporation"], "The CBN is Nigeria's central bank.", "Financial institutions"),
        ("The main function of the central bank is to", "Control the money supply", ["Accept deposits from the public", "Give loans to individuals", "Sell goods"], "The central bank regulates money and credit.", "Financial institutions"),
        ("Commercial banks create money through", "Lending", ["Printing notes", "Accepting deposits only", "Paying interest"], "Banks create deposits when they lend.", "Financial institutions"),
        ("Inflation is a", "General rise in the price level", ["Fall in the price level", "Rise in unemployment only", "Fall in money supply"], "Inflation is a sustained rise in general prices.", "Money and inflation"),
        ("Deflation is a", "General fall in the price level", ["Rise in the price level", "Rise in money supply", "Fall in unemployment"], "Deflation is a sustained fall in general prices.", "Money and inflation"),
        ("A major cause of demand-pull inflation is", "Excess demand over supply", ["Fall in demand", "Increase in productivity", "Fall in money supply"], "Too much money chasing too few goods causes demand-pull inflation.", "Money and inflation"),
        ("The main functions of money are medium of exchange, store of value, unit of account and", "Standard of deferred payment", ["Measure of inflation", "Source of income", "Means of production"], "Money is also a standard of deferred payment.", "Money and inflation"),
        ("Gross Domestic Product (GDP) is the total value of goods and services produced", "Within a country in a year", ["By citizens abroad only", "By the government only", "In the informal sector only"], "GDP measures production within a country's borders.", "National income"),
        ("National income is the total value of goods and services produced by a country in", "One year", ["One month", "One decade", "One quarter"], "National income is measured over a year.", "National income"),
        ("The largest sector of the Nigerian economy by employment is", "Agriculture", ["Manufacturing", "Mining", "Services"], "Agriculture employs the largest share of Nigeria's labour force.", "Agriculture"),
        ("The main source of government revenue in Nigeria is", "Oil revenue", ["Personal income tax", "Customs duties only", "Value Added Tax only"], "Petroleum provides the largest share of federal revenue.", "Public finance"),
        ("A budget deficit occurs when government expenditure exceeds government", "Revenue", ["Borrowing", "Savings", "Investment"], "A deficit is expenditure above revenue.", "Public finance"),
        ("A tax levied as a percentage of income is a", "Proportional tax", ["Progressive tax", "Regressive tax", "Direct tax only"], "A proportional tax takes the same percentage at all income levels.", "Public finance"),
        ("A tax that takes a larger percentage from higher incomes is a", "Progressive tax", ["Regressive tax", "Proportional tax", "Indirect tax"], "Progressive taxes rise as a share of income.", "Public finance"),
        ("Value Added Tax (VAT) is an example of an", "Indirect tax", ["Direct tax", "Progressive tax", "Poll tax"], "VAT is paid by consumers through sellers.", "Public finance"),
        ("Personal income tax is an example of a", "Direct tax", ["Indirect tax", "Excise duty", "Customs duty"], "Income tax is levied directly on the earner.", "Public finance"),
        ("The balance of payments records a country's", "Transactions with the rest of the world", ["Internal trade only", "Government spending only", "Bank deposits"], "The balance of payments records international transactions.", "International trade and balance of payments"),
        ("A country's visible exports are goods", "Sold to other countries", ["Bought from other countries", "Sold within the country", "Given as aid"], "Visible exports are goods sold abroad.", "International trade and balance of payments"),
        ("The Economic Community of West African States (ECOWAS) was founded in", "1975", ["1960", "1963", "1980"], "ECOWAS was founded by the Treaty of Lagos in 1975.", "Economic integration"),
        ("The headquarters of ECOWAS is in", "Abuja, Nigeria", ["Lagos, Nigeria", "Accra, Ghana", "Dakar, Senegal"], "ECOWAS headquarters is in Abuja.", "Economic integration"),
        ("The headquarters of the African Union is in", "Addis Ababa, Ethiopia", ["Cairo, Egypt", "Nairobi, Kenya", "Pretoria, South Africa"], "The AU headquarters is in Addis Ababa.", "International economic organisations"),
        ("The headquarters of the United Nations is in", "New York, USA", ["Geneva, Switzerland", "London, UK", "Paris, France"], "The UN headquarters is in New York.", "International economic organisations"),
        ("The International Monetary Fund (IMF) mainly provides", "Short-term loans to countries with balance of payments problems", ["Long-term development loans", "Military aid", "Food aid"], "The IMF lends to countries facing balance of payments difficulties.", "International economic organisations"),
        ("The World Bank mainly provides", "Long-term loans for development projects", ["Short-term balance of payments loans", "Military aid", "Emergency food aid"], "The World Bank funds development projects.", "International economic organisations"),
        ("Unemployment in which people are out of work between jobs is", "Frictional unemployment", ["Structural unemployment", "Cyclical unemployment", "Seasonal unemployment"], "Frictional unemployment is short-term, between jobs.", "Population and labour market"),
        ("Unemployment caused by changes in the structure of the economy is", "Structural unemployment", ["Frictional unemployment", "Cyclical unemployment", "Voluntary unemployment"], "Structural unemployment follows shifts in industries and skills.", "Population and labour market"),
        ("The labour force is made up of people who are", "Employed or actively seeking work", ["Of working age only", "Employed only", "Retired"], "The labour force includes the employed and the unemployed seeking work.", "Population and labour market"),
        ("A population pyramid with a wide base shows a", "High birth rate", ["Low birth rate", "Ageing population", "Low death rate only"], "A wide base means many young people, i.e. high birth rate.", "Population and labour market"),
        ("The Malthusian theory of population states that population grows in", "Geometric progression while food grows arithmetically", ["Arithmetic progression", "The same rate as food", "Declining numbers"], "Malthus said population grows geometrically, food arithmetically.", "Population and labour market"),
        ("The demand for labour is a", "Derived demand", ["Direct demand", "Joint demand", "Composite demand"], "Labour is demanded because goods are demanded.", "Population and labour market"),
        ("A trade union is an association of", "Workers", ["Employers", "Consumers", "Shareholders"], "A trade union represents workers.", "Population and labour market"),
        ("The main aim of a trade union is to", "Protect workers' interests", ["Maximise employers' profits", "Reduce wages", "Close factories"], "Trade unions seek better pay and conditions for members.", "Population and labour market"),
    ]
    for q, c, ds, e, t in facts:
        add(q, c, ds, e, t)
    for _ in range(25):
        kind = rng.choice(["ped", "pct", "index", "gdp", "rev"])
        if kind == "ped":
            q1 = rng.choice([100, 200]); q2 = q1 + rng.choice([10, 20, 50]); p1 = rng.choice([10, 20]); p2 = p1 - rng.choice([1, 2, 5])
            if p2 <= 0:
                continue
            ped = round(abs(((q2 - q1) / q1) / ((p2 - p1) / p1)), 2)
            add(f"When price falls from \u20a6{p1} to \u20a6{p2}, quantity demanded rises from {q1} to {q2} units. Calculate the price elasticity of demand.",
                str(ped), _pick(rng, str(ped), [str(round(ped + 0.5, 2)), str(round(ped - 0.5, 2)) if ped > 0.5 else "0.25", "1.00", "0.00"]),
                f"PED = %\u0394Q / %\u0394P = {round((q2 - q1) / q1 * 100, 1)}% / {round(abs((p2 - p1) / p1) * 100, 1)}% = {ped}.", "Demand: elasticity")
        elif kind == "pct":
            old = rng.choice([100, 200, 400]); new = old + rng.choice([10, 20, 50, 100])
            pct = (new - old) * 100 // old
            add(f"Price rises from \u20a6{old} to \u20a6{new}. Calculate the percentage increase.", f"{pct}%",
                _pick(rng, f"{pct}%", [f"{pct + 5}%", f"{pct - 5}%", f"{pct * 2}%"]), f"Increase = {new - old}; % increase = {new - old}/{old} \u00d7 100% = {pct}%.", "Basic tools of economic analysis")
        elif kind == "index":
            base = rng.choice([100, 200]); cur = base + rng.choice([10, 20, 50])
            idx = cur * 100 // base
            add(f"If the price of a basket was \u20a6{base} in the base year and \u20a6{cur} in the current year, find the price index.", str(idx),
                _pick(rng, str(idx), [str(idx + 5), str(idx - 5), "100"]), f"Price index = (current price/base price) \u00d7 100 = {cur}/{base} \u00d7 100 = {idx}.", "Basic tools of economic analysis")
        elif kind == "gdp":
            c = rng.choice([400, 500]); i = rng.choice([100, 200]); g = rng.choice([100, 150]); x = rng.choice([50, 80]); m = rng.choice([30, 60])
            gdp = c + i + g + (x - m)
            add(f"Given consumption \u20a6{c}bn, investment \u20a6{i}bn, government spending \u20a6{g}bn, exports \u20a6{x}bn and imports \u20a6{m}bn, calculate GDP.",
                f"\u20a6{gdp}bn", _pick(rng, f"\u20a6{gdp}bn", [f"\u20a6{c + i + g}bn", f"\u20a6{gdp + 50}bn", f"\u20a6{gdp - 50}bn"]),
                f"GDP = C + I + G + (X - M) = {c} + {i} + {g} + ({x} - {m}) = \u20a6{gdp}bn.", "National income")
        elif kind == "rev":
            p = rng.choice([10, 20, 25]); q = rng.choice([100, 200, 400])
            add(f"A firm sells {q} units at \u20a6{p} each. Find its total revenue.", f"\u20a6{p * q}",
                _pick(rng, f"\u20a6{p * q}", [f"\u20a6{p + q}", f"\u20a6{p * q + 100}", f"\u20a6{p * q - 100}"]),
                f"Total revenue = price \u00d7 quantity = \u20a6{p} \u00d7 {q} = \u20a6{p * q}.", "Theory of cost and revenue")
    return uniq_pool(P)

def computer_pool(year):
    rng = random.Random(f"comp-{year}")
    P = []
    def add(q, correct, ds, expl, topic):
        P.append(mk(q, correct, ds, expl, year, topic))
    facts = [
        ("The first generation of computers used", "Vacuum tubes", ["Transistors", "Integrated circuits", "Microprocessors"], "First-generation computers (1940-1956) used vacuum tubes.", "Computing devices: history of computers"),
        ("The second generation of computers used", "Transistors", ["Vacuum tubes", "Integrated circuits", "Microprocessors"], "Second-generation computers used transistors.", "Computing devices: history of computers"),
        ("The third generation of computers used", "Integrated circuits", ["Vacuum tubes", "Transistors", "Microprocessors"], "Third-generation computers used integrated circuits.", "Computing devices: history of computers"),
        ("The fourth generation of computers used", "Microprocessors", ["Vacuum tubes", "Transistors", "Integrated circuits"], "Fourth-generation computers used microprocessors.", "Computing devices: history of computers"),
        ("The brain of the computer is the", "CPU", ["Monitor", "Mouse", "Keyboard"], "The Central Processing Unit controls all computer operations.", "Overview of computing systems"),
        ("CPU stands for", "Central Processing Unit", ["Central Program Unit", "Computer Processing Unit", "Central Peripheral Unit"], "CPU = Central Processing Unit.", "Overview of computing systems"),
        ("The full meaning of RAM is", "Random Access Memory", ["Read Access Memory", "Rapid Access Memory", "Remote Access Memory"], "RAM = Random Access Memory.", "Overview of computing systems"),
        ("RAM is a", "Volatile memory", ["Non-volatile memory", "Permanent memory", "External memory"], "RAM loses its contents when power is off.", "Overview of computing systems"),
        ("ROM is a", "Non-volatile memory", ["Volatile memory", "Temporary memory", "External memory"], "ROM keeps its contents without power.", "Overview of computing systems"),
        ("The full meaning of ROM is", "Read Only Memory", ["Random Only Memory", "Read Open Memory", "Rapid Only Memory"], "ROM = Read Only Memory.", "Overview of computing systems"),
        ("Which of the following is an example of an operating system?", "Linux", ["Microsoft Word", "Google Chrome", "Oracle"], "Linux is an operating system.", "System software"),
        ("Which of the following is an example of application software?", "Microsoft Word", ["Linux", "Windows", "Android"], "Microsoft Word is application software.", "Application software"),
        ("Which of the following is an input device?", "Keyboard", ["Monitor", "Printer", "Speaker"], "A keyboard enters data into the computer.", "Computing devices: input devices"),
        ("Which of the following is an output device?", "Printer", ["Keyboard", "Mouse", "Scanner"], "A printer produces output on paper.", "Computing devices: output devices"),
        ("Which of the following is a storage device?", "Hard disk", ["Monitor", "Keyboard", "Mouse"], "A hard disk stores data permanently.", "Computing devices: storage devices"),
        ("The smallest unit of data in a computer is the", "Bit", ["Byte", "Nibble", "Word"], "A bit is a single binary digit, 0 or 1.", "Data representation"),
        ("One byte is equal to", "8 bits", ["4 bits", "16 bits", "2 bits"], "1 byte = 8 bits.", "Data representation"),
        ("One kilobyte is equal to", "1024 bytes", ["1000 bytes", "1024 bits", "100 bytes"], "1 KB = 1024 bytes.", "Data representation"),
        ("The binary number system uses base", "2", ["8", "10", "16"], "Binary uses digits 0 and 1, base 2.", "Data representation: number systems"),
        ("The decimal number system uses base", "10", ["2", "8", "16"], "Decimal uses digits 0-9, base 10.", "Data representation: number systems"),
        ("The octal number system uses base", "8", ["2", "10", "16"], "Octal uses digits 0-7, base 8.", "Data representation: number systems"),
        ("The hexadecimal number system uses base", "16", ["2", "8", "10"], "Hexadecimal uses base 16.", "Data representation: number systems"),
        ("The full meaning of ICT is", "Information and Communication Technology", ["Information and Computer Technology", "Internet and Communication Technology", "Information and Control Technology"], "ICT = Information and Communication Technology.", "Overview of computing systems"),
        ("The full meaning of WWW is", "World Wide Web", ["World Wide Website", "Wide World Web", "Web World Wide"], "WWW = World Wide Web.", "Internet"),
        ("The full meaning of URL is", "Uniform Resource Locator", ["Universal Resource Link", "Uniform Resource Link", "Universal Record Locator"], "URL = Uniform Resource Locator.", "Internet"),
        ("The full meaning of HTML is", "HyperText Markup Language", ["HyperText Mark Language", "HighText Markup Language", "Hyperlink Text Markup Language"], "HTML = HyperText Markup Language.", "Internet"),
        ("The full meaning of HTTP is", "HyperText Transfer Protocol", ["HyperText Transmission Program", "HighText Transfer Protocol", "Hyperlink Transfer Protocol"], "HTTP = HyperText Transfer Protocol.", "Internet"),
        ("The device that connects a computer to the internet through a telephone line is the", "Modem", ["Router only", "Monitor", "Scanner"], "A modem modulates and demodulates signals.", "Internet"),
        ("A network that covers a small area such as an office is a", "LAN", ["WAN", "MAN", "Internet"], "LAN = Local Area Network.", "Computer networks"),
        ("LAN stands for", "Local Area Network", ["Large Area Network", "Local Access Network", "Long Area Network"], "LAN = Local Area Network.", "Computer networks"),
        ("WAN stands for", "Wide Area Network", ["World Area Network", "Wide Access Network", "Wireless Area Network"], "WAN = Wide Area Network.", "Computer networks"),
        ("The main function of an antivirus is to", "Detect and remove viruses", ["Increase computer speed", "Store data", "Print documents"], "Antivirus software protects against malware.", "Computer security"),
        ("A computer virus is a", "Program that harms a computer", ["Hardware fault", "Power failure", "Network cable"], "A virus is malicious software.", "Computer security"),
        ("The process of converting data into a secret code is called", "Encryption", ["Decryption", "Compression", "Formatting"], "Encryption protects data by coding it.", "Computer security"),
        ("A password is used for", "Authentication", ["Storage", "Printing", "Formatting"], "Passwords verify a user's identity.", "Computer security"),
        ("Which of the following is a programming language?", "Python", ["Microsoft Excel", "Windows", "Google Chrome"], "Python is a programming language.", "Programming"),
        ("The language that the computer understands directly is", "Machine language", ["Python", "Java", "C++"], "Machine language is binary code the CPU executes directly.", "Programming"),
        ("A program that translates high-level language into machine code at once is a", "Compiler", ["Interpreter", "Assembler", "Debugger"], "A compiler translates the whole program before execution.", "Programming"),
        ("A program that translates and executes code line by line is an", "Interpreter", ["Compiler", "Assembler", "Linker"], "An interpreter executes code line by line.", "Programming"),
        ("The shortcut for copying selected text is", "Ctrl + C", ["Ctrl + V", "Ctrl + X", "Ctrl + Z"], "Ctrl + C copies.", "Application software"),
        ("The shortcut for pasting copied text is", "Ctrl + V", ["Ctrl + C", "Ctrl + X", "Ctrl + P"], "Ctrl + V pastes.", "Application software"),
        ("The shortcut for undoing an action is", "Ctrl + Z", ["Ctrl + Y", "Ctrl + U", "Ctrl + S"], "Ctrl + Z undoes.", "Application software"),
        ("The shortcut for saving a document is", "Ctrl + S", ["Ctrl + P", "Ctrl + O", "Ctrl + N"], "Ctrl + S saves.", "Application software"),
        ("The file extension for a Microsoft Word document is", ".docx", [".xlsx", ".pptx", ".txt"], "Word documents use .docx.", "Application software"),
        ("The file extension for a Microsoft Excel workbook is", ".xlsx", [".docx", ".pptx", ".pdf"], "Excel workbooks use .xlsx.", "Application software"),
        ("The file extension for a PowerPoint presentation is", ".pptx", [".docx", ".xlsx", ".txt"], "PowerPoint uses .pptx.", "Application software"),
        ("Which of the following is a search engine?", "Google", ["Microsoft Word", "Windows", "Linux"], "Google is a search engine.", "Internet"),
        ("An email address must contain the", "@ symbol", ["# symbol", "$ symbol", "% symbol"], "Email addresses use @ to separate user and domain.", "Internet"),
        ("The full meaning of E-mail is", "Electronic mail", ["Express mail", "Electric mail", "Encoded mail"], "E-mail = electronic mail.", "Internet"),
        ("A database is a", "Collection of related data", ["Single file only", "Hardware device", "Programming language"], "A database stores related data in an organised way.", "Databases"),
        ("The software used to manage a database is called a", "DBMS", ["DML", "SQL only", "CPU"], "DBMS = Database Management System.", "Databases"),
        ("SQL stands for", "Structured Query Language", ["Standard Query Language", "Simple Query Language", "System Query Language"], "SQL = Structured Query Language.", "Databases"),
        ("Which of the following is a database management system?", "MySQL", ["Python", "Windows", "Excel only"], "MySQL is a DBMS.", "Databases"),
        ("The process of starting a computer is called", "Booting", ["Formatting", "Installing", "Debugging"], "Booting loads the operating system.", "System software"),
        ("Which of the following is a pointing device?", "Mouse", ["Keyboard", "Monitor", "Printer"], "A mouse points and selects on screen.", "Computing devices: input devices"),
        ("A scanner is a", "Input device", ["Output device", "Storage device", "Processing device"], "A scanner captures images into the computer.", "Computing devices: input devices"),
        ("A speaker is an", "Output device", ["Input device", "Storage device", "Processing device"], "A speaker produces sound output.", "Computing devices: output devices"),
        ("The monitor is also called the", "Visual Display Unit", ["Central Processing Unit", "Arithmetic Logic Unit", "Control Unit"], "Monitor = Visual Display Unit (VDU).", "Computing devices: output devices"),
        ("The ALU performs", "Arithmetic and logical operations", ["Input operations", "Storage operations", "Output operations"], "ALU = Arithmetic Logic Unit.", "Overview of computing systems"),
        ("The control unit of the CPU", "Controls the flow of data", ["Stores data permanently", "Performs calculations", "Displays output"], "The control unit directs operations.", "Overview of computing systems"),
        ("Which of the following is a secondary storage device?", "Flash drive", ["RAM", "Cache", "Register"], "A flash drive stores data permanently.", "Computing devices: storage devices"),
        ("Cache memory is", "Faster than RAM", ["Slower than RAM", "The same as ROM", "External storage"], "Cache is small, fast memory close to the CPU.", "Overview of computing systems"),
        ("A folder is used to", "Organise files", ["Run programs", "Print documents", "Connect to the internet"], "Folders organise files on a computer.", "Operating systems: file management"),
        ("Deleting a file sends it to the", "Recycle Bin", ["Desktop", "Control Panel", "Taskbar"], "Deleted files go to the Recycle Bin.", "Operating systems: file management"),
        ("The part of the computer that displays the desktop is the", "Monitor", ["Keyboard", "Mouse", "CPU"], "The monitor displays output.", "Computing devices: output devices"),
        ("Which of these is a social media platform?", "Facebook", ["Google Chrome", "Microsoft Word", "Linux"], "Facebook is a social media platform.", "Internet"),
        ("The internet is a", "Global network of computers", ["Single computer", "Local network only", "Software program"], "The internet connects networks worldwide.", "Internet"),
        ("A website address is also called a", "URL", ["IP address only", "Email address", "Username"], "A website address is its URL.", "Internet"),
        ("The first page of a website is the", "Home page", ["Web page only", "Search page", "Login page"], "The home page is the main entry page.", "Internet"),
        ("Which of the following is a web browser?", "Mozilla Firefox", ["Microsoft Word", "Notepad", "Paint"], "Firefox is a web browser.", "Internet"),
        ("A computer network that allows sharing of resources is used to", "Share files and printers", ["Increase viruses", "Slow down computers", "Waste electricity"], "Networks share files, printers and internet access.", "Computer networks"),
    ]
    for q, c, ds, e, t in facts:
        add(q, c, ds, e, t)
    for _ in range(25):
        kind = rng.choice(["bin", "dec", "bits"])
        if kind == "bin":
            n = rng.randint(3, 30)
            b = bin(n)[2:]
            add(f"Convert {n} to binary.", b,
                _pick(rng, b, [bin(n + 1)[2:], bin(n - 1)[2:], bin(n + 2)[2:], "101", "1101"]),
                f"{n} in binary is {b}.", "Data representation: number systems")
        elif kind == "dec":
            b = rng.choice(["101", "110", "1010", "1111", "1001", "1100", "10101"])
            v = int(b, 2)
            add(f"Convert {b}\u2082 to decimal.", str(v),
                _dist(rng, v, 3, lo=0), f"{b}\u2082 = {v} in decimal.", "Data representation: number systems")
        elif kind == "bits":
            kb = rng.choice([2, 4, 8, 16])
            add(f"How many bytes are in {kb} kilobytes?", str(kb * 1024),
                _pick(rng, str(kb * 1024), [str(kb * 1000), str(kb * 512), str(kb * 2048)]),
                f"1 KB = 1024 bytes, so {kb} KB = {kb * 1024} bytes.", "Data representation")
    return uniq_pool(P)
