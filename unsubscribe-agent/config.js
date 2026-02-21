// Unsubscribe Agent Configuration

module.exports = {
  // Senders to NEVER unsubscribe from
  EXCLUSIONS: [
    'heygen',
    'tiktok',
    'chris lee',
    'julian goldie',
    'adt',
    'skool',
    'skool.com',
    'texanscu',
    'texans credit union',
    'cash app',
    'cashapp',
    'square',
    'highlevel',
    'gohighlevel',
    'pennymac',
    'julia mccoy',
    'jlpschell+cc',
    'at&t',
    'att.com',
    'alpaca',
    'fidelity',
    'hostinger',
    'truist',
    'reliant',
    'reliantenergy'
  ],

  // Skip starred emails entirely
  SKIP_STARRED: true,

  // Path to Google credentials
  TOKEN_PATH: '/home/plotting1/frankie-bot/workspace/credentials/token.json',

  // How many emails to scan per batch
  BATCH_SIZE: 100,

  // Delay between unsubscribe attempts (ms) - avoid rate limiting
  UNSUBSCRIBE_DELAY: 2000,

  // Timeout for page loads (ms)
  PAGE_TIMEOUT: 15000,

  // Log file location
  LOG_PATH: '/home/plotting1/frankie-bot/workspace/unsubscribe-agent/logs'
};
