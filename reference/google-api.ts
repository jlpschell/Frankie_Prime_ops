/**
 * GOOGLE API — Multi-Account Router (Task 0.5)
 * 
 * WHY THIS EXISTS:
 * Before: One set of credentials, split across two Cloud projects, incomplete scopes.
 * After: One Cloud project (frankie1-486714), three accounts, each with full scopes.
 * 
 * HOW IT WORKS:
 * Every function takes an `account` parameter: "personal" | "business" | "workspace"
 * This picks the right Client ID, Client Secret, and Refresh Token from .env
 * Then uses that token to make the API call.
 * 
 * ACCOUNT MAP:
 *   personal  = jlpschell@gmail.com    (Jay's primary — Drive, Gmail, Calendar, Sheets, YouTube)
 *   business  = humanledai@gmail.com   (Business stopgap — Gmail, Calendar, Drive, Sheets)
 *   workspace = jason@humanledai.net   (Future — Gmail, Calendar only for now)
 */

import { google, type Auth } from "googleapis";

// ═══════════════════════════════════════════════════════
// ACCOUNT TYPES & AUTH
// ═══════════════════════════════════════════════════════

export type GoogleAccount = "personal" | "business" | "workspace";

interface AccountCredentials {
  clientId: string;
  clientSecret: string;
  refreshToken: string;
}

/**
 * Pulls the right credentials from .env based on account name.
 * 
 * In plain English: This is like picking the right key ring 
 * for whichever office you need to open.
 */
function getCredentials(account: GoogleAccount): AccountCredentials {
  const prefix = `GOOGLE_${account.toUpperCase()}`;
  
  const clientId = process.env[`${prefix}_CLIENT_ID`] || "";
  const clientSecret = process.env[`${prefix}_CLIENT_SECRET`] || "";
  const refreshToken = process.env[`${prefix}_REFRESH_TOKEN`] || "";
  
  if (!clientId || !clientSecret || !refreshToken) {
    throw new Error(
      `Missing credentials for ${account} account. ` +
      `Check .env for ${prefix}_CLIENT_ID, ${prefix}_CLIENT_SECRET, ${prefix}_REFRESH_TOKEN`
    );
  }
  
  return { clientId, clientSecret, refreshToken };
}

/**
 * Creates an authenticated Google OAuth2 client for the given account.
 * This is the "master key" that all Google API calls use.
 */
function getAuthClient(account: GoogleAccount): Auth.OAuth2Client {
  const creds = getCredentials(account);
  
  const auth = new google.auth.OAuth2(
    creds.clientId,
    creds.clientSecret,
    "http://localhost:3456/callback"
  );
  
  auth.setCredentials({ refresh_token: creds.refreshToken });
  
  return auth;
}

// Cache auth clients so we don't recreate them every call
const authCache: Partial<Record<GoogleAccount, Auth.OAuth2Client>> = {};

function getAuth(account: GoogleAccount): Auth.OAuth2Client {
  if (!authCache[account]) {
    authCache[account] = getAuthClient(account);
  }
  return authCache[account]!;
}

// ═══════════════════════════════════════════════════════
// GMAIL FUNCTIONS
// ═══════════════════════════════════════════════════════

/**
 * Gets recent emails from the specified account.
 * 
 * account: which inbox to check
 * maxResults: how many emails to return (default 10)
 * query: Gmail search query (e.g., "is:unread", "from:boss@company.com")
 */
export async function getEmails(
  account: GoogleAccount,
  maxResults: number = 10,
  query: string = ""
): Promise<any[]> {
  const auth = getAuth(account);
  const gmail = google.gmail({ version: "v1", auth });
  
  try {
    const listResponse = await gmail.users.messages.list({
      userId: "me",
      maxResults,
      q: query,
    });
    
    const messages = listResponse.data.messages || [];
    
    // Fetch full details for each message
    const detailed = await Promise.all(
      messages.map(async (msg) => {
        const full = await gmail.users.messages.get({
          userId: "me",
          id: msg.id!,
          format: "metadata",
          metadataHeaders: ["From", "To", "Subject", "Date"],
        });
        
        const headers = full.data.payload?.headers || [];
        const getHeader = (name: string) =>
          headers.find((h) => h.name?.toLowerCase() === name.toLowerCase())?.value || "";
        
        return {
          id: msg.id,
          threadId: msg.threadId,
          from: getHeader("From"),
          to: getHeader("To"),
          subject: getHeader("Subject"),
          date: getHeader("Date"),
          snippet: full.data.snippet,
          labelIds: full.data.labelIds,
          isUnread: full.data.labelIds?.includes("UNREAD") || false,
        };
      })
    );
    
    console.log(`GMAIL [${account}]: Retrieved ${detailed.length} emails`);
    return detailed;
    
  } catch (error: any) {
    console.error(`GMAIL ERROR [${account}]:`, error.message);
    throw error;
  }
}

