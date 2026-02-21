#!/usr/bin/env python3
"""
clean_leads.py - Frankie Lead Cleaner
Reads all CSVs in ghl_import/, filters to TX-only leads with valid phones,
writes cleaned files to ghl_import/cleaned/, and prints a summary table.
"""

import csv
import os
import re
import sys
from pathlib import Path

# Paths
IMPORT_DIR = Path("/home/plotting1/frankie-bot/workspace/ghl_import")
CLEANED_DIR = IMPORT_DIR / "cleaned"

# Standard column order for output
STANDARD_HEADERS = [
    "First Name", "Last Name", "Company Name", "Phone", "Email",
    "Address", "City", "State", "Postal Code", "Website", "Tags"
]

# Texas identifiers (case-insensitive)
TX_VALUES = {"tx", "texas"}


def is_texas(state_val):
    """Check if the state value represents Texas."""
    if not state_val or not state_val.strip():
        return False
    return state_val.strip().lower() in TX_VALUES


def clean_phone(phone_raw):
    """
    Strip phone to digits only, normalize to +1XXXXXXXXXX format.
    Returns cleaned phone string or None if invalid.
    """
    if not phone_raw or not phone_raw.strip():
        return None

    # Strip everything except digits
    digits = re.sub(r"[^\d]", "", phone_raw.strip())

    # Handle different digit counts
    if len(digits) == 10:
        # US number without country code
        digits = "1" + digits
    elif len(digits) == 11:
        # Should start with 1
        if not digits.startswith("1"):
            return None
    else:
        # Wrong number of digits
        return None

    return "+" + digits


def is_valid_email(email):
    """Basic email validation."""
    if not email or not email.strip():
        return False
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()))


def normalize_row(row):
    """Normalize a row to standard column order, handling missing columns."""
    normalized = {}
    for header in STANDARD_HEADERS:
        val = row.get(header, "")
        normalized[header] = val.strip() if val else ""
    return normalized


def process_csv(filepath):
    """
    Process a single CSV file.
    Returns stats dict and writes cleaned CSV to cleaned/ directory.
    """
    filename = filepath.name
    stats = {
        "filename": filename,
        "original_count": 0,
        "cleaned_count": 0,
        "valid_phones": 0,
        "valid_emails": 0,
        "removed_out_of_state": 0,
        "removed_bad_phone": 0,
        "duplicate_companies": 0,
    }

    rows = []

    # Read the CSV
    with open(filepath, "r", encoding="utf-8-sig", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    stats["original_count"] = len(rows)

    # --- Pass 1: Filter by state (TX only) ---
    tx_rows = []
    for row in rows:
        normed = normalize_row(row)
        if is_texas(normed["State"]):
            tx_rows.append(normed)
        else:
            stats["removed_out_of_state"] += 1

    # --- Pass 2: Clean & validate phone numbers ---
    clean_rows = []
    for row in tx_rows:
        cleaned_phone = clean_phone(row["Phone"])
        if cleaned_phone:
            row["Phone"] = cleaned_phone
            clean_rows.append(row)
        else:
            stats["removed_bad_phone"] += 1

    # --- Count valid phones and emails in cleaned set ---
    for row in clean_rows:
        stats["valid_phones"] += 1  # All remaining rows have valid phones
        if is_valid_email(row["Email"]):
            stats["valid_emails"] += 1

    stats["cleaned_count"] = len(clean_rows)

    # --- Flag duplicate companies ---
    company_counts = {}
    for row in clean_rows:
        company = row["Company Name"].strip().lower()
        if company:
            company_counts[company] = company_counts.get(company, 0) + 1

    duplicates = {k: v for k, v in company_counts.items() if v > 1}
    stats["duplicate_companies"] = len(duplicates)

    # --- Write cleaned CSV ---
    output_path = CLEANED_DIR / filename
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=STANDARD_HEADERS)
        writer.writeheader()
        writer.writerows(clean_rows)

    # Print duplicate companies if any
    if duplicates:
        print(f"  [{filename}] Duplicate companies:")
        for company, count in sorted(duplicates.items(), key=lambda x: -x[1]):
            print(f"    - \"{company}\" appears {count} times")

    return stats


def main():
    print("=" * 100)
    print("FRANKIE LEAD CLEANER - Cleaning GHL Import CSVs")
    print("=" * 100)
    print()

    # Create cleaned directory
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {CLEANED_DIR}")
    print()

    # Find all CSV files (exclude cleaned/ subdirectory)
    csv_files = sorted([
        f for f in IMPORT_DIR.glob("*.csv")
        if f.is_file()
    ])

    if not csv_files:
        print("No CSV files found. Exiting.")
        sys.exit(1)

    print(f"Found {len(csv_files)} CSV files to process.")
    print()

    # Process each file
    all_stats = []
    total_original = 0
    total_cleaned = 0
    total_valid_phones = 0
    total_valid_emails = 0
    total_removed_state = 0
    total_removed_phone = 0

    for csv_file in csv_files:
        stats = process_csv(csv_file)
        all_stats.append(stats)
        total_original += stats["original_count"]
        total_cleaned += stats["cleaned_count"]
        total_valid_phones += stats["valid_phones"]
        total_valid_emails += stats["valid_emails"]
        total_removed_state += stats["removed_out_of_state"]
        total_removed_phone += stats["removed_bad_phone"]

    # --- Print summary table ---
    print()
    print("=" * 140)
    print("SUMMARY TABLE")
    print("=" * 140)

    # Header
    header_fmt = "{:<50} {:>8} {:>8} {:>8} {:>8} {:>12} {:>12} {:>8}"
    print(header_fmt.format(
        "Filename", "Original", "Cleaned", "Phones", "Emails",
        "Rm'd State", "Rm'd Phone", "Dupes"
    ))
    print("-" * 140)

    # Rows
    for s in all_stats:
        # Truncate filename if too long
        fname = s["filename"]
        if len(fname) > 48:
            fname = fname[:45] + "..."
        print(header_fmt.format(
            fname,
            s["original_count"],
            s["cleaned_count"],
            s["valid_phones"],
            s["valid_emails"],
            s["removed_out_of_state"],
            s["removed_bad_phone"],
            s["duplicate_companies"],
        ))

    # Totals
    print("-" * 140)
    print(header_fmt.format(
        "TOTALS",
        total_original,
        total_cleaned,
        total_valid_phones,
        total_valid_emails,
        total_removed_state,
        total_removed_phone,
        sum(s["duplicate_companies"] for s in all_stats),
    ))
    print("=" * 140)

    # Summary
    removed_total = total_original - total_cleaned
    pct_kept = (total_cleaned / total_original * 100) if total_original > 0 else 0
    print()
    print(f"Total leads processed: {total_original}")
    print(f"Total leads kept:      {total_cleaned} ({pct_kept:.1f}%)")
    print(f"Total removed:         {removed_total}")
    print(f"  - Out of state:      {total_removed_state}")
    print(f"  - Bad phone:         {total_removed_phone}")
    print(f"Valid emails in set:   {total_valid_emails}")
    print()
    print(f"Cleaned files written to: {CLEANED_DIR}/")
    print("Done.")


if __name__ == "__main__":
    main()
