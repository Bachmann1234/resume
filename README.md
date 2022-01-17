# My Resume

Made from [This overleaf template](https://www.overleaf.com/latex/templates/awesome-source-cv/wrdjtkkytqcw) with some minor changes and additions

## Build the resume

`latexmk -lualatex cv.tex`

## Clear the latex temp files

`latexmk -c`

## Version info

```
❯ latexmk --version

Latexmk, John Collins, 29 September 2020. Version 4.70b

❯ brew info mactex
mactex: 2021.0328
https://www.tug.org/mactex/
/usr/local/Caskroom/mactex/2021.0328 (4.4GB)
From: https://github.com/Homebrew/homebrew-cask/blob/HEAD/Casks/mactex.rb
==> Name
MacTeX
==> Description
Full TeX Live distribution with GUI applications
==> Artifacts
mactex-20210328.pkg (Pkg)
==> Caveats
You must restart your terminal window for the installation of MacTex CLI tools to take effect.
Alternatively, Bash and Zsh users can run the command:

  eval "$(/usr/libexec/path_helper)"

==> Analytics
install: 3,119 (30 days), 9,427 (90 days), 35,098 (365 days)
```
