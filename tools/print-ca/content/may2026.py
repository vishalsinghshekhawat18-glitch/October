# May 2026 print edition: the authored story layer for tools/print-ca/build.py.
# Facts only from the May notes; every number written here is checked against them.
# The May notes are not yet archived in the repo. Until they are, point CA_MAY_NOTES at a local copy of
# the project file CA_May_2026.html; the default is where the archived copy will be.
import os
NOTES = os.environ.get('CA_MAY_NOTES', '../../../archive/current-affairs/CA_May_2026.html')
MONTH = 'May 2026'
PERIOD = '1–31 May'
OUTFILE = 'CA_May_2026_print'

COVER = dict(kicker='Section 2', title='The RBI’s record surplus for the Centre', lead='surplus',
             dek='The RBI Central Board approves ₹2,86,588.46 crore for the Centre, the highest ever. Add a 15% customs duty on gold and silver, final rules for four labour codes and a ₹2,55,000 crore credit guarantee: what happened, and the numbers to keep.',
             stats=[('6.5%', 'RBI Contingent Risk Buffer'), ('15%', 'Customs duty, gold and silver'), ('29 laws', 'Merged into four labour codes'), ('125 days', 'VB-G RAM G guarantee')])
COVER_LINES = [('Section 1 · Trade', 'Customs duty on gold and silver rises from 6% to 15%', 'golddut'),
               ('Section 4 · Labour', 'Final rules are notified under all four labour codes', 'labour'),
               ('Section 8 · Schemes', 'ECLGS 5.0 backs ₹2,55,000 crore of credit', 'cab'),
               ('Section 6 · Sports', 'Royal Challengers Bengaluru win IPL 2026', 'ipl')]
LEADS = {1: 'RBI gold · forex and FDI · gold duty 15% · UPI record · PSB profit · maritime insurance pool',
         2: 'RBI surplus · CET1 · IFR · FEMA rules · phone-locking draft · SEBI nominees · NPS Sanchay',
         3: 'US Special 301 list · India–UAE $5 bn · India–Italy partnership',
         4: 'Judges at 38 · labour codes · 18th railway zone · Bhiwadi chip plant · cheetahs',
         5: 'RBI–ECB MoU · Kotak stakes · BRICS and Quad · Nordic summit · new Chief Ministers',
         6: 'Drishti satellite · LR-AShM · PRAGATI · weightlifting · IPL 2026',
         7: 'Agricola Medal · Palme d’Or · Henley 78th · remittances $137.67 bn · SRS 2024',
         8: 'ECLGS 5.0 · gasification · VB-G RAM G · Kharif MSP',
         9: 'Key numbers · upcoming dates · flashcards'}
DASH = '''<table class="score dash"><thead><tr><th>Indicator</th><th>Before</th><th>Now</th><th>Trend</th></tr></thead><tbody>
<tr><td>Customs duty, gold and silver</td><td>6%</td><td>15%<small> from 13 May</small></td><td>▲ more than doubled</td></tr>
<tr><td>RBI surplus to the Centre</td><td>₹2.68 lakh crore</td><td>₹2,86,588.46 crore</td><td>▲ highest ever</td></tr>
<tr><td>Transfer to the Contingent Risk Buffer</td><td>₹44,861.70 crore</td><td>₹1,09,379.64 crore</td><td>▲ higher</td></tr>
<tr><td>Gold share of forex reserves</td><td>13.92%<small> Sep 2025</small></td><td>16.70%<small> Mar 2026</small></td><td>▲ larger</td></tr>
<tr><td>Forex reserves</td><td>$696.988 bn<small> 8 May</small></td><td>$688.894 bn<small> 15 May</small></td><td>▼ lower</td></tr>
<tr><td>Guaranteed rural work</td><td>100 days</td><td>125 days<small> from 1 July</small></td><td>▲ 25 more days</td></tr>
<tr><td>Minimum annuity, non-government NPS</td><td>40%</td><td>20%</td><td>▼ halved</td></tr>
<tr><td>Crimes registered (NCRB)</td><td>62.41 lakh</td><td>58.85 lakh</td><td>▼ down 6%</td></tr>
</tbody></table>'''

