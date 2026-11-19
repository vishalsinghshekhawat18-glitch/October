# Jan–Mar 2026 print edition: the authored story layer for tools/print-ca/build.py.
# Facts only from the Jan–Mar notes; every number written here is checked against them.
# The month in each story's tag comes from the card's own ID (JAN-, FEB-, MAR-), so stories can be grouped by theme.
import os, re as _re
NOTES = '../../../archive/current-affairs/CA_Jan-Mar_2026.html'
MONTH = 'Jan–Mar 2026'
PERIOD = 'January–March'
OUTFILE = 'CA_Jan-Mar_2026_print'
UNIT = 'quarter'
DASH_TITLE = 'The quarter in numbers'

_notes = open(os.path.join(os.path.dirname(__file__), NOTES), encoding='utf-8').read()
_MON = {'JAN': 'January', 'FEB': 'February', 'MAR': 'March'}
_IDS = {_re.sub(r'\s+', ' ', t).strip().lstrip('★ ').strip(): p for p, t in
        _re.findall(r'<details class="card"[^>]*>\s*<!--\s*([A-Z]{3})-\d+\s*-->\s*<summary>(.*?)</summary>', _notes, _re.S)}
def _month(card, month=None):
    if month: return month
    hits = [p for t, p in _IDS.items() if card in t]
    return _MON[hits[0]] if len(hits) == 1 and hits[0] in _MON else None

COVER = dict(kicker='Section 1 · Budget 2026-27', title='The Budget that sells, builds and borrows', lead='budget',
             dek='A ₹80,000 crore disinvestment target, a sixfold rise in public capex in a decade and two new ₹10,000 crore funds: the numbers from Budget 2026-27 that exams ask about.',
             stats=[('7.6%', 'GDP growth FY26, new series'), ('₹80,000 cr', 'Disinvestment target'), ('4%', 'Inflation target to 2031'), ('22nd', 'EU as FTA partner')])
COVER_LINES = [('Section 2 · RBI', 'The 4% inflation target stays till March 2031', 'inft31'),
               ('Section 3 · Trade', 'The US sets an 18% tariff on Indian goods', 'usint'),
               ('Section 4 · Census', 'India\'s first digital census: reference date 1 Mar 2027', 'census'),
               ('Section 8 · Rural jobs', '125 days of work replace MGNREGA\'s 100', 'vbg')]
LEADS = {1: 'New base years · GDP 7.4% then 7.6% · Budget 2026-27 · India–EU FTA · West Asia shock',
         2: '4% inflation target to 2031 · dividend caps · loans against shares · deposit insurance · SEBI',
         3: 'India–US interim trade deal · EFTA and Oman · Hormuz and the war · BBNJ treaty · BRICS chair',
         4: '16th Finance Commission · Census 2027 · NDC 2031-35 · PLFS 2025 · Ramsar sites reach 98',
         5: 'CSPOC and AIPOC · PFRDA and IRDAI committees · India–Canada CEPA talks',
         6: 'PRAHAAR counter-terrorism policy · science, defence and sports in brief',
         7: 'Padma Awards 2026 · QS subject rankings: 27 Indian entries in the top 50',
         8: 'VB–G RAM G Act · Jal Jeevan Mission to 2028 · Modified UDAN · PM-KISAN',
         9: 'Key numbers · upcoming dates · important days · flashcards'}
DASH = '''<table class="score dash"><thead><tr><th>Indicator</th><th>The quarter</th><th>What it is</th></tr></thead><tbody>
<tr><td>CPI (retail) inflation</td><td>1.33% → 2.75% → 3.21%</td><td>Dec, Jan, Feb · ▲ rising; base 2024 from Jan</td></tr>
<tr><td>WPI (wholesale) inflation</td><td>0.83% → 1.81% → 2.13%</td><td>Dec, Jan, Feb · ▲ rising</td></tr>
<tr><td>Industrial production (IIP)</td><td>7.8% → 4.8% → 5.2%</td><td>Dec, Jan, Feb · Dec was a 26-month high</td></tr>
<tr><td>Real GDP growth FY26</td><td>7.4% → 7.6%</td><td>first advance estimate → second (new series)</td></tr>
<tr><td>Inflation target</td><td>4% (2–6%)</td><td>1 Apr 2026 – 31 Mar 2031</td></tr>
<tr><td>Disinvestment target FY27</td><td>₹80,000 cr</td><td>Budget 2026-27</td></tr>
<tr><td>States' share of taxes</td><td>41%</td><td>16th Finance Commission, 2026-31</td></tr>
<tr><td>Ramsar sites</td><td>98</td><td>26 in 2014</td></tr>
</tbody></table>'''

def make_charts(hbar, steps, table_chart):
    return {
     'cpi': hbar('CPI weights: old basket vs new (%)', [('Food and beverages, old', 45.86, '45.86'), ('Food and beverages, new', 36.75, '36.75'), ('Housing, old', 10.07, '10.07'), ('Housing, new', 17.66, '17.66')], 45.86),
     'sectors': hbar('Who pulled growth (real, FY26, %)', [('Finance, real estate, prof. + pub. admin', 9.9, '9.9'), ('Trade, hotels, transport', 7.5, '7.5'),
                ('Manufacturing and construction', 7.0, '7.0'), ('Agriculture', 3.1, '3.1'), ('Utilities', 2.1, '2.1')], 9.9),
     'ladder': hbar("India's growth forecast: the ladder (%)", [('IMF · FY25-26', 7.3, '7.3'), ('World Bank · FY25-26', 7.2, '7.2'), ('Economic Survey · FY27', 7.2, '6.8–7.2'),
                ('UN DESA · 2026-27', 6.6, '6.6'), ('World Bank · FY26-27', 6.5, '6.5'), ('IMF · FY26-27', 6.4, '6.4')], 7.3, hi=0),
     'gas': table_chart('Who gets gas first (Essential Commodities Act rationing)', ['Priority', 'Users', 'Supply'],
                [['Tier 1', 'Domestic PNG, CNG, LPG production', '100%'], ['Tier 2', 'Fertiliser', '70%'], ['Tier 3 and 4', 'Industry / CGD', '80%']], big_cols=(2,)),
     'budget': hbar('Budget 2026-27: the big-ticket allocations (₹ crore)', [('Disinvestment and monetisation target', 80000, '80,000'), ('ECMS (was 22,919)', 40000, '40,000'),
                ('PMAY-U 2.0', 18625, '18,625'), ('Biopharma SHAKTI', 10000, '10,000'), ('SME Growth Fund', 10000, '10,000')], 80000, hi=0),
     'borrow': hbar('Government borrowing, 2026-27 (₹ lakh crore)', [('Gross borrowing, BE', 17.20, '17.20'), ('After G-Sec switches', 16.09, '16.09'), ('First half (H1)', 8.20, '8.20'), ('WMA limit, H1', 2.50, '2.50')], 17.20),
     'nmp': hbar('NMP 2.0 targets by sector (₹ lakh crore)', [('Highways, logistics parks, ropeways', 4.42, '4.42'), ('Power', 2.76, '2.76'), ('Railways', 2.62, '≈2.62'), ('Ports', 2.62, '≈2.62')], 4.42, hi=0),
     'eu': steps('India–EU: the long road', [('2004', 'Strategic partners'), ('2007', 'Talks launched'), ('2022', 'Talks relaunched'), ('26 Jan 2026', 'Deal concluded'), ('27 Jan 2026', '16th India–EU Summit')]),
     'itact': table_chart('Income-tax Act 2025 vs the 1961 Act', ['', 'Old', 'New'], [['Sections', '819', '536'], ['Chapters', '47', '23'], ['Words', '5.12 lakh', '2.6 lakh']], big_cols=(1, 2)),
     'inft': steps('Inflation targeting in India', [('2016', 'First mandate, to 31 Mar 2021'), ('Mar 2026', 'Review due'), ('1 Apr 2026', 'New five-year term'), ('31 Mar 2031', 'Term ends')]),
     'divall': table_chart('Maximum dividend payout, by bank type', ['Bank type', 'Cap (% of adjusted PAT)'],
                [['Commercial banks', '75%'], ['Payments banks', '75%'], ['Small finance banks', '75%'], ['Local area banks', '80%'], ['Regional rural banks', '80%']], big_cols=(1,)),
     'las': hbar('Maximum loan-to-value for individuals (%)', [('Listed shares', 60, '60'), ('Equity MFs, ETFs, REITs, InvITs', 75, '75'), ('AA–BBB listed debt', 75, '75'), ('Debt MFs', 85, '85'), ('AAA listed debt', 85, '85')], 85),
     'rbp': table_chart('Who pays what for deposit insurance', ['', 'Before', 'From 1 Apr 2026'],
                [['Premium', 'Flat 12 paise per ₹100', 'Risk-based'], ['Safer banks', 'Same rate', 'Up to 33.33% off card rate'], ['Long-standing banks', 'Same rate', 'Vintage incentive up to 25%']]),
     'ustar': hbar('US tariffs on Indian goods after the framework (%)', [('Most goods (reciprocal tariff)', 18, '18'), ('$30.94 bn of exports: was', 50, '50 → 18'), ('$10.03 bn of exports: was', 50, '50 → 0')], 50, hi=0),
     'hormuz': table_chart('The Strait of Hormuz in numbers', ['Measure', 'Figure'], [['Share of world oil', '~20%'], ['Barrels a day', '20+ mn'], ['Qatar LNG', 'nearly all'], ['Rank among oil chokepoints', 'second, after Malacca']], big_cols=(1,)),
     'fc': steps('Finance Commission: the States\' share', [('41%', '15th FC, 2021-26'), ('41%', '16th FC, 2026-31')]),
     'census': steps('Census 2027, step by step', [('1–15 Apr 2026', 'Self-enumeration'), ('16 Apr–15 May', 'House listing'), ('Sep 2026', 'Population enumeration'), ('1 Mar 2027', 'Reference date')]),
     'ndc': table_chart("India's climate targets: met and new", ['Target', 'Where India is', 'By 2035'],
                [['Emissions intensity of GDP (vs 2005)', '36% cut by 2020', '47%'], ['Non-fossil share of power capacity', '52.57% (Feb 2026)', '60%'], ['Extra carbon sink', '2.29 bn tCO2e by 2021', '3.5–4.0 bn tCO2e']], big_cols=(2,)),
     'plfs': hbar('PLFS 2025: who is in the workforce (%)', [('LFPR, all', 59.3, '59.3'), ('LFPR, male', 79.1, '79.1'), ('LFPR, female', 40.0, '40.0'), ('WPR', 57.4, '57.4')], 79.1),
     'vbg': table_chart('MGNREGA vs VB–G RAM G', ['', 'MGNREGA', 'VB–G RAM G'], [['Guaranteed days', '100', '125'], ['Centre–state funding', '–', '60:40 (NE and Himalayan 90:10)'], ['Administrative ceiling', '6%', '9%']], big_cols=(1, 2)),
     'jjm': hbar('Central assistance for Jal Jeevan Mission (₹ lakh crore)', [('Original (2019-20)', 2.08, '2.08'), ('Extended (to Dec 2028)', 3.59, '3.59')], 3.59, hi=1),
    }

