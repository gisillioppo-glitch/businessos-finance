# BusinessOS Lead Intake & Demo Request MVP v0.1

## Status

Lead Intake & Demo Request MVP v0.1 adds the public demo request flow to the BusinessOS landing website.

## Product intent

The landing page now moves from presentation-only to lead intake. Visitors can submit structured demo interest through a form surface that is ready to connect to an external form provider or future BusinessOS backend endpoint.

## What this block adds

- Request Demo anchors point to the form section.
- Public demo request form.
- Required fields for lead qualification.
- Consent checkbox.
- Honeypot anti-spam field.
- Client-side placeholder endpoint detection.
- Local MVP confirmation message.
- Documentation for activating real email delivery.

## Form fields

```text
name
email
organization
role
organization_size
primary_interest
message
consent
source
request_type
```

## Current email status

The form is implemented, but automatic email delivery requires one of these activation paths:

1. Formspree endpoint.
2. Tally or Typeform form embed/link.
3. Netlify Forms if hosted on Netlify.
4. Future BusinessOS backend endpoint.

Current placeholder endpoint:

```text
https://formspree.io/f/REPLACE_WITH_FORM_ID
```

Until the endpoint is replaced, the form shows a local MVP confirmation instead of sending email.

## Recommended activation path

For fastest public MVP activation:

1. Create a Formspree form.
2. Copy its endpoint URL.
3. Replace `REPLACE_WITH_FORM_ID` in `public/index.html`.
4. Push to GitHub.
5. Test from the public GitHub Pages URL.

## Security boundary

The lead form remains on the public/static surface and does not connect to:

```text
app/
finance.db
.env
.streamlit/secrets.toml
```

## Future backend version

A later backend-powered version should:

- Store leads in a database.
- Send confirmation email to requester.
- Send internal notification to BusinessOS owner.
- Write lead intake audit event.
- Create CRM/support follow-up record.
- Add rate limiting and abuse protection.
