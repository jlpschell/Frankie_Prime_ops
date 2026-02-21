#!/usr/bin/env python3
"""
Lead Enrichment Pipeline — Frankie's Background Worker

Reads CSV leads, scrapes websites for emails, validates phones,
writes enriched CSV back. Designed to run as a background drip.

Usage:
    python enrich_leads.py --input leads.csv --output enriched.csv
    python enrich_leads.py --input leads.csv --output enriched.csv --limit 10
    python enrich_leads.py --input leads.csv --output enriched.csv --skip-existing
"""

import os
import re
import csv
import json
import argparse
import time
import sys
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import phonenumbers
from phonenumbers import carrier, number_type

try:
    import dns.resolver
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


# === Email Verification ===

DOMAIN_TYPOS = {
    'gmial.com': 'gmail.com', 'gmai.com': 'gmail.com',
    'gamil.com': 'gmail.com', 'gnail.com': 'gmail.com',
    'yahooo.com': 'yahoo.com', 'yaho.com': 'yahoo.com',
    'hotmal.com': 'hotmail.com', 'hotmai.com': 'hotmail.com',
    'outloo.com': 'outlook.com',
}

_mx_cache = {}

def fix_email_typos(email: str) -> str:
    if '@' not in email:
        return email
    local, domain = email.rsplit('@', 1)
    domain_lower = domain.lower()
    if domain_lower in DOMAIN_TYPOS:
        return f"{local}@{DOMAIN_TYPOS[domain_lower]}"
    return email

def verify_mx(email: str) -> bool:
    if not DNS_AVAILABLE or '@' not in email:
        return True
    domain = email.rsplit('@', 1)[1].lower()
    if domain in _mx_cache:
        return _mx_cache[domain]
    try:
        records = dns.resolver.resolve(domain, 'MX')
        result = len(records) > 0
    except Exception:
        result = True  # permissive on error
    _mx_cache[domain] = result
    return result


# === Phone Validation ===

def validate_phone(phone_str: str) -> dict:
    """Validate phone number — carrier, type, active format."""
    result = {
        'phone_valid': False,
        'phone_type': 'unknown',
        'phone_carrier': '',
        'phone_formatted': '',
    }
    if not phone_str or not phone_str.strip():
        return result

    # Clean the phone string
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    if not cleaned.startswith('+') and len(cleaned) == 10:
        cleaned = '+1' + cleaned
    elif not cleaned.startswith('+') and len(cleaned) == 11 and cleaned.startswith('1'):
        cleaned = '+' + cleaned

    try:
        parsed = phonenumbers.parse(cleaned, 'US')
        if phonenumbers.is_valid_number(parsed):
            result['phone_valid'] = True
            result['phone_formatted'] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )

            # Get number type
            ntype = number_type(parsed)
            type_map = {
                phonenumbers.PhoneNumberType.MOBILE: 'mobile',
                phonenumbers.PhoneNumberType.FIXED_LINE: 'landline',
                phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: 'mobile_or_landline',
                phonenumbers.PhoneNumberType.VOIP: 'voip',
                phonenumbers.PhoneNumberType.TOLL_FREE: 'toll_free',
            }
            result['phone_type'] = type_map.get(ntype, 'unknown')

            # Get carrier
            result['phone_carrier'] = carrier.name_for_number(parsed, 'en') or ''
    except Exception:
        pass

    return result


# === Website Scraping ===

CONTACT_PAGES = [
    "/contact", "/contact-us", "/about", "/about-us",
    "/team", "/our-team", "/staff", "/company"
]

EMAIL_PATTERN = re.compile(
    r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    re.IGNORECASE
)

GENERIC_EMAIL_PATTERNS = [
    r'info@', r'contact@', r'sales@', r'support@',
    r'hello@', r'admin@', r'noreply@', r'no-reply@',
    r'webmaster@', r'postmaster@'
]

TITLE_PATTERNS = [
    r'owner', r'president', r'ceo', r'founder',
    r'general manager', r'manager', r'director',
    r'proprietor', r'principal'
]

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})


def fetch_page(url: str, timeout: int = 10) -> Optional[str]:
    try:
        resp = session.get(url, timeout=timeout, allow_redirects=True)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            for el in soup(['script', 'style', 'nav']):
                el.decompose()
            return soup.get_text(separator=' ', strip=True)
    except Exception:
        pass
    return None


def extract_emails(text: str) -> set:
    emails = set(EMAIL_PATTERN.findall(text))
    return {e for e in emails if not any(
        ext in e.lower() for ext in ['.png', '.jpg', '.gif', '.svg', '.webp']
    )}


def select_best_email(emails: list) -> Optional[str]:
    if not emails:
        return None
    personal = [e for e in emails if not any(
        re.search(p, e.lower()) for p in GENERIC_EMAIL_PATTERNS
    )]
    generic = [e for e in emails if e not in personal]
    return (personal or generic or emails)[0]


def extract_contact_info(text: str) -> dict:
    # Common false positive words that aren't names
    false_positives = {
        'water', 'fire', 'storm', 'mold', 'flood', 'damage', 'values',
        'family', 'property', 'service', 'countless', 'quality', 'trusted',
        'premier', 'professional', 'certified', 'licensed', 'local',
        'north', 'south', 'east', 'west', 'fort', 'dallas', 'texas',
        'restoration', 'construction', 'roofing', 'plumbing', 'hvac',
        'emergency', 'commercial', 'residential', 'our', 'the', 'your',
    }

    for title_pat in TITLE_PATTERNS:
        p1 = re.compile(rf'([A-Z][a-z]+ [A-Z][a-z]+),?\s*(?:{title_pat})', re.IGNORECASE)
        p2 = re.compile(rf'(?:{title_pat})[:\-\s]+([A-Z][a-z]+ [A-Z][a-z]+)', re.IGNORECASE)
        match = p1.search(text) or p2.search(text)
        if match:
            name = match.group(1).strip()
            # Filter out false positives
            words = name.lower().split()
            if any(w in false_positives for w in words):
                continue
            # Name should be 2-3 words, each 2+ chars
            if all(len(w) >= 2 for w in words) and len(words) in (2, 3):
                return {'contact_name': name, 'contact_title': title_pat.title()}
    return {}


