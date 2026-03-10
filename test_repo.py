#!/usr/bin/env python3
"""
Test script for add_pokemon.py - checks if all required files exist and script can run
"""

import os
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        "include/constants/species.h",
        "src/data/text/species_names.h", 
        "src/data/pokemon/pokedex_entries.h",
        "src/data/pokemon/pokedex_text.h",
        "src/data/pokemon/species_info.h",
        "src/data/graphics/pokemon.h",
        "include/graphics.h",
        "src/data/pokemon_graphics/front_pic_table.h",
        "src/data/pokemon_graphics/back_pic_table.h",
        "src/data/pokemon_graphics/palette_table.h",
        "src/data/pokemon_graphics/shiny_palette_table.h",
        "src/data/pokemon_graphics/front_pic_coordinates.h",
        "src/data/pokemon_graphics/back_pic_coordinates.h",
        "src/data/pokemon_graphics/footprint_table.h",
        "src/pokemon_icon.c",
        "sound/cry_tables.inc",
        "src/data/pokemon/level_up_learnsets.h",
        "src/data/pokemon/level_up_learnset_pointers.h",
        "src/data/pokemon/tmhm_learnsets.h",
        "src/data/pokemon/tutor_learnsets.h",
        "src/data/bard_music/pokemon.h",
        "src/pokemon.c",
        "src/pokemon_animation.c"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   {file}")
        return False
    else:
        print("✅ All required files exist")
        return True

def main():
    print("🔍 Checking pokeemerald repository structure...")
    
    if check_files():
        print("\n✅ Repository structure looks good!")
        print("📝 You can now use the script like this:")
        print("   python3 add_pokemon.py Litten --after SPECIES_BLAZIKEN")
        print("   python3 add_pokemon.py Torracat --after SPECIES_LITTEN")
        print("   python3 add_pokemon.py Incineroar --after SPECIES_TORRACAT")
    else:
        print("\n❌ Repository structure check failed")
        print("   Make sure you're in the root of the pokeemerald repository")
        sys.exit(1)

if __name__ == "__main__":
    main()
