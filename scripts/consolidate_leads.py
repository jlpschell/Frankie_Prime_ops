#!/usr/bin/env python3
"""
Lead Consolidation Script for Human Led AI
Consolidates, deduplicates, and organizes leads from multiple sources into GHL-ready CSVs
"""

import pandas as pd
import os
import re
from pathlib import Path
import json

# Configuration
BASE_DIR = Path("/home/plotting1/frankie-bot/workspace")
OUTPUT_DIR = BASE_DIR / "leads"

# Source directories
SOURCE_DIRS = [
    BASE_DIR / "jay/human_led_ai/lead_gen/lead-gen-engines/HL-AI Lead GNRTR/output",
    BASE_DIR / "jay/human_led_ai/lead_gen/lead-gen-engines/HL-AI Lead GNRTR1/output",
    BASE_DIR / "jay/human_led_ai/lead_gen/lead-gen-engines/HL-AO Lead GNRTR-VVOBK/output",
    BASE_DIR / "uploads/filtered",
    BASE_DIR / "jay/human_led_ai/lead_gen",
]

# Target GHL columns
GHL_COLUMNS = [
    "First Name", "Last Name", "Phone", "Email",
    "Company Name", "City", "State", "Website", "Tags"
]

# Industry mappings based on file names and content
INDUSTRY_KEYWORDS = {
    "hvac": ["hvac", "heating", "air_conditioning", "ac_repair"],
    "medspas": ["med_spa", "medspa", "medical_spa"],
    "water_damage": ["water_damage", "restoration"],
    "public_adjusters": ["public_adjuster"],
    "estate_attorneys": ["estate_attorney", "estate_planning"],
    "title_companies": ["title_company", "title_companies"],
    "massage_therapy": ["massage", "massage_therapy"],
    "roofers": ["roofer", "roofing"],
    "general_contractors": ["general_contractor", "construction"],
}

def clean_phone(phone):
    """Standardize phone number format"""
    if pd.isna(phone) or phone == '':
        return ''
    phone_str = str(phone)
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone_str)
    # Remove leading 1 if 11 digits
    if len(digits) == 11 and digits.startswith('1'):
        digits = digits[1:]
    # Return 10 digit phone or empty
    if len(digits) == 10:
        return digits
    return ''

def clean_name(name):
    """Clean and normalize name fields"""
    if pd.isna(name) or name == '':
        return ''
    return str(name).strip()

def determine_industry(filename, df=None):
    """Determine industry from filename or content"""
    filename_lower = filename.lower()

    for industry, keywords in INDUSTRY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return industry

    # If we can't determine from filename, return None
    return None

def extract_first_name(value):
    """Extract first name from a full name value"""
    if pd.isna(value) or str(value).strip() == '' or str(value).lower() == 'nan':
        return ''
    name = str(value).strip()
    # Filter out obvious non-name values
    non_names = ['there', 'many', 'every', 'of', 'and', 'the', 'is', 'its', 'when', 'home', 'company', 'business', 'plumbers', 'tx']
    parts = name.split()
    if parts and parts[0].lower() not in non_names and len(parts[0]) > 1:
        return parts[0].title()
    return ''

def extract_last_name(value):
    """Extract last name from a full name value"""
    if pd.isna(value) or str(value).strip() == '' or str(value).lower() == 'nan':
        return ''
    name = str(value).strip()
    parts = name.split()
    # Filter out obvious non-name values
    non_names = ['there', 'many', 'every', 'of', 'and', 'the', 'is', 'its', 'when', 'home', 'company', 'business', 'plumbers', 'tx']
    if len(parts) > 1 and parts[0].lower() not in non_names:
        return ' '.join(parts[1:]).title()
    return ''

