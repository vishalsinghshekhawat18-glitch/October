# September 2026 print edition: the authored story layer for tools/print-ca/build.py.
# Facts only from the September notes; every number written here is checked against them.
NOTES = '../../../archive/current-affairs/CA_September_2026.html'
MONTH = 'September 2026'
PERIOD = '1–30 September'
OUTFILE = 'CA_September_2026_print'

COVER = dict(kicker='Section 1', title='The month India got its ‘A’ back', lead='jcr',
             dek='A Japanese agency lifts India’s rating to A-, the first return to the ‘A’ category in more than 35 years. Add 7.8% growth, record reserves and a $136.4 bn swap window: what happened, and the numbers to keep.',
             stats=[('7.8%', 'Real GDP growth, Q1 FY27'), ('4.82%', 'CPI inflation, August'), ('$785.7 bn', 'Forex reserves, record'), ('131st', 'India, Gender Gap Index')])
COVER_LINES = [('Section 1 · Trade', 'The New Zealand deal comes into force on 20 October', 'nz'),
               ('Section 1 · Payments', 'UPI payments up to ₹2,000 stay free of charge', 'upi0'),
               ('Section 3 · World', 'India hosts the 18th BRICS Summit in New Delhi', 'brics'),
               ('Section 6 · Sports', 'The Asian Games open in Aichi-Nagoya', 'asiang')]
LEADS = {1: 'JCR rating A- · GDP 7.8% · CPI 4.82% · forex $785.7 bn · NZ FTA · UPI free up to ₹2,000',
         2: 'Debit hold on mule accounts · tokenised bonds · NSE IPO · NPS Swasthya · UPSC at 100',
         3: 'BRICS in New Delhi · NDB · sea-level declaration · COP17 · G20 in Miami · G4 and GCC',
         4: 'Rabi MSP · Western DFC · Kishau dam · UNESCO list · Project Cheetah · FASTag annual pass',
         5: 'Global Fintech Fest · SCO in Bishkek · PRAHAAR · NFRA panel · CBFC',
         6: 'Radar and EOS-05 · Semicon 2.0 · RAKSHA · Asian Games · Mandhana and Gill',
         7: 'Magsaysay · National Film Awards · Gender Gap 131st · UNEP overshoot',
         8: 'UDAN · ECLGS 5.0 · Vibrant Villages · AB PM-JAY',
         9: 'Key numbers · upcoming dates · flashcards'}
DASH = '''<table class="score dash"><thead><tr><th>Indicator</th><th>Before</th><th>Now</th><th>Trend</th></tr></thead><tbody>
<tr><td>India’s rating (JCR)</td><td>BBB+</td><td>A-<small> stable outlook</small></td><td>▲ first ‘A’ in 35+ years</td></tr>
<tr><td>ADB forecast, FY27 growth</td><td>6.6% July</td><td>7.0% Sep</td><td>▲ raised</td></tr>
<tr><td>WPI (wholesale) inflation</td><td>9.78% Jul</td><td>9.92% Aug</td><td>▲ rising</td></tr>
<tr><td>Industrial production (IIP)</td><td>6.7% Jul</td><td>8.0% Aug</td><td>▲ faster</td></tr>
<tr><td>Core industries</td><td>5.0% Jul</td><td>4.8% Aug</td><td>▼ slower</td></tr>
<tr><td>Gross GST collection</td><td>₹2.11 lakh cr Jul</td><td>₹1,99,853 cr Aug</td><td>▼ lower</td></tr>
<tr><td>UPI payments</td><td>23.66 bn Jul</td><td>24.51 bn Aug</td><td>▲ record</td></tr>
</tbody></table>'''

def make_charts(hbar, steps, table_chart):
    return {
     'jcr': steps('India’s sovereign rating, step by step', [('A2', 'Moody’s, 1988'), ('Lost', '1990–91 payments crisis'), ('BBB+', 'JCR, before'), ('A-', 'JCR, September 2026')]),
     'fcst': table_chart('India’s FY27 growth forecast: earlier and now', ['Agency', 'Earlier', 'Now'],
                         [['ADB', '6.6%', '7.0%'], ['Moody’s', '6.0%', '7.0%'], ['S&P Global', '6.6%', '7.0%'], ['Fitch', '6.4%', '6.9%']], big_cols=(2,)),
     'gdpq1': table_chart('The first quarter of FY27, four ways', ['Measure', 'Level', 'Growth'],
                          [['Real GDP', '₹81.36 lakh crore', '7.8%'], ['Nominal GDP', '₹88.27 lakh crore', '10.3%'], ['Real GVA', '₹73.82 lakh crore', '8.2%'], ['Nominal GVA', '₹80.53 lakh crore', '11.5%']], big_cols=(2,)),
     'cpi': hbar('Heaviest weights in the new CPI (%)', [('Food & beverages', 36.75, '36.75'), ('Housing and fuels', 17.67, '17.67'), ('Transport', 8.8, '8.80'), ('Clothing', 6.38, '6.38'), ('Health', 6.1, '6.10')], 36.75, hi=0),
     'ici': hbar('Core industries: heaviest, newest and lightest (weight, %)', [('Electricity', 30.932, '30.932'), ('Refinery products', 22.572, '22.572'), ('Steel', 17.584, '17.584'), ('Iron ore (new)', 4.905, '4.905'), ('Fertilisers', 2.731, '2.731')], 30.932, hi=0),
     'forex': steps('What the reserves are made of', [('Largest', 'Foreign currency assets'), ('Part', 'Gold'), ('Part', 'SDRs'), ('Part', 'Reserve position with the IMF')], on_last=False),
     'borrow': hbar('Gross market borrowing, FY27 (₹ lakh crore)', [('Budget estimate', 17.2, '17.2'), ('After the cut', 15.99, '15.99')], 17.2, hi=1),
     'exp': table_chart('April–August 2026-27, in $ billion', ['', 'Exports', 'Imports'], [['Merchandise', '215.91', '363.00'], ['Services', '183.36', '96.65']], big_cols=(1, 2)),
     'disinv': hbar('The biggest stake sales (₹ crore)', [('LIC (6.5%)', 31515, '31,515'), ('Coal India (2%)', 5542, '5,542'), ('NHPC (6.01%)', 4357, '4,357'), ('Hindustan Copper (6%)', 3041, '3,041')], 31515, hi=0),
     'upi0': table_chart('What a UPI payment costs the merchant', ['Payment', 'Charge'],
                         [['UPI, up to ₹2,000', 'Nil'], ['Person to merchant, above ₹2,000', '0.4%'], ['₹75,000 and above', 'Capped at ₹300'], ['Railways, telecom, insurance, fuel, agri inputs, above ₹2,000', 'Flat ₹5'], ['Capital markets (MFs, brokers)', '0.02%, capped at ₹300']], big_cols=(1,)),
     'nz': steps('The New Zealand deal', [('27 Apr 2026', 'FTA signed'), ('20 Oct 2026', 'Comes into force'), ('2030', 'Trade to double to NZ$7 bn')]),
     'fcnr': hbar('Where the $136.377 bn came from ($ bn)', [('FCNR(B) deposits', 127.23, '127.23'), ('OFCB', 5.26, '5.26'), ('ECB', 3.89, '3.89')], 127.23, hi=0),
     'bmip': steps('The pool in three dates', [('18 Apr 2026', 'Approved'), ('12 May 2026', 'Launched; first H&M war-risk policy'), ('30 Jul', 'First P&I policy, to SCI')]),
     'epfo': hbar('Government outgo a year (₹ crore)', [('After the change', 11339, '11,339'), ('Existing support', 10250, '10,250')], 11339, hi=0),
     'ssr': hbar('Small savings rates, October–December 2026 (%)', [('Sukanya Samriddhi', 8.2, '8.2'), ('Kisan Vikas Patra', 7.5, '7.5'), ('PPF', 7.1, '7.1'), ('Post Office Savings Account', 4, '4.0')], 8.2, hi=0),
     'msp': hbar('Rabi MSP for 2027-28 (₹ per quintal)', [('Masur', 7390, '7,390'), ('Safflower', 7215, '7,215'), ('Rapeseed-mustard', 6613, '6,613'), ('Gram', 5958, '5,958'), ('Wheat', 2610, '2,610'), ('Barley', 2286, '2,286')], 7390, hi=4),
     'dfc': hbar('Length of the two freight corridors (km)', [('Western DFC', 1506, '1,506'), ('Eastern DFC', 1337, '1,337'), ('Network total', 2843, '2,843')], 2843, hi=2),
     'eclgs': table_chart('ECLGS 5.0: terms by borrower', ['Borrower', 'Guarantee', 'Support', 'Tenor'],
                          [['MSMEs', '100%', '20% of peak Q4 FY26 working capital, cap ₹100 crore', '5 years + 1-year moratorium'], ['Non-MSMEs', '90%', 'Same', 'Same'], ['Scheduled airlines', '90%', 'Up to ₹1,500 crore', '7 years + 2']], big_cols=(1,)),
     'vvp': table_chart('The two parts of the programme', ['', 'Type', 'Outlay', 'Villages'],
                        [['VVP-I', 'Centrally Sponsored', '₹4,800 crore', '662'], ['VVP-II', 'Central Sector', '₹6,839 crore', '1,954']], big_cols=(2, 3)),
     'brics': steps('How BRICS came about', [('2001', 'Jim O’Neill coins BRIC'), ('2006', 'BRIC formalised'), ('2009', 'First summit, Yekaterinburg'), ('2010–11', 'South Africa joins'), ('2024', 'Partner-country framework'), ('2026', 'India hosts the 18th')]),
     'gg1': hbar('India’s score on the four dimensions (%)', [('Education', 96.6, '96.6'), ('Health and survival', 95.6, '95.6'), ('Economic participation', 41.2, '41.2'), ('Political empowerment', 24.5, '24.5')], 96.6, hi=3),
     'gg2': hbar('South Asia’s ranks (lower is better)', [('Bangladesh', 79, '79th'), ('Maldives', 119, '119th'), ('Nepal', 120, '120th'), ('Bhutan', 121, '121st'), ('Sri Lanka', 129, '129th'), ('India', 131, '131st')], 131, hi=5),
     'swas': table_chart('The deductible rises with the cover', ['Cover', 'Deductible'], [['₹1 lakh', '₹10,000'], ['₹5 lakh', '₹50,000'], ['₹10 lakh', '₹1 lakh'], ['₹30 lakh', '₹3 lakh']], big_cols=(1,)),
     'aqi': steps('The air quality index', [('0–50', 'Good'), ('51–100', 'Satisfactory'), ('101–200', 'Moderate'), ('201–300', 'Poor'), ('301–400', 'Very poor'), ('401–500', 'Severe')], on_last=False),
    }