def make_charts(hbar, steps, table_chart):
    return {
     'surplus': hbar('The surplus transferred to the Centre', [('2025-26', 286588.46, '₹2,86,588.46 crore'), ('Previous year', 268000, '₹2.68 lakh crore')], 286588.46, hi=0),
     'crb': hbar('The transfer to the Contingent Risk Buffer (₹ crore)', [('2025-26', 109379.64, '1,09,379.64'), ('Previous year', 44861.70, '44,861.70')], 109379.64, hi=0),
     'dutytab': table_chart('The new duty at a glance', ['Item', 'Before', 'Now'],
                            [['Gold and silver', '6%', '15%'], ['Platinum', '6.4%', '15.4%'], ['Spent catalysts or ash with precious metals', '—', '4.35%']], big_cols=(2,)),
     'ore': hbar('Gold ore resources by state (%)', [('Bihar', 43, '43%'), ('Rajasthan', 24.92, '24.92%'), ('Karnataka', 20, '20%')], 43, hi=1),
     'spot': hbar('RBI in the spot forex market, 2025-26 ($ bn)', [('Sold', 195, '195'), ('Bought', 142, '142'), ('Net sale', 53.13, '53.13')], 195, hi=2),
     'fdi': hbar('FDI in 2025-26 ($ bn)', [('Gross FDI', 94.53, '94.53'), ('Net FDI', 7.65, '7.65')], 94.53, hi=0),
     'paytab': table_chart('Who leads, second half of 2025', ['', 'By volume', 'By value'],
                           [['Highest share', 'UPI 85.5%', 'RTGS 68.6%'], ['Next', 'NEFT 3.6%, PPIs 3.6%', 'NEFT 14.9%, UPI 9.5%'], ['Lowest share', 'RTGS 0.1%', 'PPIs 0.1%']], big_cols=(1, 2)),
     'upi': hbar('UPI transactions (crore)', [('2021', 3873, '3,873'), ('2025', 22828, '22,828')], 22828, hi=1),
     'codes': table_chart('The four codes', ['Code', 'Year'], [['Code on Wages', '2019'], ['Industrial Relations Code', '2020'], ['Code on Social Security', '2020'], ['OSHWC Code', '2020']], big_cols=(1,)),
     'socsec': hbar('Social security coverage (% of population)', [('Before', 19, '19%'), ('Now', 64, '64%')], 64, hi=1),
     'schemes': hbar('Credit or outlay by scheme (₹ crore)', [('ECLGS 5.0 (credit)', 255000, '2,55,000'), ('Coal gasification', 37500, '37,500'), ('BHAVYA', 33660, '33,660'), ('SARTHAK-PDS', 25530, '25,530'), ('Cotton Mission', 5659.22, '5,659.22')], 255000, hi=0),
     'eclgs': table_chart('ECLGS 5.0: terms by borrower', ['Borrower', 'Guarantee', 'Support', 'Tenor'],
                          [['MSMEs', '100%', '20% of peak Q4 FY26 working capital, cap ₹100 crore', '5 years'], ['Non-MSMEs', '90%', 'Same', '5 years'], ['Airlines', '90%', 'Up to ₹1,500 crore', '7 years']], big_cols=(1,)),
     'days': hbar('Days of guaranteed work a year', [('MGNREGA', 100, '100'), ('VB-G RAM G', 125, '125')], 125, hi=1),
     'fund': table_chart('Who pays', ['Group', 'Funding'], [['North-East and Himalayan states', '90:10'], ['Other states', '60:40'], ['UTs without legislature', '100% Centre']], big_cols=(1,)),
     'mspr': hbar('Largest MSP rises, 2026-27 (₹ per quintal)', [('Sunflower seed', 622, '₹622'), ('Cotton', 557, '₹557'), ('Nigerseed', 515, '₹515'), ('Sesamum', 500, '₹500')], 622, hi=0),
     'grain': table_chart('Third Advance Estimates, 2025-26 (million tonnes)', ['Crop', 'Output'],
                          [['Rice', '154.024'], ['Wheat', '120.657'], ['Maize', '55.093'], ['Oilseeds', '43.059'], ['Sugarcane', '500.063']], big_cols=(1,)),
     'infl': hbar('Inflation in April 2026 (%)', [('WPI (wholesale)', 8.3, '8.3%'), ('CPI food', 4.20, '4.20%'), ('CPI (retail)', 3.48, '3.48%')], 8.3, hi=0),
     'plfs': table_chart('PLFS, January–March 2026', ['Measure', 'Rate'],
                         [['Labour force participation (LFPR)', '55.5%'], ['Female LFPR', '34.7%'], ['Worker population ratio (WPR)', '52.8%'], ['Urban unemployment', '6.6%'], ['Rural unemployment', '4.3%']], big_cols=(1,)),
     'goldwhere': hbar('Where the gold is (tonnes)', [('In India', 680.05, '680.05'), ('Bank of England and BIS', 197.67, '197.67'), ('Gold deposits', 2.80, '2.80')], 680.05, hi=0),
     'goldshare': steps('Gold as a share of total reserves', [('13.92%', 'End-September 2025'), ('16.70%', 'End-March 2026')]),
     'npa': hbar('Bad loans at 31 March 2026 (%)', [('Gross NPA', 1.93, '1.93%'), ('Net NPA', 0.39, '0.39%')], 1.93, hi=0),
     'viab': steps('Plans for the regional rural banks', [('FY22 to FY25', 'First plan'), ('2025-26 to 2027-28', 'Viability Plan 2.0')]),
     'iftab': table_chart('IFR rule by bank type', ['Bank type', 'Rule'],
                          [['Commercial banks, LABs', 'Discontinued'], ['SFBs, payments banks', 'At least 2% of AFS and FVTPL portfolio'], ['RRBs', 'At least 2% of HFT and AFS portfolio'],
                           ['UCBs', 'Minimum 5% of investment portfolio'], ['RCBs', 'Not less than 5% of investments in the Current category']], big_cols=()),
     'femat': table_chart('Net worth and turnover', ['Category', 'Minimum net worth', 'Minimum forex turnover'],
                          [['AD Category-II', '₹10 crore', '₹50 crore'], ['AD Category-III', '₹2 crore', '—'], ['FFMC', '₹25 lakh (single branch), ₹50 lakh (multiple)', '₹10 crore']], big_cols=(1,)),
     'uae5': hbar('The UAE’s $5 bn pledge ($ bn)', [('Emirates NBD in RBL Bank', 3, '3'), ('ADIA with NIIF', 1, '1'), ('IHC in Sammaan Capital', 1, '1')], 3, hi=0),
     'remit': hbar('Top five receivers of remittances, 2024 ($ bn)', [('India', 137.67, '137.67'), ('Mexico', 67.64, '67.64'), ('Philippines', 40.28, '40.28'), ('France', 38.78, '38.78'), ('Pakistan', 34.91, '34.91')], 137.67, hi=0),
     'send': hbar('Top senders, 2024 ($ bn)', [('US', 103.18, '103.18'), ('Saudi Arabia', 46.56, '46.56'), ('Switzerland', 40.11, '40.11')], 103.18, hi=0),
    }