/**
 * Gets unread email count for the specified account.
 */
export async function getUnreadCount(account: GoogleAccount): Promise<number> {
  const auth = getAuth(account);
  const gmail = google.gmail({ version: "v1", auth });
  
  const response = await gmail.users.messages.list({
    userId: "me",
    q: "is:unread",
    maxResults: 1,
  });
  
  return response.data.resultSizeEstimate || 0;
}

/**
 * Sends an email from the specified account.
 * ACTION CLASS: CONFIRM (per PRD — requires Jay's approval before sending)
 */
export async function sendEmail(
  account: GoogleAccount,
  to: string,
  subject: string,
  body: string
): Promise<string> {
  const auth = getAuth(account);
  const gmail = google.gmail({ version: "v1", auth });
  
  // Build RFC 2822 formatted email
  const email = [
    `To: ${to}`,
    `Subject: ${subject}`,
    `Content-Type: text/html; charset=utf-8`,
    `MIME-Version: 1.0`,
    "",
    body,
  ].join("\r\n");
  
  const encodedMessage = Buffer.from(email)
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
  
  const response = await gmail.users.messages.send({
    userId: "me",
    requestBody: { raw: encodedMessage },
  });
  
  console.log(`GMAIL [${account}]: Sent email to ${to} — ID: ${response.data.id}`);
  return response.data.id || "";
}

/**
 * Creates a draft email (does NOT send).
 * ACTION CLASS: SAFE (per PRD — drafts don't leave the inbox)
 */
export async function createDraft(
  account: GoogleAccount,
  to: string,
  subject: string,
  body: string
): Promise<string> {
  const auth = getAuth(account);
  const gmail = google.gmail({ version: "v1", auth });
  
  const email = [
    `To: ${to}`,
    `Subject: ${subject}`,
    `Content-Type: text/html; charset=utf-8`,
    `MIME-Version: 1.0`,
    "",
    body,
  ].join("\r\n");
  
  const encodedMessage = Buffer.from(email)
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
  
  const response = await gmail.users.drafts.create({
    userId: "me",
    requestBody: {
      message: { raw: encodedMessage },
    },
  });
  
  console.log(`GMAIL [${account}]: Draft created — ID: ${response.data.id}`);
  return response.data.id || "";
}

// ═══════════════════════════════════════════════════════
// CALENDAR FUNCTIONS
// ═══════════════════════════════════════════════════════

/**
 * Gets calendar events for today (or a specific date range).
 */
export async function getCalendarEvents(
  account: GoogleAccount,
  timeMin?: string,
  timeMax?: string
): Promise<any[]> {
  const auth = getAuth(account);
  const calendar = google.calendar({ version: "v3", auth });
  
  // Default to today if no range specified
  const now = new Date();
  const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const endOfDay = new Date(startOfDay.getTime() + 24 * 60 * 60 * 1000);
  
  try {
    const response = await calendar.events.list({
      calendarId: "primary",
      timeMin: timeMin || startOfDay.toISOString(),
      timeMax: timeMax || endOfDay.toISOString(),
      singleEvents: true,
      orderBy: "startTime",
      maxResults: 20,
    });
    
    const events = (response.data.items || []).map((event) => ({
      id: event.id,
      summary: event.summary,
      start: event.start?.dateTime || event.start?.date,
      end: event.end?.dateTime || event.end?.date,
      location: event.location,
      description: event.description,
      attendees: event.attendees?.map((a) => a.email),
      hangoutLink: event.hangoutLink,
    }));
    
    console.log(`CALENDAR [${account}]: Retrieved ${events.length} events`);
    return events;
    
  } catch (error: any) {
    console.error(`CALENDAR ERROR [${account}]:`, error.message);
    throw error;
  }
}

/**
 * Gets tomorrow's calendar events.
 */
export async function getTomorrowEvents(account: GoogleAccount): Promise<any[]> {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const start = new Date(tomorrow.getFullYear(), tomorrow.getMonth(), tomorrow.getDate());
  const end = new Date(start.getTime() + 24 * 60 * 60 * 1000);
  
  return getCalendarEvents(account, start.toISOString(), end.toISOString());
}

/**
 * Creates a calendar event.
 * ACTION CLASS: CONFIRM (per PRD)
 */
export async function createCalendarEvent(
  account: GoogleAccount,
  summary: string,
  startTime: string,
  endTime: string,
  description?: string,
  location?: string
): Promise<string> {
  const auth = getAuth(account);
  const calendar = google.calendar({ version: "v3", auth });
  
  const response = await calendar.events.insert({
    calendarId: "primary",
    requestBody: {
      summary,
      description,
      location,
      start: { dateTime: startTime, timeZone: "America/Chicago" },
      end: { dateTime: endTime, timeZone: "America/Chicago" },
    },
  });
  
  console.log(`CALENDAR [${account}]: Created event "${summary}" — ID: ${response.data.id}`);
  return response.data.id || "";
}

