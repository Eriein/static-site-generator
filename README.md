# Static Site Generator

A custom static site generator built from scratch in Python. Converts Markdown content into a fully linked HTML site, with support for deploying to GitHub Pages under a custom basepath.

## How it works

1. Markdown files in `content/` are parsed into an HTML node tree
2. Each node tree is rendered into HTML and injected into `template.html`
3. Static assets from `src/static/` are copied to the output directory
4. Root-relative links (`href="/`, `src="/`) are rewritten to include the basepath

The output is written to `docs/`, which GitHub Pages serves directly.

## Project structure

```
content/        # Markdown source files (mirrors output structure)
src/
  main.py       # Entry point and page generation pipeline
  converter.py  # Markdown → HTML node tree
  htmlnode.py   # Base HTML node
  leafnode.py   # Leaf (no children) HTML node
  parentnode.py # Parent (with children) HTML node
  textnode.py   # Inline text node types
  copystatic.py # Copies static assets to output
  utils.py      # Helpers (e.g. extract_title)
src/static/     # CSS, images, and other static assets
template.html   # HTML shell — {{ Title }} and {{ Content }} are replaced per page
docs/           # Generated output (served by GitHub Pages)
```

## Usage

**Build for GitHub Pages:**
```bash
bash build.sh
```
Generates `docs/` with basepath `/static-site-generator/`.

**Run locally:**
```bash
bash main.sh
```
Generates `docs/` without a basepath and serves it at `http://localhost:8888`.

**Run tests:**
```bash
bash test.sh
```

## Adding content

Create a Markdown file anywhere under `content/`. The directory structure maps directly to the output URL structure.

```
content/blog/my-post/index.md  →  /blog/my-post/index.html
```

The first `# Heading` in each file becomes the page `<title>`.

## Deploying

1. Run `bash build.sh` to regenerate `docs/`
2. Commit and push — GitHub Pages picks up changes from `docs/` on `main` automatically
