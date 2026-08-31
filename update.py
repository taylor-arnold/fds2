#!/usr/bin/env python3
"""
update.py

Behavior:
- Searches `nb289` and `nb389` for files matching `notebookXX.qmd`.
- Parses the YAML header in each file for `title` and `solutions-release-date`.
- Compares the release date (at that directory's release hour) to the current system time.
- If the current time is past the release time (or if MAKE_ALL is True), the notebook is marked for release.
- Updates the `_quarto.yml` file in the respective directory, specifically modifying 
  the `project.render` list and the `website.sidebar.contents` list.
- Deletes any already-rendered HTML in the output directory belonging to a notebook
  that has not been released, so unreleased solutions are not left reachable by URL.

Pass --dry-run to report what would change without touching any files.
"""

import os
import re
import sys
import json
import shutil
import datetime

# ==========================================
# CONFIGURATION
# ==========================================
# Set to True to forcefully release all notebooks (ignore dates). Useful when
# testing a full render; leave it False so solutions appear on their own dates.
MAKE_ALL = False

# Hour of the day (24-hour clock) at which a notebook's solutions go live on its
# release date. Each course keeps its own hour so solutions can appear after that
# section has met; anything not listed here falls back to noon.
RELEASE_HOURS = {"nb289": 9, "nb389": 9}
DEFAULT_RELEASE_HOUR = 12

# Quarto never deletes files it has already written, so a notebook dropped from
# the render list keeps its old HTML sitting in the output directory, reachable
# at its direct URL even though it no longer appears in the sidebar. Set this to
# True to delete the rendered output of any notebook that has not been released.
PRUNE_UNRELEASED = True

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

_YAML_RE = re.compile(r"^---\n(.*?)\n---(\n|$)", re.DOTALL)

def _extract_metadata(content: str) -> tuple[str, str]:
    """Extracts the title and solutions-release-date from the YAML header."""
    m = _YAML_RE.match(content)
    if not m:
        return "Untitled", "Unknown"
        
    yaml_text = m.group(1)
    
    title_match = re.search(r'^title:\s*["\'](.*?)["\']', yaml_text, re.MULTILINE)
    date_match = re.search(r'^solutions-release-date:\s*["\'](.*?)["\']', yaml_text, re.MULTILINE)
    
    title = title_match.group(1) if title_match else "Untitled"
    rel_date = date_match.group(1) if date_match else "Unknown"
    
    return title, rel_date

def _should_release(date_str: str, hour: int = DEFAULT_RELEASE_HOUR) -> bool:
    """Determines if a notebook should be released based on the given date and hour."""
    if MAKE_ALL:
        return True
        
    try:
        # Assuming date format is YYYY-MM-DD
        release_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        release_time = release_date.replace(hour=hour, minute=0, second=0)
        
        return datetime.datetime.now() >= release_time
    except ValueError:
        # If the date is malformed (e.g., "2026-XX-XX"), we default to False unless MAKE_ALL is True
        return False

