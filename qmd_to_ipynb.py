#!/usr/bin/env python3
"""
qmd_to_ipynb.py

Behavior:
- Automatically searches `nb289` and `nb389` for files matching `notebookXX.qmd`
- Converts a Quarto .qmd to a Jupyter .ipynb in OUTPUT_DIR (student version)
  and also to OUTPUT_DIR_FULL (solutions version, all code blocks kept)
- Executable code blocks -> code cells
- All code cells are cleared EXCEPT those marked to keep via:
    #| tags: [noclear]   OR   #| keep: true
- Blocks marked with #| tags: [uncomment] are kept AND have all lines
  uncommented (leading '# ' removed). This implicitly acts as [noclear].
- Blocks marked with #| tags: [remove] are completely removed from the
  output (no cell created), including any trailing blank lines.
- In kept code cells, ALL lines starting with '#|' are removed
- Markdown text is preserved as markdown cells, with each paragraph
  (text separated by blank lines) becoming a separate cell
- Lines starting with '**Answer**:' have everything after '**Answer**:' removed,
  including any continuation lines of a multi-line answer
- Parses Quarto YAML headers, transforming the `title` into a markdown cell
  and tracking the `solutions-release-date`.
"""

import os
import json
import re

# ===== Hard-coded output directories =====
OUTPUT_DIR = "nb"
OUTPUT_DIR_FULL = "nb_full"

# --- ANSI Colors for CLI -----------------------------------------------------

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- Helpers -----------------------------------------------------------------

_LANGS_COMMON = {"python", "r", "bash", "sh", "zsh", "julia", "javascript", "js", "typescript", "ts"}

def _is_executable_chunk(langspec: str) -> bool:
    langspec = langspec.strip().lower()
    if langspec.startswith("{") and langspec.endswith("}"):
        return True
    bare = langspec.strip("` ").strip()
    return bare in _LANGS_COMMON

_KEEP_TAG_RE = re.compile(r"^\s*#\|\s*tags\s*:\s*\[([^\]]*)\]", re.IGNORECASE | re.MULTILINE)
_KEEP_FLAG_RE = re.compile(r"^\s*#\|\s*keep\s*:\s*(true|yes|1)\s*$", re.IGNORECASE | re.MULTILINE)
# Matches a YAML frontmatter block at the very start of the file
_YAML_RE = re.compile(r"^---\n(.*?)\n---(\n|$)", re.DOTALL)

def _get_tags(body: str) -> set:
    """Extract tags from a code block body."""
    m = _KEEP_TAG_RE.search(body)
    if m:
        tags_str = m.group(1)
        return {t.strip().strip("'\"").lower() for t in tags_str.split(",")}
    return set()

def _has_keep_signal(body: str) -> bool:
    if _KEEP_FLAG_RE.search(body):
        return True
    tags = _get_tags(body)
    return bool(tags & {"noclear", "keep", "uncomment"})

def _has_uncomment_signal(body: str) -> bool:
    return "uncomment" in _get_tags(body)

def _has_remove_signal(body: str) -> bool:
    return "remove" in _get_tags(body)

def _uncomment_lines(lines):
    """Remove leading '# ' from lines (single comment prefix)."""
    result = []
    for ln in lines:
        if ln.startswith("# "):
            result.append(ln[2:])
        elif ln.startswith("#") and (len(ln) == 1 or ln[1:].startswith("\n")):
            result.append(ln[1:])
        else:
            result.append(ln)
    return result

def _strip_quarto_option_lines(lines):
    """Remove all Quarto option lines that start with '#|' (any indentation)."""
    return [ln for ln in lines if not ln.lstrip().startswith("#|")]

def _strip_answer_content(lines):
    """For lines starting with '**Answer**:', keep only '**Answer**:' and remove
    everything after it, including any continuation lines that belong to the
    same paragraph (an answer's explanation can span multiple lines)."""
    result = []
    for ln in lines:
        stripped = ln.lstrip()
        if stripped.startswith("**Answer**:"):
            idx = ln.find("**Answer**:")
            if ln.endswith("\n"):
                result.append(ln[:idx] + "**Answer**:\n")
            else:
                result.append(ln[:idx] + "**Answer**:")
            break
        else:
            result.append(ln)
    return result

def _split_into_paragraphs(text: str) -> list:
    """Split text into paragraphs (separated by one or more blank lines)."""
    paragraphs = re.split(r'\n\s*\n', text)
    return [p.strip() for p in paragraphs if p.strip()]