SEC_INTRO = {
 1: 'The RBI’s gold and reserves, a much higher customs duty on gold and silver, a record month for UPI, record profits at public sector banks and a new pool for ship insurance.',
 2: 'The RBI sends a record surplus to the Centre, drops one reserve and tightens others, and rewrites who may deal in foreign exchange. SEBI and PFRDA set new rules for indices, nominees, AI risk and pensions.',
 3: 'A US trade report keeps India on its watch list, the UAE pledges investment, and India raises its ties with Italy.',
 4: 'More judges for the Supreme Court, final rules for the labour codes, a new railway zone and chip plant, and a good month for cheetahs and forts.',
 5: 'Central banks sign agreements, banks take stakes in one another, India hosts BRICS and Quad ministers, and several states get new Chief Ministers.',
 6: 'The first satellite that carries a camera and a radar, new missile tests, a new army exercise and the IPL.',
 7: 'Honours for the Prime Minister and for Chandrayaan-3, rankings, a report on remittances, and population and climate reports.',
 8: 'A new round of credit guarantees and four other approvals, a new law for rural work and higher Kharif support prices.',
}

CHAPTERS = {
 1: [('1.1', 'Reserves and the foreign accounts', 'Gold, forex reserves and dollar sales, and the UN forecast for India.', ['goldhold', 'forex', 'undesa']),
     ('1.2', 'Prices, output and jobs', 'Inflation, factory output, jobs and what the states are asked to change.', ['data', 'iip', 'sasci']),
     ('1.3', 'Trade, investment and energy', 'A much higher duty on gold and silver, an easier rule for Chinese stakes and the fuel mix.', ['golddut', 'fdiland', 'energy']),
     ('1.4', 'Banks and payments', 'A payments report, a UPI record, a Dubai bank buying into RBL Bank and the profits of public sector banks.', ['pay', 'upi', 'end', 'psb']),
     ('1.5', 'Insurance and pensions', 'Full foreign ownership of insurers, a pool for ships and three schemes at eleven years.', ['insfdi', 'bmip', 'jan'])],
 2: [('2.1', 'RBI: capital, reserves and rules', 'The surplus, capital rules, a reserve ended, foreign exchange dealers and two drafts.', ['surplus', 'cet1', 'ifr', 'coop', 'ccyb', 'swap', 'fema', 'recov', 'pillar3']),
     ('2.2', 'SEBI: indices, nominees and AI risk', 'Significant indices, nominees, a task force, price data and two proposals.', ['sigidx', 'nomin', 'aiadv', 'lag', 'garuda']),
     ('2.3', 'The pension regulator', 'New bonds for NPS and a simple scheme for informal workers.', ['pfrda', 'sanchay'])],
 3: [('3.1', 'Watch lists and partners', 'A US report, the UAE and Italy.', ['intlorg', 'uae', 'italy'])],
 4: [('4.1', 'Courts, sport and labour law', 'More judges, rules for sports bodies and the final labour code rules.', ['sc', 'sports', 'labour']),
     ('4.2', 'Rails, chips and industry', 'A new railway zone, firsts in infrastructure and a chip plant in Rajasthan.', ['infra', 'raj']),
     ('4.3', 'Wildlife and heritage', 'Cheetahs, a big cat alliance and a long wall.', ['wild'])],
 5: [('5.1', 'Agreements and deals', 'Central bank pacts and bank stakes.', ['rbimou', 'stake']),
     ('5.2', 'Summits', 'BRICS and Quad ministers in New Delhi and the Nordic summit.', ['summits', 'nordic']),
     ('5.3', 'People and committees', 'New chiefs, new Chief Ministers and a quantum committee.', ['appts', 'cm', 'qsafe'])],
 6: [('6.1', 'Space', 'A satellite with a camera and a radar.', ['space']),
     ('6.2', 'Defence', 'Missile tests, ships and an army exercise.', ['missiles', 'defplat', 'pragati']),
     ('6.3', 'Sports', 'Weightlifting at home and the IPL.', ['sportsres', 'ipl'])],
 7: [('7.1', 'Honours', 'Awards for people and missions.', ['awards']),
     ('7.2', 'Reports and rankings', 'Rankings, remittances, population and crime, and energy and climate.', ['rank', 'migr', 'srs', 'enclim'])],
 8: [('8.1', 'Schemes of the month', 'Credit, rural work and farm prices.', ['cab', 'vbgramg', 'msp'])],
}