SEC_INTRO = {
 1: 'India’s rating moves up, the economy grows 7.8%, and prices, output and trade arrive on new base years. The month also brings free small UPI payments, a swap window that drew in $136.4 bn and a higher wage ceiling for provident fund.',
 2: 'The RBI proposes a debit hold for fraud accounts and tightens capital and deposit-rate rules; SEBI tests tokenised bonds and clears the NSE for an IPO; PFRDA and IFSCA set new rules.',
 3: 'India hosts the BRICS summit, the UN adopts declarations on sea-level rise and maps, and India meets the G4, the GCC and the G20.',
 4: 'New rules for passports and time, farm prices and sugar limits, freight corridors and trains, and a month of wildlife and heritage news.',
 5: 'Global Fintech Fest, the SCO summit at 25 years, a ten-year counter-terror strategy and two reconstituted bodies.',
 6: 'A debris-tracking radar and a new satellite, a bigger chip plan, a defence diplomacy framework and a long-range drone, and the Asian Games.',
 7: 'Awards from Asia and the film world, and two reports: the Gender Gap Index and a UN warning on temperature overshoot.',
 8: 'Five schemes: a ten-year UDAN, shipbuilding aid, a fifth round of emergency credit guarantees, border villages and health insurance at 8 years.',
}

CHAPTERS = {
 1: [('1.1', 'Ratings, forecasts and the foreign accounts', 'A rating upgrade, higher growth forecasts, a wider current account deficit and record reserves.', ['jcr', 'fcst', 'cad', 'forex']),
     ('1.2', 'Growth, prices and output', 'First-quarter growth, retail and wholesale inflation, factories, core industries and GST.', ['gdpq1', 'cpi', 'wpi', 'iip', 'ici', 'gst']),
     ('1.3', 'Borrowing, stake sales and savings', 'Lower borrowing, disinvestment, a record IPO and unchanged small savings rates.', ['borrow', 'disinv', 'ssr', 'jio']),
     ('1.4', 'Trade and investment', 'Exports, two trade deals, record FDI and rules for online sellers.', ['exp', 'nz', 'eufta', 'fdi', 'fdiecom', 'oils', 'deh', 'ecomrules', 'mii']),
     ('1.5', 'Banks and payments', 'Free small UPI payments, new ways to pay, a swap window, bank data and a new evidence law.', ['upirec', 'upi0', 'tap', 'erupee', 'treds', 'blue', 'bbea', 'coastal', 'ifc', 'uff', 'fcnr', 'bankdata']),
     ('1.6', 'Insurance and pensions', 'A plan to remake insurance sales, a pool for ships and a higher EPFO wage ceiling.', ['irdai', 'bmip', 'epfo'])],
 2: [('2.1', 'RBI: rules, limits and surveys', 'A debit hold for fraud accounts, capital and deposit-rate rules, the exporters’ deadline and the Centre’s overdraft limit.', ['surveys', 'sop', 'mrisk', 'bulk', 'exportrel', 'wma', 'lic', 'psl']),
     ('2.2', 'SEBI: bonds, stocks and commodities', 'An IPO for the NSE, tokenised bonds, new position limits and a board package.', ['nse', 'demat', 'comm', 'sboard', 'dr']),
     ('2.3', 'Other regulators', 'GIFT City’s rulebook, pension schemes, a crackdown on digital-asset firms, Nidhi companies and UPSC at 100.', ['ifsca', 'msf', 'swasthya', 'fiu', 'nidhi', 'upsc'])],
 3: [('3.1', 'Banks and groups', 'Development banks, the BRICS summit in New Delhi and what BRICS is.', ['adb', 'ndb', 'aiib', 'brics']),
     ('3.2', 'The UN, climate and trade', 'Statehood after sea-level rise, the drought toolkit, the Equal Earth map, carbon rules and trade pacts.', ['sealevel', 'unccd', 'map', 'ukcbam', 'mercosur', 'atlas']),
     ('3.3', 'G20, G4 and partners', 'The next G20 summit, three new groupings in the UN week and India’s role in a fighter programme.', ['g20', 'p4m', 'g4', 'gcc', 'fipic', 'gcap'])],
 4: [('4.1', 'Laws and institutions', 'Passports, a dissolved commission, a victims’ centre, Ladakh, land records, standard time and a joint committee.', ['passport', 'dcc', 'victims', 'a371', 'dilrmp', 'legalmet', 'jpc']),
     ('4.2', 'Farms, food and gas', 'Grain stores, piped gas, sugar, a district programme and Rabi support prices.', ['grain', 'png', 'sugar', 'ddky', 'msp']),
     ('4.3', 'Roads, rails, ports and power', 'Toll-tag changes, mega ports, new trains, a dam, coal gas, green power lines and a finished freight corridor.', ['onetag', 'megaports', 'rail', 'fastag', 'kishau', 'coalgas', 'gec', 'dfc']),
     ('4.4', 'Heritage, wildlife and air', 'The UNESCO list, cheetahs, port clearances, the Great Indian Bustard, clean air and tiger reserves.', ['unesco', 'cheetah', 'greenclear', 'gib', 'skies', 'mangrove', 'meetr'])],
 5: [('5.1', 'Conferences', 'Fintech, circular economy, the SCO summit and a counter-terrorism strategy.', ['gff', 'wcef', 'sco', 'prahaar']),
     ('5.2', 'Committees and boards', 'An audit panel and the film certification board.', ['nfra', 'cbfc'])],
 6: [('6.1', 'Space and technology', 'A radar, two satellites, a new Artemis signatory and a bigger chip plan.', ['radar', 'eos', 'trishna', 'artemis', 'semicon']),
     ('6.2', 'Defence', 'A diplomacy framework, a long-range drone, Tejas deliveries and a large approval.', ['raksha', 'kal', 'hal', 'dac']),
     ('6.3', 'Sports', 'The Asian Games, para archery, cricket, a run of firsts and two batting records.', ['asiang', 'para', 'cricket', 'wins', 'mandhana', 'gill'])],
 7: [('7.1', 'Prizes', 'The Magsaysay winners and the National Film Awards.', ['rm', 'film']),
     ('7.2', 'Reports and rankings', 'India’s place on the Gender Gap Index and a warning on temperature overshoot.', ['gender', 'unep'])],
 8: [('8.1', 'Schemes of the month', 'Flights, ships, credit guarantees, border villages and health.', ['udan', 'sbfas', 'eclgs', 'vvp', 'pmjay'])],
}

