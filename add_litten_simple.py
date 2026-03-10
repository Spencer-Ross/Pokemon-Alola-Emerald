#!/usr/bin/env python3
"""
Simple Pokémon addition script for pokeemerald ROM hack
"""

import re
import argparse
import os
import sys

def add_litten():
    """Add Litten specifically after SPECIES_BLAZIKEN"""
    print("🔥 Adding Litten to pokeemerald...")
    
    # Step 1: Add species constant
    print("Adding species constant...")
    with open("include/constants/species.h", "r") as f:
        content = f.read()
    
    # Find SPECIES_BLAZIKEN and get its number
    blaziken_match = re.search(r"#define SPECIES_BLAZIKEN\s+(\d+)", content)
    if not blaziken_match:
        print("❌ Could not find SPECIES_BLAZIKEN")
        return False
    
    litten_number = int(blaziken_match.group(1)) + 1
    
    # Add SPECIES_LITTEN after BLAZIKEN
    pattern = r"(#define SPECIES_BLAZIKEN\s+\d+)"
    replacement = rf"\1\n#define SPECIES_LITTEN             {litten_number}"
    content = re.sub(pattern, replacement, content)
    
    with open("include/constants/species.h", "w") as f:
        f.write(content)
    
    # Step 2: Increment SPECIES_COUNT
    print("Incrementing SPECIES_COUNT...")
    with open("include/constants/species.h", "r") as f:
        content = f.read()
    
    count_pattern = r"(#define SPECIES_COUNT\s+)(\d+)"
    match = re.search(count_pattern, content)
    if match:
        current_count = int(match.group(2))
        new_count = current_count + 1
        content = re.sub(count_pattern, rf"\g<1>{new_count}", content)
        
        with open("include/constants/species.h", "w") as f:
            f.write(content)
    
    # Step 3: Add species name
    print("Adding species name...")
    with open("src/data/text/species_names.h", "r") as f:
        content = f.read()
    
    pattern = r"(\[SPECIES_BLAZIKEN\]\s*=\s*_\([^)]+\),)"
    replacement = r'\1\n    [SPECIES_LITTEN] = _("LITTEN"),'
    content = re.sub(pattern, replacement, content)
    
    with open("src/data/text/species_names.h", "w") as f:
        f.write(content)
    
    print("✅ Successfully added Litten!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Add Litten to pokeemerald ROM hack")
    parser.add_argument("pokemon_name", help="Name of the Pokémon to add (only Litten supported)")
    parser.add_argument("--after", required=True, help="Species constant to add after")
    
    args = parser.parse_args()
    
    if args.pokemon_name.lower() != "litten":
        print("❌ This simple script only supports adding Litten")
        print("   Usage: python3 add_pokemon.py Litten --after SPECIES_BLAZIKEN")
        sys.exit(1)
    
    if args.after != "SPECIES_BLAZIKEN":
        print("❌ This simple script only supports adding after SPECIES_BLAZIKEN")
        sys.exit(1)
    
    # Validate we're in a pokeemerald directory
    if not os.path.exists("include/constants/species.h"):
        print("❌ Error: This doesn't appear to be a pokeemerald repository")
        print("   Make sure you're in the root directory of pokeemerald")
        sys.exit(1)
    
    success = add_litten()
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
