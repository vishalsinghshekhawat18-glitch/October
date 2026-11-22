# August 2026 print edition: the authored story layer for tools/print-ca/build.py.
# Facts only from the August notes; every number written here is checked against them.
NOTES = '../../../archive/current-affairs/CA_August_2026.html'
MONTH = 'August 2026'
PERIOD = '1–31 August'
OUTFILE = 'CA_August_2026_print'

COVER = dict(kicker='Section 2', title='Rates hold, rules tighten', lead='mpc',
             dek='The RBI keeps the repo rate at 5.25%, trims its inflation view, and issues rules on recovery, rates and supervision: what changed, and the numbers to keep.',
             stats=[('5.25%', 'Repo rate'), ('4.45%', 'CPI, July'), ('9.78%', 'WPI, July'), ('39', 'Medals, CWG')])
COVER_LINES = [('Section 8 · Welfare', 'Jan Dhan at twelve: 59.09 crore accounts', 'jandhan'),
               ('Section 8 · Energy', 'A ₹23,731 crore push for compressed biogas', 'gobar'),
               ('Section 6 · Sports', 'India fourth at the Commonwealth Games with 39 medals', 'cwg'),
               ('Section 7 · Rankings', 'India 176th of 177 on the environment index', 'epi')]
LEADS = {1: 'CPI 4.45% · WPI 9.78% · exports · UPI turns ten · LIC stake sale',
         2: 'Repo rate 5.25% · loan recovery rules · SEBI closing auction · NPS charges',
         3: 'IMF · EU carbon border tax · Uzbekistan visit',
         4: 'Tribunals Bill · Independence Day · sugar price · Ramsar sites reach 101',
         5: 'BRICS Summit · Jio Credit and Bharti Life deals · appointments',
         6: 'PRAHAAR · SeaGuardian lease · hockey World Cup · Commonwealth Games',
         7: 'COSPAR medal · gallantry awards · EPI 2026 · Hurun family businesses',
         8: 'Jan Dhan · e-Shram · biogas · Samudra Manthan · phones',
         9: 'Key numbers · upcoming dates · flashcards'}
DASH = '''<table class="score dash"><thead><tr><th>Indicator</th><th>Before</th><th>Now</th><th>Trend</th></tr></thead><tbody>
<tr><td>Repo rate</td><td>5.25%</td><td>5.25%<small> 62nd MPC</small></td><td>■ unchanged</td></tr>
<tr><td>WPI (wholesale) inflation</td><td>9.87% June</td><td>9.78% July</td><td>▼ easing</td></tr>
<tr><td>Industrial production (IIP)</td><td>7.3% June</td><td>6.7% July</td><td>▼ slower</td></tr>
<tr><td>Core industries</td><td>6.0% June</td><td>5.4% July</td><td>▼ slower</td></tr>
<tr><td>Unemployment (PLFS, 15+)</td><td>5.5% June</td><td>5.1% July</td><td>▼ lower</td></tr>
</tbody></table>'''

def make_charts(hbar, steps, table_chart):
    return {
     'trade': hbar('India merchandise trade, April–July 2026-27 ($ bn)', [('Imports', 365.85, '365.85'), ('Exports', 316.42, '316.42'), ('Deficit', 49.43, '49.43')], 365.85, hi=2),
     'jandhan': hbar('Jan Dhan accounts (crore)', [('2015', 14.72, '14.72'), ('19 Aug 2026', 59.09, '59.09')], 59.09, hi=1),
     'cwg': hbar('Commonwealth Games 2026: total medals', [('Australia', 171, '171'), ('England', 110, '110'), ('Canada', 62, '62'), ('India', 39, '39')], 171, hi=3),
     'cbg': steps('CBG obligation for city gas companies', [('3%', 'FY 2026-27'), ('4%', 'FY 2027-28'), ('5%', 'from FY 2028-29')]),
     'epi': hbar('Environmental Performance Index 2026: score', [('Estonia', 74.79, '74.79'), ('India', 22.46, '22.46')], 74.79, hi=1),
     'sam': hbar('Where the ₹84,084 crore goes (₹ crore)', [('Deepwater wells', 43200, '43,200'), ('Seismic data', 28534, '28,534'), ('Common hubs', 10000, '10,000'), ('Manufacturing zones', 2000, '2,000'), ('Monitoring', 350, '350')], 43200, hi=0),
     'ship': hbar('India share of global ship recycling (%)', [('2024', 30.1, '30.1'), ('2025', 35.4, '35.4')], 35.4, hi=1),
    }

