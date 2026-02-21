#!/usr/bin/env npx ts-node
/**
 * Scrape DFW painter leads from Bing Maps and output GHL-ready CSV.
 * Usage: npx ts-node scripts/scrape-painters.ts
 */

import { chromium } from 'playwright';
import * as fs from 'fs';
import * as path from 'path';

interface Lead {
  name: string;
  phone: string;
  address: string;
  city: string;
  website: string;
}

const DFW_CITIES = [
  'Royse City TX',
  'Rockwall TX',
  'McKinney TX',
  'Allen TX',
  'Frisco TX',
  'Plano TX',
  'Garland TX',
  'Mesquite TX',
  'Forney TX',
  'Heath TX',
  'Caddo Mills TX',
  'Greenville TX',
  'Wylie TX',
  'Sachse TX',
  'Rowlett TX',
  'Fate TX',
  'Lavon TX',
  'Nevada TX',
  'Farmersville TX',
  'Terrell TX',
];

function cleanPhone(raw: string): string {
  const digits = raw.replace(/\D/g, '');
  if (digits.length === 10) return `+1${digits}`;
  if (digits.length === 11 && digits.startsWith('1')) return `+${digits}`;
  return '';
}

function extractCity(address: string): string {
  // Try to pull city from address like "123 Main St, Rockwall, TX 75087"
  const parts = address.split(',').map(s => s.trim());
  if (parts.length >= 2) {
    // City is usually the second-to-last part before state/zip
    const cityCandidate = parts[parts.length - 2] || parts[1];
    // Strip state abbreviation and zip if present
    return cityCandidate.replace(/\s*(TX|Texas)\s*\d*/i, '').trim();
  }
  return '';
}

async function scrapeBingMaps(query: string): Promise<Lead[]> {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const leads: Lead[] = [];

  try {
    const url = `https://www.bing.com/maps?q=${encodeURIComponent(query)}&FORM=HDRSC6`;
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

    // Wait for listings to load
    await page.waitForSelector('.b_sideBleed, .taskCont, .b_entityTP', { timeout: 15000 }).catch(() => {});
    await page.waitForTimeout(3000);

    // Try multiple selector strategies for Bing Maps listings
    const text = await page.evaluate(() => document.body.innerText);

    // Parse the text content for business listings
    // Bing Maps shows listings with name, address, phone in a structured way
    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

    let currentName = '';
    let currentPhone = '';
    let currentAddress = '';
    let currentWebsite = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];

      // Phone pattern
      const phoneMatch = line.match(/\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}/);
      if (phoneMatch && currentName) {
        currentPhone = phoneMatch[0];
      }

      // Address pattern (contains TX or Texas)
      if (/\b(TX|Texas)\b/i.test(line) && /\d/.test(line) && line.length > 15) {
        currentAddress = line;
      }

      // Website pattern
      const webMatch = line.match(/(?:www\.)?[\w-]+\.(?:com|net|org|biz|us|co)/i);
      if (webMatch && !line.includes('bing.com') && !line.includes('microsoft')) {
        currentWebsite = line.includes('http') ? line : '';
      }

      // Business name heuristic: a line that's a proper name (title case, not a phone, not an address)
      if (
        line.length > 3 &&
        line.length < 80 &&
        !phoneMatch &&
        !/\b(TX|Texas)\b/i.test(line) &&
        !/^\d/.test(line) &&
        !line.includes('©') &&
        !line.includes('Bing') &&
        !line.includes('Microsoft') &&
        !line.includes('Map') &&
        !line.includes('Directions') &&
        !line.includes('Reviews') &&
        !line.includes('Website') &&
        !line.includes('Open') &&
        !line.includes('Closed') &&
        !line.includes('hours') &&
        /[A-Z]/.test(line[0]) &&
        (line.toLowerCase().includes('paint') || line.toLowerCase().includes('coat') || line.toLowerCase().includes('finish'))
      ) {
        // Save previous lead if we have enough
        if (currentName && currentPhone) {
          leads.push({
            name: currentName,
            phone: currentPhone,
            address: currentAddress,
            city: extractCity(currentAddress),
            website: currentWebsite,
          });
        }
        currentName = line;
        currentPhone = '';
        currentAddress = '';
        currentWebsite = '';
      }
    }

    // Don't forget the last one
    if (currentName && currentPhone) {
      leads.push({
        name: currentName,
        phone: currentPhone,
        address: currentAddress,
        city: extractCity(currentAddress),
        website: currentWebsite,
      });
    }
  } catch (err) {
    console.error(`  Error scraping "${query}":`, (err as Error).message);
  } finally {
    await browser.close();
  }

  return leads;
}