S = {}
def st(key, card, tag, h, size='short', **kw): S[key] = dict(card=card, tag=tag, h=h, size=size, **kw)

# ---------- 1 ----------
st('jcr', 'JCR upgrades India', 'Rating', 'JCR lifts India to A-, the first ‘A’ in over 35 years', 'feature',
   lede='The Japan Credit Rating Agency raised India’s long-term foreign-currency and local-currency issuer ratings by one notch, from BBB+ to A-, with a stable outlook. The country ceiling also rose one notch, to A. It is India’s first return to the ‘A’ category in more than 35 years: the last ‘A’ was Moody’s A2 in 1988, lost in the 1990–91 balance of payments crisis.',
   nums=[('BBB+ → A-', 'Issuer ratings'), ('Stable', 'Outlook'), ('A', 'Country ceiling'), ('35+ years', 'Since India was last ‘A’')], chart=['jcr'],
   trap='JCR is the Japanese agency. The issuer ratings are A-; only the country ceiling is A.')
st('fcst', 'FY27 GDP growth forecasts raised', 'Forecasts', 'Five agencies lift India’s growth forecast to about 7%', 'feature',
   lede='Five agencies raised their forecasts for India’s FY27 growth. Moody’s, which said India proved more resilient to the Middle East conflict, went from 6.0% to 7.0%. ADB went from 6.6% to 7.0% and S&P Global from 6.6% to 7.0%, though S&P warns of a slower second half. Fitch moved from 6.4% to 6.9%, and the OECD to 7.1%, a rise of 80 basis points.',
   nums=[('7.0%', 'ADB, Moody’s, S&P'), ('6.9%', 'Fitch'), ('7.1%', 'OECD'), ('7.8%', 'Actual, Q1 FY27')], chart=['fcst'],
   trap='ADB raised FY27 but cut FY28, from 7.3% to 7.1%. Moody’s keeps its Baa3 rating, stable.')
st('cad', 'Current Account Deficit (CAD) widens', 'Balance of payments', 'Current account deficit widens to $4.2 billion',
   lede='India’s current account deficit was $4.2 billion, 0.5% of GDP, in April–June 2026, against $3.4 billion (0.4%) a year earlier. FDI was $6.1 billion against $5.2 billion, while ECB borrowing fell to $1.0 billion from $5.5 billion. Reserves fell by $8.1 billion on a balance of payments basis, and by $22.5 billion once valuation is counted.')
st('forex', 'forex reserves hit record', 'Reserves', 'Forex reserves hit a record $785.7 billion', 'feature',
   lede='India’s foreign exchange reserves reached an all-time high of $785.706 billion in the week ended 4 September 2026, a rise of $44.9 billion in a single week. India is now the fourth-largest holder, after China, Japan and Switzerland.',
   nums=[('$785.706 bn', 'Reserves, 4 Sep'), ('+$44.9 bn', 'Rise in the week'), ('4th', 'Largest holder')], chart=['forex'],
   trap='SDRs are the IMF-created Special Drawing Rights; they sit alongside foreign currency assets, gold and the reserve position with the IMF.')
st('borrow', 'gross market borrowing', 'Government finances', 'The Centre trims FY27 borrowing to ₹15.99 lakh crore', 'feature',
   lede='The Centre cut its gross market borrowing for FY27 by ₹1.2 lakh crore from the budget estimate of ₹17.2 lakh crore, to ₹15,99,506 crore. The second-half plan is ₹7,86,000 crore, including ₹15,000 crore of Sovereign Green Bonds, through 23 weekly auctions. The FY27 fiscal deficit target is 4.3% of GDP.',
   nums=[('₹15,99,506 cr', 'FY27 borrowing'), ('₹17.2 lakh cr', 'Budget estimate'), ('₹7,86,000 cr', 'Second-half plan'), ('4.3%', 'Fiscal deficit target')], chart=['borrow'],
   trap='Tenors on offer are 3, 5, 7, 10, 15, 30, 40 and 50 years; the greenshoe is ₹2,000 crore and the H2 WMA limit ₹50,000 crore.')
st('gdpq1', 'GDP Q1 FY2026-27', 'GDP', 'The economy grows 7.8% in the first quarter', 'feature',
   lede='India’s real GDP grew 7.8% in the first quarter of FY27, to ₹81.36 lakh crore; nominal GDP was ₹88.27 lakh crore, up 10.3%. It is the highest first-quarter growth between 2023-24 and 2026-27, helped by manufacturing, services and domestic demand. Real GVA grew faster, at 8.2%. The release also moved the national accounts to a new base year, 2022-23.',
   nums=[('7.8%', 'Real GDP growth'), ('8.2%', 'Real GVA growth'), ('10.3%', 'Nominal GDP growth'), ('2022-23', 'New base year')], chart=['gdpq1'],
   trap='GDP counts final goods and services; GVA counts the value added by producers and sectors. Two new indices came with the revision: the Output PPI and the Banking Services Price Index.')
