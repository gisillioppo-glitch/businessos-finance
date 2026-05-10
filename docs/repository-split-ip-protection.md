# BusinessOS Repository Split & IP Protection MVP v0.1

## Status

Repository Split & IP Protection MVP v0.1 separates the public BusinessOS landing website from the private BusinessOS product runtime.

## Public repository

```text
https://github.com/gisillioppo-glitch/businessos-landing
```

Purpose:

- Public landing website.
- Static HTML/CSS/JS only.
- Public brand and product presentation.
- Demo request form surface.
- GitHub Pages deployment for the public website.

Public repository contents:

```text
index.html
styles.css
lead-intake.js
assets/dashboard-preview.png
.github/workflows/pages.yml
README.md
.nojekyll
```

## Private repository

```text
https://github.com/gisillioppo-glitch/businessos-finance
```

Purpose:

- Private BusinessOS product runtime.
- Finance, Operations, Governance, Support, Command Center modules.
- Dashboard implementation.
- Security layer.
- Deployment and internal architecture docs.
- Future backend and lead intake automation.

Private repository contents include:

```text
app/
cli.py
main.py
scripts/
docs/
data/
reports/
```

## Protection decision

The private product repository should be converted to private after the public landing repository is confirmed live.

Recommended sequence:

1. Confirm `businessos-landing` exists and is public.
2. Enable GitHub Pages on `businessos-landing` using GitHub Actions.
3. Confirm public landing URL works.
4. Convert `businessos-finance` repository visibility to private.
5. Keep only public/brand assets in `businessos-landing`.

## Workflow change

The GitHub Pages workflow was removed from the private product repository after creating the public landing repository.

Reason:

- Prevent accidental public deployment from the private product repo.
- Make `businessos-landing` the canonical public website repo.
- Keep internal product code and architecture out of public Pages deployment.

## Security boundary

Public repo may contain:

```text
Static product presentation
Brand copy
Demo request form UI
Generated product preview image
```

Public repo must not contain:

```text
finance.db
.env
app/
scripts/
reports/
data/
.streamlit/
Internal architecture notes
Private credentials
Customer data
```

## Next action

After this block is committed and tagged:

1. Enable Pages in `businessos-landing`.
2. Confirm the public URL.
3. Change `businessos-finance` visibility to private.
