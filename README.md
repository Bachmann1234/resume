# My Résumé

Single source of truth: [`resume.yaml`](resume.yaml). Everything else is
generated from it.

```
resume.yaml ──(templates/ + build.py)──┬──> build/cv.pdf      (LaTeX résumé)
                                        └──> build/resume.json (feeds mattbachmann.dev)
```

Edit `resume.yaml`, run the build, and **both** the PDF and the website content
update — no second copy to maintain. The LaTeX layout comes from
[this Overleaf template](https://www.overleaf.com/latex/templates/awesome-source-cv/wrdjtkkytqcw)
with minor changes; `templates/*.tex.j2` render it from the YAML.

## Setup (macOS)

Install a TeX distribution that includes `latexmk` and `lualatex`:

```
brew install --cask mactex-no-gui
```

Open a new shell so `/Library/TeX/texbin` is on your `PATH`, then set up Python:

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Build

```
.venv/bin/python build.py          # render LaTeX, build PDF, emit resume.json
.venv/bin/python build.py --no-pdf # skip LaTeX (no TeX install needed)
```

Outputs land in `build/` (git-ignored). Clean with `rm -rf build`.

## Editing content

Edit `resume.yaml`. Highlights:

- `experience[].group_with_previous: true` stacks a role under the company above
  it without a separator (e.g. the three Fitbit roles).
- `experience[].note` is the small parenthetical after a company name.
- Content is plain text — the templates handle LaTeX escaping and the JSON stays
  clean for the website.

To change the PDF's *visual* style, edit `templates/*.tex.j2` or
`yaac-another-awesome-cv.cls`.

## CI

`.github/workflows/build.yml` rebuilds on every push to `main` and publishes
`cv.pdf` + `resume.json` to a rolling `latest` release. The
[mattbachmann.dev portfolio](https://github.com/Bachmann1234/Portfolio) fetches
them from there at deploy time:

```
https://github.com/Bachmann1234/resume/releases/download/latest/cv.pdf
https://github.com/Bachmann1234/resume/releases/download/latest/resume.json
```

## Version info

```
❯ latexmk --version
Latexmk, John Collins, 9 March 2026. Version 4.88

❯ brew info --cask mactex-no-gui
mactex-no-gui: 2026.0324
```
