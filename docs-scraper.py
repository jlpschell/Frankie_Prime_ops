#!/usr/bin/env python3
"""
OpenClaw Docs Scraper
Downloads and maintains local copy of https://docs.openclaw.ai/

Features:
- Downloads all 200+ pages from the index
- Checks for updates (compares timestamps/hashes)
- Organizes by category (automation/, channels/, cli/, etc.)
- Creates searchable index
- Handles rate limiting and retries
"""

import os
import sys
import time
import hashlib
import json
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from datetime import datetime
import re

class OpenClawDocsScraper:
    def __init__(self, output_dir="docs-openclaw"):
        self.base_url = "https://docs.openclaw.ai/"
        self.output_dir = Path(output_dir)
        self.index_url = "https://docs.openclaw.ai/llms.txt"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (OpenClaw-Docs-Scraper/1.0)'
        })
        
        # Create output structure
        self.output_dir.mkdir(exist_ok=True)
        (self.output_dir / "pages").mkdir(exist_ok=True)
        
        # Track metadata
        self.metadata_file = self.output_dir / "metadata.json"
        self.metadata = self.load_metadata()
        
    def load_metadata(self):
        """Load existing metadata or create new"""
        if self.metadata_file.exists():
            with open(self.metadata_file) as f:
                return json.load(f)
        return {
            "last_update": None,
            "pages": {},
            "stats": {"total": 0, "updated": 0, "new": 0}
        }
    
    def save_metadata(self):
        """Save metadata to disk"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def get_file_hash(self, content):
        """Get SHA256 hash of content"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]
    
    def fetch_page(self, url, retries=3):
        """Fetch a single page with retries"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as e:
                print(f"  ❌ Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
    
    def extract_urls_from_index(self):
        """Extract all doc URLs from the index"""
        print("📋 Fetching docs index...")
        index_content = self.fetch_page(self.index_url)
        
        # Extract URLs using regex
        url_pattern = r'https://docs\.openclaw\.ai/[^\s\)]+\.md'
        urls = re.findall(url_pattern, index_content)
        
        # Add the main index page
        urls.append("https://docs.openclaw.ai/")
        
        # Clean and deduplicate
        urls = list(set(url.rstrip(')') for url in urls))
        urls.sort()
        
        print(f"📄 Found {len(urls)} pages to scrape")
        return urls
    
    def get_category_from_url(self, url):
        """Extract category from URL path"""
        path = urlparse(url).path.strip('/')
        if not path or path == 'index.md':
            return 'root'
        
        # Extract first directory
        parts = path.split('/')
        return parts[0] if len(parts) > 1 else 'misc'
    
    def get_local_filename(self, url):
        """Convert URL to local filename"""
        if url == "https://docs.openclaw.ai/":
            return "index.md"
        
        path = urlparse(url).path
        if path.endswith('/'):
            path = path + 'index.md'
        elif not path.endswith('.md'):
            path = path + '.md'
        
        return path.lstrip('/')
    
    def scrape_page(self, url):
        """Scrape a single page and save it"""
        try:
            print(f"📥 {url}")
            content = self.fetch_page(url)
            
            # Get metadata
            content_hash = self.get_file_hash(content)
            filename = self.get_local_filename(url)
            category = self.get_category_from_url(url)
            local_path = self.output_dir / "pages" / filename
            
            # Check if updated
            page_meta = self.metadata["pages"].get(url, {})
            is_new = url not in self.metadata["pages"]
            is_updated = page_meta.get("hash") != content_hash
            
            if is_new or is_updated:
                # Create directory structure
                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Save content
                with open(local_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Update metadata
                self.metadata["pages"][url] = {
                    "filename": filename,
                    "category": category,
                    "hash": content_hash,
                    "scraped_at": datetime.now().isoformat(),
                    "size": len(content)
                }
                
                if is_new:
                    self.metadata["stats"]["new"] += 1
                    print(f"  ✅ NEW: {filename}")
                else:
                    self.metadata["stats"]["updated"] += 1
                    print(f"  🔄 UPDATED: {filename}")
            else:
                print(f"  ⏭️  UNCHANGED: {filename}")
            
            return True
            
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            return False
    
    def create_index(self):
        """Create searchable index of all pages"""
        print("📚 Creating local index...")
        
        # Group by category
        categories = {}
        for url, meta in self.metadata["pages"].items():
            cat = meta["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                "url": url,
                "filename": meta["filename"],
                "size": meta["size"],
                "scraped_at": meta["scraped_at"]
            })
        
        # Create index file
        index_content = f"""# OpenClaw Documentation (Local Copy)

