# November 2026 print edition: the authored story layer for tools/print-ca/build.py.
import json, os
_D = os.path.dirname(__file__)
NOTES = '/home/claude/nov/CA_November_2026.html'   # the November notes (join the project parts); read only
MONTH = 'November 2026'
PERIOD = '1–17 November'
OUTFILE = 'CA_November_2026_print'
COVER = dict(kicker='Section 1', title='The month prices broke the ceiling', lead='cpi',
             dek="Retail inflation crossed the RBI's 6% line and wholesale prices rose past 12%: what it means, and the numbers to keep.",
             stats=[('6.09%', 'CPI, October'), ('12.29%', 'WPI, October'), ('$479 bn', 'Exports, Apr–Sep'), ('25.47 bn', 'UPI payments, October')])
LEADS = {1: 'Inflation above 6% · record exports · GST ₹2.31 lakh crore · UPI records',
         2: 'RBI cash-transfer and cyber rules · SEBI depositary receipts for REITs · IRDAI four-layer motor cover',
         3: 'COP31 in Antalya · India re-elected ISA President · Kimberley Process chair',
         4: 'Bharatiya Vayuyan Niyam, 2026 · visa categories 13 → 9 · bullet train North Corridor',
         5: 'IORA Foreign Ministers in India · 49th ASEAN Summit, Manila · who got which post',
         6: 'Deep-sea mission to 6,000 m · Malabar 2026 · first Youth Olympic medals in swimming and wushu',
         7: 'Booker Prize 2026 · CCPI 2027: India 28th · QS Asia 2027: IIT Delhi 66th',
         8: 'Stand-Up India to March 2031 · VGF for energy storage · VISTAR for statistics',
         9: 'Key numbers · upcoming dates · flashcards'}
RAW_CHARTS = json.load(open(os.path.join(_D, 'nov2026_charts.json'), encoding='utf-8'))
DASH = open(os.path.join(_D, 'nov2026_dash.html'), encoding='utf-8').read().replace('<p class="chartlab">October at a glance (released in November)</p>', '')
# Full November 2026 print edition: authored story layer. Facts come only from the notes; numbers are validated.
# size: 'feature' (strip + chart + boxes) or 'short' (lede = the card's "In plain words" unless 'lede' is given).
# hook defaults to the card's Remember line; 'angle' defaults to the card's Exam angle.

SEC_INTRO = {
 1: 'Jobs, prices, money crossing the border and payments: the month\'s economy in four chapters.',
 2: 'The RBI rewrote its rulebooks on cash transfers, cyber security and priority lending; SEBI and IRDAI followed with their own changes.',
 3: 'Climate talks in Antalya, India\'s third term at the head of the International Solar Alliance, and a first meeting of BIMSTEC health ministers.',
 4: 'New laws and rules, record farm and solar numbers, a bullet train corridor to Guwahati and better health figures.',
 5: 'Two summits this month: the IORA foreign ministers in India and ASEAN leaders in Manila.',
 6: 'A crewed deep-sea dive planned for 2028, India-made AI models, new warships and exercises, and first medals at the Youth Olympics.',
 7: 'The Booker Prize, Blue Flag beaches, cleanliness awards, and the reports and rankings that carry India\'s position.',
 8: 'Eight schemes approved, extended or funded this month, from battery minerals to credit for micro-units.',
}