def enrich_website(website: str) -> dict:
    """Scrape a website for email and contact info."""
    result = {
        'scraped_email': '',
        'email_verified': False,
        'contact_name': '',
        'contact_title': '',
        'enrichment_status': 'pending',
    }

    if not website or not website.strip():
        result['enrichment_status'] = 'no_website'
        return result

    # Clean URL
    url = website.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    # Strip tracking params for cleaner scraping
    base_url = url.split('?')[0].rstrip('/')

    try:
        all_emails = set()
        all_text = ""

        # Scrape main page
        page = fetch_page(base_url)
        if page:
            all_text += page
            all_emails.update(extract_emails(page))

        # Scrape contact/about pages
        for path in CONTACT_PAGES:
            page_url = base_url.rstrip('/') + path
            page = fetch_page(page_url)
            if page:
                all_text += page
                all_emails.update(extract_emails(page))
            time.sleep(0.5)

        # Best email
        best = select_best_email(list(all_emails))
        if best:
            best = fix_email_typos(best)
            verified = verify_mx(best)
            if verified:
                result['scraped_email'] = best
                result['email_verified'] = True
            else:
                result['enrichment_status'] = 'email_failed_mx'

        # Contact info
        info = extract_contact_info(all_text)
        result['contact_name'] = info.get('contact_name', '')
        result['contact_title'] = info.get('contact_title', '')
        result['enrichment_status'] = 'success'

    except Exception as e:
        result['enrichment_status'] = f'failed: {str(e)[:80]}'

    return result


# === Main Pipeline ===

def main():
    parser = argparse.ArgumentParser(description="Enrich CSV leads with email + phone validation")
    parser.add_argument("--input", "-i", required=True, help="Input CSV file")
    parser.add_argument("--output", "-o", required=True, help="Output CSV file")
    parser.add_argument("--limit", "-l", type=int, help="Limit number of leads to process")
    parser.add_argument("--skip-existing", action="store_true",
                        help="Skip leads that already have an email")

    args = parser.parse_args()

    # Read input CSV
    with open(args.input, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        leads = list(reader)
        fieldnames = reader.fieldnames

    total = len(leads)
    print(f"Loaded {total} leads from {args.input}")

    # Add enrichment columns to fieldnames
    extra_fields = [
        'scraped_email', 'email_verified', 'contact_name', 'contact_title',
        'phone_valid', 'phone_type', 'phone_carrier', 'phone_formatted',
        'enrichment_status'
    ]
    out_fields = list(fieldnames) + [f for f in extra_fields if f not in fieldnames]

    if args.limit:
        leads = leads[:args.limit]

    processed = 0
    emails_found = 0
    phones_validated = 0
    contacts_found = 0

    # Open output for streaming writes
    with open(args.output, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=out_fields, extrasaction='ignore')
        writer.writeheader()

        for i, lead in enumerate(leads, 1):
            existing_email = (lead.get('Email') or '').strip()
            website = (lead.get('Website') or '').strip()
            phone = (lead.get('Phone') or '').strip()

            # Phone validation (always do this)
            phone_info = validate_phone(phone)
            lead.update(phone_info)
            if phone_info['phone_valid']:
                phones_validated += 1

            # Email enrichment
            if args.skip_existing and existing_email:
                lead['scraped_email'] = ''
                lead['email_verified'] = ''
                lead['contact_name'] = ''
                lead['contact_title'] = ''
                lead['enrichment_status'] = 'skipped_has_email'
                print(f"[{i}/{len(leads)}] {lead.get('Company Name', '?')[:40]} — skipped (has email)")
            elif website:
                print(f"[{i}/{len(leads)}] {lead.get('Company Name', '?')[:40]}...", end=" ", flush=True)
                enrichment = enrich_website(website)
                lead.update(enrichment)

                if enrichment['scraped_email']:
                    emails_found += 1
                    print(f"EMAIL: {enrichment['scraped_email']}", flush=True)
                elif enrichment['contact_name']:
                    contacts_found += 1
                    print(f"Contact: {enrichment['contact_name']}", flush=True)
                else:
                    print(f"({enrichment['enrichment_status']})", flush=True)

                time.sleep(1)  # Rate limit between leads
            else:
                lead['scraped_email'] = ''
                lead['email_verified'] = ''
                lead['contact_name'] = ''
                lead['contact_title'] = ''
                lead['enrichment_status'] = 'no_website'
                print(f"[{i}/{len(leads)}] {lead.get('Company Name', '?')[:40]} — no website")

            writer.writerow(lead)
            processed += 1

            # Progress update every 25 leads
            if processed % 25 == 0:
                print(f"\n--- Progress: {processed}/{len(leads)} | Emails: {emails_found} | Phones valid: {phones_validated} ---\n")

    # Final summary
    print("\n" + "=" * 60)
    print(f"ENRICHMENT COMPLETE")
    print(f"=" * 60)
    print(f"  Processed:        {processed}")
    print(f"  Emails found:     {emails_found} ({100*emails_found/max(processed,1):.1f}%)")
    print(f"  Phones validated:  {phones_validated} ({100*phones_validated/max(processed,1):.1f}%)")
    print(f"  Contacts found:   {contacts_found}")
    print(f"  Output:           {args.output}")
    print(f"=" * 60)


if __name__ == "__main__":
    main()