S = {}
def st(key, card, tag, h, size='short', **kw): S[key] = dict(card=card, tag=tag, h=h, size=size, **kw)

# ---------- 1 ----------
st('goldhold', 'RBI gold holdings', 'Reserves', 'The RBI keeps 77.23% of its 880.52 tonnes of gold at home', 'feature',
   lede='The RBI’s Half-Yearly Report on Management of Foreign Exchange Reserves shows 880.52 tonnes of gold at end-March 2026: 680.05 tonnes in India, 197.67 tonnes with the Bank of England and BIS, and 2.80 tonnes as gold deposits. The share held in India is 77.23%, up from 59.2% a year ago. Gold is now 16.70% of total reserves by dollar value, against 13.92% at end-September 2025.',
   nums=[('880.52 t', 'Gold held'), ('77.23%', 'Kept in India'), ('16.70%', 'Gold share of reserves'), ('$552 bn', 'Foreign currency assets')], chart=['goldwhere', 'goldshare'],
   trap='Of the $552 billion in foreign currency assets, 84.31% is in securities, 8.48% in deposits with other central banks and BIS, and 7.21% in deposits with commercial banks overseas.')
st('forex', 'Forex reserves, FDI', 'Reserves', 'Reserves slip to $688.894 billion as the RBI sells a record net $53.13 billion', 'feature',
   lede='Foreign exchange reserves rose $6.295 bn to $696.988 bn in the week ended 8 May, then fell $8.094 bn to $688.894 bn in the week ended 15 May. Over 2025-26 the RBI bought $142 bn and sold $195 bn in the spot market, a net sale of $53.13 bn, the highest in a financial year. Gross FDI reached a record $94.53 bn, up 17%, but net FDI was only $7.65 bn, against $959 million the year before.',
   nums=[('$688.894 bn', 'Reserves, 15 May'), ('$53.13 bn', 'RBI net dollar sale'), ('$94.53 bn', 'Gross FDI, record'), ('$7.65 bn', 'Net FDI')], chart=['spot', 'fdi'],
   trap='Outward FDI in April 2026 was $5.6 bn, down 10.8%. The LRS limit is $250,000 per financial year, and the scheme began in 2004.')
st('undesa', 'UN World Economic', 'Forecast', 'The UN cuts India’s 2026 growth forecast to 6.4%')
st('data', 'Price, output and jobs', 'Data', 'Retail inflation is 3.48% but wholesale is 8.3%', 'feature',
   lede='In April 2026 retail inflation (CPI, base 2024) was 3.48%, with food at 4.20%, while wholesale inflation (WPI, base 2011-12) was 8.3%, provisional. The eight core industries grew 1.7% in April; March 2026 was finalised at 1.2% and FY26 at 2.7%. The PLFS for January–March 2026 puts labour force participation at 55.5% and female participation at 34.7%, with 57.4 crore people employed. Non-food bank credit grew 15.9% in FY26.',
   nums=[('3.48%', 'CPI, April'), ('8.3%', 'WPI, April'), ('1.7%', 'Eight core industries'), ('55.5%', 'LFPR, Jan–Mar')], chart=['infl', 'plfs'],
   trap='CPI comes from MoSPI through NSO; WPI comes from DPIIT, on the 14th. Both figures are for April 2026.')
