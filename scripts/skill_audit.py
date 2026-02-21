#!/usr/bin/env python3
"""
ClawdHub / OpenClaw Skill Package Auditor v2 — Contextual Scoring Engine
Extracts a zip and produces a binary SAFE / NOT SAFE verdict based on
weighted contextual analysis, not just raw pattern matches.

Usage: python3 skill_audit.py <path_to_zip_or_directory> [...]

Scoring philosophy:
  - Every flag gets a base weight
  - Context modifiers reduce weight (e.g., pattern inside markdown code block)
  - Context modifiers increase weight (e.g., pattern inside executable script)
  - Combination multipliers detect attack playbooks (e.g., executable + env harvest + outbound URL)
  - Known IoCs = instant NOT SAFE regardless of score
  - Final score maps to binary verdict: SAFE or NOT SAFE
"""

import os
import re
import sys
import zipfile
import tempfile
import shutil
from pathlib import Path
from collections import defaultdict

# =============================================================================
# CONFIGURATION
# =============================================================================

EXECUTABLE_EXTENSIONS = {
    '.sh', '.py', '.js', '.ts', '.exe', '.bat', '.cmd', '.ps1',
    '.rb', '.pl', '.php', '.cgi', '.jar', '.msi', '.com', '.vbs',
    '.wsf', '.scr'
}

DOCUMENTATION_EXTENSIONS = {'.md', '.txt', '.rst', '.html', '.htm'}

TEXT_EXTENSIONS = DOCUMENTATION_EXTENSIONS | {
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    '.xml', '.csv', '.js', '.ts', '.py', '.sh', '.rb', '.pl', '.php'
}

# Files that are inherently benign
BENIGN_FILENAMES = {'.gitignore', '.python-version', 'requirements.txt',
                    'pyproject.toml', 'package.json', 'Dockerfile',
                    'LICENSE', 'LICENSE.txt', 'LICENSE.md'}

# =============================================================================
# PATTERN DEFINITIONS — each pattern has (regex, category, base_weight)
#
# Weight scale:
#   0-2   = informational noise
#   3-5   = notable, worth logging
#   6-10  = concerning
#   11-20 = serious
#   21+   = critical / instant kill
# =============================================================================