**Last updated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total pages:** {len(self.metadata['pages'])}
**Source:** https://docs.openclaw.ai/

## Categories

"""
        
        for category, pages in sorted(categories.items()):
            index_content += f"### {category.title()} ({len(pages)} pages)\n\n"
            for page in sorted(pages, key=lambda x: x['filename']):
                local_path = f"pages/{page['filename']}"
                title = page['filename'].replace('.md', '').replace('/', ' / ').title()
                index_content += f"- [{title}]({local_path})\n"
            index_content += "\n"
        
        with open(self.output_dir / "README.md", 'w') as f:
            f.write(index_content)
        
        print(f"📖 Index created: {self.output_dir / 'README.md'}")
    
    def create_search_script(self):
        """Create a search script for the docs"""
        # Create simple Python search instead of bash with variables
        search_script = '''#!/usr/bin/env python3
import sys
import os
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: ./search.py 'search terms'")
    print("Example: ./search.py 'telegram bot'")
    sys.exit(1)

query = ' '.join(sys.argv[1:]).lower()
docs_dir = Path(__file__).parent / "pages"

print(f"🔍 Searching OpenClaw docs for: '{query}'")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

results = []
for md_file in docs_dir.rglob("*.md"):
    try:
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines, 1):
            if query in line.lower():
                rel_path = md_file.relative_to(docs_dir)
                context_start = max(0, i-2)
                context_end = min(len(lines), i+2)
                
                print(f"\\n📄 {rel_path}:{i}")
                for j in range(context_start, context_end):
                    prefix = ">>> " if j == i-1 else "    "
                    print(f"{prefix}{lines[j].rstrip()}")
                    
    except Exception:
        pass

print("\\n💡 Tip: Open files with: cat pages/path/to/file.md")
'''
        
        search_path = self.output_dir / "search.py"
        with open(search_path, 'w') as f:
            f.write(search_script)
        search_path.chmod(0o755)
        
        # Also create bash wrapper
        bash_wrapper = """#!/bin/bash
python3 "$(dirname "$0")/search.py" "$@"
"""
        wrapper_path = self.output_dir / "search.sh"
        with open(wrapper_path, 'w') as f:
            f.write(bash_wrapper)
        wrapper_path.chmod(0o755)
        
        print(f"🔍 Search script created: {search_path}")
    
    def run(self):
        """Run the complete scraping process"""
        start_time = time.time()
        print("🦞 OpenClaw Docs Scraper Starting")
        print(f"📂 Output directory: {self.output_dir}")
        print()
        
        try:
            # Get all URLs to scrape
            urls = self.extract_urls_from_index()
            
            # Reset stats
            self.metadata["stats"] = {"total": len(urls), "updated": 0, "new": 0, "failed": 0}
            
            # Scrape all pages
            print(f"🚀 Scraping {len(urls)} pages...")
            failed = 0
            for i, url in enumerate(urls, 1):
                print(f"[{i}/{len(urls)}]", end=" ")
                
                if not self.scrape_page(url):
                    failed += 1
                
                # Rate limiting
                time.sleep(0.5)
            
            # Update metadata
            self.metadata["last_update"] = datetime.now().isoformat()
            self.metadata["stats"]["failed"] = failed
            self.save_metadata()
            
            # Create index and tools
            self.create_index()
            self.create_search_script()
            
            # Summary
            elapsed = time.time() - start_time
            stats = self.metadata["stats"]
            
            print()
            print("🎉 Scraping Complete!")
            print(f"📊 Results: {stats['total']} total, {stats['new']} new, {stats['updated']} updated, {stats['failed']} failed")
            print(f"⏱️  Time: {elapsed:.1f} seconds")
            print(f"📂 Location: {self.output_dir.absolute()}")
            print()
            print("🔍 Search docs: ./search.sh 'query'")
            print("📖 Browse index: cat README.md")
            
        except KeyboardInterrupt:
            print("\n⏹️  Interrupted by user")
            self.save_metadata()
        except Exception as e:
            print(f"\n❌ Fatal error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    scraper = OpenClawDocsScraper()
    scraper.run()