SEC_INTRO = {
 1: 'How India measured its economy, how fast it grew, the Budget, the trade deals and the credit schemes of the quarter, with banking and insurance at the end.',
 2: 'The RBI kept its 4% inflation target and rewrote rules on dividends, loans and deposit insurance; SEBI, PFRDA and others changed theirs.',
 3: 'A trade deal with the US, two more with Europe and the Gulf, a war in West Asia and a treaty for the high seas.',
 4: 'How money is shared with the States, the coming census, climate pledges, jobs data, new rules and news from Rajasthan.',
 5: 'Two conferences of presiding officers, new expert committees and trade talks with Canada.',
 6: 'A national counter-terrorism policy; science, defence and sport are in brief.',
 7: 'The Padma Awards and a record year for Indian universities in the QS subject rankings.',
 8: 'The schemes of the quarter, from rural jobs to tap water and regional flights.',
}

CHAPTERS = {
 1: [('1.1', 'The quarter India changed its measuring tape', 'Between February and May 2026 India re-measures prices, output, factory production and trade on newer base years. Any question with "new series" in it starts here.', ['cpi', 'gdpnew', 'jan02']),
     ('1.2', 'How fast is India growing?', "Three kinds of number answer this: the government's own estimates, India's size against other countries, and forecasts from outside bodies.", ['gdpae', 'fourth', 'fcast', 'survey']),
     ('1.3', 'The monthly pulse', 'Read these as a trend: inflation rose each month, while factory output cooled after December and then picked up.', ['dec', 'feb31', 'trade62', 'core', 'iipepf']),
     ('1.4', 'War next door: the West Asia shock', 'In March 2026 the war in West Asia hit energy supplies, shipping and insurance costs. The government answered with a cushion fund, gas rationing and cover for exporters.', ['esf', 'relief']),
     ('1.5', 'Budget 2026-27', 'Learn the headline number for each scheme first; the details come second.', ['budget', 'bio', 'msme', 'infra', 'mat', 'borrow', 'ucf', 'nmp']),
     ('1.6', 'Trade deals and tax rules', 'One giant trade deal, one treaty rewrite, a new tax law and new rules for listed companies.', ['eufta', 'sin', 'france', 'itr', 'mps']),
     ('1.7', 'Credit for small firms, exporters and startups', 'Most of these schemes work the same way: the government guarantees part of a loan so that banks lend without collateral. Learn the cover and the corpus.', ['cgse', 'cgsmfi', 'cam', 'startup']),
     ('1.8', 'Banking', 'Rates that did not move, a new self-regulator, a reform agenda that spells a word, and a fund that rescues stuck homes.', ['ssr', 'apy', 'fedai', 'ease', 'swamih', 'coop']),
     ('1.9', 'Insurance', 'Foreigners can now own insurers outright, cashless claims got deadlines, and the target is insurance for all by 2033.', ['insfdi', 'irdai', 'insrules'])],
 2: [('2.1', 'The RBI\'s targets and plans', 'The 4% inflation target is kept for five more years, and the RBI set out its strategy to 2029.', ['inft31', 'inft', 'utkarsh', 'board', 'prb', 'rbidpi']),
     ('2.2', 'How much a bank may pay out and risk', 'Dividend caps, related-party loans, takeover finance and limits on stock-market exposure.', ['divall', 'divdraft', 'div2fa', 'relparty', 'acq', 'cme', 'las', 'lei']),
     ('2.3', 'Complaints and the ombudsman', 'Every bank needs an internal ombudsman, and the RBI Ombudsman can award compensation.', ['iob', 'ombcomp']),
     ('2.4', 'Lending to farms, small firms and NBFCs', 'Easier rules for infrastructure loans and small businesses, a stricter test for priority sector loans and a new KCC rule book.', ['nbfcrw', 'psl', 'coopncdc', 'calam', 'msmel', 'kcc']),
     ('2.5', 'Deposit insurance', 'How much of your money is insured, and why safer banks will now pay less for it.', ['rbp', 'dicgc']),
     ('2.6', 'Money across borders', 'Guarantees, foreign borrowing, bond routes, land-border investment, tax pricing deals and baggage rules.', ['fema', 'ecb', 'vrr', 'lbc', 'apa', 'baggage']),
     ('2.7', 'Payments and phones', 'Auto-debits get a warning rule, and banks must call from a separate number.', ['emandate', 'trai']),
     ('2.8', 'SEBI', 'A new end to the trading day, stronger merchant bankers, fixed mutual fund categories and tighter derivative rules.', ['cas', 'merchant', 'mfcat', 'sebifeb', 'sebimar']),
     ('2.9', 'Pensions, carbon and startups', 'New NPS schemes, banks as pension funds, carbon targets for industry and a new startup definition.', ['swasthya', 'vatsalya', 'pfrdab', 'ghg', 'startrec'])],
 3: [('3.1', 'India\'s trade deals', 'An interim framework with the US, and deals with EFTA, Oman and the UAE.', ['usint', 'efta', 'oman', 'uae']),
     ('3.2', 'A war and a walk-out', 'The Strait of Hormuz was disrupted, and the US left the WHO and 66 other bodies.', ['wawar', 'uswd']),
     ('3.3', 'Climate and the oceans', 'A high-seas treaty, the first Paris carbon credits and the EU\'s carbon border tax.', ['bbnj', 'pacm', 'cbam']),
     ('3.4', 'Groups, blocs and neighbours', 'India chairs BRICS, new members join the UNSC and the eurozone, and the EU signs with Mercosur.', ['brics', 'unsc', 'bulgaria', 'mercosur', 'indpak'])],
 4: [('4.1', 'Money between the Centre and the States', 'The Finance Commission\'s share, a record Budget run and the census that will redraw the numbers.', ['fc16', 'budget9', 'census']),
     ('4.2', 'Laws and courts', 'Insolvency, online content, a State\'s new name, a Supreme Court ruling and a sports law.', ['ibc', 'itrules', 'keralam', 'scmens', 'sports', 'ecinet', 'seed']),
     ('4.3', 'Jobs, health and welfare', 'The year\'s jobs survey, faster EPF withdrawals, a cancer vaccine drive and cashless treatment for accident victims.', ['plfs', 'epfo', 'hpv', 'rahat', 'cbdcpds', 'manav', 'startdef']),
     ('4.4', 'Farms, rails and roads', 'Rice, the bullet train, coking coal and the rules that started on 1 April.', ['rice', 'bullet', 'coking', 'apr1']),
     ('4.5', 'Climate, waste and wildlife', 'India\'s new climate pledge, new waste rules, more Ramsar sites and a dolphin count.', ['ndc', 'swm', 'ramsar', 'dolphin', 'biodiv', 'roots']),
     ('4.6', 'Rajasthan and the States', 'An eco-sensitive zone, a State copy of PRAGATI and PESA rules in Jharkhand.', ['kumbhal', 'unnati', 'pesa'])],
 5: [('5.1', 'Conferences and committees', 'Presiding officers met in Delhi and Lucknow, and new panels were set up for pensions, reinsurance and foreign banks.', ['cspoc', 'cmte']),
     ('5.2', 'Agreements', 'Trade talks with Canada restart.', ['canada'])],
 6: [('6.1', 'Defence', 'A national counter-terrorism policy with seven pillars.', ['prahaar'])],
 7: [('7.1', 'Awards', 'The Padma Awards and an Ashoka Chakra for an astronaut.', ['padma']),
     ('7.2', 'Rankings', 'A record for Indian universities.', ['qs'])],
 8: [('8.1', 'Work and livelihoods', 'More days of rural work, bigger loans for street vendors and support for craftspeople.', ['vbg', 'svanidhi', 'vishwakarma']),
     ('8.2', 'Farmers', 'Cash transfers, cheap crop credit and a mission for pulses.', ['pmkisan', 'pulses']),
     ('8.3', 'Water, flights and factories', 'Tap water to 2028, flights to smaller towns and ready-made industrial parks.', ['jjm', 'udan', 'bhavya']),
     ('8.4', 'Digital and road safety', 'India\'s digital public infrastructure and how PM RAHAT pays for accident care.', ['dpi', 'rahatchain'])],
}

