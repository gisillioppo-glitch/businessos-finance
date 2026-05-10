# BusinessOS Landing Website MVP v0.1

## Status

Landing Website MVP v0.1 is implemented as a public static product presentation page.

## Product intent

This block creates the first public-facing BusinessOS website without exposing the private dashboard, database, or backend logic.

## What this block adds

- Static public landing page.
- BusinessOS dark/red/white visual identity.
- Product hero section.
- Dashboard preview image asset.
- Module explanation for Finance, Operations, Governance, Support, and Command Center.
- Security positioning section.
- Request demo call to action.

## Files

```text
public/
  index.html
  styles.css
  assets/
    dashboard-preview.png
```

## Security boundary

The landing page is intentionally static:

- No connection to `finance.db`.
- No private dashboard logic.
- No internal module imports.
- No secret keys.
- No customer data.

## How to view locally

Open this file in a browser:

```text
public/index.html
```

## Recommended next work

- Replace placeholder contact email with real business contact.
- Add real product screenshots when ready.
- Add deployment target: GitHub Pages, Netlify, Vercel, or Cloudflare Pages.
- Add custom domain when brand is ready.
