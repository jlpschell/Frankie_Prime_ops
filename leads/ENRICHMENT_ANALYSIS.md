# Lead Data Quality & Enrichment Analysis
**Generated:** 2026-02-14
**Analyst:** Frankie

---

## Executive Summary

Analyzed **12 campaign-ready niches** totaling **1,193 leads** across water damage, general contractors, septic, turf, garage doors, pool builders, concrete, floor coating, steel/metal, medspas, roofing, and HVAC.

### Key Findings:
- **79% of all leads are missing email addresses** (phone-only coverage)
- **Water damage is the #1 enrichment target**: 390 leads with only 21% email coverage
- **Easy enrichment path exists**: 454 leads have phone numbers that can be reverse-looked up for emails
- **Current data structure**: All CSVs have consistent columns (Name, Phone, Email, Company, City, State, Website, Tags)

---

## Overall Data Quality by Niche

| NICHE                | SOURCE          | LEADS | EMAIL % | PHONE % | WEB %  | GRADE | ROI SCORE |
|----------------------|-----------------|-------|---------|---------|--------|-------|-----------|
| **water-damage**     | leads/          | 390   | 21.0%   | 99.2%   | 92.6%  | B     | **155**   |
| **septic**           | leads/          | 99    | 0.0%    | 99.0%   | 84.8%  | C     | **49**    |
| **garage-doors**     | leads/          | 52    | 1.9%    | 100.0%  | 86.5%  | C     | **25**    |
| concrete             | leads/          | 111   | 62.2%   | 99.1%   | 77.5%  | A     | 21        |
| medspa               | leads/          | 59    | 28.8%   | 100.0%  | 100.0% | B     | 21        |
| hvac                 | leads/          | 56    | 30.4%   | 98.2%   | 98.2%  | B     | 19        |
| general-contractors  | leads/          | 156   | 76.9%   | 100.0%  | 82.7%  | A     | 18        |
| steel-metal          | ghl_import/     | 47    | 76.6%   | 100.0%  | 78.7%  | A     | 5         |
| pool-builders        | ghl_import/     | 89    | 89.9%   | 100.0%  | 93.3%  | A     | 4         |
| roofing              | leads/          | 29    | 86.2%   | 100.0%  | 93.1%  | A     | 2         |
| turf                 | ghl_import/     | 96    | 96.9%   | 100.0%  | 99.0%  | A     | 1         |
| floor-coating        | leads/          | 14    | 78.6%   | 100.0%  | 100.0% | A     | 1         |

**ROI Score Formula:** `(List Size ÷ 100) × Missing Contact %`
Higher score = Bigger list with more gaps = Best enrichment ROI

---

## Top 3 Enrichment Priorities

### 1. WATER DAMAGE (ROI: 155)
**File:** `/leads/water_damage/water_damage_restoration.csv`

- **Total Leads:** 390
- **Email Coverage:** 21.0% (82 leads)
- **Phone Coverage:** 99.2% (387 leads)
- **Website Coverage:** 92.6% (361 leads)

#### Data Breakdown:
```
✓ Both email + phone:    82 ( 21.0%)
⚠ Email only:             0 (  0.0%)
⚠ Phone only:           305 ( 78.2%)  ← ENRICHMENT TARGET
✗ Neither:                3 (  0.8%)
```

#### Enrichment Strategy:
- **Easy wins:** 305 leads with phone → reverse lookup for email
- **Hard cases:** 3 leads missing both (scrape website or paid enrichment)
- **Expected cost:** $30-60 (305 lookups × $0.10-0.20/lookup)
- **Expected lift:** 78% → 95%+ email coverage

---

### 2. SEPTIC (ROI: 49)
**File:** `/leads/septic_services/septic_services.csv`

- **Total Leads:** 99
- **Email Coverage:** 0.0% (0 leads)
- **Phone Coverage:** 99.0% (98 leads)
- **Website Coverage:** 84.8% (84 leads)

#### Data Breakdown:
```
✓ Both email + phone:     0 (  0.0%)
⚠ Email only:             0 (  0.0%)
⚠ Phone only:            98 ( 99.0%)  ← ENRICHMENT TARGET
✗ Neither:                1 (  1.0%)
```

#### Enrichment Strategy:
- **Easy wins:** 98 leads with phone → reverse lookup for email
- **Hard cases:** 1 lead missing both (scrape website)
- **Expected cost:** $10-20 (98 lookups × $0.10-0.20/lookup)
- **Expected lift:** 0% → 90%+ email coverage