CHAPTERS = {
 1: [
  ('1.1', 'Jobs and factories', 'Two surveys from the statistics ministry: who is working, and how factories grew.', ['plfs', 'asi']),
  ('1.2', 'Prices are running hot', 'Both price gauges released in November point up: shop prices crossed the RBI\'s upper limit, and wholesale prices rose even faster.', ['cpi', 'wpi']),
  ('1.3', 'Money crossing the border', 'Indian firms are investing abroad faster than foreigners invest in India, exports hit a half-year record, and tax on imports lifted GST.', ['fla', 'exp', 'gst']),
  ('1.4', 'Pay, payments and small shops', 'A dearness allowance rise, another UPI record and an incentive scheme to take UPI into small towns.', ['da', 'upi', 'vyapaar']),
 ],
 2: [
  ('2.1', 'New rulebooks for moving money', 'The RBI rewrote its rules for cash transfers and payment-system security, drafted priority lending limits, eased service-trade reporting and set up a markets committee.', ['dmt', 'cyb', 'psl', 'fema', 'tccfm']),
  ('2.2', 'SEBI opens new doors', 'Depositary receipts for REITs and InvITs, a tax wish-list for the Budget, net settlement for mutual funds and a faster route to accredited investor status.', ['reit', 'ltcg', 'mfnet', 'accr']),
  ('2.3', 'Insurance rules', 'IRDAI cut a share-transfer fee and split motor insurance into four layers.', ['irfee', 'motor']),
 ],
 3: [
  ('3.1', 'India in the world\'s clubs', 'A UN restoration honour, a third ISA presidency, India\'s stand at COP31 and the Kimberley Process chair.', ['dolphin', 'isa', 'cop31', 'kp']),
  ('3.2', 'Neighbours', 'BIMSTEC health ministers met for the first time.', ['bimstec']),
 ],
 4: [
  ('4.1', 'New rules for citizens', 'A new aviation rulebook, a board for gig workers, EPFO and pension services, a simpler visa system and forest rights.', ['vayuyan', 'nssb', 'epfo', 'dlc', 'visa', 'fra']),
  ('4.2', 'Farms and villages', 'Complaint rules for the rural jobs scheme, the winter fertiliser subsidy and a record horticulture harvest.', ['ramg', 'nbs', 'horti']),
  ('4.3', 'Rails, chips and power', 'A bullet train corridor to Guwahati, chip-making support, green hydrogen deals, solar growth and an LPG cavern.', ['bullet', 'semicon', 'gh2', 'solar', 'lpg']),
  ('4.4', 'Health and heritage', 'A national museum in North and South Block, the trade fair, falling TB deaths and lower out-of-pocket health spending.', ['museum', 'iitf', 'tb', 'nha']),
 ],
 5: [
  ('5.1', 'Summits', 'India hosts the Indian Ocean Rim ministers while ASEAN leaders meet in Manila.', ['iora', 'asean']),
 ],
 6: [
  ('6.1', 'Deep sea and AI', 'A crewed dive to 6,000 m by 2028 and three Indian AI models.', ['deepsea', 'indiaai']),
  ('6.2', 'Defence', 'A new path for Agniveers, eight new corvettes, production targets for 2029 and a busy month of exercises.', ['tiger', 'agniveer', 'corvette', 'deftarget', 'exercises']),
  ('6.3', 'Sports', 'Firsts for India at the Youth Olympic Games in Dakar.', ['yog']),
 ],
 7: [
  ('7.1', 'Awards and honours', 'From the Booker to Blue Flag beaches, the Memory of the World register and the national sports awards.', ['booker', 'blueflag', 'infosys', 'mowcap', 'swachh', 'sportsaw']),
  ('7.2', 'Reports and rankings', 'Gold demand, the climate adaptation gap, India\'s climate rank, renewables outlook and Asian universities.', ['gold', 'adapt', 'ccpi', 'iea', 'qs']),
 ],
 8: [
  ('8.1', 'Money for minerals, storage, statistics and courts', 'Four Cabinet approvals with outlays and five-year periods.', ['crit', 'vgf', 'vistar', 'ftsc']),
  ('8.2', 'Credit for small businesses', 'A subsidy release under PMEGP and two schemes extended to March 2031.', ['pmegp', 'standup', 'cgfmu']),
 ],
}

S = {}
def st(key, card, tag, h, size='short', **kw):
    S[key] = dict(card=card, tag=tag, h=h, size=size, **kw)

# ---------- Section 1 ----------
st('plfs', 'PLFS quarterly bulletin, July', 'Jobs', 'Unemployment eases to 5.1%', 'feature',
   lede='The Periodic Labour Force Survey, run by the National Statistics Office, measures who is working and who is looking for work. For July to September 2026, unemployment among people aged 15 and above fell to 5.1%, from 5.4% in the previous quarter. More people joined the labour force, and villages had lower unemployment than the national average.',
   nums=[('5.4 → 5.1%', 'Unemployment rate'), ('4.3%', 'Rural unemployment'), ('55.5%', 'LFPR, overall'), ('52.7%', 'WPR, overall')],
   chart=['plfs'], trap='LFPR counts people working or looking for work; WPR counts only those working. So WPR is always the smaller figure.')