S = {}
def st(key, card, tag, h, size='short', month=None, **kw):
    m = _month(card, month)
    S[key] = dict(card=card, tag=(f'{m} · {tag}' if m else tag), h=h, size=size, **kw)

# ---------------------------------------------------------------- 1
st('cpi', 'CPI inflation Dec 2025 and base-year revision', 'Inflation', "Food now counts for less in India's price index", 'feature',
   lede='Retail inflation is measured by pricing a fixed basket of what families buy. The old series (base 2012) reflected spending patterns that have changed since 2011-12. So the new series, first used for January 2026 data, prices more items, gives food a much smaller share and gives housing a much bigger one. December 2025 was the last month on the old basket, at just 1.33%.',
   chart=['cpi'],
   hook='"Less roti, more rent." Food\'s share falls from 45.86% to 36.75%; housing\'s share rises from 10.07% to 17.66%.',
   trap="CPI's new base is 2024. GDP and IIP move to 2022-23, not 2024.")
st('gdpnew', 'National Accounts base year revision (GDP new series)', 'Growth · new series', 'GDP gets a new base year: 2022-23 replaces 2011-12', 'feature',
   lede='A base year is the reference year that all GDP figures are compared with. MoSPI moved it from 2011-12 to 2022-23 and published the new series on 27 Feb 2026. The method changed too: gig and platform work and hired domestic workers are now counted. Because GDP itself changed, ratios built on it were recalculated: the fiscal deficit for 2024-25 is now 4.9% of GDP, not 4.8%.',
   nums=[('7.6%', 'FY26 growth, new series'), ('₹345.47 lakh cr', 'FY26 nominal GDP'), ('B N Goldar', 'chairs ACNAS'), ('5', 'sub-committees')],
   hook='"Goldar set the new gold standard": Prof B N Goldar chaired the advisory committee (ACNAS) behind the new series.',
   trap='First advance estimate (old series, January): 7.4%. Second advance estimate (new series, February): 7.6%. Check which one a question means.')
st('gdpae', 'GDP First Advance Estimates FY2025-26 (Jan 2026)', 'Growth', "India's first guess for the year: 7.4% growth, up from 6.5%", 'feature',
   lede='In January 2026, before the financial year was over, NSO made its first estimate of how much the economy grew. For FY26 it put real growth at 7.4%, a clear step up from 6.5% the year before. Finance, real estate and public administration grew fastest, while farming and utilities lagged far behind.',
   nums=[('7.4%', 'Real GDP growth'), ('8.0%', 'Nominal GDP growth'), ('7.3%', 'Real GVA growth'), ('₹357.14 lakh cr', 'Nominal GDP')],
   chart=['sectors'],
   hook='"Seven-four beats six-five." Top sector 9.9% (finance), bottom 2.1% (utilities), farming 3.1%.',
   trap='7.4% is real GDP. 8.0% is nominal GDP and 7.3% is real GVA: three numbers for three different questions.')
st('fourth', 'India becomes 4th largest economy', 'Growth · milestone', "India passes Japan to become the world's 4th largest economy",
   lede='With GDP of USD 4.18 trillion, India has moved past Japan. Only the US, China and Germany are bigger, and India is expected to pass Germany for 3rd place by 2030. Growth has been picking up quarter after quarter.',
   hook='"4.18 trillion, 4th place": both start with 4.')
st('fcast', 'Growth forecasts for India: UN, World Bank, IMF (Jan 2026)', 'Forecasts', 'Forecasters agree India stays above 6%, but differ on how fast', 'feature',
   lede="For this year the IMF (7.3%) is a notch more hopeful than the World Bank (7.2%). For next year the outside bodies expect growth to cool to the mid-6s, while the government's own Economic Survey 2026, tabled by FM Nirmala Sitharaman and prepared under CEA V. Anantha Nageswaran, is the most optimistic at 6.8–7.2%.",
   chart=['ladder'],
   hook='"IMF one up": IMF 7.3 sits one notch above the World Bank\'s 7.2 for FY26.',
   trap='UN DESA gives no FY26 figure here: its 6.6% is for 2026-27 and 6.8% for 2027-28.')
st('dec', 'December 2025 data snapshot: UPI, WPI, trade, PMI', 'December data', 'December: 21.63 billion UPI payments and a $6.92 bn trade gap',
   lede="UPI handled 21.63 billion transactions in December, 29% more than a year before, worth about ₹28 lakh crore. Wholesale inflation stayed below 1% at 0.83%. Imports ($80.94 bn) beat exports ($74.01 bn), leaving a deficit of $6.92 bn. India also has the world's 2nd-largest 5G subscriber base (400 million+), after China.",
   hook='PMI above 50 means expansion. 55.0 is still growth, just the lowest in 38 months.')
st('jan02', 'Price and output data: January 2026', 'January data', 'January: the first reading on the new CPI is 2.75%',
   lede='January 2026 was the first month measured on the new CPI (base 2024): 2.75%. Wholesale inflation, still on the old 2011-12 base, was 1.81%. Separately, DGCI&S moved the base year of merchandise trade indices from 2012-13 to 2022-23, on the advice of a committee under Prof. Nachiketa Chattopadhyay of ISI.',
   hook='In WPI, manufactured goods weigh 64.23%, almost two-thirds; primary articles 22.62%; fuel and power 13.15%.',
   trap='WPI still uses base 2011-12. Only CPI moved to 2024.')
st('feb31', 'Monthly numbers: Feb 2026 data (released Mar)', 'February data', 'February: factory mood at its best since October 2025',
   lede="February's numbers: CPI 3.21%, WPI 2.13%, core industries 2.3%. The HSBC manufacturing PMI rose to 56.9 from 55.4, its highest since October 2025, and gross GST brought in about ₹1.83 lakh crore, up 8.1%. Coal output crossed 1 billion tonnes for the second year, and NMDC became the first miner to produce 50 MT of iron ore in a year.")
st('trade62', 'Trade and inflation data, Feb 2026', 'Trade and prices', 'Exports reach $790.86 billion in eleven months',
   lede="From April 2025 to February 2026, India's merchandise and services exports together reached US$790.86 billion. The new CPI basket prices 358 items (308 goods, 50 services) in 12 divisions. WPI, released by DPIIT on the 14th of every month, was 2.13% in February.",
   hook='CPI 3.21 and WPI 2.13 use the same three digits.',
   trap='Goods in the CPI basket went 259 → 308 and services 40 → 50.')
st('core', 'Eight Core Industries Feb 2026 and other data', 'Core industries', 'The eight industries that carry 40% of factory output',
   lede="The eight core industries (refinery products, electricity, steel, coal, crude oil, natural gas, cement and fertilisers) carry 40.27% of the IIP's weight, so they move first. They grew 2.3% in February, down from 4% in January. The same season brought other facts: India's bio-economy grew from $10 bn in 2014 to $195.3 bn, milk production reached 247 MT, and Rajasthan has the highest renewable energy potential.",
   hook='Top three by weight: Refinery, Electricity, Steel ("RES": about 28, 20, 18). Fertilisers are smallest at 2.63%.',
   trap='Bio-economy target is $300 bn by 2030; today it is $195.3 bn.')
st('iipepf', 'IIP and EPF decisions (Mar 2026)', 'Savings · output', 'EPF savers get 8.25% for 2025-26',
   lede="The EPFO's Central Board of Trustees (239th meeting, chaired by Mansukh Mandaviya) recommended 8.25% interest for FY 2025-26. It also brought in a new EPF Scheme, EPS and EDLI Scheme 2026, and a pilot to settle balances up to ₹1,000 automatically. An account goes inoperative if nothing is paid in for 3 years after age 55. Factory output slowed to 4.8% in January from 7.8% in December, then picked up to 5.2% in February.",
   hook='IIP quick estimates come out on the 28th of each month.')
