const { google } = require('googleapis');
const fs = require('fs');
const config = require('./config');

class GmailScanner {
  constructor() {
    this.gmail = null;
    this.auth = null;
  }

  async initialize() {
    const tokenData = JSON.parse(fs.readFileSync(config.TOKEN_PATH, 'utf8'));

    this.auth = new google.auth.OAuth2(
      tokenData.client_id,
      tokenData.client_secret,
      'http://localhost:8085'
    );

    this.auth.setCredentials({
      access_token: tokenData.token,
      refresh_token: tokenData.refresh_token,
      token_type: 'Bearer'
    });

    // Refresh token if needed
    this.auth.on('tokens', (tokens) => {
      if (tokens.access_token) {
        tokenData.token = tokens.access_token;
        if (tokens.refresh_token) {
          tokenData.refresh_token = tokens.refresh_token;
        }
        if (tokens.expiry_date) {
          tokenData.expiry = new Date(tokens.expiry_date).toISOString();
        }
        fs.writeFileSync(config.TOKEN_PATH, JSON.stringify(tokenData, null, 2));
        console.log('Token refreshed and saved');
      }
    });

    this.gmail = google.gmail({ version: 'v1', auth: this.auth });
    console.log('Gmail scanner initialized');
  }

  isExcluded(sender) {
    const senderLower = sender.toLowerCase();
    return config.EXCLUSIONS.some(exclusion =>
      senderLower.includes(exclusion.toLowerCase())
    );
  }

  extractUnsubscribeLink(headers, body) {
    // Check List-Unsubscribe header first (most reliable)
    const listUnsub = headers.find(h => h.name.toLowerCase() === 'list-unsubscribe');
    if (listUnsub) {
      const httpMatch = listUnsub.value.match(/<(https?:\/\/[^>]+)>/);
      if (httpMatch) {
        return httpMatch[1];
      }
    }

    // Fall back to searching email body for unsubscribe links
    if (body) {
      const unsubPatterns = [
        /href=["'](https?:\/\/[^"']*unsubscribe[^"']*)/i,
        /href=["'](https?:\/\/[^"']*optout[^"']*)/i,
        /href=["'](https?:\/\/[^"']*opt-out[^"']*)/i,
        /href=["'](https?:\/\/[^"']*remove[^"']*)/i,
        /href=["'](https?:\/\/[^"']*preferences[^"']*)/i
      ];

      for (const pattern of unsubPatterns) {
        const match = body.match(pattern);
        if (match) {
          return match[1];
        }
      }
    }

    return null;
  }

  decodeBody(payload) {
    let body = '';

    const decode = (data) => {
      if (!data) return '';
      return Buffer.from(data.replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8');
    };

    if (payload.body && payload.body.data) {
      body = decode(payload.body.data);
    }

    if (payload.parts) {
      for (const part of payload.parts) {
        if (part.mimeType === 'text/html' && part.body && part.body.data) {
          body += decode(part.body.data);
        } else if (part.parts) {
          body += this.decodeBody(part);
        }
      }
    }

    return body;
  }

  async scanForUnsubscribeEmails(maxResults = 500) {
    console.log(`Scanning for emails with unsubscribe links (max ${maxResults})...`);

    const results = [];
    let pageToken = null;
    let scanned = 0;

    while (scanned < maxResults) {
      const batchSize = Math.min(config.BATCH_SIZE, maxResults - scanned);

      const response = await this.gmail.users.messages.list({
        userId: 'me',
        maxResults: batchSize,
        pageToken: pageToken,
        q: 'unsubscribe' // Only get emails mentioning unsubscribe
      });

      if (!response.data.messages || response.data.messages.length === 0) {
        console.log('No more messages found');
        break;
      }

      console.log(`Processing batch of ${response.data.messages.length} emails...`);

      for (const msg of response.data.messages) {
        try {
          const email = await this.gmail.users.messages.get({
            userId: 'me',
            id: msg.id,
            format: 'full'
          });

          // Skip starred emails if configured
          if (config.SKIP_STARRED && email.data.labelIds && email.data.labelIds.includes('STARRED')) {
            console.log(`  SKIP (starred): ${msg.id}`);
            continue;
          }

          const headers = email.data.payload.headers;
          const from = headers.find(h => h.name.toLowerCase() === 'from');
          const subject = headers.find(h => h.name.toLowerCase() === 'subject');

          if (!from) continue;

          const sender = from.value;

          // Skip if excluded
          if (this.isExcluded(sender)) {
            console.log(`  SKIP (excluded): ${sender}`);
            continue;
          }

          const body = this.decodeBody(email.data.payload);
          const unsubLink = this.extractUnsubscribeLink(headers, body);

          if (unsubLink) {
            // Check if we already have this sender
            const existingSender = results.find(r =>
              r.sender.toLowerCase() === sender.toLowerCase()
            );

            if (!existingSender) {
              results.push({
                messageId: msg.id,
                sender: sender,
                subject: subject ? subject.value : '(no subject)',
                unsubscribeLink: unsubLink
              });
              console.log(`  FOUND: ${sender}`);
            }
          }

          scanned++;
        } catch (err) {
          console.error(`  Error processing message ${msg.id}:`, err.message);
        }
      }

      pageToken = response.data.nextPageToken;
      if (!pageToken) break;
    }

    console.log(`\nScan complete. Found ${results.length} unique senders with unsubscribe links.`);
    return results;
  }
}

module.exports = GmailScanner;