async function scrapeYellowPagesStyle(query: string, city: string): Promise<Lead[]> {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const leads: Lead[] = [];

  try {
    // Use Bing search to find painters - more reliable than specific directories
    const searchUrl = `https://www.bing.com/search?q=${encodeURIComponent(query + ' phone number')}`;
    await page.goto(searchUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(2000);

    const text = await page.evaluate(() => document.body.innerText);
    const lines = text.split('\n').map(l => l.trim()).filter(Boolean);

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const phoneMatch = line.match(/\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}/);

      if (phoneMatch) {
        // Look backwards for a business name
        let name = '';
        for (let j = i - 1; j >= Math.max(0, i - 5); j--) {
          const candidate = lines[j];
          if (
            candidate.length > 3 &&
            candidate.length < 80 &&
            /[A-Z]/.test(candidate[0]) &&
            !candidate.match(/\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}/) &&
            (candidate.toLowerCase().includes('paint') ||
             candidate.toLowerCase().includes('coat') ||
             candidate.toLowerCase().includes('finish') ||
             candidate.toLowerCase().includes('color') ||
             candidate.toLowerCase().includes('pro'))
          ) {
            name = candidate;
            break;
          }
        }

        if (name) {
          leads.push({
            name,
            phone: phoneMatch[0],
            address: '',
            city,
            website: '',
          });
        }
      }
    }
  } catch (err) {
    console.error(`  Error searching "${query}":`, (err as Error).message);
  } finally {
    await browser.close();
  }

  return leads;
}

async function main() {
  console.log('🎨 Scraping DFW painter leads...\n');

  const allLeads: Lead[] = [];
  const seenPhones = new Set<string>();
  const seenNames = new Set<string>();

  for (const city of DFW_CITIES) {
    const query = `painters near ${city}`;
    console.log(`Scraping: ${query}`);

    // Try Bing Maps first
    const mapLeads = await scrapeBingMaps(query);
    console.log(`  Bing Maps: ${mapLeads.length} leads`);

    // Also try Bing search
    const searchLeads = await scrapeYellowPagesStyle(`painters ${city}`, city.replace(' TX', ''));
    console.log(`  Bing Search: ${searchLeads.length} leads`);

    // Deduplicate and add
    for (const lead of [...mapLeads, ...searchLeads]) {
      const phone = cleanPhone(lead.phone);
      const nameLower = lead.name.toLowerCase();

      if (phone && !seenPhones.has(phone) && !seenNames.has(nameLower)) {
        seenPhones.add(phone);
        seenNames.add(nameLower);
        allLeads.push({ ...lead, phone });
      }
    }

    // Small delay between cities to be polite
    await new Promise(r => setTimeout(r, 1000));
  }

  console.log(`\n✅ Total unique leads: ${allLeads.length}\n`);

  // Build CSV
  const csvHeader = 'First Name,Last Name,Phone,Email,Company Name,City,State,Website,Tags';
  const csvRows = allLeads.map(lead => {
    const companyName = lead.name.replace(/"/g, '""');
    const city = lead.city.replace(/"/g, '""');
    const website = lead.website || '';
    return `,,${lead.phone},,"${companyName}","${city}",Texas,${website},"painter-campaign,human-led-ai,dfw"`;
  });

  const csv = [csvHeader, ...csvRows].join('\n');
  const outPath = path.join(__dirname, '..', 'ghl_import', 'painters_ghl_import.csv');
  fs.writeFileSync(outPath, csv, 'utf-8');
  console.log(`📄 Saved to: ${outPath}`);
  console.log(`   ${allLeads.length} leads ready for GHL import`);

  // Print summary
  const cityCounts: Record<string, number> = {};
  for (const lead of allLeads) {
    const c = lead.city || 'Unknown';
    cityCounts[c] = (cityCounts[c] || 0) + 1;
  }
  console.log('\nLeads by city:');
  for (const [city, count] of Object.entries(cityCounts).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${city}: ${count}`);
  }
}

main().catch(console.error);
