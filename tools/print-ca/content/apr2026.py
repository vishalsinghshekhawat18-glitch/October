# April 2026 print edition: the authored story layer for tools/print-ca/build.py.
# Facts only from the April notes; every number written here is checked against them.
NOTES = '../../../archive/current-affairs/CA_April_2026.html'
MONTH = 'April 2026'
PERIOD = '1–30 April'
OUTFILE = 'CA_April_2026_print'

COVER = dict(kicker='Section 2', title='A new year starts, and the RBI holds at 5.25%', lead='mpc',
             dek='The Income Tax Act 2025 takes effect on 1 April, the IMF moves India down to sixth in dollar GDP, and UPI turns 10. The RBI keeps its repo rate unchanged and shares its forecasts: what happened, and the numbers to keep.',
             stats=[('5.25%', 'Repo rate, unchanged'), ('3.4%', 'CPI inflation, March'), ('$860.09 bn', 'Exports, FY26'), ('6th', 'India, IMF dollar-GDP list')])
COVER_LINES = [('Section 1 · Tax', 'The Income Tax Act 2025 comes into force on 1 April', 'ita'),
               ('Section 1 · Trade', 'The New Zealand FTA gives duty-free access to all Indian exports', 'nz'),
               ('Section 3 · World', 'The UAE leaves OPEC and OPEC+ from 1 May', 'opec'),
               ('Section 4 · Politics', 'A Bill would take the Lok Sabha up to 850 seats', 'ls850')]
LEADS = {1: 'Income Tax Act 2025 · growth forecasts · CPI 3.4% · exports $860.09 bn · NZ FTA · UPI at 10',
         2: 'Repo 5.25% · ECL norms · Basel III · digital-fraud hold · Paytm Payments Bank · SEBI platforms',
         3: 'IFC $10 bn · UAE leaves OPEC · CMS COP15 · Maldives swap · Mauritius $680 mn',
         4: 'Lok Sabha 850 seats · SHANTI Act · Census 2027 · non-fossil 283.46 GW · PAI 2.0 · Ladakh',
         5: 'Emirates NBD and RBL Bank · WTO MC14 · appointments · Mythos panel',
         6: 'Artemis II · fast breeder reactor · Vikram-1 · Taragiri · Asian wrestling and boxing',
         7: 'Goldman Prize · press freedom 157th · SIPRI · IRENA · Knight Frank',
         8: 'SMILE · Poshan 2.0 · e-NAM · Urban Challenge Fund · PMGSY-III',
         9: 'Key numbers · upcoming dates · flashcards'}
DASH = '''<table class="score dash"><thead><tr><th>Indicator</th><th>Before</th><th>Now</th><th>Trend</th></tr></thead><tbody>
<tr><td>Repo rate</td><td>5.25%</td><td>5.25%<small> unchanged</small></td><td>■ steady</td></tr>
<tr><td>CPI (retail) inflation</td><td>3.21% Feb</td><td>3.4% Mar</td><td>▲ rising, new base 2024</td></tr>
<tr><td>Manufacturing PMI</td><td>56.9 Feb</td><td>53.9 Mar</td><td>▼ slower, above 50</td></tr>
<tr><td>Industrial production (IIP)</td><td>5.2% Feb</td><td>4.1% Mar</td><td>▼ slower</td></tr>
<tr><td>Forex reserves</td><td>$688.05 bn Mar</td><td>$703 bn+ 17 Apr</td><td>▲ recovering</td></tr>
<tr><td>Exports, goods and services</td><td>$825.26 bn FY25</td><td>$860.09 bn FY26</td><td>▲ record</td></tr>
</tbody></table>'''