def map_columns(df, source_type):
    """Map various source column formats to GHL format"""
    result = pd.DataFrame()

    # Common column mappings
    column_maps = {
        # First Name variations
        'first_name': ['First Name', 'first_name', 'FirstName', 'first name'],
        # Last Name variations
        'last_name': ['Last Name', 'last_name', 'LastName', 'last name'],
        # Phone variations
        'phone': ['Phone', 'phone', 'Phone Number', 'phone_number', 'company_phone'],
        # Email variations
        'email': ['Email', 'email', 'Email Address', 'email_address'],
        # Company variations
        'company': ['Company Name', 'company_name', 'Business Name', 'name', 'Company'],
        # City variations
        'city': ['City', 'city'],
        # State variations
        'state': ['State', 'state', 'state_code'],
        # Website variations
        'website': ['Website', 'website', 'Website URL', 'website_url'],
        # Tags variations
        'tags': ['Tags', 'tags'],
    }

    df_cols_lower = {col.lower(): col for col in df.columns}

    # Extract First Name
    first_name_found = False
    for col in column_maps['first_name']:
        if col in df.columns:
            result['First Name'] = df[col].apply(extract_first_name)
            first_name_found = True
            break
        elif col.lower() in df_cols_lower:
            result['First Name'] = df[df_cols_lower[col.lower()]].apply(extract_first_name)
            first_name_found = True
            break
    if not first_name_found:
        # Try to extract from full_name or Contact Name
        if 'full_name' in df_cols_lower:
            result['First Name'] = df[df_cols_lower['full_name']].apply(extract_first_name)
        elif 'Contact Name' in df.columns:
            result['First Name'] = df['Contact Name'].apply(extract_first_name)
        else:
            result['First Name'] = ''

    # Extract Last Name
    last_name_found = False
    for col in column_maps['last_name']:
        if col in df.columns:
            result['Last Name'] = df[col].apply(extract_last_name)
            last_name_found = True
            break
        elif col.lower() in df_cols_lower:
            result['Last Name'] = df[df_cols_lower[col.lower()]].apply(extract_last_name)
            last_name_found = True
            break
    if not last_name_found:
        # Try to extract from full_name
        if 'full_name' in df_cols_lower:
            result['Last Name'] = df[df_cols_lower['full_name']].apply(extract_last_name)
        elif 'Contact Name' in df.columns:
            result['Last Name'] = df['Contact Name'].apply(extract_last_name)
        else:
            result['Last Name'] = ''

    # Extract Phone
    for col in column_maps['phone']:
        if col in df.columns:
            result['Phone'] = df[col].apply(clean_phone)
            break
        elif col.lower() in df_cols_lower:
            result['Phone'] = df[df_cols_lower[col.lower()]].apply(clean_phone)
            break
    if 'Phone' not in result.columns:
        result['Phone'] = ''

    # Extract Email
    for col in column_maps['email']:
        if col in df.columns:
            result['Email'] = df[col].apply(clean_name)
            break
        elif col.lower() in df_cols_lower:
            result['Email'] = df[df_cols_lower[col.lower()]].apply(clean_name)
            break
    if 'Email' not in result.columns:
        result['Email'] = ''

    # Extract Company Name
    for col in column_maps['company']:
        if col in df.columns:
            result['Company Name'] = df[col].apply(clean_name)
            break
        elif col.lower() in df_cols_lower:
            result['Company Name'] = df[df_cols_lower[col.lower()]].apply(clean_name)
            break
    if 'Company Name' not in result.columns:
        result['Company Name'] = ''

    # Extract City
    for col in column_maps['city']:
        if col in df.columns:
            result['City'] = df[col].apply(clean_name)
            break
        elif col.lower() in df_cols_lower:
            result['City'] = df[df_cols_lower[col.lower()]].apply(clean_name)
            break
    if 'City' not in result.columns:
        result['City'] = ''

    # Extract State
    for col in column_maps['state']:
        if col in df.columns:
            result['State'] = df[col].apply(clean_name)
            break
        elif col.lower() in df_cols_lower:
            result['State'] = df[df_cols_lower[col.lower()]].apply(clean_name)
            break
    if 'State' not in result.columns:
        result['State'] = ''

    # Extract Website
    for col in column_maps['website']:
        if col in df.columns:
            result['Website'] = df[col].apply(clean_name)
            break
        elif col.lower() in df_cols_lower:
            result['Website'] = df[df_cols_lower[col.lower()]].apply(clean_name)
            break
    if 'Website' not in result.columns:
        result['Website'] = ''

    # Extract Tags
    for col in column_maps['tags']:
        if col in df.columns:
            result['Tags'] = df[col].apply(clean_name)
            break
        elif col.lower() in df_cols_lower:
            result['Tags'] = df[df_cols_lower[col.lower()]].apply(clean_name)
            break
    if 'Tags' not in result.columns:
        result['Tags'] = ''

    return result