st('esf', 'Economic Stabilisation Fund and West Asia shock (Mar 2026)', 'Economy · shock', 'A ₹1 lakh crore cushion against the West Asia war', 'feature',
   lede='FM Sitharaman proposed an Economic Stabilisation Fund of ₹1 lakh crore to absorb the shock: about ₹57,000 crore of fresh cash plus ₹43,000 crore from savings. To protect households, the government used the Essential Commodities Act 1955 to ration natural gas by priority. LPG refills now come every 25 days instead of 21. The WTO expects world trade growth to fall from 4.6% in 2025 to 1.9% in 2026.',
   chart=['gas'],
   hook='57 + 43 = 100: fresh cash plus savings make the ₹1 lakh crore fund.',
   trap='The law used for gas rationing is the Essential Commodities Act, 1955.')
st('relief', 'RELIEF: export support amid West Asia disruptions', 'Exports · shock', "RELIEF: the government shares exporters' war risk",
   lede='With shipping and insurance costs rising, the Resilience & Logistics Intervention for Export Facilitation (RELIEF), part of the Export Promotion Mission, has ₹497 crore and works through ECGC. Insured consignments get up to 100% extra risk cover from 14 Feb to 15 Mar 2026, then up to 95% from 16 Mar to 15 Jun 2026. MSME exporters without insurance can get up to 50% reimbursement, capped at ₹50 lakh.',
   hook='100 → 95 → 50: two phases of cover, then reimbursement for the uninsured.',
   trap='Nodal agency is ECGC (Export Credit Guarantee Corporation of India Ltd.), not NCGTC.')
st('budget', 'Union Budget 2026-27: key numbers (Feb 2026)', 'Budget', "Sell more, build more homes: the Budget's headline targets", 'feature',
   lede='The government wants ₹80,000 crore in 2026-27 from disinvestment and asset monetisation, more than double the ₹33,837 crore it expects for FY26, with IDBI Bank and LIC as the big sources. PMAY-U 2.0 gets ₹18,625 crore, and the target for homes built by beneficiaries jumps from 1.1 lakh to 5 lakh. Lakhpati Didi has crossed 3 crore women; the new target is 6 crore by March 2029.',
   nums=[('₹80,000 cr', 'Disinvestment target'), ('₹18,625 cr', 'PMAY-U 2.0'), ('6 crore', 'Lakhpati Didi by 2029'), ('₹2 lakh cr', 'Agri Infra Fund loans')],
   chart=['budget'],
   hook='Two things double: Lakhpati Didi (3 crore → 6 crore) and the Agriculture Infrastructure Fund loan target (₹1 lakh crore → ₹2 lakh crore).',
   trap='MDR is already zero on RuPay debit and BHIM-UPI (since Jan 2020); the ₹2,000 crore is an incentive for P2M payments.')
st('bio', 'Budget 2026-27 items: Biopharma SHAKTI, ECMS, ISM 2.0, EPF tax', 'Budget · industry', 'Medicines, chips and electronics get the money',
   lede='Biopharma SHAKTI puts ₹10,000 crore over 5 years into biologics and biosimilars, aiming for 5% of the global biopharma market. The electronics components scheme (ECMS) grows from ₹22,919 crore to ₹40,000 crore, chasing $500 bn of electronics by 2030-31. India Semiconductor Mission 2.0 gets ₹1,000 crore for FY27. EPF tax changes too: employer contributions above ₹7.5 lakh are taxed as a perquisite.',
   hook='SHAKTI 10, ECMS 40, ISM 2.0 just 1 (₹ thousand crore).',
   trap="ISM 1.0 (Dec 2021) was ₹76,000 crore; ISM 2.0's ₹1,000 crore is for FY27 only.")
st('msme', 'Budget 2026-27 MSME and startup measures', 'Budget · MSME', 'Small firms get a growth fund and bigger guarantees',
   lede='A new SME Growth Fund of ₹10,000 crore, and the CGTMSE guarantee ceiling doubles from ₹5 crore to ₹10 crore. CPSEs must buy from MSMEs through TReDS, the platform that lets small firms get paid early on invoices. Startups get a second Fund of Funds with ₹10,000 crore. The National Manufacturing Mission aims for manufacturing at 25% of GDP by 2035.',
   hook='Two ₹10,000 crore funds: the SME Growth Fund and Startup India Fund of Funds 2.0.',
   trap='The ₹7 lakh crore figure is what TReDS has already unlocked, not a new fund.')
st('infra', 'Budget 2026-27: infrastructure finance and services exports', 'Budget · infrastructure', 'Capex grows sixfold in a decade; foreign cloud firms get a tax holiday till 2047',
   lede='Public capital spending has grown from ₹2 lakh crore in FY15 to ₹12.2 lakh crore budgeted for 2026-27. New tools to draw in private money: an Infrastructure Risk Guarantee Fund, ₹5,000 crore per City Economic Region and dedicated REITs for CPSE property. For services (49.9% of GDP), foreign cloud providers using Indian data centres get a tax holiday till 2047, and IT services get a single safe-harbour margin of 15.5%.',
   hook='2047 twice: the cloud tax holiday runs till then, and services aim for 10% of the global share by then.',
   trap='Safe harbour is 15.5% for IT services but 15% on cost for data-centre services.')
st('mat', 'Budget 2026-27 ease-of-business and tax reforms', 'Budget · tax', 'MAT cut to 14% and made a final tax',
   lede='Minimum Alternate Tax is now treated as a final tax and its rate falls from 15% to 14%. Buybacks are taxed as capital gains. Individual persons resident outside India investing in listed shares through PIS can each hold up to 10% (was 5%), and together up to 24% (was 10%). Customs advance rulings now last 5 years instead of 3.',
   hook='Individual cap doubles (5 → 10); aggregate more than doubles (10 → 24).',
   trap='MAT for cooperatives is a separate cut: 18.5% → 15%.')
st('borrow', 'Government borrowing plan, H1 FY2026-27', 'Budget · borrowing', 'How the government will borrow ₹8.20 lakh crore in six months', 'feature',
   lede="Gross borrowing was budgeted at ₹17.20 lakh crore, cut to ₹16.09 lakh crore after bond switches. In the first half of 2026-27 the government borrows ₹8.20 lakh crore, 51.0% of the year, through 26 weekly auctions, including ₹15,000 crore of Sovereign Green Bonds. The 10-year bond takes the biggest share (29%). For short cash gaps, RBI's Ways and Means Advances limit is ₹2.50 lakh crore.",
   nums=[('₹8.20 lakh cr', 'H1 borrowing'), ('51.0%', 'Share of year'), ('26', 'Weekly auctions'), ('₹2.50 lakh cr', 'WMA limit H1')],
   chart=['borrow'],
   hook="Half the year's borrowing (51.0%) in the first half; 26 auctions, one a week.",
   trap='T-bills are separate: ₹24,000 crore a week in Q1 (91-day ₹12,000 cr, 182-day and 364-day ₹6,000 cr each).')
st('ucf', 'Urban Challenge Fund (Cabinet, Feb 2026)', 'Cabinet · cities', 'Cities must raise half the money: the ₹1 lakh crore Urban Challenge Fund',
   lede="The Centre will pay 25% of a city project's cost from a ₹1 lakh crore fund, but at least 50% must come from the market through municipal bonds, loans or PPP. That adds up to about ₹4 lakh crore of investment from FY2025-26 to FY2030-31. Projects are chosen by competition (challenge mode), and a ₹5,000 crore corpus helps 4,223 cities become more creditworthy.",
   hook='25 from the Centre, at least 50 from the market: ₹1 lakh crore becomes about ₹4 lakh crore.',
   trap='The Credit Repayment Guarantee Scheme (₹5,000 crore) is for ULBs below 1 lakh population and NE/hill states.')
st('nmp', 'National Monetisation Pipeline 2.0 (NMP 2.0)', 'Assets', '₹16.72 lakh crore from leasing out public assets', 'feature',
   lede='Monetisation means leasing out existing public assets, such as highways, power lines and railways, to private players for money. NMP 2.0, developed by NITI Aayog for FY26–FY30, targets ₹16.72 lakh crore from 12 sectors, 2.6 times the first pipeline. NMP 1.0 aimed for ₹6 lakh crore and achieved about ₹5.3 lakh crore.',
   chart=['nmp'],
   hook='16.72 vs 6: the second pipeline is 2.6 times the first.',
   trap='Developed by NITI Aayog, but monitored by the Core Group of Secretaries on Asset Monetisation under the Cabinet Secretary.')
st('eufta', 'India–EU Free Trade Agreement concluded (26 Jan 2026)', 'Trade', 'After nearly 20 years of talks, India and the EU seal a free trade deal', 'feature',
   lede="Talks began in 2007, restarted in 2022 and concluded on 26 Jan 2026, while EU leaders Costa and von der Leyen were chief guests at the 77th Republic Day. The EU becomes India's 22nd FTA partner and is already its largest goods partner (USD 136.53 bn in 2024-25). India gets access on 97% of EU tariff lines; India opens 92.1% of its own. EU banks may open 15 branches over 4 years, and India binds insurance FDI at 100%.",
   nums=[('22nd', 'FTA partner'), ('15 in 4 yrs', 'EU bank branches'), ('97%', 'EU lines open to India'), ('$136.53 bn', 'Goods trade 2024-25')],
   chart=['eu'],
   hook='15 branches in 4 years (not 12, which was the earlier offer).',
   trap="Meat, dairy, honey, rice, sugar and tobacco are excluded from the EU's offer.")
