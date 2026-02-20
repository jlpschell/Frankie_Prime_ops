#!/bin/bash
# sb-sync.sh — Shared Brain: Read/write files, messages, logs, skills via Supabase
# Usage:
#   sb-sync.sh read <file_path>            — pull file from Supabase
#   sb-sync.sh write <file_path> <agent>   — push local file to Supabase
#   sb-sync.sh list                        — list all shared files
#   sb-sync.sh log <agent> <action> <summary> [file_path] — write to sync_log
#   sb-sync.sh changelog [limit]           — read recent sync_log entries
#   sb-sync.sh msg <to> "<message>" <from> — send agent message
#   sb-sync.sh inbox <agent>               — check unread messages
#   sb-sync.sh ack <message_id> "<response>" — respond to a message
#   sb-sync.sh skill-push <name> <file> <agent> "<desc>" — push a skill
#   sb-sync.sh skill-pull <name>           — pull a skill's code
#   sb-sync.sh skill-list                  — list available skills

source /home/plotting1/frankie-bot/.env 2>/dev/null

SB_URL="${SUPABASE_URL}"
SB_KEY="${SUPABASE_SERVICE_ROLE_KEY}"
HEADERS=(-H "apikey: $SB_KEY" -H "Authorization: Bearer $SB_KEY" -H "Content-Type: application/json")

json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))"
}

case "$1" in
  read)
    curl -s "$SB_URL/rest/v1/shared_files?file_path=eq.$2&select=content,updated_by,updated_at,version" \
      "${HEADERS[@]}" | python3 -c "
import sys,json
data=json.load(sys.stdin)
if data: print(data[0]['content'])
else: print('FILE_NOT_FOUND')"
    ;;

  write)
    FILE_PATH="$2"; AGENT="${3:-prime}"
    CONTENT=$(cat "$FILE_PATH" 2>/dev/null || echo "")
    if [ -z "$CONTENT" ]; then echo "ERROR: File empty/missing: $FILE_PATH"; exit 1; fi
    JSON_CONTENT=$(echo "$CONTENT" | json_escape)
    curl -s "$SB_URL/rest/v1/shared_files" \
      "${HEADERS[@]}" \
      -H "Prefer: resolution=merge-duplicates,return=minimal" \
      -d "{\"file_path\":\"$FILE_PATH\",\"content\":$JSON_CONTENT,\"updated_by\":\"$AGENT\",\"updated_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"version\":1}" \
      -X POST
    echo "SYNCED: $FILE_PATH by $AGENT"
    ;;

  list)
    curl -s "$SB_URL/rest/v1/shared_files?select=file_path,updated_by,updated_at,version,tags&order=updated_at.desc" \
      "${HEADERS[@]}" | python3 -c "
import sys,json
for f in json.load(sys.stdin): print(f'{f[\"file_path\"]} | by {f[\"updated_by\"]} | {f[\"updated_at\"]}')"
    ;;

  log)
    AGENT="$2"; ACTION="$3"; SUMMARY="$4"; FPATH="${5:-}"
    JSON_SUM=$(echo "$SUMMARY" | json_escape)
    BODY="{\"agent\":\"$AGENT\",\"action\":\"$ACTION\",\"summary\":$JSON_SUM"
    [ -n "$FPATH" ] && BODY="$BODY,\"file_path\":\"$FPATH\""
    BODY="$BODY}"
    curl -s "$SB_URL/rest/v1/sync_log" \
      "${HEADERS[@]}" -H "Prefer: return=minimal" -d "$BODY" -X POST
    echo "LOGGED: [$AGENT] $ACTION — $SUMMARY"
    ;;

  changelog)
    LIMIT="${2:-20}"
    curl -s "$SB_URL/rest/v1/sync_log?select=agent,action,file_path,summary,created_at&order=created_at.desc&limit=$LIMIT" \
      "${HEADERS[@]}" | python3 -c "