def read_file(filepath):
    """Read CSV or Excel file and return DataFrame"""
    filepath_str = str(filepath)
    try:
        if filepath_str.endswith('.csv'):
            # Try different encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    return pd.read_csv(filepath, encoding=encoding, on_bad_lines='skip')
                except:
                    continue
            return pd.DataFrame()
        elif filepath_str.endswith('.xlsx') or filepath_str.endswith('.xls'):
            return pd.read_excel(filepath)
        elif filepath_str.endswith('.json'):
            with open(filepath, 'r') as f:
                data = json.load(f)
            if isinstance(data, list):
                return pd.DataFrame(data)
            return pd.DataFrame()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return pd.DataFrame()
    return pd.DataFrame()

def dedupe_leads(df):
    """Deduplicate leads by phone (primary) and company name (secondary)"""
    if df.empty:
        return df

    # First, keep rows with valid phones
    df_with_phone = df[df['Phone'] != ''].copy()
    df_no_phone = df[df['Phone'] == ''].copy()

    # Dedupe by phone number
    if not df_with_phone.empty:
        df_with_phone = df_with_phone.drop_duplicates(subset=['Phone'], keep='first')

    # For rows without phone, dedupe by company name
    if not df_no_phone.empty:
        df_no_phone = df_no_phone[df_no_phone['Company Name'] != '']
        df_no_phone = df_no_phone.drop_duplicates(subset=['Company Name'], keep='first')
        # Remove companies that already have a phone entry
        existing_companies = set(df_with_phone['Company Name'].str.lower().dropna())
        df_no_phone = df_no_phone[~df_no_phone['Company Name'].str.lower().isin(existing_companies)]

    return pd.concat([df_with_phone, df_no_phone], ignore_index=True)

def categorize_outscraper_leads(df):
    """Categorize leads from outscraper based on type/category columns"""
    industries = {}

    if 'type' not in df.columns and 'category' not in df.columns and 'subtypes' not in df.columns:
        return {'general_contractors': df}

    type_col = None
    for col in ['type', 'category', 'subtypes', 'Business Type', 'Services']:
        if col in df.columns:
            type_col = col
            break

    if type_col is None:
        return {'general_contractors': df}

    for idx, row in df.iterrows():
        row_type = str(row.get(type_col, '')).lower()

        # Determine industry
        industry = None
        if 'roofing' in row_type or 'roofer' in row_type:
            industry = 'roofers'
        elif 'hvac' in row_type or 'heating' in row_type or 'air conditioning' in row_type:
            industry = 'hvac'
        elif 'water damage' in row_type or 'restoration' in row_type:
            industry = 'water_damage'
        elif 'general contractor' in row_type or 'construction' in row_type:
            industry = 'general_contractors'
        elif 'public adjuster' in row_type:
            industry = 'public_adjusters'
        elif 'turf' in row_type or 'landscap' in row_type:
            industry = 'turf_landscaping'
        elif 'pool' in row_type or 'swimming' in row_type:
            industry = 'pool_contractors'
        elif 'foundation' in row_type:
            industry = 'foundation_repair'
        elif 'septic' in row_type:
            industry = 'septic_services'
        elif 'garage door' in row_type:
            industry = 'garage_door'
        elif 'tree' in row_type:
            industry = 'tree_service'
        elif 'electric' in row_type:
            industry = 'electricians'
        elif 'plumb' in row_type:
            industry = 'plumbers'
        else:
            industry = 'other_contractors'

        if industry not in industries:
            industries[industry] = []
        industries[industry].append(idx)

    result = {}
    for industry, indices in industries.items():
        result[industry] = df.loc[indices]

    return result