st('sin', 'Tobacco and pan masala: new levies from 1 Feb 2026', 'Tax', 'Sin goods move to 40% GST and new levies',
   lede='From 1 Feb 2026 the compensation cess on sin goods ends. Pan masala, cigarettes and tobacco now pay GST at 40% (biris 18%), with a health and national security cess on pan masala and additional excise duty on tobacco.',
   hook='40 for cigarettes, 18 for biris.',
   trap='The new cess is on pan masala; tobacco gets additional excise duty instead.')
st('france', 'India–France DTAC amending protocol; India–GCC FTA', 'Tax treaty · trade', 'India and France rewrite their tax treaty; Gulf trade talks begin',
   lede='India and France amended their 1992 tax treaty (DTAC): dividends are now taxed at 5% for holdings of 10% or more and 15% for others, instead of a single 10%. Capital gains on shares are taxed where the company is resident, and the MFN clause is gone. India also signed Terms of Reference for an FTA with the GCC, its largest trading bloc at $178.56 bn in FY25.',
   hook='The old 10% splits into 5 and 15.',
   trap='GCC trade is import-heavy: imports $121.68 bn vs exports $56.87 bn.')
st('itr', 'Income Tax Rules 2026 (effective 1 Apr 2026)', 'Tax', 'A shorter tax law: 819 sections become 536', 'feature',
   lede='Income Tax Rules 2026, in force from 1 April 2026, put the Income-tax Act 2025 into practice, replacing the 1961 Act. The 50% HRA exemption now covers 8 cities, not 4 metros. PAN is needed for cash deposits or withdrawals of ₹10 lakh a year (earlier ₹50,000 a day) and for property above ₹20 lakh (earlier ₹10 lakh).',
   chart=['itact'],
   hook='8 HRA cities: the 4 metros plus Hyderabad, Pune, Ahmedabad and Bengaluru.',
   trap='Other cities get a 40% HRA exemption.')
st('mps', 'Minimum public shareholding norms revised (SCRR 1957)', 'Markets', 'Big companies get up to 10 years to reach 25% public shareholding',
   lede='Listed companies must keep at least 25% of shares with the public. The revised rules under SCRR 1957 sort companies into 6 size bands instead of 3, giving larger companies 3 to 10 years to reach 25%. The minimum IPO offer is halved, from 5% to 2.5%.',
   hook='Bands double (3 → 6); IPO minimum halves (5 → 2.5).')
st('cgse', 'Credit Guarantee Scheme for Exporters (CGSE) operational', 'Exports · credit', 'Exporters get collateral-free loans, 100% backed by the government',
   lede='Since 1 Dec 2025 the Credit Guarantee Scheme for Exporters lets MSME exporters borrow extra working capital, up to 20% of their existing export credit limit, without collateral. NCGTC guarantees 100% of the extra loan, up to ₹20,000 crore in all, through the Jan Samarth portal. It is open till 31 Mar 2026.',
   hook='100% cover, ₹20,000 crore, 20% of limit.',
   trap='Run by DFS through NCGTC, not through CGTMSE.')
st('cgsmfi', 'Credit guarantee: CGSMFI-2.0 and MCGS-MSME changes (Mar 2026)', 'Credit guarantee', 'Microfinance lenders get a ₹20,000 crore safety net',
   lede='CGSMFI-2.0 (₹20,000 crore, 20 Mar–30 Jun 2026) guarantees loans to microfinance institutions: NCGTC covers 80% of defaults for small MFIs, 75% for medium and 70% for large, reaching about 36 lakh borrowers. A second scheme, MCGS-MSME, gives 60% cover on loans up to ₹100 crore for machinery and now includes services MSMEs.',
   hook='Smaller MFI, bigger cover: 80 → 75 → 70.',
   trap='A small MFI has AUM below ₹500 crore.')
st('cam', 'MSME credit: PSB Credit Assessment Model (CAM)', 'MSME credit', 'Small-business loans approved from data, not paperwork',
   lede='Public sector banks now give MSMEs an instant in-principle loan sanction by reading their digital footprint: GST, ITR, bank statement and CIC data, end to end on the Jan Samarth portal. From 1 Apr to 31 Dec 2025, 3.96 lakh applications brought ₹52,300+ crore of sanctions.',
   hook='Four data sources: GST, ITR, bank statement, CIC.')
st('startup', 'Startup India: 10 years and National Startup Awards 5.0', 'Startups', 'Startup India turns 10: from under 500 startups to over 2 lakh',
   lede='Startup India was launched in 2016, and 16 Jan is National Startup Day. DPIIT-recognised startups have grown from under 500 in 2014 to above 2.07 lakh, and unicorns from 4 to nearly 125, making India the 3rd largest startup ecosystem. Maharashtra has the most (35,991). About 50% of startups come from Tier II/III cities.',
   hook="Best Performers in the States' Startup Ranking 5.0: Gujarat (Category A); Arunachal Pradesh and Goa (Category B).",
   trap='Fund of Funds for Startups (₹10,000 crore) is managed by SIDBI; the Seed Fund Scheme is ₹945 crore.')
st('ssr', 'Small savings rates unchanged: Jan–Mar 2026 quarter', 'Small savings', 'Small savings rates frozen for a 7th straight quarter',
   lede='The government reviews small-savings rates every quarter. From 1 Jan 2026 they stayed unchanged for the 7th consecutive quarter. Sukanya Samriddhi still pays the most, 8.2%; the post office savings deposit the least, 4%.',
   hook='PPF and the 3-year term deposit share the same rate: 7.1%.',
   trap='Kisan Vikas Patra matures in 115 months.')
st('apy', 'Atal Pension Yojana continued to FY2030-31; Sukanya Samriddhi basics', 'Pensions · savings', 'Atal Pension Yojana extended to 2030-31',
   lede='The Cabinet extended Atal Pension Yojana, with gap funding, till 2030-31. Launched on 9 May 2015 for the unorganised sector, it guarantees ₹1,000–₹5,000 a month from age 60. Sukanya Samriddhi (22 Jan 2015) can be opened for a girl up to age 10: deposit ₹250 to ₹1.5 lakh a year for 15 years; it matures after 21 years and pays 8.2%.',
   hook='₹250 min, ₹1.5 lakh max; 15 years of deposits, 21 years to maturity.',
   trap='SSY allows 50% withdrawal for education at 18 or after Class 10.')
st('fedai', 'RBI recognises FEDAI as a Self-Regulatory Organisation (SRO)', 'Regulation', 'RBI makes FEDAI a self-regulator for forex dealers',
   lede='RBI recognised FEDAI, the association of Authorised Dealer banks set up in 1958, as a Self-Regulatory Organisation (SRO): a non-government body that a regulator authorises to oversee its sector.',
   hook="FEDAI 1958: the forex dealers' association, now also their referee.")
st('ease', 'EASE 8.0 (EASERise) for public sector banks', 'PSB reform', 'EASE 8.0 is branded EASERise, and its themes spell RISE',
   lede='EASE 8.0 is the FY2025-26 reform agenda common to all public sector banks. Its four themes are Risk and Resilience, Innovation, Socio-economic Impact and Excellence, with a push for GenAI and agentic AI and for inclusive banking.',
   hook='R-I-S-E: Risk, Innovation, Socio-economic, Excellence = EASERise.')
st('swamih', 'SWAMIH Fund: stalled housing finance', 'Housing finance', 'SWAMIH: the fund that finishes stuck housing projects',
   lede='Stuck housing projects cannot finish without money. SWAMIH (Special Window for Affordable and Mid-Income Housing), launched Nov 2019 and managed by SBI Ventures, gives last-mile funding to RERA-registered stalled projects. Its ₹15,531 crore corpus was fully committed before 5 Dec 2025; about ₹7,000 crore has been invested and ₹3,500 crore recovered. SWAMIH Fund-2 adds ₹15,000 crore for 1 lakh more homes.',
   hook='SBI Ventures; last-mile funding for RERA-registered stalled projects.',
   trap='Sponsor is DEA; manager is SBI Ventures. Rivali Park was the first project completed.')
st('coop', 'Cooperatives: International Year, policy and reforms (Dec 2025 data)', 'Cooperatives', '8.5 lakh cooperatives, a new policy and a cooperative taxi',
   lede='The UN made 2025 the International Year of Cooperatives ("Cooperatives Build a Better World"). India\'s National Cooperative Database counts 8.5 lakh cooperatives with about 32 crore members. The National Cooperation Policy 2025 (24 Jul 2025) has 16 objectives and six pillars under the vision Sahkar-se-Samriddhi. Sahakar Taxi is the first cooperative mobility initiative.',
   hook='16 objectives, 6 pillars.',
   trap='Nodal financier of cooperatives: NCDC (est. 1963).')