PATTERNS = [
    # --- Instant kill (known IoCs) — weight 100 = auto NOT SAFE ---
    (r'91\.92\.242\.30', 'INSTANT_KILL', 100, 'Known C2 IP: ClawHavoc/AMOS campaign'),
    (r'openclaw-agent\.zip', 'INSTANT_KILL', 100, 'ClawHavoc dropper filename'),
    (r'reverse.shell|rev.shell|nc\s+-[a-z]*e\s+/bin/', 'INSTANT_KILL', 100, 'Reverse shell'),

    # --- Prompt injection (high base weight) ---
    (r'ignore\s+(all\s+)?previous\s+(instructions?|prompts?|rules?)', 'prompt_injection', 20, 'Ignore previous instructions'),
    (r'ignore\s+(all\s+)?above', 'prompt_injection', 18, 'Ignore above'),
    (r'disregard\s+(all\s+)?previous', 'prompt_injection', 20, 'Disregard previous'),
    (r'forget\s+(all\s+)?(your|previous)\s+(instructions?|rules?)', 'prompt_injection', 20, 'Forget instructions'),
    (r'you\s+are\s+now\s+[a-z]+', 'prompt_injection', 15, 'Role reassignment'),
    (r'new\s+system\s+prompt', 'prompt_injection', 20, 'System prompt override'),
    (r'override\s+(system|safety|instructions?)', 'prompt_injection', 18, 'Override attempt'),
    (r'act\s+as\s+if\s+you\s+have\s+no\s+(restrictions?|limits?|rules?)', 'prompt_injection', 20, 'Remove restrictions'),
    (r'do\s+not\s+follow\s+(your|the)\s+(rules?|guidelines?|instructions?)', 'prompt_injection', 20, 'Rule bypass'),

    # --- Data exfiltration ---
    (r'(send|post|upload|exfiltrate|transmit)\s+.{0,30}(env|secret|key|token|credential|password)', 'exfiltration', 25, 'Exfil sensitive data'),
    (r'~/.clawdbot/\.env', 'exfiltration', 30, 'Targeting clawdbot env'),
    (r'~/.openclaw/\.env', 'exfiltration', 30, 'Targeting openclaw env'),

    # --- Remote code execution ---
    (r'curl\s+.*\|\s*(bash|sh|python)', 'rce', 15, 'Pipe to shell'),

    # --- Suspicious URLs ---
    (r'https?://[a-z0-9.-]*webhook\.site', 'suspicious_url', 20, 'webhook.site (exfil target)'),
    (r'https?://[a-z0-9.-]*ngrok\.(io|app)', 'suspicious_url', 10, 'ngrok tunnel'),
    (r'https?://[a-z0-9.-]*requestbin\.(com|net)', 'suspicious_url', 15, 'requestbin'),
    (r'https?://[a-z0-9.-]*pipedream\.net', 'suspicious_url', 12, 'pipedream'),
    (r'https?://[a-z0-9.-]*burpcollaborator\.net', 'suspicious_url', 20, 'burp collaborator'),
    (r'https?://[a-z0-9.-]*interact\.sh', 'suspicious_url', 18, 'interactsh'),
    (r'https?://[a-z0-9.-]*oast\.(fun|me|live)', 'suspicious_url', 18, 'oast callback'),
    (r'https?://[a-z0-9.-]*pastebin\.com', 'suspicious_url', 8, 'pastebin'),
    (r'https?://[a-z0-9.-]*glot\.io', 'suspicious_url', 25, 'glot.io (ClawHavoc IoC)'),
    (r'https?://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', 'suspicious_url', 5, 'Raw IP address'),

    # --- Env access (low base — context determines real weight) ---
    (r'os\.environ', 'env_access', 1, 'os.environ'),
    (r'process\.env', 'env_access', 1, 'process.env'),
    (r'load_dotenv', 'env_access', 1, 'dotenv loading'),
    (r'\$\{?[A-Z_]{3,}(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)\}?', 'env_ref', 2, 'Sensitive var name'),

    # --- Obfuscation ---
    (r'eval\s*\(', 'obfuscation', 6, 'eval()'),
    (r'exec\s*\(', 'obfuscation', 6, 'exec()'),
    (r'atob\s*\(', 'obfuscation', 8, 'atob() base64 decode'),
    (r'btoa\s*\(', 'obfuscation', 4, 'btoa() base64 encode'),
    (r'base64\.(b64)?decode', 'obfuscation', 7, 'base64 decode'),
    (r'\\x[0-9a-f]{2}\\x[0-9a-f]{2}\\x[0-9a-f]{2}', 'obfuscation', 10, 'Hex escape sequences'),
    (r'String\.fromCharCode', 'obfuscation', 8, 'fromCharCode'),
    (r'[A-Za-z0-9+/=]{100,}', 'obfuscation', 3, 'Possible base64 blob'),

    # --- Command execution ---
    (r'subprocess\.(run|call|Popen|check_output)', 'cmd_exec', 5, 'subprocess'),
    (r'child_process\.(exec|spawn|fork)', 'cmd_exec', 5, 'child_process'),
    (r'os\.system\s*\(', 'cmd_exec', 7, 'os.system'),
    (r'os\.popen\s*\(', 'cmd_exec', 7, 'os.popen'),

    # --- Social engineering ---
    (r'prerequisite|pre-requisite', 'social_eng', 4, 'Prerequisite mention'),
    (r'paste\s+(it\s+)?(in|into)\s+(your\s+)?(terminal|shell|command\s+line|console)', 'social_eng', 8, 'Paste into terminal'),

    # --- Hidden plugin configs ---
    (r'\.claude-plugin', 'hidden_plugin', 8, '.claude-plugin directory'),

    # --- Typosquats ---
    (r'\b(clawhub[b1l]|clawwhub|clawhubcli|claw-hub|cllawhub|clawhuub)\b', 'typosquat', 25, 'clawhub variant'),
    (r'\b(openc1aw|openclaaw|opennclaw|0penclaw)\b', 'typosquat', 25, 'openclaw variant'),
    (r'\b(clawdb0t|clawdbot[t1]|clawddbot)\b', 'typosquat', 25, 'clawdbot variant'),

    # --- Memory poisoning ---
    (r'(write|append|add|inject|insert)\s+.{0,30}(memory|MEMORY\.md|memory/)', 'memory_poison', 12, 'Writes to memory files'),
    (r'(when|if|once)\s+.{0,40}(available|enabled|installed|connected)\s*[,.]?\s*(then\s+)?(run|execute|send|post|fetch)', 'logic_bomb', 10, 'Conditional delayed execution'),

    # --- Bait categories (weak signal alone, amplifier with other flags) ---
    (r'(solana|bitcoin|ethereum|crypto|wallet).*(track|find|recover|lost)', 'bait_category', 3, 'Crypto bait'),
    (r'polymarket', 'bait_category', 3, 'Polymarket bait'),
    (r'auto.?update', 'bait_category', 2, 'Auto-updater bait'),
]

