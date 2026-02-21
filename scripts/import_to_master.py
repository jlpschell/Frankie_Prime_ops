#!/usr/bin/env python3
"""Import Outscraper .xlsx files into Supabase master_leads (dedup by phone)"""
import openpyxl, re, os, sys, glob, requests, json, time
from datetime import date

with open('/home/plotting1/frankie-bot/.env') as f:
    env = {}
    for line in f:
        if '=' in line and not line.startswith('#'):
            k, v = line.strip().split('=', 1)
            env[k] = v.strip('"').strip("'")

SB_URL = env['SUPABASE_URL']
SB_KEY = env['SUPABASE_SERVICE_ROLE_KEY']
sb_headers = {"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Content-Type": "application/json", "Prefer": "resolution=merge-duplicates"}

FILE_NICHE_MAP = {
    "water_damage": "water-damage", "artificial_turf": "artificial-turf",
    "septic_system": "septic", "asphalt_contractor": "asphalt",
    "well_drilling": "well-drilling", "swimming_pool": "swimming-pool",
    "garage_door": "garage-door", "tree_service": "tree-service",
    "epoxy_floor": "epoxy", "retaining_wall": "retaining-wall",
    "metal_buildings": "metal-buildings", "foundation_repair": "foundation-repair",
    "heavy_equipment": "heavy-equipment", "roofer": "roofer", "hvac": "hvac",
    "electrician": "electrician", "plumber": "plumber", "concrete": "concrete",
    "fence": "fence", "landscaping": "landscaping", "general_contractor": "general-contractor",
    "pest_control": "pest-control", "medspa": "medspa", "med_spa": "medspa",
    "attorney": "attorney",
}

def get_niche(fname):
    for pattern, tag in FILE_NICHE_MAP.items():
        if pattern in fname.lower():
            return tag
    return None

def normalize_phone(phone):
    if not phone: return None
    digits = re.sub(r'[^\d]', '', str(phone))
    if len(digits) == 10: return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith('1'): return f"+{digits}"
    return None

def is_mobile(row, hmap):
    for col in ['phone.phones_enricher.carrier_type','company_phone.phones_enricher.carrier_type','contact_phone.phones_enricher.carrier_type']:
        if col in hmap:
            val = row[hmap[col]] if hmap[col] < len(row) else None
            if val and str(val).strip().lower() == 'mobile':
                return True, 'mobile'
    for col in ['phone.whitepages_phones.lookup_type','phone_1.whitepages_phones.lookup_type']:
        if col in hmap:
            val = row[hmap[col]] if hmap[col] < len(row) else None
            if val and ('cell' in str(val).lower() or 'mobile' in str(val).lower()):
                return True, 'mobile'
    return False, None

def process_file(fpath):
    fname = os.path.basename(fpath)
    niche = get_niche(fname)
    if not niche:
        print(f"  SKIP (no niche): {fname}")
        return 0
    
    wb = openpyxl.load_workbook(fpath, read_only=True)
    ws = wb.active
    rows = list(ws.iter_rows())
    if not rows:
        wb.close()
        return 0
    
    headers = [c.value for c in rows[0]]
    hmap = {h: i for i, h in enumerate(headers) if h}
    phone_col = hmap.get('phone')
    name_col = hmap.get('name')
    email_col = hmap.get('email') or hmap.get('email_1')
    site_col = hmap.get('site') or hmap.get('website')
    
    if phone_col is None:
        wb.close()
        return 0
    
    batch = []
    today_str = date.today().isoformat()
    
    for row_cells in rows[1:]:
        row = [c.value for c in row_cells]
        phone = normalize_phone(row[phone_col] if phone_col < len(row) else None)
        if not phone: continue
        
        mobile, carrier = is_mobile(row, hmap)
        company = str(row[name_col]).strip() if name_col and name_col < len(row) and row[name_col] else ''
        email = str(row[email_col]).strip() if email_col and email_col < len(row) and row[email_col] else ''
        website = str(row[site_col]).strip() if site_col and site_col < len(row) and row[site_col] else ''
        
        batch.append({
            "phone": phone,
            "company_name": company if company != 'None' else '',
            "email": email if email != 'None' and '@' in email else '',
            "website": website if website != 'None' else '',
            "niche": niche,
            "source": "outscraper",
            "source_date": today_str,
            "carrier_type": carrier,
            "mobile_verified": mobile,
            "uploaded_to_ghl": False,
            "tags": [niche, f'{niche}_{today_str}', 'cold-outreach']
        })
    
    wb.close()
    
    if batch:
        r = requests.post(f"{SB_URL}/rest/v1/master_leads", headers=sb_headers, json=batch)
        if r.status_code in [200, 201]:
            print(f"  {niche}: {len(batch)} leads imported")
            return len(batch)
        else:
            print(f"  {niche}: ERROR {r.status_code} {r.text[:200]}")
            return 0
    return 0

# Main
upload_dir = sys.argv[1] if len(sys.argv) > 1 else '/home/plotting1/frankie-bot/workspace/uploads'
files = sorted(glob.glob(os.path.join(upload_dir, 'Outscraper-*.xlsx')))
print(f"Found {len(files)} Outscraper files in {upload_dir}")

total = 0
for f in files:
    total += process_file(f)

print(f"\nDONE. Total imported/updated: {total}")
