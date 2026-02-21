#!/usr/bin/env python3
"""
Lead Filter Script for Human Led AI
Separates mobile-only leads into hot list, preserves all for future campaigns
"""

import pandas as pd
import os
from datetime import datetime

UPLOADS_DIR = "/home/plotting1/frankie-bot/workspace/uploads"
OUTPUT_DIR = "/home/plotting1/frankie-bot/workspace/uploads/filtered"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Key columns to keep for dial list
DIAL_COLUMNS = [
    'name', 'phone', 'phone.phones_enricher.carrier_type',
    'email', 'email.emails_validator.status',
    'website', 'city', 'state_code',
    'rating', 'reviews', 'category', 'subtypes',
    'full_name', 'first_name', 'last_name', 'title',
    'contact_phone', 'contact_phone.phones_enricher.carrier_type'
]

def get_best_mobile(row):
    """Find best mobile number from available phone fields"""
    # Priority: contact_phone (owner cell) > phone (main listing)
    if pd.notna(row.get('contact_phone.phones_enricher.carrier_type')):
        if str(row['contact_phone.phones_enricher.carrier_type']).lower() == 'mobile':
            return row.get('contact_phone'), 'contact_mobile'

    if pd.notna(row.get('phone.phones_enricher.carrier_type')):
        if str(row['phone.phones_enricher.carrier_type']).lower() == 'mobile':
            return row.get('phone'), 'primary_mobile'

    return None, None

def score_lead(row):
    """Score lead quality 0-100"""
    score = 0

    # Has mobile phone (+40)
    phone, phone_type = get_best_mobile(row)
    if phone:
        score += 40

    # Has verified email (+20)
    email_status = str(row.get('email.emails_validator.status', '')).lower()
    if email_status in ['valid', 'deliverable']:
        score += 20
    elif email_status == 'risky':
        score += 10

    # Google reviews (+15 max)
    reviews = row.get('reviews', 0)
    if pd.notna(reviews):
        score += min(15, int(reviews) // 10)

    # Rating (+15 max)
    rating = row.get('rating', 0)
    if pd.notna(rating):
        score += int(float(rating) * 3)

    # Has website (+10)
    if pd.notna(row.get('website')) and str(row.get('website')).strip():
        score += 10

    return min(100, score)

def process_files():
    # Get all Excel files
    files = [f for f in os.listdir(UPLOADS_DIR)
             if f.endswith('.xlsx') and 'Zone.Identifier' not in f]

    all_leads = []
    mobile_leads = []

    print(f"Processing {len(files)} Outscraper files...\n")

    for file in files:
        filepath = os.path.join(UPLOADS_DIR, file)
        df = pd.read_excel(filepath)

        # Extract vertical from filename
        vertical = file.split('_', 2)[-1].replace('.xlsx', '').replace('_+3', '').replace('_+2', '').replace('_+8', '').replace(' (1)', '').replace(' (3)', '')
        df['vertical'] = vertical
        df['source_file'] = file

        # Score each lead
        df['lead_score'] = df.apply(score_lead, axis=1)

        # Identify mobile leads (handle missing columns)
        phone_carrier_col = 'phone.phones_enricher.carrier_type'
        contact_carrier_col = 'contact_phone.phones_enricher.carrier_type'

        mobile_mask = pd.Series([False] * len(df), index=df.index)

        if phone_carrier_col in df.columns:
            mobile_mask = mobile_mask | (df[phone_carrier_col].fillna('').str.lower() == 'mobile')

        if contact_carrier_col in df.columns:
            mobile_mask = mobile_mask | (df[contact_carrier_col].fillna('').str.lower() == 'mobile')

        mobile_count = mobile_mask.sum()
        total = len(df)

        print(f"{vertical}: {total} leads, {mobile_count} mobile ({mobile_count/total*100:.0f}%)")

        all_leads.append(df)
        mobile_leads.append(df[mobile_mask])

    # Combine all
    all_df = pd.concat(all_leads, ignore_index=True)
    mobile_df = pd.concat(mobile_leads, ignore_index=True)

    # Sort by score
    mobile_df = mobile_df.sort_values('lead_score', ascending=False)
    all_df = all_df.sort_values('lead_score', ascending=False)

    # Add email status flag
    all_df['email_verified'] = all_df['email.emails_validator.status'].str.lower().isin(['valid', 'deliverable'])
    mobile_df['email_verified'] = mobile_df['email.emails_validator.status'].str.lower().isin(['valid', 'deliverable'])

    # Select columns that exist
    available_cols = [c for c in DIAL_COLUMNS if c in mobile_df.columns]
    extra_cols = ['vertical', 'lead_score', 'email_verified', 'source_file']
    output_cols = available_cols + extra_cols

    # Save outputs
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')

    # Hot list - mobile only, sorted by score
    hot_file = f"{OUTPUT_DIR}/HOT_LIST_mobile_only_{timestamp}.csv"
    mobile_df[output_cols].to_csv(hot_file, index=False)

    # Full list - all leads for email/retargeting
    full_file = f"{OUTPUT_DIR}/FULL_LIST_all_leads_{timestamp}.csv"
    all_df.to_csv(full_file, index=False)

    # Email list - leads with verified emails regardless of phone
    email_verified = all_df[all_df['email_verified'] == True]
    email_file = f"{OUTPUT_DIR}/EMAIL_LIST_verified_{timestamp}.csv"
    email_verified[output_cols].to_csv(email_file, index=False)

    print(f"\n{'='*50}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*50}")
    print(f"Total leads processed: {len(all_df)}")
    print(f"Mobile phone leads (HOT LIST): {len(mobile_df)}")
    print(f"Verified email leads: {len(email_verified)}")
    print(f"\nFiles created in {OUTPUT_DIR}:")
    print(f"  - HOT_LIST (dial first): {len(mobile_df)} leads")
    print(f"  - FULL_LIST (all campaigns): {len(all_df)} leads")
    print(f"  - EMAIL_LIST (email campaigns): {len(email_verified)} leads")
    print(f"\nTop 10 leads by score:")

    top10 = mobile_df[['name', 'city', 'vertical', 'lead_score', 'reviews']].head(10)
    print(top10.to_string(index=False))

if __name__ == "__main__":
    process_files()
