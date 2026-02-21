#!/usr/bin/env python3
"""
Detailed gap analysis for top enrichment candidates
Shows exactly what's missing and what we have
"""

import csv
from pathlib import Path

def analyze_gaps(csv_path: str, niche_name: str):
    """Show detailed breakdown of missing data"""
    if not csv_path or not Path(csv_path).exists():
        print(f"\nFile not found: {csv_path}")
        return

    stats = {
        'total': 0,
        'has_both': 0,
        'email_only': 0,
        'phone_only': 0,
        'neither': 0,
        'missing_email': 0,
        'missing_phone': 0
    }

    with open(csv_path, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.DictReader(f)

        for row in reader:
            stats['total'] += 1

            # Check email
            email = row.get('email', '') or row.get('Email', '') or row.get('EMAIL', '')
            has_email = bool(email and email.strip() and '@' in email)

            # Check phone
            phone = (row.get('phone', '') or row.get('Phone', '') or
                    row.get('phone_number', '') or row.get('Phone Number', ''))
            has_phone = bool(phone and phone.strip() and len(phone.strip()) >= 10)

            # Categorize
            if has_email and has_phone:
                stats['has_both'] += 1
            elif has_email and not has_phone:
                stats['email_only'] += 1
            elif has_phone and not has_email:
                stats['phone_only'] += 1
            else:
                stats['neither'] += 1

            if not has_email:
                stats['missing_email'] += 1
            if not has_phone:
                stats['missing_phone'] += 1

    print(f"\n{'='*80}")
    print(f"{niche_name.upper()} — DETAILED GAP ANALYSIS")
    print(f"{'='*80}\n")

    print(f"Total Leads: {stats['total']:,}\n")

    print("CONTACT DATA BREAKDOWN:")
    print(f"  ✓ Both email + phone:  {stats['has_both']:>4} ({stats['has_both']/stats['total']*100:>5.1f}%)")
    print(f"  ⚠ Email only:          {stats['email_only']:>4} ({stats['email_only']/stats['total']*100:>5.1f}%)")
    print(f"  ⚠ Phone only:          {stats['phone_only']:>4} ({stats['phone_only']/stats['total']*100:>5.1f}%)")
    print(f"  ✗ Neither:             {stats['neither']:>4} ({stats['neither']/stats['total']*100:>5.1f}%)")

    print(f"\nENRICHMENT TARGETS:")
    print(f"  Missing emails:        {stats['missing_email']:>4} ({stats['missing_email']/stats['total']*100:>5.1f}%)")
    print(f"  Missing phones:        {stats['missing_phone']:>4} ({stats['missing_phone']/stats['total']*100:>5.1f}%)")

    # Enrichment potential
    easy_enrichment = stats['phone_only']  # Have phone, just need email lookup
    hard_enrichment = stats['neither']     # Need both (website scrape or paid service)

    print(f"\nENRICHMENT STRATEGY:")
    print(f"  Easy (reverse phone → email):     {easy_enrichment:>4} leads")
    print(f"  Hard (need both or scrape site):  {hard_enrichment:>4} leads")

    return stats

def main():
    workspace = Path('/home/plotting1/frankie-bot/workspace')

    # Top 3 niches from audit
    targets = [
        ('water-damage', workspace / 'leads' / 'water_damage'),
        ('septic', workspace / 'leads' / 'septic_services'),
        ('garage-doors', workspace / 'leads' / 'garage_door')
    ]

    for niche_name, niche_dir in targets:
        if niche_dir.exists():
            csv_files = list(niche_dir.glob('*.csv'))
            if csv_files:
                master_csv = max(csv_files, key=lambda f: f.stat().st_size)
                analyze_gaps(str(master_csv), niche_name)

    print(f"\n{'='*80}\n")

if __name__ == '__main__':
    main()
