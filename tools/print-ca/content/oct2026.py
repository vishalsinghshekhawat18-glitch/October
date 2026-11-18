# October 2026 print edition: the authored story layer for tools/print-ca/build.py.
# Facts only from the October notes; every number written here is checked against them.
NOTES = '../../../archive/current-affairs/CA_October_2026.html'
MONTH = 'October 2026'
PERIOD = '1–31 October'
OUTFILE = 'CA_October_2026_print'

COVER = dict(kicker='Section 2', title='The month the RBI turned the dial up', lead='mpc',
             dek='The first repo rate hike in nearly four years, a tighter stance, and a string of rules to cool the rupee market: what changed, and the numbers to keep.',
             stats=[('5.50%', 'Repo rate'), ('11.39%', 'WPI, September'), ('$476.20 bn', 'Exports, Apr–Sep'), ('100th', 'India, Global Hunger Index')])
COVER_LINES = [('Section 1 · Growth', 'Who said India will grow how fast', 'gdp'),
               ('Section 1 · Banking', 'IDBI Bank goes to a Fairfax arm for ₹52,878.08 crore', 'idbi'),
               ('Section 4 · Farms', 'Safflower gets the biggest MSP rise', 'msp'),
               ('Section 6 · Sports', 'India fourth at the Asian Games with 85 medals', 'asiang')]
LEADS = {1: 'GDP forecasts · WPI 11.39% · exports and FTAs · GST Council reforms · IDBI sale',
         2: 'Repo up to 5.50% · CRR and forex rules · SEBI closing auction · credit risk-o-meter',
         3: 'G7 oil release · COP31 in Antalya · SCO in Dushanbe · India–UK JETCO',
         4: 'Rabi MSP · 375 rural works · BS-VII draft · GOBARdhan · Ramsar sites reach 103',
         5: 'High Level Committee on Banking for Viksit Bharat',
         6: 'First Indian CAR-T therapy · NVS-03 launch · Asian Games and Chess Olympiad',
         7: 'Nobel Prizes · poverty and hunger indices · Emissions Gap Report',
         8: 'Schemes of the month at a glance',
         9: 'Key numbers · GDP forecasts · upcoming dates · flashcards'}
DASH = '''<table class="score dash"><thead><tr><th>Indicator</th><th>Before</th><th>Now</th><th>Trend</th></tr></thead><tbody>
<tr><td>Repo rate</td><td>5.25%</td><td>5.50%<small> from 7 Oct</small></td><td>▲ first hike in nearly 4 years</td></tr>
<tr><td>WPI (wholesale) inflation</td><td>9.92% Aug</td><td>11.39% Sep</td><td>▲ rising</td></tr>
<tr><td>CPI (retail) inflation</td><td>4.83% Aug</td><td>5.54% Sep</td><td>▲ rising</td></tr>
<tr><td>Core industries (ICI)</td><td>5.9% Aug</td><td>7.9% Sep</td><td>▲ faster</td></tr>
<tr><td>Industrial production (IIP)</td><td>8.0% Aug</td><td>6.7% Sep</td><td>▼ slower</td></tr>
<tr><td>Unemployment (PLFS, 15+)</td><td>5.0% Aug</td><td>5.0% Sep</td><td>■ steady</td></tr>
</tbody></table>'''

def make_charts(hbar, steps, table_chart):
    return {
     'gdp': hbar("India's growth forecasts (%)", [('UNCTAD, calendar 2026', 7.3, '7.3'), ('World Bank, FY27', 7.1, '7.1'), ('RBI, FY27', 7.1, '7.1'), ('IMF, FY27', 7, '7')], 7.3),
     'repo': steps('The repo rate path', [('6.50%', '8 Feb 2023 · last hike'), ('5.25%', '5 Dec 2025 · cut'), ('5.50%', '7 Oct 2026 · hike')]),
     'expg': hbar('Fastest-growing merchandise exports, September 2026 (%)', [('Electronic goods', 70.44, '70.44'), ('Other cereals', 49.88, '49.88'), ('Handicrafts', 43.19, '43.19')], 70.44, hi=0),
     'fisc': hbar('Fiscal deficit in the first half, as % of the full-year target', [('Apr–Sep 2026 (H1 FY27)', 42.1, '42.1'), ('Same point last year', 36.5, '36.5')], 42.1, hi=0),
     'iciw': hbar('The three heaviest core industries (weight)', [('Electricity', 30.932, '30.932'), ('Refinery products', 22.572, '22.572'), ('Steel', 17.584, '17.584')], 30.932),
     'jfdi': hbar('FDI equity inflows, April–June 2026 ($ bn)', [('Japan', 5.71, '5.71'), ('Singapore', 5.22, '5.22'), ('Netherlands', 1.38, '1.38')], 5.71, hi=0),
     'fta': steps("India's trade deals in order", [('2021', 'Mauritius CECPA'), ('May 2022', 'UAE CEPA'), ('Dec 2022', 'Australia ECTA'), ('Mar 2024', 'EFTA TEPA signed'), ('Jul 2025', 'UK CETA signed'), ('Dec 2025', 'Oman CEPA · NZ FTA'), ('Jan 2026', 'EU FTA'), ('Feb 2026', 'US interim framework')]),
     'idbi': hbar('Who owns IDBI Bank after the sale (%)', [('Life Insurance Corporation', 19, '19'), ('Government', 15, '15')], 19),
     'cas': steps('The new end of the trading day (PM)', [('3:30', 'closing auction opens'), ('3:31–3:36', 'market and limit orders'), ('3:36–3:40', 'limit orders only'), ('3:38–3:40', 'random close'), ('3:45', 'derivatives stop'), ('3:50–4:00', 'post-close session')], on_last=False),
     'msp': hbar('Rise in MSP, ₹ per quintal', [('Safflower', 675, '675'), ('Rapeseed and mustard', 413, '413'), ('Lentil', 390, '390'), ('Barley', 136, '136'), ('Gram', 83, '83'), ('Wheat', 25, '25')], 675, hi=0),
     'works': hbar('375 permissible works, by pillar', [('Water security', 128, '128'), ('Core rural infrastructure', 111, '111'), ('Livelihood infrastructure', 98, '98'), ('Disaster preparedness', 38, '38')], 128),
     'cbg': steps('CBG blending obligation for city gas companies', [('3%', 'FY27'), ('4%', 'FY28'), ('5%', 'from FY29')]),
     'crim': table_chart('Old law and new law, by number of sections', ['Old law', 'Sections', 'New law', 'Sections'],
                         [['Indian Penal Code', '511', 'Bharatiya Nyaya Sanhita', '358'], ['Code of Criminal Procedure', '484', 'Bharatiya Nagarik Suraksha Sanhita', '531'], ['Indian Evidence Act', '167', 'Bharatiya Sakshya Adhiniyam', '170']], big_cols=(1, 3)),
     'asg': hbar('Asian Games 2026: total medals', [('China', 341, '341'), ('Japan', 269, '269'), ('South Korea', 150, '150'), ('India', 85, '85')], 341, hi=3),
     'mpi': hbar('Share of Indians in multidimensional poverty (%)', [('2005/06', 55.1, '55.1'), ('2019/21', 16.4, '16.4')], 55.1, hi=1),
     'wbp': hbar('Indians below $4.20 a day (%)', [('2011', 57.7, '57.7'), ('2023', 16.1, '16.1'), ('2026, projected', 14.2, '14.2'), ('2028, projected', 12.1, '12.1')], 57.7, hi=1),
     'ghi': hbar('Global Hunger Index 2026: South Asia ranks (lower is better)', [('Sri Lanka', 53, '53rd'), ('Nepal', 72, '72nd'), ('Bangladesh', 84, '84th'), ('India', 100, '100th'), ('Pakistan', 106, '106th'), ('Afghanistan', 108, '108th')], 108, hi=3),
    }

