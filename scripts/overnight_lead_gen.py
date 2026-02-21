#!/usr/bin/env python3
"""
Overnight lead gen — fill thin niches in East DFW corridor.
Runs against Outscraper API with full enrichment.
"""

import os
import csv
import json
import time
import sys
from datetime import datetime
from outscraper import ApiClient

API_KEY = 'N2U3MTY4ZjU2NGMwNGEyOTk4MTZkYzNlYzQ1OTIzYTB8OTM3ZTc1MTA5YQ'
OUTPUT_DIR = '/home/plotting1/frankie-bot/workspace/leads'
LOG_FILE = '/home/plotting1/.openclaw/workspace/scripts/overnight_lead_gen.log'

# East DFW subcities
SUBCITIES = [
    "Royse City, TX", "Rockwall, TX", "Garland, TX", "Mesquite, TX",
    "Greenville, TX", "Terrell, TX", "Forney, TX", "Heath, TX",
    "Rowlett, TX", "Wylie, TX", "Sachse, TX", "Murphy, TX",
    "Fate, TX", "Caddo Mills, TX", "Quinlan, TX", "Commerce, TX",
    "Sulphur Springs, TX", "Tyler, TX", "Canton, TX", "Kaufman, TX"
]

# Thin niches to fill
JOBS = [
    # R1: Plumber 137, Electrician 151, Asphalt 80, Well 56, Tree 109, Epoxy 58, Painting 132 = 723
    # R2: Roofer 187, Pool 100, Garage 89, Foundation 63, Metal 102, Retaining 104 = 645
    # R3: HVAC 213, General 247, Water 114, Septic 51, MedSpa 62, Massage 48 = 735
    # ROUND 4: Remaining from batch config + new niches
    {"niche": "Public adjuster", "folder": "public_adjusters", "limit": 150},
    {"niche": "Estate attorney", "folder": "estate_attorneys", "limit": 150},
    {"niche": "Title company", "folder": "title_companies", "limit": 150},
    {"niche": "Artificial turf installer", "folder": "turf_landscaping", "limit": 150},
    {"niche": "Fence contractor", "folder": "fence_contractors", "limit": 200},
    {"niche": "Concrete contractor", "folder": "concrete_contractors", "limit": 200},
]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

def run_job(client, job):
    niche = job['niche']
    folder = job['folder']
    limit = job['limit']
    
    out_dir = os.path.join(OUTPUT_DIR, folder)
    os.makedirs(out_dir, exist_ok=True)
    
    all_results = []
    
    for city in SUBCITIES:
        query = f"{niche} near {city}"
        log(f"  Searching: {query} (limit {limit // len(SUBCITIES) + 5})")
        
        try:
            results = client.google_maps_search(
                query,
                limit=max(10, limit // len(SUBCITIES) + 5),
                language='en',
                region='us',
                enrichment=[
                    'emails_validator_service',
                    'phones_enricher_service',
                    'company_insights_service',
                ]
            )
            
            if results and isinstance(results, list):
                # Flatten if nested
                for r in results:
                    if isinstance(r, list):
                        all_results.extend(r)
                    elif isinstance(r, dict):
                        all_results.append(r)
            
            log(f"    Got {len(results[0]) if results and isinstance(results[0], list) else len(results) if results else 0} results from {city}")
            
            # Rate limit - be nice to the API
            time.sleep(2)
            
        except Exception as e:
            log(f"    ERROR on {city}: {e}")
            time.sleep(5)
            continue
    
    # Deduplicate by place_id or name+phone
    seen = set()
    unique = []
    for r in all_results:
        if not isinstance(r, dict):
            continue
        key = r.get('place_id') or f"{r.get('name','')}_{r.get('phone','')}"
        if key not in seen:
            seen.add(key)
            unique.append(r)
    
    if not unique:
        log(f"  No results for {niche} — skipping")
        return 0
    
    # Write CSV
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    outfile = os.path.join(out_dir, f"{folder}_overnight_{ts}.csv")
    
    # Get all keys
    all_keys = set()
    for r in unique:
        all_keys.update(r.keys())
    all_keys = sorted(all_keys)
    
    with open(outfile, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=all_keys, extrasaction='ignore')
        writer.writeheader()
        for r in unique:
            writer.writerow(r)
    
    log(f"  ✅ {niche}: {len(unique)} unique leads → {outfile}")
    return len(unique)

def main():
    log("=" * 60)
    log("OVERNIGHT LEAD GEN — Starting")
    log(f"Niches: {len(JOBS)}, Cities: {len(SUBCITIES)}")
    log("=" * 60)
    
    client = ApiClient(API_KEY)
    
    total = 0
    for job in JOBS:
        log(f"\n🔍 Starting: {job['niche']} (target: {job['limit']})")
        count = run_job(client, job)
        total += count
        log(f"  Subtotal so far: {total} leads")
        # Pause between niches
        time.sleep(5)
    
    log(f"\n{'=' * 60}")
    log(f"DONE — Total new leads: {total}")
    log(f"{'=' * 60}")

if __name__ == '__main__':
    main()