# =============================================================================
# CONTEXT MODIFIERS
# =============================================================================

def is_inside_markdown_codeblock(lines, line_num):
    """Check if a line is inside a ``` code block in a markdown file."""
    in_block = False
    for i in range(min(line_num, len(lines))):
        stripped = lines[i].strip()
        if stripped.startswith('```'):
            in_block = not in_block
    return in_block

def is_in_comment(line):
    """Check if the match is in a code comment."""
    stripped = line.strip()
    return stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('*')

def get_context_modifier(filepath, line, lines, line_num, category):
    """
    Returns a multiplier (0.0 to 3.0) based on where the pattern was found.
    < 1.0 = reduces weight (benign context)
    1.0   = neutral
    > 1.0 = amplifies weight (dangerous context)
    """
    ext = Path(filepath).suffix.lower()
    fname = Path(filepath).name
    is_doc = ext in DOCUMENTATION_EXTENSIONS
    is_exec = ext in EXECUTABLE_EXTENSIONS
    is_test = 'test' in fname.lower() or 'spec' in fname.lower()
    is_example = 'example' in fname.lower() or 'sample' in fname.lower()
    is_benign_file = fname in BENIGN_FILENAMES

    # .gitignore mentioning .env = good practice, not suspicious
    if is_benign_file and category in ('env_access', 'env_ref'):
        return 0.0

    # Test files — env manipulation is expected
    if is_test and category in ('env_access', 'env_ref', 'cmd_exec'):
        return 0.1

    # Example/sample files
    if is_example:
        return 0.2

    # Pattern inside a markdown code block = documentation/example
    if is_doc and lines:
        if is_inside_markdown_codeblock(lines, line_num):
            # Env refs in code examples = teaching, not stealing
            if category in ('env_access', 'env_ref'):
                return 0.1
            # But RCE/exfil patterns in code blocks are still suspicious
            # (ClawHavoc hides `curl | sh` in "prerequisite" code blocks)
            if category in ('rce', 'exfiltration', 'suspicious_url'):
                return 0.7
            return 0.3

    # Comments
    if is_in_comment(line):
        if category in ('env_access', 'env_ref'):
            return 0.1
        return 0.4

    # Documentation file but NOT in a code block
    if is_doc:
        if category in ('env_access', 'env_ref'):
            return 0.2
        if category == 'social_eng':
            return 1.5  # Social engineering in docs = the actual attack surface
        return 0.8

    # Executable file — distinguish between "tool using its own env" and "tool stealing your env"
    if is_exec:
        if category in ('exfiltration', 'rce', 'suspicious_url', 'obfuscation'):
            return 2.0  # Dangerous patterns in actual code = very bad
        if category == 'env_access':
            return 0.15  # Apps reading their own config is normal — volume shouldn't inflate score
        if category == 'env_ref':
            return 0.15  # Same — referencing env var names in own code is expected
        if category == 'cmd_exec':
            return 0.5   # Subprocess in app code is common — only dangerous with other signals
        return 1.5

    return 1.0