SEC_INTRO = {
 1: 'Growth forecasts, prices and output, trade and tax changes, and a busy month for banks, pensions and payments.',
 2: 'The RBI raised the repo rate and tightened its rules on cash, currency and capital; SEBI changed how the trading day ends.',
 3: 'An oil release by the G7, the run-up to COP31, regional meetings and new partners for India.',
 4: 'New laws and campaigns, farm prices and rural works, cleaner fuel and roads, wildlife and heritage, and news from the states.',
 5: 'One committee to note this month: a review of banking for Viksit Bharat.',
 6: 'A first Indian cancer cell therapy, supercomputers and quantum links, new ships and deals, and a big month in sport.',
 7: 'The Nobel Prizes and the reports that measure poverty, hunger and the emissions gap.',
 8: 'This month the schemes are covered in their own sections; here they are side by side.',
}

CHAPTERS = {
 1: [('1.1', 'Who expects what growth', 'Five institutions forecast India\'s growth, and a new survey asks companies about their investment plans.', ['gdp', 'wbidu', 'unctad', 'imf', 'capex']),
     ('1.2', 'Prices, factories and jobs', 'Wholesale prices rose, core industries sped up, factory output slowed and unemployment held steady.', ['wpi', 'plfs', 'ici', 'iip', 'asi']),
     ('1.3', 'The government\'s money', 'Half-year borrowing and the rates on small savings.', ['fisc', 'ssr']),
     ('1.4', 'Trade, investment and tax', 'Exports, the FTA list, Japan\'s investment surge and a long list of tax changes.', ['trade', 'fta', 'jfdi', 'igst', 'mdr', 'dtaa', 'maldives', 'gstc', 'ecom', 'fastds', 'sgf']),
     ('1.5', 'Clean power and foreign earnings', 'World Bank money for minerals, a non-fossil milestone and new FEMA rules for freelancers.', ['wbg', 'nonfossil', 'femaf']),
     ('1.6', 'Society and pay', 'Child marriage, the EPFO wage ceiling and a dearness allowance rise.', ['child', 'epfo', 'da']),
     ('1.7', 'Banks, pensions and payments', 'A bank sale, two pension platforms, UPI numbers and RBI\'s new backup data centre.', ['idbi', 'bob', 'tatkal', 'npsc', 'upi', 'sdr', 'cic', 'paytm', 'bangkok', 'fincl', 'polymer', 'rbidc'])],
 2: [('2.1', 'The RBI raises rates', 'The repo rate went up, the Bank Rate followed, and banks must keep almost all their CRR every day.', ['mpc', 'bankrate', 'crr', 'sdrp', 'aa']),
     ('2.2', 'RBI rules for currency and capital', 'Curbs on rupee derivatives, a dollar swap window, bond rates, ownership and new capital rules.', ['fx', 'swap', 'frb', 'share', 'cva', 'oprisk', 'notes', 'scst']),
     ('2.3', 'SEBI changes the rules of the market', 'A new closing auction, a credit risk-o-meter, settlement and advertising codes and portfolio manager rules.', ['cas', 'crm', 'settle', 'jagrook', 'pms', 'cac', 'ipo', 'fpikyc']),
     ('2.4', 'Other regulators', 'Rules for AI in ads and audits of multi-state cooperatives.', ['asci', 'mscs'])],
 3: [('3.1', 'Oil, climate and trade', 'A G7 oil release, the COP31 line-up, climate pledges that fall short and a better trade outlook.', ['g7', 'cop31', 'ndc', 'wto']),
     ('3.2', 'Groups and partners', 'Ghana joins the Big Cat Alliance, two regional meetings, the UK trade talks and a new chair for the IMF and World Bank boards.', ['ibca', 'bimstec', 'sco', 'jetco', 'pak', 'brazil'])],
 4: [('4.1', 'Laws and institutions', 'Classical language centres, UPSC at 100, AFSPA, a new evidence law and the criminal laws ranking.', ['crim', 'bbea', 'upsc', 'classical', 'bharatpol', 'nsf', 'afspa', 'shram']),
     ('4.2', 'Farms, food and welfare', 'Winter crop prices, more rural works, pensions renamed, Farmer IDs, cheaper cancer drugs and piped gas.', ['msp', 'works', 'nsap', 'farmerid', 'cancer', 'png']),
     ('4.3', 'Roads, ports and cleaner fuel', 'A biogas scheme, stricter vehicle norms, old trucks replaced, toll passes and greener shipping.', ['gobar', 'bs7', 'parivartan', 'fastagx', 'annual', 'ports', 'greenship', 'plb']),
     ('4.4', 'Wildlife, heritage and schools', 'Cheetah cubs, two new Ramsar sites, three tentative heritage sites and a report on school toilets.', ['cheetah', 'ramsar', 'unesco', 'wash']),
     ('4.5', 'States and UTs', 'Delhi, Ladakh, Odisha, Assam and Nagaland.', ['organic', 'lahdc', 'fnta', 'delhi', 'lao'])],
 5: [('5.1', 'Committees', 'A review of the banking sector for 2047.', ['hlcb'])],
 6: [('6.1', 'Science and health', 'An Indian CAR-T therapy, a WHO-approved HPV vaccine, supercomputers, quantum links and a navigation satellite.', ['cart', 'cervavac', 'gslv', 'nsm', 'nqm']),
     ('6.2', 'Defence', 'Record exports, new ships and contracts, exercises and rice for the Army.', ['defexp', 'gsat', 'contracts', 'navy', 'samarthak', 'exer', 'dad', 'rice']),
     ('6.3', 'Sports', 'Asian Games and Asian Para Games in Japan, the Chess Olympiad and a change of captain.', ['asiang', 'para', 'chess', 'harman'])],
 7: [('7.1', 'Prizes', 'The Nobel winners and Indian award winners.', ['nobel', 'indaw']),
     ('7.2', 'Reports and rankings', 'Poverty falls, hunger stays serious and the emissions gap widens.', ['mpi', 'wbpov', 'ghi', 'egap'])],
}

