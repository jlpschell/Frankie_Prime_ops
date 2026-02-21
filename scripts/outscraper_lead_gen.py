#!/usr/bin/env python3
"""
Outscraper Lead Gen MVP — Pull fully enriched leads from Google Maps.

Pulls: business name, phone, carrier type, email (validated), website,
       owner/contact name, title, social links, Google rating/reviews,
       company insights (employees, revenue, founded year).

Usage:
    # Single niche + location
    python outscraper_lead_gen.py --niche "HVAC" --location "DFW, TX" --limit 100

    # Batch from config file
    python outscraper_lead_gen.py --batch batch_config.json

    # Dry run (show what would be searched, no API call)
    python outscraper_lead_gen.py --niche "HVAC" --location "DFW, TX" --limit 100 --dry-run

Cost: ~$0.002-0.01 per result depending on enrichments
"""

import os
import csv
import json
import time
import argparse
import re
import sys
from datetime import datetime

import requests
from dotenv import load_dotenv

# Load .env
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(ENV_PATH)

API_KEY = os.environ.get('OUTSCRAPER_API_KEY', '') or os.environ.get('OUTSCRAPER_API_TOKEN', '')
BASE_URL = 'https://api.outscraper.cloud'

# All enrichments for full data
ENRICHMENTS = [
    'contacts_n_leads',          # emails, social links, phones, contacts
    'emails_validator_service',  # validates found emails
    'phones_enricher_service',   # carrier name/type
    'company_insights_service',  # revenue, employees, founded
    'whitepages_phones',         # phone owner identity
]

# EAST DFW → GREENVILLE/TYLER CORRIDOR
# Tight zone: everything east of US-75 out to Greenville/Tyler
EAST_DFW_CITIES = [
    # Inner east (Dallas suburbs)
    "Garland, TX", "Mesquite, TX", "Rowlett, TX", "Sachse, TX",
    "Wylie, TX", "Murphy, TX", "Lucas, TX",
    # Rockwall / I-30 corridor
    "Rockwall, TX", "Royse City, TX", "Fate, TX", "Heath, TX",
    # Forney / Kaufman corridor
    "Forney, TX", "Terrell, TX", "Kaufman, TX", "Crandall, TX",
    "Seagoville, TX", "Combine, TX",
    # US-380 corridor (north)
    "McKinney, TX", "Allen, TX", "Princeton, TX", "Anna, TX",
    "Melissa, TX", "Celina, TX",
    # Rural east (Jay's backyard)
    "Farmersville, TX", "Caddo Mills, TX", "Josephine, TX",
    "Nevada, TX", "Lavon, TX", "Blue Ridge, TX", "Quinlan, TX",
    # Greenville / Hunt County
    "Greenville, TX", "Commerce, TX", "Wolfe City, TX",
    "Sulphur Springs, TX", "Emory, TX",
    # Canton / Van Zandt
    "Canton, TX", "Wills Point, TX", "Van, TX", "Grand Saline, TX",
    "Edgewood, TX",
    # Tyler / Smith County
    "Tyler, TX", "Lindale, TX", "Whitehouse, TX", "Mineola, TX",
    "Flint, TX", "Bullard, TX", "Chandler, TX", "Brownsboro, TX",
    # Athens / Henderson
    "Athens, TX", "Henderson, TX", "Jacksonville, TX",
    "Mabank, TX", "Gun Barrel City, TX", "Kemp, TX",
]

# Full DFW (kept for reference / wider searches)
DFW_CITIES = EAST_DFW_CITIES + [
    "Dallas, TX", "Fort Worth, TX", "Plano, TX", "Frisco, TX",
    "Arlington, TX", "Irving, TX", "Richardson, TX", "Denton, TX",
    "Lewisville, TX", "Carrollton, TX", "Flower Mound, TX",
    "Grand Prairie, TX", "Mansfield, TX", "Cedar Hill, TX",
    "Keller, TX", "Southlake, TX", "Grapevine, TX",
    "North Richland Hills, TX", "Bedford, TX", "Euless, TX",
    "Hurst, TX", "Haltom City, TX",
]