# =============================================================================
# COMBINATION MULTIPLIERS — detect attack playbooks
# =============================================================================

def compute_combination_bonus(result):
    """
    Look at the full set of findings and apply bonus points when dangerous
    combinations are detected. Returns bonus points to add to total score.
    """
    bonus = 0
    categories_found = set(f['category'] for f in result.findings)
    has_executables = len(result.executable_files) > 0
    has_hidden = len(result.hidden_files) > 0

    # --- ClawHavoc playbook: executable + env harvest + outbound URL ---
    if has_executables and 'env_access' in categories_found and \
       ('suspicious_url' in categories_found or 'exfiltration' in categories_found):
        bonus += 30
        result.combos.append('🔗 COMBO: Executable + env access + outbound URL = exfiltration pipeline')

    # --- Hidden plugin + any other suspicious activity ---
    if 'hidden_plugin' in categories_found and len(categories_found) > 2:
        bonus += 20
        result.combos.append('🔗 COMBO: Hidden plugin config + other suspicious activity')

    # --- Social engineering + RCE ---
    if 'social_eng' in categories_found and 'rce' in categories_found:
        bonus += 25
        result.combos.append('🔗 COMBO: Social engineering + remote code execution = ClawHavoc pattern')

    # --- Obfuscation + any outbound communication ---
    if 'obfuscation' in categories_found and \
       ('suspicious_url' in categories_found or 'exfiltration' in categories_found):
        bonus += 20
        result.combos.append('🔗 COMBO: Obfuscation + outbound communication = hiding exfiltration')

    # --- Typosquat + anything ---
    if 'typosquat' in categories_found:
        bonus += 30
        result.combos.append('🔗 COMBO: Typosquat name = malicious intent')

    # --- Bait category + executable + env access ---
    if 'bait_category' in categories_found and has_executables and 'env_access' in categories_found:
        bonus += 15
        result.combos.append('🔗 COMBO: Known bait category + executable + env access')

    # --- Many hidden files (>3) beyond just .gitignore ---
    non_benign_hidden = [f for f in result.hidden_files
                         if Path(f).name not in BENIGN_FILENAMES]
    if len(non_benign_hidden) > 3:
        bonus += 10
        result.combos.append(f'🔗 COMBO: {len(non_benign_hidden)} non-standard hidden files')

    # --- Memory poisoning + any other flag ---
    if 'memory_poison' in categories_found and len(categories_found) > 1:
        bonus += 20
        result.combos.append('🔗 COMBO: Memory manipulation + other suspicious patterns')

    return bonus

# =============================================================================
# VERDICT THRESHOLDS
# =============================================================================
THRESHOLD_NOT_SAFE = 25   # Total weighted score >= this = NOT SAFE
THRESHOLD_REVIEW  = 12    # Score >= this but < NOT_SAFE = MANUAL REVIEW

# =============================================================================
# AUDIT RESULT CLASS
# =============================================================================