S = {}
def st(key, card, tag, h, size='short', **kw): S[key] = dict(card=card, tag=tag, h=h, size=size, **kw)

# ---------- 1 ----------
st('gdp', 'India GDP growth: who projected what', 'Growth forecasts', 'Who said India will grow how fast', 'feature',
   lede='Several institutions forecast India\'s growth this month, and their figures are close enough to confuse. The World Bank and the RBI both expect 7.1% for FY27, the IMF 7%, and UNCTAD 7.3%, but UNCTAD\'s figure is for calendar 2026. Actual growth in April–June 2026 was 7.8%.',
   nums=[('7.1%', 'World Bank, FY27'), ('7.1%', 'RBI, FY27'), ('7%', 'IMF, FY27'), ('7.8%', 'Actual, Q1 FY27')], chart=['gdp'],
   trap="UNCTAD's 7.3% is for calendar 2026, not FY27. The Finance Ministry's 7.35% is a nowcast for July–September only.")
st('wbidu', 'World Bank: India Development Update', 'World Bank', 'World Bank raises India to 7.1% and looks at AI')
st('unctad', 'UNCTAD Trade and Development Report', 'UNCTAD', 'UNCTAD: the world slows, India stays fastest')
st('imf', 'IMF reports, October 2026', 'IMF', 'IMF lifts India\'s forecast to 7%')
st('capex', 'Capital expenditure (CAPEX) 2026 survey', 'Survey', 'A survey of what big companies plan to invest')
st('ssr', 'Small savings rates unchanged', 'Small savings', 'Small savings rates stay where they are')
st('asi', 'Annual Survey of Industries (ASI) 2024-25', 'Industry', 'Factory jobs cross 2 crore for the first time')
st('wpi', 'WPI (Wholesale Price Index) inflation, September', 'Inflation', 'Wholesale inflation jumps to 11.39%')
st('plfs', 'PLFS (Periodic Labour Force Survey) monthly bulletin', 'Jobs', 'Unemployment steady at 5.0%')
st('ici', 'Index of Core Industries (ICI)', 'Core industries', 'Core industries grow 7.9%, led by iron ore', 'feature',
   lede='The Index of Core Industries tracks nine basic industries, from coal and steel to electricity. In September 2026 it grew 7.9% from a year earlier, faster than the revised 5.9% of August. Six of the nine grew; iron ore rose most, by 18.4%, while fertilizers fell 11.7%.',
   nums=[('7.9%', 'Growth, September'), ('5.9%', 'August, revised'), ('18.4%', 'Iron ore, highest'), ('−11.7%', 'Fertilizers, lowest')], chart=['iciw'],
   trap='The base year is 2022-23. Electricity, not steel, has the largest weight.')
