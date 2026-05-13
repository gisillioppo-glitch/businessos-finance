# BusinessOS Landing Publish MVP v0.1

## Status

Landing Publish MVP v0.1 prepares the BusinessOS public landing website for GitHub Pages deployment.

This block publishes only the static `public/` surface and keeps the private dashboard/backend out of the public website.

## Boundary Classification

- Primary boundary: Public AI boundary
- Secondary boundary: Static public deployment boundary
- Private data touched: no
- Public surface touched: yes
- Approval required: future
- Evidence generated: no
- Audit generated: no
- Reusable core candidate: partial
- Extraction timing: after public/private deployment boundary repeats in another vertical

## What this block adds

- GitHub Actions workflow for Pages deployment.
- Deployment validation before publishing.
- `.nojekyll` marker so GitHub Pages serves the static site directly.
- Documentation for the public/private boundary.

## Files

```text
.github/workflows/pages.yml
public/.nojekyll
docs/landing-publish-mvp-status.md
```

## Deployment workflow

The workflow runs when:

- `main` receives changes under `public/**`.
- `.github/workflows/pages.yml` changes.
- `scripts/deployment_check.py` changes.
- It is manually triggered from GitHub Actions.

The workflow does this:

1. Checks out the repository.
2. Runs `python scripts/deployment_check.py`.
3. Uploads only `public/` as the GitHub Pages artifact.
4. Deploys that artifact to GitHub Pages.

## Required GitHub setting

In GitHub:

```text
Repository -> Settings -> Pages -> Build and deployment -> Source -> GitHub Actions
```

After that, pushes to `main` can deploy the landing page.

## Expected public URL

For the current repository, the expected GitHub Pages URL should be similar to:

```text
https://gisillioppo-glitch.github.io/businessos-finance/
```

The exact URL will also appear in the workflow deployment output.

## Security boundary

This deployment intentionally publishes only:

```text
public/
```

It does not publish:

```text
app/
finance.db
.env
.streamlit/secrets.toml
reports/
data/
```

## Manual validation before push

Run locally:

```bash
python scripts/deployment_check.py
python scripts/smoke_test.py
```

Expected output:

```text
Deployment readiness check passed.
Smoke test completed successfully.
```

## Next recommended work

- Confirm GitHub Pages source is set to GitHub Actions.
- Push this block.
- Open the GitHub Actions run.
- Copy the deployed Pages URL.
- Replace placeholder contact email with a real address later.
