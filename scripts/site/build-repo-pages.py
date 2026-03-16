#!/usr/bin/env python3
import csv, pathlib, html
from collections import defaultdict, Counter
base=pathlib.Path('wk')
per_repo_reason=defaultdict(Counter)
recent_prs=defaultdict(list)
for run_dir in sorted(base.glob('r*')):
    rm=run_dir/'remediated.csv'
    if not rm.exists(): continue
    with rm.open() as f:
        for row in csv.DictReader(f):
            repo=row.get('repo','').strip(); prs=row.get('pr_url','').strip(); ts=row.get('timestamp','').strip()
            reasons=(row.get('reasons') or '').strip()
            if not repo or not reasons: continue
            for r in [s.strip() for s in reasons.split(',') if s.strip()]:
                per_repo_reason[repo][r]+=1
            if prs:
                recent_prs[repo].append((ts, prs, reasons))
site=pathlib.Path('site/repos'); site.mkdir(parents=True, exist_ok=True)
rows=[]
for repo,cnts in per_repo_reason.items(): rows.append((repo, sum(cnts.values())))
rows.sort(key=lambda x:-x[1])
with (site/'index.html').open('w',encoding='utf-8') as out:
    out.write('<!doctype html><meta charset="utf-8"><title>Xcectua Repos</title>')
    out.write('<style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto;max-width:1120px;margin:24px auto}table{border-collapse:collapse;width:100%}th,td{border:1px solid #e5e7eb;padding:6px}</style>')
    out.write('<h1>Repos — Weekly Snapshot</h1><table><thead><tr><th>Repo</th><th>Total</th></tr></thead><tbody>')
    for repo,total in rows:
        out.write(f'<tr><td><a href="{html.escape(repo)}.html">{html.escape(repo)}</a></td><td>{total}</td></tr>')
    out.write('</tbody></table>')
for repo,cnts in per_repo_reason.items():
    with (site/f'{repo}.html').open('w',encoding='utf-8') as out:
        out.write('<!doctype html><meta charset="utf-8"><title>Repo: '+html.escape(repo)+'</title>')
        out.write('<style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto;max-width:1120px;margin:24px auto}table{border-collapse:collapse;width:100%}th,td{border:1px solid #e5e7eb;padding:6px}</style>')
        out.write(f'<h1>{html.escape(repo)}</h1>')
        out.write('<h2>Top reasons</h2><table><thead><tr><th>Reason</th><th>Count</th></tr></thead><tbody>')
        for reason,count in cnts.most_common(): out.write(f'<tr><td>{html.escape(reason)}</td><td>{count}</td></tr>')
        out.write('</tbody></table>')
        if recent_prs.get(repo):
            out.write('<h2>Recent PRs</h2><ul>')
            for ts,pr,rs in sorted(recent_prs[repo], reverse=True)[:10]:
                out.write(f'<li>{html.escape(ts)} — <a href="{html.escape(pr)}">PR</a> — {html.escape(rs)}</li>')
            out.write('</ul>')
print('repo pages written')