st('cpi', 'CPI inflation August 2026', 'Inflation', 'Retail inflation is 4.82% on a new base year', 'feature',
   lede='Retail inflation was 4.82% in August 2026, and food inflation 5.95%. From this release the consumer price index uses a new base year, 2024=100, with 358 weighted items (299 earlier) in 12 divisions. Food and beverages carry the biggest weight, 36.75%.',
   nums=[('4.82%', 'CPI inflation, Aug'), ('5.95%', 'Food inflation (CFPI)'), ('358', 'Weighted items'), ('36.75%', 'Weight of food and beverages')], chart=['cpi'],
   trap='The 358 items are 308 goods and 50 services, against 299 items earlier.')
st('wpi', 'WPI inflation August 2026', 'Inflation', 'Wholesale inflation edges up to 9.92%',
   lede='Wholesale inflation was 9.92% in August 2026, up from 9.78% in July. The index has the base 2022-23 and covers 957 items; manufactured products carry the most weight, 63.12%. The Office of Economic Adviser in DPIIT releases it by the 14th of the next month.')
st('iip', 'IIP August 2026', 'Industry', 'Industrial output grows 8.0% in August',
   lede='Industrial output grew 8.0% in August 2026, against a quick estimate of 6.7% for July, and the index stood at 123.3. The NSO releases it on the 28th of each month. The new basket, on base 2022-23, has 1,042 products in 463 item groups, up from 839 and 407; manufacturing carries the most weight, 76.062%.')
st('ici', 'Index of Core Industries (new base', 'Core industries', 'Core industries grow 4.8% on a new base', 'feature',
   lede='The Index of Core Industries grew 4.8% in August 2026, a little slower than the final 5.0% of July. The index was rebuilt on a new base, 2022-23 (the old one was 2011-12), and now covers nine industries instead of eight, with iron ore added. Electricity has the largest weight and fertilisers the smallest.',
   nums=[('4.8%', 'Growth, August'), ('5.0%', 'July, final'), ('8 → 9', 'Core industries'), ('2022-23', 'New base year')], chart=['ici'],
   trap='Steel is measured on gross production and coal means raw coal only; the linking factor is 1.47.')
st('gst', 'Gross GST collection, August 2026', 'GST', 'August GST collection: ₹1,99,853 crore',
   lede='Gross GST collection in August 2026 was ₹1,99,853 crore, up 14.8% on a year earlier and close to ₹2 trillion. It was lower than the ₹2.11 lakh crore of July 2026. The Ministry of Finance released the data.')
st('jio', 'Jio Platforms IPO', 'IPO', 'SEBI clears Jio Platforms’ ₹37,700 crore IPO',
   lede='SEBI cleared the IPO of Jio Platforms, a fresh issue of about ₹37,700 crore (27 crore shares, about 2.93% dilution). It would be India’s largest IPO, bigger than Hyundai’s in 2024. ₹27,500 crore of the money is meant for debt, and Reliance holds 66.43%.')
st('disinv', 'Disinvestment ₹62,124', 'Disinvestment', 'Stake sales raise ₹62,124 crore, 78% of the target', 'feature',
   lede='The government has raised ₹62,124 crore from disinvestment in FY27, which is 78% of its ₹80,000 crore target. Minority stake sales in nine PSUs brought ₹55,757 crore and InvIT monetisation ₹6,367 crore. The biggest sale was 6.5% of LIC, for ₹31,515 crore.',
   nums=[('₹62,124 cr', 'Raised so far'), ('78%', 'Of the target'), ('₹80,000 cr', 'FY27 target'), ('₹31,515 cr', 'From LIC, 6.5%')], chart=['disinv'],
   trap='The receipts are booked under Miscellaneous Capital Receipts.')
st('ssr', 'Small savings rates unchanged', 'Small savings', 'Small savings rates unchanged for the 10th quarter', 'feature',
   lede='The government left small savings rates unchanged for October–December 2026, the tenth quarter in a row. Sukanya Samriddhi pays 8.2%, PPF 7.1%, Kisan Vikas Patra 7.5% (it matures in 115 months) and a Post Office Savings Account 4.0%.',
   nums=[('10th', 'Quarter unchanged'), ('8.2%', 'Sukanya Samriddhi'), ('7.5%', 'Kisan Vikas Patra'), ('7.1%', 'PPF')], chart=['ssr'],
   trap='The rates are the same as in the second quarter of FY27.')
st('exp', 'Exports in August 2026', 'Trade', 'Exports jump 25.41% in August', 'feature',
   lede='India’s merchandise and services exports together were $82.68 billion in August 2026, up 25.41% on a year earlier. Over April–August, merchandise exports were $215.91 billion against imports of $363.00 billion, while services exports were $183.36 billion against imports of $96.65 billion. The total trade balance was −$60.38 billion.',
   nums=[('$82.68 bn', 'Exports, August'), ('25.41%', 'Growth on a year earlier'), ('$215.91 bn', 'Merchandise exports, Apr–Aug'), ('−$60.38 bn', 'Trade balance, Apr–Aug')], chart=['exp'],
   trap='Fastest export growth, April–August: Tanzania (129%), then Singapore, Malaysia, China and the USA.')
st('nz', 'New Zealand FTA to come into force', 'Trade deals', 'The India–New Zealand FTA starts on 20 October', 'feature',
   lede='India and New Zealand signed a free trade agreement on 27 April 2026, and Commerce Minister Piyush Goyal announced that it comes into force on 20 October 2026. All of India’s exports get duty-free access, against peak tariffs of up to 10% on ceramics, carpets, automobiles and auto components. New Zealand will invest $20 billion in India over 15 years, and both want trade to double to NZ$7 billion by 2030.',
   nums=[('20 Oct 2026', 'In force'), ('100%', 'Indian exports duty-free'), ('$20 bn', 'NZ investment, 15 years'), ('NZ$7 bn', 'Trade target, 2030')], chart=['nz'],
   trap='Dairy, meat (except sheep), sugar and edible oils are excluded. Each year brings 5,000 temporary employment visas and 1,000 working-holiday visas.')
st('eufta', 'India–EU FTA concluded', 'Trade deals', 'India and the EU conclude a trade deal after 25 years')
st('fdi', 'Record FDI inflow', 'Investment', 'Record FDI: $94.53 billion in 2025–26',
   lede='India received a record $94.53 billion of foreign direct investment in 2025–26, the highest ever in a year, and Commerce Minister Piyush Goyal put the total since 2014 at $843 billion. The coal sector now allows 100% FDI under the automatic route.')
st('fdiecom', 'FDI rules: e-commerce', 'FDI', 'E-commerce firms may hold stock for exports')
st('oils', 'Basic customs duty cut on edible oils', 'Customs', 'Import duty on edible oils is cut')
st('deh', 'Districts as Export Hubs', 'Exports', 'Every district an export hub')
st('ecomrules', 'Consumer Protection (E-Commerce) Amendment Rules', 'Consumer', 'Online shops must show the real earlier price')
st('mii', 'Make in India: 12 years', 'Industry', 'Make in India turns 12',
   lede='Make in India completed 12 years on 25 September 2026. Its second phase covers 27 sectors, 15 in manufacturing and 12 in services. Manufacturing GVA grew at 10.88% a year from 2022-23 to 2025-26, electronics output reached ₹13.11 lakh crore, and mobile phones ₹6.3 lakh crore, which makes India the second-largest producer. Cumulative FDI since 2014-15 is $843 billion.')