st('asi', 'Annual Survey of Industries (ASI) 2024-25', 'Industry', 'Five states make over half of India\'s factory output')
st('cpi', 'Retail inflation rises to 6.09%', 'Inflation · retail', "Shop prices cross the RBI's 6% red line", 'feature',
   lede="The RBI is asked to keep retail inflation at 4%, with room to move between 2% and 6%. In October 2026 it reached 6.09%, up from 5.54% in September. That is the first time in two years it has gone above the band, and the highest reading since October 2024. Villages felt it more than cities, and food prices rose faster still.",
   nums=[('6.09%', 'CPI, October'), ('5.54%', 'CPI, September'), ('8.94%', 'Food inflation'), ('6.63 / 5.41', 'Rural / urban %')],
   chart=['gauge', 'cpiw'],
   hook='"Six-oh-nine breaks the six." The band is 4 ± 2, so 6 is the ceiling; 6.09 is just over it.',
   trap="The new CPI's base year is 2024 and it prices 358 items (was 299). Food's weight is 36.75%, not the old basket's figure.")
st('wpi', 'Wholesale price inflation rises to 12.29%', 'Inflation · wholesale', 'Wholesale prices rise twice as fast as shop prices', 'feature',
   lede='The wholesale price index tracks prices at the factory gate and the mandi, before goods reach a shop. It rose 12.29% in October from a year earlier, up from 11.39% in September. Manufactured goods make up almost two-thirds of the index, so factory goods move it most.',
   nums=[('12.29%', 'WPI, October'), ('11.39%', 'WPI, September'), ('957', 'Items priced'), ('2022-23', 'Base year')],
   chart=['wpiw'], hook='"Twelve wholesale, six retail": October\'s WPI is about double the CPI.',
   trap="WPI's base is 2022-23; CPI's is 2024. WPI is compiled by the Office of the Economic Adviser in DPIIT, not by MoSPI.")
st('fla', 'RBI census on foreign liabilities', 'Investment', 'Indian companies are buying abroad faster than the world buys into India', 'feature',
   lede="Every year the RBI counts how much foreigners have invested in Indian companies and how much Indian companies have invested abroad. In 2025-26 the outward side grew faster. So for every one rupee Indian firms hold abroad, foreigners now hold 4.2 rupees in India, down from 5.5. Most outward money goes to Singapore, the UAE and the USA.",
   nums=[('5.5 → 4.2', 'FDI ÷ ODI ratio'), ('16.5%', "USA's share of FDI"), ('50.1%', 'FDI in manufacturing'), ('over 50%', 'ODI to top 3 places')],
   chart=['ratio', 'fdi'], hook='"U-M-S-U": USA, Mauritius, Singapore, UK, the order of FDI sources.',
   trap='A falling ratio does not mean FDI fell. It means Indian investment abroad grew faster.')
st('exp', 'Exports hit a record $479 billion', 'Trade', 'A record half-year: exports reach $479 billion', 'feature',
   lede="Between April and September 2026 India sold $479 billion of goods and services abroad, the most ever for those six months. Goods brought in $259.71 billion and services $219.27 billion. Electronics was the star, up 44%, led by smartphones. A string of trade deals signed since 2021 opens more markets.",
   nums=[('$479.0 bn', 'Total exports'), ('+18.4%', 'Goods growth'), ('+44%', 'Electronics'), ('$719.55 bn', 'Forex reserves')],
   chart=['ftas'], hook='"479 = 259.71 + 219.27": goods first, services second.',
   trap='The UK deal is a CETA (July 2025); the EFTA deal is a TEPA (March 2024); Australia is an ECTA.')
st('gst', 'GST collections, October 2026', 'Tax', 'Tax on imports lifts GST to ₹2.31 lakh crore',
   lede='Gross GST collected in October 2026 rose 22.9% from a year earlier to ₹2.31 lakh crore. Domestic collections grew 15.8%, but tax on imports jumped 42.2%. After refunds, net GST was ₹2.03 lakh crore.',
   trap='Gross 2.31, net 2.03 lakh crore: do not mix them. The GST Council comes from the 101st Amendment Act, 2016.')