# Output columns we care about
OUTPUT_FIELDS = [
    'Company Name', 'Phone', 'Phone_Carrier_Type', 'Phone_Carrier_Name',
    'Email', 'Email_Status', 'Website', 'Contact_Name', 'First Name',
    'Last Name', 'Contact_Title', 'Contact_Phone', 'Contact_Phone_Type',
    'Company_Phone', 'Company_Phone_Type', 'Street', 'City', 'State',
    'State_Code', 'Zip', 'Google_Rating', 'Google_Reviews', 'Employees',
    'Revenue', 'Founded', 'LinkedIn', 'Facebook', 'Instagram', 'Domain',
    'Category', 'Subtypes', 'Google_Verified', 'Business_Status', 'About',
    'Tags', 'Source'
]


def search_google_maps(query, limit=500, enrichments=None, region='US'):
    """Submit async search to Outscraper Google Maps API."""
    params = {
        'query': query,
        'limit': limit,
        'dropDuplicates': 'true',
        'region': region,
        'language': 'en',
        'async': 'true',
    }

    # Add enrichments
    if enrichments:
        for e in enrichments:
            params.setdefault('enrichment', [])
        # Outscraper wants repeated params for arrays
        enrichment_str = '&'.join(f'enrichment={e}' for e in enrichments)
    else:
        enrichment_str = ''

    headers = {'X-API-KEY': API_KEY}

    url = f'{BASE_URL}/google-maps-search?{enrichment_str}'
    resp = requests.get(url, params=params, headers=headers)

    if resp.status_code == 401:
        print("ERROR: Invalid API key. Check OUTSCRAPER_API_KEY in .env")
        sys.exit(1)
    if resp.status_code == 402:
        print("ERROR: Payment required. Check your Outscraper balance.")
        sys.exit(1)

    data = resp.json()

    if resp.status_code == 200 and data.get('status') == 'Success':
        return {'status': 'complete', 'data': data.get('data', [])}

    if resp.status_code == 202 or data.get('status') == 'Pending':
        request_id = data.get('id')
        print(f"  Task submitted: {request_id}")
        return {'status': 'pending', 'request_id': request_id}

    print(f"  Unexpected response ({resp.status_code}): {resp.text[:200]}")
    return {'status': 'error', 'data': []}


def poll_results(request_id, max_wait=600, interval=15):
    """Poll for async results."""
    headers = {'X-API-KEY': API_KEY}
    url = f'{BASE_URL}/requests/{request_id}'

    elapsed = 0
    while elapsed < max_wait:
        resp = requests.get(url, headers=headers)
        data = resp.json()

        status = data.get('status', '')
        if status == 'Success':
            return data.get('data', [])
        elif status == 'Failure':
            print(f"  Task failed: {request_id}")
            return []

        print(f"  Waiting... ({elapsed}s / {max_wait}s) status={status}")
        time.sleep(interval)
        elapsed += interval

    print(f"  Timeout waiting for {request_id}")
    return []