st('upirec', 'UPI record: 24.51 bn', 'Payments', 'UPI hits a record 24.51 billion payments',
   lede='UPI handled a record 24.51 billion transactions in August 2026, worth ₹29.82 lakh crore. Volume was up 3.6% on July (23.66 billion) and 22% on a year earlier. The record for value, ₹29.90 lakh crore, is still May 2026. UPI completed 10 years on 25 August 2026, with an average daily volume of 791 million.')
st('upi0', 'zero charges on UPI', 'Payments', 'UPI payments up to ₹2,000 stay free', 'feature',
   lede='The Finance Ministry notified that UPI payments up to ₹2,000 carry no direct or indirect charges, which keeps about 96% of UPI volume free. Person-to-person payments stay free, and so do all RuPay debit card payments. Above ₹2,000, a person-to-merchant payment can attract a merchant discount rate (MDR) of 0.4%, capped at ₹300 a payment from ₹75,000. The legal basis is Section 10A of the Payment and Settlement Systems Act, 2007.',
   nums=[('₹2,000', 'Free up to'), ('0.4%', 'MDR above it'), ('₹300', 'Cap, ₹75,000 and above'), ('96%', 'Of UPI volume stays free')], chart=['upi0'],
   trap='MDR applies to only about 4% of merchant transactions, and 18% GST is charged on MDR above ₹2,000. MDR is not a government tax.')
st('tap', 'UPI Tap and Pay', 'Payments', 'UPI Tap and Pay and MyUPI are announced')
st('erupee', 'programmable Digital Rupee', 'Digital rupee', 'Bank of India launches a programmable digital rupee')
st('treds', 'TReDS receivables', 'MSME credit', 'Unpaid bills of small firms get a guarantee cover')
st('blue', 'Sagarmala Finance', 'Bonds', 'India’s first blue bond')
st('bbea', 'Books Evidence Act, 2026', 'Law', 'A new law for bank records as evidence')
st('coastal', 'Coastal Local Area Bank', 'RBI', 'A local area bank becomes a scheduled bank for the first time')
st('ifc', 'IFC funding for long-term MSME', 'MSME credit', 'IFC lends $1 billion for small-business loans')
st('uff', 'Unified Fintech Forum as SRO-FT', 'Fintech', 'A second fintech self-regulator is recognised')
st('fcnr', 'swap window: $136.4', 'RBI · forex', 'The swap window pulls in $136.4 billion', 'feature',
   lede='The RBI’s special USD-INR swap, open from 8 June 2026 for FCNR(B) deposits, ECBs and OFCBs, mobilised $136.377 billion by 31 August, against an expected $90–100 billion. FCNR(B) deposits made up $127.23 billion, about 93%; OFCBs brought $5.26 billion and ECBs $3.89 billion. Deposit growth reached 17.8% in the fortnight to 31 August, the highest since 2011, and credit grew 19.1%.',
   nums=[('$136.377 bn', 'Mobilised by 31 Aug'), ('$127.23 bn', 'FCNR(B), about 93%'), ('17.8%', 'Deposit growth'), ('19.1%', 'Credit growth')], chart=['fcnr'],
   trap='The FCNR(B) window closed on 31 August, not 30 September as first planned. ECB and OFCB stay open till 31 December 2026.')
st('bankdata', 'Bank credit and deposit data', 'Banking data', 'Credit grows 16.5%, gold loans surge, bad loans at a low',
   lede='Bank credit grew 16.5% in June 2026 against 9.9% a year earlier, and deposits grew 11.5%; the weighted average lending rate was 9.26%, down from 9.71%. NBFC gold loans grew 68.5% year on year in July, to about ₹3.54 trillion, while banks hold ₹5.52 trillion. The Financial Stability Report puts gross NPAs at 1.8%, a multi-decade low, with CRAR at 17.7% and CET1 at 15.3%. PMJDY, begun on 28 August 2014, now has 59.09 crore accounts holding ₹3.17 lakh crore.')
st('irdai', 'IRDAI proposes overhaul', 'IRDAI', 'IRDAI proposes a three-tier model for selling insurance',
   lede='IRDAI proposed an overhaul of how insurance is sold: a simpler three-tier distribution structure, lower limits on the expense of management, revised commissions and tougher safeguards against mis-selling. For life insurers the ceiling would fall to 15% in two years and 12.5% in five. For general insurers the limit would move from 30% of gross written premium to 20% of domestic gross direct premium income in five years.')
st('bmip', 'Bharat Maritime Insurance Pool', 'Insurance', 'Indian insurers pool their capacity for ships', 'feature',
   lede='Indian insurers have pooled their capacity in the Bharat Maritime Insurance Pool, approved on 18 April 2026 and launched on 12 May 2026. Its capacity is ₹13,906.50 crore (US$1.5 billion), backed by a sovereign guarantee of ₹12,980 crore, and GIC Re is the administrator. It covers hull and machinery, cargo, P&I and war risks. About 95% of India’s trade by value moves by sea, and foreign P&I premium outflow is US$45–60 million a year.',
   nums=[('₹13,906.50 cr', 'Capacity (US$1.5 bn)'), ('₹12,980 cr', 'Sovereign guarantee'), ('10 years', 'Tenure, extendable to 15'), ('US$100 m', 'Claims met from reserves')], chart=['bmip'],
   trap='Claims up to US$100 million come from reserves and reinsurance.')
st('epfo', 'EPFO wage ceiling', 'EPFO', 'The EPFO wage ceiling rises to ₹25,000', 'feature',
   lede='The Cabinet raised the EPFO wage ceiling for mandatory coverage from ₹15,000 to ₹25,000 a month. The ₹15,000 ceiling dated from September 2014. More workers will get provident fund cover, a pension under the Employees’ Pension Scheme and insurance under the EDLI scheme. The annual cost to the government is about ₹11,339 crore, against existing budgetary support of about ₹10,250 crore, and the five-year cost about ₹56,696 crore.',
   nums=[('₹15,000 → ₹25,000', 'Monthly ceiling'), ('₹11,339 cr', 'Annual outgo'), ('₹10,250 cr', 'Existing support'), ('₹56,696 cr', 'Five-year cost')], chart=['epfo'],
   trap='The ceiling was last revised in September 2014.')

# ---------- 2 ----------
st('surveys', 'three surveys for monetary policy', 'RBI · surveys', 'The RBI launches three surveys of households')
st('sop', 'draft SOP', 'RBI · fraud', 'A 60-day debit hold for suspected mule accounts')
st('mrisk', 'market-risk capital framework', 'RBI · capital', 'New market-risk capital rules from 1 April 2027')
st('bulk', 'bulk deposit rate disclosure', 'RBI · deposits', 'Banks must publish their deposit rates by 10 AM')
st('exportrel', 'export-realisation limit', 'RBI · FEMA', 'Exporters keep their 9-month deadline')
st('wma', 'Ways and Means Advances limit', 'RBI · government', 'The WMA limit for the second half is ₹50,000 crore')
st('lic', 'LIC stake of up to 9.99%', 'RBI · ownership', 'LIC may hold up to 9.99% of ICICI Bank')
st('psl', 'PSL cut-off date', 'RBI · PSL', 'A new PSL cut-off date and less reporting for AD banks',
   lede='The RBI moved the cut-off date for excluding FCNR(B) and NRE funds from the priority-sector lending base (ANBC) from 30 September to 31 August 2026. Separately, AD-I banks no longer have to file an annual list of rupee accounts of non-resident banks or 5-day overdraw reports.')
