import * as http from 'http';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SCOPES = [
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/calendar.readonly'
];

const PORT = 8085;
const CREDENTIALS_PATH = path.join(__dirname, '..', 'gmail_credentials.json');
const TOKEN_PATH = path.join(__dirname, '..', 'credentials', 'token.json');

async function main() {
  // Load credentials
  const credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf-8'));
  const { client_id, client_secret } = credentials.installed;

  const redirect_uri = `http://localhost:${PORT}`;

  // Build auth URL
  const authUrl = new URL('https://accounts.google.com/o/oauth2/auth');
  authUrl.searchParams.set('client_id', client_id);
  authUrl.searchParams.set('redirect_uri', redirect_uri);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('scope', SCOPES.join(' '));
  authUrl.searchParams.set('access_type', 'offline');
  authUrl.searchParams.set('prompt', 'consent');

  console.log('\n=== GOOGLE OAUTH ===');
  console.log('\nOpen this URL in your browser:\n');
  console.log(authUrl.toString());
  console.log('\n\nWaiting for callback on port', PORT, '...\n');

  // Start server to catch callback
  const server = http.createServer(async (req, res) => {
    const url = new URL(req.url!, `http://localhost:${PORT}`);
    const code = url.searchParams.get('code');

    if (code) {
      console.log('Got authorization code. Exchanging for tokens...');

      try {
        // Exchange code for tokens
        const tokenResponse = await fetch('https://oauth2.googleapis.com/token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: new URLSearchParams({
            code,
            client_id,
            client_secret,
            redirect_uri,
            grant_type: 'authorization_code'
          })
        });

        const tokens = await tokenResponse.json();

        if (tokens.error) {
          console.error('Token error:', tokens);
          res.writeHead(500);
          res.end('Error: ' + tokens.error_description);
          server.close();
          return;
        }

        // Add timestamp
        tokens.obtained_at = new Date().toISOString();

        // Save token
        fs.mkdirSync(path.dirname(TOKEN_PATH), { recursive: true });
        fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));

        console.log('\nToken saved to:', TOKEN_PATH);
        console.log('Access token:', tokens.access_token?.substring(0, 30) + '...');
        console.log('Refresh token:', tokens.refresh_token ? 'Present' : 'Missing');
        console.log('Expires in:', tokens.expires_in, 'seconds');

        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('<h1>Success!</h1><p>You can close this window.</p>');

        server.close();
        process.exit(0);

      } catch (err) {
        console.error('Exchange error:', err);
        res.writeHead(500);
        res.end('Error exchanging code');
        server.close();
      }
    } else {
      res.writeHead(400);
      res.end('No code received');
    }
  });

  server.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
  });
}

main().catch(console.error);
