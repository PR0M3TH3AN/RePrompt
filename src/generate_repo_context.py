#!/usr/bin/env python3
"""
Script Name: generate_repo_context.py
Description: Generates a context file (``repo-context.txt``) for AI coding assistants.
             This revised version **only shows the directory structure for files that
             are explicitly whitelisted** via the Streamlit UI (``important_files`` in
             ``config.yaml``). All other paths are ignored, so the directory tree is
             minimal and focused on the user-selected scope.

Usage:
    Streamlit writes an updated ``config.yaml`` that includes:
        source_directory: <absolute path to repo>
        important_files:  # list[str] – paths *relative* to the repo root
        exclude_dirs:     # (optional) patterns to skip entirely
    Then it invokes this script.

    See README or Streamlit UI for full workflow.
"""

from __future__ import annotations

import logging
import os
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

import yaml

# ─── Configuration Constants ────────────────────────────────────────────────────
CONFIG_FILE = "config.yaml"
OUTPUT_FILE = "repo-context.txt"

# Static text sections that can be dropped in verbatim
STATIC_FILES = [
    {"file": "overview.txt", "section_title": "Overview"},
    {"file": "important_info.txt", "section_title": "Important Information"},
    {"file": "to-do_list.txt", "section_title": "To-Do List"},
]

# File-extension → syntax-highlight language map for fenced code blocks
LANGUAGE_MAP = {
    ".py": "python",
    ".json": "json",
    ".env": "bash",
    ".js": "javascript",
    ".html": "html",
    ".css": "css",
    ".csv": "csv",
    ".md": "markdown",
    ".txt": "",  # plain text
    ".xml": "xml",
}

# Binary extensions (skipped – we don’t dump binary blobs into markdown)
BINARY_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".db",
    ".exe",
    ".bin",
]

# ─── Helpers ────────────────────────────────────────────────────────────────────

def setup_logging() -> None:
    """Configure basic colourless log output."""
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def load_config(config_path: Path) -> Dict:
    """Load YAML config or abort if it’s missing/invalid."""
    if not config_path.exists():
        logging.error(f"Configuration file {config_path} not found.")
        sys.exit(1)
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        logging.info("Loaded configuration.")
        return cfg
    except yaml.YAMLError as exc:
        logging.error(f"Error parsing configuration file: {exc}")
        sys.exit(1)

# ─── Directory-tree generation (whitelist-aware) ───────────────────────────────

def build_whitelist_tree(
    repo_root: Path, *, included_files: List[str], exclude_dirs: List[str] | None = None
) -> List[str]:
    """Return a list of tree-view lines that *only* contain
    directories + files present in ``included_files``.

    Args:
        repo_root: absolute path to repo root (``source_directory``)
        included_files: list of *relative* paths (as written by Streamlit)
        exclude_dirs: optional patterns to ignore entirely (even if they’d be
                       parents of an included file)
    """

    exclude_dirs = exclude_dirs or []
    repo_root = repo_root.resolve()

    # Normalise the whitelist: Posix style, unique, ensure they exist
    norm_files: Set[Path] = set()
    for rel in included_files:
        p = (repo_root / rel).resolve()
        if not p.exists():
            logging.warning(f"Whitelisted file missing on disk – skipped: {rel}")
            continue
        norm_files.add(p)

    if not norm_files:
        logging.warning("No valid whitelisted files – directory tree will be empty.")
        return []

    # Collect every ancestor directory for each whitelisted file
    keep_dirs: Set[Path] = set([repo_root])
    for file_path in norm_files:
        for parent in [*file_path.parents]:  # includes repo_root eventually
            if any(parent.match(excl) or excl in parent.name for excl in exclude_dirs):
                break  # stop climbing when encountering an excluded dir
            keep_dirs.add(parent)

    # Build children mapping for deterministic ordering
    children: Dict[Path, List[Path]] = defaultdict(list)
    for d in keep_dirs:
        children[d.parent].append(d)
    for fp in norm_files:
        children[fp.parent].append(fp)

    for kid_list in children.values():
        kid_list.sort(key=lambda p: (not p.is_dir(), p.name.lower()))  # dirs first

    # Depth-first traversal to emit tree lines
    tree_lines: List[str] = ["."]

    def recurse(dir_path: Path, depth: int) -> None:
        for entry in children.get(dir_path, []):
            if entry == repo_root:
                continue  # skip root as it is already represented by '.'
            indent = "    " * depth
            connector = "├── "
            if entry.is_dir():
                tree_lines.append(f"{indent}{connector}{entry.name}/")
                recurse(entry, depth + 1)
            else:
                tree_lines.append(f"{indent}{connector}{entry.name}")

    recurse(repo_root, 1)
    logging.info("Whitelist-filtered directory tree generated.")
    return tree_lines