def map_outscraper_to_row(item):
    """Map raw Outscraper result to our standard row format."""
    row = {f: '' for f in OUTPUT_FIELDS}

    row['Company Name'] = item.get('name', '')
    row['Phone'] = item.get('phone', '')
    row['Website'] = item.get('site', '') or item.get('website', '')
    row['Street'] = item.get('street', '')
    row['City'] = item.get('city', '')
    row['State'] = item.get('us_state', '') or item.get('state', '')
    row['State_Code'] = item.get('state_code', '')
    row['Zip'] = item.get('postal_code', '')
    row['Google_Rating'] = item.get('rating', '')
    row['Google_Reviews'] = item.get('reviews', '')
    row['Category'] = item.get('category', '')
    row['Subtypes'] = item.get('subtypes', '')
    row['Google_Verified'] = item.get('verified', '')
    row['Business_Status'] = item.get('business_status', '')
    row['About'] = str(item.get('about', ''))[:200]  # Truncate
    row['Domain'] = item.get('domain', '')

    # Phone enrichment
    phone_carrier = item.get('phone.phones_enricher.carrier_type', '')
    if not phone_carrier:
        # Try nested format
        pe = item.get('phones_enricher', {})
        if isinstance(pe, dict):
            phone_carrier = pe.get('carrier_type', '')
    row['Phone_Carrier_Type'] = phone_carrier
    row['Phone_Carrier_Name'] = item.get('phone.phones_enricher.carrier_name', '')

    # Email
    row['Email'] = item.get('email', '')
    row['Email_Status'] = item.get('email.emails_validator.status', '')

    # Contact info
    row['Contact_Name'] = item.get('full_name', '')
    row['First Name'] = item.get('first_name', '')
    row['Last Name'] = item.get('last_name', '')
    row['Contact_Title'] = item.get('title', '')
    row['Contact_Phone'] = item.get('contact_phone', '')
    row['Contact_Phone_Type'] = item.get('contact_phone.phones_enricher.carrier_type', '')

    # Company phone
    row['Company_Phone'] = item.get('company_phone', '')
    row['Company_Phone_Type'] = item.get('company_phone.phones_enricher.carrier_type', '')

    # Company insights
    ci = {}
    for k, v in item.items():
        if k.startswith('company_insights.'):
            ci[k.replace('company_insights.', '')] = v
    row['Employees'] = ci.get('employees', '')
    row['Revenue'] = ci.get('revenue', '')
    row['Founded'] = ci.get('founded_year', '')

    # Socials
    row['LinkedIn'] = item.get('company_linkedin', '')
    row['Facebook'] = item.get('company_facebook', '')
    row['Instagram'] = item.get('company_instagram', '')

    row['Source'] = 'outscraper_api'

    return row


def clean_phone(p):
    if not p:
        return ''
    return re.sub(r'[^\d]', '', str(p))[-10:]


