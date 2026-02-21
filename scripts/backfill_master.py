#!/usr/bin/env python3
"""Backfill master_leads from existing GHL contacts"""
import requests, json, time, re, os

# Load keys
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

ghl_headers = {"Authorization": f"Bearer {GHL_KEY}", "Version": "2021-07-28"}
sb_headers = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"}

# Known niche tags
NICHE_TAGS = {
    'roofer','hvac','electrician','plumber','concrete','fence','landscaping',
    'general-contractor','medspa','med-spa','med spa','attorney','estate_attorney',
    'pest-control','garage-door','garage door','artificial-turf','artificial turf',
    'asphalt','heavy-equipment','heavy equipment','metal-buildings','metal buildings',
    'swimming-pool','swimming pool','tree-service','tree service','septic',
    'water-damage','water damage','massage','public adjusters','foundation-repair',
    'retaining-wall','epoxy','well-drilling','roofing'
}

def detect_niche(tags):
    for t in tags:
        if t.lower() in NICHE_TAGS:
            return t.lower()
    # Try parsing from date tags like roofers_02-16-26
    for t in tags:
        parts = t.split('_')
        if len(parts) >= 2 and any(c.isdigit() for c in parts[-1]):
            prefix = parts[0].lower()
            niche_map = {
                'roofers':'roofer','hvac':'hvac','electricians':'electrician',
                'plumbers':'plumber','concrete':'concrete','fence':'fence',
                'landscaping':'landscaping','general':'general-contractor',
                'pest':'pest-control','garage':'garage-door','medspas':'medspa',
                'attorneys':'attorney'
            }
            if prefix in niche_map:
                return niche_map[prefix]
    return 'unknown'

def normalize_phone(phone):
    if not phone: return None
    digits = re.sub(r'[^\d]', '', str(phone))
    if len(digits) == 10: return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith('1'): return f"+{digits}"
    return None

# Paginate all GHL contacts
start_after = None
start_after_id = None
total = 0
inserted = 0
skipped = 0
batch = []
BATCH_SIZE = 50

while True:
    url = f"https://services.leadconnectorhq.com/contacts/?locationId={LOCATION}&limit=100"
    if start_after and start_after_id:
        url += f"&startAfter={start_after}&startAfterId={start_after_id}"
    
    resp = requests.get(url, headers=ghl_headers)
    if resp.status_code != 200:
        print(f"GHL error: {resp.status_code}")
        break
    
    data = resp.json()
    contacts = data.get('contacts', [])
    if not contacts:
        break
    
    for c in contacts:
        total += 1
        phone = normalize_phone(c.get('phone'))
        if not phone:
            skipped += 1
            continue
        
        tags = c.get('tags', [])
        niche = detect_niche(tags)
        is_mobile = 'mobile-verified' in tags
        
        row = {
            "phone": phone,
            "company_name": c.get('companyName') or c.get('contactName') or '',
            "email": c.get('email') or '',
            "website": c.get('website') or '',
            "niche": niche,
            "source": "ghl-backfill",
            "carrier_type": "mobile" if is_mobile else None,
            "mobile_verified": is_mobile,
            "uploaded_to_ghl": True,
            "ghl_contact_id": c.get('id'),
            "tags": tags
        }
        batch.append(row)
    
    # Flush batch
    if len(batch) >= BATCH_SIZE:
        r = requests.post(f"{SB_URL}/rest/v1/master_leads", headers=sb_headers, json=batch)
        if r.status_code in [200, 201]:
            inserted += len(batch)
        else:
            print(f"Supabase error: {r.status_code} {r.text[:200]}")
        batch = []
        time.sleep(0.1)
    
    meta = data.get('meta', {})
    start_after = meta.get('startAfter')
    start_after_id = meta.get('startAfterId')
    if not meta.get('nextPage'):
        break

# Flush remaining
if batch:
    r = requests.post(f"{SB_URL}/rest/v1/master_leads", headers=sb_headers, json=batch)
    if r.status_code in [200, 201]:
        inserted += len(batch)
    else:
        print(f"Supabase error: {r.status_code} {r.text[:200]}")

print(f"\nDONE. GHL contacts scanned: {total} | Inserted to master_leads: {inserted} | Skipped (no phone): {skipped}")