---

### 3. GARAGE DOORS (ROI: 25)
**File:** `/leads/garage_door/garage_door.csv`

- **Total Leads:** 52
- **Email Coverage:** 1.9% (1 lead)
- **Phone Coverage:** 100.0% (52 leads)
- **Website Coverage:** 86.5% (45 leads)

#### Data Breakdown:
```
✓ Both email + phone:     1 (  1.9%)
⚠ Email only:             0 (  0.0%)
⚠ Phone only:            51 ( 98.1%)  ← ENRICHMENT TARGET
✗ Neither:                0 (  0.0%)
```

#### Enrichment Strategy:
- **Easy wins:** 51 leads with phone → reverse lookup for email
- **Hard cases:** None (all have phone)
- **Expected cost:** $5-10 (51 lookups × $0.10-0.20/lookup)
- **Expected lift:** 2% → 95%+ email coverage

---

## Recommended Action Plan

### Phase 1: Water Damage (Highest ROI)
1. **Extract phone numbers** from `/leads/water_damage/water_damage_restoration.csv`
2. **Reverse phone lookup** via:
   - TruePeopleSearch (free, slower)
   - FastPeopleSearch (free, slower)
   - RocketReach API ($0.10/lookup, faster)
   - Hunter.io ($0.15/lookup, higher quality)
3. **Update master CSV** with enriched emails
4. **Re-import to GHL** or update existing contacts
5. **Expected ROI:** 305 new email addresses for $30-60 investment

### Phase 2: Septic (Medium ROI, Zero Email Baseline)
- Same strategy as water damage
- **Critical:** This niche has ZERO emails currently — enrichment is mandatory for email campaigns

### Phase 3: Garage Doors (Quick Win)
- Smallest list (52 leads) = cheapest enrichment ($5-10)
- Perfect test case before scaling to water damage

---

## Data Structure Analysis

All CSV files follow this consistent schema:

```csv
First Name,Last Name,Phone,Email,Company Name,City,State,Website,Tags
```

### Observations:
- **First/Last Name:** Usually empty (business listings, not individuals)
- **Phone:** 95%+ coverage across all niches
- **Email:** 20-30% coverage (primary gap)
- **Company Name:** 90%+ coverage
- **Website:** 80-95% coverage (good fallback for scraping)
- **City/State:** Present but not always accurate
- **Tags:** Empty or niche-specific

---

## Enrichment Tools Comparison

### Free Options (Slow, Manual):
- **TruePeopleSearch** — Phone reverse lookup (rate limited)
- **FastPeopleSearch** — Phone reverse lookup (rate limited)
- **Google Maps scraping** — Can extract emails from websites listed

### Paid Options (Fast, API):
| Service          | Cost/Lookup | Email Quality | Phone Lookup | Notes                        |
|------------------|-------------|---------------|--------------|------------------------------|
| **RocketReach**  | $0.10       | High          | Yes          | Best for B2B contacts        |
| **Hunter.io**    | $0.15       | Very High     | Limited      | Email-focused, domain search |
| **Clearbit**     | $0.20       | Very High     | Yes          | Premium pricing              |
| **Prospeo**      | $0.05       | Medium        | No           | Budget option                |

### Recommended: RocketReach
- **Why:** Best balance of cost ($0.10) vs. quality
- **Batch API:** Can process 100-500 lookups at once
- **Phone → Email:** Primary use case supported
- **Estimated cost for all 3 niches:** $45-90 (454 lookups)

---

## Next Steps

1. **Decision:** Pick enrichment tool (RocketReach recommended)
2. **Test batch:** Start with garage doors (52 leads, $5-10 test)
3. **Validate results:** Check email deliverability on test batch
4. **Scale to water damage:** 305 leads if test succeeds
5. **Update GHL campaigns:** Re-import enriched CSVs
6. **Monitor:** Track email open rates vs. phone-only campaigns

---

## Notes

- **Scripts created:**
  - `/scripts/audit-lead-quality.py` — Generate this analysis
  - `/scripts/detailed-gap-analysis.py` — Deep dive on specific niches

- **Raw data locations:**
  - `/leads/{niche}/` — Master CSVs by niche
  - `/ghl_import/` — GHL-ready import files (some overlap)

- **Campaign alignment:**
  - Water damage, general contractors, roofing = active campaigns
  - Septic, garage doors, turf = next wave
  - HVAC, medspas, concrete = backlog