st('iip', 'Index of Industrial Production, September', 'Industry', 'Factory output growth slows to 6.7%')
st('fisc', 'Fiscal deficit, April–September', 'Government finances', 'Half the year gone, 42.1% of the deficit used', 'feature',
   lede='The fiscal deficit is the gap between what the government spends and what it earns. By the end of September 2026 it had reached ₹7,14,413 crore, which is 42.1% of the target for the whole year. At the same point last year it was 36.5%.',
   nums=[('₹7,14,413 cr', 'Deficit, Apr–Sep'), ('42.1%', 'Of full-year target'), ('50.3%', 'Receipts, of target'), ('47.7%', 'Spending, of target')], chart=['fisc'],
   trap='The full-year Budget Estimate is ₹16,95,768 crore; the figures are released by the Controller General of Accounts.')
st('igst', 'Integrated GST (IGST) on gold', 'Tax', 'Banks now pay 3% IGST on imported gold and silver')
st('jfdi', 'Japan tops India\'s FDI chart', 'Investment', 'Japan becomes the biggest investor in India', 'feature',
   lede='In April–June 2026 Japan invested $5.71 billion in India, more than in the whole of 2025-26 ($3.74 billion), and became the largest source of foreign direct investment. Singapore came second. Total equity FDI for the quarter was $19.81 billion, up 6%.',
   nums=[('$5.71 bn', 'Japan, Q1'), ('$3.74 bn', 'Japan, all of 2025-26'), ('$19.81 bn', 'Total equity FDI'), ('$7.3 bn', 'Net FDI, July')], chart=['jfdi'],
   trap='Order: Japan, Singapore, Mauritius, Netherlands, US.')
st('fta', 'India\'s FTA network', 'Trade deals', 'Nine trade deals, 38 countries', 'feature',
   lede='India has signed a run of trade agreements since 2021 so that its goods enter other markets more easily. The list runs from Mauritius in 2021 to the European Union in January 2026, with an interim framework with the United States announced in February 2026.',
   chart=['fta'], trap='The EFTA TEPA was signed on 10 Mar 2024 but came into force only on 1 Oct 2025.')
st('mdr', 'UPI Merchant Discount Rate (MDR) deferred', 'Payments', 'A fee on big UPI shop payments is put off till after Diwali')
st('dtaa', 'India–Mauritius tax treaty amended', 'Tax treaty', 'Mauritius treaty gets a test against tax dodging')
st('maldives', 'Maldives: India rolls over', 'Neighbours', 'India rolls over a ₹30 billion swap for the Maldives')
st('gstc', '57th GST Council meeting', 'GST', 'GST Council drops arrest powers and speeds up refunds', 'feature',
   lede='At its 57th meeting on 8 October, the GST Council made the tax gentler and simpler. It removed the power to arrest, raised the limit for prosecution from ₹1 crore to ₹5 crore, cut the top general penalty and started moving refunds to an automatic system.',
   nums=[('₹1 cr → ₹5 cr', 'Prosecution limit'), ('₹25,000 → ₹10,000', 'Top general penalty'), ('15 → 10 days', 'Refund acknowledgement'), ('90%', 'Refund paid provisionally')],
   trap='Arrest powers go by omitting Section 69 of the CGST Act, 2017.')
st('trade', 'India trade data, April–September', 'Trade', 'Exports grow, but imports grow faster', 'feature',
   lede='In April–September 2026 India sold $476.20 billion of goods and services abroad, up 13.84%. It bought $551.13 billion, up 15.68%, leaving a trade deficit of $74.93 billion. In September, electronic goods exports grew fastest, by 70.44%.',
   nums=[('$476.20 bn', 'Total exports'), ('$551.13 bn', 'Total imports'), ('$74.93 bn', 'Trade deficit'), ('$44.40 bn', 'Goods exports, September')], chart=['expg'],
   trap='The US is the largest merchandise export destination.')
st('ecom', 'GST registration for small e-commerce sellers', 'GST', 'Small online sellers can register in other states through a platform\'s warehouse')
st('fastds', 'Foreign Assets of Small Taxpayers Disclosure Scheme', 'Tax', 'A one-time window to declare foreign assets')
st('sgf', 'SME Growth Fund', 'MSME', '₹10,000 crore to buy stakes in growing small firms')
st('wbg', 'World Bank Group (WBG): critical minerals', 'World Bank', 'World Bank to put $19 billion into critical minerals')
st('nonfossil', 'India crosses 300 GW non-fossil', 'Energy', 'India crosses 300 GW of non-fossil power')
st('femaf', 'New FEMA rules for freelancers', 'FEMA', 'Freelancers must declare foreign earnings to their bank')
st('child', 'Child marriage in India', 'Social issue', 'One in three child brides in the world is Indian',
   lede='India accounts for about one in three child brides worldwide, and about one in five young Indian women are married before 18. Five states, led by Uttar Pradesh and Bihar, have more than half of India\'s child marriages. The law sets the minimum age at 18 for women and 21 for men.')
st('epfo', 'EPFO wage ceiling raised', 'EPFO', 'Compulsory PF now covers pay up to ₹25,000')
st('da', 'Dearness Allowance up 3 points', 'Cabinet', 'DA goes up to 63%, and three schemes get money')
st('bob', 'Bank of Baroda (BoB) enters pension fund', 'Pensions', 'Bank of Baroda starts a pension fund company')
st('tatkal', 'NPS Tatkal', 'Pensions', 'Join NPS in minutes through UPI')
st('sdr', 'Special Drawing Rights (SDR)', 'IMF', 'SDR: five currencies, next review by July 2027',
   lede='Special Drawing Rights are a reserve asset created by the IMF in 1969. They are not a currency, but countries hold them alongside their foreign exchange reserves. Their value comes from five currencies: the US dollar, euro, renminbi, yen and pound sterling.')
