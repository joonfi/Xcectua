#!/usr/bin/env python3
import os, json, csv, pathlib, re
from datetime import datetime, timezone, timedelta

s_sla = os.getenv('SLA_DAYS_JSON','').strip()
try: SLA = json.loads(s_sla) if s_sla else {}
except Exception: SLA = {}

# Collect FAIL reasons across history to find first FAIL date
entries = []
for p in sorted(pathlib.Path('hist').glob('r*/')):
    slo = p/'slo_report.md'; meta = p/'run.json'
    if not slo.exists() or not meta.exists():
        continue
    try:
        meta_ts = json.loads(meta.read_text()).get('updatedAt')
    except Exception:
        meta_ts = None
    text = slo.read_text(encoding='utf-8')
    for m in re.finditer(r'^-\s+([^:]+):\s+\d+.*\*\*FAIL\*\*\s*$', text, re.M):
        reason = m.group(1).strip()
        entries.append((reason, meta_ts))
# earliest FAIL date per reason
first_fail = {}
for r, ts in entries:
    if not ts: continue
    first_fail.setdefault(r, ts)
    if ts < first_fail[r]: first_fail[r] = ts

# build SLA table for reasons that are currently FAIL
fail_now = set()
cur_slo = pathlib.Path('slo_report.md')
if cur_slo.exists():
    txt = cur_slo.read_text(encoding='utf-8')
    for m in re.finditer(r'^-\s+([^:]+):\s+\d+.*\*\*FAIL\*\*\s*$', txt, re.M): fail_now.add(m.group(1).strip())

rows = []
now = datetime.now(timezone.utc)
for r in sorted(fail_now):
    opened = first_fail.get(r)
    if opened:
        try: opened_dt = datetime.fromisoformat(opened.replace('Z','+00:00'))
        except Exception: opened_dt = now
    else:
        opened_dt = now
    days_open = (now - opened_dt).days
    sla_days = int(SLA.get(r, 7))
    due_dt = opened_dt + timedelta(days=sla_days)
    status = 'on_track'
    if now >= due_dt: status = 'overdue'
    elif (due_dt - now).days <= 2: status = 'at_risk'
    rows.append({
        'reason': r,
        'first_fail_date': opened_dt.strftime('%Y-%m-%d'),
        'days_open': str(days_open),
        'sla_days': str(sla_days),
        'due_date': due_dt.strftime('%Y-%m-%d'),
        'status': status
    })

with open('sla_status.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=['reason','first_fail_date','days_open','sla_days','due_date','status'])
    w.writeheader(); [w.writerow(r) for r in rows]

lines = ['### SLA Status (breached reasons)']
if rows:
    for r in rows:
        lines.append(f"- {r['reason']}: open {r['days_open']}d, due {r['due_date']} — **{r['status']}**")
else:
    lines.append('_No active breaches._')
pathlib.Path('sla_status.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
