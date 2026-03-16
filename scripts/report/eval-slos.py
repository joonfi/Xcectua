#!/usr/bin/env python3
import os, json, csv, pathlib
from datetime import datetime, timezone
roll = pathlib.Path('weekly_reason_rollup.csv')
if not roll.exists():
    pathlib.Path('slo_report.md').write_text('_No SLO data (weekly_reason_rollup.csv missing)._\n', encoding='utf-8')
    raise SystemExit(0)
s = os.getenv('SLOS_JSON','').strip()
try: cfg = json.loads(s) if s else {}
except Exception: cfg = {}
reason_caps = (cfg.get('reason_caps') or {})
weekly_total_reason_max = int(cfg.get('weekly_total_reason_max') or 0)
counts = {}
with roll.open() as f:
    for row in csv.DictReader(f):
        counts[row['reason']] = int(row.get('total_count') or 0)

total_sum = sum(counts.values())
lines = []
lines.append(f"### SLO Report — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%SZ')}\n")
pass_all = True
if weekly_total_reason_max:
    ok = total_sum <= weekly_total_reason_max
    status = 'PASS' if ok else 'FAIL'
    if not ok: pass_all = False
    lines.append(f"- **Total reason volume**: {total_sum} (SLO ≤ {weekly_total_reason_max}) — **{status}**")
if reason_caps:
    lines.append('\n**Per‑reason SLOs**')
    for r, cap in reason_caps.items():
        cap = int(cap); val = counts.get(r, 0)
        ok = val <= cap
        status = 'PASS' if ok else 'FAIL'
        if not ok: pass_all = False
        lines.append(f"- {r}: {val} (SLO ≤ {cap}) — **{status}**")
if not reason_caps and not weekly_total_reason_max:
    lines.append('_No SLOs configured (set SLOS_JSON variable)._')
lines.append('\nOverall: **' + ('PASS' if pass_all else 'ATTENTION') + '**\n')
pathlib.Path('slo_report.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