st('da', 'DA and DR raised 3%', 'Pay', 'Dearness allowance goes up to 63%')
st('upi', 'UPI in October 2026', 'Payments', 'UPI moves over ₹1 lakh crore a day for the first time', 'feature',
   lede='October 2026 was UPI\'s biggest month on both counts. It handled 25.47 billion payments, beating the August record of 24.51 billion, and moved ₹31.53 lakh crore, the first month above ₹30 lakh crore. On an average day it carried ₹1,01,707 crore, crossing ₹1 lakh crore a day for the first time.',
   nums=[('25.47 bn', 'Transactions'), ('₹31.53 lakh cr', 'Value'), ('₹1,01,707 cr', 'Average a day'), ('822 mn', 'Payments a day')],
   chart=['upid'], trap='The previous volume record was August 2026 (24.51 bn); the previous value high was May 2026 (₹29.90 lakh crore). They are different months.')
st('vyapaar', 'UPI Vyapaar Saksham', 'Payments', 'NPCI pays banks to put UPI in small-town shops')

# ---------- Section 2 ----------
st('dmt', 'RBI consolidates Domestic Money Transfer', 'RBI · payments', 'Same cash limits, tighter checks for sending money home', 'feature',
   lede="Many workers send money to their families in cash, through a bank branch, a business correspondent or an ATM. On 11 November the RBI put all its rules for this into one set of directions. The money limits did not change. What changed is the safety net: every sender must now register with a mobile number and a valid KYC document.",
   chart=['dmt'], hook='"50, 5, 10, 25": branch NEFT ₹50,000; cash in ₹5,000; cash out ₹10,000; monthly cap ₹25,000.',
   trap='Card-to-card transfers are outside these directions.')
st('cyb', 'consolidated cyber security rules for payment system operators', 'RBI · cyber security', 'Six hours to tell the RBI when a payment system is attacked', 'feature',
   lede="Payment companies that are not banks, such as wallet and card-network operators, got one combined cyber security rulebook on 5 November. If they suffer an attack, an outage or an internal fraud, they must report it to the RBI within six hours. Large and medium operators must follow it at once; small ones have until April 2028.",
   chart=['cyber'], hook='"6 to report, 12 to cool": six hours to report, twelve hours\' wait after a change of mobile or email.',
   trap='Cyber incidents also go to CERT-In, not only to the RBI.')
st('psl', 'RBI draft priority sector lending', 'RBI · lending', 'How big a loan can be and still count as priority lending',
   lede='On 5 November the RBI released draft directions that bring all its priority sector lending instructions together, with a separate draft for commercial banks, small finance banks, local area banks and regional rural banks. Each draft sets a size limit per category.',
   hook='"4, 4, 4, then 100": ₹4 crore for each farm-loan type, ₹100 crore for farm infrastructure.')
st('fema', 'RBI eases reporting for small service exporters', 'RBI · FEMA', 'Less paperwork for selling services abroad')
st('tccfm', 'Technical Consultative Committee for Financial Markets', 'RBI · markets', 'Seven market experts to advise the RBI every quarter')
st('reit', 'SEBI opens depositary receipts for REITs', 'SEBI · markets', 'REIT and InvIT units can now trade abroad from GIFT City')
st('ltcg', 'SEBI seeks LTCG relief', 'SEBI · tax', 'SEBI asks the Budget to drop LTCG tax for foreign investors',
   trap='LTCG on equity came back in 2018-19 at 10% above ₹1 lakh; since 23 Jul 2024 it is 12.5% above ₹1.25 lakh.')
st('mfnet', 'SEBI lets mutual fund schemes net fund', 'SEBI · mutual funds', 'Mutual funds will settle only the net amount from April 2027',
   trap='Netting is within one scheme only, not across schemes of the same fund; FPIs got a similar rule earlier, on 24 Apr 2026.')
st('accr', 'fund and portfolio managers can now grant accredited', 'SEBI · investors', 'Fund managers can now accredit their own investors')
st('irfee', 'IRDAI master circular: share-transfer fee', 'IRDAI', 'Insurers pay 80% less to get a share transfer approved')
st('motor', 'four-layer motor insurance policy', 'IRDAI · motor', 'Motor insurance splits into four layers from 15 December', 'feature',
   lede='From 15 December 2026, insurance for private cars and two-wheelers must be sold in four separate layers. Only the first, third-party liability, is compulsory; the other three are options the buyer can choose. Every general insurer must use the same policy wording, a customer option form and a customer information sheet.',
   nums=[('4', 'Layers'), ('1', 'Compulsory layer'), ('15 Dec 2026', 'Start date')],
   chart=['motor'], trap='Only third-party cover is compulsory, subject to the rule on compulsory personal accident cover for owner-drivers.')