st('insfdi', '100% FDI in insurance (automatic route)', 'Insurance · FDI', 'Foreign companies can now own 100% of an Indian insurer',
   lede='Foreign ownership of insurers can now go up to 100% through the automatic route, up from 74%. DPIIT operationalised this in Feb 2026 under the Sabka Bima Sabki Raksha (Amendment of Insurance Laws) Act, 2025, in force from 5 Feb. The chair, MD or CEO must still be a resident Indian citizen. LIC stays at 20% FDI.',
   hook='Sabka Bima Sabki Raksha amends three laws: Insurance Act 1938, LIC Act 1956, IRDAI Act 1999.',
   trap="Foreign reinsurers' Net Owned Fund requirement falls from ₹5,000 crore to ₹1,000 crore.")
st('irdai', 'IRDAI Annual Report FY25: health insurance', 'Health insurance', '580 million Indians have health cover; group policies cover the most',
   lede="IRDAI's annual report for FY25: 580 million lives covered, up from 573 mn. Premium grew 9.12% to ₹1.17 trillion. Insurers settled 32.6 mn claims worth ₹94,248 crore, an average of ₹28,910 per claim, and 58% of claims were cashless.",
   hook='Group policies cover the most lives (47.4%), individual policies the fewest (10.3%).',
   trap='Incurred claims ratio fell to 86.98% from 88.15%.')
st('insrules', 'Insurance rules and data (Mar 2026)', 'Insurance rules', 'Cashless claims: 1 hour to approve, 3 hours to settle',
   lede="From 1 Apr 2026 all life, general and health insurers and reinsurers adopt Ind AS, including Ind AS 117. Cashless health claims must be pre-authorised within 1 hour and finally approved within 3 hours. FM Sitharaman set the goal of insurance for all by 2033; India's per-capita premium is $97 against a global $943. Under PMFBY, insurers that settle claims late (beyond 21 days) pay 12% interest.",
   hook='1 hour to say yes, 3 hours to settle.',
   trap='PMJJBY gives ₹2 lakh cover for ₹436 a year.')
st('survey', 'Economic Survey 2026', 'Economic Survey', 'Economic Survey 2026 projects 6.8–7.2% growth for FY27',
   lede='The Economic Survey is the Finance Ministry\'s yearly report card on the economy, tabled just before the Budget. FM Nirmala Sitharaman tabled it in the Lok Sabha; it was prepared under Chief Economic Adviser V. Anantha Nageswaran and projects real GDP growth of 6.8–7.2% for FY27.')

# ---------------------------------------------------------------- 2
st('inft31', 'Inflation target renewed to March 2031', 'Monetary policy', 'The 4% inflation target stays for five more years', 'feature',
   lede='Since 2016 the RBI has worked to a fixed inflation target: CPI inflation of 4%, within a band of 2–6%. The target is reviewed every five years, and the government, with the RBI, has now notified the same 4% target for 1 Apr 2026 to 31 Mar 2031. The RBI also released Payments Vision 2028 and set the government\'s short-term borrowing limit (WMA) at ₹2.5 lakh crore for the first half of 2026-27.',
   nums=[('4%', 'CPI target'), ('2–6%', 'Tolerance band'), ('31 Mar 2031', 'Term ends'), ('₹2.5 lakh cr', 'WMA limit, H1')], chart=['inft'],
   trap='The first mandate (2016) ran to 31 Mar 2021. WMA is charged at the repo rate; an overdraft costs repo + 2%.')
st('inft', 'Inflation target to be retained at 4%', 'Monetary policy', 'Before the decision: the target was due for review in March 2026')
st('utkarsh', 'RBI Utkarsh 2029 strategy framework', 'RBI strategy', 'Utkarsh 2029: six pillars and 49 deliverables')
st('board', 'RBI Central Board 622nd meeting', 'RBI board', 'RBI\'s board meets in Patna and approves Utkarsh 2029',
   lede='The RBI\'s Central Board held its 622nd meeting in Patna, chaired by Governor Sanjay Malhotra, and approved the 2026-27 budget and the Utkarsh 2029 strategy. The balance of payments data for October–December 2025 showed a current account deficit of $30.1 bn for April–December 2025, 1% of GDP, and foreign portfolio investors taking out a net $4.3 bn.')
st('prb', 'Payments Regulatory Board (PRB)', 'Payments', 'The new Payments Regulatory Board meets for the first time')
st('rbidpi', 'RBI Digital Payments Index (RBI-DPI)', 'Payments', 'India\'s digital payments index rises to 516.76')
st('divall', 'RBI: dividend norms for all bank types', 'Banks · dividends', 'How much profit a bank may hand out', 'feature',
   lede='A dividend is the part of profit a bank pays its shareholders. New RBI Directions cover every type of bank: a bank first deducts 50% of its net NPAs from profit, and then may pay out only a share of what is left, depending on how strong its capital is, in 10 buckets from 0% to 100%. The overall cap is 75% for commercial banks, payments banks and small finance banks, and 80% for local area banks and regional rural banks.',
   nums=[('75%', 'Commercial, payments, SFBs'), ('80%', 'LABs and RRBs'), ('10', 'Capital buckets'), ('50%', 'Of net NPA deducted')], chart=['divall'],
   trap='The earlier draft proposed raising the cap from 40% to 75%; the final cap for LABs and RRBs is 80%, not 75%.')
st('divdraft', 'RBI draft: bank dividend payout cap 75% of PAT', 'Banks · dividends', 'The draft that raised the dividend cap from 40% to 75%')
st('div2fa', 'RBI: 2FA from 1 Apr 2026; dividend cap; CCR norms', 'Banks · payments', 'Two-step verification for every digital payment from 1 April')
st('relparty', 'RBI: related-party lending rules', 'Banks · governance', 'Loans to a bank\'s own insiders get board-level checks')
st('acq', 'RBI final acquisition finance framework for banks', 'Banks · lending', 'Banks may fund takeovers, but only up to 75% of the deal')
st('cme', 'RBI: Capital Market Exposure (CME) ceilings', 'Banks · risk', 'A bank\'s stock-market exposure is capped at 40% of its capital',
   lede='Capital Market Exposure is a bank\'s total exposure to the stock market. Under the new Concentration Risk Management Directions, a bank\'s aggregate exposure can be at most 40% of its eligible capital (Tier 1 + Tier 2), with direct investment and acquisition finance at most 20% each. Payment commitments by custodian banks to clearing corporations now count as financial guarantees.')
st('las', 'RBI: loans against eligible securities', 'Banks · lending', 'How much a bank may lend against your shares and mutual funds', 'feature',
   lede='When you borrow against shares, mutual funds or bonds, the bank lends only part of their value, the loan-to-value (LTV) ratio. From 1 Apr 2026 the RBI fixes it by asset: 60% against listed shares, 75% against equity mutual funds, and 85% against debt mutual funds. An individual can borrow at most ₹1 crore this way, and ₹25 lakh to buy shares in the market or in an IPO.',
   nums=[('60%', 'Listed shares'), ('75%', 'Equity MFs'), ('85%', 'Debt MFs'), ('₹1 cr', 'Cap per individual')], chart=['las'],
   trap='A breach of the LTV must be cured within 7 working days; loans against a bank\'s own securities are banned (except ₹10 lakh against its own long-term infra bonds).')
st('lei', 'RBI: Unique Identifiers in Financial Markets', 'Markets', 'A 20-character ID for every party and, from 2027, every derivative trade')
st('iob', 'RBI: Internal Ombudsman Directions, 2026', 'Banks · complaints', 'Every bank must have an internal ombudsman')
st('ombcomp', 'RBI Ombudsman: compensation limits', 'Banks · complaints', 'The RBI Ombudsman can award up to ₹30 lakh, plus ₹3 lakh for harassment',
   lede='When a customer\'s complaint against a bank is upheld, the RBI Ombudsman can settle a dispute of any amount. For consequential loss it can award compensation of up to ₹30 lakh, plus up to ₹3 lakh for time lost, expenses, harassment or mental anguish. Complaints are filed online on the CMS portal.')
st('nbfcrw', 'RBI: risk weights for NBFC infrastructure lending eased', 'NBFCs', 'NBFCs need less capital for good infrastructure loans')
st('psl', 'RBI: priority sector lending (PSL) tightening', 'Priority sector', 'One loan, one claim: priority sector rules tightened')
st('coopncdc', 'RBI/Government: cooperative banks measures', 'Cooperative banks', 'Bank loans to NCDC now count as priority sector lending')
st('calam', 'RBI: resolution framework for loans hit by natural calamities', 'Lending', 'A clear framework for relief when disaster hits borrowers')
st('msmel', 'RBI: MSME lending directions amended', 'MSME', 'Small firms can borrow ₹20 lakh without collateral')
st('kcc', 'RBI draft: Kisan Credit Card (KCC) Directions 2026', 'Farm credit', 'A draft rule book for Kisan Credit Cards')
st('rbp', 'DICGC: Risk-Based Premium (RBP) framework', 'Deposit insurance', 'Safer banks will pay less for deposit insurance', 'feature',
   lede='Every bank pays DICGC a premium to insure its customers\' deposits up to ₹5 lakh each. Until now every bank paid the same flat rate, 12 paise per ₹100 of deposits. From 1 Apr 2026 the premium depends on risk: a safer bank can pay up to 33.33% below card rate, and long-standing banks a further vintage incentive of up to 25%.',
   nums=[('12 paise', 'Old flat rate per ₹100'), ('33.33%', 'Max risk discount'), ('25%', 'Max vintage incentive'), ('₹5 lakh', 'Cover per depositor')], chart=['rbp'],
   trap='Local area banks and payments banks stay at the card rate; UCBs under SAF or PCA stay at card rate until they exit.')
