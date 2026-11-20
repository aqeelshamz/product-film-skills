// The product's UI and the world around it, as HTML strings in screen px (window.MOCK). film.js composes these.
// Build each piece from the REAL thing, never from memory: the product's own renderer or components where possible,
// real OS chrome (menu bar, Dock/taskbar, home screen) with real app icons, real dashboards with real logos.
// Put one screen at a time in screens.html and compare it side by side with a screenshot of the real one.
window.MOCK = {};