st('iip', 'new IIP series', 'Statistics', 'The new IIP series moves to the 2022-23 base year')
st('sasci', 'Fiscal and statistical reforms', 'States', 'A ₹3,000 crore pool rewards fiscally disciplined states')
st('golddut', 'Gold, silver and platinum', 'Customs', 'Customs duty on gold and silver jumps from 6% to 15%', 'feature',
   lede='From 13 May 2026 the effective customs duty on gold and silver rose from 6% to 15%: a basic customs duty of 10% plus an AIDC of 5%. Platinum went from 6.4% to 15.4%, and dore, coins and findings are covered too. Silver bars of 99.9% purity or more moved from free to restricted import, so a licence is needed. DGFT capped duty-free gold under Advance Authorisation at 100 kg, with the next authorisation only after 50% of the export obligation is met. India is the second largest gold consumer after China and imports about 90% of its gold.',
   nums=[('6% → 15%', 'Gold and silver'), ('10% + 5%', 'Basic duty + AIDC'), ('6.4% → 15.4%', 'Platinum'), ('100 kg', 'Cap on duty-free gold')], chart=['dutytab', 'ore'],
   trap='Bihar holds the largest gold ore resources, but Karnataka produces 97% of the gold mined in India.')
st('fdiland', 'FDI from land-border', 'FDI', 'A Chinese stake of up to 10% now qualifies for the automatic route')
st('energy', 'Energy: renewables', 'Energy', 'India is 3rd in renewable capacity as E30 petrol gets a standard')
st('pay', 'RBI Payment Systems Report', 'Payments', 'UPI leads payments by volume, RTGS by value', 'feature',
   lede='The RBI’s Payment Systems Report covers the second half of 2025. UPI had 85.5% of transactions by volume, but RTGS carried 68.6% of the value, with UPI at 9.5%. Total payments came to 14,270.2 crore transactions worth ₹1,642.8 lakh crore. From 2021 to 2025 all payments grew from 6,437 crore to 26,819 crore transactions, a CAGR of 42.9%, and UPI grew from 3,873 crore to 22,828 crore.',
   nums=[('85.5%', 'UPI, share by volume'), ('68.6%', 'RTGS, share by value'), ('99.8%', 'Digital share by volume, 2025'), ('22,828 cr', 'UPI transactions, 2025')], chart=['paytab', 'upi'],
   trap='Debit cards have fallen since 2021, down 24.4% in volume and 11.7% in value, while credit cards grew about 27%. The IMPS limit is ₹5 lakh per transaction.')
st('upi', 'UPI record and payment firsts', 'Payments', 'UPI hits a record 23.2 bn transactions in May')
st('end', 'Emirates NBD', 'Banking', 'Emirates NBD clears all approvals for RBL Bank')
st('psb', 'Public sector banks FY26', 'Banking', 'Public sector banks earn a record ₹1.98 lakh crore', 'feature',
   lede='Public sector banks posted a net profit of ₹1.98 lakh crore in FY26, the highest ever, on total business of ₹283.3 lakh crore. Gross advances grew 15.7% to ₹127 lakh crore. Gross NPA fell to 1.93% and net NPA to 0.39% at 31 March 2026, the lowest on record. DFS also set a Viability Plan 2.0 for regional rural banks, with 30 performance parameters.',
   nums=[('₹1.98 lakh cr', 'Net profit, record'), ('1.93%', 'Gross NPA'), ('0.39%', 'Net NPA'), ('₹283.3 lakh cr', 'Total business')], chart=['npa', 'viab'],
   trap='DFS also launched a Common Landing Portal for unclaimed financial assets with the PSB Alliance, under the line "Your Money, Your Right".')
st('insfdi', '100% FDI in insurance', 'Insurance', 'Insurance FDI goes to 100% on the automatic route')
st('bmip', 'Bharat Maritime Insurance Pool', 'Insurance', 'A $1.5 bn pool for ships comes with a $1.4 bn guarantee')
st('jan', 'Jan Suraksha schemes', 'Social security', 'Jan Suraksha schemes complete 11 years')

