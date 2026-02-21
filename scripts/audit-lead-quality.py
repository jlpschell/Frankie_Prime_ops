#!/usr/bin/env python3
"""
Lead Data Quality Audit
Analyzes CSV files in leads/ and ghl_import/ for contact data completeness
"""

import csv
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Campaign-ready niches mapped to directory names
NICHE_MAP = {
    'water-damage': 'water_damage',
    'general-contractors': 'general_contractors',
    'septic': 'septic_services',
    'turf': 'turf_landscaping',
    'garage-doors': 'garage_door',
    'pool-builders': 'pool_contractors',
    'concrete': 'other_contractors',  # checking for concrete in other_contractors
    'floor-coating': 'epoxy_flooring',
    'steel-metal': 'metal_buildings',
    'medspa': 'medspas',
    'roofing': 'roofers',
    'hvac': 'hvac',
    'painters': 'other_contractors'  # may need to check
}

GHL_MAP = {
    'water-damage': 'water-damage_ghl_import.csv',
    'septic': 'septic_ghl_import.csv',
    'turf': 'turf_ghl_import.csv',
    'garage-doors': 'garage-door_ghl_import.csv',
    'pool-builders': 'pool-builder_ghl_import.csv',
    'concrete': 'concrete_ghl_import.csv',
    'floor-coating': 'floor-coating_ghl_import.csv',
    'steel-metal': 'steel-construction_ghl_import.csv',
    'roofing': 'roofing_ghl_import.csv',
}

def analyze_csv(file_path: str) -> Dict:
    """Analyze a single CSV file for contact data quality"""
    if not os.path.exists(file_path):
        return None

    stats = {
        'total': 0,
        'has_email': 0,
        'has_phone': 0,
        'has_website': 0,
        'has_name': 0
    }

    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.DictReader(f)

            for row in reader:
                stats['total'] += 1

                # Check for email (multiple possible column names)
                email = row.get('email', '') or row.get('Email', '') or row.get('EMAIL', '')
                if email and email.strip() and '@' in email:
                    stats['has_email'] += 1

                # Check for phone (multiple possible column names)
                phone = (row.get('phone', '') or row.get('Phone', '') or
                        row.get('phone_number', '') or row.get('Phone Number', ''))
                if phone and phone.strip() and len(phone.strip()) >= 10:
                    stats['has_phone'] += 1

                # Check for website
                website = (row.get('website', '') or row.get('Website', '') or
                          row.get('url', '') or row.get('URL', ''))
                if website and website.strip():
                    stats['has_website'] += 1

                # Check for name
                name = (row.get('name', '') or row.get('Name', '') or
                       row.get('business_name', '') or row.get('Business Name', ''))
                if name and name.strip():
                    stats['has_name'] += 1

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    return stats

def calculate_percentages(stats: Dict) -> Dict:
    """Calculate percentage completeness"""
    if not stats or stats['total'] == 0:
        return None

    total = stats['total']
    return {
        'total': total,
        'email_pct': round((stats['has_email'] / total) * 100, 1),
        'phone_pct': round((stats['has_phone'] / total) * 100, 1),
        'website_pct': round((stats['has_website'] / total) * 100, 1),
        'name_pct': round((stats['has_name'] / total) * 100, 1),
        'email_count': stats['has_email'],
        'phone_count': stats['has_phone']
    }

def assess_quality(pct_data: Dict) -> Tuple[str, int]:
    """
    Assess overall data quality and ROI potential
    Returns (grade, roi_score)
    """
    if not pct_data:
        return 'N/A', 0

    # Average of email and phone coverage (most important)
    avg_contact = (pct_data['email_pct'] + pct_data['phone_pct']) / 2

    # Quality grade
    if avg_contact >= 80:
        grade = 'A'
    elif avg_contact >= 60:
        grade = 'B'
    elif avg_contact >= 40:
        grade = 'C'
    elif avg_contact >= 20:
        grade = 'D'
    else:
        grade = 'F'

    # ROI score: bigger list with worse data = higher ROI for enrichment
    # Scale: 0-100 based on (list size) * (missing contact %)
    missing_pct = 100 - avg_contact
    roi_score = int((pct_data['total'] / 100) * missing_pct)

    return grade, roi_score

