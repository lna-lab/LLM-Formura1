# Deploying the LLM Formula site (Xserver / any static host)

The site is **fully static** — generated HTML from `results/**/*.json`. No backend,
no database, no Node/PHP runtime needed. It deploys to Xserver (or any web host)
by copying files into the public web root.

## 1. Build
```bash
python3 tools/build_site.py        # -> site/index.html
```
Re-run after every merged result to refresh the leaderboard.

## 2. Upload to Xserver (SFTP)
Xserver serves static files from `~/<your-domain>/public_html/`. Upload the `site/`
contents there. With the `lftp` mirror (or any SFTP client / Xserver File Manager):

```bash
# one-time: set your values
HOST=svNNNN.xserver.jp        # your Xserver host
USER=your-xserver-id
DOMAIN=llmformula.example     # your domain
REMOTE="/home/$USER/$DOMAIN/public_html"

lftp -u "$USER" sftp://$HOST -e "
  mirror -R --delete --verbose site/ $REMOTE ;
  bye"
```
(or `rsync -avz --delete site/ $USER@$HOST:$REMOTE/` if SSH is enabled on your plan.)

The page is `index.html`, so `https://<your-domain>/` serves the leaderboard directly.

## 3. (optional) one-button refresh script
```bash
#!/usr/bin/env bash
set -euo pipefail
python3 tools/build_site.py
lftp -u "$XS_USER" sftp://"$XS_HOST" -e "mirror -R --delete site/ $XS_REMOTE; bye"
echo "deployed $(date)"
```
Put your credentials in env vars (never commit them). On Xserver you can also run this
from a **cron job** (Server Panel → Cron) to auto-rebuild+publish on a schedule.

## Notes
- The markdown docs (REGULATIONS, MEASUREMENT, ENTRY, PARTNERS) are linked from the
  page to their GitHub source — no rendering step needed. If you want them served on
  your domain too, drop a markdown-to-HTML step into `build_site.py` later.
- Static hosting means the leaderboard is tamper-evident: every figure traces to a
  committed JSON manifest in `results/` on GitHub. Submissions come in by PR (or a
  web form that opens a PR), keeping the chain auditable — exactly the integrity the
  series sells.
