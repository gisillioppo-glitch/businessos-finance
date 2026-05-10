# BusinessOS Security Foundation MVP v0.1

## Status

Security Foundation MVP v0.1 is open and implemented as the first protection layer for the local BusinessOS dashboard.

## What this block adds

- Local dashboard sign-in before accessing BusinessOS metrics.
- Basic role context for future role-based access control.
- Secret configuration through environment variables.
- `.env.example` template for local setup.
- `.env` and Streamlit secrets ignored by Git.
- Safer absolute database path resolution for the dashboard.

## Current local credentials

These credentials are only for local MVP validation:

- Username: `admin`
- Password: `businessos-local`

Before any external deployment, set a private password through `BUSINESSOS_ADMIN_PASSWORD` and do not commit secrets.

## Protected surfaces

- Streamlit dashboard entry point: `app/dashboard/main.py`
- Local database remains gitignored: `finance.db`
- Local secret files remain gitignored: `.env`, `.streamlit/secrets.toml`

## Remaining work before public deployment

- Replace local MVP password with managed secrets.
- Add real user table and password hashing.
- Add role permissions per module.
- Add dashboard access audit logging.
- Add HTTPS hosting and network restrictions.
- Add production deployment checklist.
