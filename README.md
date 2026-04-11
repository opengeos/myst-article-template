# MyST Article Template

A reusable template for writing single-page articles with [MyST Markdown](https://mystmd.org/), built as HTML and PDF via GitHub Actions.

## Features

- **MyST Markdown** source format with Jupyter code-cell support
- **`article-theme`** single-page layout
- **PDF export** via the `lapreprint-typst` template, driven by a Python script
- **GitHub Pages** deployment on push to `main` (HTML + downloadable PDF)
- **Pre-commit hooks**: Black, codespell, nbstripout for code quality

## Quick Start

1. Click **Use this template** on GitHub to create a new repository
2. Update `myst.yml` with your article title and GitHub `owner/repo`
3. Edit the frontmatter and content of `article.md` (title, authors, abstract, keywords, body)
4. Push to GitHub to trigger automated HTML and PDF builds

## Project Structure

```
.
├── myst.yml                    # MyST configuration (article-theme)
├── article.md                  # The article (single source of truth)
├── references.bib              # Bibliography
├── build_pdf.py                # Python script that builds the PDF
├── requirements.txt            # Python dependencies
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
    ├── build.yml               # PR build: HTML + PDF artifact
    └── deploy.yml              # Production deploy to GitHub Pages
```

## Customization

### Article Metadata

Edit the frontmatter at the top of `article.md`:

- `title`, `subtitle`, `short_title`
- `authors`: name, affiliations, email
- `abstract`, `keywords`
- `exports`: PDF template and output path

### Site Metadata

Edit `myst.yml`:

- `project.title`: matches the article title
- `project.github`: your GitHub `owner/repo`
- `project.bibliography`: bibliography files
- `site.template`: kept as `article-theme`

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
# output: _build/exports/article.pdf
```

The script wraps `myst build --pdf`, checks that `myst` and `typst` are on `PATH`, and verifies the expected output file was produced.

## Deployment

### GitHub Pages (production)

Pushes to `main` trigger the `deploy.yml` workflow, which:

1. Installs `mystmd` (via npm) and `typst`
2. Builds the HTML site (`myst build --html`)
3. Builds the PDF (`python build_pdf.py`)
4. Copies `article.pdf` into the HTML output so it's downloadable from the published site
5. Deploys to GitHub Pages

By default, `BASE_URL` is set to `/<repo-name>` so asset paths work when served at `username.github.io/repo-name/`. If you configure a custom domain (via `CNAME`), remove the `BASE_URL` environment variable from `deploy.yml`.

### Pull request builds

Pull requests trigger the `build.yml` workflow, which builds the HTML site and the PDF, then uploads the PDF as an `article-pdf` workflow artifact for download from the run summary.

## License

[MIT](LICENSE)