def make_charts(hbar, steps, table_chart):
    return {
     'fcst': table_chart('India’s growth, as six forecasters see it', ['Forecaster', 'First year', 'Next year'],
                         [['World Bank', '7.6% (FY26)', '6.6% (FY27)'], ['ADB', '6.9% (2026)', '7.3% (2027)'], ['UN ESCAP', '6.4% (2026)', '6.6% (2027)'],
                          ['IMF', '6.5% (FY27)', '6.5% (FY28)'], ['Moody’s', '6.0% (FY27)', '–'], ['RBI (MPC)', '6.9% (FY27)', '–']], big_cols=(1, 2)),
     'imf': hbar('The 2026 dollar-GDP list ($ tn)', [('United States', 32.38, '32.38'), ('China', 20.85, '20.85'), ('Germany', 5.45, '5.45'), ('Japan', 4.38, '4.38'), ('United Kingdom', 4.26, '4.26'), ('India', 4.15, '4.15')], 32.38, hi=5),
     'wpiw': hbar('Weights in the wholesale price index (%)', [('Manufactured products', 64.23, '64.23'), ('Primary articles', 22.62, '22.62'), ('Fuel and power', 13.15, '13.15')], 64.23, hi=0),
     'iciw': hbar('Weights of the eight core industries (%)', [('Refinery products', 28.04, '28.04'), ('Electricity', 19.85, '19.85'), ('Steel', 17.92, '17.92'), ('Coal', 10.33, '10.33'), ('Crude oil', 8.98, '8.98'), ('Natural gas', 6.88, '6.88'), ('Cement', 5.37, '5.37'), ('Fertilisers', 2.63, '2.63')], 28.04, hi=0),
     'fdis': hbar('Top sources of FDI equity, April–December FY26 (share, %)', [('Singapore', 37, '37'), ('United States', 16, '16'), ('Mauritius', 10, '10')], 37, hi=0),
     'fdist': hbar('Top states for FDI equity ($ bn)', [('Maharashtra', 15.38, '15.38'), ('Karnataka', 11.15, '11.15')], 15.38, hi=0),
     'exp': table_chart('Exports and trade balance, FY25 and FY26', ['', 'FY2024-25', 'FY2025-26'],
                        [['Exports, goods and services', '$825.26 bn', '$860.09 bn'], ['Merchandise trade deficit', '$283.50 bn', '$333.19 bn'], ['Services surplus', '$188.84 bn', '$213.89 bn']], big_cols=(1, 2)),
     'nzv': table_chart('The mobility window for Indians', ['Visa', 'Quota', 'Stay'],
                        [['Temporary Employment Entry', '5,000', 'Up to 3 years'], ['Working Holiday', '1,000 a year', '12 months']], big_cols=(1,)),
     'fof': table_chart('Fund of Funds, the first and the second', ['', 'FoF 1.0', 'FoF 2.0'],
                        [['Money', '₹7,000 cr to 135+ AIFs', '₹10,000 cr corpus'], ['Result or route', '₹26,900 cr invested in 1,420+ startups', 'SEBI-registered Category I and II AIFs only']], big_cols=()),
     'ssr': hbar('Small savings rates, April–June 2026 (%)', [('Sukanya Samriddhi', 8.2, '8.2'), ('National Savings Certificate', 7.7, '7.7'), ('Kisan Vikas Patra', 7.5, '7.5'), ('Monthly Income Scheme', 7.4, '7.4'), ('PPF', 7.1, '7.1'), ('3-year term deposit', 7.1, '7.1'), ('Post office savings account', 4, '4.0')], 8.2, hi=0),
     'upi': table_chart('UPI, ten years apart', ['', 'FY17', 'FY26'],
                        [['Transactions', '2 crore', '24,162 crore'], ['Value', '₹0.07 lakh cr', 'About ₹314 lakh cr'], ['Banks live', '44', '703']], big_cols=(1, 2)),
     'mudra': table_chart('The four MUDRA loan sizes', ['Category', 'Loan size'],
                          [['Shishu', 'Up to ₹50,000'], ['Kishor', '₹50,000 – ₹5 lakh'], ['Tarun', '₹5 – ₹10 lakh'], ['Tarun Plus (2024)', '₹10 – ₹20 lakh']], big_cols=(1,)),
     'insl': table_chart('The 2025 insurance law, before and after', ['Rule', 'Before', 'After'],
                         [['Foreign investment', '74%', '100%'], ['IRDAI approval for a share transfer', '1%', '5%'], ['Net owned fund, foreign reinsurer', '₹5,000 cr', '₹1,000 cr'], ['Maximum penalty', '₹1 cr', '₹10 cr']], big_cols=(1, 2)),
     'corr': steps('The RBI rate corridor, top to bottom', [('5.50%', 'MSF and Bank Rate'), ('5.25%', 'Repo (LAF)'), ('5.00%', 'SDF')], on_last=False),
     'proj': table_chart('RBI projections for FY27, by quarter (%)', ['', 'Q1', 'Q2', 'Q3', 'Q4'],
                         [['GDP growth', '6.8', '6.7', '7.0', '7.2'], ['CPI inflation', '4.0', '4.4', '5.2', '4.7']], big_cols=(1, 2, 3, 4)),
     'fpil': hbar('Total debt limit for foreign investors (₹ crore)', [('Current', 1470655, '14,70,655'), ('April–September 2026', 1551646, '15,51,646'), ('October 2026–March 2027', 1632640, '16,32,640')], 1632640, hi=2),
     'ecl': table_chart('The three stages of expected credit loss', ['Stage', 'Meaning', 'Provision'],
                        [['Stage 1', 'Normal loans', '0.4% minimum (12-month loss)'], ['Stage 2', 'Risky loans, for example 60–90 days overdue', '5% minimum'], ['Stage 3', 'NPAs', 'Full lifetime loss']], big_cols=(2,)),
     'cens': steps('The census in two phases', [('Apr–Sep 2026', 'Phase I: houselisting and housing census'), ('Feb 2027', 'Phase II: population count, with castes'), ('1 Mar 2027', 'Reference date')]),
     'nfc': hbar('Non-fossil capacity by source, 31 March 2026 (GW)', [('Solar', 150.26, '150.26'), ('Wind', 56.09, '56.09'), ('Large hydro', 51.41, '51.41'), ('Bio', 11.75, '11.75'), ('Nuclear', 8.78, '8.78'), ('Small hydro', 5.17, '5.17')], 150.26, hi=0),
     'tat': hbar('Turnaround time at major ports (hours)', [('2014', 96, '96'), ('2025', 49.5, '49.5')], 96, hi=1),
     'nso': table_chart('Health care in households, before and now', ['', 'Before', 'Now'],
                        [['Health scheme or insurance cover, rural', '12.9%', '45.5%'], ['Health scheme or insurance cover, urban', '8.9%', '31.8%'], ['Institutional deliveries, rural', '90.5%', '95.6%'], ['Institutional deliveries, urban', '96.1%', '97.8%']], big_cols=(1, 2)),
     'pai': hbar('Gram panchayats by grade', [('Achiever A+ (90 and above)', 0, 'none'), ('Front Runner A (75 to under 90)', 3635, '3,635'), ('Performer B (60 to under 75)', 118824, '1,18,824')], 118824, hi=2),
     'wcr': hbar('Women’s credit (₹ lakh crore)', [('2017', 16, '16'), ('2025', 76, '76')], 76, hi=1),
    }

SEC_INTRO = {
 1: 'The new financial year brings a new income tax law, and the month’s data show growth, prices and trade. The IMF moves India down to sixth in dollar GDP, UPI turns 10, and insurers move to a new accounting standard.',
 2: 'The RBI keeps the repo rate at 5.25% and sets final rules on expected credit loss and Basel III. It also proposes a pause on big online transfers, cancels a payments bank licence and issues new note and coin rules. SEBI and PFRDA change their rules too.',
 3: 'The IFC plans to lift its investment in India, the UAE leaves OPEC, and countries meet to protect migratory species. India extends a currency swap to the Maldives, signs a $680 million package with Mauritius and widens OCI for people of Indian origin in Sri Lanka.',
 4: 'A Bill to enlarge the Lok Sabha, a nuclear energy law, the first digital census and a record year for clean power. Rajasthan gets a $225 million World Bank loan for highways, and Ladakh gets five new districts.',
 5: 'Deals, a WTO ministerial, summits and appointments: Emirates NBD takes control of RBL Bank, and the finance minister sets up a panel on risks from an AI platform.',
 6: 'Artemis II flies round the Moon, India’s fast breeder reactor reaches criticality and a Gujarat zone is set for India’s first chip plant. The Navy adds ships, and Vaishali wins the Women’s Candidates.',
 7: 'Prizes for a forest guard, scientists and cricketers, and the rankings and reports that measure India: press freedom, billionaires, military spending and renewable energy.',
 8: 'Seven schemes side by side, from help for transgender persons to nutrition, farm markets, city finance, village roads, food processing and insurance.',
}

