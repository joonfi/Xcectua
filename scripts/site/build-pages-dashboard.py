#!/usr/bin/env python3
import html, pathlib, csv
from collections import defaultdict

roll = pathlib.Path('weekly_reason_rollup.csv')
top = pathlib.Path('weekly_top_repos.csv')
leader = pathlib.Path('weekly_owner_leaderboard.md')
slo_md = pathlib.Path('slo_report.md')
sla_md = pathlib.Path('sla_status.md')

rows_roll=[]; rows_top=[]
if roll.exists():
    with roll.open() as f:
        rows_roll=list(csv.DictReader(f))
if top.exists():
    with top.open() as f:
        rows_top=list(csv.DictReader(f))

# Build trends from hist2 weekly_reason_rollup.csv files
hist_dir = pathlib.Path('hist2')
series = defaultdict(list)
if hist_dir.exists():
    for p in sorted(hist_dir.glob('r*/weekly_reason_rollup.csv')):
        data = {}
        with p.open() as f:
            for row in csv.DictReader(f):
                data[row['reason']] = int(row.get('total_count') or 0)
        for k,v in data.items(): series[k].append(v)
cur_data = {r['reason']: int(r.get('total_count') or 0) for r in rows_roll}
for k,v in cur_data.items(): series[k].append(v)

# Top 8 reasons
top_reasons = [k for k,_ in sorted(cur_data.items(), key=lambda x:-x[1])[:8]]

# Sparkline inline SVG
def spark(vals, w=240, h=48, pad=4, color="#2563eb"):
    if not vals: return ''
    m = min(vals); M = max(vals) or 1
    def sx(i):
        n = max(1,len(vals)-1)
        return pad + (w-2*pad)*(i/n)
    def sy(v):
        return h-pad - (h-2*pad)*((v-m)/(M-m if M>m else 1))
    d=[]
    for i,v in enumerate(vals):
        x,y=sx(i), sy(v)
        d.append(("M" if i==0 else "L")+f"{x:.1f},{y:.1f}")
    return f'<svg width="{w}" height="{h}"><path d="{' '.join(d)}" fill="none" stroke="{color}" stroke-width="2"/></svg>'

parts=[]
parts.append('<!doctype html><meta charset="utf-8"><title>Xcectua Weekly Dashboard</title>')
parts.append('<style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto;max-width:1160px;margin:24px auto;color:#111}h1{margin:0 0 8px}small{color:#666}table{border-collapse:collapse;width:100%;margin:12px 0}th,td{border:1px solid #e5e7eb;padding:6px;text-align:left;font-size:14px}th{background:#f3f4f6}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}</style>')
parts.append('<h1>Xcectua Weekly Dashboard</h1>')
parts.append('<small>Static snapshot generated from weekly CSVs</small>')

# Tabs
parts.append('<p><a href="#overview">Overview</a> • <a href="#trends">Trends</a> • <a href="#owners">Owners</a> • <a href="#sla">SLA</a></p>')

# Overview
parts.append('<h2 id="overview">Overview</h2>')
if rows_roll:
    parts.append('<table><thead><tr><th>Reason</th><th>Total</th></tr></thead><tbody>')
    for r in rows_roll:
        parts.append(f"<tr><td>{html.escape(r.get('reason',''))}</td><td>{html.escape(r.get('total_count',''))}</td></tr>")
    parts.append('</tbody></table>')
else:
    parts.append('<p><em>No rollup data.</em></p>')

# Heatmap embed
if pathlib.Path('site/heatmap.svg').exists():
    parts.append('<h3>Heatmap — Reasons × Repos</h3>')
    parts.append('<img src="heatmap.svg" alt="heatmap" style="max-width:100%;height:auto;border:1px solid #e5e7eb;"/>')

# Trends
parts.append('<h2 id="trends">Trends (last ~12 runs)</h2>')
if top_reasons:
    parts.append('<div class="grid">')
    colors=["#2563eb","#dc2626","#059669","#7c3aed","#f59e0b","#0ea5e9","#be185d","#1f2937"]
    for i,r in enumerate(top_reasons):
        vals = series.get(r, [])
        parts.append(f'<div><strong>{html.escape(r)}</strong><br/>{spark(vals, color=colors[i%len(colors)])}</div>')
    parts.append('</div>')
else:
    parts.append('<p><em>No trend data available.</em></p>')

# Owners
parts.append('<h2 id="owners">Owner Leaderboard</h2>')
if leader.exists():
    parts.append('<div style="border:1px solid #e5e7eb;padding:12px;border-radius:8px;background:#fafafa">')
    parts.append(leader.read_text(encoding='utf-8'))
    parts.append('</div>')
else:
    parts.append('<p><em>No owner leaderboard.</em></p>')

# SLA
parts.append('<h2 id="sla">SLA Status</h2>')
parts.append(sla_md.read_text(encoding='utf-8') if sla_md.exists() else '<p><em>No SLA data.</em></p>')

pathlib.Path('site/index.html').write_text('\n'.join(parts), encoding='utf-8')
print('site/index.html written')
