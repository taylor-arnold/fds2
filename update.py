#!/usr/bin/env python3
"""
update.py

Behavior:
- Searches `nb289` and `nb389` for files matching `notebookXX.qmd`.
- Parses the YAML header in each file for `title` and `solutions-release-date`.
- Compares the release date (at 12:00 PM / noon) to the current system time.
- If the current time is past the release time (or if MAKE_ALL is True), the notebook is marked for release.
- Updates the `_quarto.yml` file in the respective directory, specifically modifying 
  the `project.render` list and the `website.sidebar.contents` list.
"""

import os
import re
import datetime

# ==========================================
# CONFIGURATION
# ==========================================
# Set to True to forcefully release all notebooks (ignore dates)
MAKE_ALL = False 

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

def _should_release(date_str: str) -> bool:
    """Determines if a notebook should be released based on noon of the given date."""
    if MAKE_ALL:
        return True
        
    try:
        # Assuming date format is YYYY-MM-DD
        release_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        # Set release time to 12:00 PM (noon)
        release_time = release_date.replace(hour=12, minute=0, second=0)
        
        return datetime.datetime.now() >= release_time
    except ValueError:
        # If the date is malformed (e.g., "2026-XX-XX"), we default to False unless MAKE_ALL is True
        return False

def _update_quarto_yml(yml_path: str, released_notebooks: list):
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

    with open(yml_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# --- Core --------------------------------------------------------------------

def process_directory(directory: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}Scanning Directory: {directory}{Colors.ENDC}")
    
    if not os.path.isdir(directory):
        print(f"{Colors.WARNING}Warning: Directory '{directory}' not found. Skipping.{Colors.ENDC}")
        return

    file_pattern = re.compile(r"^notebook\d+\.qmd$")
    found_files = [f for f in os.listdir(directory) if file_pattern.match(f)]
    found_files.sort()

    released_notebooks = []

    if not found_files:
        print(f"  {Colors.WARNING}No matching 'notebookXX.qmd' files found.{Colors.ENDC}")
        return

    for filename in found_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        title, rel_date = _extract_metadata(content)
        will_release = _should_release(rel_date)

        if will_release:
            released_notebooks.append({
                "filename": filename,
                "title": title
            })
            status = f"{Colors.OKGREEN}Releasing{Colors.ENDC}"
        else:
            status = f"{Colors.WARNING}Skipping{Colors.ENDC} "

        print(f"  {status} | {Colors.OKCYAN}{filename}{Colors.ENDC} | Date: {rel_date} | Title: {title}")

    # Update the _quarto.yml for this specific directory
    yml_path = os.path.join(directory, "_quarto.yml")
    print(f"\n  {Colors.BOLD}Updating {yml_path}...{Colors.ENDC}")
    _update_quarto_yml(yml_path, released_notebooks)
    print(f"  {Colors.OKGREEN}✓{Colors.ENDC} Added {len(released_notebooks)} notebooks to configuration.")

# --- Automation --------------------------------------------------------------

def main():
    target_dirs = ["nb289", "nb389"]
    
    for d in target_dirs:
        process_directory(d)
        
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}All updates complete!{Colors.ENDC}\n")

if __name__ == "__main__":
    main()
