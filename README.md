# My Resume

Made from [This overleaf template](https://www.overleaf.com/latex/templates/awesome-source-cv/wrdjtkkytqcw) with some minor changes and additions

## Setup (macOS)

Install a TeX distribution that includes `latexmk` and `lualatex`:

```
brew install --cask mactex-no-gui
```

After install, open a new shell so `/Library/TeX/texbin` is on your `PATH`.

## Build the resume

`latexmk -lualatex cv.tex`

## Clear the latex temp files

`latexmk -c`

## Version info

```
❯ latexmk --version
Latexmk, John Collins, 9 March 2026. Version 4.88

❯ brew info --cask mactex-no-gui
mactex-no-gui: 2026.0324
```