st('dicgc', 'DICGC deposit insurance data', 'Deposit insurance', '97.6% of accounts are fully insured, but only 41.5% of the money')
st('fema', 'RBI: FEMA (Guarantees) Regulations, 2026', 'FEMA', 'Residents can no longer give credit guarantees for NRIs')
st('ecb', 'RBI: ECB framework eased', 'Foreign borrowing', 'Companies can borrow abroad up to $1 billion or 300% of net worth')
st('vrr', 'RBI: Voluntary Retention Route (VRR) folded into General Route', 'Foreign investment', 'A special bond route for foreign investors is merged into the normal one')
st('lbc', 'Land-border country (LBC) investment guidelines eased', 'FDI', 'Small stakes from neighbouring countries can come in without approval')
st('apa', 'CBDT: record Advance Pricing Agreements', 'Tax', 'A record 219 advance pricing deals in a year')
st('baggage', 'Baggage Rules, 2026 and DFS digital platforms', 'Customs', 'What a returning traveller can bring in duty-free')
st('emandate', 'RBI: Digital Payments e-mandate Framework 2026', 'Payments', 'Auto-debits: a warning 24 hours before, and limits without extra checks')
st('trai', 'TRAI: spam call penalty and 1600 series', 'Telecom', 'Telcos fined ₹150 crore for spam; banks must call from 1600 numbers')
st('cas', 'SEBI: closing auction session (CAS) and FPI reforms', 'SEBI', 'A 20-minute auction will set each share\'s closing price')
st('merchant', 'SEBI: merchant banker net worth overhaul', 'SEBI', 'Only financially stronger merchant bankers can handle big issues')
st('mfcat', 'SEBI: mutual fund scheme categorisation', 'SEBI · mutual funds', 'What each type of mutual fund must hold')
st('sebifeb', 'SEBI (Feb 2026): derivatives and market-structure rules', 'SEBI', 'Tighter derivative margins and a new rule for valuing gold in funds')
st('sebimar', 'SEBI Mar 2026: board reforms, MF safeguards, claims', 'SEBI', 'A voluntary lock on mutual fund folios and easier claims for nominees')
st('swasthya', 'PFRDA: NPS Swasthya Pension Scheme', 'Pensions', 'An NPS account that can also pay medical bills')
st('vatsalya', 'NPS Vatsalya Scheme Guidelines 2025', 'Pensions', 'NPS Vatsalya: a pension account a parent opens for a child')
st('pfrdab', 'PFRDA: banks may set up pension funds', 'Pensions', 'Banks may now run their own NPS pension funds')
st('ghg', 'MoEFCC: second round of GHG Emission Intensity targets', 'Carbon market', '208 more industries get binding carbon targets')
st('startrec', 'Startup recognition framework revised', 'Startups', 'Startups can be bigger, and deep-tech ones last 20 years')

# ---------------------------------------------------------------- 3
st('usint', 'India–US interim trade framework', 'Trade', 'The US sets an 18% tariff on Indian goods; India promises $500 bn of purchases', 'feature',
   lede='India and the US agreed the outline of an interim trade agreement, part of the bilateral trade talks launched on 13 Feb 2025. The US will charge a reciprocal tariff of 18% on most Indian goods, down from 50% on some of them, and remove it on generic medicines, gems and diamonds and aircraft parts once the agreement is concluded. India will cut tariffs on US industrial goods and intends to buy $500 bn of US energy, aircraft, technology and coking coal over 5 years.',
   nums=[('18%', 'US tariff on Indian goods'), ('$500 bn', 'Indian purchases, 5 years'), ('$30.94 bn', 'Exports cut 50% → 18%'), ('$86.35 bn', 'Exports to US, 2024')], chart=['ustar'],
   trap='The 18% still applies to leather and footwear, gems and jewellery, textiles, toys and machinery; $10.03 bn of exports go from 50% to zero.')
st('efta', 'India–EFTA TEPA', 'Trade', 'Four European countries, $100 bn of investment promised')
st('oman', 'India–Oman CEPA', 'Trade', 'Oman cuts duty to zero on 98.08% of its tariff lines')
st('uae', 'India–UAE: double trade to $200 billion by 2032', 'Trade', 'India and the UAE aim for $200 billion of trade by 2032')
st('wawar', 'West Asia (Iran) war: Hormuz, FATF, trade effects', 'World', 'War closes in on the Strait of Hormuz, the route for a fifth of the world\'s oil', 'feature',
   lede='The conflict between Israel and Iran disrupted the Strait of Hormuz, the narrow sea lane between Iran to the north and Oman and the UAE to the south. About 20% of the world\'s oil and nearly all of Qatar\'s LNG pass through it, which makes it the second-busiest oil chokepoint after the Strait of Malacca. Also in this period, FATF added Kuwait and Papua New Guinea to its grey list, and the WTO met at Yaoundé for MC14.',
   nums=[('~20%', 'Of world oil'), ('20+ mn', 'Barrels a day'), ('2nd', 'Busiest oil chokepoint'), ('60 days', 'US Jones Act waiver')], chart=['hormuz'],
   trap='Malacca is the busiest oil chokepoint, Hormuz the second. WTO MC14 was at Yaoundé, Cameroon.')
st('uswd', 'US withdrawals: WHO, Paris Agreement, 66 organisations, ISA', 'World', 'The US leaves the WHO, the Paris deal and 66 other bodies')
st('bbnj', 'UN High Seas (BBNJ) treaty enters into force', 'Oceans', 'A treaty for the high seas comes into force on 17 January')
st('pacm', 'UNFCCC: first carbon credits under Paris Agreement Crediting Mechanism', 'Climate', 'The first carbon credits under the Paris Agreement go to a Myanmar cooking project')
st('cbam', 'EU CBAM comes into force', 'Climate · trade', 'The EU starts charging for the carbon in imported steel and cement')
st('brics', 'India chairs BRICS in 2026', 'BRICS', 'India takes the BRICS chair and hosts the 18th summit')
st('unsc', 'UNSC new non-permanent members and OPEC+', 'UN', 'Five new members join the UN Security Council')
st('bulgaria', 'Bulgaria joins the euro', 'Europe', 'Bulgaria becomes the 21st country to use the euro')
st('mercosur', 'EU–Mercosur trade agreement', 'Trade', 'The EU and Mercosur sign a trade deal after talks begun in 1999')
st('indpak', 'India–Pakistan: nuclear installations list', 'Neighbours', 'India and Pakistan swap nuclear lists every 1 January')

# ---------------------------------------------------------------- 4
st('fc16', '16th Finance Commission report', 'Federal finance', 'The States keep 41% of central taxes for 2026-31', 'feature',
   lede='The Finance Commission is a constitutional body under Article 280 that decides how the Centre shares its tax money with the States. The 16th Commission, set up on 31 Dec 2023 under Arvind Panagariya, covers 2026-31. Its report keeps the States\' share of the divisible tax pool at 41%, the same as under the 15th Commission (2021-26).',
   nums=[('41%', 'States\' share'), ('2026-31', 'Period'), ('Article 280', 'Constitution'), ('Arvind Panagariya', 'Chair')], chart=['fc'],
   trap='41% is unchanged: the 15th Finance Commission (2021-26) also gave 41%.')
st('budget9', 'Union Budget 2026: Sitharaman', 'Budget', 'Sitharaman presents her ninth Budget in a row')
st('census', 'Census 2027: freeze on administrative boundaries', 'Census', 'Census 2027: India\'s first digital count', 'feature',
   lede='India\'s 16th census, and 8th since independence, will be the first digital one, with an option for people to count themselves. Phase I begins on 1 Apr 2026 with self-enumeration and house listing; population enumeration follows in September 2026. To keep the count clean, States may not change district or tehsil boundaries until 31 Mar 2027. The last census was in 2011.',
   nums=[('1 Mar 2027', 'Reference date'), ('₹11,718.24 cr', 'Outlay'), ('16', 'Languages on app and portal'), ('31 Mar 2027', 'Boundary freeze till')], chart=['census'],
   trap='For Ladakh and snow-bound areas of J&K, Uttarakhand and Himachal the reference date is 1 Oct 2026.')