CHAPTERS = {
 1: [('1.1', 'A new financial year begins', 'A new income tax law and the month’s tax collection.', ['ita', 'gst']),
     ('1.2', 'Forecasts and the world ranking', 'Six forecasters put a number on India’s growth, and the IMF moves India down the dollar-GDP list.', ['fcst', 'imf']),
     ('1.3', 'Prices, output and the national accounts', 'Inflation, the core industries, factory output and the PMI for March, and a new base year.', ['inf', 'ici', 'iip', 'pmi', 'base']),
     ('1.4', 'Making things and selling them', 'Hubs and an export target, a record export year and the schemes that back exporters.', ['mfg', 'exp', 'china', 'relief', 'rodtep', 'pli', 'textile', 'gem']),
     ('1.5', 'Investment, startups and trade deals', 'Where the foreign money came from, a record year for startups and a deal with New Zealand.', ['fdi', 'startup', 'nz']),
     ('1.6', 'Work, women and savings', 'Provident fund withdrawals, women’s credit and the rates on small savings.', ['epfo', 'women', 'ssr']),
     ('1.7', 'Banks and payments', 'UPI at ten, a new number two bank, gold imports and the MUDRA loans.', ['upi', 'sbi', 'gold', 'mudra']),
     ('1.8', 'Insurance', 'A new accounting standard, cyber-security rules, premium and the shape of the whole sector.', ['indas', 'dsii', 'cyber', 'nonlife', 'ins'])],
 2: [('2.1', 'The RBI’s policy and numbers', 'The repo rate, limits for foreign investors, state borrowing, cash and reserves.', ['mpc', 'fpi', 'sdl', 'cic', 'forex']),
     ('2.2', 'Rules for banks and borrowers', 'Final rules on expected credit loss and credit risk, and new rules on capital, defaulters and lenders.', ['ecl', 'basel', 'capcard', 'wilful', 'type1', 'nbfcul', 'ucb']),
     ('2.3', 'Payments, fraud and currency', 'A draft pause on big transfers, faster inward credit, prepaid wallets, note rules, export credit and a cancelled licence.', ['hold', 'inward', 'ppi', 'notes', 'fxrules', 'fema', 'paytm']),
     ('2.4', 'SEBI', 'Buybacks, new platforms, the Social Stock Exchange and public shareholding.', ['buyback', 'supcoms', 'sse', 'mps']),
     ('2.5', 'Pension regulator', 'NPS charges and a pension scheme with health cover.', ['nps', 'swasthya'])],
 3: [('3.1', 'Banks, groups and oil', 'The IFC, the OPEC exit, food prices and a conference on migratory species.', ['ifc', 'opec', 'fao', 'cms']),
     ('3.2', 'India and its partners', 'A currency swap, an aid package, new members for two groupings and a trade portal.', ['maldives', 'mauritius', 'korea', 'usgermany'])],
 4: [('4.1', 'Laws, the Constitution and the Census', 'A bigger Lok Sabha, a nuclear law, anti-defection, court rulings, the census and a bill on small offences.', ['ls850', 'shanti', 'tenth', 'decisions', 'janvishwas', 'gaming', 'census', 'welfare']),
     ('4.2', 'Farms, fish and fertiliser', 'Pulses, seafood, fisheries and the fertiliser subsidy.', ['pulses', 'seafood', 'aif', 'fisheries', 'nbs']),
     ('4.3', 'Energy, roads and ports', 'Dams and a refinery, coal gas, an expressway, ports, solar, wind and non-fossil power.', ['ccea', 'coalgas', 'westasia', 'expressway', 'ports', 'sagarmala', 'iwai', 'solar', 'wind', 'nonfossil']),
     ('4.4', 'Nature and the environment', 'A new Ramsar site and a decade of conservation numbers.', ['shekha', 'green']),
     ('4.5', 'Panchayats, surveys and statistics', 'Panchayati Raj Day, a health survey, a panchayat index, a gender report and patent filings.', ['panchayat', 'pai', 'nso', 'wmi', 'patents']),
     ('4.6', 'States and territories', 'A World Bank loan, new districts and a first for Odisha.', ['rajhighway', 'ladakh', 'odisha'])],
 5: [('5.1', 'Deals and meetings', 'MoUs, a bank takeover, the WTO ministerial and summits.', ['mous', 'mna', 'wto', 'summits']),
     ('5.2', 'People and panels', 'New office-holders and a panel on AI risks.', ['appts', 'mythos'])],
 6: [('6.1', 'Science and technology', 'A quantum link, a Moon flight, a reactor, a private rocket and a chip plant.', ['nqm', 'artemis', 'skyroot', 'chip']),
     ('6.2', 'Defence', 'A logistics pact with Russia and new Navy ships.', ['relos', 'navy']),
     ('6.3', 'Sports', 'A doping warning, chess and athletics milestones and the month’s tournaments.', ['aiu', 'chess', 'tourn'])],
 7: [('7.1', 'Awards and prizes', 'April’s awards and two global prizes.', ['awards', 'prizes']),
     ('7.2', 'Rankings and reports', 'Where India stands on a dozen lists and in four reports.', ['rank', 'reports'])],
 8: [('8.1', 'Schemes of the month', 'Seven schemes side by side.', ['smile', 'poshan', 'enam', 'ucf', 'pmgsy', 'plisfpi', 'insschemes'])],
}

S = {}
def st(key, card, tag, h, size='short', **kw): S[key] = dict(card=card, tag=tag, h=h, size=size, **kw)

# ---------- 1 ----------
st('ita', 'Income Tax Act 2025 in force', 'Tax', 'The Income Tax Act 2025 comes into force on 1 April; Form 130 replaces Form 16')
st('gst', 'Gross GST, March 2026', 'GST', 'Gross GST: over ₹2 lakh crore in March, ₹22 lakh crore in the year')
st('fcst', 'India growth forecasts: World Bank', 'Forecasts', 'Six forecasters, six numbers for India’s growth', 'feature',
   lede='Six forecasters gave India’s growth a number in April, and they did not agree. The World Bank put FY26 at 7.6%, up 1.1 points from October 2025, and FY27 at 6.6%. The ADB said 6.9% for 2026 and 7.3% for 2027, while cutting its forecast for Asia to 4.7% for 2026 from 5.1%. UN ESCAP said 6.4% and 6.6%. The IMF has 6.5% for both FY27 and FY28, up from 6.4%, and Moody’s cut FY27 to 6.0% from 6.8% because of the West Asia conflict. The RBI’s own figure for FY27 is 6.9%.',
   nums=[('7.6%', 'World Bank, FY26'), ('6.9%', 'ADB, 2026'), ('6.5%', 'IMF, FY27'), ('6.0%', 'Moody’s, FY27, cut from 6.8%')], chart=['fcst'])
st('imf', 'IMF April 2026 World Economic Outlook', 'Rankings', 'The IMF moves India from 4th to 6th in dollar GDP', 'feature',
   lede='The IMF’s April World Economic Outlook moved India from 4th to 6th place among the world’s economies by nominal GDP, which converts local-currency output into US dollars at current exchange rates. India’s 2026 GDP is $4.15 tn, behind the US ($32.38 tn), China ($20.85 tn), Germany ($5.45 tn), Japan ($4.38 tn) and the UK ($4.26 tn). The IMF expects India to pass Japan by 2028 ($5.06 tn against $4.74 tn) and to move decisively to 3rd by 2031 ($6.79 tn against Japan’s $5.13 tn).',
   nums=[('6th', 'India’s place, 2026'), ('$4.15 tn', 'India’s GDP, 2026'), ('2028', 'India passes Japan'), ('2031', 'India moves to 3rd')], chart=['imf'])
