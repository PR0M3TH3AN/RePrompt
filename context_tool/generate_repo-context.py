#!/usr/bin/env python3

"""
Script Name: generate_repo_context.py
Description: Generates a context file (`repo-context.txt`) for AI coding assistants.
             Includes an overview, important information, a directory tree with exclusions,
             content of important files with syntax highlighting, and a to-do list.

Usage:
1. Ensure you have Python 3.7 or higher installed.

2. (Optional) Set up a Python virtual environment:
     python3 -m venv venv
     source venv/bin/activate               # On Unix or MacOS
     venv\Scripts\activate.bat              # On Windows (Command Prompt)
     venv\Scripts\Activate.ps1              # On Windows (PowerShell)

3. Install the required Python packages:
     pip install -r requirements.txt

4. Configure `config.yaml` as needed.

5. Place `overview.txt`, `important_info.txt`, and `to-do_list.txt` in the script directory.

6. Run the script:
     ./generate_repo_context.py             # Unix-like systems
     python generate_repo_context.py        # Windows
     
The script will create `repo-context.txt` with the specified structure.
"""

import os
import sys
import yaml
from pathlib import Path
import mimetypes
import logging
from typing import List, Dict
from datetime import datetime  # Added import for datetime

# Configuration Constants
CONFIG_FILE = "config.yaml"
OUTPUT_FILE = "repo-context.txt"

# Static Text Files and Their Corresponding Section Titles
STATIC_FILES = [
    {"file": "overview.txt", "section_title": "Overview"},
    {"file": "important_info.txt", "section_title": "Important Information"},
    {"file": "to-do_list.txt", "section_title": "To-Do List"}
]

# Mapping of File Extensions to Programming Languages for Syntax Highlighting
LANGUAGE_MAP = {
    '.py': 'python',
    '.json': 'json',
    '.env': 'bash',
    '.js': 'javascript',
    '.html': 'html',
    '.css': 'css',
    '.csv': 'csv',
    '.md': 'markdown',
    '.txt': '',  # Plain text
    # Add more mappings as needed
}

# Extensions of Binary Files to Skip
BINARY_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.db', '.exe', '.bin']