st('cic', 'Core Investment Company (CIC)', 'NBFC', 'Indiabulls becomes a Core Investment Company',
   lede='The RBI registered Indiabulls as a Core Investment Company, a kind of NBFC that mainly holds shares in its own group companies. To qualify, a company needs assets of at least ₹100 crore, with at least 90% of net assets in group companies.')
st('paytm', 'Paytm Payments Bank removed', 'RBI', 'Paytm Payments Bank leaves the list of scheduled banks')
st('idbi', 'IDBI Bank: Cabinet approves sale', 'Privatisation', 'IDBI Bank goes to a Fairfax arm for ₹52,878.08 crore', 'feature',
   lede='The government and LIC will sell 60.72% of IDBI Bank to a Canadian subsidiary of Fairfax Financial Holdings for ₹52,878.08 crore. The government sells 30.48% and LIC 30.24%. Afterwards they keep 34% between them.',
   nums=[('60.72%', 'Stake sold'), ('₹52,878.08 cr', 'Price'), ('30.48% + 30.24%', 'Government + LIC'), ('34%', 'Kept by both')], chart=['idbi'],
   trap='IDBI began in 1964 as a development financial institution and has been a private-sector bank in RBI\'s books since 21 Jan 2019.')
st('bangkok', "'Bangkok Blueprint' to fight cyber fraud", 'Cyber fraud', 'IMF and World Bank plan to fight a $1 trillion fraud problem')
st('fincl', 'Nationwide Financial Inclusion saturation campaign', 'Inclusion', 'A campaign to cover every panchayat with accounts, insurance and pensions')
st('polymer', 'Polymer banknotes: RBI proposal', 'Currency', 'Plastic ₹10 and ₹20 notes for field trials')
st('upi', 'UPI data, September 2026', 'Payments', 'UPI: 24.07 billion payments in September')
st('npsc', 'NPS Central: one platform', 'Pensions', 'One NPS website, log in without your PRAN')
st('rbidc', 'RBI second Data Centre and ECCTI', 'RBI', 'RBI\'s backup data centre opens at Jatni, Odisha')

# ---------- 2 ----------
st('mpc', 'Monetary Policy, October 2026', 'RBI · monetary policy', 'The RBI raises the repo rate for the first time in nearly four years', 'feature',
   lede='At its meeting on 5–7 October, the Monetary Policy Committee led by Governor Sanjay Malhotra raised the repo rate by 25 basis points, from 5.25% to 5.50%. It also changed its stance from neutral to calibrated tightening, so a rate cut is off the table for now. The last hike before this was in February 2023.',
   nums=[('5.25 → 5.50%', 'Repo rate'), ('5.25%', 'Standing Deposit Facility'), ('5.75%', 'MSF and Bank Rate'), ('+25 bps', 'Change')], chart=['repo'],
   trap='The stance is now "calibrated tightening", not neutral: the next move can be a hike or a pause.')
st('sdrp', 'Statement on Developmental and Regulatory Policies', 'RBI', 'Bank deposits to join your consolidated account statement')
st('crr', 'CRR daily maintenance raised', 'RBI · liquidity', 'Banks must keep 99% of their CRR every day')
st('fx', 'Forex derivatives tightened', 'RBI · forex', 'RBI curbs bets on the rupee')
st('frb', 'Floating Rate Bond (FRB) 2028 coupon', 'Bonds', 'FRB 2028 will pay 6.45% for six months',
   lede='Floating rate bonds pay interest that resets every six months. The RBI fixed the FRB 2028 rate at 6.45% for 4 October 2026 to 3 April 2027, and the FRB 2034 rate at 7.26%. The rate is linked to the 182-day treasury bill yield plus a fixed spread.')
st('share', 'Bank shareholding norms eased', 'RBI · ownership', 'One approval lets funds and insurers hold up to 10% of a bank')
st('swap', 'RBI special USD-INR forex swap window', 'RBI · forex', 'A swap window brings in $143.5 billion')
st('cva', 'Credit Valuation Adjustment (CVA)', 'RBI · capital', 'Banks to hold capital for derivative partners that may default')
st('notes', 'Note Sorting Machines', 'RBI · currency', 'When is a note too dirty to reuse? The RBI sets the rules')
st('scst', 'credit facilities to SCs and STs', 'RBI · credit', 'One rulebook for bank loans to SCs and STs')
st('bankrate', 'Bank Rate raised, penal interest', 'RBI', 'Bank Rate goes up to 5.75%')
st('aa', 'Account Aggregator network must be interoperable', 'RBI · data', 'Account aggregators must work together by 31 December')
st('oprisk', 'new operational-risk and leverage-ratio', 'RBI · capital', 'New capital rules for operational risk and leverage from April 2027')
st('crm', 'Credit Risk-o-Meter', 'SEBI · bonds', 'A colour-coded meter shows how risky a bond is')
st('settle', 'New settlement formula and fast-track', 'SEBI · enforcement', 'A new settlement formula and a fast route for small cases')
st('jagrook', 'Project Jagrook', 'SEBI · investors', 'Brokers must show investor warnings on their websites')
st('cas', 'Closing Auction Session (CAS) revised', 'SEBI · markets', 'A ten-minute auction will set the closing price', 'feature',
   lede='SEBI is changing how the trading day ends. From 3:30 to 3:40 PM a closing auction will decide each share\'s closing price, with the close falling at a random moment between 3:38 and 3:40 PM. Derivatives keep trading until 3:45 PM, and a post-close session runs from 3:50 to 4:00 PM.',
   nums=[('10 min', 'Auction length'), ('7 Dec 2026', 'Phase 1'), ('8 Feb 2027', 'Phase 2')], chart=['cas'],
   trap='Expiring derivatives settle at the VWAP of the last 30 minutes of continuous trading, 3:00–3:30 PM, not at the auction price.')