st('inf', 'Inflation, March 2026', 'Inflation', 'Retail inflation is 3.4% on a new base year; wholesale inflation is 3.88%', 'feature',
   lede='Retail inflation was 3.4% in March 2026, up from 3.21% in February, and it was the first reading on a new base year, 2024. The basket grew from 299 to 358 items (goods 259 to 308, services 40 to 50) in 12 divisions; the 2024 series shows rural inflation at 3.63% and urban at 3.11%. Wholesale inflation was 3.88% year on year, the fastest in over three years, pushed by oil, food and manufactured goods; the WPI base year is still 2011-12.',
   nums=[('3.4%', 'CPI, March'), ('3.88%', 'WPI, March'), ('358', 'Items in the new basket'), ('2024', 'New CPI base year')], chart=['wpiw'],
   trap='DPIIT releases the WPI on the 14th of each month; the food index has a weight of 24.38%.')
st('ici', 'Index of Eight Core Industries, March 2026', 'Core industries', 'Core industries shrink 0.4% in March', 'feature',
   lede='The Index of Eight Core Industries fell 0.4% year on year in March 2026 (provisional); for April–March 2025-26 it grew 2.6%. The eight industries make up 40.27% of the Index of Industrial Production, on the base 2011-12. March fell in fertilisers, crude oil, coal and electricity. Refinery products carry the biggest weight, 28.04, followed by electricity at 19.85 and steel at 17.92.',
   nums=[('−0.4%', 'March, year on year'), ('2.6%', 'April–March 2025-26'), ('40.27%', 'Share of the IIP'), ('8', 'Core industries')], chart=['iciw'],
   trap='The index is compiled by the Office of the Economic Adviser (DPIIT/Commerce); fertilisers carry the smallest weight, 2.63.')
st('iip', 'IIP, female workforce and DPI roadmap', 'Output', 'Factory output grows 4.1% in March; NITI Aayog maps DPI to 2047')
st('pmi', 'PMI and exports', 'PMI', 'Manufacturing PMI is 53.9 in March; exports hit a record $860 bn')
st('base', 'Base year 2022-23: GSVA and DDP guidelines', 'National accounts', 'The national accounts move to base year 2022-23')
st('mfg', 'Manufacturing hubs and export target', 'Industry', 'Manufacturing hubs and a $2 tn export target for 2030-31')
st('exp', 'Exports and trade balance, FY2025-26', 'Trade', 'Exports reach $860.09 billion in FY26', 'feature',
   lede='India’s merchandise and services exports together were $860.09 bn in FY2025-26, against $825.26 bn the year before, a rise of 4.22%. The merchandise trade deficit widened to $333.19 bn from $283.50 bn, while the services surplus grew to $213.89 bn from $188.84 bn. Fastest export growth was to China (36.66%), then Spain, Hong Kong, Vietnam and Sri Lanka.',
   nums=[('$860.09 bn', 'Exports, FY26'), ('4.22%', 'Growth'), ('$333.19 bn', 'Merchandise deficit'), ('$213.89 bn', 'Services surplus')], chart=['exp'],
   trap='Import growth was led by China, the USA, Hong Kong, Peru and the UK.')
st('china', 'China becomes India', 'Trade', 'China becomes India’s top trading partner')
st('relief', 'RELIEF scheme for exporters', 'Exports', 'RELIEF: help for exporters hit by the West Asia disruption')
st('rodtep', 'RoDTEP, RoSCTL and SEZ-to-DTA relief', 'Exports', 'RoDTEP, RoSCTL and SEZ-to-DTA relief are extended')
st('pli', 'PLI for large-scale electronics', 'Industry', 'PLI makes India the second-largest mobile maker')
st('textile', 'Textile exports FY2025-26', 'Textiles', 'Textile exports rise 2.1% to ₹3,16,334.9 crore')
st('gem', 'GeM crosses', 'Procurement', 'GeM sales cross ₹18.4 lakh crore')
st('fdi', 'FDI equity inflows, April-December', 'FDI', 'Singapore tops FDI equity inflows with $17.6 billion', 'feature',
   lede='Foreign direct investment is money from abroad put into Indian businesses. DPIIT data for April to December of FY26 show Singapore as the biggest source, with $17.6 bn, or 37%; the US followed with 16% and Mauritius with 10%. FDI from the Cayman Islands rose five times, from $422 mn to $2 bn. Among states, Maharashtra received $15.38 bn and Karnataka $11.15 bn.',
   nums=[('$17.6 bn', 'From Singapore'), ('37%', 'Singapore’s share'), ('$2 bn', 'From Cayman Islands, up from $422 mn'), ('$15.38 bn', 'Into Maharashtra')], chart=['fdis', 'fdist'],
   trap='The figures cover April to December of FY26 and come from DPIIT, the Department for Promotion of Industry and Internal Trade.')
st('startup', 'Startup India: record recognitions', 'Startups', 'More than 55,200 startups recognised in FY26; Fund of Funds 2.0 gets ₹10,000 crore', 'feature',
   lede='More than 55,200 startups were recognised in FY26, the highest ever and up 51.6%; by 31 March 2026 the total was 2.23 lakh, with 23.36 lakh direct jobs, and 48% have a woman director or partner. Startup India began on 16 January 2016, and Maharashtra, Karnataka, UP, Delhi and Gujarat lead. Fund of Funds 2.0 has a corpus of ₹10,000 cr for SEBI-registered AIFs across the 16th and 17th Finance Commission cycles, with SIDBI as the implementing agency. The credit guarantee cover per borrower rises from ₹10 cr to ₹20 cr.',
   nums=[('55,200+', 'Recognised in FY26'), ('2.23 lakh', 'Total by 31 March 2026'), ('23.36 lakh', 'Direct jobs'), ('₹10,000 cr', 'Fund of Funds 2.0')], chart=['fof'],
   trap='The government’s money in any one AIF is capped at 50%, and the implementing agency’s cost at 0.50% a year.')
st('nz', 'India-New Zealand Free Trade Agreement', 'Trade deals', 'The India–New Zealand FTA gives duty-free access to all Indian exports', 'feature',
   lede='The India–New Zealand free trade agreement removes duties on 100% of Indian exports from the day it enters into force; the leather and footwear tariff goes from 5% to zero. It has the first FTA chapter on Health and Traditional Medicine (AYUSH). New Zealand commits $20 bn of investment, and India opens 70% of its tariff lines, covering 95% of New Zealand’s trade, against trade of about $1.3 bn. It is India’s 9th trade agreement in recent years.',
   nums=[('100%', 'Indian exports duty-free'), ('$20 bn', 'New Zealand investment'), ('70%', 'India’s tariff lines opened'), ('5% → 0', 'Leather and footwear tariff')], chart=['nzv'],
   trap='Agra makes about 75% of India’s leather footwear (GI tag, One District One Product).')
