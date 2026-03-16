#!/usr/bin/env python3
import csv, pathlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

site = pathlib.Path('site'); site.mkdir(parents=True, exist_ok=True)
fn = pathlib.Path('weekly_top_repos.csv')
if not fn.exists():
    print('weekly_top_repos.csv missing; skip heatmap export'); raise SystemExit(0)
reason_set=set(); repo_set=set(); counts=defaultdict(lambda: defaultdict(int))
with fn.open() as f:
    for row in csv.DictReader(f):
        r=row.get('reason',''); repo=row.get('repo',''); c=int(row.get('count','0') or 0)
        reason_set.add(r); repo_set.add(repo); counts[r][repo]=c
reasons=sorted(reason_set)
repos=sorted(repo_set, key=lambda k: -sum(counts[r].get(k,0) for r in reasons))[:25]
if not reasons or not repos:
    print('no data for heatmap'); raise SystemExit(0)
M=np.array([[counts[r].get(repo,0) for repo in repos] for r in reasons])
fig, ax = plt.subplots(figsize=(max(6, 0.35*len(repos)), max(4, 0.35*len(reasons))))
im=ax.imshow(M, cmap='Blues', aspect='auto')
ax.set_xticks(range(len(repos))); ax.set_xticklabels(repos, rotation=45, ha='right', fontsize=8)
ax.set_yticks(range(len(reasons))); ax.set_yticklabels(reasons, fontsize=8)
ax.set_title('Weekly Heatmap — Reasons × Repos')
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
fig.tight_layout(); fig.savefig(site/'heatmap.png', dpi=180); fig.savefig(site/'heatmap.svg')
print('heatmap exported')