# ---------- Section 3 ----------
st('dolphin', 'Ganges river dolphin programme a World Restoration Flagship', 'UNEP', 'India\'s river dolphin plan named a UN restoration flagship')
st('isa', 'International Solar Alliance: India re-elected', 'ISA', 'India leads the Solar Alliance for a third term')
st('cop31', 'COP31 (UNFCCC), Antalya', 'Climate', 'At COP31, India asks for climate finance that does not create debt',
   trap='COP31 is in Antalya, Turkiye; COP30 was in Belém, Brazil (2025).')
st('kp', 'India chairs the Kimberley Process', 'Diamonds', 'India chairs the Kimberley Process for the third time')
st('bimstec', 'First BIMSTEC Health Ministers', 'BIMSTEC', 'BIMSTEC health ministers meet for the first time, in Colombo')

# ---------- Section 4 ----------
st('vayuyan', 'Bharatiya Vayuyan Niyam', 'Aviation', 'A new flying rulebook replaces the rules of 1937')
st('nssb', 'National Social Security Board', 'Labour', 'A national board for gig and platform workers')
st('epfo', 'EPFO 74th Foundation Day', 'EPFO', 'PF on WhatsApp, and small dormant accounts paid out automatically')
st('dlc', 'Digital Life Certificate campaign', 'Pensions', 'Pensioners prove they are alive by face scan, all November')
st('visa', 'Visa regime rationalised', 'Visas', 'Fewer visa types, and the tourist visa becomes a visitor visa')
st('fra', 'Forest Rights Act: 25.42 lakh titles', 'Tribal affairs', 'Forest rights claims go fully online')
st('ramg', 'VB–G RAM G Grievance Redressal Rules', 'Rural jobs', 'Rural job complaints: enquiry in 7 days, settled in 15')
st('nbs', 'Nutrient Based Subsidy for P&K', 'Fertilisers', '₹62,370 crore to keep winter fertiliser affordable')
st('horti', 'Horticulture output to hit a record', 'Horticulture', 'A record 386.9 million tonnes of fruit, vegetables and flowers', 'feature',
   lede='India\'s horticulture harvest for 2025-26 is estimated at a record 386.9 million tonnes, up 4.36% on the year, even though less land was used. Vegetables are the largest part, but flowers grew fastest, by 14.45%.',
   nums=[('386.9 mn t', 'Total output'), ('+4.36%', 'Growth'), ('14.45%', 'Flowers, fastest'), ('297.21 lakh ha', 'Area (lower)')],
   chart=['horti'], trap='These are Third Advance Estimates for 2025-26, not final figures.')
st('bullet', 'Bullet train North Corridor', 'Railways', 'A bullet train corridor from Delhi to Guwahati', 'feature',
   lede='The Prime Minister has approved a high-speed rail corridor from Delhi to Guwahati, running through Uttar Pradesh, Bihar and Siliguri in West Bengal. Delhi to Agra would take 59 minutes. India\'s first bullet train, Mumbai to Ahmedabad, is 508 km long and still being built.',
   chart=['bullet'])
st('semicon', 'Semicon 2.0 portal launched', 'Electronics', 'Chip mission phase two opens for applications')
st('gh2', 'National Green Hydrogen Mission: offtake', 'Energy', 'Green hydrogen deals reach 11% of the 2030 target', 'feature',
   lede='Indian companies have signed contracts to sell 5,55,610 tonnes of green hydrogen a year. That is about 11% of the national target of 5 million tonnes a year by 2030. Most of it, over 70%, is meant for export, and 18 of the 23 contracts were signed in 2026.',
   nums=[('5.5 lakh t', 'Signed a year'), ('11%', 'Of 2030 target'), ('over 70%', 'For export'), ('₹19,744 cr', 'Mission outlay')],
   chart=['gh2'])
