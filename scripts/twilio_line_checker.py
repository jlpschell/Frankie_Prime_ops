#!/usr/bin/env python3
"""
Twilio Line-Type Checker — Validates phone numbers as mobile/landline/voip
before SMS campaigns. Protects your number from carrier penalties.

Usage:
    python twilio_line_checker.py --input leads.csv --output checked.csv
    python twilio_line_checker.py --input leads.csv --output checked.csv --limit 10
    python twilio_line_checker.py --input leads.csv --output checked.csv --mobile-only mobile_leads.csv

Cost: $0.005 per lookup ($5 per 1,000 numbers)
"""

import os
import csv
import re
import sys
import time
import argparse
from dotenv import load_dotenv

# Load .env from project root
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(ENV_PATH)

from twilio.rest import Client


def clean_phone(phone_str):
    """Normalize phone to E.164 format."""
    if not phone_str or not phone_str.strip():
        return None
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    if not cleaned.startswith('+') and len(cleaned) == 10:
        cleaned = '+1' + cleaned
    elif not cleaned.startswith('+') and len(cleaned) == 11 and cleaned.startswith('1'):
        cleaned = '+' + cleaned
    if len(cleaned) < 11:
        return None
    return cleaned


def lookup_line_type(client, phone_e164):
    """Call Twilio Lookup API v2 for line type intelligence."""
    try:
        result = client.lookups.v2.phone_numbers(phone_e164).fetch(
            fields='line_type_intelligence'
        )
        lti = result.line_type_intelligence or {}
        return {
            'line_type': lti.get('type', 'unknown'),
            'carrier': lti.get('carrier_name', ''),
            'mobile_country_code': lti.get('mobile_country_code', ''),
            'mobile_network_code': lti.get('mobile_network_code', ''),
            'lookup_status': 'success',
            'lookup_error': '',
        }
    except Exception as e:
        return {
            'line_type': 'error',
            'carrier': '',
            'mobile_country_code': '',
            'mobile_network_code': '',
            'lookup_status': 'failed',
            'lookup_error': str(e)[:100],
        }


def main():
    parser = argparse.ArgumentParser(description="Twilio line-type checker for lead lists")
    parser.add_argument("--input", "-i", required=True, help="Input CSV file")
    parser.add_argument("--output", "-o", required=True, help="Output CSV with line type data")
    parser.add_argument("--mobile-only", "-m", help="Optional: output CSV with only mobile numbers")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of lookups")
    parser.add_argument("--phone-column", default="Phone", help="Column name for phone numbers (default: Phone)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be looked up without calling API")
    args = parser.parse_args()

    # Init Twilio
    sid = os.environ.get('TWILIO_ACCOUNT_SID')
    token = os.environ.get('TWILIO_AUTH_TOKEN')
    if not sid or not token:
        print("ERROR: TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in .env")
        sys.exit(1)

    client = Client(sid, token)

    # Read input
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
        fieldnames = list(reader.fieldnames)

    total = len(leads)
    print(f"Loaded {total} leads from {args.input}")

    if args.limit:
        leads = leads[:args.limit]
        print(f"Limited to {len(leads)} leads")

    # Add lookup columns
    extra = ['line_type', 'carrier', 'lookup_status']
    out_fields = fieldnames + [f for f in extra if f not in fieldnames]

    # Stats
    stats = {'mobile': 0, 'landline': 0, 'voip': 0, 'unknown': 0, 'error': 0, 'skipped': 0}
    cost_per_lookup = 0.005
    lookups_done = 0

    # Process
    with open(args.output, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=out_fields, extrasaction='ignore')
        writer.writeheader()

        mobile_rows = []

        for i, lead in enumerate(leads, 1):
            phone_raw = lead.get(args.phone_column, '').strip()
            phone_e164 = clean_phone(phone_raw)

            if not phone_e164:
                lead['line_type'] = 'invalid'
                lead['carrier'] = ''
                lead['lookup_status'] = 'skipped_no_phone'
                stats['skipped'] += 1
                name = lead.get('Company Name', lead.get('Name', '?'))[:40]
                print(f"[{i}/{len(leads)}] {name} — no valid phone, skipped")
                writer.writerow(lead)
                continue

            if args.dry_run:
                print(f"[{i}/{len(leads)}] Would lookup: {phone_e164}")
                lead['line_type'] = 'pending'
                lead['carrier'] = ''
                lead['lookup_status'] = 'dry_run'
                writer.writerow(lead)
                continue

            # Live lookup
            name = lead.get('Company Name', lead.get('Name', '?'))[:40]
            result = lookup_line_type(client, phone_e164)
            lead.update(result)
            lookups_done += 1

            ltype = result['line_type']
            if ltype in stats:
                stats[ltype] += 1
            else:
                stats['unknown'] += 1

            icon = {'mobile': '📱', 'landline': '☎️', 'voip': '🌐'}.get(ltype, '❓')
            print(f"[{i}/{len(leads)}] {name} — {phone_e164} → {icon} {ltype} ({result['carrier']})")

            if ltype == 'mobile':
                mobile_rows.append(lead)

            writer.writerow(lead)

            # Rate limit: Twilio allows 100/sec but let's be safe
            if lookups_done % 50 == 0:
                print(f"\n--- Progress: {lookups_done} lookups | Cost so far: ${lookups_done * cost_per_lookup:.2f} ---\n")
                time.sleep(0.5)

        # Write mobile-only file
        if args.mobile_only and mobile_rows:
            with open(args.mobile_only, 'w', newline='', encoding='utf-8') as f_mob:
                mob_writer = csv.DictWriter(f_mob, fieldnames=out_fields, extrasaction='ignore')
                mob_writer.writeheader()
                for row in mobile_rows:
                    mob_writer.writerow(row)

    # Summary
    total_cost = lookups_done * cost_per_lookup
    print("\n" + "=" * 60)
    print("LINE TYPE CHECK COMPLETE")
    print("=" * 60)
    print(f"  Total leads:     {len(leads)}")
    print(f"  Lookups done:    {lookups_done}")
    print(f"  Cost:            ${total_cost:.2f}")
    print(f"")
    print(f"  📱 Mobile:       {stats['mobile']}  ← SAFE TO SMS")
    print(f"  ☎️  Landline:     {stats['landline']}  ← DO NOT SMS")
    print(f"  🌐 VoIP:         {stats['voip']}  ← RISKY")
    print(f"  ❓ Unknown:      {stats['unknown']}")
    print(f"  ⏭️  Skipped:      {stats['skipped']}")
    print(f"  ❌ Errors:       {stats['error']}")
    print(f"")
    print(f"  Output:          {args.output}")
    if args.mobile_only:
        print(f"  Mobile-only:     {args.mobile_only} ({stats['mobile']} leads)")
    print("=" * 60)


if __name__ == "__main__":
    main()
