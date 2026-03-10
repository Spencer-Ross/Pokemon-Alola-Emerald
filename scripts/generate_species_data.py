#!/usr/bin/env python3
"""
Generate include/constants/species.h from data/species_list.txt (single source of truth).
Run from the repository root (Pokemon-Alola-Emerald).

Usage:
  python3 scripts/generate_species_data.py [--validate]
  --validate: also run validation for species-keyed tables and exit with non-zero if any species is missing.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from typing import List, Tuple

# Default repo root = parent of scripts/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

SPECIES_LIST_PATH = os.path.join(REPO_ROOT, "data", "species_list.txt")
SPECIES_H_PATH = os.path.join(REPO_ROOT, "include", "constants", "species.h")

# Species that get a #define; UNUSED and empty lines do not
RESERVED_TOKENS = {"UNUSED", ""}

# Unown form suffixes (generated after NUM_SPECIES)
UNOWN_FORMS = [
    "UNOWN_B", "UNOWN_C", "UNOWN_D", "UNOWN_E", "UNOWN_F", "UNOWN_G", "UNOWN_H",
    "UNOWN_I", "UNOWN_J", "UNOWN_K", "UNOWN_L", "UNOWN_M", "UNOWN_N", "UNOWN_O",
    "UNOWN_P", "UNOWN_Q", "UNOWN_R", "UNOWN_S", "UNOWN_T", "UNOWN_U", "UNOWN_V",
    "UNOWN_W", "UNOWN_X", "UNOWN_Y", "UNOWN_Z", "UNOWN_EMARK", "UNOWN_QMARK",
]


def load_species_list(path: str) -> List[Tuple[int, str]]:
    """Load (index, name) pairs. Name is stripped; empty/UNUSED are included for index alignment.
    Comment lines (starting with #) are skipped; order of non-comment lines defines species index."""
    if not os.path.isfile(path):
        sys.stderr.write(f"Error: species list not found: {path}\n")
        sys.exit(1)
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            raw = line.strip()
            if raw.startswith("#"):
                continue
            name = raw.split("#")[0].strip()  # strip inline comment
            entries.append((len(entries), name))
    return entries


def generate_species_h(entries: List[Tuple[int, str]], out_path: str) -> None:
    """Write include/constants/species.h from the species list."""
    lines = [
        "#ifndef GUARD_CONSTANTS_SPECIES_H",
        "#define GUARD_CONSTANTS_SPECIES_H",
        "",
    ]
    for idx, name in entries:
        if name and name not in RESERVED_TOKENS:
            lines.append(f"#define SPECIES_{name} {idx}")
        # else: reserved/unused slot, no #define
    lines.append("")
    lines.append("#define NUM_SPECIES SPECIES_EGG")
    lines.append("")
    # Unown forms (computed from NUM_SPECIES)
    lines.append("#define SPECIES_UNOWN_B (NUM_SPECIES + 1)")
    for i, form in enumerate(UNOWN_FORMS[1:], start=1):
        prev = UNOWN_FORMS[i - 1]
        lines.append(f"#define SPECIES_{form} (SPECIES_{prev} + 1)")
    lines.append("")
    lines.append("#endif  // GUARD_CONSTANTS_SPECIES_H")
    lines.append("")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def get_species_names_for_validation(entries: List[Tuple[int, str]]) -> set:
    """Return set of SPECIES_ names (without SPECIES_ prefix) that have a #define."""
    return {name for _, name in entries if name and name not in RESERVED_TOKENS}


def validate_tables(entries: List[Tuple[int, str]], repo_root: str) -> bool:
    """
    Check that every species in the master list has an entry in the required tables.
    Returns True if all pass, False otherwise.
    """
    species_names = get_species_names_for_validation(entries)
    # Tables that must have an explicit entry for every species (evolution is sparse).
    # Optional set of species to skip per table (e.g. EGG may be zero-initialized).
    required_tables = [
        ("src/data/pokemon/species_info.h", "species_info", set()),
        ("src/data/pokemon/level_up_learnset_pointers.h", "level_up_learnset_pointers", {"EGG"}),
        ("src/data/text/species_names.h", "species_names", {"EGG"}),
    ]
    all_ok = True
    for rel_path, table_name, skip_species in required_tables:
        path = os.path.join(repo_root, rel_path)
        if not os.path.isfile(path):
            sys.stderr.write(f"Validation: file not found {rel_path}\n")
            all_ok = False
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        missing = []
        for name in species_names:
            if name in skip_species:
                continue
            # Match [SPECIES_<name>] in table
            pattern = r"\[\s*SPECIES_" + re.escape(name) + r"\s*\]"
            if not re.search(pattern, content):
                missing.append(name)
        if missing:
            sys.stderr.write(f"Validation failed: {table_name} missing species: {', '.join(sorted(missing)[:10])}")
            if len(missing) > 10:
                sys.stderr.write(f" ... and {len(missing) - 10} more")
            sys.stderr.write("\n")
            all_ok = False
    return all_ok


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate species.h from species_list.txt")
    parser.add_argument("--validate", action="store_true", help="Validate species-keyed tables and exit with error if any species is missing")
    parser.add_argument("--no-write", action="store_true", help="Only validate; do not write species.h")
    args = parser.parse_args()

    entries = load_species_list(SPECIES_LIST_PATH)
    if not args.no_write:
        generate_species_h(entries, SPECIES_H_PATH)
        print(f"Generated {SPECIES_H_PATH}")

    if args.validate:
        if not validate_tables(entries, REPO_ROOT):
            sys.exit(1)
        print("Validation passed.")


if __name__ == "__main__":
    main()