def main():
    print("=" * 60)
    print("Lead Consolidation Script - Human Led AI")
    print("=" * 60)

    # Create output directories
    for industry in list(INDUSTRY_KEYWORDS.keys()) + ['roofers', 'general_contractors', 'turf_landscaping',
                                                        'pool_contractors', 'foundation_repair', 'septic_services',
                                                        'garage_door', 'tree_service', 'electricians', 'plumbers',
                                                        'other_contractors']:
        (OUTPUT_DIR / industry).mkdir(parents=True, exist_ok=True)

    # Collect all leads by industry
    leads_by_industry = {}

    # Process each source directory
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            print(f"Skipping non-existent directory: {source_dir}")
            continue

        print(f"\nProcessing: {source_dir}")

        # Get all CSV and Excel files
        files = list(source_dir.glob("*.csv")) + list(source_dir.glob("*.xlsx"))

        for filepath in files:
            # Skip Zone.Identifier files and files we don't want
            if ':Zone.Identifier' in str(filepath):
                continue
            if 'outreach' in filepath.name.lower():
                continue
            if 'pipeline' in filepath.name.lower():
                continue
            if 'send_log' in filepath.name.lower():
                continue

            print(f"  Reading: {filepath.name}")

            df = read_file(filepath)
            if df.empty:
                print(f"    -> Empty or unreadable")
                continue

            print(f"    -> {len(df)} rows found")

            # Determine industry
            industry = determine_industry(filepath.name)

            # Special handling for the large filtered files - they contain multiple industries
            if 'FULL_LIST' in filepath.name or 'outscraper' in filepath.name.lower():
                print(f"    -> Multi-industry file, categorizing...")
                categorized = categorize_outscraper_leads(df)
                for ind, ind_df in categorized.items():
                    mapped = map_columns(ind_df, 'outscraper')
                    if ind not in leads_by_industry:
                        leads_by_industry[ind] = []
                    leads_by_industry[ind].append(mapped)
                    print(f"       {ind}: {len(mapped)} leads")
                continue

            # Map columns to GHL format
            mapped = map_columns(df, 'standard')

            if industry:
                if industry not in leads_by_industry:
                    leads_by_industry[industry] = []
                leads_by_industry[industry].append(mapped)
            else:
                # Try to determine from content
                if 'general_contractors' not in leads_by_industry:
                    leads_by_industry['general_contractors'] = []
                leads_by_industry['general_contractors'].append(mapped)

    # Also process niches folder xlsx files
    niches_dir = BASE_DIR / "jay/human_led_ai/lead_gen/niches"
    if niches_dir.exists():
        print(f"\nProcessing niches folder: {niches_dir}")
        for filepath in niches_dir.glob("*.xlsx"):
            if ':Zone.Identifier' in str(filepath):
                continue

            print(f"  Reading: {filepath.name}")
            df = read_file(filepath)
            if df.empty:
                continue

            print(f"    -> {len(df)} rows found")

            # Determine industry from filename
            fname_lower = filepath.name.lower()
            if 'public_adjuster' in fname_lower:
                industry = 'public_adjusters'
            elif 'foundation' in fname_lower:
                industry = 'foundation_repair'
            elif 'metal_building' in fname_lower or 'barndo' in fname_lower:
                industry = 'metal_buildings'
            elif 'pool' in fname_lower or 'swimming' in fname_lower:
                industry = 'pool_contractors'
            elif 'turf' in fname_lower:
                industry = 'turf_landscaping'
            elif 'equipment' in fname_lower:
                industry = 'equipment_repair'
            elif 'epoxy' in fname_lower:
                industry = 'epoxy_flooring'
            elif 'retaining_wall' in fname_lower:
                industry = 'retaining_walls'
            elif 'septic' in fname_lower:
                industry = 'septic_services'
            elif 'asphalt' in fname_lower:
                industry = 'asphalt_contractors'
            elif 'well_drilling' in fname_lower:
                industry = 'well_drilling'
            elif 'tree' in fname_lower:
                industry = 'tree_service'
            elif 'garage_door' in fname_lower:
                industry = 'garage_door'
            else:
                industry = 'other_contractors'

            mapped = map_columns(df, 'outscraper')
            if industry not in leads_by_industry:
                leads_by_industry[industry] = []
            leads_by_industry[industry].append(mapped)

    # Combine and dedupe each industry
    print("\n" + "=" * 60)
    print("Combining and Deduplicating Leads")
    print("=" * 60)

    final_counts = {}

    for industry, dfs in leads_by_industry.items():
        if not dfs:
            continue

        # Combine all dataframes
        combined = pd.concat(dfs, ignore_index=True)
        print(f"\n{industry}:")
        print(f"  Raw combined: {len(combined)} leads")

        # Deduplicate
        deduped = dedupe_leads(combined)
        print(f"  After dedup: {len(deduped)} leads")

        # Ensure output directory exists
        output_subdir = OUTPUT_DIR / industry
        output_subdir.mkdir(parents=True, exist_ok=True)

        # Save to CSV
        output_file = output_subdir / f"{industry}_dfw_master.csv"
        deduped.to_csv(output_file, index=False)
        print(f"  Saved to: {output_file}")

        final_counts[industry] = len(deduped)

    # Print summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)

    total = 0
    for industry, count in sorted(final_counts.items()):
        print(f"  {industry}: {count} leads")
        total += count

    print(f"\n  TOTAL: {total} unique leads")
    print("=" * 60)

    return final_counts

if __name__ == "__main__":
    main()