def run_search(niche, location='DFW, TX', limit=500, use_subcities=False,
               enrichments=None, output_dir='leads_v2', dry_run=False, zone='east'):
    """Run a full search for one niche."""
    niche_slug = niche.lower().replace(' ', '_').replace('/', '_')
    os.makedirs(f'{output_dir}/{niche_slug}', exist_ok=True)

    if enrichments is None:
        enrichments = ENRICHMENTS

    # Build queries
    city_list = EAST_DFW_CITIES if zone == 'east' else DFW_CITIES
    if use_subcities:
        queries = [f'{niche}, {city}' for city in city_list]
        per_query_limit = min(limit // len(queries) + 1, 500)
    else:
        queries = [f'{niche}, {location}']
        per_query_limit = limit

    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN — {niche}")
        print(f"{'='*60}")
        print(f"Queries ({len(queries)}):")
        for q in queries[:10]:
            print(f"  • {q}")
        if len(queries) > 10:
            print(f"  ... and {len(queries)-10} more")
        print(f"Limit per query: {per_query_limit}")
        print(f"Enrichments: {', '.join(enrichments)}")
        print(f"Estimated results: {limit}")
        return []

    all_results = []
    seen_phones = set()

    print(f"\n{'='*60}")
    print(f"SEARCHING: {niche} in {location}")
    print(f"{'='*60}")

    # Batch queries (up to 250 per request)
    batch_size = 25  # Conservative to avoid timeouts with enrichments
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]
        print(f"\nBatch {i//batch_size + 1}: {len(batch)} queries...")

        # For batched queries, use POST with multiple query params
        for query in batch:
            print(f"  → {query}")
            result = search_google_maps(query, limit=per_query_limit,
                                       enrichments=enrichments, region='US')

            if result['status'] == 'pending':
                # Poll for results
                data = poll_results(result['request_id'])
            elif result['status'] == 'complete':
                data = result['data']
            else:
                data = []

            # Flatten nested arrays
            if data and isinstance(data[0], list):
                data = [item for sublist in data for item in sublist]

            for item in data:
                if not isinstance(item, dict):
                    continue
                phone = clean_phone(item.get('phone', ''))
                if phone and phone in seen_phones:
                    continue  # Dedupe
                if phone:
                    seen_phones.add(phone)

                row = map_outscraper_to_row(item)
                row['Tags'] = f'outscraper-api,{niche_slug}'
                all_results.append(row)

            # Rate limit between queries
            time.sleep(1)

    # Write results
    if all_results:
        outpath = f'{output_dir}/{niche_slug}/{niche_slug}_master_v2.csv'
        with open(outpath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(all_results)

        # Also write mobile-only
        mobile_rows = [r for r in all_results
                       if r.get('Phone_Carrier_Type', '').lower() == 'mobile']
        if mobile_rows:
            for r in mobile_rows:
                tags = r.get('Tags', '')
                if 'mobile-verified' not in tags:
                    r['Tags'] = f'{tags},mobile-verified'

            mobpath = f'{output_dir}/{niche_slug}/{niche_slug}_mobile_v2.csv'
            with open(mobpath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(mobile_rows)

        # Stats
        has_phone = sum(1 for r in all_results if r.get('Phone'))
        has_email = sum(1 for r in all_results if r.get('Email'))
        has_email_valid = sum(1 for r in all_results if r.get('Email_Status') == 'RECEIVING')
        has_carrier = sum(1 for r in all_results if r.get('Phone_Carrier_Type'))
        mobile = len(mobile_rows)
        has_contact = sum(1 for r in all_results if r.get('Contact_Name'))

        print(f"\n{'='*60}")
        print(f"COMPLETE: {niche}")
        print(f"{'='*60}")
        print(f"  Total leads:       {len(all_results)}")
        print(f"  📞 With phone:     {has_phone}")
        print(f"  📱 Mobile:         {mobile}")
        print(f"  📧 Valid email:    {has_email_valid}")
        print(f"  👤 Contact name:   {has_contact}")
        print(f"  🔍 Carrier known:  {has_carrier}")
        print(f"  Output:            {outpath}")
        if mobile_rows:
            print(f"  Mobile-only:       {mobpath}")
        print(f"{'='*60}")

    return all_results


def main():
    parser = argparse.ArgumentParser(description='Outscraper Lead Gen MVP')
    parser.add_argument('--niche', '-n', help='Business niche (e.g., "HVAC", "Roofing contractor")')
    parser.add_argument('--location', '-l', default='DFW, TX', help='Location (default: DFW, TX)')
    parser.add_argument('--limit', type=int, default=500, help='Max results (default: 500)')
    parser.add_argument('--subcities', action='store_true', help='Split into sub-city queries for more coverage')
    parser.add_argument('--zone', default='east', choices=['east', 'full'], help='Search zone: east (East Dallas→Tyler) or full (all DFW)')
    parser.add_argument('--output', '-o', default='leads_v2', help='Output directory')
    parser.add_argument('--no-enrichment', action='store_true', help='Skip enrichments (basic data only)')
    parser.add_argument('--dry-run', action='store_true', help='Show queries without calling API')
    parser.add_argument('--batch', help='JSON config file for batch processing')

    args = parser.parse_args()

    if not API_KEY and not args.dry_run:
        print("ERROR: OUTSCRAPER_API_KEY not set in .env")
        print("Get your key at: https://outscraper.com/profile")
        sys.exit(1)

    enrichments = [] if args.no_enrichment else ENRICHMENTS

    if args.batch:
        # Batch mode: read config file
        with open(args.batch) as f:
            config = json.load(f)

        total = 0
        for job in config.get('jobs', []):
            niche = job['niche']
            location = job.get('location', args.location)
            limit = job.get('limit', args.limit)
            subcities = job.get('subcities', args.subcities)

            results = run_search(niche, location, limit, subcities,
                               enrichments, args.output, args.dry_run,
                               zone=job.get('zone', args.zone))
            total += len(results)

        print(f"\n\nBATCH COMPLETE: {total} total leads across {len(config['jobs'])} niches")

    elif args.niche:
        run_search(args.niche, args.location, args.limit, args.subcities,
                  enrichments, args.output, args.dry_run, zone=args.zone)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
