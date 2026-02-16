# File Routing Rules

## Auto-Route by Extension
- .csv → leads/ (if headers contain: name, phone, email, address, business)
- .csv → data/ (all other CSVs)
- .pdf → docs/
- .png, .jpg, .jpeg → images/
- .mp3, .wav → audio/
- .md, .txt → notes/

## Auto-Route by Content
- CSV with columns matching lead schema → leads/
- PDF with "invoice" or "estimate" in filename → invoices/
- Any file with "GHL" or "GoHighLevel" in name → ghl/

## Safety Rules
- Files are NEVER auto-deleted — moved to _processed/ after routing
- 50MB max for auto-processing — larger files alert Jay
- Code files (.ts, .js, .py, .sh) ALWAYS ask Jay before processing
- Unknown file types: ask Jay on Discord before routing

## Teachable Routes
- Jay can add new rules by telling Frankie: "route all [pattern] files to [folder]"
- New rules get added to this file automatically
