#!/usr/bin/env python3
"""
GHL Contact Importer - Push leads directly to GoHighLevel via API
"""
import requests
import csv
import sys
import time
from pathlib import Path

# GHL Configuration (rotated 2/8/25)
GHL_API_KEY = "pit-ff293406-83dd-4ce3-a7d7-9b1c66c94f40"
GHL_LOCATION_ID = "tabcgomNBVaWpWAkIXL8"
GHL_BASE_URL = "https://services.leadconnectorhq.com"

HEADERS = {
    "Authorization": f"Bearer {GHL_API_KEY}",
    "Content-Type": "application/json",
    "Version": "2021-07-28"
}


def format_phone(phone):
    """Format phone to E.164 (+1XXXXXXXXXX)"""
    if not phone:
        return None
    # Strip non-digits
    digits = ''.join(c for c in str(phone) if c.isdigit())
    if len(digits) == 10:
        return f"+1{digits}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"+{digits}"
    return None


def create_contact(contact_data):
    """Create or update a contact in GHL (upsert)"""
    url = f"{GHL_BASE_URL}/contacts/upsert"

    payload = {
        "locationId": GHL_LOCATION_ID,
    }

    # Add fields if they exist
    if contact_data.get('firstName'):
        payload['firstName'] = contact_data['firstName']
    if contact_data.get('lastName'):
        payload['lastName'] = contact_data['lastName']
    if contact_data.get('phone'):
        formatted = format_phone(contact_data['phone'])
        if formatted:
            payload['phone'] = formatted
    if contact_data.get('email'):
        payload['email'] = contact_data['email']
    if contact_data.get('companyName'):
        payload['companyName'] = contact_data['companyName']
    if contact_data.get('city'):
        payload['city'] = contact_data['city']
    if contact_data.get('state'):
        payload['state'] = contact_data['state']
    if contact_data.get('tags'):
        # Tags are passed as a list
        tags = contact_data['tags'].split(',') if isinstance(contact_data['tags'], str) else contact_data['tags']
        payload['tags'] = [t.strip() for t in tags]

    # Source tracking
    payload['source'] = 'Human Led AI - Frankie Import'

    response = requests.post(url, headers=HEADERS, json=payload)
    return response


def import_csv(csv_path, test_mode=False):
    """Import contacts from CSV file"""
    results = {
        'success': 0,
        'failed': 0,
        'errors': []
    }

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if test_mode:
        rows = rows[:1]  # Only first contact for testing
        print("TEST MODE: Importing 1 contact only")

    total = len(rows)
    print(f"Importing {total} contacts to GHL...")

    for i, row in enumerate(rows, 1):
        # Map CSV columns to GHL fields
        contact = {
            'firstName': row.get('First Name', ''),
            'lastName': row.get('Last Name', ''),
            'phone': row.get('Phone', ''),
            'email': row.get('Email', ''),
            'companyName': row.get('Company Name', ''),
            'city': row.get('City', ''),
            'state': row.get('State', ''),
            'tags': row.get('Tags', '')
        }

        # Need at least phone or email
        if not contact['phone'] and not contact['email']:
            results['failed'] += 1
            results['errors'].append(f"Row {i}: No phone or email")
            continue

        try:
            response = create_contact(contact)

            if response.status_code in [200, 201]:
                results['success'] += 1
                contact_id = response.json().get('contact', {}).get('id', 'unknown')
                company = contact.get('companyName', 'Unknown')
                print(f"[{i}/{total}] ✓ {company} - ID: {contact_id}")
            else:
                results['failed'] += 1
                error_msg = response.json().get('message', response.text)
                results['errors'].append(f"Row {i}: {error_msg}")
                print(f"[{i}/{total}] ✗ {contact.get('companyName', 'Unknown')} - {error_msg}")

            # Rate limiting - 100 requests per 10 seconds
            time.sleep(0.15)

        except Exception as e:
            results['failed'] += 1
            results['errors'].append(f"Row {i}: {str(e)}")
            print(f"[{i}/{total}] ✗ Error: {str(e)}")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python ghl_import.py <csv_file> [--test]")
        sys.exit(1)

    csv_path = sys.argv[1]
    test_mode = '--test' in sys.argv

    if not Path(csv_path).exists():
        print(f"File not found: {csv_path}")
        sys.exit(1)

    print("=" * 50)
    print("GHL CONTACT IMPORTER")
    print("=" * 50)
    print(f"Location ID: {GHL_LOCATION_ID}")
    print(f"Source file: {csv_path}")
    print("=" * 50)

    results = import_csv(csv_path, test_mode)

    print("\n" + "=" * 50)
    print("IMPORT COMPLETE")
    print("=" * 50)
    print(f"Success: {results['success']}")
    print(f"Failed:  {results['failed']}")

    if results['errors']:
        print("\nErrors:")
        for error in results['errors'][:10]:  # Show first 10 errors
            print(f"  - {error}")
        if len(results['errors']) > 10:
            print(f"  ... and {len(results['errors']) - 10} more")


if __name__ == "__main__":
    main()
