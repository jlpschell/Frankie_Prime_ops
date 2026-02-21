import os, re, json, urllib.request, urllib.parse
ENV_PATH = os.path.expanduser('~/.openclaw/.env')
CLIENT_ID = '581850119904-bqpi8pcs0r841ji1244l0ei1na0b8rsc.apps.googleusercontent.com'
CLIENT_SECRET = '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'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
KEYS = ['GOOGLE_PERSONAL_REFRESH_TOKEN','GOOGLE_BUSINESS_REFRESH_TOKEN','GOOGLE_REFRESH_TOKEN']

def load_env():
    return open(ENV_PATH).read()

def get_token(env, key):
    m = re.search(rf'^{key}=(.+)$', env, re.MULTILINE)
    return m.group(1).strip() if m else None

def refresh(token):
    data = urllib.parse.urlencode({'client_id':CLIENT_ID,'client_secret':CLIENT_SECRET,'refresh_token':token,'grant_type':'refresh_token'}).encode()
    req = urllib.request.Request(TOKEN_URL, data=data, method='POST')
    req.add_header('Content-Type','application/x-www-form-urlencoded')
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result.get('refresh_token', token)
    except Exception as e:
        print(f'  ERROR: {e}')
        return None

env = load_env()
for key in KEYS:
    current = get_token(env, key)
    if not current:
        print(f'SKIP: {key} not in .env')
        continue
    new = refresh(current)
    if new:
        env = re.sub(rf'^{key}=.*$', f'{key}={new}', env, flags=re.MULTILINE)
        print(f'OK: {key}')
    else:
        print(f'FAILED: {key}')

open(ENV_PATH,'w').write(env)
print('Done')
