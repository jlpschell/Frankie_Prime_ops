#!/usr/bin/env python3
"""Upload mobile-verified leads to GHL with tags and identifiers."""
import json
import os
import time
import sys
import requests
from datetime import datetime

# Load env
from dotenv import load_dotenv
load_dotenv("/home/plotting1/frankie-bot/.env")

API_KEY = os.getenv("GHL_API_KEY")
LOCATION_ID = os.getenv("GHL_LOCATION_ID", "tabcgomNBVaWpWAkIXL8")
BASE_URL = os.getenv("GHL_BASE_URL", "https://services.leadconnectorhq.com")

TODAY = datetime.now().strftime("%m-%d-%y")
LOAD_DATE = datetime.now().strftime("%Y-%m-%d")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28",
}

# Load leads
json_file = f"/home/plotting1/.openclaw/workspace/ghl_upload/ghl_mobile_master_{TODAY}.json"
with open(json_file) as f:
    leads = json.load(f)

print(f"Uploading {len(leads)} leads to GHL...")
print(f"Location: {LOCATION_ID}")
print()

created = 0
updated = 0
errors = 0
dupes = 0

for i, lead in enumerate(leads):
    tags = lead['tags'].split(',')
    
    # Build GHL contact payload
    payload = {
        "locationId": LOCATION_ID,
        "phone": lead['phone'],
        "companyName": lead['business_name'],
        "tags": tags,
        "source": "outscraper",
        "customFields": [
            {"key": "niche", "field_value": lead['niche']},
            {"key": "voice_assignment", "field_value": lead['voice']},
            {"key": "carrier_type", "field_value": "mobile"},
            {"key": "load_date", "field_value": LOAD_DATE},
            {"key": "google_rating", "field_value": str(lead.get('rating', ''))},
            {"key": "google_reviews", "field_value": str(lead.get('reviews', ''))},
        ],
    }
    
    if lead.get('email'):
        payload['email'] = lead['email']
    if lead.get('website'):
        payload['website'] = lead['website']
    if lead.get('city'):
        payload['city'] = lead['city']
    if lead.get('state'):
        payload['state'] = lead['state']
    if lead.get('zip'):
        payload['postalCode'] = lead['zip']
    if lead.get('address'):
        payload['address1'] = lead['address']
    if lead.get('first_name'):
        payload['firstName'] = lead['first_name']
    if lead.get('last_name'):
        payload['lastName'] = lead['last_name']
    
    # First check if contact exists by phone
    search_url = f"{BASE_URL}/contacts/search"
    search_payload = {
        "locationId": LOCATION_ID,
        "filters": [
            {
                "field": "phone",
                "operator": "eq",
                "value": lead['phone']
            }
        ]
    }
    
    try:
        # Try to create - GHL will return 400 if dupe phone
        resp = requests.post(f"{BASE_URL}/contacts/", headers=HEADERS, json=payload)
        
        if resp.status_code == 200:
            created += 1
            contact_id = resp.json().get('contact', {}).get('id', 'unknown')
            if (i + 1) % 25 == 0:
                print(f"  [{i+1}/{len(leads)}] Created {created} | Dupes {dupes} | Errors {errors}")
        elif resp.status_code == 400 and 'duplicate' in resp.text.lower():
            dupes += 1
            # Try to find and update with new tags
            lookup = requests.get(
                f"{BASE_URL}/contacts/lookup?phone={lead['phone']}&locationId={LOCATION_ID}",
                headers=HEADERS
            )
            if lookup.status_code == 200:
                contacts = lookup.json().get('contacts', [])
                if contacts:
                    cid = contacts[0]['id']
                    # Update tags
                    update_payload = {"tags": tags}
                    requests.put(f"{BASE_URL}/contacts/{cid}", headers=HEADERS, json=update_payload)
                    updated += 1
        else:
            errors += 1
            if errors <= 3:
                print(f"  ERROR [{resp.status_code}]: {resp.text[:200]}")
        
        # Rate limit: GHL allows ~100 req/min
        time.sleep(0.7)
        
    except Exception as e:
        errors += 1
        if errors <= 3:
            print(f"  EXCEPTION: {e}")
        time.sleep(1)

print(f"\n{'='*50}")
print(f"✅ UPLOAD COMPLETE")
print(f"  Created: {created}")
print(f"  Updated (dupes with new tags): {updated}")
print(f"  Duplicates: {dupes}")
print(f"  Errors: {errors}")
print(f"  Total processed: {len(leads)}")
