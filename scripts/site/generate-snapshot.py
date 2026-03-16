#!/usr/bin/env python3
import os, json, hashlib, pathlib, hmac
from datetime import datetime, timezone
files = ['weekly_reason_rollup.csv','weekly_top_repos.csv','weekly_owner_leaderboard.csv','slo_report.md','sla_status.csv','site/index.html','site/heatmap.png','site/heatmap.svg']
manifest={'generated_at_utc': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),'files':{}}
for p in files:
  fp=pathlib.Path(p)
  if fp.exists(): manifest['files'][p]=hashlib.sha256(fp.read_bytes()).hexdigest()
pathlib.Path('site').mkdir(parents=True, exist_ok=True)
(pathlib.Path('site/snapshot.manifest.json')).write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n', encoding='utf-8')
secret=os.getenv('SNAPSHOT_SIGNING_SECRET','').encode('utf-8') if os.getenv('SNAPSHOT_SIGNING_SECRET') else None
if secret:
  payload=json.dumps(manifest, separators=(',',':')).encode('utf-8')
  sig=hmac.new(secret,payload,hashlib.sha256).hexdigest()
  pathlib.Path('site/snapshot.signature').write_text(sig+'\n', encoding='utf-8')
else:
  pathlib.Path('site/snapshot.signature').write_text(''+'\n', encoding='utf-8')
print('snapshot manifest/signature written')
