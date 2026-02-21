const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const config = require('./config');

class Unsubscriber {
  constructor() {
    this.browser = null;
    this.results = {
      success: [],
      failed: [],
      needsManual: []
    };
    this.logDir = config.LOG_PATH;
  }

  async initialize() {
    // Create log directory if it doesn't exist
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir, { recursive: true });
    }

    this.browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--disable-gpu'
      ]
    });
    console.log('Browser initialized');
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async attemptUnsubscribe(subscription) {
    const { sender, unsubscribeLink, subject } = subscription;
    console.log(`\nAttempting to unsubscribe from: ${sender}`);
    console.log(`  Link: ${unsubscribeLink}`);

    const page = await this.browser.newPage();

    try {
      // Set a realistic user agent
      await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

      // Navigate to the unsubscribe link
      const response = await page.goto(unsubscribeLink, {
        waitUntil: 'networkidle2',
        timeout: config.PAGE_TIMEOUT
      });

      if (!response) {
        throw new Error('No response received');
      }

      const status = response.status();
      const finalUrl = page.url();

      // Check for immediate success indicators in URL
      if (finalUrl.includes('success') ||
          finalUrl.includes('confirmed') ||
          finalUrl.includes('unsubscribed') ||
          finalUrl.includes('removed')) {
        this.results.success.push({
          sender,
          subject,
          link: unsubscribeLink,
          method: 'URL redirect (auto)'
        });
        console.log(`  SUCCESS: Auto-confirmed via URL`);
        await page.close();
        return true;
      }

      // Get page content
      const content = await page.content();
      const contentLower = content.toLowerCase();

      // Check for success messages on page
      const successIndicators = [
        'successfully unsubscribed',
        'you have been unsubscribed',
        'unsubscribe successful',
        'removed from our list',
        'no longer receive',
        'subscription cancelled',
        'you\'ve been removed',
        'successfully removed'
      ];

      for (const indicator of successIndicators) {
        if (contentLower.includes(indicator)) {
          this.results.success.push({
            sender,
            subject,
            link: unsubscribeLink,
            method: 'One-click (success message found)'
          });
          console.log(`  SUCCESS: Found success message`);
          await page.close();
          return true;
        }
      }

      // Look for confirm/unsubscribe buttons to click
      const buttonSelectors = [
        'button[type="submit"]',
        'input[type="submit"]',
        'button:contains("Unsubscribe")',
        'button:contains("Confirm")',
        'a:contains("Unsubscribe")',
        'a:contains("Confirm")',
        '[class*="unsubscribe"]',
        '[id*="unsubscribe"]'
      ];

      let clicked = false;
      for (const selector of buttonSelectors) {
        try {
          const elements = await page.$$(selector);
          for (const el of elements) {
            const text = await page.evaluate(e => e.textContent || e.value || '', el);
            const textLower = text.toLowerCase();

            if (textLower.includes('unsubscribe') ||
                textLower.includes('confirm') ||
                textLower.includes('remove') ||
                textLower.includes('yes')) {

              console.log(`  Clicking button: "${text.trim()}"`);
              await el.click();
              clicked = true;

              // Wait for navigation or page update
              await Promise.race([
                page.waitForNavigation({ waitUntil: 'networkidle2', timeout: 5000 }).catch(() => {}),
                this.delay(3000)
              ]);

              // Check for success after click
              const newContent = await page.content();
              const newContentLower = newContent.toLowerCase();

              for (const indicator of successIndicators) {
                if (newContentLower.includes(indicator)) {
                  this.results.success.push({
                    sender,
                    subject,
                    link: unsubscribeLink,
                    method: 'Button click confirmed'
                  });
                  console.log(`  SUCCESS: Confirmed after button click`);
                  await page.close();
                  return true;
                }
              }

              break;
            }
          }
          if (clicked) break;
        } catch (e) {
          // Selector failed, try next
        }
      }

      // If we clicked something but couldn't confirm success, mark as likely success
      if (clicked) {
        this.results.success.push({
          sender,
          subject,
          link: unsubscribeLink,
          method: 'Button clicked (unconfirmed)'
        });
        console.log(`  LIKELY SUCCESS: Clicked button, no confirmation`);
        await page.close();
        return true;
      }

      // Check for CAPTCHA or email confirmation required
      if (contentLower.includes('captcha') ||
          contentLower.includes('recaptcha') ||
          contentLower.includes('verify you\'re human')) {
        this.results.needsManual.push({
          sender,
          subject,
          link: unsubscribeLink,
          reason: 'CAPTCHA required'
        });
        console.log(`  MANUAL: CAPTCHA detected`);
        await page.close();
        return false;
      }

      if (contentLower.includes('confirm your email') ||
          contentLower.includes('email has been sent') ||
          contentLower.includes('check your inbox')) {
        this.results.needsManual.push({
          sender,
          subject,
          link: unsubscribeLink,
          reason: 'Email confirmation required'
        });
        console.log(`  MANUAL: Email confirmation needed`);
        await page.close();
        return false;
      }

      // No clear indicators - mark as needs manual review
      this.results.needsManual.push({
        sender,
        subject,
        link: unsubscribeLink,
        reason: 'Unclear outcome - needs manual check'
      });
      console.log(`  MANUAL: Unclear outcome`);
      await page.close();
      return false;

    } catch (err) {
      console.log(`  FAILED: ${err.message}`);
      this.results.failed.push({
        sender,
        subject,
        link: unsubscribeLink,
        error: err.message
      });
      await page.close();
      return false;
    }
  }

  async processAll(subscriptions) {
    console.log(`\nProcessing ${subscriptions.length} subscriptions...\n`);

    for (let i = 0; i < subscriptions.length; i++) {
      console.log(`[${i + 1}/${subscriptions.length}]`);
      await this.attemptUnsubscribe(subscriptions[i]);

      // Delay between requests to avoid rate limiting
      if (i < subscriptions.length - 1) {
        await this.delay(config.UNSUBSCRIBE_DELAY);
      }
    }

    return this.results;
  }

  generateReport() {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const reportPath = path.join(this.logDir, `unsubscribe-report-${timestamp}.json`);

    const report = {
      timestamp: new Date().toISOString(),
      summary: {
        total: this.results.success.length + this.results.failed.length + this.results.needsManual.length,
        success: this.results.success.length,
        failed: this.results.failed.length,
        needsManual: this.results.needsManual.length
      },
      details: this.results
    };

    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    console.log(`\nReport saved to: ${reportPath}`);

    return report;
  }

  printSummary() {
    console.log('\n' + '='.repeat(60));
    console.log('UNSUBSCRIBE SUMMARY');
    console.log('='.repeat(60));
    console.log(`SUCCESS: ${this.results.success.length}`);
    console.log(`FAILED: ${this.results.failed.length}`);
    console.log(`NEEDS MANUAL: ${this.results.needsManual.length}`);
    console.log('='.repeat(60));

    if (this.results.needsManual.length > 0) {
      console.log('\nMANUAL ACTION REQUIRED:');
      for (const item of this.results.needsManual) {
        console.log(`\n  Sender: ${item.sender}`);
        console.log(`  Reason: ${item.reason}`);
        console.log(`  Link: ${item.link}`);
      }
    }
  }
}

module.exports = Unsubscriber;