st('ibc', 'Insolvency and Bankruptcy Code (Amendment) Bill', 'Law', 'Lenders can start insolvency themselves under the IBC Bill')
st('itrules', 'IT Rules amendment 2026', 'Law · internet', 'Platforms must take down unlawful content within 3 hours')
st('keralam', 'Kerala to be renamed Keralam', 'States', 'Kerala is to become Keralam')
st('scmens', 'Supreme Court: menstrual hygiene is part of Article 21', 'Courts', 'Free sanitary napkins in every school: menstrual hygiene is a right')
st('sports', 'National Sports Governance Act 2025', 'Sport · law', 'A sports board and tribunal to clean up federations')
st('ecinet', 'ECINET and IICDEM 2026', 'Elections', 'ECINET: one app for every election service')
st('seed', 'India–Japan swap renewed; new Seed and Pesticide Acts', 'RBI · farms', 'A $75 billion swap line with Japan and new Seed and Pesticide Acts')
st('plfs', 'PLFS Annual Report 2025', 'Jobs', 'Unemployment at 3.1%; fewer Indians work on farms', 'feature',
   lede='The Periodic Labour Force Survey measures who is working or looking for work. For 2025 (age 15+, usual status), 59.3% of people were in the labour force and unemployment was 3.1%. Youth unemployment fell from 10.3% to 9.9%. The share of workers in agriculture fell from 44.8% to 43.0%, while manufacturing rose from 11.6% to 12.1%.',
   nums=[('59.3%', 'LFPR'), ('3.1%', 'Unemployment'), ('9.9%', 'Youth unemployment'), ('43.0%', 'Work in agriculture')], chart=['plfs'],
   trap='Urban unemployment (4.8%) is double rural (2.4%); urban youth unemployment is 13.6%.')
st('epfo', 'EPFO: UPI withdrawals and simplified rules', 'Provident fund', 'EPF money straight to your bank through UPI')
st('hpv', 'HPV vaccination drive launched from Ajmer', 'Health', 'Free HPV vaccine for 14-year-old girls, launched from Ajmer')
st('rahat', 'PM RAHAT scheme (road accident victims)', 'Road safety', 'Cashless treatment up to ₹1.5 lakh for accident victims')
st('cbdcpds', 'CBDC-based digital food coupon pilot', 'Food · payments', 'Ration through the e-rupee: a pilot in Gujarat')
st('manav', 'MANAV Vision for AI', 'AI', 'MANAV: India\'s idea of human-centred AI')
st('startdef', 'DPIIT revised start-up definition', 'Startups', 'Startup turnover limit doubles to ₹200 crore')
st('rice', 'India is the world\'s largest rice producer', 'Farms', 'India grows more rice than China')
st('bullet', 'Mumbai–Ahmedabad bullet train', 'Railways', 'The first bullet train is due on 15 Aug 2027')
st('coking', 'Coking coal notified as Critical and Strategic Mineral', 'Mining', 'Coking coal becomes a critical mineral')
st('apr1', 'Rules from 1 April 2026: FASTag pass, FSSAI, waste', 'Rules', 'What changed on 1 April: FASTag pass, food licences and waste')
st('ndc', 'India\'s NDC 2031-35', 'Climate', 'India\'s new climate pledge: 60% clean power capacity by 2035', 'feature',
   lede='Under the Paris Agreement every country files a Nationally Determined Contribution (NDC), its climate promise. India has already met its 2030 targets: emissions intensity of GDP was cut 36% by 2020, and non-fossil sources make up 52.57% of power capacity. The new NDC for 2031-35 raises the bar to a 47% intensity cut and 60% non-fossil capacity by 2035, on the way to net zero by 2070.',
   nums=[('47%', 'Intensity cut by 2035'), ('60%', 'Non-fossil capacity by 2035'), ('3.5–4.0 bn t', 'Extra carbon sink'), ('2070', 'Net zero')], chart=['ndc'],
   trap='The 2030 targets (33–35% intensity cut, 40% non-fossil) are already met; 47% and 60% are the 2035 targets.')
st('swm', 'Solid Waste Management Rules, 2026', 'Waste', 'Four bins for every home under the new waste rules')
st('ramsar', 'Ramsar sites: India now has 98', 'Wetlands', 'India now has 98 Ramsar sites')
st('dolphin', 'Project Dolphin: second range-wide dolphin survey', 'Wildlife', 'A second count of the Ganges river dolphin')
st('biodiv', 'India\'s biodiversity reports: Nagoya NR1 and CBD NR-7', 'Biodiversity', 'India reports to the UN on nature: all 23 targets on track')
st('roots', 'Meghalaya living root bridges: UNESCO nomination', 'Heritage', 'Meghalaya\'s living root bridges nominated for World Heritage')
st('kumbhal', 'Kumbhalgarh Wildlife Sanctuary declared Eco-Sensitive Zone', 'Rajasthan', 'Kumbhalgarh gets a 1 km eco-sensitive zone')
st('unnati', 'Rajasthan: Raj-UNNATI project monitoring', 'Rajasthan', 'Rajasthan is the first State to copy PRAGATI, as Raj-UNNATI')
st('pesa', 'PESA Act rules in Jharkhand', 'States', 'Jharkhand notifies PESA rules after 25 years')

# ---------------------------------------------------------------- 5
st('cspoc', 'CSPOC and AIPOC', 'Conferences', 'Commonwealth Speakers meet in Delhi; India\'s presiding officers in Lucknow')
st('cmte', 'Committees: PFRDA, IRDAI and foreign banks', 'Committees', 'New panels on NPS payouts, reinsurance and foreign bank branches')
st('canada', 'India–Canada CEPA talks launched', 'Trade', 'India and Canada restart trade talks, aiming at $50 billion by 2030')

# ---------------------------------------------------------------- 6
st('prahaar', 'PRAHAAR: national counter-terrorism policy', 'Security', 'PRAHAAR: India\'s counter-terrorism policy in seven pillars')

# ---------------------------------------------------------------- 7
st('padma', 'Padma Awards 2026 and gallantry awards', 'Awards', '131 Padma Awards, and an Ashoka Chakra for Shubhanshu Shukla')
st('qs', 'QS World University Rankings by Subject 2026', 'Rankings', 'A record 27 Indian entries in the world\'s top 50')

# ---------------------------------------------------------------- 8
st('vbg', 'Viksit Bharat–G RAM G Act, 2025', 'Rural jobs', '125 days of work: a new law replaces MGNREGA', 'feature',
   lede='The Viksit Bharat–Guarantee for Rozgar and Ajeevika Mission (Gramin) Act replaces the MGNREGA framework. Every rural household is now guaranteed 125 days of paid work a year instead of 100. The cost is shared between the Centre and States 60:40 (90:10 for NE and Himalayan states), and States may declare up to 60 no-work days a year in the sowing and harvest seasons.',
   nums=[('125', 'Days guaranteed'), ('60:40', 'Centre : State'), ('60', 'No-work days allowed'), ('₹1,51,282 cr', 'Annual need')], chart=['vbg'],
   trap='An unemployment allowance is due after 15 days and is the State\'s liability; social audits every 6 months.')
st('svanidhi', 'PM SVANidhi restructured', 'Street vendors', 'Bigger loans for street vendors, now till March 2030')
st('vishwakarma', 'PM Vishwakarma scheme: benefits', 'Craftspeople', 'PM Vishwakarma: training, tools and loans for craftspeople')
st('pmkisan', 'PM-KISAN 22nd instalment', 'Farmers', 'PM-KISAN\'s 22nd instalment reaches 9.32 crore farmers',
   lede='PM-KISAN pays farmers ₹6,000 a year in three instalments of ₹2,000. The 22nd instalment, about ₹18,640 crore, was released on 13 Mar 2026 from Guwahati to 9.32 crore farmers. The Kisan Credit Card gives cheap crop loans: with the 3% prompt-repayment subvention, the effective rate is 4% on loans up to ₹3 lakh, and 7.72 crore cards are active.')
st('pulses', 'Mission for Aatmanirbharta in Pulses', 'Farmers', 'A ₹11,440 crore mission to make India self-sufficient in pulses')
st('jjm', 'Jal Jeevan Mission extended to Dec 2028', 'Water', 'Tap water for every rural home: deadline pushed to December 2028', 'feature',
   lede='The Jal Jeevan Mission, launched in August 2019 as Har Ghar Jal, aims to give every rural home a tap connection. 15.80 crore of 19.36 crore rural households, 81.61%, now have one. The Cabinet extended the mission to December 2028 with a total outlay of ₹8.69 lakh crore, and raised central assistance from ₹2.08 lakh crore to ₹3.59 lakh crore.',
   nums=[('Dec 2028', 'New deadline'), ('₹8.69 lakh cr', 'Total outlay'), ('81.61%', 'Homes with taps'), ('₹3.59 lakh cr', 'Central assistance')], chart=['jjm'],
   trap='Central assistance rose by ₹1.51 lakh crore; ₹8.69 lakh crore is the total outlay, not the Centre\'s share.')
st('udan', 'Regional Connectivity Scheme – Modified UDAN', 'Aviation', 'Modified UDAN: ₹28,840 crore for flights to small towns over 10 years')
st('bhavya', 'BHAVYA and Small Hydro Power scheme', 'Industry · energy', 'BHAVYA: 100 ready-made industrial parks')
st('dpi', 'India\'s Digital Public Infrastructure (DPI) snapshot', 'Digital', 'India\'s digital public infrastructure, from UPI to DigiLocker')
st('rahatchain', 'How PM RAHAT works', 'Road safety', 'From a 112 call to payment in 10 days: how PM RAHAT works', month='February')