st('pms', 'Portfolio Managers Regulations, 2026', 'SEBI · PMS', 'New rules for portfolio managers, and a route into mutual funds')
st('cac', 'Common Advertisement Code', 'SEBI · ads', 'Celebrities can promote the firm, not the product')
st('ipo', 'IPO-size relaxation extended', 'SEBI · IPOs', 'IPOs can change their fresh issue by 50% till March 2027')
st('fpikyc', 'FPI KYC review made less frequent', 'SEBI · FPIs', 'Foreign investors face KYC reviews less often')
st('asci', 'ASCI guidelines on AI-generated ad content', 'Advertising', 'Ads must say when AI content could sway buyers')
st('mscs', 'Multi-State Co-operative Societies (Auditor', 'Cooperatives', 'Big cooperatives get a company-style audit report')

# ---------- 3 ----------
st('g7', 'G7 coordinated oil release', 'Energy', 'G7 to release 100 million barrels of oil')
st('cop31', 'COP31 (Conference of the Parties)', 'Climate', 'COP31: Antalya, 9–20 November',
   lede='The 31st UN climate conference, COP31, will be held at Antalya in Türkiye from 9 to 20 November 2026. Murat Kurum is COP31 President, and Australia\'s Chris Bowen leads the negotiations.')
st('ndc', 'Climate reports: NDC Synthesis Report', 'Climate', 'Climate pledges cut emissions only 6% by 2035')
st('wto', 'WTO: Global Trade Outlook', 'WTO', 'WTO doubles its goods trade forecast for 2026')
st('ibca', 'International Big Cat Alliance (IBCA)', 'Wildlife', 'Ghana joins the Big Cat Alliance, which gets a new home in Delhi')
st('bimstec', 'First BIMSTEC Home Ministers', 'BIMSTEC', 'BIMSTEC home ministers meet for the first time')
st('sco', 'SCO: 25th Council of Heads of Government', 'SCO', 'At the SCO in Dushanbe, India pushes INSTC and Chabahar')
st('jetco', 'India–UK JETCO', 'India–UK', 'India and the UK aim to double trade to $120 billion')
st('pak', 'Pakistan to chair IMF and World Bank Boards', 'IMF and World Bank', 'Pakistan to chair the IMF and World Bank boards in 2027')
st('brazil', 'Brazil: Lula wins fourth term', 'World', 'Lula wins a fourth term in Brazil')

# ---------- 4 ----------
st('classical', 'Five Centres of Excellence for classical languages', 'Languages', 'Five new centres for classical languages',
   lede='The Education Ministry approved five new Centres of Excellence for classical languages: Assamese at Tezpur University, Bengali at Visva-Bharati, Marathi at Deccan College in Pune, Pali at the Central University of Odisha and Prakrit at the Central University of Gujarat. India has 11 classical languages.')
st('bharatpol', 'BHARATPOL', 'Policing', 'BHARATPOL links Indian police with INTERPOL')
st('nsf', 'Scheme of Assistance to National Sports Federations', 'Sports', '₹7,386.74 crore for national sports federations')
st('upsc', 'UPSC completes 100 years', 'Institutions', 'UPSC turns 100',
   lede='India\'s first Public Service Commission was set up on 1 October 1926, so UPSC completed 100 years this month. It became the Union Public Service Commission on 26 January 1950. The Constitution deals with it in Part XIV, Articles 315 to 323.')
st('afspa', 'AFSPA extended in three states', 'Security', 'AFSPA extended for six months in three north-eastern states',
   lede='The Home Ministry extended the Armed Forces (Special Powers) Act, 1958, for six months from 1 October 2026 in parts of Manipur, Nagaland and Arunachal Pradesh. In Manipur it covers the whole state except 13 police-station areas.')
st('shram', 'Shram Samvad', 'Labour', 'A 90-day campaign to explain the four labour codes')
st('bbea', "Bankers' Books Evidence Act, 2026", 'Law', 'A new law for bank records as evidence replaces one from 1891')
st('crim', 'New criminal laws: implementation ranking', 'Criminal law', 'Assam tops the ranking for the new criminal laws', 'feature',
   lede='Three new criminal laws replaced the IPC, the CrPC and the Indian Evidence Act on 1 July 2024. The Home Ministry ranks states on how well they apply them, and Assam came first in implementing the Bharatiya Nyaya Sanhita, as it did in November 2025.',
   chart=['crim'], trap='BNS has fewer sections than the IPC (358 vs 511), but BNSS has more than the CrPC (531 vs 484).')
st('cancer', 'Cap on anti-cancer drug margins', 'Health', 'Margins on 137 cancer drugs capped at 30%')
st('png', 'National PNG Drive 3.0', 'Energy', 'A drive for 50 lakh new piped gas connections')
st('msp', 'MSP for Rabi crops', 'Farm prices', 'Safflower gets the biggest MSP rise', 'feature',
   lede='The government raised the minimum support prices for all six winter (Rabi) crops for the 2027-28 marketing season. Safflower got the biggest rise, ₹675 a quintal, and wheat the smallest, ₹25, taking wheat to ₹2,610. But wheat has the highest margin over cost, 106%.',
   nums=[('₹2,610', 'Wheat, per quintal'), ('₹675', 'Safflower rise, highest'), ('106%', 'Wheat margin over cost'), ('₹90,962 cr', 'Procurement payout')], chart=['msp'],
   trap='MSP is at least 1.5 times the all-India weighted average cost of production (Budget 2018-19).')
