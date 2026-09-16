# José E. Rodríguez-Ríos portfolio

Static portfolio for GitHub Pages, with four featured projects, an 18-project collection filtered by seven themes, and separate experience, awards, and workshops pages. The general Resume and full CV are the public downloads.

## Preview

From this directory, run `python -m http.server 8765` and visit http://localhost:8765.

## Publish

The public repository is `joserico00/joserico00.github.io`. Push to `main`; GitHub Pages deploys from **main / (root)**. No build dependencies are needed to serve the site.

Live address: https://joserico00.github.io/

## Update

- Edit `data/projects.json` for project titles, descriptions, themes, GitHub links, and case studies.
- Edit `templates/home.template` for the homepage's main introduction and featured layout.
- Edit `tools/build_site.py` for shared navigation and the experience, awards, and workshops content.
- Run `python tools/build_site.py` to regenerate the static HTML. Commit both the source and generated pages.
- Edit `styles.css` for site-wide appearance and responsive layouts.
- Edit `site.js` for progressive enhancement of theme filters and mobile navigation. Content remains readable without JavaScript.
- Replace the PDFs in `downloads/` to update the public Resume and CV; stable filenames preserve existing links.
- Preserve experiment context and distinguish personal contributions from student-team results.

The site uses semantic HTML, CSS, and a small dependency-free script, with no analytics or backend. Theme URLs are shareable (`projects.html?theme=security`) and support browser back/forward navigation. Fonts load from Google Fonts with system-font fallbacks.

## Content provenance

The September 15 expansion uses José's supplied project descriptions, his Resume/CV, relevant career and bootcamp discussion, and the public repository READMEs verified during the update. It distinguishes bootcamp-provided material from personal contributions, historical ML experiments from the current evaluation pipeline, and the 4.8 MW fusion allocation from the 12 MW facility budget. LLNL work is described as internship experience without an invented source-code link.