st('epfo', 'EPFO 3.0 and EPFO updates', 'EPFO', 'EPFO 3.0: UPI withdrawals and up to 75% of the balance')
st('women', 'NITI Aayog: Women and India', 'Women and credit', 'Women’s credit reaches ₹76 lakh crore', 'feature',
   lede='NITI Aayog’s second report on women and India’s credit market, From Borrowers to Builders, was released on 7 April 2026 with TransUnion CIBIL and MicroSave under the Women Entrepreneurship Platform. Women’s credit rose from ₹16 lakh cr in 2017 to ₹76 lakh cr in 2025, 4.8 times, and is now 26% of system credit; penetration rose from 19% to 36%, among about 45 crore credit-eligible women. Business lending grew 7.5 times, lifting its share from 16% to 25%, at 31% a year over 2022–25 against 17% overall.',
   nums=[('₹16 → ₹76 lakh cr', 'Women’s credit, 2017 to 2025'), ('4.8x', 'Growth'), ('26%', 'Of system credit'), ('36%', 'Penetration, from 19%')], chart=['wcr'],
   trap='Microfinance grew slowest, 2.9 times. Top graduation rates: Tamil Nadu 27%, West Bengal 23%.')
st('ssr', 'Small savings rates, April-June 2026', 'Small savings', 'Small savings rates are unchanged for the 8th quarter', 'feature',
   lede='The government left small savings rates unchanged for April–June 2026, the eighth quarter in a row. Sukanya Samriddhi pays the most, 8.2%, then the National Savings Certificate at 7.7%, Kisan Vikas Patra at 7.5% (it matures in 115 months), the Monthly Income Scheme at 7.4%, PPF and the 3-year term deposit at 7.1% each, and a post office savings account at 4.0%.',
   nums=[('8th', 'Quarter unchanged'), ('8.2%', 'Sukanya Samriddhi'), ('7.1%', 'PPF'), ('4.0%', 'Post office savings account')], chart=['ssr'])
st('upi', 'UPI at 10 years', 'Payments', 'UPI turns 10: 24,162 crore payments in FY26', 'feature',
   lede='UPI was launched by NPCI on 11 April 2016, when Raghuram Rajan was RBI Governor, and has now run for ten years. In FY26 it handled 24,162 crore transactions worth about ₹314 lakh cr, with 703 banks live; March 2026 alone set a record of 22.64 bn payments worth ₹29.52 trn. In 2025 UPI counted 228.5 bn transactions, up 33% from 172.2 bn, worth ₹299.74 trn. The IMF puts UPI at about 49% of the world’s real-time payments volume.',
   nums=[('24,162 crore', 'Transactions, FY26'), ('₹314 lakh cr', 'Value, FY26'), ('703', 'Banks live'), ('49%', 'Of world real-time payments, IMF')], chart=['upi'],
   trap='P2M is 63% of volume, but P2P is 71% of value; 86% of P2M payments are below ₹500.')
st('sbi', 'SBI overtakes ICICI Bank', 'Banks', 'SBI overtakes ICICI Bank as the second-largest lender')
st('gold', 'Gold and silver import: 15 banks', 'Banks', 'Fifteen banks may import gold and silver until March 2029')
st('mudra', 'PM MUDRA Yojana: 11 years', 'Credit', 'PM MUDRA at 11: ₹40.07 lakh crore lent', 'feature',
   lede='PM MUDRA Yojana completed 11 years on 8 April 2026. It has made more than 57 crore loans worth ₹40.07 lakh cr (to 27 March 2026), collateral-free up to ₹20 lakh. Loans come in four sizes: Shishu up to ₹50,000, Kishor to ₹5 lakh, Tarun to ₹10 lakh and Tarun Plus, added in 2024, to ₹20 lakh. The top states by disbursal are UP, Bihar and Maharashtra.',
   nums=[('57 crore+', 'Loans'), ('₹40.07 lakh cr', 'Lent'), ('₹20 lakh', 'Collateral-free limit'), ('59.81%', 'Accounts held by women')], chart=['mudra'],
   trap='Women hold 59.81% of the accounts but 37.45% of the amount.')
st('indas', 'Ind AS for insurers', 'IRDAI', 'Insurers move to Ind AS from 1 April 2026')
st('dsii', 'Domestic Systemically Important Insurers', 'IRDAI', 'LIC, GIC Re and New India keep their D-SII status')
st('cyber', 'IRDAI revised cyber-security norms', 'IRDAI', 'IRDAI tightens cyber-security rules')
st('nonlife', 'Non-life insurance premium FY26', 'Insurance', 'Non-life premium rises 9.2% to ₹3,35,918 crore')
st('ins', 'Insurance sector snapshot and reforms', 'Insurance', 'India is the 10th-largest insurance market', 'feature',
   lede='India is the world’s 10th largest insurance market, with a 1.8% share. Penetration is 3.7% (life 2.7%, non-life 1.0%) and density is $97.0. In FY25 there were 41.84 crore policies, premium of ₹11.93 lakh cr, claims of ₹8.36 lakh cr, assets under management of ₹74.44 lakh cr and 74 insurers; health is 41% of non-life premium, ahead of motor. The Sabka Bima, Sabki Raksha (Amendment of Insurance Laws) Act 2025 raised the foreign investment limit from 74% to 100% and made other changes to bring in more insurers.',
   nums=[('10th', 'Largest insurance market'), ('3.7%', 'Penetration'), ('$97.0', 'Density'), ('100%', 'FDI limit, from 74%')], chart=['insl'],
   trap='The health-insurance moratorium was cut from 8 to 5 years (60 months) in 2024; GST on individual life and health policies was removed from 22 September 2025 (it was 18%).')

# ---------- 2 ----------
st('mpc', 'Monetary Policy, 6-8 April 2026', 'RBI · policy', 'The RBI keeps the repo rate at 5.25%', 'feature',
   lede='The 60th meeting of the Monetary Policy Committee, held on 6–8 April 2026 under Governor Sanjay Malhotra, kept the repo rate at 5.25% and the stance neutral. The SDF is 5.00%, and the MSF and the Bank Rate are 5.50%. The RBI projects GDP growth of 6.9% for FY27 (6.8, 6.7, 7.0 and 7.2 by quarter) and CPI inflation of 4.6% (4.0, 4.4, 5.2 and 4.7), with core inflation at 4.4%. The next meeting is on 3–5 June 2026.',
   nums=[('5.25%', 'Repo rate, unchanged'), ('5.00%', 'SDF'), ('6.9%', 'GDP forecast, FY27'), ('4.6%', 'CPI forecast, FY27')], chart=['corr', 'proj'])