# ─── Markdown writers ──────────────────────────────────────────────────────────

def write_directory_tree(tree_lines: List[str], out_path: Path) -> None:
    with out_path.open("a", encoding="utf-8") as fh:
        fh.write("## Directory Tree (Whitelist Only)\n\n")
        fh.write("```\n")
        fh.writelines(line + "\n" for line in tree_lines)
        fh.write("```\n\n")


def write_file_content(file_path: Path, out_path: Path) -> None:
    ext = file_path.suffix
    lang = LANGUAGE_MAP.get(ext, "")

    try:
        relative_display = file_path.relative_to(file_path.parents[1])
    except ValueError:
        relative_display = file_path

    with out_path.open("a", encoding="utf-8") as fh:
        fh.write(f"## {relative_display}\n")
        fh.write(f"```{lang}\n" if lang else "```\n")
        if ext in BINARY_EXTENSIONS:
            fh.write(f"*Binary file ({ext}) cannot be displayed.*\n")
        else:
            try:
                fh.write(file_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception as exc:
                fh.write(f"*Error reading file: {exc}*\n")
        fh.write("\n```\n\n")


def write_static_file(src: Path, out_path: Path, section_title: str) -> None:
    if not src.exists():
        logging.warning(f"Static file missing – skipped: {src}")
        return
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as fh:
        fh.write(f"## {section_title}\n\n")
        fh.write(src.read_text(encoding="utf-8", errors="ignore") + "\n\n")


def write_custom_sections(sections: List[Dict], script_dir: Path, out_path: Path) -> None:
    for entry in sections:
        file_name = entry.get("file")
        title = entry.get("section_title", "Custom Section")
        write_static_file(script_dir / "static_files" / file_name, out_path, title)

# ─── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    setup_logging()

    script_dir = Path(__file__).parent.resolve()
    cfg = load_config(script_dir / CONFIG_FILE)

    # Resolve repo root (can be absolute or relative)
    source_dir_cfg = cfg.get("source_directory", "src")
    repo_root = Path(source_dir_cfg).expanduser()
    if not repo_root.is_absolute():
        repo_root = (script_dir.parent / repo_root).resolve()
    if not repo_root.exists():
        logging.error(f"Source directory does not exist: {repo_root}")
        sys.exit(1)

    important_files: List[str] = cfg.get("important_files", [])
    exclude_dirs: List[str] = cfg.get("exclude_dirs", [])
    custom_sections: List[Dict] = cfg.get("custom_sections", [])

    out_path = script_dir / OUTPUT_FILE
    out_path.unlink(missing_ok=True)

    # ── Header ───────────────────────────────────────────────────────────────
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write("# Repository Context\n\n")
        fh.write(f"Generated on: {datetime.now():%Y-%m-%d}\n\n")

    # ── Static boilerplate docs ──────────────────────────────────────────────
    for static in STATIC_FILES:
        write_static_file(script_dir / "static_files" / static["file"], out_path, static["section_title"])

    # ── Directory tree (whitelist only) ──────────────────────────────────────
    tree_lines = build_whitelist_tree(repo_root, included_files=important_files, exclude_dirs=exclude_dirs)
    write_directory_tree(tree_lines, out_path)

    # ── Important file dumps ─────────────────────────────────────────────────
    with out_path.open("a", encoding="utf-8") as fh:
        fh.write("## Important Files\n\n")
    for rel_path in important_files:
        abs_path = repo_root / rel_path
        if abs_path.exists():
            write_file_content(abs_path, out_path)
        else:
            with out_path.open("a", encoding="utf-8") as fh:
                fh.write(f"*File `{rel_path}` not found – skipped.*\n\n")
            logging.warning(f"Important file not found on disk: {rel_path}")

    # ── Custom sections ─────────────────────────────────────────────────────
    if custom_sections:
        write_custom_sections(custom_sections, script_dir, out_path)

    logging.info(f"Context file created → {out_path}")


if __name__ == "__main__":
    main()