# ---------- 2 ----------
st('surplus', 'RBI surplus transfer', 'RBI', 'The RBI transfers a record ₹2,86,588.46 crore to the Centre', 'feature',
   lede='At its 623rd meeting in Mumbai on 22 May 2026, chaired by Governor Sanjay Malhotra, the RBI Central Board approved a surplus transfer of ₹2,86,588.46 crore to the Central Government for 2025-26, the highest ever; the year before it was ₹2.68 lakh crore. The board kept the Contingent Risk Buffer at 6.5% of the balance sheet, inside the revised Economic Capital Framework range of 4.5% to 7.5%, and moved ₹1,09,379.64 crore into it, against ₹44,861.70 crore a year earlier. The balance sheet grew 20.61% to ₹91,97,121.08 crore at 31 March 2026.',
   nums=[('₹2,86,588.46 cr', 'Surplus to the Centre'), ('6.5%', 'CRB, share of balance sheet'), ('₹1,09,379.64 cr', 'Transfer to the CRB'), ('20.61%', 'Balance sheet growth')], chart=['surplus', 'crb'],
   trap='Gross income rose 26.42% and spending before risk provisions rose 27.60%. Net income before risk provision and transfer to statutory funds was ₹3,95,972.10 crore.')
st('cet1', 'Quarterly profits in CET1', 'Capital', 'Banks may count quarterly profits in CET1 capital')
st('ifr', 'Investment Fluctuation Reserve', 'Reserves', 'Commercial banks no longer need an Investment Fluctuation Reserve', 'feature',
   lede='From 18 May 2026 the IFR requirement is discontinued for commercial banks and local area banks, and the balance as on 17 May 2026 moves below the line to the Statutory Reserve, General Reserve or Profit and Loss balance. The IFR is a buffer against a fall in the value of investments. Small finance banks, payments banks and RRBs still keep at least 2%, and urban and rural co-operative banks keep 5%.',
   nums=[('18 May 2026', 'Discontinued from'), ('2%', 'SFBs, payments banks, RRBs'), ('5%', 'UCBs, RCBs')], chart=['iftab'],
   trap='Foreign bank branches move the balance to statutory reserves kept in Indian books, or to remittable surplus retained in Indian books.')
st('coop', 'Co-operative bank directors', 'Co-operative banks', 'Co-operative bank directors face a 3-year cooling-off')
st('ccyb', 'Countercyclical capital buffer', 'Capital', 'The RBI keeps the countercyclical buffer switched off')
st('swap', 'buy/sell swap', 'Liquidity', 'The RBI runs a $5 billion, 3-year dollar swap')
st('fema', 'FEMA (Authorised Persons)', 'FEMA', 'New FEMA rules redraw who may deal in foreign exchange', 'feature',
   lede='The FEMA (Authorised Persons) Regulations, 2026, notified on 30 April 2026 and in force from Gazette publication on 6 May 2026, allow fresh authorisation in only three categories: AD Category-I, II and III. No fresh applications are taken from full-fledged money changers (FFMCs) apart from those already under process. Net worth must be at least ₹10 crore for AD Category-II and ₹2 crore for AD Category-III, and an applicant must be a company with at least 50% of its directors and KMPs experienced in financial services.',
   nums=[('3', 'Categories open to new authorisation'), ('₹25 lakh', 'Foreign trade cap per transaction, AD-II'), ('₹10 crore', 'Net worth, AD-II'), ('₹2 crore', 'Net worth, AD-III')], chart=['femat'],
   trap='An appeal against rejection or revocation must be filed within 45 calendar days; the Appellate Authority decides within 60 calendar days.')
st('recov', 'loan recovery conduct', 'Recovery', 'A draft would limit phone locking to loans 90 days overdue')
st('pillar3', 'Pillar 3 disclosures', 'Disclosure', 'A draft asks banks to keep Pillar 3 disclosures online for 10 years')
st('sigidx', 'Significant Indices', 'SEBI', 'A significant index is one tracked by over ₹20,000 crore of fund assets')
st('nomin', 'nomination in demat', 'SEBI', 'Nomination becomes mandatory for single demat accounts from 1 September')
st('aiadv', 'AI vulnerability-detection', 'SEBI', 'SEBI sets up a task force on AI cyber risks')
st('lag', '30-day lag', 'SEBI', 'Price data used for education must be 30 days old')
st('garuda', 'GARUDA for AIFs', 'SEBI', 'GARUDA proposes a 10-working-day launch for AIF schemes')
st('pfrda', 'NPS investment, retirement', 'Pensions', 'NPS funds can buy New Development Bank rupee bonds')
st('sanchay', 'NPS Sanchay and insider', 'Pensions', 'NPS Sanchay brings a simple pension plan to informal workers')