st('fpi', 'FPI debt investment limits', 'RBI · FPI', 'Foreign investors’ debt limits for FY27: 6%, 2% and 15%', 'feature',
   lede='From 1 April 2026 foreign portfolio investors may hold up to 6% of government securities, 2% of state government securities and 15% of corporate bonds. The total debt limit rises from ₹14,70,655 cr to ₹15,51,646 cr for April–September 2026 and ₹16,32,640 cr for October 2026–March 2027. The incremental G-Sec limit is split 50:50 between the General and Long-term routes, all specified securities fall under the Fully Accessible Route, and Voluntary Retention Route investments now sit under General Route limits. Credit default swaps sold by FPIs are capped at 5% of outstanding corporate bonds, with an extra limit of ₹3,30,464 cr for 2026-27.',
   nums=[('6%', 'G-Secs'), ('2%', 'State government securities'), ('15%', 'Corporate bonds'), ('₹16,32,640 cr', 'Limit, Oct 2026–Mar 2027')], chart=['fpil'],
   trap='The limits are issued under FEMA 1999, Sections 10(4) and 11(1).')
st('sdl', 'State market borrowing', 'RBI · states', 'States plan to borrow ₹2,54,509 crore in April–June',
   lede='State governments and UTs plan to borrow ₹2,54,509 crore in the first quarter of FY27. The RBI is also trying a Benchmark Issuance Strategy for nine states: Andhra Pradesh, Bihar, Chhattisgarh, Kerala, Madhya Pradesh, Maharashtra, Rajasthan, Telangana and UP. Their borrowing under it comes to ₹1,53,900 crore.')
st('cic', 'Currency in circulation, FY26', 'RBI · cash', 'Currency in circulation rises 11.9% to ₹41.68 trillion')
st('forex', 'Forex reserves, week ended 17 April', 'RBI · reserves', 'Forex reserves rise $2.3 billion to over $703 billion')
st('ecl', 'Expected Credit Loss (ECL) norms', 'RBI · provisioning', 'Expected credit loss: banks must provide before loans go bad', 'feature',
   lede='The RBI issued final expected credit loss norms, effective 1 April 2027. Banks must provide in advance for likely losses, using the probability of default, loss given default and exposure at default. Stage 1 (normal loans) needs a minimum of 0.4%, Stage 2 (risky loans, for example 60–90 days overdue) a minimum of 5%, and Stage 3 (NPAs) the full lifetime loss. The extra provision from the transition can be spread over 4 years to 31 March 2031, with a CET1 add-back during that period.',
   nums=[('1 Apr 2027', 'Norms take effect'), ('0.4%', 'Stage 1 minimum'), ('5%', 'Stage 2 minimum'), ('31 Mar 2031', 'End of the transition spread')], chart=['ecl'])
st('basel', 'Basel III credit-risk', 'RBI · capital', 'Basel III credit-risk rules: from 1 April 2027')
st('capcard', 'RBI capital, card and classification directions', 'RBI · directions', 'Tier 2 capital, card charges and new asset-classification rules')
st('wilful', 'wilful defaulters and calamity relief', 'RBI · defaulters', 'Banks get 6 months to classify a wilful defaulter')
st('type1', 'Unregistered Type I NBFCs', 'RBI · NBFCs', 'Small Type I NBFCs are exempt from registration')
st('nbfcul', 'NBFC Upper Layer identification', 'RBI · NBFCs', 'RBI proposes ₹1 lakh crore as the Upper Layer cut-off for NBFCs')
st('ucb', 'lending norms for urban co-operative banks', 'RBI · UCBs', 'Urban co-operative banks: unsecured loans capped at 20%')
st('hold', 'delay on high-value digital transfers', 'RBI · fraud', 'RBI proposes a one-hour hold on transfers above ₹10,000')
st('inward', 'Cross-border inward payments', 'RBI · payments', 'Faster credit for money sent from abroad')
st('ppi', 'Master Direction on Prepaid Payment Instruments', 'RBI · wallets', 'Draft rules for prepaid payment instruments')
st('notes', 'RBI note and coin rules', 'RBI · currency', 'New rules on soiled notes, fake notes and currency chests')
st('fxrules', 'Trade relief and FX derivative rules', 'RBI · exporters', 'Export credit is extended to 450 days; an FX derivative circular is withdrawn')
st('fema', 'FEMA (Guarantees) Regulations', 'RBI · FEMA', 'FEMA (Guarantees) Regulations, 2026')
st('paytm', 'Paytm Payments Bank licence', 'RBI · licence', 'RBI cancels Paytm Payments Bank’s licence')
st('buyback', 'SEBI: buyback and IPO norms', 'SEBI', 'SEBI: open-market buybacks may return; IPO approvals get relief')
st('supcoms', 'SEBI: new IT platforms', 'SEBI', 'SEBI launches three new IT platforms')
st('sse', 'Social Stock Exchange relief', 'SEBI', 'Social Stock Exchange relief and new fit-and-proper rules')
st('mps', 'Minimum public shareholding: six bands', 'SEBI · listing', 'Minimum public shareholding gets six size bands')
st('nps', 'PFRDA and NPS rules', 'PFRDA', 'PFRDA trims Tier II charges; NPS retirees get their medical allowance in the bank')
st('swasthya', 'NPS Swasthya Pension Scheme (sandbox)', 'PFRDA', 'NPS Swasthya: a pension and health plan in a sandbox')

# ---------- 3 ----------
st('ifc', 'IFC and World Bank in India', 'IFC', 'The IFC aims to invest $10 billion a year in India by 2030')
st('opec', 'UAE exits OPEC and OPEC+', 'OPEC', 'The UAE leaves OPEC and OPEC+ from 1 May')
st('fao', 'Food prices, energy task force and climate', 'FAO · climate', 'Food prices rise, and India withdraws its bid for COP33')
st('cms', 'CMS COP15', 'Environment', 'CMS COP15 adds 40 species to the protected list')
st('maldives', 'first drawdown for Maldives', 'Maldives', 'India approves ₹30 billion for the Maldives under the SAARC swap')
st('mauritius', 'India-Mauritius $680 million package', 'Mauritius', 'India and Mauritius sign agreements on a $680 million package')
st('korea', 'India-South Korea and Sri Lanka diaspora', 'Partners', 'South Korea to join the ISA and IPOI; OCI reaches the 6th generation in Sri Lanka')
st('usgermany', 'India-US trade portal and India-Germany ties', 'Partners', 'An India–US trade portal and 75 years of India–Germany ties')

# ---------- 4 ----------
st('ls850', 'Constitutional Amendment Bill: Lok Sabha', 'Constitution', 'A Bill would take the Lok Sabha up to 850 seats')
st('shanti', 'SHANTI Act', 'Nuclear', 'The SHANTI Act opens nuclear power to private firms')
st('tenth', 'Tenth Schedule', 'Constitution', 'The Tenth Schedule: a two-thirds merger is needed')
st('decisions', 'Supreme Court, Lok Sabha and state decisions', 'Law',
   'The Supreme Court ties highway safety to the right to life',
   lede='The Supreme Court held that safe passage on highways and commuter safety are part of the right to life under Article 21. The Lok Sabha passed a bill making Amaravati the sole, permanent capital of Andhra Pradesh. Telangana declared cancer a notifiable disease, and Meghalaya made Khasi and Garo official languages besides English. Prashast 2.0, an upgraded platform, identifies 21 types of disabilities in children.')
