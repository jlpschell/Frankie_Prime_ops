#!/usr/bin/env node

/**
 * Unsubscribe Worker - Runs independently as a background process
 * Gemini can trigger this and monitor progress via log files
 *
 * Usage:
 *   node worker.js                    # Full run (500 emails)
 *   node worker.js --max=1000         # Scan more emails
 *   node worker.js --dry-run          # Preview only, no unsubscribes
 *   node worker.js --status           # Check current run status
 */

const GmailScanner = require('./gmail-scanner');
const Unsubscriber = require('./unsubscriber');
const config = require('./config');
const fs = require('fs');
const path = require('path');

const STATUS_FILE = path.join(config.LOG_PATH, 'worker-status.json');
const PROGRESS_FILE = path.join(config.LOG_PATH, 'worker-progress.json');

function updateStatus(status, data = {}) {
  const statusData = {
    status,
    timestamp: new Date().toISOString(),
    ...data
  };

  if (!fs.existsSync(config.LOG_PATH)) {
    fs.mkdirSync(config.LOG_PATH, { recursive: true });
  }

  fs.writeFileSync(STATUS_FILE, JSON.stringify(statusData, null, 2));
  return statusData;
}

function getStatus() {
  if (!fs.existsSync(STATUS_FILE)) {
    return { status: 'idle', message: 'No runs yet' };
  }
  return JSON.parse(fs.readFileSync(STATUS_FILE, 'utf8'));
}

function updateProgress(current, total, currentSender) {
  const progress = {
    current,
    total,
    percent: Math.round((current / total) * 100),
    currentSender,
    timestamp: new Date().toISOString()
  };
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

async function runWorker(options = {}) {
  const { maxEmails = 500, dryRun = false } = options;

  console.log('='.repeat(60));
  console.log('FRANKIE UNSUBSCRIBE WORKER');
  console.log('='.repeat(60));
  console.log(`Mode: ${dryRun ? 'Dry Run (preview only)' : 'Full Unsubscribe'}`);
  console.log(`Max emails: ${maxEmails}`);
  console.log(`Exclusions: ${config.EXCLUSIONS.join(', ')}`);
  console.log('='.repeat(60));

  updateStatus('running', {
    mode: dryRun ? 'dry-run' : 'full',
    maxEmails,
    startedAt: new Date().toISOString()
  });

  try {
    // Phase 1: Scan
    updateStatus('scanning', { phase: 'Finding subscription emails' });

    const scanner = new GmailScanner();
    await scanner.initialize();
    const subscriptions = await scanner.scanForUnsubscribeEmails(maxEmails);

    if (subscriptions.length === 0) {
      const result = updateStatus('complete', {
        message: 'No subscriptions found to unsubscribe from',
        found: 0,
        processed: 0
      });
      console.log('\nNo subscriptions found!');
      return result;
    }

    console.log(`\nFound ${subscriptions.length} unique senders to unsubscribe from`);

    // Save scan results
    const scanPath = path.join(config.LOG_PATH, 'last-scan.json');
    fs.writeFileSync(scanPath, JSON.stringify(subscriptions, null, 2));

    if (dryRun) {
      console.log('\n--- DRY RUN MODE ---');
      console.log('Would unsubscribe from:');
      subscriptions.forEach((s, i) => {
        console.log(`  ${i + 1}. ${s.sender}`);
      });

      const result = updateStatus('complete', {
        mode: 'dry-run',
        found: subscriptions.length,
        message: 'Dry run complete - no unsubscribes performed',
        subscriptions: subscriptions.map(s => s.sender)
      });
      return result;
    }

    // Phase 2: Unsubscribe
    updateStatus('unsubscribing', {
      phase: 'Processing unsubscribe links',
      total: subscriptions.length
    });

    const unsubscriber = new Unsubscriber();
    await unsubscriber.initialize();

    // Custom processing with progress updates
    console.log(`\nProcessing ${subscriptions.length} subscriptions...\n`);

    for (let i = 0; i < subscriptions.length; i++) {
      updateProgress(i + 1, subscriptions.length, subscriptions[i].sender);
      console.log(`[${i + 1}/${subscriptions.length}]`);
      await unsubscriber.attemptUnsubscribe(subscriptions[i]);

      if (i < subscriptions.length - 1) {
        await new Promise(r => setTimeout(r, config.UNSUBSCRIBE_DELAY));
      }
    }

    // Generate report
    const report = unsubscriber.generateReport();
    unsubscriber.printSummary();
    await unsubscriber.close();

    const result = updateStatus('complete', {
      found: subscriptions.length,
      success: report.summary.success,
      failed: report.summary.failed,
      needsManual: report.summary.needsManual,
      reportPath: report.timestamp,
      completedAt: new Date().toISOString()
    });

    console.log('\n=== WORKER COMPLETE ===');
    return result;

  } catch (err) {
    console.error('Worker error:', err);
    updateStatus('error', {
      error: err.message,
      stack: err.stack
    });
    throw err;
  }
}

// CLI handling
const args = process.argv.slice(2);

if (args.includes('--status')) {
  const status = getStatus();
  console.log(JSON.stringify(status, null, 2));
  process.exit(0);
}

if (args.includes('--progress')) {
  if (fs.existsSync(PROGRESS_FILE)) {
    console.log(fs.readFileSync(PROGRESS_FILE, 'utf8'));
  } else {
    console.log('{ "status": "no active run" }');
  }
  process.exit(0);
}

const dryRun = args.includes('--dry-run');
const maxArg = args.find(a => a.startsWith('--max='));
const maxEmails = maxArg ? parseInt(maxArg.split('=')[1]) : 500;

runWorker({ maxEmails, dryRun }).catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
