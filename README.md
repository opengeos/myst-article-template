# MyST Article Template

A reusable template for writing single-page articles with [MyST Markdown](https://mystmd.org/), built as an interactive HTML site on GitHub Pages and as a publication-ready PDF via a customized Typst template.

## Features

- **Single-file article** authored in MyST Markdown with Jupyter code-cell support, figures, citations, and a bibliography
- **`article-theme`** HTML layout for the published website
- **Customized `lapreprint-typst`** template vendored locally under `templates/` for full control over the PDF output
- **Publication-ready PDF styling**: 1-inch margins, three-line tables in the booktabs style of peer-reviewed journals, shaded code blocks, `1.1.1` heading numbering, figure and table captions ending in a period, and no left-margin gutter or running headers
- **PDF export driven by a Python script** (`build_pdf.py`) that wraps `myst build --pdf`
- **GitHub Pages** deployment on every push to `main`: the HTML site is built with MyST, the PDF is generated, and the PDF is copied alongside the HTML so it is reachable at a stable URL on the deployed site
- **Pre-commit hooks**: Black, codespell, nbstripout

## Quick Start

1. Click **Use this template** on GitHub to create a new repository
2. Update [myst.yml](myst.yml) with your article title and GitHub `owner/repo`
3. Edit the frontmatter and content of [article.md](article.md) (title, authors, abstract, keywords, body)
4. Edit [references.bib](references.bib) with the sources you actually cite
5. Push to `main` to trigger the HTML and PDF builds

## Project Structure

```
.
├── myst.yml                    # MyST configuration (article-theme)
├── article.md                  # The article (single source of truth)
├── references.bib              # Bibliography
├── build_pdf.py                # Python wrapper around `myst build --pdf`
├── requirements.txt            # Python dependencies for code cells
├── templates/
│   └── lapreprint-typst/       # Vendored + customized Typst PDF template
│       ├── template.typ
│       ├── lapreprint.typ
│       ├── frontmatter.typ
│       ├── template.yml
│       └── LICENSE
├── images/                     # Article figures
│   └── sample_figure.png
├── logo.png                    # Site logo
├── fav.ico                     # Favicon
├── custom.css                  # Site styling overrides
├── CNAME                       # Custom domain (optional)
├── robots.txt                  # Search engine directives
├── .pre-commit-config.yaml     # Pre-commit hook configuration
├── CONTRIBUTING.md             # Contribution guidelines
├── CONDUCT.md                  # Code of conduct
└── .github/workflows/
    ├── build.yml               # PR checks: HTML + PDF artifact
    └── deploy.yml              # Production deploy to GitHub Pages
```

## Customization

### Article metadata

Edit the YAML frontmatter at the top of [article.md](article.md):

- `title`, `short_title`
- `authors`: name, affiliations, email
- `abstract`, `keywords`
- `exports`: points at the local `./templates/lapreprint-typst` and writes to `article.pdf` in the repo root

### Bibliography

Replace the example entries in [references.bib](references.bib) with your own. Cite them from `article.md` using MyST's `[@key]` (parenthetical) and `@key` (textual) syntax. MyST auto-generates a References section with only the entries you cite.

### Site metadata

Edit [myst.yml](myst.yml):

- `project.title`, `project.github` (your `owner/repo`)
- `project.bibliography`
- `site.template` (kept as `article-theme`)

### PDF template

The PDF styling is controlled entirely by the files under [templates/lapreprint-typst/](templates/lapreprint-typst/). The vendored copy has been modified from the upstream `lapreprint-typst` to better suit a traditional journal layout. Edit [templates/lapreprint-typst/lapreprint.typ](templates/lapreprint-typst/lapreprint.typ) and [templates/lapreprint-typst/template.typ](templates/lapreprint-typst/template.typ) directly to tweak margins, fonts, table styling, or any other typography. Changes persist across `_build/` wipes because the template lives in the source tree rather than being downloaded on each build.

## Building Locally

Install the toolchain:

```bash
pip install -r requirements.txt
npm install -g mystmd
# Install the Typst CLI from https://github.com/typst/typst
```

Build the HTML site:

```bash
myst build --html
# output: _build/html/
```

Build the PDF:

```bash
python build_pdf.py
# output: ./article.pdf
```

The script wraps `myst build --pdf`, checks that `myst` and `typst` are on `PATH`, and verifies that `./article.pdf` was produced.

Preview the site with a live dev server:

```bash
myst start
```

## Deployment

Pushes to `main` trigger [deploy.yml](.github/workflows/deploy.yml), which:

1. Installs `mystmd` (via npm), Python, and `typst`
2. Builds the PDF via `python build_pdf.py` (writes `./article.pdf`)
3. Builds the HTML site with `myst build --html` (uses `BASE_URL=/<repo-name>` so asset paths work under `username.github.io/<repo-name>/`)
4. Copies `article.pdf` into `_build/html/article.pdf` so it ships alongside the site
5. Deploys `_build/html/` to GitHub Pages

The PDF is published at a stable URL next to the HTML site, for example:

```
https://opengeos.org/myst-article-template/article.pdf
```

Link to that URL from anywhere you reference the article (the landing page, README, external posts, etc.). If you configure a custom domain via [CNAME](CNAME), remove the `BASE_URL` environment variable from [deploy.yml](.github/workflows/deploy.yml).

### Pull request builds

Pull requests trigger [build.yml](.github/workflows/build.yml), which builds the HTML site and the PDF, then uploads the PDF as an `article-pdf` workflow artifact for download from the run summary.

## License

[MIT](LICENSE)