st('nse', 'NSE gets SEBI nod', 'SEBI · IPO', 'SEBI clears the NSE’s IPO as an offer for sale')
st('demat', 'Demat 2.0', 'SEBI · bonds', 'SEBI pilots tokenised corporate bonds')
st('comm', 'commodity derivatives position limits', 'SEBI · commodities', 'Commodity position limits and penalties are revised')
st('sboard', 'SEBI board: PMS overhaul', 'SEBI · board', 'SEBI board: portfolio managers, settlement and FPIs')
st('dr', 'depository receipts against REIT', 'SEBI · REITs', 'Depository receipts against REIT and InvIT units')
st('ifsca', 'IFSCA notifies a single', 'IFSCA', 'GIFT City gets its own market-abuse rulebook')
st('msf', 'reclassifies NPS Multiple Scheme', 'PFRDA', 'NPS multiple schemes are sorted by equity share')
st('swasthya', 'NPS Swasthya Pension Scheme, 2026', 'PFRDA', 'NPS Swasthya: a pension and health cover in one', 'feature',
   lede='PFRDA issued operational guidelines for the NPS Swasthya Pension Scheme, 2026, which links retirement savings with health insurance. It covers the subscriber, the spouse and up to two dependent children on a family floater; parents are excluded. It has two parts, an NPS Swasthya Investment Account and a Super Top-up, and the deductible rises with the cover.',
   nums=[('18–70', 'Entry age (renewal to 85)'), ('2', 'Dependent children covered'), ('₹1,000', 'Minimum investment'), ('₹10', 'Later contributions')], chart=['swas'],
   trap='The legal basis is Section 14 of the PFRDA Act, 2013.')
st('fiu', 'FIU-IND acts', 'FIU-IND', 'FIU-IND acts against 15 digital-asset service providers')
st('nidhi', 'MCA advisory on Nidhi', 'MCA', 'Nidhi companies: a warning on high-return promises')
st('upsc', 'UPSC centenary', 'Institutions', 'UPSC completes a century',
   lede='The first Public Service Commission was constituted on 1 October 1926, and the UPSC completed a century on 1 October 2026; the Prime Minister released a coin, a stamp and a book, and the Chairman is Dr Ajay Kumar. It became the UPSC on 26 January 1950. The Constitution deals with it in Articles 315–323 (Part XIV): Article 316 covers appointment and Article 317 removal after a Supreme Court inquiry. The first woman chair was Rose Millian Bathew Kharbuli.')

# ---------- 3 ----------
st('adb', 'ADB signs its first Transaction', 'ADB', 'ADB will advise Madhya Pradesh on clean-energy PPPs')
st('ndb', 'New Development Bank (NDB)', 'NDB', 'The NDB: five founders and new members',
   lede='The New Development Bank was set up in 2015 by the BRICS countries (Brazil, Russia, India, China and South Africa) and is headquartered in Shanghai. Its authorised capital is $100 billion; each founder subscribed $10 billion of the $50 billion initial capital, 18.72% each. Since 2021 it has added Bangladesh, the UAE, Egypt, Algeria and Uzbekistan (June 2026). Uruguay, Colombia, Ethiopia, Angola and Zimbabwe are prospective members.')
st('aiib', 'AIIB Annual Meeting', 'AIIB', 'AIIB meets in Doha')
st('brics', '18th BRICS Summit', 'BRICS', 'India hosts the 18th BRICS Summit', 'feature',
   lede='India hosted the 18th BRICS Summit at Bharat Mandapam, New Delhi, on 12–13 September 2026, as it chairs BRICS in 2026 (it also chaired in 2012, 2016 and 2021). The theme was “Building for Resilience, Innovation, Cooperation, and Sustainability”. BRICS has 11 members and 10 partner countries; the 11 members together hold 49.5% of the world’s population, 40% of GDP and 26% of trade. China hosts the 19th summit in 2027.',
   nums=[('18th', 'BRICS Summit'), ('11', 'Members'), ('10', 'Partner countries'), ('49.5%', 'Of world population')], chart=['brics'],
   trap='India’s earlier summits: the 4th (New Delhi, 2012), the 8th (Goa, 2016) and the 13th (2021). The 11 members are Brazil, Russia, India, China, South Africa, Egypt, Ethiopia, Iran, Saudi Arabia, the UAE and Indonesia.')
st('sealevel', 'Political Declaration on Sea-Level Rise', 'UN', 'A country keeps its statehood even if the sea takes its land')
st('unccd', 'UNCCD COP17', 'UN · land', 'UNCCD COP17 builds a drought toolkit')
st('map', 'Correct the Map', 'UN', 'The UN backs the Equal Earth map')
st('ukcbam', 'UK recognises India', 'Climate trade', 'The UK accepts India’s carbon market for CBAM relief')
st('mercosur', 'India–MERCOSUR', 'Trade', 'India and MERCOSUR talk of widening their trade pact')
st('atlas', 'ATLAS initiative', 'Nuclear', 'India joins an initiative on nuclear power at sea')
st('g20', 'G20: Energy Abundance', 'G20', 'The G20 summit is set for Miami on 14–15 December',
   lede='G20 energy ministers met for the Energy Abundance Ministerial, and India endorsed a consensus on household energy access, faster approvals for infrastructure, water reuse and resilient critical-mineral supply chains. The 2026 G20 Leaders’ Summit will be held on 14–15 December 2026 at Trump National Doral, Miami; the UK has confirmed Manchester for 2027. The G20 was founded in 1999 after the 1997–98 Asian crisis, has 19 countries plus the EU and the AU (a permanent member since 2023), and accounts for about 85% of global GDP.')
st('p4m', 'Inaugural P4M', 'UN', 'India co-sponsors a new UN group, P4M')
st('g4', 'G4 foreign ministers', 'UN', 'The G4 press for reform of the UN Security Council')
st('gcc', 'India–GCC Troika', 'Gulf', 'India and the GCC review their action plan')
st('fipic', 'FIPIC and Pacific', 'Pacific', 'FIPIC: India’s forum with the Pacific islands',
   lede='FIPIC, the Forum for India–Pacific Islands Cooperation, was formed in 2014 during PM Modi’s Fiji visit and links India with 14 Pacific island countries on clean energy, health and digital connectivity. Its summits were FIPIC I in Suva (November 2014), FIPIC II in Jaipur (August 2015) and FIPIC III in Port Moresby (May 2023). The Pacific Islands Forum, founded in 1971, has 18 members and its Secretariat in Suva; India sits in its Strategic Partner stream.')
st('gcap', 'dialogue partner in GCAP', 'Defence', 'India joins the GCAP fighter programme as a dialogue partner')

# ---------- 4 ----------
st('passport', 'Passports (Amendment) Rules', 'Passports', 'Children’s passports stay valid for longer')
st('dcc', 'Digital Communications Commission', 'Telecom', 'The Digital Communications Commission is dissolved',
   lede='The government dissolved the Digital Communications Commission, the apex inter-departmental body under the Department of Telecommunications. It was set up in 1989 as the Telecom Commission and renamed in 2018, so it lasted about 37 years.')