import sys,json
for e in json.load(sys.stdin):
  fp = f' ({e[\"file_path\"]})' if e.get('file_path') else ''
  print(f'[{e[\"created_at\"]}] {e[\"agent\"]}/{e[\"action\"]}{fp}: {e[\"summary\"]}')"
    ;;

  msg)
    TO="$2"; MSG="$3"; FROM="${4:-prime}"
    JSON_MSG=$(echo "$MSG" | json_escape)
    curl -s "$SB_URL/rest/v1/agent_messages" \
      "${HEADERS[@]}" -H "Prefer: return=minimal" \
      -d "{\"from_agent\":\"$FROM\",\"to_agent\":\"$TO\",\"message\":$JSON_MSG,\"message_type\":\"chat\",\"status\":\"sent\"}" \
      -X POST
    echo "MSG SENT: $FROM → $TO"
    ;;

  inbox)
    AGENT="${2:-prime}"
    curl -s "$SB_URL/rest/v1/agent_messages?to_agent=eq.$AGENT&status=eq.sent&order=created_at.desc&limit=10" \
      "${HEADERS[@]}" | python3 -c "
import sys,json
data=json.load(sys.stdin)
if not data: print('No unread messages.')
for m in data: print(f'[{m[\"created_at\"]}] {m[\"from_agent\"]}: {m[\"message\"]} (id:{m[\"id\"]})')"
    ;;

  ack)
    MSG_ID="$2"; RESPONSE="$3"
    JSON_RESP=$(echo "$RESPONSE" | json_escape)
    curl -s "$SB_URL/rest/v1/agent_messages?id=eq.$MSG_ID" \
      "${HEADERS[@]}" -H "Prefer: return=minimal" \
      -d "{\"response\":$JSON_RESP,\"status\":\"read\",\"responded_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
      -X PATCH
    echo "ACK: $MSG_ID"
    ;;

  skill-push)
    NAME="$2"; FILE="$3"; AGENT="${4:-prime}"; DESC="${5:-}"
    CODE=$(cat "$FILE" 2>/dev/null || echo "")
    if [ -z "$CODE" ]; then echo "ERROR: File empty/missing: $FILE"; exit 1; fi
    LANG="bash"
    [[ "$FILE" == *.py ]] && LANG="python"
    [[ "$FILE" == *.js ]] && LANG="javascript"
    JSON_CODE=$(echo "$CODE" | json_escape)
    JSON_DESC=$(echo "$DESC" | json_escape)
    curl -s "$SB_URL/rest/v1/skills" \
      "${HEADERS[@]}" -H "Prefer: resolution=merge-duplicates,return=minimal" \
      -d "{\"name\":\"$NAME\",\"code\":$JSON_CODE,\"language\":\"$LANG\",\"created_by\":\"$AGENT\",\"description\":$JSON_DESC,\"updated_at\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
      -X POST
    echo "SKILL PUSHED: $NAME ($LANG) by $AGENT"
    ;;

  skill-pull)
    curl -s "$SB_URL/rest/v1/skills?name=eq.$2&select=code,language,description,created_by,updated_at" \
      "${HEADERS[@]}" | python3 -c "
import sys,json
data=json.load(sys.stdin)
if data: print(data[0]['code'])
else: print('SKILL_NOT_FOUND')"
    ;;

  skill-list)
    curl -s "$SB_URL/rest/v1/skills?select=name,language,description,created_by,updated_at&order=updated_at.desc" \
      "${HEADERS[@]}" | python3 -c "
import sys,json
for s in json.load(sys.stdin): print(f'{s[\"name\"]} ({s[\"language\"]}) by {s[\"created_by\"]} — {s.get(\"description\",\"\")} [{s[\"updated_at\"]}]')"
    ;;

  *)
    echo "sb-sync.sh — Shared Brain CLI"
    echo "  read <path>                    Pull file from Supabase"
    echo "  write <path> <agent>           Push file to Supabase"
    echo "  list                           List shared files"
    echo "  log <agent> <action> <summary> Write sync log"
    echo "  changelog [limit]              Read sync log"
    echo "  msg <to> <msg> <from>          Send agent message"
    echo "  inbox <agent>                  Check unread messages"
    echo "  ack <id> <response>            Respond to message"
    echo "  skill-push <name> <file> <agent> <desc>  Push skill"
    echo "  skill-pull <name>              Pull skill code"
    echo "  skill-list                     List skills"
    ;;
esac