st('nsap', 'National Social Assistance Programme (NSAP) continued', 'Welfare', 'Social pensions renewed, renamed, and open to more disabled people')
st('works', 'MoRD notifies 375 permissible works', 'Rural jobs', 'Villages can now choose from 375 kinds of work', 'feature',
   lede='Under the VB–G RAM G Act, 2025, the rural jobs law, the Rural Development Ministry raised the list of permissible works from 266 to 375. Water security has the most, 128, followed by core rural infrastructure, livelihood infrastructure and disaster preparedness.',
   nums=[('266 → 375', 'Permissible works'), ('+109', 'Added'), ('128', 'Water security'), ('181', 'Farm-related')], chart=['works'])
st('farmerid', '11 crore Farmer IDs', 'Agriculture', '11 crore Farmer IDs, five months early')
st('fastagx', 'Exempted FASTag guidelines', 'Roads', 'Free FASTags for vehicles of people with disabilities')
st('ports', 'Ports and waterways', 'Ports', 'First cargo by river from Assam to Dhaka in about 80 years',
   lede='Methanol from Assam Petro-Chemicals became the first international cargo on the Brahmaputra route, from Bogibeel terminal in Dibrugarh to Pangaon Port near Dhaka, reviving it after about 80 years. In Mumbai, the Jawahar Dweep Marine Oil Terminal was declared plastic-free on 2 October.')
st('greenship', 'India–EU green shipping corridor', 'Shipping', 'India and the EU launch a green shipping coalition')
st('annual', 'FASTag Annual Pass crosses 1 crore', 'Roads', 'One crore FASTag annual passes sold')
st('plb', '78 days\' Productivity Linked Bonus', 'Railways', '78 days\' bonus for railway staff')
st('bs7', 'Draft Bharat Stage VII (BS-VII)', 'Pollution', 'BS-VII norms from 2029, with limits on brake and tyre dust')
st('parivartan', 'PARIVARTAN: old truck and bus', 'Pollution', 'Delhi-NCR pays owners to scrap old trucks and buses')
st('gobar', 'GOBARdhan: ₹23,731 crore', 'Biogas', '₹23,731 crore to raise biogas output tenfold', 'feature',
   lede='The Petroleum Ministry has set up a ten-year, ₹23,731 crore scheme to raise compressed biogas (CBG) output nearly tenfold. City gas companies must blend a rising share of CBG, plant owners get a fixed price and capital support, and loans get a credit guarantee.',
   nums=[('₹23,731 cr', 'Outlay'), ('10 years', 'FY27 to FY36'), ('₹2,110', 'Price per MMBtu'), ('217+', 'Plants, Aug 2026')], chart=['cbg'])
st('cheetah', 'Project Cheetah: five cubs', 'Wildlife', 'An India-born cheetah has five cubs at Kuno')
st('ramsar', "India's Ramsar sites reach 103", 'Wetlands', 'Sukhna Lake and Sauj Jheel take India to 103 Ramsar sites')
st('unesco', 'UNESCO Tentative List', 'Heritage', 'Three sites added to India\'s UNESCO waiting list')
st('wash', 'WHO–UNICEF JMP report on school WASH', 'Schools', '50 million Indian schoolchildren have no toilet at school')
st('delhi', '★ Delhi', 'Delhi', 'Delhi: newborn screening, higher ASHA pay, no protests at Jantar Mantar',
   lede='Delhi\'s ANMOL programme screens newborns for 63 disorders, and the monthly incentive for ASHA workers doubled from ₹3,000 to ₹6,000. Jantar Mantar is no longer a protest site; Ramlila Ground, Burari Ground and CBD Ground are designated instead.')
st('lao', 'Ladakh, Odisha, Assam', 'States', 'A snow leopard safari, a MICE portal and all four Assam tiger reserves certified',
   lede='Ladakh launched India\'s first high-altitude snow leopard safari, Odisha opened India\'s first incentive portal for meetings, conferences and exhibitions, and Assam\'s Nameri Tiger Reserve got CA|TS approval, so all four tiger reserves in Assam are now approved.')
st('organic', 'Ladakh becomes India\'s first fully organic', 'Ladakh', 'Ladakh is India\'s first fully organic Union Territory')
st('fnta', 'Frontier Nagaland Territorial Authority', 'Nagaland', 'Eastern Nagaland gets its own territorial authority')
st('lahdc', 'Ladakh: 100 seats', 'Ladakh', 'Ladakh redraws its Hill Councils: 100 seats, 8 councils')

# ---------- 5 ----------
st('hlcb', 'High Level Committee on Banking for Viksit Bharat', 'Committee', 'A committee to plan banking for 2047')