class AuditResult:
    def __init__(self, package_name):
        self.package_name = package_name
        self.findings = []   # list of dicts
        self.file_count = 0
        self.executable_files = []
        self.hidden_files = []
        self.text_files_scanned = 0
        self.combos = []
        self.total_score = 0
        self.has_instant_kill = False
        self.instant_kill_reason = ''

    def add(self, category, weight, filepath, line_num=None, detail='', context=''):
        self.findings.append({
            'category': category,
            'weight': weight,
            'file': filepath,
            'line': line_num,
            'detail': detail,
            'context': context.strip()[:120] if context else '',
        })

    def compute_verdict(self):
        """Calculate total score and determine binary verdict.
        
        Per-category caps prevent volume inflation — 50 harmless env reads
        in a Python app shouldn't score the same as 1 actual exfiltration attempt.
        """
        if self.has_instant_kill:
            self.total_score = 999
            return

        # Cap per-category contribution to prevent volume inflation
        CATEGORY_CAPS = {
            'env_access': 8,      # Reading env vars is normal for apps
            'env_ref': 6,         # Referencing var names is normal
            'cmd_exec': 15,       # Subprocess is common in tools
            'social_eng': 20,     # Can compound but has a ceiling
            'bait_category': 10,  # Weak signal, don't let it dominate
            'obfuscation': 25,    # Can be legit (base64 in data processing)
        }

        category_totals = defaultdict(float)
        for f in self.findings:
            category_totals[f['category']] += f['weight']

        self.total_score = 0
        for cat, total in category_totals.items():
            cap = CATEGORY_CAPS.get(cat)
            if cap is not None:
                self.total_score += min(total, cap)
            else:
                self.total_score += total  # No cap for high-danger categories

        self.total_score += compute_combination_bonus(self)

    def verdict(self):
        if self.has_instant_kill:
            return f'🚨 NOT SAFE — Instant kill: {self.instant_kill_reason}'
        elif self.total_score >= THRESHOLD_NOT_SAFE:
            return f'🚨 NOT SAFE (score: {self.total_score})'
        elif self.total_score >= THRESHOLD_REVIEW:
            return f'🟡 MANUAL REVIEW (score: {self.total_score})'
        else:
            return f'✅ SAFE (score: {self.total_score})'

    def is_safe(self):
        return self.total_score < THRESHOLD_NOT_SAFE and not self.has_instant_kill

    def report(self):
        lines = []
        lines.append(f'\n{"="*60}')
        lines.append(f'  AUDIT: {self.package_name}')
        lines.append(f'  VERDICT: {self.verdict()}')
        lines.append(f'{"="*60}')
        lines.append(f'  Files: {self.file_count} total, {self.text_files_scanned} scanned')
        lines.append(f'  Executables: {len(self.executable_files)}')
        lines.append(f'  Hidden: {len(self.hidden_files)}')
        lines.append(f'  Raw findings: {len(self.findings)}')
        lines.append(f'  Weighted score: {self.total_score}')
        lines.append(f'{"="*60}')

        # Show combos first — these tell the story
        if self.combos:
            lines.append('\n🔗 ATTACK PATTERN COMBINATIONS:')
            for c in self.combos:
                lines.append(f'  {c}')

        # Show significant findings (weight > 0, skip noise)
        significant = sorted([f for f in self.findings if f['weight'] >= 3],
                             key=lambda f: -f['weight'])

        if significant:
            lines.append(f'\n📋 SIGNIFICANT FINDINGS ({len(significant)}):')
            for f in significant[:30]:  # Cap output
                loc = f['file']
                if f['line']:
                    loc += f':{f["line"]}'
                icon = '🔴' if f['weight'] >= 15 else '🟡' if f['weight'] >= 5 else '🟠'
                lines.append(f'  {icon} [{f["weight"]:>3}pts] {f["detail"]}')
                lines.append(f'         {loc}')
                if f['context']:
                    lines.append(f'         > {f["context"]}')

        # Show suppressed noise count
        noise = [f for f in self.findings if f['weight'] < 3]
        if noise:
            lines.append(f'\n  ℹ️  {len(noise)} low-weight findings suppressed (env refs in docs/tests/comments)')

        # Show executables if any
        if self.executable_files:
            lines.append(f'\n📁 EXECUTABLE FILES ({len(self.executable_files)}):')
            for f in self.executable_files[:15]:
                lines.append(f'  ⚠️  {f}')
            if len(self.executable_files) > 15:
                lines.append(f'  ... and {len(self.executable_files) - 15} more')

        # Show non-benign hidden files
        non_benign_hidden = [f for f in self.hidden_files
                             if Path(f).name not in BENIGN_FILENAMES]
        if non_benign_hidden:
            lines.append(f'\n👁️ HIDDEN FILES ({len(non_benign_hidden)} non-standard):')
            for f in non_benign_hidden:
                lines.append(f'  ⚠️  {f}')

        lines.append(f'\n{"="*60}\n')
        return '\n'.join(lines)


