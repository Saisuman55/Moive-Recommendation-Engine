# Design Doc — Movie Recommendation Engine (UI)

## Inspiration direction

- Clean academic / product-demo aesthetic: readable type, plenty of whitespace, subtle borders (similar to modern dashboard UIs — Linear-style clarity without copying assets).

## Design language

### Colors

- Background: `#f8fafc` (page), `#ffffff` (cards).
- Text: `#0f172a` primary, `#475569` / `#64748b` secondary.
- Accents: `#2563eb` links; info banners `#eff6ff` on `#bfdbfe` border.

### Layout

- Single column, max width ~880px, centered.
- Sections as cards: 12px radius, 1px border `#e2e8f0`, comfortable padding.

### Typography

- System UI stack: `system-ui`, `-apple-system`, `Segoe UI`, `Roboto`, sans-serif.
- Page title ~1.5rem; section titles ~1.1rem; helper text 13–14px.

### Components

- Forms: stacked labels, full-width inputs (capped ~360px on auth).
- Movie list: each row = title/year/genres + numeric rating + Save.
- Primary actions: native buttons; disabled state while async requests run.
- Status: single message strip below content for errors and confirmations.

### Accessibility

- Sufficient contrast for body text on white/slate backgrounds.
- Interactive elements are real `<button>` elements where possible.

## Screens (v1)

1. **Guest** — email, password, Register, Log in.
2. **Signed in** — header with email + Log out + Refresh recommendations + Train model.
3. **Movies** — list with rating input and Save.
4. **Recommendations** — ordered list with predicted score.

## Future polish

- Toasts instead of inline message; skeleton loaders; keyboard focus styles; dark mode tokens.
