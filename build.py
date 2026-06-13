#!/usr/bin/env python3
"""Build the résumé from resume.yaml.

Single source of truth -> two outputs:
  build/cv.pdf      LaTeX résumé (templates/*.tex.j2 -> .tex -> lualatex)
  build/resume.json normalized content for the mattbachmann.dev portfolio site

Usage:
    python build.py            # render .tex, emit resume.json, build the PDF
    python build.py --no-pdf   # render .tex + resume.json only (no LaTeX needed)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import jinja2
import yaml

ROOT = Path(__file__).parent.resolve()
TEMPLATES = ROOT / "templates"
BUILD = ROOT / "build"

# Sections that become \input files, plus the main document.
SECTION_TEMPLATES = [
    "section_headline",
    "section_competences",
    "section_experience",
    "section_education",
    "section_talks",
]

# Characters that must be escaped to appear literally in LaTeX. Order matters:
# backslash first so we don't double-escape the replacements we insert.
_TEX_REPLACEMENTS = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]


def tex_escape(value) -> str:
    """Escape a value for safe literal inclusion in LaTeX source."""
    text = "" if value is None else str(value)
    for char, replacement in _TEX_REPLACEMENTS:
        text = text.replace(char, replacement)
    return text


def make_env() -> jinja2.Environment:
    """Jinja env with LaTeX-safe delimiters (\\VAR{}, \\BLOCK{}) so the template
    syntax never collides with LaTeX's own { } and %."""
    env = jinja2.Environment(
        block_start_string=r"\BLOCK{",
        block_end_string="}",
        variable_start_string=r"\VAR{",
        variable_end_string="}",
        comment_start_string=r"\#{",
        comment_end_string="}",
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        keep_trailing_newline=True,
        loader=jinja2.FileSystemLoader(str(TEMPLATES)),
    )
    env.filters["tex"] = tex_escape
    return env


def load_data() -> dict:
    with open(ROOT / "resume.yaml", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    data["name"]["full"] = f"{data['name']['first']} {data['name']['last']}"
    return data


def render_latex(env: jinja2.Environment, data: dict) -> None:
    BUILD.mkdir(exist_ok=True)
    # Make the build dir self-contained so lualatex finds the class and fonts
    # (the .cls loads fonts via a cwd-relative `Path = fonts/`).
    for name in ("yaac-another-awesome-cv.cls", "fonts"):
        link = BUILD / name
        if not link.exists():
            os.symlink(ROOT / name, link)

    for name in ["cv", *SECTION_TEMPLATES]:
        rendered = env.get_template(f"{name}.tex.j2").render(**data)
        (BUILD / f"{name}.tex").write_text(rendered, encoding="utf-8")


def write_json(data: dict) -> None:
    """Emit the portfolio-facing artifact. Clean text, plus a display-friendly
    date range per role."""
    for job in data.get("experience", []):
        start, end = job.get("date_start", ""), job.get("date_end", "")
        if start and end:
            job["dates"] = f"{start} – {end}"
        else:
            job["dates"] = end or start or ""
    BUILD.mkdir(exist_ok=True)
    (BUILD / "resume.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def build_pdf() -> None:
    if shutil.which("latexmk") is None:
        sys.exit("latexmk not found on PATH — install a TeX distribution, or use --no-pdf")
    subprocess.run(
        ["latexmk", "-lualatex", "-interaction=nonstopmode", "-halt-on-error", "cv.tex"],
        cwd=BUILD,
        check=True,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-pdf", action="store_true", help="skip the LaTeX build")
    args = parser.parse_args()

    data = load_data()
    render_latex(make_env(), data)
    write_json(data)
    print(f"Rendered LaTeX + resume.json into {BUILD}")
    if not args.no_pdf:
        build_pdf()
        print(f"Built {BUILD / 'cv.pdf'}")


if __name__ == "__main__":
    main()
