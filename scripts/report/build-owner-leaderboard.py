#!/usr/bin/env python3
import os, json, csv, pathlib, re
owners = json.loads(os.getenv('SLO_OWNERS_JSON') or '{}')
roll = pathlib.Path('weekly_reason_rollup.csv')
slo = pathlib.Path('slo_report.md')
if not (roll.exists() and slo.exists()):
    pathlib.Path('weekly_owner_leaderboard.csv').write_text('owner,score,reasons\n', encoding='utf-8')
    pathlib.Path('weekly_owner_leaderboard.md').write_text('_No data._\n', encoding='utf-8')
    raise SystemExit(0)
reason_counts = {}
with roll.open() as f:
    for row in csv.DictReader(f):
        try: reason_counts[row['reason']] = int(row.get('total_count') or 0)
        except: pass
text = slo.read_text(encoding='utf-8')
fails = re.findall(r'^-\s+([^:]+):\s+\d+.*\*\*FAIL\*\*\s*$', text, re.M)
from collections import defaultdict
scores = defaultdict(int); reasons_map = defaultdict(list)
for r in fails:
    val = reason_counts.get(r, 0)
    for who in owners.get(r, []):
        scores[who] += val; reasons_map[who].append(r)
with open('weekly_owner_leaderboard.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=['owner','score','reasons']); w.writeheader()
    for who,score in sorted(scores.items(), key=lambda x:-x[1]):
        w.writerow({'owner':who,'score':score,'reasons':','.join(sorted(set(reasons_map[who])))})
lines = ['### Weekly Owner Leaderboard (by failed reason volume)']
if scores:
    for i,(who,score) in enumerate(sorted(scores.items(), key=lambda x:-x[1]),1):
        if i>10: break
        lines.append(f"{i}. {who}: **{score}**")
else:
    lines.append('_No SLO breaches detected._')
pathlib.Path('weekly_owner_leaderboard.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
