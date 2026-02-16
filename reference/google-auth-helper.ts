#!/usr/bin/env bun
/**
 * GOOGLE AUTH HELPER — Task 0.5
 * 
 * Run this ONCE per Google account to get a refresh token.
 * Uses Cloud project: frankie1-486714 (per PRD decision)
 * 
 * USAGE:
 *   bun run google-auth-helper.ts personal    # for jlpschell@gmail.com
 *   bun run google-auth-helper.ts business    # for humanledai@gmail.com
 *   bun run google-auth-helper.ts workspace   # for jason@humanledai.net (future)
 * 
 * WHAT IT DOES:
 *   1. Prints a URL — you open it in your browser
 *   2. You log in with the right Google account and approve permissions
 *   3. Google gives you a code — you paste it back here
 *   4. Script exchanges the code for a refresh token
 *   5. You copy the refresh token into your .env file
 * 
 * REQUIRES: CLIENT_ID and CLIENT_SECRET from frankie1-486714 project
 *           Set these in .env BEFORE running:
 *           GOOGLE_OAUTH_CLIENT_ID=...
 *           GOOGLE_OAUTH_CLIENT_SECRET=...
 */

// Load .env
import { readFileSync } from "fs";
import { join } from "path";

// Simple .env loader (no external deps)
function loadEnv(): Record<string, string> {
  const envPath = join(process.cwd(), ".env");
  const env: Record<string, string> = {};
  try {
    const lines = readFileSync(envPath, "utf-8").split("\n");
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const eqIndex = trimmed.indexOf("=");
      if (eqIndex === -1) continue;
      const key = trimmed.slice(0, eqIndex).trim();
      const val = trimmed.slice(eqIndex + 1).trim();
      env[key] = val;
    }
  } catch {
    console.error("ERROR: Could not read .env file. Run this from ~/frankie-bot/");
    process.exit(1);
  }
  return env;
}

const env = loadEnv();

// Get client ID and secret from .env
const CLIENT_ID = env.GOOGLE_OAUTH_CLIENT_ID || env.GOOGLE_PERSONAL_CLIENT_ID || "";
const CLIENT_SECRET = env.GOOGLE_OAUTH_CLIENT_SECRET || env.GOOGLE_PERSONAL_CLIENT_SECRET || "";

if (!CLIENT_ID || !CLIENT_SECRET) {
  console.error(`
ERROR: Missing OAuth credentials in .env

You need these two values from the Google Cloud Console:
  Project: frankie1-486714
  Page: APIs & Services > Credentials > OAuth 2.0 Client IDs

Add to your .env:
  GOOGLE_OAUTH_CLIENT_ID=your-client-id-here
  GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here

If you don't have an OAuth client yet:
  1. Go to https://console.cloud.google.com/apis/credentials?project=frankie1-486714
  2. Click "+ CREATE CREDENTIALS" > "OAuth client ID"
  3. Application type: "Web application"
  4. Authorized redirect URIs: add "http://localhost:3456/callback"
  5. Copy the Client ID and Client Secret into .env
`);
  process.exit(1);
}

// Account argument
const account = process.argv[2];
if (!account || !["personal", "business", "workspace"].includes(account)) {
  console.error(`
USAGE: bun run google-auth-helper.ts <account>

  personal   = jlpschell@gmail.com (primary arm)
  business   = humanledai@gmail.com (stopgap)
  workspace  = jason@humanledai.net (future)
`);
  process.exit(1);
}

// Scopes per PRD
const SCOPES_MAP: Record<string, string[]> = {
  personal: [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/youtube.readonly",
  ],
  business: [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
  ],
  workspace: [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
  ],
};

const ACCOUNT_EMAILS: Record<string, string> = {
  personal: "jlpschell@gmail.com",
  business: "humanledai@gmail.com",
  workspace: "jason@humanledai.net",
};

const REDIRECT_URI = "http://localhost:3456/callback";
const scopes = SCOPES_MAP[account];
const email = ACCOUNT_EMAILS[account];