st('janvishwas', 'Jan Vishwas (Amendment of Provisions) Bill', 'Law', 'The Jan Vishwas Bill 2026 would amend 79 Acts')
st('gaming', 'Online Gaming Rules, 2026', 'Law', 'The Online Gaming Rules take effect on 1 May')
st('census', 'first digital census', 'Census', 'India begins its first digital census', 'feature',
   lede='India has begun its 16th Census, the 8th since Independence and the first fully digital one, with an outlay of ₹11,718.24 cr. Caste is counted, on a Cabinet Committee on Political Affairs decision of 30 April 2025. Phase I, houselisting, runs from April to September 2026, for 30 days in each state or UT, with an optional 15-day self-enumeration window before it. Phase II, the population count with castes, is in February 2027, with a reference date of 1 March 2027. About 31 lakh enumerators and supervisors will use digital tools such as an offline mobile app in 16 languages.',
   nums=[('16th', 'Census, 8th since Independence'), ('₹11,718.24 cr', 'Outlay'), ('31 lakh', 'Enumerators and supervisors'), ('16', 'App languages')], chart=['cens'],
   trap='Section 15 of the Census Act 1948 keeps the data confidential: not under RTI, not court evidence.')
st('welfare', 'Welfare and finance decisions', 'Cabinet', 'DA rises to 60%; MGNREGA wages are released; a maritime insurance pool is approved')
# ... farms
st('pulses', 'Structured pulse procurement', 'Farms', 'Structured pulse procurement in Bihar and Chhattisgarh')
st('seafood', 'Seafood exports and fisheries output', 'Fisheries', 'Seafood exports reach a record ₹72,325.82 crore')
st('aif', 'Agriculture Infrastructure Fund target doubled', 'Farms', 'The Agriculture Infrastructure Fund target doubles to ₹2 lakh crore')
st('fisheries', 'Fisheries: Budget 2026-27 and schemes', 'Fisheries', 'Budget 2026-27 gives fisheries its highest-ever support')
st('nbs', 'NBS rates for Kharif 2026', 'Fertiliser', 'Kharif 2026 fertiliser subsidy: ₹41,533.81 crore')
st('ccea', 'CCEA approvals: Arunachal', 'Cabinet', 'Two Arunachal dams and a costlier Rajasthan refinery')
st('coalgas', 'Coal gasification incentive scheme', 'Energy', 'Coal gasification: an ₹8,500 crore scheme')
st('westasia', 'West Asia conflict: energy and trade responses', 'Energy', 'West Asia conflict: duty cuts, a PNG drive and E20 petrol')
st('expressway', 'Delhi-Dehradun Expressway', 'Roads', 'The Delhi–Dehradun Expressway cuts the journey to 2.5 hours')
st('ports', 'Ports: FY26 cargo', 'Ports', 'Major ports handle 915 MT; Kandla is back on top')
st('solar', 'Solar capacity and rare earths', 'Energy', 'A record of about 45 GW of solar is added in FY26')
st('sagarmala', 'Sagarmala and ports', 'Ports', 'Sagarmala: 845 projects, 315 complete', 'feature',
   lede='Sagarmala, launched in 2015, is India’s programme for port-led development, built on five pillars: port modernisation, connectivity, port-led industrialisation, coastal community development, and coastal shipping and inland waterways. It lists 845 projects worth ₹6.06 lakh cr, of which 315 (₹1.57 lakh cr) are complete; Sagarmala 2.0 brings ₹85,482 cr of budget support and ₹3.6 lakh cr of investment. Major ports handled 915.17 MT, against a target of 904 MT, and turnaround time fell from 96 hours in 2014 to 49.5 hours in 2025.',
   nums=[('845', 'Projects'), ('315', 'Complete'), ('915.17 MT', 'Major ports cargo'), ('49.5 h', 'Turnaround time, 2025')], chart=['tat'],
   trap='Sagarmala Finance Corporation, restructured in June 2025 from SDCL (set up in August 2016), is India’s first maritime NBFC.')
st('wind', 'Wind energy, 2025-26', 'Energy', 'Wind power: a record 6.05 GW in FY26')
st('iwai', 'Inland waterways: numbers and policies', 'Waterways', 'Inland waterways: 111 declared, 32 in use')
st('nonfossil', 'Non-fossil capacity FY2025-26', 'Energy', 'Non-fossil capacity reaches 283.46 GW', 'feature',
   lede='India added a record 55.3 GW of non-fossil capacity in FY26, taking the total to 283.46 GW on 31 March 2026: 274.68 GW of renewables (solar 150.26, wind 56.09, large hydro 51.41, bio 11.75 and small hydro 5.17) plus 8.78 GW of nuclear. Non-fossil sources generated 538.97 BU, 29.2% of the 1,845.921 BU produced. India reached 50% non-fossil capacity in June 2025, five years early.',
   nums=[('283.46 GW', 'Non-fossil capacity'), ('55.3 GW', 'Added in FY26'), ('150.26 GW', 'Solar'), ('29.2%', 'Of generation')], chart=['nfc'],
   trap='Non-fossil capacity reached 50% in June 2025, but non-fossil sources gave only 29.2% of generation.')
st('shekha', 'Shekha Jheel becomes', 'Wetlands', 'Shekha Jheel becomes India’s 99th Ramsar site')
st('green', 'Green Pathway', 'Environment', 'India’s conservation and climate numbers after a decade',
   lede='India’s conservation numbers have risen over the last decade. Protected areas went from 745 in 2014 to 1,134 in 2025, tiger reserves from 46 to 58 (3,167 tigers in 2022) and elephant reserves from 26 to 33. Ramsar sites reached 98 by 31 January 2026, up from 26 in 2014, the most in Asia and 3rd in the world. On climate, the 2022 NDC cuts emission intensity by 45% by 2030, India aims at net zero by 2070, and the Green Hydrogen Mission of 2023 targets 5 MMT by 2030.',
   nums=[('1,134', 'Protected areas, 2025'), ('58', 'Tiger reserves'), ('98', 'Ramsar sites, 31 Jan 2026'), ('2070', 'Net-zero year')])