st('victims', 'Rights Centre inaugurated', 'Justice', 'The first Victims’ Rights Centre opens in Patna')
st('a371', 'Article 371(K)', 'Constitution', 'A special article for Ladakh is proposed')
st('dilrmp', 'DILRMP 3.0', 'Land records', 'DILRMP 3.0: digital land records for ₹565.50 crore')
st('legalmet', 'Legal Metrology (Indian Standard Time)', 'Law', 'Indian Standard Time becomes the legal time')
st('jpc', 'JPC on Foreign Contribution', 'Parliament', 'A 31-member JPC will study the FCRA amendment bill')
st('grain', 'Decentralised Grain Storage', 'Cooperatives', 'Grain stores at village cooperatives')
st('png', 'Incentive Scheme for Promotion of Domestic PNG', 'Energy', 'Cheap gas for firms that add home connections')
st('sugar', 'Sugar: stockholding limits', 'Sugar', 'Sugar stock limits change and the FRP is set at ₹365')
st('ddky', 'PM Dhan-Dhaanya', 'Agriculture', 'PM Dhan-Dhaanya: 100 districts and rising scores')
st('msp', 'Rabi MSP for marketing season 2027-28', 'Farm prices', 'Wheat MSP ₹2,610, safflower up ₹675', 'feature',
   lede='The Cabinet Committee on Economic Affairs fixed the minimum support prices for the Rabi crops of the 2027-28 marketing season. Wheat is ₹2,610 a quintal. Safflower got the biggest rise, ₹675, then rapeseed-mustard, ₹413. Wheat has the best margin over cost, 106%, and safflower the lowest, 50%.',
   nums=[('₹2,610', 'Wheat, per quintal'), ('₹675', 'Safflower rise, highest'), ('106%', 'Wheat margin over cost'), ('50%', 'Safflower margin, lowest')], chart=['msp'],
   trap='MSP is at least 1.5 times the cost (Budget 2018-19), and 22 crops are mandated on CACP advice.')
st('onetag', 'OneTag', 'Roads', 'OneTag: switch FASTag banks without a new tag')
st('megaports', 'four Mega Ports', 'Ports', 'Four ports are notified as mega ports')
st('rail', 'rail firsts', 'Railways', 'India’s first LNG-powered and hydrogen trains')
st('fastag', 'FASTag Annual Pass crosses', 'Roads', 'One crore FASTag annual passes')
st('kishau', 'Kishau Multipurpose', 'Water', 'Six states sign for the Kishau dam')
st('coalgas', 'Coal/lignite gasification', 'Energy', 'A ₹37,500 crore scheme to gasify coal')
st('gec', 'Green Energy Corridor Phase-III', 'Energy', 'Green Energy Corridor III: ₹1,86,405 crore')
st('dfc', 'Western Dedicated Freight Corridor', 'Railways', 'The Western freight corridor is complete', 'feature',
   lede='The Prime Minister dedicated the Western Dedicated Freight Corridor, built at ₹73,000 crore. The last three sections, 326 route km, include New Saphale–JNPA, and the corridor runs 1,506 km across five states (Maharashtra, Gujarat, Rajasthan, Haryana and UP) from Dadri to JNPA. With the 1,337 km Eastern DFC (October 2023, ₹51,000 crore), the network is 2,843 km. The project began in 2005, and DFCCIL builds and runs it.',
   nums=[('1,506 km', 'Western DFC'), ('1,337 km', 'Eastern DFC'), ('2,843 km', 'Network total'), ('₹73,000 cr', 'Western DFC cost')], chart=['dfc'],
   trap='The network has capacity for 480 trains a day, at an average speed of 50+ kmph.')
st('unesco', 'UNESCO Tentative List', 'Heritage', 'India’s UNESCO tentative list grows to 78',
   lede='India’s UNESCO Tentative List grew in two steps. The first four sites took it to 73 (53 cultural, 17 natural and 3 mixed); a later five entries took it to 78. Among the additions are the Painted Haveli Towns of Shekhawati in Rajasthan and a serial transnational proposal, Sites of Satyagraha, with South Africa.')
st('cheetah', 'Four years of Project Cheetah', 'Wildlife', 'Project Cheetah: 52 cheetahs after four years',
   lede='Project Cheetah completed four years in September 2026. It was launched on 17 September 2022 at Kuno National Park in Madhya Pradesh with 8 cheetahs from Namibia, followed by 12 from South Africa in 2023 and 9 from Botswana in 2026. India now has 52 cheetahs, 32 of them born in India; 49 are at Kuno and 3 at Gandhi Sagar Sanctuary.')
st('greenclear', 'Green clearances for ports', 'Environment', 'Port clearances can now last up to 30 years')
st('gib', 'Great Indian Bustard', 'Wildlife', 'Great Indian Bustard: Critically Endangered',
   lede='The Great Indian Bustard (Ardeotis nigriceps) lives mainly in Rajasthan’s Thar Desert, with small numbers in Gujarat, Maharashtra, Karnataka and Andhra Pradesh. It is Critically Endangered on the IUCN list, in Appendix I of both CITES and CMS, and in Schedule I of the Wildlife (Protection) Act, 1972.')
st('skies', 'Path to Blue Skies', 'Clean air', 'Clean-air facts: 1,646 stations and the AQI scale',
   lede='India marks the International Day of Clean Air for Blue Skies, 7 September, as Swachh Vayu Diwas. The National Air Quality Monitoring Programme has 1,646 stations in 603 cities and tracks 8 pollutants. NCAP, begun in 2019, covers 130 cities with a performance-linked grant of ₹16,425 crore.',
   chart=['aqi'])
st('mangrove', 'Mangroves, ozone and net-zero', 'Environment', 'Mangroves, ozone and net-zero portals')
st('meetr', 'MEE-TR 2026', 'Tigers', 'Tiger reserves face their 6th management check-up')

# ---------- 5 ----------
st('gff', 'Global Fintech Fest 2026, Mumbai', 'Conference', 'Global Fintech Fest 2026 in Mumbai')
st('wcef', 'World Circular Economy Forum', 'Conference', 'The World Circular Economy Forum comes to South Asia')
st('sco', '26th SCO Summit', 'SCO', 'The SCO at 25: the Bishkek summit',
   lede='The 26th SCO Summit in Bishkek, Kyrgyzstan, marked 25 years of the Shanghai Cooperation Organisation, founded in 2001. It has 10 members: the six founders (China, Russia, Kazakhstan, Kyrgyzstan, Tajikistan and Uzbekistan), India and Pakistan (2017), Iran (2023) and Belarus (2024). The chair passes from Kyrgyzstan to Pakistan, and Islamabad hosts the 2027 summit. PM Modi’s S-C-O pillars are Security, Connectivity and Opportunity.')
st('prahaar', 'PRAHAAR', 'Security', 'PRAHAAR: a 10-year counter-terror strategy')
st('nfra', 'NFRA sets up', 'NFRA', 'NFRA forms an audit-quality panel')
st('cbfc', 'CBFC reconstituted', 'CBFC', 'The CBFC is reconstituted for three years')