// Build the auth URL
const authUrl = new URL("https://accounts.google.com/o/oauth2/v2/auth");
authUrl.searchParams.set("client_id", CLIENT_ID);
authUrl.searchParams.set("redirect_uri", REDIRECT_URI);
authUrl.searchParams.set("response_type", "code");
authUrl.searchParams.set("scope", scopes.join(" "));
authUrl.searchParams.set("access_type", "offline");
authUrl.searchParams.set("prompt", "consent"); // Force re-consent to get refresh token
authUrl.searchParams.set("login_hint", email); // Pre-fill the email

console.log(`
╔══════════════════════════════════════════════════════════════╗
║  GOOGLE AUTH — ${account.toUpperCase()} (${email})
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Step 1: Open this URL in your browser:                      ║
╚══════════════════════════════════════════════════════════════╝

${authUrl.toString()}

╔══════════════════════════════════════════════════════════════╗
║  Step 2: Log in as ${email}
║  Step 3: Click "Allow" on ALL permission screens             ║
║  Step 4: You'll be redirected — the page will show a code    ║
║                                                              ║
║  Waiting for callback on http://localhost:3456 ...           ║
╚══════════════════════════════════════════════════════════════╝
`);

// Start a tiny HTTP server to catch the OAuth callback
const server = Bun.serve({
  port: 3456,
  async fetch(req) {
    const url = new URL(req.url);
    
    if (url.pathname === "/callback") {
      const code = url.searchParams.get("code");
      const error = url.searchParams.get("error");
      
      if (error) {
        console.error(`\nERROR: Google returned error: ${error}`);
        server.stop();
        process.exit(1);
      }
      
      if (!code) {
        return new Response("No code received. Try again.", { status: 400 });
      }
      
      // Exchange code for tokens
      console.log("Got authorization code! Exchanging for refresh token...\n");
      
      try {
        const tokenResponse = await fetch("https://oauth2.googleapis.com/token", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams({
            code,
            client_id: CLIENT_ID,
            client_secret: CLIENT_SECRET,
            redirect_uri: REDIRECT_URI,
            grant_type: "authorization_code",
          }),
        });
        
        const tokenData = await tokenResponse.json() as any;
        
        if (tokenData.error) {
          console.error(`TOKEN ERROR: ${tokenData.error} — ${tokenData.error_description}`);
          server.stop();
          process.exit(1);
        }
        
        const refreshToken = tokenData.refresh_token;
        const accessToken = tokenData.access_token;
        
        if (!refreshToken) {
          console.error(`
WARNING: No refresh token returned!
This usually means the account already had a token issued.
Go to https://myaccount.google.com/permissions and REMOVE
the "frankie" app, then run this script again.
`);
          server.stop();
          process.exit(1);
        }
        
        // Verify the token works by hitting userinfo
        const userInfo = await fetch("https://www.googleapis.com/oauth2/v2/userinfo", {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        const user = await userInfo.json() as any;
        
        const envKey = `GOOGLE_${account.toUpperCase()}_REFRESH_TOKEN`;
        
        console.log(`
╔══════════════════════════════════════════════════════════════╗
║  ✅ SUCCESS — ${account.toUpperCase()} AUTH COMPLETE
╠══════════════════════════════════════════════════════════════╣
║  Account: ${user.email || email}
║  Name:    ${user.name || "N/A"}
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Add this to your .env file:                                 ║
║                                                              ║
║  ${envKey}=${refreshToken}
║                                                              ║
║  Also make sure these are set:                               ║
║  GOOGLE_${account.toUpperCase()}_CLIENT_ID=${CLIENT_ID}
║  GOOGLE_${account.toUpperCase()}_CLIENT_SECRET=${CLIENT_SECRET}
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
`);
        
        server.stop();
        
        // Give the response time to send before exiting
        setTimeout(() => process.exit(0), 1000);
        
        return new Response(`
          <html><body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>✅ Auth Complete!</h1>
            <p>Refresh token for <strong>${user.email || email}</strong> has been printed in your terminal.</p>
            <p>You can close this tab.</p>
          </body></html>
        `, { headers: { "Content-Type": "text/html" } });
        
      } catch (err) {
        console.error("Failed to exchange code:", err);
        server.stop();
        process.exit(1);
      }
    }
    
    return new Response("Waiting for OAuth callback...", { status: 200 });
  },
});

console.log("(Press Ctrl+C to cancel)\n");