st('solar', "India's solar growth", 'Solar', 'Solar grows from 3 GW in 2014 to about 175 GW', 'feature',
   lede='India had 3 GW of solar power in 2014. By 31 October 2026 it had about 175 GW. In 2025 alone it added 37 GW, more than the United States, which made India the world\'s second-largest solar growth market.',
   nums=[('about 175 GW', 'Solar installed'), ('37 GW', 'Added in 2025'), ('34.97 GW', 'Rooftop'), ('308.03 GW', 'Non-fossil total')],
   chart=['solar'], trap='Non-fossil capacity (308.03 GW) includes 8.78 GW of nuclear; renewable alone is 299.25 GW.')
st('lpg', "India's largest underground LPG storage", 'Energy', 'India\'s largest underground LPG store opens at Mangaluru')
st('museum', 'Yuge Yugeen Bharat Museum', 'Culture', 'North and South Block to become a ₹3,230 crore national museum')
st('iitf', '45th India International Trade Fair', 'Trade fair', 'The 45th trade fair opens at Bharat Mandapam')
st('tb', 'WHO Global TB Report 2026', 'Health', 'TB deaths in India fall faster than the world average', 'feature',
   lede='The World Health Organization\'s 2026 TB report says deaths from tuberculosis in India fell 38% between 2015 and 2025, against 35% for the world. Deaths dropped from 28 to 18 for every lakh people, and 94% of patients with drug-susceptible TB are treated successfully.',
   nums=[('38%', 'Fall in deaths, India'), ('35%', 'Fall, world'), ('28 → 18', 'Deaths per lakh'), ('94%', 'Treatment success')],
   chart=['tb'])
st('nha', 'National Health Accounts 2023-24', 'Health', 'Households pay a smaller share of the health bill')

# ---------- Section 5 ----------
st('iora', 'India hosts IORA Foreign Ministers', 'IORA', 'India hosts the Indian Ocean Rim foreign ministers')
st('asean', '49th ASEAN Summit, Manila', 'ASEAN', 'ASEAN leaders meet in Manila for the 49th summit')

# ---------- Section 6 ----------
st('deepsea', 'First human deep-sea mission', 'Deep Ocean Mission', 'Three Indians to dive 6,000 m by 2028')
st('indiaai', 'IndiaAI Mission: foundation models', 'AI', 'Three India-made AI models, two that run on phones')
st('tiger', 'Exercise Tiger Triumph 2026', 'Exercise', 'Tiger Triumph: NDRF joins the India–US drill for the first time')
st('agniveer', 'Second Tour of Duty', 'Agnipath', 'Agniveers get a second chance: two more years', 'feature',
   lede='Under the Agnipath scheme, Agniveers serve four years and 25% are then offered regular service on merit. The Cabinet has now given the other 75% an option to serve two more years, called the Second Tour of Duty. After six years they can be enrolled as regular soldiers if they are willing and meet the selection criteria.',
   chart=['agni'], trap='The 25% figure is for regular service after four years; the Second Tour is optional, for the remaining 75%.')
st('corvette', 'Next Generation Corvettes', 'Navy', 'Eight Navy-designed corvettes ordered from two shipyards')
st('deftarget', 'Targets: defence production', 'Defence industry', 'Defence targets for 2029: make ₹3 lakh crore, sell ₹50,000 crore abroad', 'feature',
   lede='Defence Minister Rajnath Singh has set two targets for 2029: defence production of ₹3 lakh crore and exports of ₹50,000 crore. In 2025-26 India produced a record ₹1.78 lakh crore and exported a record ₹38,424 crore, to more than 80 countries.',
   nums=[('₹1.78 lakh cr', 'Production, 2025-26'), ('₹38,424 cr', 'Exports, 2025-26'), ('62.66%', 'Export growth'), ('₹7.85 lakh cr', 'Defence budget 2026-27')],
   chart=['defx'])
st('exercises', 'Exercises: Malabar 2026', 'Exercises', 'Malabar turns 30; Sea Vigil guards the whole coast')
st('yog', 'Dakar 2026 Youth Olympic Games', 'Youth Olympics', 'First Indian medals in swimming and wushu, in Dakar')