# =============================================================================
# SCANNING
# =============================================================================

def scan_file(filepath, rel_path, result):
    """Scan a single text file with contextual weighting."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return

    result.text_files_scanned += 1
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        for pattern, category, base_weight, detail in PATTERNS:
            flags = re.IGNORECASE if category in ('prompt_injection', 'suspicious_url',
                                                    'social_eng', 'typosquat',
                                                    'bait_category') else 0
            match = re.search(pattern, line, flags)
            if match:
                # Instant kill — no context needed
                if category == 'INSTANT_KILL':
                    result.has_instant_kill = True
                    result.instant_kill_reason = detail
                    result.add(category, base_weight, rel_path, line_num, detail, line)
                    continue

                # Apply context modifier
                modifier = get_context_modifier(rel_path, line, lines, line_num, category)
                weighted = round(base_weight * modifier, 1)

                # Only record if weight > 0
                if weighted > 0:
                    result.add(category, weighted, rel_path, line_num, detail, line)


def audit_directory(dirpath, package_name=None):
    """Audit an extracted package directory."""
    dirpath = Path(dirpath)
    if not package_name:
        package_name = dirpath.name

    result = AuditResult(package_name)

    for root, dirs, files in os.walk(dirpath):
        for fname in files:
            filepath = Path(root) / fname
            rel_path = str(filepath.relative_to(dirpath))
            result.file_count += 1

            # Check hidden
            parts = Path(rel_path).parts
            if any(p.startswith('.') and p not in ('.', '..') for p in parts):
                result.hidden_files.append(rel_path)

            # Check executable
            ext = filepath.suffix.lower()
            if ext in EXECUTABLE_EXTENSIONS:
                result.executable_files.append(rel_path)

            # Scan text files
            if ext in TEXT_EXTENSIONS or filepath.stat().st_size < 100_000:
                scan_file(filepath, rel_path, result)

    result.compute_verdict()
    return result


def audit_zip(zip_path):
    """Extract and audit a zip file."""
    zip_path = Path(zip_path)
    tmpdir = tempfile.mkdtemp(prefix='skill_audit_')

    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmpdir)

        contents = os.listdir(tmpdir)
        if len(contents) == 1 and os.path.isdir(os.path.join(tmpdir, contents[0])):
            audit_root = os.path.join(tmpdir, contents[0])
        else:
            audit_root = tmpdir

        result = audit_directory(audit_root, zip_path.stem)
        return result
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <zip_file_or_directory> [...]')
        print('  Audits ClawdHub/OpenClaw skill packages for security red flags.')
        print(f'  Thresholds: SAFE < {THRESHOLD_REVIEW} | REVIEW {THRESHOLD_REVIEW}-{THRESHOLD_NOT_SAFE} | NOT SAFE >= {THRESHOLD_NOT_SAFE}')
        sys.exit(1)

    all_safe = True
    for target in sys.argv[1:]:
        target = Path(target)
        if not target.exists():
            print(f'❌ Not found: {target}')
            all_safe = False
            continue

        if target.is_file() and target.suffix == '.zip':
            result = audit_zip(target)
        elif target.is_dir():
            result = audit_directory(target)
        else:
            print(f'❌ Not a zip or directory: {target}')
            all_safe = False
            continue

        print(result.report())
        if not result.is_safe():
            all_safe = False

    # Exit code: 0 = all safe, 1 = at least one not safe
    sys.exit(0 if all_safe else 1)


if __name__ == '__main__':
    main()