# ---------- 6 ----------
st('cart', 'NexCAR19', 'Medicine', 'India\'s own CAR-T therapy for blood cancers')
st('nsm', 'National Supercomputing Mission', 'Computing', '40 supercomputers and counting')
st('nqm', 'National Quantum Mission', 'Quantum', 'A 1,000 km quantum-secure link in three years')
st('cervavac', 'CERVAVAC', 'Vaccines', 'India\'s HPV vaccine gets WHO prequalification')
st('gslv', 'GSLV-F18 launches NVS-03', 'Space', 'GSLV-F18 puts NavIC satellite NVS-03 in orbit')
st('exer', 'Exercises', 'Exercises', 'A month of exercises with the UAE, ASEAN, the UK, Russia and Australia')
st('dad', 'Defence Accounts Department', 'Defence finance', 'New IT systems for defence accounts and pay')
st('navy', 'Navy and Coast Guard', 'Navy', 'A fleet support ship, an anti-submarine craft and a patrol vessel')
st('contracts', 'Contracts and trials', 'Defence deals', 'BrahMos launchers, a stratospheric platform and new radars')
st('rice', "'Bharat Rice' for the Army", 'Army', 'Bharat Rice reaches the Army\'s forward posts')
st('samarthak', 'INS/MPV Samarthak', 'Navy', 'INS Samarthak, first of four multi-purpose vessels')
st('gsat', 'MoD contracts: GSAT-7C and Varunastra', 'Defence deals', 'Over ₹4,000 crore for a satellite and heavy torpedoes')
st('defexp', 'Defence exports and production (FY 2025-26)', 'Defence industry', 'Record defence exports of ₹38,424 crore',
   lede='India\'s defence exports reached a record ₹38,424 crore in 2025-26, up 62.66%, to more than 80 countries. Domestic defence production also hit a record, ₹1.78 lakh crore. Defence public sector units made 54.84% of the exports and private companies 45.16%.')
st('asiang', '20th Asian Games, Aichi-Nagoya', 'Asian Games', 'India fourth at the Asian Games with 85 medals', 'feature',
   lede='India finished fourth at the 20th Asian Games in Aichi-Nagoya, Japan, with 85 medals: 21 gold, 27 silver and 37 bronze. The men\'s and women\'s cricket teams kept their titles, both kabaddi teams won, and the women\'s hockey team won gold for the first time since 1982.',
   nums=[('4th', 'India'), ('85', 'Medals'), ('21', 'Gold'), ('1982', 'Last women\'s hockey gold before')], chart=['asg'],
   trap='The men\'s hockey gold was India\'s 5th: 1966, 1998, 2014, 2022 and 2026.')
st('harman', 'Harmanpreet Kaur quits', 'Cricket', 'Harmanpreet Kaur steps down; Smriti Mandhana takes over')
st('chess', '46th Chess Olympiad', 'Chess', 'India keeps the top combined chess trophy for a third time')
st('para', '5th Asian Para Games 2026', 'Para sport', 'Sheetal Devi wins two golds at the Asian Para Games',
   lede='At the 5th Asian Para Games in Aichi-Nagoya, archer Sheetal Devi won gold in the women\'s individual compound and the compound mixed team. Mona Agarwal won the women\'s 10 m air rifle standing SH1 with a Games record of 250.0.')

# ---------- 7 ----------
st('nobel', '★ Winners', 'Nobel Prizes', 'Who won the 2026 Nobel Prizes',
   lede='The 2026 Nobel Prizes went to work on optogenetics in medicine, neutrinos from space in physics and asymmetric organic synthesis in chemistry. The Peace Prize went to South African jurist Navi Pillay for her work on accountability for war crimes and genocide.')
st('indaw', 'Indian winners', 'Awards', 'Mahesh Kakde wins the Ramanujan Prize',
   lede='Mahesh Kakde of IISc Bengaluru won the 2026 Ramanujan Prize for young mathematicians from developing countries. The Indian Olympic Association gave its first Jaspal Rana Award to archer Kumkum Anil Mohod and its first Raja Randhir Singh Award to Sujeet Kalkal.')
st('mpi', 'Global Multidimensional Poverty Index', 'Poverty', 'India cuts poverty sharply while world poverty rises', 'feature',
   lede='The UN\'s multidimensional poverty index looks at health, education and living standards, not just income. Across 108 countries, 1.2 billion people are poor by this measure, and the number rose for the first time since 2010. India\'s share of poor people fell from 55.1% to 16.4% over 14.5 years.',
   nums=[('0.283 → 0.069', 'India\'s MPI'), ('55.1% → 16.4%', 'Share of poor'), ('1.2 bn', 'Poor worldwide'), ('108', 'Countries')], chart=['mpi'],
   trap='The MPI runs from 0 to 1, and a higher figure means poorer.')
st('wbpov', 'World Bank Poverty and Equity Brief', 'Poverty', 'Extreme poverty in India falls to 2.6%', 'feature',
   lede='The World Bank says the share of Indians below the $4.20-a-day line fell from 57.7% in 2011 to 16.1% in 2023, lifting 496 million people out. Extreme poverty, below $3 a day, fell to 2.6%. Poverty is higher in villages, 19.3%, than in towns, 8.6%.',
   nums=[('16.1%', 'Below $4.20 a day, 2023'), ('2.6%', 'Below $3 a day, 2023'), ('496 mn', 'Lifted out'), ('19.3 / 8.6%', 'Rural / urban')], chart=['wbp'])
st('ghi', 'Global Hunger Index (GHI) 2026', 'Hunger', 'India 100th of 122 on hunger, still "serious"', 'feature',
   lede='The Global Hunger Index ranks India 100th of 122 countries, with a score of 24.1, in the "serious" band where it has been since 2012. Child wasting in India, 19.0%, is the highest in South Asia. Pakistan is 106th and Sri Lanka 53rd.',
   nums=[('100th', 'Of 122'), ('24.1', 'Score'), ('19.0%', 'Child wasting'), ('29.3%', 'Child stunting')], chart=['ghi'],
   trap='The serious band is 20 to 34.9; a lower score is better.')
st('egap', 'UNEP Emissions Gap Report 2026', 'Climate', 'UNEP: holding warming to 1.5°C is no longer possible')