def main():
    workspace = Path('/home/plotting1/frankie-bot/workspace')
    leads_dir = workspace / 'leads'
    ghl_dir = workspace / 'ghl_import'

    results = []

    print("\n" + "="*100)
    print("LEAD DATA QUALITY AUDIT")
    print("="*100 + "\n")

    # Analyze each campaign-ready niche
    for niche_name in ['water-damage', 'general-contractors', 'septic', 'turf',
                       'garage-doors', 'pool-builders', 'concrete', 'floor-coating',
                       'steel-metal', 'medspa', 'roofing', 'hvac']:

        # Check leads/ directory
        leads_stats = None
        niche_dir = NICHE_MAP.get(niche_name)
        if niche_dir:
            niche_path = leads_dir / niche_dir
            if niche_path.exists():
                # Find master CSV (usually largest or most recent)
                csv_files = list(niche_path.glob('*.csv'))
                if csv_files:
                    # Use the largest CSV as the master
                    master_csv = max(csv_files, key=lambda f: f.stat().st_size)
                    leads_stats = analyze_csv(str(master_csv))

        # Check ghl_import/ directory
        ghl_stats = None
        ghl_file = GHL_MAP.get(niche_name)
        if ghl_file:
            ghl_path = ghl_dir / ghl_file
            ghl_stats = analyze_csv(str(ghl_path))

        # Use whichever source has more data
        if leads_stats and ghl_stats:
            main_stats = leads_stats if leads_stats['total'] >= ghl_stats['total'] else ghl_stats
            source = 'leads/' if leads_stats['total'] >= ghl_stats['total'] else 'ghl_import/'
        elif leads_stats:
            main_stats = leads_stats
            source = 'leads/'
        elif ghl_stats:
            main_stats = ghl_stats
            source = 'ghl_import/'
        else:
            main_stats = None
            source = 'N/A'

        pct_data = calculate_percentages(main_stats)
        grade, roi_score = assess_quality(pct_data)

        if pct_data:
            results.append({
                'niche': niche_name,
                'source': source,
                'total': pct_data['total'],
                'email_pct': pct_data['email_pct'],
                'phone_pct': pct_data['phone_pct'],
                'website_pct': pct_data['website_pct'],
                'grade': grade,
                'roi_score': roi_score
            })

    # Sort by ROI score (highest first)
    results.sort(key=lambda x: x['roi_score'], reverse=True)

    # Print summary table
    print(f"{'NICHE':<20} {'SOURCE':<15} {'LEADS':<8} {'EMAIL %':<10} {'PHONE %':<10} {'WEB %':<10} {'GRADE':<8} {'ROI':<6}")
    print("-" * 100)

    for r in results:
        print(f"{r['niche']:<20} {r['source']:<15} {r['total']:<8} "
              f"{r['email_pct']:<10.1f} {r['phone_pct']:<10.1f} {r['website_pct']:<10.1f} "
              f"{r['grade']:<8} {r['roi_score']:<6}")

    print("\n" + "="*100)
    print("ENRICHMENT PRIORITY (Top 3):")
    print("="*100 + "\n")

    for i, r in enumerate(results[:3], 1):
        avg_contact = (r['email_pct'] + r['phone_pct']) / 2
        missing_pct = 100 - avg_contact
        print(f"{i}. {r['niche'].upper()}")
        print(f"   - List size: {r['total']:,} leads")
        print(f"   - Contact coverage: {avg_contact:.1f}%")
        print(f"   - Missing contacts: {missing_pct:.1f}% ({int(r['total'] * missing_pct / 100):,} leads)")
        print(f"   - Data grade: {r['grade']}")
        print(f"   - ROI score: {r['roi_score']}/100")
        print()

    print("="*100)
    print("\nROI Score Formula: (List Size / 100) × Missing Contact %")
    print("Higher score = Bigger list with more gaps = Best enrichment ROI\n")

if __name__ == '__main__':
    main()