def setup_logging():
    """Configures the logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s'
    )

def load_config(config_path: Path) -> Dict:
    """
    Loads configuration from a YAML file.

    Args:
        config_path (Path): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary containing 'exclude_dirs' and 'important_files'.
    """
    if not config_path.exists():
        logging.error(f"Configuration file {config_path} not found.")
        sys.exit(1)
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.info(f"Loaded configuration from {config_path}.")
        return config
    except yaml.YAMLError as e:
        logging.error(f"Error parsing configuration file: {e}")
        sys.exit(1)

def generate_directory_tree(start_path: Path, exclude_dirs: List[str]) -> List[str]:
    """
    Generates a directory tree as a list of strings, excluding specified directories.

    Args:
        start_path (Path): The root directory to start generating the tree from.
        exclude_dirs (list): List of directory patterns to exclude.

    Returns:
        list: List of strings representing the directory tree.
    """
    tree_lines = []
    root = start_path.resolve()
    for dirpath, dirnames, filenames in os.walk(start_path):
        current_path = Path(dirpath)
        rel_path = current_path.relative_to(root)

        # Skip excluded directories
        if any(current_path.match(excl) or excl in rel_path.parts for excl in exclude_dirs):
            dirnames[:] = []  # Don't traverse further into subdirectories
            continue

        # Determine the indentation level
        depth = len(rel_path.parts)
        indent = "    " * depth
        connector = "├── " if depth > 0 else "."
        if depth > 0:
            tree_lines.append(f"{indent}{connector}{current_path.name}/")
        else:
            tree_lines.append(f"{connector}")

        # Add files in the current directory
        for filename in sorted(filenames):
            file_rel_path = rel_path / filename
            if any(file_rel_path.match(excl) or excl in file_rel_path.parts for excl in exclude_dirs):
                continue
            file_indent = "    " * (depth + 1)
            tree_lines.append(f"{file_indent}├── {filename}")

    logging.info("Directory tree generated.")
    return tree_lines

def write_directory_tree(tree_lines: List[str], output_file: Path):
    """
    Writes the directory tree to the output file within markdown code blocks.

    Args:
        tree_lines (list): List of strings representing the directory tree.
        output_file (Path): Path to the output file where the tree will be written.
    """
    with output_file.open('a', encoding='utf-8') as f:
        f.write("## Directory Tree with Exclusions\n\n")
        f.write("```\n")
        for line in tree_lines:
            f.write(line + "\n")
        f.write("```\n\n")
    logging.info("Directory tree written to the context file.")

def write_file_content(file_path: Path, output_file: Path):
    """
    Writes the content of a file to the output file within markdown code blocks with syntax highlighting.

    Args:
        file_path (Path): Path to the file whose content is to be written.
        output_file (Path): Path to the output file where the content will be written.
    """
    ext = file_path.suffix
    language = LANGUAGE_MAP.get(ext, '')
    try:
        relative_display_path = file_path.relative_to(file_path.parents[1])
    except ValueError:
        # If relative_to fails, fallback to absolute path
        relative_display_path = file_path
    with output_file.open('a', encoding='utf-8') as f:
        f.write(f"## {relative_display_path}\n")
        if language:
            f.write(f"```{language}\n")
        else:
            f.write("```\n")
        try:
            if ext in BINARY_EXTENSIONS:
                # Skip binary files
                f.write(f"*Binary file ({ext}) cannot be displayed.*\n")
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_content:
                    content = file_content.read()
                    f.write(content)
        except Exception as e:
            f.write(f"*Error reading file: {e}*\n")
        f.write("\n```\n\n")
    logging.info(f"Included content from {file_path}.")

def write_static_file(file_path: Path, output_file: Path, section_title: str):
    """
    Writes the content of a static text file to the output file with a section header.

    Args:
        file_path (Path): Path to the static text file.
        output_file (Path): Path to the output file where the content will be written.
        section_title (str): Title of the section to be added before the content.
    """
    if not file_path.exists():
        logging.warning(f"Static file {file_path} not found, skipping...")
        return
    with output_file.open('a', encoding='utf-8') as f:
        f.write(f"## {section_title}\n\n")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as sf:
                content = sf.read()
                f.write(content + "\n\n")
        except Exception as e:
            f.write(f"*Error reading {file_path.name}: {e}*\n\n")
            logging.error(f"Error reading {file_path}: {e}")
    logging.info(f"Included static section: {section_title}.")

def write_custom_sections(custom_sections: List[Dict], script_dir: Path, output_file: Path):
    """
    Writes custom sections to the output file based on configuration.

    Args:
        custom_sections (list): List of dictionaries with 'file' and 'section_title'.
        script_dir (Path): Directory where the script is located.
        output_file (Path): Path to the output file.
    """
    for section in custom_sections:
        file_name = section.get('file')
        section_title = section.get('section_title', 'Custom Section')
        file_path = script_dir / file_name
        write_static_file(file_path, output_file, section_title)

def main():
    """Main function that orchestrates the generation of the repository context file."""
    setup_logging()

    # Determine the script's directory
    script_dir = Path(__file__).parent.resolve()

    # Load configuration
    config_path = script_dir / CONFIG_FILE
    config = load_config(config_path)
    exclude_dirs = config.get("exclude_dirs", [])
    important_files = config.get("important_files", [])
    custom_sections = config.get("custom_sections", [])

    # Define the starting path (default to 'src' directory or as specified)
    source_dir = config.get("source_directory", "src")
    start_path = script_dir.parent / source_dir
    if not start_path.exists():
        logging.error(f"Source directory {start_path} does not exist.")
        sys.exit(1)

    output_file = script_dir / OUTPUT_FILE
    output_file.unlink(missing_ok=True)  # Remove if exists

    # Write a header to the output file
    with output_file.open('w', encoding='utf-8') as f:
        f.write(f"# Repository Context\n\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")  # Updated line

    # Write static sections
    for static in STATIC_FILES:
        static_path = script_dir / static["file"]
        write_static_file(static_path, output_file, static["section_title"])

    # Generate and write the directory tree
    tree_lines = generate_directory_tree(start_path, exclude_dirs)
    write_directory_tree(tree_lines, output_file)

    # Write important files
    with output_file.open('a', encoding='utf-8') as f:
        f.write("## Important Files\n\n")
    for relative_file in important_files:
        file_path = start_path / relative_file
        if file_path.exists():
            write_file_content(file_path, output_file)
        else:
            with output_file.open('a', encoding='utf-8') as f:
                f.write(f"*File `{relative_file}` not found, skipping...*\n\n")
            logging.warning(f"Important file {relative_file} not found, skipping...")

    # Write custom sections if any
    if custom_sections:
        write_custom_sections(custom_sections, script_dir, output_file)

    # Write to-do list
    todo_path = script_dir / "to-do_list.txt"
    write_static_file(todo_path, output_file, "To-Do List")

    logging.info(f"Context file created: {output_file}")

if __name__ == "__main__":
    main()