// ═══════════════════════════════════════════════════════
// DRIVE FUNCTIONS
// ═══════════════════════════════════════════════════════

/**
 * Searches Google Drive for files matching a query.
 */
export async function searchDrive(
  account: GoogleAccount,
  query: string,
  maxResults: number = 10
): Promise<any[]> {
  const auth = getAuth(account);
  const drive = google.drive({ version: "v3", auth });
  
  try {
    const response = await drive.files.list({
      q: `fullText contains '${query.replace(/'/g, "\\'")}'`,
      pageSize: maxResults,
      fields: "files(id, name, mimeType, modifiedTime, webViewLink)",
      orderBy: "modifiedTime desc",
    });
    
    const files = (response.data.files || []).map((f) => ({
      id: f.id,
      name: f.name,
      type: f.mimeType,
      modified: f.modifiedTime,
      link: f.webViewLink,
    }));
    
    console.log(`DRIVE [${account}]: Found ${files.length} files for "${query}"`);
    return files;
    
  } catch (error: any) {
    console.error(`DRIVE ERROR [${account}]:`, error.message);
    throw error;
  }
}

// ═══════════════════════════════════════════════════════
// SHEETS FUNCTIONS
// ═══════════════════════════════════════════════════════

/**
 * Reads data from a Google Sheet.
 */
export async function readSheet(
  account: GoogleAccount,
  spreadsheetId: string,
  range: string
): Promise<any[][]> {
  const auth = getAuth(account);
  const sheets = google.sheets({ version: "v4", auth });
  
  const response = await sheets.spreadsheets.values.get({
    spreadsheetId,
    range,
  });
  
  return response.data.values || [];
}

/**
 * Writes data to a Google Sheet.
 * ACTION CLASS: CONFIRM
 */
export async function writeSheet(
  account: GoogleAccount,
  spreadsheetId: string,
  range: string,
  values: any[][]
): Promise<number> {
  const auth = getAuth(account);
  const sheets = google.sheets({ version: "v4", auth });
  
  const response = await sheets.spreadsheets.values.update({
    spreadsheetId,
    range,
    valueInputOption: "USER_ENTERED",
    requestBody: { values },
  });
  
  return response.data.updatedCells || 0;
}

// ═══════════════════════════════════════════════════════
// UTILITY — DEFAULT ACCOUNT ROUTING
// ═══════════════════════════════════════════════════════

/**
 * Figures out which account to use based on context.
 * 
 * In plain English: If Jay says "check my email" without specifying,
 * this decides which inbox to check based on keywords.
 * 
 * Rules:
 *   - "business" / "humanledai" / "HLAI" → business account
 *   - "workspace" / "humanledai.net" / "jason@" → workspace account
 *   - Everything else → personal account (primary arm per PRD)
 */
export function resolveAccount(message: string): GoogleAccount {
  const lower = message.toLowerCase();
  
  if (
    lower.includes("business") ||
    lower.includes("humanledai@gmail") ||
    lower.includes("hlai")
  ) {
    return "business";
  }
  
  if (
    lower.includes("workspace") ||
    lower.includes("humanledai.net") ||
    lower.includes("jason@")
  ) {
    return "workspace";
  }
  
  return "personal";
}

// ═══════════════════════════════════════════════════════
// HEALTH CHECK — Used by heartbeat and tests
// ═══════════════════════════════════════════════════════

/**
 * Tests that a specific account's auth is working.
 * Returns true if the token can hit the Gmail API without error.
 */
export async function testAuth(account: GoogleAccount): Promise<boolean> {
  try {
    const auth = getAuth(account);
    const gmail = google.gmail({ version: "v1", auth });
    
    // Simple profile fetch — lightest possible API call
    const profile = await gmail.users.getProfile({ userId: "me" });
    console.log(`AUTH CHECK [${account}]: ✅ ${profile.data.emailAddress}`);
    return true;
    
  } catch (error: any) {
    console.error(`AUTH CHECK [${account}]: ❌ ${error.message}`);
    return false;
  }
}

/**
 * Tests ALL configured accounts. Used during startup and heartbeat.
 */
export async function testAllAuth(): Promise<Record<GoogleAccount, boolean>> {
  const results: Record<GoogleAccount, boolean> = {
    personal: false,
    business: false,
    workspace: false,
  };
  
  for (const account of ["personal", "business", "workspace"] as GoogleAccount[]) {
    try {
      results[account] = await testAuth(account);
    } catch {
      results[account] = false;
    }
  }
  
  return results;
}