def _update_quarto_yml(yml_path: str, released_notebooks: list, dry_run: bool = False):
    """
    Updates the _quarto.yml file safely by replacing the render block 
    and contents block with the new lists of released notebooks.
    """
    if not os.path.exists(yml_path):
        print(f"  {Colors.FAIL}Error: {yml_path} not found.{Colors.ENDC}")
        return

    with open(yml_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip_mode = None  # Tracks if we are currently skipping old lines in a list block

    for line in lines:
        stripped = line.rstrip()

        # Handle skipping old project.render list items
        if skip_mode == 'render':
            if line.startswith('    -') or stripped == '':
                continue
            else:
                skip_mode = None

        # Handle skipping old website.sidebar.contents list items
        if skip_mode == 'contents':
            if line.startswith('      -') or line.startswith('        text:') or line.startswith('        file:') or stripped == '':
                continue
            else:
                skip_mode = None

        # Detect the start of the render block
        if stripped == '  render:':
            new_lines.append(line)
            for nb in released_notebooks:
                new_lines.append(f'    - "{nb["filename"]}"\n')
            skip_mode = 'render'
            continue

        # Detect the start of the sidebar contents block
        if stripped == '    contents:':
            new_lines.append(line)
            for nb in released_notebooks:
                new_lines.append(f'      - file: {nb["filename"]}\n')
                new_lines.append(f'        text: "{nb["title"]}"\n')
            skip_mode = 'contents'
            continue

        if skip_mode is None:
            new_lines.append(line)

    if dry_run:
        return

    with open(yml_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def _output_dir(yml_path: str) -> str | None:
    """Reads project.output-dir out of a _quarto.yml, resolved against its location."""
    if not os.path.exists(yml_path):
        return None

    with open(yml_path, 'r', encoding='utf-8') as f:
        m = re.search(r'^\s*output-dir:\s*["\']?(.*?)["\']?\s*$', f.read(), re.MULTILINE)

    if not m:
        return None

    return os.path.normpath(os.path.join(os.path.dirname(yml_path), m.group(1)))


def _prune_unreleased_output(directory: str, unreleased: list, dry_run: bool = False):
    """
    Removes the rendered HTML of unreleased notebooks from the output directory.

    Quarto only ever writes to its output directory, so dropping a notebook from
    the render list leaves the previous render in place and publicly reachable.
    Each notebook renders to `notebookXX.html` plus, when it produced figures, a
    `notebookXX_files/` directory; both are removed here, along with the notebook's
    entries in `search.json`, which holds the full text of every page it indexes.
    """
    out_dir = _output_dir(os.path.join(directory, "_quarto.yml"))

    if out_dir is None:
        print(f"  {Colors.WARNING}No output-dir found; skipping prune.{Colors.ENDC}")
        return

    if not os.path.isdir(out_dir):
        print(f"  {Colors.OKCYAN}Nothing rendered in {out_dir} yet; nothing to prune.{Colors.ENDC}")
        return

    removed = 0

    for nb in unreleased:
        base = os.path.splitext(nb["filename"])[0]
        targets = [
            os.path.join(out_dir, base + ".html"),
            os.path.join(out_dir, base + "_files"),
        ]

        for target in targets:
            if not os.path.exists(target):
                continue

            label = "Would remove" if dry_run else "Removed"
            print(f"  {Colors.FAIL}{label}{Colors.ENDC} {target}")
            removed += 1

            if dry_run:
                continue

            if os.path.isdir(target):
                shutil.rmtree(target)
            else:
                os.remove(target)

    removed += _prune_search_index(out_dir, unreleased, dry_run=dry_run)

    if removed == 0:
        print(f"  {Colors.OKGREEN}✓{Colors.ENDC} No unreleased output found in {out_dir}.")
    else:
        verb = "would be removed" if dry_run else "removed"
        print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {removed} stale item(s) {verb} from {out_dir}.")


def _prune_search_index(out_dir: str, unreleased: list, dry_run: bool = False) -> int:
    """
    Drops unreleased notebooks from Quarto's search index.

    `search.json` stores the full text of each page it indexes, so leaving an
    unreleased notebook in it exposes the solutions through the search box even
    after its HTML has been deleted. Quarto rewrites this file from scratch on
    the next render; this keeps it honest in the meantime.
    """
    index_path = os.path.join(out_dir, "search.json")

    if not os.path.exists(index_path):
        return 0

    with open(index_path, 'r', encoding='utf-8') as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            print(f"  {Colors.WARNING}Could not parse {index_path}; leaving it alone.{Colors.ENDC}")
            return 0

    bases = {os.path.splitext(nb["filename"])[0] for nb in unreleased}

    def is_unreleased(entry):
        href = entry.get("href", "").split("#")[0]
        return os.path.splitext(os.path.basename(href))[0] in bases

    kept = [e for e in entries if not is_unreleased(e)]
    dropped = len(entries) - len(kept)

    if dropped == 0:
        return 0

    label = "Would drop" if dry_run else "Dropped"
    print(f"  {Colors.FAIL}{label}{Colors.ENDC} {dropped} search index entr(ies) from {index_path}")

    if not dry_run:
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(kept, f, indent=2)

    return dropped

# --- Core --------------------------------------------------------------------

def process_directory(directory: str, dry_run: bool = False):
    hour = RELEASE_HOURS.get(os.path.basename(os.path.normpath(directory)), DEFAULT_RELEASE_HOUR)
    print(f"\n{Colors.HEADER}{Colors.BOLD}Scanning Directory: {directory}{Colors.ENDC} {Colors.OKCYAN}(releases at {hour:02d}:00){Colors.ENDC}")
    
    if not os.path.isdir(directory):
        print(f"{Colors.WARNING}Warning: Directory '{directory}' not found. Skipping.{Colors.ENDC}")
        return

    file_pattern = re.compile(r"^notebook\d+\.qmd$")
    found_files = [f for f in os.listdir(directory) if file_pattern.match(f)]
    found_files.sort()

    released_notebooks = []
    unreleased_notebooks = []

    if not found_files:
        print(f"  {Colors.WARNING}No matching 'notebookXX.qmd' files found.{Colors.ENDC}")
        return

    for filename in found_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        title, rel_date = _extract_metadata(content)
        will_release = _should_release(rel_date, hour)

        if will_release:
            released_notebooks.append({
                "filename": filename,
                "title": title
            })
            status = f"{Colors.OKGREEN}Releasing{Colors.ENDC}"
        else:
            unreleased_notebooks.append({
                "filename": filename,
                "title": title
            })
            status = f"{Colors.WARNING}Skipping{Colors.ENDC} "

        print(f"  {status} | {Colors.OKCYAN}{filename}{Colors.ENDC} | Date: {rel_date} | Title: {title}")

    # Update the _quarto.yml for this specific directory
    yml_path = os.path.join(directory, "_quarto.yml")
    print(f"\n  {Colors.BOLD}Updating {yml_path}...{Colors.ENDC}")
    _update_quarto_yml(yml_path, released_notebooks, dry_run=dry_run)
    verb = "would be added to" if dry_run else "added to"
    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} {len(released_notebooks)} notebooks {verb} configuration.")

    if PRUNE_UNRELEASED and unreleased_notebooks:
        print(f"\n  {Colors.BOLD}Pruning rendered output for {len(unreleased_notebooks)} unreleased notebook(s)...{Colors.ENDC}")
        _prune_unreleased_output(directory, unreleased_notebooks, dry_run=dry_run)

# --- Automation --------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv[1:]
    target_dirs = ["nb289", "nb389"]

    if dry_run:
        print(f"\n{Colors.BOLD}{Colors.WARNING}Dry run: no files will be written or deleted.{Colors.ENDC}")

    if MAKE_ALL:
        print(f"\n{Colors.WARNING}MAKE_ALL is on: every notebook is released regardless of its date.{Colors.ENDC}")

    for d in target_dirs:
        process_directory(d, dry_run=dry_run)

    tail = "Dry run complete." if dry_run else "All updates complete!"
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}{tail}{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