def _extract_and_replace_yaml(content: str) -> tuple[str, str, str]:
    """
    Looks for a YAML header at the start. Extracts the title and solutions-release-date,
    and replaces the YAML block with a standard Markdown title to be parsed.
    """
    m = _YAML_RE.match(content)
    if not m:
        return content, None, None
        
    yaml_text = m.group(1)
    
    # Extract fields with regex to avoid requiring external pyyaml dependency
    title_match = re.search(r'^title:\s*["\'](.*?)["\']', yaml_text, re.MULTILINE)
    date_match = re.search(r'^solutions-release-date:\s*["\'](.*?)["\']', yaml_text, re.MULTILINE)
    
    title = title_match.group(1) if title_match else "Untitled"
    rel_date = date_match.group(1) if date_match else "Unknown"
    
    # Remove the YAML block and prepend the Markdown title string
    new_content = content[m.end():]
    header_markdown = f"## {title}\n\n"
    
    return header_markdown + new_content, title, rel_date

# --- Core --------------------------------------------------------------------

FENCE_RE = re.compile(
    r"```([^\n]*)\n"      # opening fence + langspec (group 1)
    r"(.*?)"              # body (group 2), non-greedy
    r"\n```",             # closing fence
    re.DOTALL
)

def _build_cells(content: str, noclear_all: bool = False) -> list:
    """Parse content and return notebook cells."""
    cells = []
    pos = 0

    for m in FENCE_RE.finditer(content):
        start, end = m.span()
        langspec = m.group(1).strip()
        body = m.group(2)

        # Preceding text -> markdown (split into separate cells per paragraph)
        if start > pos:
            text_chunk = content[pos:start]
            for para in _split_into_paragraphs(text_chunk):
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": _strip_answer_content(para.splitlines(keepends=True))
                })

        if _is_executable_chunk(langspec):
            # Check if block should be removed entirely
            if _has_remove_signal(body):
                # Skip trailing blank lines after the removed block
                trailing = content[end:]
                stripped = trailing.lstrip('\n')
                pos = end + (len(trailing) - len(stripped))
                continue

            keep_code = noclear_all or _has_keep_signal(body)
            if keep_code:
                raw_lines = body.splitlines(keepends=True)
                code_source = _strip_quarto_option_lines(raw_lines)
                if _has_uncomment_signal(body):
                    code_source = _uncomment_lines(code_source)
            else:
                code_source = []
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_source
            })
        else:
            # Non-exec fence -> markdown (as literal fenced block)
            fence_text = content[start:end]
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": _strip_answer_content(fence_text.splitlines(keepends=True))
            })

        pos = end

    # Trailing text (split into separate cells per paragraph)
    if pos < len(content):
        tail = content[pos:]
        for para in _split_into_paragraphs(tail):
            cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": _strip_answer_content(para.splitlines(keepends=True))
            })

    return cells


def _write_notebook(cells: list, out_path: str):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(notebook, f, indent=2)


def qmd_to_ipynb(filepath: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR_FULL, exist_ok=True)

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pre-process YAML out of the content
    content, title, rel_date = _extract_and_replace_yaml(content)
    
    if title:
         print(f"  {Colors.WARNING}Title:{Colors.ENDC} {title}  |  {Colors.WARNING}Release Date:{Colors.ENDC} {rel_date}")

    base = os.path.splitext(os.path.basename(filepath))[0]

    out_path = os.path.join(OUTPUT_DIR, base + ".ipynb")
    _write_notebook(_build_cells(content, noclear_all=False), out_path)
    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Saved student:  {Colors.OKBLUE}{out_path}{Colors.ENDC}")

    out_path_full = os.path.join(OUTPUT_DIR_FULL, base + ".ipynb")
    _write_notebook(_build_cells(content, noclear_all=True), out_path_full)
    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Saved solution: {Colors.OKBLUE}{out_path_full}{Colors.ENDC}")

# --- Automation --------------------------------------------------------------

def main():
    target_dirs = ["nb289", "nb389"]
    # Matches strings like "notebook01.qmd", "notebook123.qmd"
    file_pattern = re.compile(r"^notebook\d+\.qmd$")
    
    found_files = []

    for d in target_dirs:
        if os.path.isdir(d):
            for filename in os.listdir(d):
                if file_pattern.match(filename):
                    found_files.append(os.path.join(d, filename))
        else:
            print(f"{Colors.WARNING}Warning: Directory '{d}' not found.{Colors.ENDC}")

    if not found_files:
        print(f"{Colors.FAIL}No matching 'notebookXX.qmd' files found in {target_dirs}.{Colors.ENDC}")
        return

    # Sort files for a neat progress readout
    found_files.sort()
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}Found {len(found_files)} notebook(s) to process.{Colors.ENDC}\n")

    for filepath in found_files:
        print(f"{Colors.OKCYAN}Processing: {filepath}{Colors.ENDC}")
        qmd_to_ipynb(filepath)
        print("-" * 40)
        
    print(f"{Colors.OKGREEN}{Colors.BOLD}All conversions complete!{Colors.ENDC}\n")

if __name__ == "__main__":
    main()