# ---------- Section 7 ----------
st('booker', 'Booker Prize 2026', 'Booker Prize', 'At 81, M. John Harrison is the oldest Booker winner')
st('blueflag', 'Blue Flag 2026-27', 'Beaches', 'Maharashtra gets its first three Blue Flag beaches')
st('infosys', 'Infosys Prize 2026', 'Science prize', 'Six researchers under 40 win the Infosys Prize')
st('mowcap', 'Mahabharata, Arthashastra and Rajatarangini', 'UNESCO', 'Three ancient manuscripts join UNESCO\'s Asia-Pacific register')
st('swachh', 'Swachh Survekshan Awards', 'Cleanliness', 'Navi Mumbai tops the cleanest-city league')
st('sportsaw', 'National Sports Awards 2025', 'Sports awards', 'No Khel Ratna this year; 17 Arjuna awards')
st('gold', 'World Gold Council: India gold demand', 'Gold', 'Indians buy less gold but pay more for it', 'feature',
   lede='Between July and September 2026 Indians bought 162.5 tonnes of gold, 29% less by weight than a year earlier. But because prices were higher, they spent 3% more, ₹2.42 lakh crore. India is still the second-largest market for gold bars and coins, after China.',
   nums=[('162.5 t', 'India demand, Q3'), ('−29%', 'By weight'), ('+3%', 'By value'), ('21%', 'Share of world bar and coin demand')],
   chart=['cbgold'], trap='Basic customs duty on gold rose from 5% to 10%; the overall customs duty is 15%.')
st('adapt', 'UNEP Adaptation Gap Report 2026', 'Climate finance', 'Poor countries need $305 billion a year to adapt; they got $28.2 billion', 'feature',
   lede='The UN environment agency says developing countries need about $305 billion a year for it, but rich countries gave only $28.2 billion in 2024. Even the promise to triple funding to $120 billion a year by 2035 would leave a gap of over two-thirds.',
   chart=['adapt'], hook='"305 needed, 28.2 given; 120 promised, 420 needed by 2035."')
st('ccpi', 'Climate Change Performance Index 2027', 'Climate ranking', 'India slips five places to 28th on climate performance')
st('iea', 'Energy and climate reports', 'Energy reports', 'IEA: India second only to China in new renewable power')
st('qs', 'QS Asia University Rankings 2027', 'Universities', 'IIT Delhi leads India at 66th in Asia')

# ---------- Section 8 ----------
st('crit', 'CAPEX Support Scheme for critical mineral', 'Critical minerals', '₹2,814 crore for four lithium and nickel plants')
st('vgf', 'Viability Gap Funding for grid-scale energy storage', 'Energy storage', '₹14,500 crore to add 92 GWh of power storage', 'feature',
   lede='The government will pay ₹14,500 crore as viability gap funding to add 92 GWh of grid-scale storage by 2030-31, mostly pumped hydro and big batteries. That is 170% of the storage the grid has today.',
   nums=[('₹14,500 cr', 'Support'), ('92 GWh', 'New storage'), ('₹97,600 cr', 'Investment expected'), ('40%', 'Domestic content, BESS')],
   chart=['vgf'])
st('vistar', 'VISTAR scheme', 'Statistics', 'VISTAR: ₹4,371 crore to modernise official statistics')
st('ftsc', 'Fast Track Special Courts scheme extended', 'Justice', 'Fast-track courts for rape and POCSO cases run to 2031')
st('pmegp', 'PMEGP: ₹1,000 crore margin money', 'PMEGP', '₹1,000 crore subsidy for 11,333 new micro-enterprises')
st('standup', 'Stand-Up India Scheme to March 2031', 'Stand-Up India', 'Stand-Up India extended to 2031 for 2.5 lakh more entrepreneurs')
st('cgfmu', 'Credit Guarantee Fund for Micro Units', 'Mudra', 'Mudra loan guarantees continue, and get cheaper')

COVER_LINES = [('Section 1 · Payments', 'UPI moves over ₹1 lakh crore a day for the first time', 'upi'),
               ('Section 4 · Railways', 'A bullet train corridor from Delhi to Guwahati', 'bullet'),
               ('Section 4 · Visas', 'Fewer visa types, and the tourist visa becomes a visitor visa', 'visa'),
               ('Section 7 · Climate', 'India slips five places to 28th on climate performance', 'ccpi')]