st('patents', 'patent filings FY26', 'Patents', 'Patent filings hit a record 1.43 lakh')
st('panchayat', 'National Panchayati Raj Day', 'Panchayats', 'National Panchayati Raj Day recalls the 73rd Amendment')
st('pai', 'Panchayat Advancement Index (PAI) 2.0', 'Panchayats', 'Panchayat Advancement Index 2.0: no Achiever, 3,635 Front Runners', 'feature',
   lede='The Panchayat Advancement Index 2.0 was released on National Panchayati Raj Day, 24 April 2026, for FY2023-24. It uses 150 indicators and 230 data points across 9 themes, against 516 indicators and 794 data points in version 1.0. Participation was 97.30% (2,59,867 gram panchayats in 33 of 36 States and UTs; West Bengal was absent), against 80.79% before. No panchayat reached the top grade; 3,635 were Front Runners and 1,18,824 (45.72%) Performers.',
   nums=[('97.30%', 'Participation'), ('150', 'Indicators'), ('3,635', 'Front Runners'), ('1,18,824', 'Performers')], chart=['pai'],
   trap='Gram Sabha validation is mandatory. Best themes: poverty-free and enhanced livelihoods (3,313 A+) and Healthy Panchayat (1,015 A+).')
st('nso', 'NSO 80th round', 'Survey', 'NSO health survey: ₹11,285 out of pocket per hospital stay', 'feature',
   lede='The NSO’s 80th round, Household Social Consumption: Health, covered 1,39,732 households (76,296 rural and 63,436 urban) over January–December 2025. The median out-of-pocket cost per hospitalisation was ₹11,285 (mean ₹34,064); at a public facility the median was ₹1,100, and outpatient care in public facilities cost a median of zero. Cover by health schemes or insurance rose from 12.9% to 45.5% in rural areas and from 8.9% to 31.8% in urban areas.',
   nums=[('₹11,285', 'Median out of pocket, per stay'), ('₹1,100', 'Median at a public facility'), ('45.5%', 'Rural cover'), ('31.8%', 'Urban cover')], chart=['nso'],
   trap='The mean out-of-pocket cost per hospitalisation is ₹34,064, against a median of ₹11,285.')
st('wmi', 'Women and Men in India 2025', 'Report', 'Women and Men in India 2025: the sex ratio at birth rises to 917')
st('rajhighway', 'World Bank $225 million loan', 'Rajasthan', 'The World Bank lends $225 million for Rajasthan highways')
st('ladakh', 'Ladakh: five new districts', 'Ladakh', 'Ladakh gets five new districts')
st('odisha', 'Odisha: first state with Marine Spatial Plan', 'Odisha', 'Odisha prepares India’s first state Marine Spatial Plan')

# ---------- 5 ----------
st('mous', 'MoUs and agreements, April 2026', 'MoUs', 'The MoUs and agreements of April')
st('mna', 'M&A: Emirates NBD', 'Deals', 'Emirates NBD takes control of RBL Bank')
st('wto', 'WTO 14th Ministerial', 'WTO', 'WTO MC14 ends in Yaoundé: what India backed and opposed')
st('summits', 'India-hosted summits', 'Summits', 'The India–Africa Forum Summit and BRICS meetings')
st('appts', 'Appointments, April 2026', 'Appointments', 'Who took charge in April')
st('mythos', 'Panel on AI platform Mythos', 'Committees', 'A panel under SBI’s chairman will study AI risks to finance')

# ---------- 6 ----------
st('nqm', 'National Quantum Mission', 'Quantum', 'A 1,000 km secure quantum link is demonstrated')
st('artemis', 'Artemis II and Prototype', 'Space and nuclear', 'Artemis II flies round the Moon; India’s fast breeder reactor reaches criticality')
st('skyroot', 'Skyroot Vikram-1', 'Space', 'Skyroot’s Vikram-1: India’s first private orbital rocket')
st('chip', 'first chip fabrication plant', 'Chips', 'Dholera gets a special economic zone for India’s first chip plant')
st('relos', 'India-Russia RELOS', 'Defence', 'India and Russia agree to reciprocal military logistics')
st('navy', 'Navy: Taragiri', 'Navy', 'Taragiri, Aridhaman and Sunayna: a frigate, a submarine and a patrol vessel')
st('aiu', 'Athletics Integrity Unit', 'Doping', 'India is placed in the highest doping-risk category')
st('chess', 'Chess and athletics landmarks', 'Sport', 'Vaishali wins the Women’s Candidates; a sub-two-hour marathon')
st('tourn', 'Tournaments and results, April 2026', 'Sport', 'April’s tournaments: medals in wrestling, boxing, para archery and shooting',
   lede='India won 17 medals, 2 of them gold, at the Asian Wrestling Championships in Bishkek, and 16 medals, 5 gold, at the Asian Boxing Championships in Ulaanbaatar. It topped the World Archery Para Series in Bangkok with 13 medals (7 gold) and the ISSF Junior World Cup in Cairo with 16 (5 gold). At the 6th Asian Beach Games in Sanya, the women won kabaddi gold and the men silver. India’s women qualified for the AFC U17 Women’s Asian Cup after 21 years, while Bangladesh beat India at the SAFF Men’s U20 Championship in the Maldives.')

# ---------- 7 ----------
st('awards', 'Awards, April 2026', 'Awards', 'The awards of April')
st('prizes', 'Prizes in science and environment', 'Prizes', 'The Breakthrough Prizes and the Goldman Environmental Prize')
st('rank', 'World rankings in the news', 'Rankings', 'World rankings: India is 157th in press freedom and 5th in military spending')
st('reports', 'Reports: energy, wealth, hunger', 'Reports', 'India is the third-largest renewable market, says IRENA')

# ---------- 8 ----------
st('smile', 'SMILE: Support', 'Schemes', 'SMILE: livelihood support for transgender persons and people who beg')
st('poshan', 'Mission Poshan 2.0 and POSHAN', 'Schemes', 'Mission Poshan 2.0 and the Poshan Tracker')
st('enam', 'e-NAM (National Agriculture Market)', 'Schemes', 'e-NAM: 1,656 mandis and ₹4.84 lakh crore of trade')
st('ucf', 'Urban Challenge Fund (UCF)', 'Schemes', 'Urban Challenge Fund: ₹1 lakh crore to bring in ₹4 lakh crore')
st('pmgsy', 'PMGSY-III extended', 'Schemes', 'PMGSY-III is extended to March 2028')
st('plisfpi', 'PLI Scheme for Food Processing', 'Schemes', 'PLI for food processing: ₹10,900 crore')
st('insschemes', 'Insurance and pension schemes at a glance', 'Schemes', 'Insurance and pension schemes side by side',
   lede='Nine schemes sit in one table. PMJJBY and PMSBY began in May 2015: PMJJBY gives ₹2 lakh of life cover for ₹436 a year at ages 18–50, and PMSBY gives ₹2 lakh of accident cover for ₹20 at ages 18–70. AB PM-JAY covers ₹5 lakh per family and has issued 43.52 cr cards (February 2026). The Atal Pension Yojana pays ₹1,000–5,000 from age 60 and has 9 crore enrolments (21 April 2026), 1.35 cr of them in FY26.',
   nums=[('26.88 cr', 'PMJJBY enrolments'), ('57.11 cr', 'PMSBY enrolments'), ('43.52 cr', 'AB PM-JAY cards'), ('9 crore', 'Atal Pension Yojana enrolments')])
