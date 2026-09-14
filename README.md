# José E. Rodríguez-Ríos portfolio

Static portfolio for GitHub Pages. Content is based on the September 2026 CV, general résumé, and Sandia résumé supplied by José. The general résumé and full CV are the public downloads.

## Preview

From this directory, run `python -m http.server 8765` and visit http://localhost:8765.

## Publish

Use a public repository named `joserico00.github.io`. Upload the contents of this directory to the root of its `main` branch. In **Settings → Pages**, select **Deploy from a branch**, then **main** and **/(root)**. No build dependencies are needed.

Intended address: https://joserico00.github.io/

## Update

- Edit `index.html` for homepage content.
- Edit `styles.css` for site-wide appearance and responsive layouts.
- Edit the HTML files in `projects/` for case studies. A source generator is retained in the parent workspace at `tools/build_portfolio.py`.
- Replace files in `downloads/` and update links if filenames change.
- Preserve experiment context and distinguish personal contributions from student-team results.

The site uses semantic HTML and CSS with no application JavaScript, analytics, or build pipeline. Fonts load from Google Fonts with system-font fallbacks.
