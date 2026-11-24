# Top-up pools for NECO placeholder generator (24 Nov 2026).
# Fills the shortfall between the base+expansion pools and the 160 unique
# standard questions needed per subject (40 x 4 years; English 200 std).
# Executed in the same namespace as gen_base.py, so mk / fmt_num / norm are available.
# Fact items are built from (term, definition) tables with two question forms
# (describe-the-term / name-the-term) so distractors stay in-topic.
# Numeric items are computed in code with varied values; distractors are
# computed wrong-way values, checked distinct by finalise.

def _pairs(subj, topic, items):
    out = []
    for term, defn in items:
        others_def = [d for t, d in items if d != defn][:3]
        out.append(mk(0, subj, topic, f"Which of these best describes {term}?", defn, others_def,
                      f"{term} is {defn}."))
        others_term = [t for t, d in items if t != term][:3]
        out.append(mk(0, subj, topic, f"Which term is described as: {defn}?", term, others_term,
                      f"{defn} describes {term}."))
    return out

def _num(subj, topic, q, correct, distractors, expl):
    return mk(0, subj, topic, q, fmt_num(correct), [fmt_num(d) for d in distractors], expl)

# ---------------- ECONOMICS (numeric) ----------------
def _econ_num():
    P = []
    def add(t, q, c, d, e): P.append(_num("Economics", t, q, c, d, e))
    for dq, dp in [(20, 10), (30, 10), (25, 5), (40, 20), (12, 4), (50, 25)]:
        E = dq / dp
        add("Elasticity", f"If quantity demanded rises by {dq}% when price falls by {dp}%, the price elasticity of demand is:",
            E, [E + 0.5, E * 2, E / 2],
            f"Elasticity = % change in quantity demanded / % change in price = {dq}/{dp} = {fmt_num(E)}.")
    for C, I, G, X, M in [(200, 50, 80, 60, 40), (300, 100, 120, 80, 50), (150, 40, 60, 30, 20),
                          (500, 200, 150, 100, 70), (120, 30, 50, 25, 15), (400, 150, 100, 90, 60)]:
        gdp = C + I + G + X - M
        add("National Income", f"Given consumption N{C}bn, investment N{I}bn, government spending N{G}bn, exports N{X}bn and imports N{M}bn, GDP is:",
            gdp, [gdp + 50, gdp - 50, gdp + 100],
            f"GDP = C + I + G + (X - M) = {C} + {I} + {G} + ({X} - {M}) = N{gdp}bn.")
    for C, S, T in [(120, 30, 20), (200, 50, 40), (90, 20, 10), (350, 80, 70)]:
        Y = C + S + T
        add("National Income", f"If consumption is N{C}bn, savings N{S}bn and taxes N{T}bn, national income is:",
            Y, [Y + 20, Y - 20, Y + 50],
            f"Y = C + S + T = {C} + {S} + {T} = N{Y}bn.")
    for cur, base in [(150, 100), (240, 200), (90, 60), (132, 110), (210, 150)]:
        idx = cur / base * 100
        add("Price Index", f"If the price of a basket of goods rises from N{base} to N{cur}, the price index is:",
            idx, [idx + 10, idx - 10, idx + 25],
            f"Price index = (current price / base price) x 100 = ({cur}/{base}) x 100 = {fmt_num(idx)}.")
    for p, q in [(50, 20), (25, 40), (80, 15), (120, 10), (45, 60), (200, 5)]:
        tr = p * q
        add("Revenue", f"A firm sells {q} units at N{p} each. Its total revenue is:",
            tr, [tr + 200, tr - 200, tr * 2],
            f"Total revenue = price x quantity = {p} x {q} = N{tr}.")
    for tc, q in [(6000, 100), (9000, 150), (4000, 80), (12000, 200), (7500, 150), (10000, 250)]:
        ac = tc / q
        add("Cost", f"If total cost is N{tc} for {q} units, the average cost is:",
            ac, [ac + 10, ac - 10, ac * 2],
            f"Average cost = total cost / output = {tc}/{q} = N{fmt_num(ac)}.")
    for mpc in [0.8, 0.75, 0.6, 0.5, 0.9, 0.7]:
        k = 1 / (1 - mpc)
        add("Multiplier", f"If the marginal propensity to consume is {mpc}, the multiplier is:",
            round(k, 2), [round(k, 2) + 1, round(k, 2) - 0.5, round(k, 2) * 2],
            f"Multiplier = 1/(1 - MPC) = 1/(1 - {mpc}) = {fmt_num(round(k, 2))}.")
    for ni, pop in [(500, 50), (900, 100), (240, 40), (1200, 200), (750, 150), (300, 25)]:
        pc = ni * 1000 // pop
        add("National Income", f"If national income is N{ni} billion and the population is {pop} million, per capita income is:",
            pc, [pc // 10, pc * 10, pc // 2],
            f"Per capita income = national income / population = N{ni}bn / {pop}m = N{pc:,}.")
    for rate, usd in [(1500, 200), (1200, 50), (800, 500), (1600, 25), (1000, 120), (1400, 150)]:
        ngn = rate * usd
        add("Exchange Rate", f"If $1 = N{rate:,}, how many naira is ${usd}?",
            ngn, [ngn // 10, ngn * 2, ngn // 2],
            f"${usd} x N{rate:,} = N{ngn:,}.")
    for u, lf in [(5, 50), (6, 40), (4, 80), (18, 90), (7, 70), (3, 60)]:
        r = u / lf * 100
        add("Unemployment", f"If {u} million people are unemployed out of a labour force of {lf} million, the unemployment rate is:",
            r, [r + 5, r - 2.5, r + 2.5],
            f"Unemployment rate = (unemployed / labour force) x 100 = ({u}/{lf}) x 100 = {fmt_num(r)}%.")
    for c1, c2 in [(120, 132), (150, 180), (80, 100), (200, 240), (90, 99), (160, 200)]:
        inf = (c2 - c1) / c1 * 100
        add("Inflation", f"If the consumer price index rises from {c1} to {c2}, the inflation rate is:",
            inf, [inf + 5, inf - 5, inf * 2],
            f"Inflation rate = (new CPI - old CPI) / old CPI x 100 = ({c2}-{c1})/{c1} x 100 = {fmt_num(inf)}%.")
    for p, r, t in [(20000, 5, 2), (50000, 10, 3), (10000, 8, 4), (40000, 6, 5), (30000, 12, 2), (60000, 4, 3)]:
        I = p * r * t // 100
        add("Interest", f"The simple interest on N{p:,} at {r}% per annum for {t} years is:",
            I, [I + 500, I * 2, I // 2],
            f"Simple interest = (P x R x T)/100 = ({p:,} x {r} x {t})/100 = N{I:,}.")
    for p1, p2, q1, q2 in [(10, 12, 100, 90), (8, 10, 50, 45), (20, 25, 200, 150),
                           (5, 6, 300, 240), (15, 18, 80, 70), (40, 50, 30, 25)]:
        te2 = p2 * q2
        te1 = p1 * q1
        add("Demand", f"When price rises from N{p1} to N{p2}, quantity demanded falls from {q1} to {q2} units. The new total expenditure is:",
            te2, [te1, te2 + 100, te2 * 2],
            f"New total expenditure = new price x new quantity = {p2} x {q2} = N{te2}.")
    return P

def _econ_facts():
    P = []
    P += _pairs("Economics", "Economic Thought", [
        ("Adam Smith", "the economist who wrote 'The Wealth of Nations' in 1776"),
        ("John Maynard Keynes", "the economist who wrote 'The General Theory of Employment, Interest and Money'"),
        ("Thomas Malthus", "the economist known for the theory of population growth"),
        ("David Ricardo", "the economist known for the theory of comparative advantage"),
        ("Alfred Marshall", "the economist who wrote 'Principles of Economics'"),
        ("scarcity", "the fundamental economic problem of limited resources and unlimited wants"),
        ("opportunity cost", "the value of the next best alternative forgone when a choice is made"),
        ("scale of preference", "a list of wants arranged in order of importance"),
    ])
    P += _pairs("Economics", "Markets and Money", [
        ("a monopoly", "a market with only one seller of a product with no close substitutes"),
        ("an oligopoly", "a market dominated by a few large sellers"),
        ("perfect competition", "a market with many buyers and sellers and identical products"),
        ("a normal good", "a good whose demand rises as income rises"),
        ("an inferior good", "a good whose demand falls as income rises"),
        ("complementary goods", "goods that are used together, such as cars and petrol"),
        ("substitute goods", "goods that can replace each other, such as tea and coffee"),
        ("the central bank", "the bank that issues currency and controls the money supply"),
        ("a commercial bank", "a bank that accepts deposits and gives loans to the public"),
        ("inflation", "a persistent rise in the general price level"),
        ("deflation", "a persistent fall in the general price level"),
        ("a tariff", "a tax placed on imported goods"),
    ])
    return P

# ---------------- COMMERCE ----------------
def _commerce_facts():
    P = []
    P += _pairs("Commerce", "Trade Documents", [
        ("an invoice", "a document sent by a seller to a buyer showing goods supplied and the amount due"),
        ("a receipt", "a document acknowledging that payment has been received"),
        ("a credit note", "a document issued to correct an overcharge on an invoice"),
        ("a debit note", "a document issued to correct an undercharge on an invoice"),
        ("a waybill", "a document that accompanies goods in transit and lists them"),
        ("a bill of lading", "a document issued by a shipping company acknowledging receipt of goods for shipment"),
        ("a certificate of origin", "a document showing the country where goods were produced"),
        ("a cheque", "a written order to a bank to pay a stated sum to a named person"),
    ])
    P += _pairs("Commerce", "Business Organisations", [
        ("a sole proprietorship", "a business owned and controlled by one person"),
        ("a partnership", "a business owned by two or more people sharing profits and losses"),
        ("a private limited company", "a company whose shares cannot be offered to the general public"),
        ("a public limited company", "a company whose shares can be offered to the general public"),
        ("a cooperative society", "a business owned by members who join voluntarily to serve their common interests"),
        ("a public corporation", "a business set up by an Act of Parliament and owned by the government"),
    ])
    P += _pairs("Commerce", "Trade and Insurance", [
        ("home trade", "the buying and selling of goods within a country"),
        ("foreign trade", "the buying and selling of goods between countries"),
        ("an import", "a good brought into a country from another country"),
        ("an export", "a good sent out of a country to another country"),
        ("entrepot trade", "trade in which goods are imported and then re-exported"),
        ("utmost good faith", "the insurance principle that both parties must disclose all material facts"),
        ("insurable interest", "the insurance principle that the insured must stand to lose if the insured event occurs"),
        ("indemnity", "the insurance principle of restoring the insured to the position before the loss, no better"),
        ("proximate cause", "the insurance principle that the nearest cause of the loss must be an insured risk"),
        ("contribution", "the insurance principle that insurers share a loss when the same risk is insured with more than one insurer"),
    ])
    P += _pairs("Commerce", "Banking, Transport and Marketing", [
        ("a current account", "a bank account from which money can be withdrawn by cheque at any time"),
        ("a savings account", "a bank account that earns interest and is meant for saving"),
        ("a fixed deposit account", "a bank account in which money is kept for a fixed period at a fixed interest rate"),
        ("an overdraft", "an arrangement allowing a customer to withdraw more than the balance in the account"),
        ("a standing order", "an instruction to a bank to pay a fixed sum regularly to a named person"),
        ("a bank draft", "a cheque drawn by a bank on itself, payable on demand"),
        ("a bonded warehouse", "a warehouse where imported goods are kept until customs duty is paid"),
        ("road transport", "the most flexible means of transport, suitable for short distances"),
        ("air transport", "the fastest but most expensive means of transport"),
        ("water transport", "the cheapest means of transport for bulky goods over long distances"),
        ("the product", "the first element of the marketing mix, being the good or service offered"),
        ("promotion", "the marketing mix element concerned with informing and persuading customers"),
        ("advertising", "a paid form of communication used to promote goods and services"),
        ("a wholesaler", "a middleman who buys in bulk from producers and sells in smaller quantities to retailers"),
        ("a retailer", "a middleman who sells goods in small quantities directly to final consumers"),
    ])
    return P

# ---------------- GOVERNMENT ----------------
def _government_facts():
    P = []
    P += _pairs("Government", "Systems of Government", [
        ("democracy", "a system of government by the whole population, usually through elected representatives"),
        ("a monarchy", "a system of government headed by a king or queen"),
        ("an oligarchy", "a system of government by a small group of people"),
        ("a theocracy", "a system of government by religious leaders claiming divine guidance"),
        ("an autocracy", "a system of government in which one person holds absolute power"),
        ("federalism", "a system in which power is shared between a central government and regional governments"),
        ("a unitary system", "a system in which all powers are concentrated in the central government"),
        ("a confederation", "a loose union of independent states that keep most of their sovereignty"),
    ])
    P += _pairs("Government", "Principles of Government", [
        ("separation of powers", "the division of government powers among the legislature, executive and judiciary"),
        ("checks and balances", "the arrangement by which each organ of government controls the others"),
        ("the rule of law", "the principle that everyone, including rulers, is subject to the law"),
        ("sovereignty", "the supreme power of a state to make and enforce laws within its territory"),
        ("legitimacy", "the general acceptance of a government by the people as rightful"),
        ("a constitution", "the body of rules that defines the structure and powers of government"),
    ])
    P += _pairs("Government", "Elections and Representation", [
        ("franchise", "the right to vote in elections"),
        ("a referendum", "a direct vote by the electorate on a specific political question"),
        ("a plebiscite", "a direct vote of the people on an issue of public importance"),
        ("proportional representation", "an electoral system in which seats are shared in proportion to votes won"),
        ("first-past-the-post", "an electoral system in which the candidate with the most votes wins the seat"),
        ("a by-election", "an election held to fill a vacancy between general elections"),
        ("a constituency", "an electoral district represented by one member in the legislature"),
        ("a manifesto", "a published statement of a political party's aims and policies"),
    ])
    P += _pairs("Government", "Institutions", [
        ("a bicameral legislature", "a legislature made up of two chambers"),
        ("a unicameral legislature", "a legislature made up of one chamber"),
        ("the judiciary", "the organ of government that interprets the law"),
        ("the executive", "the organ of government that implements and enforces the law"),
        ("the civil service", "the body of permanent officials who carry out government policies"),
        ("local government", "the third tier of government closest to the people"),
        ("a political party", "an organised group that seeks to win power through elections"),
        ("a pressure group", "a group that seeks to influence government policy without seeking power"),
    ])
    P += _pairs("Government", "Nigerian Government", [
        ("the 1999 Constitution", "the constitution currently in force in Nigeria"),
        ("the presidential system", "the system of government practised in Nigeria since 1979"),
        ("INEC", "the body responsible for conducting elections in Nigeria"),
        ("federal character", "the principle of fair representation of all parts of Nigeria in public appointments"),
        ("revenue allocation", "the sharing of national revenue among the tiers of government"),
        ("the Fourth Republic", "the democratic era in Nigeria that began in 1999"),
        ("the Senate", "the upper chamber of the National Assembly in Nigeria"),
        ("the House of Representatives", "the lower chamber of the National Assembly in Nigeria"),
    ])
    return P

# ---------------- CIVIC EDUCATION ----------------
def _civic_facts():
    P = []
    P += _pairs("Civic", "Citizenship", [
        ("citizenship by birth", "citizenship acquired by being born in a country or to parents who are citizens"),
        ("citizenship by registration", "citizenship granted to a person who applies and meets stated conditions"),
        ("citizenship by naturalisation", "citizenship granted to an alien after long residence and fulfilment of conditions"),
        ("dual citizenship", "the status of being a citizen of two countries at the same time"),
    ])
    P += _pairs("Civic", "Rights and Duties", [
        ("the right to life", "the fundamental right of every person not to be unlawfully killed"),
        ("freedom of expression", "the right to hold and express opinions without interference"),
        ("freedom of movement", "the right to move freely within a country and to leave and return to it"),
        ("freedom of religion", "the right to practise any religion of one's choice"),
        ("the right to fair hearing", "the right of an accused person to be heard before an impartial court"),
        ("paying tax", "a civic duty by which citizens contribute to government revenue"),
        ("obeying the law", "a civic duty requiring citizens to keep the laws of the land"),
        ("voting", "a civic duty by which citizens choose their leaders"),
    ])
    P += _pairs("Civic", "Values and National Symbols", [
        ("honesty", "the value of being truthful and sincere"),
        ("integrity", "the value of being upright and consistent in moral principles"),
        ("discipline", "the value of self-control and obedience to rules"),
        ("cooperation", "the value of working together for a common purpose"),
        ("tolerance", "the value of accepting the views and beliefs of others"),
        ("patriotism", "the love and loyalty a citizen shows to his or her country"),
        ("the national flag", "the green-white-green symbol of Nigeria"),
        ("the coat of arms", "the national symbol bearing an eagle, horses and the motto 'Unity and Faith, Peace and Progress'"),
        ("the national anthem", "the song that expresses the ideals and aspirations of a nation"),
        ("the national pledge", "the promise of loyalty recited by Nigerians to their country"),
    ])
    P += _pairs("Civic", "Social Issues", [
        ("drug abuse", "the harmful use of drugs without medical advice"),
        ("cultism", "the practice of belonging to a secret society, often violent, in schools"),
        ("examination malpractice", "cheating or other dishonest conduct in examinations"),
        ("corruption", "the abuse of public office for private gain"),
        ("human trafficking", "the illegal movement of people for exploitation"),
        ("HIV/AIDS", "a disease that weakens the body's immune system and is spread mainly through infected blood and sexual contact"),
        ("traffic rules", "the regulations that guide the safe use of roads"),
        ("youth empowerment", "programmes that give young people skills and opportunities to be self-reliant"),
    ])
    P += _pairs("Civic", "Institutions and Governance", [
        ("the NYSC", "the scheme that requires Nigerian graduates to serve the nation for one year"),
        ("the Nigerian Police", "the body responsible for maintaining law and order"),
        ("the judiciary", "the arm of government that interprets the law and settles disputes"),
        ("the EFCC", "the agency that investigates and prosecutes economic and financial crimes"),
        ("good governance", "government that is transparent, accountable and responsive to the people"),
        ("accountability", "the obligation of public officers to answer for their actions"),
    ])
    return P

# ---------------- CRS ----------------
def _crs_facts():
    P = []
    P += _pairs("CRS", "Patriarchs and Leaders", [
        ("Abraham", "the patriarch called by God to leave his country and become the father of many nations"),
        ("Isaac", "the son of Abraham and Sarah, born in their old age"),
        ("Jacob", "the patriarch whose twelve sons became the twelve tribes of Israel"),
        ("Joseph", "the son of Jacob who was sold into slavery and later became governor of Egypt"),
        ("Moses", "the leader who led the Israelites out of Egypt"),
        ("Joshua", "the leader who succeeded Moses and led Israel into Canaan"),
    ])
    P += _pairs("CRS", "Kings and Prophets", [
        ("Saul", "the first king of Israel"),
        ("David", "the shepherd boy who became king of Israel and wrote many psalms"),
        ("Solomon", "the king of Israel known for his wisdom and for building the temple"),
        ("Isaiah", "the prophet who foretold the coming of the Messiah"),
        ("Jeremiah", "the prophet known as the weeping prophet"),
        ("Amos", "the prophet who preached justice and righteousness in Israel"),
    ])
    P += _pairs("CRS", "Parables and Miracles", [
        ("the Good Samaritan", "the parable of a man who helped a wounded traveller neglected by others"),
        ("the Prodigal Son", "the parable of a son who wasted his inheritance and was welcomed back by his father"),
        ("the Sower", "the parable of seed falling on different kinds of soil"),
        ("the Mustard Seed", "the parable of the smallest seed growing into a great tree, like the kingdom of God"),
        ("the Talents", "the parable of servants given money to use profitably for their master"),
        ("the feeding of the 5,000", "the miracle in which Jesus fed a great crowd with five loaves and two fish"),
        ("walking on water", "the miracle in which Jesus walked on the Sea of Galilee"),
        ("the raising of Lazarus", "the miracle in which Jesus brought his friend Lazarus back to life"),
        ("turning water into wine", "the first miracle of Jesus, performed at a wedding in Cana"),
    ])
    P += _pairs("CRS", "Events and People", [
        ("the creation", "the account of God making the heavens, the earth and all living things"),
        ("the Exodus", "the departure of the Israelites from Egypt under Moses"),
        ("the Ten Commandments", "the laws given to Moses on Mount Sinai"),
        ("the birth of Jesus", "the event announced to Mary by the angel Gabriel and fulfilled in Bethlehem"),
        ("the crucifixion", "the death of Jesus on the cross at Calvary"),
        ("the resurrection", "the rising of Jesus from the dead on the third day"),
        ("Pentecost", "the day the Holy Spirit came upon the apostles"),
        ("Peter", "the apostle who denied Jesus three times and later preached at Pentecost"),
        ("Paul", "the apostle who persecuted Christians before his conversion on the road to Damascus"),
        ("John the Baptist", "the prophet who baptised Jesus in the River Jordan"),
    ])
    return P

# ---------------- IRS ----------------
def _irs_facts():
    P = []
    P += _pairs("IRS", "Pillars of Islam", [
        ("Shahada", "the declaration of faith that there is no god but Allah and Muhammad is His messenger"),
        ("Salat", "the five daily prayers in Islam"),
        ("Zakat", "the compulsory almsgiving of a portion of one's wealth to the poor"),
        ("Sawm", "the fasting observed during the month of Ramadan"),
        ("Hajj", "the pilgrimage to Makkah which every able Muslim should perform once in a lifetime"),
    ])
    P += _pairs("IRS", "Articles of Faith", [
        ("Tawhid", "the belief in the oneness of Allah"),
        ("the angels", "the beings created from light who carry out Allah's commands, including Jibril"),
        ("the prophets", "the messengers sent by Allah to guide mankind"),
        ("the holy books", "the revelations of Allah, including the Qur'an, the Torah, the Psalms and the Gospel"),
        ("the Day of Judgement", "the day on which all people will be judged for their deeds"),
        ("Qadar", "the belief in Allah's divine decree"),
    ])
    P += _pairs("IRS", "Prophets", [
        ("Adam", "the first man and first prophet in Islam"),
        ("Nuh", "the prophet who built the ark to save believers from the flood"),
        ("Ibrahim", "the prophet who was willing to sacrifice his son in obedience to Allah"),
        ("Musa", "the prophet to whom the Torah was revealed and who led the Israelites out of Egypt"),
        ("Isa", "the prophet born to Maryam and given the Gospel"),
        ("Muhammad", "the last prophet, to whom the Qur'an was revealed"),
    ])
    P += _pairs("IRS", "Islamic History", [
        ("the Hijra", "the migration of the Prophet Muhammad from Makkah to Madinah in 622 CE"),
        ("the Battle of Badr", "the first major battle of the Muslims, fought in 624 CE"),
        ("the Battle of Uhud", "the battle fought in 625 CE in which the Muslims suffered a setback"),
        ("the Treaty of Hudaybiyyah", "the peace agreement between the Muslims and the Quraysh in 628 CE"),
        ("Abubakar", "the first caliph after the death of the Prophet Muhammad"),
        ("Umar", "the second caliph, known for justice and the expansion of Islam"),
    ])
    P += _pairs("IRS", "Practices and Worship", [
        ("wudu", "the ritual ablution performed before prayer"),
        ("Ramadan", "the ninth month of the Islamic calendar, observed with fasting"),
        ("Eid al-Fitr", "the festival marking the end of Ramadan"),
        ("Eid al-Adha", "the festival of sacrifice during Hajj"),
        ("the mosque", "the place of worship for Muslims"),
        ("the imam", "the leader of congregational prayer in a mosque"),
        ("the Kaaba", "the sacred house in Makkah towards which Muslims face in prayer"),
    ])
    return P

# ---------------- AGRICULTURAL SCIENCE ----------------
def _agric_facts():
    P = []
    P += _pairs("Agric", "Soil", [
        ("sandy soil", "a soil with large particles, good drainage and poor water retention"),
        ("clay soil", "a soil with tiny particles, poor drainage and good water retention"),
        ("loamy soil", "the best soil for farming, with a balance of sand, silt and clay"),
        ("humus", "the dark organic matter in soil formed from decayed plants and animals"),
        ("soil pH", "the measure of the acidity or alkalinity of soil"),
    ])
    P += _pairs("Agric", "Crops", [
        ("maize", "a cereal crop used as food for man and feed for livestock"),
        ("rice", "a cereal crop grown mainly in swampy areas"),
        ("millet", "a cereal crop that grows well in dry areas"),
        ("sorghum", "a cereal crop also known as guinea corn"),
        ("cowpea", "a leguminous crop that adds nitrogen to the soil"),
        ("groundnut", "a leguminous oil crop grown for its seeds"),
        ("yam", "a root crop that is a staple food in West Africa"),
        ("cassava", "a root crop from which garri and starch are made"),
    ])
    P += _pairs("Agric", "Livestock, Diseases and Pests", [
        ("cattle", "livestock kept for beef, milk and draught purposes"),
        ("poultry", "birds such as chickens kept for eggs and meat"),
        ("fish farming", "the rearing of fish in ponds, also called aquaculture"),
        ("Newcastle disease", "a viral disease of poultry that causes heavy losses"),
        ("foot-and-mouth disease", "a viral disease affecting cattle, sheep and goats"),
        ("coccidiosis", "a disease of poultry caused by a protozoan parasite"),
        ("the stem borer", "an insect pest that bores into the stems of cereal crops"),
        ("the armyworm", "an insect pest that feeds on the leaves of crops in large numbers"),
        ("aphids", "small insects that suck sap from plants and spread diseases"),
    ])
    P += _pairs("Agric", "Farming Practices and Animal Husbandry", [
        ("crop rotation", "the practice of growing different crops on the same land in successive seasons"),
        ("mixed cropping", "the practice of growing two or more crops on the same land at the same time"),
        ("intercropping", "the practice of growing two crops together with one as the main crop"),
        ("irrigation", "the artificial application of water to farmland"),
        ("a hoe", "a farm tool used for tilling and weeding"),
        ("a cutlass", "a farm tool used for clearing bushes and harvesting"),
        ("a tractor", "a farm machine used for ploughing and pulling implements"),
        ("gestation", "the period between mating and birth in animals"),
        ("weaning", "the separation of young animals from their mothers at the end of suckling"),
        ("castration", "the removal of the testes of a male animal to prevent breeding"),
        ("vaccination", "the giving of a vaccine to protect animals against disease"),
        ("dehorning", "the removal of the horns of farm animals"),
    ])
    return P

# ---------------- ACCOUNTING (numeric + facts) ----------------
def _accounting_num():
    P = []
    def add(t, q, c, d, e): P.append(_num("Accounting", t, q, c, d, e))
    for cost, scrap, life in [(10000, 2000, 4), (20000, 4000, 8), (15000, 3000, 6),
                              (50000, 10000, 10), (12000, 0, 4), (30000, 6000, 8)]:
        dep = (cost - scrap) // life
        add("Depreciation", f"A machine costs N{cost:,} with a scrap value of N{scrap:,} and a useful life of {life} years. The annual depreciation by the straight-line method is:",
            dep, [dep + 500, dep * 2, dep // 2],
            f"Straight-line depreciation = (cost - scrap value) / useful life = ({cost:,} - {scrap:,}) / {life} = N{dep:,}.")
    for cost, rate in [(20000, 10), (50000, 20), (10000, 25), (40000, 10)]:
        dep = cost * rate // 100
        add("Depreciation", f"A machine costs N{cost:,}. The first year's depreciation at {rate}% on the reducing-balance method is:",
            dep, [dep + 1000, dep * 2, dep // 2],
            f"Reducing-balance depreciation = cost x rate = {cost:,} x {rate}% = N{dep:,}.")
    for sales, cogs in [(50000, 30000), (80000, 45000), (120000, 70000), (60000, 35000)]:
        gp = sales - cogs
        add("Final Accounts", f"A trader's sales are N{sales:,} and cost of goods sold is N{cogs:,}. The gross profit is:",
            gp, [gp + 5000, gp - 5000, gp * 2],
            f"Gross profit = sales - cost of goods sold = {sales:,} - {cogs:,} = N{gp:,}.")
    for gp, exp in [(20000, 8000), (35000, 15000), (50000, 20000), (25000, 9000)]:
        np_ = gp - exp
        add("Final Accounts", f"If gross profit is N{gp:,} and total expenses are N{exp:,}, the net profit is:",
            np_, [np_ + 2000, np_ - 2000, np_ * 2],
            f"Net profit = gross profit - expenses = {gp:,} - {exp:,} = N{np_:,}.")
    for ca, cl in [(60000, 30000), (90000, 30000), (50000, 25000), (120000, 40000)]:
        r = ca / cl
        add("Ratios", f"If current assets are N{ca:,} and current liabilities are N{cl:,}, the current ratio is:",
            r, [r + 1, r - 0.5, r * 2],
            f"Current ratio = current assets / current liabilities = {ca:,}/{cl:,} = {fmt_num(r)}:1.")
    for ca, stock, cl in [(60000, 20000, 20000), (90000, 30000, 30000), (80000, 40000, 20000), (50000, 10000, 20000)]:
        r = (ca - stock) / cl
        add("Ratios", f"Current assets are N{ca:,}, stock is N{stock:,} and current liabilities are N{cl:,}. The acid-test ratio is:",
            r, [r + 1, r - 0.5, r * 2],
            f"Acid-test ratio = (current assets - stock) / current liabilities = ({ca:,} - {stock:,})/{cl:,} = {fmt_num(r)}:1.")
    for ca, cl in [(60000, 30000), (90000, 40000), (50000, 20000), (120000, 70000)]:
        wc = ca - cl
        add("Ratios", f"If current assets are N{ca:,} and current liabilities are N{cl:,}, the working capital is:",
            wc, [wc + 10000, wc - 10000, wc * 2],
            f"Working capital = current assets - current liabilities = {ca:,} - {cl:,} = N{wc:,}.")
    for cost, pct in [(20000, 25), (40000, 20), (10000, 50), (60000, 10)]:
        mu = cost * pct // 100
        add("Final Accounts", f"Goods costing N{cost:,} are sold at a mark-up of {pct}%. The mark-up is:",
            mu, [mu + 1000, mu * 2, mu // 2],
            f"Mark-up = cost x mark-up % = {cost:,} x {pct}% = N{mu:,}.")
    for assets, liab in [(150000, 60000), (200000, 80000), (90000, 30000), (300000, 120000)]:
        cap = assets - liab
        add("Balance Sheet", f"If total assets are N{assets:,} and total liabilities are N{liab:,}, the capital is:",
            cap, [cap + 10000, cap - 10000, cap * 2],
            f"Capital = total assets - total liabilities = {assets:,} - {liab:,} = N{cap:,}.")
    for bal, rate in [(100000, 5), (200000, 10), (50000, 8), (80000, 5)]:
        disc = bal * rate // 100
        add("Discounts", f"A debt of N{bal:,} is settled with a cash discount of {rate}%. The discount allowed is:",
            disc, [disc + 1000, disc * 2, disc // 2],
            f"Discount = debt x rate = {bal:,} x {rate}% = N{disc:,}.")
    return P

def _accounting_facts():
    return _pairs("Accounting", "Bookkeeping", [
        ("double entry", "the principle that every transaction is recorded twice, as a debit and a credit"),
        ("a debit", "an entry on the left-hand side of an account"),
        ("a credit", "an entry on the right-hand side of an account"),
        ("a ledger", "the book in which accounts are kept"),
        ("a trial balance", "a list of debit and credit balances used to check the arithmetical accuracy of the ledger"),
        ("a balance sheet", "a statement showing the assets, liabilities and capital of a business at a given date"),
        ("depreciation", "the fall in the value of a fixed asset due to use and passage of time"),
        ("a bad debt", "a debt that cannot be collected from a debtor"),
    ])

# ---------------- COMPUTER STUDIES ----------------
def _computer_num():
    P = []
    def add(t, q, c, d, e): P.append(_num("Computer", t, q, c, d, e))
    for b, dec in [("1010", 10), ("1100", 12), ("10101", 21), ("1111", 15), ("100000", 32), ("11010", 26)]:
        add("Number Systems", f"What is the decimal equivalent of the binary number {b}?",
            dec, [dec + 2, dec - 2, dec * 2],
            f"{b} in binary = {dec} in decimal.")
    for dec, b in [(9, "1001"), (13, "1101"), (18, "10010"), (25, "11001"), (7, "111"), (20, "10100")]:
        add("Number Systems", f"What is the binary equivalent of the decimal number {dec}?",
            b, [b + "0", b[:-1] + ("1" if b[-1] == "0" else "0"), "1" + b],
            f"{dec} in decimal = {b} in binary.")
    return P

def _computer_facts():
    P = []
    P += _pairs("Computer", "Hardware", [
        ("the CPU", "the part of the computer that carries out instructions, also called the processor"),
        ("the ALU", "the part of the CPU that performs arithmetic and logical operations"),
        ("RAM", "the temporary memory that loses its contents when the computer is switched off"),
        ("ROM", "the permanent memory that stores instructions needed to start the computer"),
        ("the keyboard", "an input device used for typing data into a computer"),
        ("the monitor", "an output device that displays information on a screen"),
        ("a printer", "an output device that produces hard copies of documents"),
        ("a scanner", "an input device that copies images and documents into a computer"),
        ("a hard disk", "a storage device that holds large amounts of data permanently"),
        ("a flash drive", "a small portable storage device that plugs into a USB port"),
    ])
    P += _pairs("Computer", "Software and Data", [
        ("an operating system", "the software that manages the hardware and other programs of a computer"),
        ("application software", "software designed to perform a specific task for the user, such as word processing"),
        ("a bit", "the smallest unit of data in a computer, being 0 or 1"),
        ("a byte", "a unit of data made up of eight bits"),
        ("a kilobyte", "a unit of data equal to 1,024 bytes"),
        ("a megabyte", "a unit of data equal to 1,024 kilobytes"),
        ("a gigabyte", "a unit of data equal to 1,024 megabytes"),
        ("a computer virus", "a harmful program that spreads and damages files or systems"),
    ])
    P += _pairs("Computer", "Networks and Internet", [
        ("a LAN", "a network connecting computers within a small area such as an office"),
        ("a WAN", "a network connecting computers over a large geographical area"),
        ("a star topology", "a network arrangement in which all computers connect to a central device"),
        ("a bus topology", "a network arrangement in which all computers share a single cable"),
        ("a web browser", "a program used to access and view pages on the internet"),
        ("an email", "a message sent electronically from one computer user to another"),
    ])
    return P

# ---------------- BIOLOGY ----------------
def _biology_facts():
    P = []
    P += _pairs("Biology", "Cell Biology", [
        ("the mitochondria", "the organelle that releases energy in respiration, known as the powerhouse of the cell"),
        ("the ribosome", "the organelle where protein synthesis takes place"),
        ("the nucleus", "the organelle that controls all cell activities and contains genetic material"),
        ("the chloroplast", "the organelle where photosynthesis takes place in plant cells"),
        ("the vacuole", "the organelle that stores water and other substances in a cell"),
        ("the cell membrane", "the structure that controls what enters and leaves a cell"),
        ("the cytoplasm", "the jelly-like substance in which cell organelles are suspended"),
    ])
    P += _pairs("Biology", "Genetics and Ecology", [
        ("a gene", "a unit of inheritance that determines a characteristic"),
        ("an allele", "one of the alternative forms of a gene"),
        ("a genotype", "the genetic make-up of an organism"),
        ("a phenotype", "the observable characteristics of an organism"),
        ("a chromosome", "a thread-like structure in the nucleus that carries genes"),
        ("a dominant trait", "a trait that is expressed even when only one copy of the gene is present"),
        ("a recessive trait", "a trait that is expressed only when two copies of the gene are present"),
        ("an ecosystem", "a community of organisms interacting with their environment"),
        ("a habitat", "the place where an organism lives"),
        ("a population", "all the members of one species living in a particular area"),
        ("a food chain", "a series of organisms through which food energy passes"),
        ("a food web", "a network of interconnected food chains in an ecosystem"),
        ("a producer", "an organism, usually a green plant, that makes its own food"),
    ])
    P += _pairs("Biology", "Human Biology", [
        ("insulin", "the hormone that lowers blood sugar level"),
        ("adrenaline", "the hormone that prepares the body for emergency action"),
        ("thyroxine", "the hormone that controls the rate of metabolism"),
        ("amylase", "the enzyme that digests starch in the mouth and small intestine"),
        ("pepsin", "the enzyme that digests protein in the stomach"),
        ("haemoglobin", "the pigment in red blood cells that carries oxygen"),
        ("a neuron", "a nerve cell that carries impulses in the body"),
        ("a nephron", "the functional unit of the kidney that filters blood"),
    ])
    return P

# ---------------- HISTORY ----------------
def _history_facts():
    P = []
    P += _pairs("History", "Pre-Colonial Nigeria", [
        ("the Oyo Empire", "a powerful Yoruba empire that flourished in the 17th and 18th centuries"),
        ("the Benin Empire", "an Edo kingdom famous for its bronze art and the Oba's palace"),
        ("the Sokoto Caliphate", "the Islamic state founded by Usman dan Fodio after the jihad of 1804"),
        ("Kanem-Bornu", "an empire around Lake Chad known for the trans-Saharan trade"),
        ("the Nok culture", "an ancient Nigerian culture known for its terracotta sculptures"),
        ("the trans-Saharan trade", "the trade across the Sahara linking West Africa with North Africa"),
    ])
    P += _pairs("History", "Colonial Nigeria", [
        ("indirect rule", "the system by which Britain governed Nigeria through traditional rulers"),
        ("the amalgamation of 1914", "the joining of the Northern and Southern Protectorates of Nigeria by Lord Lugard"),
        ("the Clifford Constitution of 1922", "the constitution that introduced the elective principle in Nigeria"),
        ("the Richards Constitution of 1946", "the constitution that introduced regional councils in Nigeria"),
        ("the Macpherson Constitution of 1951", "the constitution that gave Nigerians a greater share in government"),
        ("the Lyttleton Constitution of 1954", "the constitution that introduced a federal system in Nigeria"),
    ])
    P += _pairs("History", "Nationalists and Independence", [
        ("Herbert Macaulay", "the Nigerian nationalist known as the father of Nigerian nationalism"),
        ("Nnamdi Azikiwe", "the first President of Nigeria and leader of the NCNC"),
        ("Obafemi Awolowo", "the leader of the Action Group and first Premier of the Western Region"),
        ("Ahmadu Bello", "the Sardauna of Sokoto and first Premier of the Northern Region"),
        ("Nigerian independence", "the event of 1 October 1960, when Nigeria became an independent nation"),
        ("the Nigerian republic", "the status Nigeria attained on 1 October 1963"),
        ("the Nigerian Civil War", "the war of 1967 to 1970 between the Federal Government and Biafra"),
        ("the Fourth Republic", "the democratic era in Nigeria that began on 29 May 1999"),
    ])
    return P

# ---------------- PHYSICS (numeric) ----------------
def _physics_num():
    P = []
    def add(t, q, c, d, e): P.append(_num("Physics", t, q, c, d, e))
    for F, d in [(50, 4), (20, 10), (100, 2.5)]:
        W = F * d
        add("Work and Energy", f"A force of {fmt_num(F)} N moves an object {fmt_num(d)} m. The work done is:",
            W, [W + 50, W * 2, W / 2],
            f"Work = force x distance = {fmt_num(F)} x {fmt_num(d)} = {fmt_num(W)} J.")
    for W, t in [(600, 10), (1200, 20), (500, 5)]:
        Pw = W / t
        add("Work and Energy", f"A machine does {W} J of work in {t} s. Its power is:",
            Pw, [Pw + 10, Pw * 2, Pw / 2],
            f"Power = work / time = {W}/{t} = {fmt_num(Pw)} W.")
    for m, v in [(2, 10), (4, 5), (10, 2)]:
        ke = 0.5 * m * v * v
        add("Work and Energy", f"A body of mass {m} kg moves with a velocity of {v} m/s. Its kinetic energy is:",
            ke, [ke + 10, ke * 2, ke / 2],
            f"Kinetic energy = 1/2 mv^2 = 0.5 x {m} x {v}^2 = {fmt_num(ke)} J.")
    for m, h in [(5, 10), (2, 20)]:
        pe = m * 10 * h
        add("Work and Energy", f"A body of mass {m} kg is raised {h} m above the ground. Its potential energy is: (g = 10 m/s^2)",
            pe, [pe + 100, pe * 2, pe / 2],
            f"Potential energy = mgh = {m} x 10 x {h} = {pe} J.")
    for m, v in [(5, 4), (10, 3)]:
        p = m * v
        add("Motion", f"A body of mass {m} kg moves with a velocity of {v} m/s. Its momentum is:",
            p, [p + 10, p * 2, p / 2],
            f"Momentum = mass x velocity = {m} x {v} = {p} kg m/s.")
    for m, V in [(200, 50), (500, 100)]:
        rho = m / V
        add("Density", f"A substance of mass {m} g occupies a volume of {V} cm^3. Its density is:",
            rho, [rho + 1, rho * 2, rho / 2],
            f"Density = mass / volume = {m}/{V} = {fmt_num(rho)} g/cm^3.")
    for F, A in [(100, 5), (200, 4)]:
        pr = F / A
        add("Pressure", f"A force of {F} N acts on an area of {A} m^2. The pressure is:",
            pr, [pr + 10, pr * 2, pr / 2],
            f"Pressure = force / area = {F}/{A} = {fmt_num(pr)} Pa.")
    for f, lam in [(50, 2), (100, 0.5)]:
        v = f * lam
        add("Waves", f"A wave has a frequency of {f} Hz and a wavelength of {fmt_num(lam)} m. Its speed is:",
            v, [v + 20, v * 2, v / 2],
            f"Wave speed = frequency x wavelength = {f} x {fmt_num(lam)} = {fmt_num(v)} m/s.")
    for I, R in [(2, 10), (0.5, 20)]:
        V = I * R
        add("Electricity", f"A current of {fmt_num(I)} A flows through a resistor of {R} ohms. The voltage across it is:",
            V, [V + 5, V * 2, V / 2],
            f"V = IR = {fmt_num(I)} x {R} = {fmt_num(V)} V.")
    for V, I in [(12, 2), (240, 0.5)]:
        Pw = V * I
        add("Electricity", f"An appliance works on {fmt_num(V)} V and draws {fmt_num(I)} A. The power consumed is:",
            Pw, [Pw + 6, Pw * 2, Pw / 2],
            f"Power = VI = {fmt_num(V)} x {fmt_num(I)} = {fmt_num(Pw)} W.")
    for m, dt in [(2, 10), (1, 5)]:
        Q = m * 4200 * dt
        add("Heat", f"How much heat is needed to raise {m} kg of water by {dt} degrees? (specific heat capacity of water = 4200 J/kgK)",
            Q, [Q + 10000, Q * 2, Q / 2],
            f"Q = mc change in temperature = {m} x 4200 x {dt} = {Q:,} J.")
    for m in [10, 5]:
        w = m * 10
        add("Motion", f"The weight of a body of mass {m} kg is: (g = 10 m/s^2)",
            w, [w + 20, w * 2, w / 2],
            f"Weight = mg = {m} x 10 = {w} N.")
    return P

# ---------------- CHEMISTRY (numeric) ----------------
def _chemistry_num():
    P = []
    def add(t, q, c, d, e): P.append(_num("Chemistry", t, q, c, d, e))
    for formula, mr, atoms in [
            ("H2SO4", 98, "H=1, O=16, S=32"), ("NaCl", 58.5, "Na=23, Cl=35.5"),
            ("CaCO3", 100, "Ca=40, C=12, O=16"), ("CO2", 44, "C=12, O=16"),
            ("NH3", 17, "N=14, H=1"), ("CH4", 16, "C=12, H=1"),
            ("H2O", 18, "H=1, O=16"), ("HNO3", 63, "H=1, N=14, O=16")]:
        add("Moles and Mass", f"What is the relative molecular mass of {formula}? ({atoms})",
            mr, [mr + 2, mr * 2, mr / 2],
            f"Relative molecular mass of {formula} = {fmt_num(mr)}.")
    for mass, mr, name in [(98, 98, "H2SO4"), (49, 98, "H2SO4"), (196, 98, "H2SO4"),
                           (10, 40, "NaOH"), (80, 40, "NaOH"), (20, 40, "NaOH")]:
        n = mass / mr
        add("Moles and Mass", f"How many moles are in {mass} g of {name}? (Mr of {name} = {mr})",
            n, [n + 0.25, n + 1, n / 2],
            f"Moles = mass / Mr = {mass}/{mr} = {fmt_num(n)} mol.")
    for n, vol in [(1, 1), (2, 4), (0.5, 2), (3, 2)]:
        conc = n / vol
        add("Moles and Mass", f"What is the concentration of a solution containing {fmt_num(n)} mol in {fmt_num(vol)} dm^3?",
            conc, [conc + 0.25, conc + 1, conc / 2],
            f"Concentration = moles / volume = {fmt_num(n)}/{fmt_num(vol)} = {fmt_num(conc)} mol/dm^3.")
    for n, vol in [(1, 22.4), (2, 44.8)]:
        add("Moles and Mass", f"What volume does {fmt_num(n)} mol of a gas occupy at s.t.p.? (molar volume = 22.4 dm^3)",
            vol, [vol + 5, vol * 2, vol / 2],
            f"Volume = moles x molar volume = {fmt_num(n)} x 22.4 = {fmt_num(vol)} dm^3.")
    return P

# ---------------- FURTHER MATHEMATICS (numeric) ----------------
def _furthermath_num():
    P = []
    def add(t, q, c, d, e): P.append(_num("FurtherMath", t, q, c, d, e))
    for a, d, n in [(3, 4, 10), (5, 3, 8), (2, 5, 12), (10, -2, 6)]:
        t = a + (n - 1) * d
        add("Sequences and Series", f"In an arithmetic progression with first term {a} and common difference {d}, the {n}th term is:",
            t, [t + 4, t - 4, t + 10],
            f"nth term = a + (n-1)d = {a} + ({n}-1) x {d} = {t}.")
    for a, r, n in [(2, 3, 4), (3, 2, 5), (1, 4, 3), (5, 2, 4)]:
        t = a * r ** (n - 1)
        add("Sequences and Series", f"In a geometric progression with first term {a} and common ratio {r}, the {n}th term is:",
            t, [t + 6, t - 6, t * 2],
            f"nth term = ar^(n-1) = {a} x {r}^({n}-1) = {t}.")
    for a, d, n in [(1, 2, 10), (2, 3, 5)]:
        s = n / 2 * (2 * a + (n - 1) * d)
        add("Sequences and Series", f"The sum of the first {n} terms of an arithmetic progression with first term {a} and common difference {d} is:",
            s, [s + 10, s - 10, s * 2],
            f"Sum = n/2 [2a + (n-1)d] = {n}/2 [2 x {a} + ({n}-1) x {d}] = {fmt_num(s)}.")
    for a, r, n in [(1, 2, 4), (3, 2, 3)]:
        s = a * (r ** n - 1) // (r - 1)
        add("Sequences and Series", f"The sum of the first {n} terms of a geometric progression with first term {a} and common ratio {r} is:",
            s, [s + 5, s - 5, s * 2],
            f"Sum = a(r^n - 1)/(r - 1) = {a}({r}^{n} - 1)/({r} - 1) = {s}.")
    import math as _math
    for n, r, val, kind in [(5, 2, 10, "C"), (6, 3, 20, "C"), (5, 2, 20, "P"), (6, 2, 30, "P")]:
        if kind == "C":
            q = f"What is the value of {n}C{r}?"
            expl = f"{n}C{r} = {n}!/({r}!({n}-{r})!) = {val}."
        else:
            q = f"What is the value of {n}P{r}?"
            expl = f"{n}P{r} = {n}!/({n}-{r})! = {val}."
        add("Permutations and Combinations", q, val, [val + 5, val - 5, val * 2], expl)
    for a, b, c, d, det in [(2, 3, 1, 4, 5), (5, 2, 3, 1, -1)]:
        add("Matrices", f"What is the determinant of the matrix [[{a}, {b}], [{c}, {d}]]?",
            det, [det + 2, det - 2, det * 2],
            f"Determinant = ad - bc = {a} x {d} - {b} x {c} = {det}.")
    for x, y in [(3, 4), (5, 12)]:
        mod = int((x * x + y * y) ** 0.5)
        add("Complex Numbers", f"What is the modulus of {x} + {y}i?",
            mod, [mod + 2, mod - 2, mod * 2],
            f"Modulus = sqrt({x}^2 + {y}^2) = sqrt({x*x + y*y}) = {mod}.")
    for base, val, ans in [(2, 32, 5), (10, 1000, 3)]:
        add("Logarithms", f"What is log{base}({val})?",
            ans, [ans + 1, ans - 1, ans * 2],
            f"log{base}({val}) = {ans} because {base}^{ans} = {val}.")
    add("Trigonometry", "What is sin 30 degrees?", 0.5, [0.87, 1, 0],
        "sin 30 degrees = 0.5.")
    add("Trigonometry", "What is tan 45 degrees?", 1, [0, 0.5, 1.73],
        "tan 45 degrees = 1.")
    return P

# ---------------- ENGLISH (top-up) ----------------
def _english_topup():
    P = []
    def add(t, q, c, d, e): P.append(mk(0, "English", t, q, c, d, e))
    for correct, wrongs in [
            ("necessary", ["neccessary", "necesary", "neccesary"]),
            ("embarrass", ["embarass", "embarras", "embarasss"]),
            ("recommend", ["recomend", "reccomend", "recommand"]),
            ("definitely", ["definately", "definitelyy", "definetly"]),
            ("government", ["goverment", "governement", "govermentt"]),
            ("environment", ["enviroment", "enviornment", "enviromentt"]),
            ("conscience", ["concscience", "consciense", "consience"]),
            ("privilege", ["priviledge", "privilage", "privalege"])]:
        add("Lexis and Structure", "Choose the correctly spelt word:", correct, wrongs,
            f"'{correct}' is the correct spelling.")
    agree = [
        ("Neither of the answers _____ correct.", "is", ["are", "was", "were"], "'Neither' is singular."),
        ("The news _____ good.", "is", ["are", "were", "have"], "'News' is singular."),
        ("Five thousand naira _____ a lot of money.", "is", ["are", "were", "have"], "A sum of money is singular."),
        ("The team _____ won the match.", "has", ["have", "had", "is"], "The team acts as one body here."),
        ("Bread and butter _____ my breakfast.", "is", ["are", "were", "have"], "Bread and butter is one item here."),
        ("Each student _____ to come early.", "is", ["are", "were", "have"], "'Each' is singular."),
        ("Politics _____ an interesting subject.", "is", ["are", "were", "have"], "'Politics' as a subject is singular."),
        ("The number of students _____ large.", "is", ["are", "were", "have"], "'The number' is singular."),
        ("A number of students _____ present.", "are", ["is", "was", "has"], "'A number' takes a plural verb."),
    ]
    for q, c, d, e in agree:
        add("Lexis and Structure", q, c, d, e)
    return P

# ---------------- LITERATURE (top-up) ----------------
def _literature_topup():
    P = []
    P += _pairs("Literature", "Literary Devices", [
        ("a simile", "a figure of speech comparing two things using 'like' or 'as'"),
        ("a metaphor", "a figure of speech that describes one thing as another"),
        ("personification", "a figure of speech that gives human qualities to non-human things"),
        ("alliteration", "the repetition of the same consonant sound at the start of nearby words"),
        ("irony", "a statement that means the opposite of what is said"),
        ("hyperbole", "deliberate exaggeration for effect"),
        ("an oxymoron", "two contradictory words used together, such as 'deafening silence'"),
        ("onomatopoeia", "a word that imitates the sound it describes, such as 'buzz'"),
        ("rhyme", "words with the same ending sound, such as 'day' and 'play'"),
        ("a stanza", "a group of lines forming a unit in a poem"),
    ])
    for title, author, others in [
            ("The Concubine", "Elechi Amadi", ["Chinua Achebe", "Cyprian Ekwensi", "Wole Soyinka"]),
            ("The Great Ponds", "Elechi Amadi", ["Chinua Achebe", "Flora Nwapa", "Ola Rotimi"]),
            ("The Gods Are Not to Blame", "Ola Rotimi", ["Wole Soyinka", "J.P. Clark", "Femi Osofisan"]),
            ("Our Husband Has Gone Mad Again", "Ola Rotimi", ["Wole Soyinka", "J.P. Clark", "Femi Osofisan"]),
            ("The Passport of Mallam Ilia", "Cyprian Ekwensi", ["Chinua Achebe", "Elechi Amadi", "Flora Nwapa"])]:
        P.append(mk(0, "Literature", "African and World Literature", f"Who wrote '{title}'?", author, others,
                    f"'{title}' was written by {author}."))
    return P

def topup_pool(subj):
    fn = {
        "Economics": lambda: _econ_num() + _econ_facts(),
        "Commerce": _commerce_facts,
        "Government": _government_facts,
        "Civic": _civic_facts,
        "CRS": _crs_facts,
        "IRS": _irs_facts,
        "Agric": _agric_facts,
        "Accounting": lambda: _accounting_num() + _accounting_facts(),
        "Computer": lambda: _computer_num() + _computer_facts(),
        "Biology": _biology_facts,
        "History": _history_facts,
        "Physics": _physics_num,
        "Chemistry": _chemistry_num,
        "FurtherMath": _furthermath_num,
        "English": _english_topup,
        "Literature": _literature_topup,
    }.get(subj)
    return fn() if fn else []