SEC_INTRO = {
 1: 'Prices and output, trade and tax, and a busy month for banks, payments and insurers.',
 2: 'The RBI held its rate and issued rules on recovery, lending and supervision; SEBI changed how the trading day ends.',
 3: 'The IMF, the EU carbon border tax and a state visit abroad.',
 4: 'New Bills and Acts, the Independence Day announcements, farm prices, wildlife and the states.',
 5: 'Deals, conferences and appointments.',
 6: 'A chip plant, space plans, a counter-terrorism policy, drones on lease and a big month in sport.',
 7: 'Honours, rankings and reports.',
 8: 'Schemes of the month, from Jan Dhan to offshore oil and gas.',
}
CHAPTERS = {
 1: [
   ('1.1', 'Prices, output and the economy', 'Retail and wholesale inflation, factory output, jobs and the size of the economy.', ['k000', 'cpi', 'k002', 'k003', 'k004', 'k005', 'k006']),
   ('1.2', 'Trade, tax and pay', 'Exports, a window for foreign assets, trade rule changes and a proposed wage ceiling.', ['k007', 'trade', 'k009', 'k010', 'k011']),
   ('1.3', 'Banks and payments', 'UPI turns ten, rural banks earn a record profit and new notes go to trial.', ['k012', 'k013', 'k014', 'k015', 'k016', 'k017', 'k018', 'k019', 'k020', 'k021']),
   ('1.4', 'Insurance', 'Tighter rules for intermediaries, a government stake sale in LIC and two penalised insurers.', ['k022', 'k023', 'k024']),
 ],
 2: [
   ('2.1', 'RBI', 'The repo rate held, new recovery conduct rules, the swap facility and a large consolidation of rules.', ['k025', 'k026', 'k027', 'mpc', 'k029', 'k030', 'k031', 'k032', 'k033', 'k034', 'k035']),
   ('2.2', 'SEBI', 'A closing auction, resilience scoring for market bodies and easier rules for bonds and trusts.', ['k036', 'k037', 'k038', 'k039', 'k040', 'k041', 'k042', 'k043', 'k044', 'k045', 'k046']),
   ('2.3', 'Other regulators and laws', 'Piped gas, the Supreme Court on mule accounts, pension charges and the data protection law.', ['k047', 'k048', 'k049', 'k050', 'k051']),
 ],
 3: [
   ('3.1', 'International bodies', 'The IMF, the EU carbon border tax and a month of world news.', ['k052', 'k053', 'k054', 'k055']),
   ('3.2', 'India and the world', 'A state visit to Uzbekistan.', ['k056']),
 ],
 4: [
   ('4.1', 'Laws and institutions', 'Tribunals, courts, schools, new Acts and what the Prime Minister announced on Independence Day.', ['k057', 'k058', 'k059', 'k060', 'k061', 'k062', 'k063', 'k064', 'k065', 'k066', 'k067', 'k068', 'k069', 'k070']),
   ('4.2', 'Farms and food', 'Sugar prices and a round of agriculture items.', ['sugar', 'k072']),
   ('4.3', 'Ships, roads and power', 'Ship recycling, a driver-owned taxi platform, road safety, non-fossil power and tap water.', ['ship', 'k074', 'k075', 'k076', 'k077', 'k078', 'k079']),
   ('4.4', 'Wildlife and wetlands', 'The elephant count and a new Ramsar site.', ['k080', 'k081']),
   ('4.5', 'States and UTs', 'Ladakh and Rajasthan.', ['k082', 'k083']),
 ],
 5: [
   ('5.1', 'Deals', 'Defence and business agreements and two big acquisitions.', ['k084', 'k085']),
   ('5.2', 'Conferences', 'BRICS meetings and summits ahead.', ['k086', 'k087']),
   ('5.3', 'Appointments', 'Who took which post this month.', ['k088', 'k089']),
 ],
 6: [
   ('6.1', 'Science and technology', 'A chip plant, farm science firsts and space plans.', ['k090', 'k091', 'k092', 'k093']),
   ('6.2', 'Defence', 'A counter-terrorism policy and two more leased drones.', ['prahaar', 'mq9b']),
   ('6.3', 'Sports', 'Hockey, badminton, the Commonwealth Games and chess.', ['k096', 'k097', 'cwg', 'k099']),
 ],
 7: [
   ('7.1', 'Awards', 'Science, sports and gallantry honours.', ['k100', 'k101']),
   ('7.2', 'Rankings and reports', 'Brands, family businesses, AI patents and the environment index.', ['k102', 'hurun', 'epi']),
 ],
 8: [
   ('8.1', 'Welfare and jobs', 'Jan Dhan at twelve, e-Shram, the employment scheme, PM-KISAN and Ayushman Bharat.', ['jandhan', 'eshram', 'vbry', 'pmkisan', 'k114']),
   ('8.2', 'Industry, trade and energy', 'Containers, biogas, urea, offshore oil and gas and phones.', ['k107', 'gobar', 'k110', 'samudra', 'mobile']),
 ],
}
S = {}
def st(key, card, tag, h, size='short', **kw): S[key] = dict(card=card, tag=tag, h=h, size=size, **kw)
st('k000', 'PLFS quarterly bulletin April–June 2026', 'Jobs', 'Labour force survey: the April–June 2026 picture', 'short')
st('cpi', 'CPI July 2026 (base 2024=100): 4.45%', 'Inflation', 'Retail inflation 4.45% in July', 'feature', lede="India's retail inflation for July 2026 was 4.45%, with rural prices rising 4.84% and urban prices 3.96%. The new CPI series uses 2024 as its base year and a basket of 358 items, up from 299, with food and beverages the heaviest group at 36.75%.", nums=[('4.45%', 'CPI, July 2026'), ('4.84%', 'Rural'), ('3.96%', 'Urban'), ('358', 'Items in the basket')], trap='The older basket had 299 items; the new base year is 2024.')
st('k002', 'WPI July 2026: 9.78%; new series with base 2022–23', 'Inflation', 'Wholesale inflation 9.78% on a new base year', 'short')
st('k003', 'IIP July 2026: 6.7%; Index of Core Industries July 2026: 5.4%', 'Industry', 'Factory output up 6.7%, core industries up 5.4%', 'short')
st('k004', 'QBUSE April–June 2026: 8.67 crore unincorporated establishments', 'Business', '8.67 crore small unincorporated businesses counted', 'short')
st('k005', 'Public finance and rankings: debt-to-GDP 58.2% in FY26; India sixth-largest economy at $3.92 trillion', 'Economy', 'Debt at 58.2% of GDP; India sixth-largest economy', 'short')
st('k006', 'Economy: PPI deflator for GDP, PLFS July 2026 at 5.1%, windfall tax cut, Japan debt', 'Economy', 'A new price index for GDP, jobless rate at 5.1%', 'short')
st('k007', 'GeM completes 10 years (9 August 2016 launch)', 'Procurement', 'GeM completes ten years', 'short')
st('trade', "India's trade April–July 2026-27: exports $316.42 bn, deficit $49.43 bn", 'Trade', 'Exports $316.42 bn, deficit $49.43 bn', 'feature', lede="In April to July 2026-27 India's merchandise exports were $316.42 billion, up 13.16%, against imports of $365.85 billion. That leaves a trade deficit of $49.43 billion.", nums=[('$316.42 bn', 'Exports'), ('13.16%', 'Export growth'), ('$365.85 bn', 'Imports'), ('$49.43 bn', 'Trade deficit')], chart=['trade'])
st('k009', 'FAST-DS 2026: foreign asset disclosure scheme for small taxpayers (16 August–31 December 2026)', 'Tax', 'A window to declare foreign assets: FAST-DS 2026', 'short')
st('k010', 'Trade policy changes: export-oriented e-commerce inventory, raw sugar import, One Star Export House, rupee invoicing', 'Trade policy', 'Raw sugar imports, export house rules and e-commerce stock', 'short')
st('k011', 'EPF wage ceiling proposed to rise from ₹15,000 to ₹25,000 a month', 'Pay', 'EPF wage ceiling may rise to ₹25,000', 'short')
st('k012', 'UPI snapshot: 741 live banks in July 2026; FY26 volume above 24,162 crore', 'Payments', 'UPI now live with 741 banks', 'short')
st('k013', 'Financial inclusion: FI Index 70.0 in March 2026; DBT ₹52.89 lakh crore', 'Inclusion', 'Financial inclusion index reaches 70.0', 'short')
st('k014', 'Regional Rural Banks: FY 2025-26 credit and record profit ₹10,176 crore', 'Rural banks', 'Regional rural banks post record profit of ₹10,176 crore', 'short')
st('k015', 'Credit guarantee for microfinance (CGSMFI 2.0): minimum 15% lending to small and mid-size MFIs', 'Microfinance', 'A bigger credit guarantee for microfinance lenders', 'short')
st('k016', 'Bank locker data: zero theft cases in public sector banks in FY26', 'Lockers', 'No locker thefts reported in public sector banks', 'short')
st('k017', 'UPI completes 10 years (launched 25 August 2016)', 'Payments', 'UPI turns ten', 'short')
st('k018', 'PSBs propose a 2% climate finance sub-target within priority sector lending', 'Green finance', 'Public sector banks propose a climate finance target', 'short')
st('k019', 'Favara–UPI corridor live between Maldives and India; UPI July 2026 record', 'Payments', 'UPI reaches the Maldives, July sets a record', 'short')
st('k020', 'FCNR(B) swap-window deposits (5 June–30 July 2026): private and foreign banks lead', 'Deposits', 'FCNR(B) swap window: who raised the most', 'short')
st('k021', 'Polymer banknotes: government approves one billion pieces each of ₹10 and ₹20 for field trials', 'Currency', 'Polymer notes: ₹10 and ₹20 go to field trials', 'short')
st('k022', "IRDAI tightens intermediary rules and eases insurers' investment norms", 'Insurance', 'IRDAI tightens intermediary rules, loosens investment norms', 'short')
st('k023', 'Government OFS in LIC: up to 6.5% stake, floor price ₹382', 'Insurance', 'Government sells up to 6.5% of LIC', 'short')
st('k024', 'IRDAI actions: Niva Bupa and Acko barred from opening new offices; Maharajah bonds opened to insurers', 'Insurance', 'Two insurers barred from opening offices', 'short')
st('k025', 'Recovery of loan dues: conduct rules for banks, NBFCs and recovery agents (Responsible Business Conduct Fourth Amendment Directions, 2026)', 'RBI rules', 'New conduct rules for loan recovery', 'short')
st('k026', 'CRR and SLR exemption on fresh FCNR(B) and NRE deposits cut short to 31 August 2026', 'RBI rules', 'Foreign-currency deposit relief cut short to 31 August', 'short')
st('k027', 'Bank lending and deposit rates: WALR 8.97% (July 2026), MCLR 8.70% (August 2026)', 'Rates', 'Lending rate 8.97%, MCLR 8.70%', 'short')
st('mpc', 'Monetary Policy Committee, 62nd meeting (3–5 August 2026): repo rate unchanged at 5.25%', 'Monetary policy', 'RBI holds the repo rate at 5.25%', 'feature', lede="The Reserve Bank's Monetary Policy Committee met for the 62nd time from 3 to 5 August 2026 and left the repo rate unchanged at 5.25%. It trimmed its inflation projection for 2026-27 to 5% from 5.1% and put real GDP growth at 6.7%. The next meeting is on 5 to 7 October.", nums=[('5.25%', 'Repo rate, unchanged'), ('5%', 'CPI projection, 2026-27'), ('6.7%', 'GDP growth projection'), ('62nd', 'MPC meeting')], trap='The rate did not move; only the inflation projection was trimmed, from 5.1% to 5%.')
st('k029', 'RBI issues 64 consolidated Master Directions on supervision', 'RBI rules', '64 Master Directions replace 628 circulars', 'short')
st('k030', 'Tata Sons classed as Upper-Layer NBFC; 17 NBFCs in the Upper Layer', 'NBFCs', 'Tata Sons joins the Upper Layer', 'short')
st('k031', 'Draft on-tap licensing for urban co-operative banks (deposits ₹10,000 crore)', 'Co-operative banks', 'On-tap licences for urban co-operative banks: the draft', 'short')
st('k032', 'Draft Interest Rates on Loans and Advances Directions, 2026 (proposed 1 April 2027)', 'RBI draft', 'A draft on how loan interest rates are set', 'short')
st('k033', 'RBI data: house price index 117.5; LRS outward remittances; NRI deposits', 'RBI data', 'House prices, remittances and NRI deposits', 'short')
st('k034', 'RBI forex swap facility inflows $72.85 billion; bank deposit growth 15.4%; Basel III Pillar 3 deferred', 'RBI data', 'Dollar swap inflows $72.85 billion, deposits up 15.4%', 'short')
st('k035', 'RBI board and executive appointments: three part-time non-official directors; Monisha Chakraborty ED', 'RBI board', 'Three new directors on the RBI board', 'short')
st('k036', 'PaRRVA enrolment deadline extended to 3 September 2026', 'SEBI', 'PaRRVA enrolment extended to 3 September', 'short')
st('k037', 'Municipal debt securities: face value, escrow and results timelines eased', 'SEBI', 'Municipal bonds get easier rules', 'short')
st('k038', 'Commodity derivatives stress test: Z-score threshold lowered from 10 to 5', 'SEBI', 'Commodity stress test threshold falls to 5', 'short')
st('k039', 'InvITs: debt-funded major maintenance of road projects can be added back to NDCF', 'SEBI', 'InvITs may add back road maintenance spending', 'short')
st('k040', 'Online bond platforms (OBPPs): IFSCA products and 54EC bonds allowed', 'SEBI', 'Bond platforms may sell IFSCA products and 54EC bonds', 'short')
st('k041', 'ITRI: half-yearly IT resilience score for market infrastructure institutions', 'SEBI', 'ITRI: a resilience score for market infrastructure', 'short')
st('k042', 'New stock market timings from 3 August 2026: Closing Auction Session', 'SEBI', 'A closing auction ends the trading day', 'short')
st('k043', 'SEBI GARUDA mechanism for AIF scheme launches', 'SEBI', 'GARUDA speeds up AIF scheme launches', 'short')
st('k044', 'SEBI Annual Report 2025-26: IPO leadership, fees and investor data', 'SEBI', 'SEBI Annual Report 2025-26', 'short')
st('k045', 'SEBI data: 87.7% of individual F&O traders lost money in FY26; losses ₹91,685 crore', 'SEBI', '87.7% of individual F&O traders lost money', 'short')
st('k046', 'SEBI cyber portals and SEBI mutual fund registration form', 'SEBI', 'New cyber portals and a mutual fund registration form', 'short')
st('k047', 'Domestic PNG connection incentive scheme (from 1 September 2026)', 'Gas', 'A bonus for new piped gas connections', 'short')
st('k048', 'Supreme Court directs RBI SOP for mule accounts and fuel-insurance pilot', 'Courts', 'Supreme Court asks RBI for a mule-account procedure', 'short')
st('k049', 'Taxation and Other Laws (Amendment) Bill, 2026: UPI MDR, rough diamonds, electronics tax exemption', 'Tax law', 'Taxation Bill: UPI MDR, rough diamonds, electronics', 'short')
st('k050', 'NPS charges revised from 1 October 2026', 'Pensions', 'NPS charges revised from 1 October', 'short')
st('k051', 'DPDP Act penalty ₹250 crore; unclaimed deposits rule; SEBI Setu portal; GI counts', 'Data law', 'DPDP penalty up to ₹250 crore; unclaimed deposits', 'short')
st('k052', 'IMF: India to cross $5 trillion in FY29; IFC and ADB financing in India', 'IMF', 'IMF: India crosses $5 trillion in FY29', 'short')
st('k053', 'EU CBAM operational from January 2026', 'Trade', 'The EU carbon border tax is live', 'short')
st('k054', 'Makkah Joint Defence Agreement; Nauru renamed Naoero; FAO Food Price Index 131.1', 'World', 'A Makkah defence pact, Nauru renamed, food prices at a high', 'short')
st('k055', 'World news: Syria off terror list, Venezuela exits Rome Statute, Lebanon abolishes death penalty, naval coalition', 'World', 'Syria, Venezuela, Lebanon: the month abroad', 'short')
st('k056', "PM Modi's state visit to Uzbekistan", 'Visit', 'PM Modi in Uzbekistan', 'short')
st('k057', 'Tribunal Reforms Bill, 2026: National Tribunals Commission', 'Law', 'Tribunal Reforms Bill creates a National Tribunals Commission', 'short')
st('k058', 'UDISE+ 2025–26: 14.67 lakh schools, 24.72 crore enrolments', 'Schools', 'UDISE+ 2025–26: 14.67 lakh schools', 'short')
st('k059', 'MSMED (Amendment) Bill, 2026 passed by Parliament', 'MSME', 'MSMED Amendment Bill passed', 'short')
st('k060', 'AISHE 2022-23 and 2023-24: GER 30 in 2023-24', 'Higher education', 'Higher education enrolment ratio reaches 30', 'short')
st('k061', 'Supreme Court (Number of Judges) Amendment Bill, 2026: 33 to 37 judges', 'Courts', 'Supreme Court to have 37 judges', 'short')
st('k062', 'MMDR Amendment Bill: captive mine sale ceiling removed, lease extensions', 'Mining', 'MMDR Bill removes the captive sale ceiling', 'short')
st('k063', 'Mediation Council of India established (Mediation Act, 2023)', 'Law', 'The Mediation Council of India is set up', 'short')
st('k064', '80th Independence Day announcements (15 August 2026)', 'Independence Day', '80th Independence Day announcements', 'short')
st('k065', 'Government to remove 12-minute advertisement cap for TV channels', 'Media', 'The 12-minute ad cap on TV is to go', 'short')
st('k066', 'Supreme Court: third-party insurance extended to 4 years (cars), 6 years (two-wheelers); court-video curbs', 'Courts', 'Longer third-party motor insurance', 'short')
st('k067', 'MHA: heatwave and lightning added to disaster list (14 calamities); renewable projects barred near borders', 'Disasters', 'Heatwave and lightning join the disaster list', 'short')
st('k068', '80th Independence Day: theme, Shakti ki Sapt Dhara, Civil Defence; Cabinet approves Ladakh High Court bench', 'Independence Day', 'Theme of the 80th Independence Day; Ladakh court bench', 'short')
st('k069', 'DoT: no new SIM beyond 9 connections; PM CARES balance; Maharashtra snakebite notifiable', 'Telecom', 'No more than 9 SIM cards per person', 'short')
st('k070', 'Parliament and Presidential assent (August 2026): Bills and Acts', 'Parliament', 'Bills and Acts of the August session', 'short')
st('sugar', "India's sugar sector: FRP ₹365 per quintal for 2026–27 season and stock limits", 'Sugar', 'Sugar price ₹365 a quintal for 2026–27', 'feature', lede='The sugar fair and remunerative price for the 2026–27 season is ₹365 per quintal at a recovery rate of 10.25%. Dealers face a stock limit of 400 tonnes from 1 August to 30 November 2026, and up to 10 lakh tonnes of raw sugar can be imported duty-free until 31 October 2026.', nums=[('₹365', 'FRP per quintal'), ('10.25%', 'Recovery rate'), ('400 tonnes', 'Dealer stock limit'), ('10 lakh tonnes', 'Duty-free raw sugar')])
st('k072', 'Agriculture items: edible oils missions, honey mission, vultures, natural farming', 'Agriculture', 'Edible oils, honey, vultures and natural farming', 'short')
st('ship', 'Ship recycling: India world number one in 2025 with 35.4% share', 'Ships', 'India is world number one in ship recycling', 'feature', lede="India was the world's number one ship-recycling nation in 2025 with a 35.4% share, up from 30.1% in 2024.", nums=[('35.4%', 'Global share, 2025'), ('30.1%', 'Share, 2024')], chart=['ship'])
st('k074', "Bharat Taxi: India's first cooperative ride-hailing platform", 'Transport', 'Bharat Taxi: a driver-owned ride-hailing platform', 'short')
st('k075', 'PM RAHAT: cashless treatment for road accident victims', 'Roads', 'PM RAHAT: cashless care for accident victims', 'short')
st('k076', 'e-Samudra launched (8 August 2026)', 'Ports', 'e-Samudra goes live', 'short')
st('k077', 'V2V communication to be mandatory from 1 October 2028 (draft)', 'Roads', 'Vehicles to talk to each other from 2028', 'short')
st('k078', 'India crosses 300 GW non-fossil capacity; Hub and spoke aviation model', 'Energy', '300 GW of non-fossil power', 'short')
st('k079', 'Jal Jeevan Mission completes 7 years: 15.91 crore tap connections', 'Water', 'Jal Jeevan Mission at seven years: 15.91 crore taps', 'short')
st('k080', 'World Elephant Day: 22,446 wild elephants (SAIEE 2021–25)', 'Wildlife', '22,446 wild elephants counted', 'short')
st('k081', "Glaw Lake designated India's 101st Ramsar site", 'Wetlands', "Glaw Lake becomes India's 101st Ramsar site", 'short')
st('k082', 'Ladakh: High Court bench approved; five new districts; wildlife safari', 'Ladakh', 'Ladakh: a High Court bench and five new districts', 'short')
st('k083', 'Rajasthan first state to execute a Rare Earth Elements exploration licence', 'Minerals', 'Rajasthan issues the first rare earth exploration licence', 'short')
st('k084', 'India–US Javelin deal; HAL–Safran Aravalli engine; other August MoUs', 'Deals', 'Javelin missiles, an engine deal and other MoUs', 'short')
st('k085', 'Bank of America to buy 49.9% of Jio Credit; Prudential to buy 75% of Bharti Life', 'Mergers', 'Bank of America buys into Jio Credit, Prudential into Bharti Life', 'short')
st('k086', 'BRICS Tourism Ministers adopt Jaipur Declaration; 12th BRICS Environment Ministers meeting 18 August', 'Summit', 'BRICS tourism ministers sign the Jaipur Declaration', 'short')
st('k087', '18th BRICS Summit (12–13 September 2026, New Delhi); 26th SCO Summit; UNCCD COP17', 'Summit', 'The 18th BRICS Summit comes to New Delhi', 'short')
st('k088', 'Key appointments (August 2026)', 'Appointments', 'Key appointments of August 2026', 'short')
st('k089', 'More appointments: NITI Aayog CEO Anurag Jain, ITLOS judge Bimal N. Patel, World Bank auditor general Yuko Keicho', 'Appointments', 'NITI Aayog gets a new CEO', 'short')
st('k090', "South India's first chip plant: ASIP Technologies OSAT, Visakhapatnam (₹2,500 crore)", 'Chips', "South India's first chip plant rises at Visakhapatnam", 'short')
st('k091', 'ICAR firsts: pigeonpea T2T genome, indigenous ASF vaccine, 16 new livestock breeds; soil texture map', 'Agri science', 'Pigeonpea genome, African swine fever vaccine, 16 new breeds', 'short')
st('k092', 'Space: NASA Roman telescope, ISRO invited to Moon Base, IN-SPACe EO constellation, EVEREST engine', 'Space', 'Moon Base invitation and a private rocket engine', 'short')
st('k093', 'Space: Bharatiya Antariksha Station target 2035; Param Pragya; other S&T', 'Space', "India's space station to be ready by 2035", 'short')
st('prahaar', 'Defence: PRAHAAR counter-terrorism policy, Agni-4 test, 6th PIL, Baaz battalion, AK-203 Sher', 'Defence', "PRAHAAR: India's first counter-terrorism policy", 'feature', lede="The Home Ministry launched PRAHAAR, India's first comprehensive national counter-terrorism policy, built on seven pillars. India also test-fired the Agni-4 missile on 6 August 2026, and the defence ministry issued a sixth list of 405 items to be made in India.", nums=[('7', 'Pillars of PRAHAAR'), ('4,000 km', 'Agni-4 range'), ('405', 'Items, 6th list'), ('₹3,070 crore', 'Business potential')])
st('mq9b', 'MoD leases two more MQ-9B SeaGuardians (₹1,943 crore); Coast Guard gender-neutral induction', 'Defence', 'Two more SeaGuardian drones on lease', 'feature', lede='The defence ministry signed a ₹1,943 crore, 30-month lease with General Atomics for two more MQ-9B SeaGuardian drones for the Navy, taking the leased fleet from two to four. The Coast Guard also opened gender-neutral induction.', nums=[('₹1,943 crore', 'Lease value'), ('30 months', 'Lease period'), ('2 → 4', 'Leased drones'), ('$204.53 million', 'In dollars')])
st('k096', "FIH Hockey World Cups 2026: Germany men's champions; India women's best finish in 52 years", 'Hockey', "Germany win the men's hockey World Cup", 'short')
st('k097', 'BWF World Championships 2026 in New Delhi; Durand Cup; other major results', 'Badminton', 'The badminton World Championships come to Delhi', 'short')
st('cwg', 'Commonwealth Games 2026 (Glasgow): India 4th with 39 medals; Khelo India revamp ₹36,441 crore', 'Commonwealth Games', 'India fourth at Glasgow with 39 medals', 'feature', lede='India finished fourth at the 23rd Commonwealth Games in Glasgow with 39 medals: 13 gold, 17 silver and 9 bronze. Boxing gave a record 10 medals including 7 golds. The Cabinet also approved a ₹36,441 crore revamp of Khelo India and support to national sports federations.', nums=[('4th', 'India'), ('39', 'Medals'), ('13', 'Gold'), ('₹36,441 crore', 'Khelo India revamp')], chart=['cwg'], trap='India finished in the same position as at Birmingham 2022; Scotland also won 39 medals and was fifth.')
st('k099', 'Hockey World Cup format, FIDE Chess Olympiad seedings, TTFI suspension, Anahat Singh', 'Sport', 'Chess Olympiad seedings, a suspended federation, a squash first', 'short')
st('k100', 'Awards: COSPAR Vikram Sarabhai Medal, Dirac Medal, National Sports Awards 2025, gallantry awards', 'Awards', 'COSPAR medal for Annapurni Subramaniam; gallantry awards', 'short')
st('k101', 'Other August awards: Handloom awards, Gaj Gaurav, Anubhav, gallantry and service medals', 'Awards', '1,057 medals for Independence Day; handloom awards', 'short')
st('k102', 'Rankings: Kroll celebrity valuation, data centre atlas, ARWU 2026', 'Rankings', 'Celebrity brands, data centres and the Shanghai ranking', 'short')
st('hurun', 'Reports: Hurun family businesses, WIPO GenAI patents, NITI skilling, WHO-UNICEF health facility WASH', 'Reports', 'Family businesses, AI patents, skills and sanitation', 'feature', lede='The Hurun India list of Most Valuable Family Businesses 2026 counts 300 families worth ₹138 lakh crore. The Ambani family is first at ₹25.82 lakh crore. In other reports, India is fifth in generative AI patent filings and 8.7 crore young Indians are NEET.', nums=[('₹138 lakh crore', '300 family businesses'), ('₹25.82 lakh crore', 'Ambani family'), ('5th', 'India, GenAI patents'), ('8.7 crore', 'Youth who are NEET')])
st('epi', 'EPI 2026: India 176th of 177; seafarer supplier rank; other August reports', 'Environment', 'India 176th of 177 on the environment index', 'feature', lede="Yale and Columbia's Environmental Performance Index 2026 ranks India 176th of 177 countries with a score of 22.46, ahead only of Laos. Estonia is first with 74.79. Separately, India is the world's second-largest supplier of seafarers, with 3,11,936.", nums=[('176th', 'Of 177'), ('22.46', 'India score'), ('74.79', 'Estonia, first'), ('3,11,936', 'Seafarers supplied')], chart=['epi'], trap='Only Laos ranks below India.')
st('jandhan', '12 years of PM Jan Dhan Yojana (data as on 19 August 2026)', 'Welfare', 'Jan Dhan at twelve: 59.09 crore accounts', 'feature', lede='PM Jan Dhan Yojana began on 28 August 2014 to give every unbanked adult a basic account. By 19 August 2026 it had 59.09 crore accounts holding ₹3,16,514 crore, and 41.29 crore RuPay cards had been issued.', nums=[('59.09 crore', 'Accounts'), ('₹3,16,514 crore', 'Deposits'), ('55.7%', 'Women account holders'), ('₹5,356', 'Average deposit')], chart=['jandhan'])
st('eshram', '5 years of the e-Shram portal', 'Welfare', 'Five years of e-Shram', 'feature', lede='The e-Shram portal for unorganised workers began on 26 August 2021. By 18 August 2026 it had 31.89 crore registered workers, 54.28% of them women.', nums=[('31.89 crore', 'Registrations'), ('54.28%', 'Women'), ('12-digit', 'Account number'), ('22', 'Languages')], trap='The one-stop solution was launched on 21 October 2024.')
st('k107', 'Container Manufacturing Assistance Scheme (Union Budget 2026–27)', 'Shipping', '₹10,000 crore to make shipping containers in India', 'short')
st('gobar', 'National Circular Bioenergy Scheme: GOBARdhan (Cabinet, 6 August 2026)', 'Energy', 'A ₹23,731 crore push for compressed biogas', 'feature', lede='The Cabinet approved the National Circular Bioenergy Scheme on 6 August 2026 with an outlay of ₹23,731 crore to scale up compressed biogas production nearly 10 times. City gas companies must buy a rising share of biogas, at an administered price of ₹2,110 per MMBTU.', nums=[('₹23,731 crore', 'Outlay'), ('₹2,110', 'Price per MMBTU'), ('85%', 'Credit guarantee, MSME projects'), ('₹2 crore', 'Capital aid per TPD, greenfield')], chart=['cbg'], trap='The scheme runs from FY 2026-27 to FY 2035-36; GOBARdhan itself began in 2018.')
st('vbry', 'PM Viksit Bharat Rojgar Yojana: one year (August 2026)', 'Jobs', 'A year of the PM Viksit Bharat Rojgar Yojana', 'feature', lede="The PM Viksit Bharat Rojgar Yojana, announced in August 2025, pays first-time employees one month's EPF wage up to ₹15,000 and gives employers up to ₹3,000 a month for each extra hire. It has an outlay of ₹99,446 crore and runs to 31 July 2027. After one year, 72 lakh first-time workers have joined.", nums=[('₹99,446 crore', 'Outlay'), ('₹15,000', 'Most an employee gets'), ('₹3,000', 'A month, employer'), ('72 lakh', 'First-time workers')])
st('k110', 'National Investment Policy for Urea-2026 (NIPU-2026)', 'Fertiliser', 'A new investment policy for urea', 'short')
st('samudra', 'Samudra Manthan: National Offshore Exploration Scheme, ₹84,084 crore', 'Energy', 'Samudra Manthan: ₹84,084 crore to find oil and gas at sea', 'feature', lede='The Cabinet approved Samudra Manthan, a ₹84,084 crore scheme to search for oil and gas offshore, mainly in deep water, running to 31 March 2031. It funds 60 deepwater wells and pays up to half the eligible drilling cost or ₹675 crore per well, whichever is lower.', nums=[('₹84,084 crore', 'Outlay'), ('60', 'Deepwater wells'), ('50%', 'Of eligible drilling cost'), ('₹675 crore', 'Cap per well')], chart=['sam'])
st('mobile', 'Mobile Phone Manufacturing Scheme notified: ₹62,500 crore (August 2026)', 'Electronics', '₹62,500 crore to make more phones in India', 'feature', lede='The electronics ministry notified a ₹62,500 crore scheme to boost mobile phone making and Indian brands, running from 2026-27 to 2030-31. Phone makers get an incentive of 2.25% to 5%; Indian brands get 5% plus 3% more for Indian design and R&D.', nums=[('₹62,500 crore', 'Outlay'), ('2.25%–5%', 'Incentive, TS1'), ('5% + 3%', 'Incentive, TS2'), ('1.5%', 'Extra for local parts')])
st('pmkisan', 'PM-KISAN continued to 2030-31 (₹3,15,614 crore); PM Surya Sarovar Yojana (₹5,070 crore)', 'Farmers', 'PM-KISAN continues; a floating solar scheme', 'feature', lede='The Cabinet extended PM-KISAN for five more years, 2026-27 to 2030-31, with ₹3,15,614 crore; farmers get ₹6,000 a year in three instalments. It also approved the PM Surya Sarovar Yojana: ₹5,070 crore for 5,000 MW of floating solar with storage.', nums=[('₹3,15,614 crore', 'PM-KISAN outlay'), ('₹6,000', 'Per farmer a year'), ('₹5,070 crore', 'PM Surya Sarovar'), ('5,000 MW', 'Floating solar')])
st('k114', 'AB-PMJAY reaches West Bengal (36th state/UT); PM E-DRIVE two-wheeler incentives extended; Palna crèches', 'Health', 'West Bengal joins Ayushman Bharat', 'short')
