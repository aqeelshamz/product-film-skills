# Realism: what makes a film read as a real product

Owners rejected every minimal mockup with words like "vibe coded", "minimal", "too simple" and "what are
these icons?". Viewers judge the product by the detail in its film. Build every screen as if it would be paused
and inspected.

## Desktops

- **Wallpaper:** a real, licensed photo or the OS's own default (macOS, Windows 11 Bloom). Never a flat gradient.
  Credit it in `assets/CREDITS.md`.
- **macOS:** menu bar with Apple menu, the frontmost app's real menus, status icons, the date/time in the real format;
  Dock with real app icons, magnification off, running dots; windows with traffic lights and the app's real title bar.
- **Windows 11:** centred taskbar, real Start/search/task view icons, system tray clock (two lines), Mica-ish window
  chrome; Segoe UI Variable sizing.
- **Only apps that exist on that OS.** Stripe, Shopify and many SaaS tools have no Mac app: show them in a browser
  window instead. Check every icon you place.
- **Real app icons:** from the vendor's site or press kit, at the size the OS shows them.

## Phones (Android shown here; iOS the same idea)

- "phone is not a desktop": use the platform's real home-screen grid. Pixel: 4 columns (5 on some), status bar
  with time and real icons, At a Glance at top, Google search bar and dock at the bottom, widgets in grid cells with
  gutters, no overlap.
- Widget sizes follow the launcher's cell sizes in dp, scaled to the phone's screen. A desktop widget is NOT a phone
  widget: redraw it at phone size, ideally with the product's own phone renderer (snapshot it, waiting for images).
- Real launcher icons for real apps; real wallpaper.

## Product UI (the thing you're selling)

- Richer than you'd think: titles, units, deltas, small charts, secondary labels, timestamps, states. A widget with a
  number and an icon reads as a toy.
- Real brand marks (from the brand's own site: SVG or the favicon they serve) instead of icon-font look-alikes.
  If the product can't render a brand mark yet and the owner wants it, that's a product change: build it, log it.
- Plausible, specific data: "₹48,210 today, +12 % vs last Tue", "PR #482 · 2 approvals", "Exam in 12 days".
  Never lorem ipsum or 1,234.
- Only what the product can really do today. If it can't, don't show it.
- Use the product's real fonts, radii, colours and component styles (read its CSS/tokens).

## Third-party apps (dashboards, AI clients)

- Recreate the real screen at real density: real nav, real table columns, real chart styles, real empty spaces.
  Screenshot the real app for reference first (in the browser), then rebuild in HTML.
- Show the AI client the product actually works with (only ones that were tested), with its real window, real
  input box and real message style.

## Characters / mascots

- Reuse the brand's existing characters (check the site). New ones match the style exactly.
- Make sprite sheets in ChatGPT (via the owner's Chrome): 12 frames in a 4×3 grid on plain white, one character per
  chat. If it returns a painted checkerboard or black background, start a fresh chat. Cut the grid evenly, trim the
  halo, save WebP. 6 frames looks stiff; 12 animates.
- Enough of them: 8+ personas when the point is range.

## Brands and legal

- While any third-party mark is on screen, show: "Product names and logos belong to their owners. They are shown
  only to identify the services <product> works with, and do not imply endorsement." at ≥ 21 px, readable.
- Check every shot with a logo has the line (it was missing on one shot once).
- Never put a brand's logo on a character or imply a partnership.