# ---------- 3 ----------
st('intlorg', 'International organisations and global events', 'World', 'India stays on the US Priority Watch List')
st('uae', 'India-UAE: energy', 'UAE', 'The UAE pledges $5 billion as India and the UAE sign energy deals', 'feature',
   lede='India and the UAE agreed cooperation on strategic petroleum reserves between ISPRL and ADNOC, and long-term LPG supply between IOCL and ADNOC. The UAE announced investments of $5 bn: $3 bn by Emirates NBD in RBL Bank, $1 bn by ADIA with NIIF in infrastructure and $1 bn by International Holding Company in Sammaan Capital. Cochin Shipyard and Drydocks World will set up a ship repair cluster at Vadinar in Gujarat under the Maritime Development Fund, and C-DAC and G42 will build an 8 exaflop supercompute cluster for the IndiaAI Mission.',
   nums=[('$5 bn', 'UAE investment pledged'), ('$3 bn', 'Emirates NBD in RBL Bank'), ('8 exaflop', 'Supercompute cluster'), ('3rd', 'UAE’s rank among India’s trade partners')], chart=['uae5'],
   trap='MAITRI stands for Master Application for International Trade and Regulatory Interface; it runs the India-UAE Virtual Trade Corridor.')
st('italy', 'India-Italy special', 'Diplomacy', 'India and Italy build a special strategic partnership')

# ---------- 4 ----------
st('sc', 'Supreme Court and judiciary', 'Courts', 'Supreme Court strength rises to 38 judges')
st('sports', 'National Sports Governance Rules', 'Sports law', 'New rules set up the National Sports Board and Tribunal')
st('labour', 'Final rules under all four', 'Labour', 'Final rules put all four labour codes to work', 'feature',
   lede='The Centre notified the final rules under all four labour codes through more than 30 Gazette notifications, after draft rules on 30 Dec 2025. The Code on Wages, the Industrial Relations Code, the Code on Social Security and the OSHWC Code replace 29 labour laws. The work week is capped at 48 hours, with up to 12 hours a day, overtime is paid at twice the normal rate, and every worker gets an appointment letter and one weekly rest day. Workers aged 40 and above get a free annual health check-up, and unorganised workers above 16 years must register with Aadhaar.',
   nums=[('29 → 4', 'Laws into codes'), ('48 hours', 'Work week cap'), ('2x', 'Overtime rate'), ('40+', 'Free health check-up')], chart=['codes', 'socsec'],
   trap='The Minister said ESIC beneficiaries rose from about 7 crore to about 15 crore, and maternity leave from 12 to 26 weeks.')
st('infra', 'Infrastructure and energy firsts', 'Infrastructure', 'India gets its 18th railway zone and a first hydrogen train route')
st('raj', 'Rajasthan and Gujarat industry', 'Rajasthan', 'Rajasthan gets its first semiconductor plant at Bhiwadi')
st('wild', 'Wildlife and heritage, May', 'Wildlife', 'India’s cheetah count reaches 53')

# ---------- 5 ----------
st('rbimou', 'RBI agreements with ECB', 'Agreements', 'The RBI signs central banking MoUs with the ECB and Vietnam')
st('stake', 'Bank and insurance stake deals', 'Deals', 'Kotak may hold up to 9.99% in three banks')
st('summits', 'Summits and ministerial', 'Summits', 'India hosts BRICS and Quad foreign ministers')
st('nordic', 'Third India-Nordic', 'Summit', 'Nordic countries pledge $100 bn at the Oslo summit')
st('appts', 'Appointments, May 2026', 'People', 'A new CDS, a new Navy chief and a new RBI deputy governor')
st('cm', 'New Chief Ministers', 'States', 'Who became Chief Minister after the 2026 elections',
   lede='Six Chief Ministers are named after the 2026 assembly elections: C. Joseph Vijay in Tamil Nadu, V. D. Satheesan in Kerala, Suvendu Adhikari in West Bengal, Himanta Biswa Sarma in Assam, N. Rangasamy in Puducherry and D K Shivakumar in Karnataka.')
st('qsafe', 'Q-SAFE', 'RBI', 'The RBI forms an eight-member committee on quantum security')

# ---------- 6 ----------
st('space', 'Space missions and firsts', 'Space', 'GalaxEye launches the first OptoSAR satellite')
st('missiles', 'Missile and weapon tests', 'Defence', 'India tests a 1,500 km hypersonic anti-ship missile and an Agni MIRV')
st('defplat', 'Defence platforms, deals', 'Defence', 'A new frigate, a new patrol vessel and the AMCA facility')
st('pragati', 'Exercise PRAGATI', 'Defence', 'The first Exercise PRAGATI draws 12 friendly nations to Meghalaya')
st('sportsres', 'Sports results, May 2026', 'Sport', 'India wins 10 medals as it hosts Asian weightlifting')
st('ipl', 'IPL 2026 and Indian highlights', 'Cricket', 'Royal Challengers Bengaluru win IPL 2026')

