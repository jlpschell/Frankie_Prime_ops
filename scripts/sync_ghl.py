#!/usr/bin/env python3
"""Sync mobile-verified leads from Supabase master_leads → GHL"""
import requests, json, time, re, os
from datetime import date

with open('/home/plotting1/frankie-bot/.env') as f:
    env = {}
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v.strip('"').strip("'")

GHL_KEY = env['GHL_API_KEY']
SB_URL = env['SUPABASE_URL']
SB_KEY = env['SUPABASE_SERVICE_ROLE_KEY']
LOCATION = "tabcgomNBVaWpWAkIXL8"

ghl_headers = {"Authorization": f"Bearer {GHL_KEY}", "Version": "2021-07-28", "Content-Type": "application/json"}
sb_headers = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json"}

today = date.today().strftime("%m-%d-%y")

# Fetch leads not yet uploaded, mobile verified
resp = requests.get(
    f"{SB_URL}/rest/v1/master_leads?uploaded_to_ghl=eq.false&mobile_verified=eq.true&select=*&limit=500",
    headers=sb_headers
)

if resp.status_code != 200:
    print(f"Supabase error: {resp.status_code} {resp.text[:200]}")
    exit(1)

leads = resp.json()
print(f"Found {len(leads)} mobile-verified leads to upload to GHL")

uploaded = 0
errors = 0
dupes = 0

for lead in leads:
    niche = lead.get('niche', 'unknown')
    tags = [niche, f'{niche}_{today}', 'cold-outreach', f'load-{today}', 'mobile-verified', 'voice-eric']
    
    contact = {
        "locationId": LOCATION,
        "phone": lead['phone'],
        "tags": tags,
    }
    if lead.get('company_name'):
        contact["companyName"] = lead['company_name']
        contact["name"] = lead['company_name'].lower()
    if lead.get('email'):
        contact["email"] = lead['email']
    if lead.get('website'):
        contact["website"] = lead['website']
    
    r = requests.post("https://services.leadconnectorhq.com/contacts/", headers=ghl_headers, json=contact)
    
    if r.status_code in [200, 201]:
        ghl_id = r.json().get('contact', {}).get('id')
        # Update Supabase
        requests.patch(
            f"{SB_URL}/rest/v1/master_leads?id=eq.{lead['id']}",
            headers=sb_headers,
            json={"uploaded_to_ghl": True, "ghl_contact_id": ghl_id, "ghl_upload_date": "now()"}
        )
        uploaded += 1
    elif r.status_code == 400 and 'duplicate' in r.text.lower():
        # Mark as uploaded (already exists)
        requests.patch(
            f"{SB_URL}/rest/v1/master_leads?id=eq.{lead['id']}",
            headers=sb_headers,
            json={"uploaded_to_ghl": True}
        )
        dupes += 1
    else:
        errors += 1
        if errors <= 5:
            print(f"  ERROR: {r.status_code} {r.text[:100]}")
    
    time.sleep(0.15)

print(f"\nDONE. Uploaded: {uploaded} | Already in GHL: {dupes} | Errors: {errors}")
