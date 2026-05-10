# BusinessOS Deployment Readiness MVP v0.1

## Status

Deployment Readiness MVP v0.1 defines the safe publication boundary for BusinessOS.

This block does not deploy the product yet. It prepares the rules, checklist, and validation commands required before publishing any part of the system externally.

## Deployment principle

BusinessOS has two different surfaces:

1. Public presentation surface.
2. Private operating system surface.

These must not be mixed.

## Public surface

The following can be published publicly:

```text
public/
  index.html
  styles.css
  assets/
    dashboard-preview.png
```

Public surface rules:

- Static only.
- No database connection.
- No private Python imports.
- No `.env` files.
- No local SQLite database.
- No customer or institutional data.
- No internal credentials.

Recommended first hosting targets:

- GitHub Pages.
- Netlify.
- Vercel static hosting.
- Cloudflare Pages.

## Private surface

The following must remain private:

```text
app/
cli.py
main.py
scripts/
finance.db
.env
.streamlit/secrets.toml
reports/
data/
```

Private surface rules:

- Do not expose directly to the public internet.
- Run dashboard only behind authentication.
- Replace local MVP password before external access.
- Do not commit local databases or secret files.
- Use HTTPS for any remote dashboard deployment.
- Add audit logging before real users are introduced.

## Current safe status

Current safe status for MVP:

- Landing website can be treated as public/static.
- Dashboard is local/private and protected by MVP login.
- `.env` is ignored by Git.
- `.streamlit/secrets.toml` is ignored by Git.
- `finance.db` is ignored by Git.

## Required checks before publishing landing

Run:

```bash
python scripts/deployment_check.py
python scripts/smoke_test.py
```

Expected result:

```text
Deployment readiness check passed.
Smoke test completed successfully.
```

## Required checks before publishing dashboard

Do not publish dashboard externally until all of these are true:

- `BUSINESSOS_ADMIN_PASSWORD` is set privately outside Git.
- Local default password is disabled or replaced.
- Deployment uses HTTPS.
- Dashboard is not served from an open unauthenticated URL.
- Access logs are enabled.
- Login events are written to audit logs.
- Role permissions are enforced by module.
- Database is backed up securely.
- Production data is not committed to Git.

## Deployment sequence

Recommended order:

1. Publish static landing website.
2. Keep dashboard local/private.
3. Add stronger authentication and audit logging.
4. Deploy private dashboard to protected hosting.
5. Add custom domain and HTTPS.
6. Add real user and tenant model.

## Next recommended block

After this readiness block, the safest next blocks are:

1. Publish Landing Website MVP v0.1 to GitHub Pages or another static host.
2. Security v0.2: password hashing, login audit logs, and real user table.
3. Dashboard Reports Download v0.3: export command center reports from the private dashboard.
