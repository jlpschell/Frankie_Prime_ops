#!/usr/bin/env python3
"""
Split master lead list into GHL-ready CSVs by niche.
Output format matches GHL contact import requirements.
"""

import csv
import os
import re
from collections import defaultdict

INPUT_FILE = "/home/plotting1/frankie-bot/workspace/uploads/filtered/FULL_LIST_all_leads_20260209_0029.csv"
OUTPUT_DIR = "/home/plotting1/frankie-bot/workspace/ghl_import"

# GHL required columns mapping (source -> GHL name)
GHL_COLUMNS = [
    "First Name",
    "Last Name",
    "Company Name",
    "Phone",
    "Email",
    "Address",
    "City",
    "State",
    "Postal Code",
    "Website",
    "Tags"
]

def normalize_niche(query):
    """Convert query string to clean niche name for tagging."""
    if not query:
        return "unknown"

    # Remove quotes and clean up
    clean = query.strip('"').strip().lower()

    # Normalize similar niches
    niche_map = {
        "septic tank installer": "septic",
        "septic system service": "septic",
        "pool builder": "pool-builder",
        "concrete contractor": "concrete",
        "water damage restoration service": "water-damage",
        "turf installation": "turf",
        "artificial turf installer": "turf",
        "artificial grass installer": "turf",
        "synthetic grass installer": "turf",
        "steel construction company": "steel-construction",
        "metal construction company": "steel-construction",
        "retaining wall contractor": "retaining-wall",
        "garage door service": "garage-door",
        "garage door repair": "garage-door",
        "repairgarage door service": "garage-door",
        "overhead door": "garage-door",
        "hardscape contractor": "hardscape",
        "heavy equipment repair": "heavy-equipment",
        "mobile equipment repair": "heavy-equipment",
        "fire damage restoration service": "fire-damage",
        "tree removal": "tree-service",
        "tree service": "tree-service",
        "industrial floor coating": "floor-coating",
        "epoxy floor coating": "floor-coating",
        "mold remediation": "mold-remediation",
        "asphalt paving": "asphalt",
    }

    for key, value in niche_map.items():
        if key in clean:
            return value

    # Default: slugify the query
    slug = re.sub(r'[^a-z0-9]+', '-', clean).strip('-')
    return slug[:30] if slug else "unknown"

def extract_first_name(row):
    """Extract first name from row data."""
    if row.get('first_name'):
        return row['first_name']
    full_name = row.get('full_name', '') or row.get('name_for_emails', '')
    if full_name:
        parts = full_name.strip().split()
        return parts[0] if parts else ''
    return ''

def extract_last_name(row):
    """Extract last name from row data."""
    if row.get('last_name'):
        return row['last_name']
    full_name = row.get('full_name', '') or row.get('name_for_emails', '')
    if full_name:
        parts = full_name.strip().split()
        return ' '.join(parts[1:]) if len(parts) > 1 else ''
    return ''

def get_best_phone(row):
    """Get the best phone number available."""
    # Priority: contact_phone > phone > company_phone
    for field in ['contact_phone', 'phone', 'company_phone']:
        phone = row.get(field, '')
        if phone and phone.strip():
            # Clean phone number
            cleaned = re.sub(r'[^\d+]', '', phone)
            if len(cleaned) >= 10:
                return cleaned
    return ''

def process_leads():
    """Read master list and split by niche."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group leads by niche
    niches = defaultdict(list)

    with open(INPUT_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)

        for row in reader:
            niche = normalize_niche(row.get('query', ''))

            # Build GHL-formatted row
            ghl_row = {
                "First Name": extract_first_name(row),
                "Last Name": extract_last_name(row),
                "Company Name": row.get('name', '') or row.get('company_name', ''),
                "Phone": get_best_phone(row),
                "Email": row.get('email', ''),
                "Address": row.get('street', '') or row.get('address', ''),
                "City": row.get('city', ''),
                "State": row.get('state_code', '') or row.get('state', ''),
                "Postal Code": row.get('postal_code', ''),
                "Website": row.get('website', '') or row.get('domain', ''),
                "Tags": f"{niche}-campaign,human-led-ai,dfw"
            }

            # Only include if we have a phone number
            if ghl_row["Phone"]:
                niches[niche].append(ghl_row)

    # Write separate CSV for each niche
    summary = []

    for niche, leads in sorted(niches.items(), key=lambda x: -len(x[1])):
        filename = f"{niche}_ghl_import.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=GHL_COLUMNS)
            writer.writeheader()
            writer.writerows(leads)

        summary.append((niche, len(leads), filename))
        print(f"✓ {niche}: {len(leads)} leads -> {filename}")

    # Write summary
    print(f"\n{'='*50}")
    print(f"TOTAL: {sum(len(leads) for leads in niches.values())} leads across {len(niches)} niches")
    print(f"Output directory: {OUTPUT_DIR}")

    return summary

if __name__ == "__main__":
    process_leads()
