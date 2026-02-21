#!/usr/bin/env node

const GmailScanner = require('./gmail-scanner');
const Unsubscriber = require('./unsubscriber');
const config = require('./config');
const fs = require('fs');
const path = require('path');

async function main() {
  const args = process.argv.slice(2);
  const scanOnly = args.includes('--scan-only');
  const dryRun = args.includes('--dry-run');
  const maxEmails = parseInt(args.find(a => a.startsWith('--max='))?.split('=')[1] || '500');

  console.log('='.repeat(60));
  console.log('FRANKIE UNSUBSCRIBE AGENT');
  console.log('='.repeat(60));
  console.log(`Mode: ${scanOnly ? 'Scan Only' : dryRun ? 'Dry Run' : 'Full Unsubscribe'}`);
  console.log(`Max emails to scan: ${maxEmails}`);
  console.log(`\nExclusions (will NOT unsubscribe):`);
  config.EXCLUSIONS.forEach(e => console.log(`  - ${e}`));
  console.log('='.repeat(60) + '\n');

  // Initialize Gmail scanner
  const scanner = new GmailScanner();
  await scanner.initialize();

  // Scan for subscriptions
  const subscriptions = await scanner.scanForUnsubscribeEmails(maxEmails);

  if (subscriptions.length === 0) {
    console.log('No subscriptions found to unsubscribe from!');
    return;
  }

  // Save scan results
  const scanResultsPath = path.join(config.LOG_PATH, 'last-scan.json');
  if (!fs.existsSync(config.LOG_PATH)) {
    fs.mkdirSync(config.LOG_PATH, { recursive: true });
  }
  fs.writeFileSync(scanResultsPath, JSON.stringify(subscriptions, null, 2));
  console.log(`\nScan results saved to: ${scanResultsPath}`);

  if (scanOnly) {
    console.log('\n--scan-only flag set. Exiting without unsubscribing.');
    console.log('\nFound subscriptions:');
    subscriptions.forEach((s, i) => {
      console.log(`\n${i + 1}. ${s.sender}`);
      console.log(`   Subject: ${s.subject}`);
    });
    return;
  }

  if (dryRun) {
    console.log('\n--dry-run flag set. Would unsubscribe from:');
    subscriptions.forEach((s, i) => {
      console.log(`${i + 1}. ${s.sender}`);
    });
    return;
  }

  // Initialize unsubscriber and process
  const unsubscriber = new Unsubscriber();
  await unsubscriber.initialize();

  try {
    await unsubscriber.processAll(subscriptions);
    unsubscriber.printSummary();
    unsubscriber.generateReport();
  } finally {
    await unsubscriber.close();
  }

  console.log('\nDone!');
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