# ---------- 7 ----------
st('awards', 'Awards, May 2026', 'Awards', 'Modi gets the FAO Agricola Medal and Chandrayaan-3 wins the Goddard award')
st('rank', 'Rankings in the news', 'Rankings', 'IISc is 43rd in Asia and India’s passport is 78th')
st('migr', 'World Migration Report', 'Remittances', 'India receives $137.67 billion in remittances, the most in the world', 'feature',
   lede='The IOM’s World Migration Report 2026 says India received $137.67 bn in remittances in 2024, the world’s top receiver and the only country above $100 bn. India has led since 2010, when it received $53.48 bn. Mexico was next at $67.64 bn, then the Philippines, France and Pakistan. The US sent the most, $103.18 bn.',
   nums=[('$137.67 bn', 'India, 2024'), ('$100 bn', 'Only country above'), ('$53.48 bn', 'India in 2010'), ('$103.18 bn', 'US, top sender')], chart=['remit', 'send'],
   trap='There were 304 million international migrants in 2024, 3.7% of the world population. The IOM is headquartered in Geneva; its Director General is Amy Pope.')
st('srs', 'SRS Statistical Report', 'Data', 'India’s fertility rate is 1.9 and recorded crime is down 6%')
st('enclim', 'Energy and climate reports', 'Climate', 'The IEA expects record energy investment of $170 bn in India')

# ---------- 8 ----------
st('cab', 'Cabinet approvals', 'Schemes', 'ECLGS 5.0 and four other schemes win approval', 'feature',
   lede='A fifth round of the Emergency Credit Line Guarantee Scheme will help businesses and airlines hit by the West Asia crisis: additional credit of ₹2,55,000 crore, of which ₹5,000 crore is for airlines. The guarantee is 100% for MSMEs and 90% for non-MSMEs and airlines through NCGTC, with no fee, and loans run till 31 March 2027. Also approved: coal and lignite gasification at ₹37,500 crore, the BHAVYA industrial parks scheme at about ₹33,660 crore, the Mission for Cotton Productivity at ₹5,659.22 crore and SARTHAK-PDS for the ration system at ₹25,530 crore.',
   nums=[('₹2,55,000 cr', 'ECLGS 5.0 credit'), ('100% / 90%', 'Guarantee: MSMEs / others'), ('₹37,500 cr', 'Coal gasification'), ('100', 'Industrial parks, BHAVYA')], chart=['schemes', 'eclgs'],
   trap='BHAVYA stands for Bharat Audyogik Vikas Yojana. Its first phase takes up to 50 of the 100 parks, chosen by challenge.')
st('vbgramg', 'Viksit Bharat-G RAM G', 'Rural work', 'VB-G RAM G replaces MGNREGA with 125 days of work', 'feature',
   lede='The Viksit Bharat-G RAM G Act, 2025 comes into force on 1 July 2026 and repeals MGNREGA 2005; Parliament passed it in December 2025. The guaranteed work rises from 100 to 125 days a year, work must be given within 15 days of application, and delay compensation is 0.05% of unpaid wages a day. Administrative expenditure goes from 6% to 9%. The Centre’s provision for FY27 is ₹95,692.31 crore.',
   nums=[('125 days', 'Guaranteed work, was 100'), ('1 July 2026', 'Comes into force'), ('₹95,692.31 cr', 'FY27 provision'), ('15 days', 'To give work')], chart=['days', 'fund'],
   trap='The four work areas are water security, core rural infrastructure, livelihood infrastructure and extreme-weather mitigation.')
st('msp', 'Kharif MSP', 'Farm prices', 'Kharif MSP for 14 crops rises, with sunflower seed gaining most', 'feature',
   lede='The MSP of 14 Kharif crops was raised for 2026-27. The biggest absolute rises a quintal are sunflower seed ₹622, cotton ₹557, nigerseed ₹515 and sesamum ₹500. Sugarcane FRP for 2026-27 is ₹365 a quintal at 10.25% recovery. The Third Advance Estimates for 2025-26 put foodgrain output at a record 376.563 MT, up 5.3%.',
   nums=[('₹622', 'Sunflower seed rise'), ('₹365', 'Sugarcane FRP a quintal'), ('376.563 MT', 'Foodgrains, record'), ('90%', 'Monsoon forecast, of LPA')], chart=['mspr', 'grain'],
   trap='The IMD cut its 2026 monsoon forecast to 90% of the long period average; the LPA is 87 cm (1971-2020).')