# ---------- 6 ----------
st('radar', 'Advanced Radar Research Centre', 'Space', 'ISRO breaks ground on a debris-tracking radar')
st('eos', 'EOS-05', 'Space', 'EOS-05: India’s first imaging satellite in geosynchronous orbit')
st('trishna', 'TRISHNA', 'Space', 'TRISHNA: an Indo-French heat-mapping satellite')
st('artemis', '71st signatory', 'Space', 'Türkiye becomes the 71st Artemis Accords signatory')
st('semicon', 'Semicon India Programme 2.0', 'Chips', 'Semicon 2.0: ₹1,27,500 crore for chips')
st('raksha', 'RAKSHA', 'Defence', 'RAKSHA: a 10-year defence diplomacy plan')
st('kal', 'KAL: India', 'Defence', 'KAL: India’s first long-range attack drone')
st('hal', 'HAL: F404', 'Defence', 'HAL becomes the 14th Maharatna',
   lede='GE Aerospace delivered 3 more F404-IN20 engines for the Tejas Mk1A, and HAL became the 14th Maharatna CPSE. HAL handed over LCA Tejas FOC twin-seat trainers and HTT-40 basic trainers to the IAF, and Dhruv-NG helicopters to Pawan Hans.')
st('dac', 'DAC approves', 'Defence', 'The DAC clears ₹1.10 lakh crore of purchases')
st('asiang', 'Asian Games 2026 (20th)', 'Asian Games', 'The Asian Games open in Aichi-Nagoya',
   lede='The 20th Asian Games opened in Aichi-Nagoya, Japan, on 19 September 2026 and run to 4 October; Emperor Naruhito declared them open. India’s flag bearers were Manu Bhaker and Pawan Sehrawat. The Games saw the debut of mixed martial arts, where Suchika Tariyal became the first Indian MMA medallist, and of surfing. India’s first gold came from the women’s cricket team, which beat Sri Lanka by 147 runs, and its first individual gold from Neeru Dhanda in women’s trap.')
st('para', 'World Archery Para Series', 'Para sport', 'India hosts a para archery event for the first time')
st('cricket', 'Cricket: Women', 'Cricket', 'India win the Women’s Asia Cup',
   lede='India won the 10th Women’s Asia Cup, beating Sri Lanka by 72 runs in Dubai; it was India’s 8th Asia Cup title overall and 4th in T20, and Shafali Verma was Player of the Match. India will host the inaugural Women’s Champions Trophy in 2027, after Sri Lanka was dropped over governance issues: six teams will play in Mumbai and Vadodara from 14 to 28 February 2027.')
st('wins', 'sports wins: badminton', 'Sport', 'Firsts in badminton, archery, hockey and chess',
   lede='A run of firsts: Satwiksairaj Rankireddy and Chirag Shetty won India’s first China Masters title; Dhiraj Bommadevara took the first Indian male recurve gold at the Archery World Cup Final; the junior hockey men won a 6th Asia Cup title, the 4th in a row; and India won the Chess Olympiad’s Nona Gaprindashvili Trophy for the 3rd time running.')
st('mandhana', 'Smriti Mandhana', 'Cricket', 'Smriti Mandhana passes 11,000 international runs')
st('gill', 'fastest ODI double century', 'Cricket', 'Shubman Gill hits the fastest ODI double century')

# ---------- 7 ----------
st('rm', 'Ramon Magsaysay Award 2026', 'Awards', 'Ramon Magsaysay Award 2026: three winners')
st('film', '72nd National Film Awards', 'Awards', 'National Film Awards: Anant Nag gets the Phalke',
   lede='The 72nd National Film Awards, for 2024, were presented on 22 September 2026 at Ekta Nagar (Kevadia), Gujarat. Anant Nag received the Phalke Award (₹10 lakh). Swarna Kamal prizes carry ₹3 lakh and Rajat Kamal ₹2 lakh, across 26 feature, 16 non-feature and 2 writing categories. Ravi Raj Murmu won Best Debut Director for Angen, in Santhali.')
st('gender', 'Global Gender Gap Index 2026', 'Gender gap', 'India stays 131st on the Gender Gap Index', 'feature',
   lede='The World Economic Forum’s Global Gender Gap Index 2026, its 20th edition, covers 145 economies and ranks India 131st, unchanged, with a score of 0.645 (64.5%) against a global 69.2%. Iceland tops the index for the 17th year and Chad is last at 145th. India’s best-ranked sub-index is political empowerment, 67th, even though its score there, 24.5%, is the lowest; education scores highest, 96.6%.',
   nums=[('131st', 'India, unchanged'), ('0.645', 'India’s score'), ('69.2%', 'Global score'), ('67th', 'Political empowerment rank')], chart=['gg1', 'gg2'])
st('unep', 'Limiting Overshoot', 'Climate', 'UNEP: the 1.5°C limit will be crossed within a few years')

# ---------- 8 ----------
st('udan', 'Modified UDAN', 'Aviation', 'UDAN continues for 10 years with ₹28,840 crore')
st('sbfas', 'Shipbuilding Financial Assistance', 'Shipping', 'Shipbuilding aid is extended to 2036')
st('eclgs', 'Emergency Credit Line', 'Credit guarantee', 'ECLGS 5.0: credit guarantees up to ₹2.55 lakh crore', 'feature',
   lede='The government approved the fifth round of the Emergency Credit Line Guarantee Scheme (ECLGS) on 5 May 2026, to be run by NCGTC. It offers credit up to ₹2.55 lakh crore and is valid until 31 March 2027 or until the limit is reached. MSMEs get a 100% guarantee; non-MSMEs and scheduled passenger airlines get 90%, with no guarantee fee.',
   nums=[('₹2.55 lakh cr', 'Credit, up to'), ('100% / 90%', 'Guarantee: MSMEs / others'), ('31 Mar 2027', 'Valid till'), ('97.3%', 'MSMEs, by number')], chart=['eclgs'],
   trap='On 20 August 2026, 6,73,979 guarantees worth ₹2,50,024 crore had been issued. Phases 1.0–4.0 issued 1.19 crore guarantees worth ₹3.68 lakh crore and closed on 31 March 2023.')
st('vvp', 'Vibrant Villages Programme (VVP)', 'Border villages', 'Vibrant Villages: ₹11,639 crore for border villages', 'feature',
   lede='The Vibrant Villages Programme, launched in 2023 under the Home Ministry, has ₹11,639 crore for more than 2,616 border villages. VVP-I covers 662 villages in Arunachal, Himachal, Sikkim, Uttarakhand and Ladakh, and was launched on 10 April 2023 at Kibithoo. VVP-II covers 1,954 villages in 15 states and 2 UTs, including Rajasthan, and was launched on 20 February 2026 at Nathanpur, Assam. It replaces the Border Area Development Programme of 1986-87.',
   nums=[('₹11,639 cr', 'Total outlay'), ('2,616+', 'Border villages'), ('662', 'VVP-I villages'), ('1,954', 'VVP-II villages')], chart=['vvp'],
   trap='India’s land border is more than 15,000 km: Bangladesh 4,096.7 km, China 3,488 km and Pakistan 3,323 km.')
st('pmjay', 'AB PM-JAY and ABDM', 'Health', 'AB PM-JAY turns 8 with 13.25 crore admissions',
   lede='AB PM-JAY completed 8 years on 23 September 2026. It gives ₹5 lakh a family and has recorded 13.25 crore admissions worth ₹2.03 lakh crore. The digital health mission ABDM, begun in September 2021, has issued 97.61 crore ABHA IDs and 119.95 crore records (17 September 2026). The adult literacy mission ULLAS/NILP targets 5 crore learners in 2022-27; literacy was 74.04% in 2011 and 81.1% in PLFS 2025.')
