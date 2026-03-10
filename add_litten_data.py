#!/usr/bin/env python3
"""
Add minimal required data for Litten to compile pokeemerald successfully
This follows the exact steps from the official guide
"""

import re
import os

def get_status():
    """Check current status"""
    print("🔍 Checking current integration status...")
    
    # Check if Litten exists in constants
    with open("include/constants/species.h", "r") as f:
        species_content = f.read()
    
    if "SPECIES_LITTEN" in species_content:
        print("✅ SPECIES_LITTEN found in constants")
    else:
        print("❌ SPECIES_LITTEN not found in constants")
        return False
    
    # Check species names
    with open("src/data/text/species_names.h", "r") as f:
        names_content = f.read()
    
    if "SPECIES_LITTEN" in names_content:
        print("✅ SPECIES_LITTEN found in species names")
    else:
        print("❌ SPECIES_LITTEN not found in species names")
        return False
    
    return True

def add_basic_data_entries():
    """Add basic data entries to prevent compilation errors"""
    print("📝 Adding basic data entries for compilation...")
    
    # 1. Add to Pokédex entries (basic entry)
    pokedex_file = "src/data/pokemon/pokedex_entries.h"
    if os.path.exists(pokedex_file):
        print("   Adding Pokédex entry...")
        with open(pokedex_file, "r") as f:
            content = f.read()
        
        # Add after BLAZIKEN if not exists
        if "[SPECIES_LITTEN]" not in content:
            pattern = r"(\[SPECIES_BLAZIKEN\]\s*=\s*\{[^}]+\},)"
            replacement = rf"""\1
    [SPECIES_LITTEN] = {{
        .categoryName = _("Fire Cat"),
        .height = 4,
        .weight = 43,
        .description = gDexLittenDescription,
        .pokemonScale = 491,
        .pokemonOffset = 12,
        .trainerScale = 256,
        .trainerOffset = 0,
    }},"""
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open(pokedex_file, "w") as f:
                f.write(content)
            print("   ✅ Added Pokédex entry")
    
    # 2. Add Pokédex description
    pokedex_text_file = "src/data/pokemon/pokedex_text.h"
    if os.path.exists(pokedex_text_file):
        print("   Adding Pokédex description...")
        with open(pokedex_text_file, "r") as f:
            content = f.read()
        
        if "gDexLittenDescription" not in content:
            # Add after another description
            pattern = r"(const u8 gDexTorchicDescription\[\] = _\([^;]+;\n)"
            replacement = rf"""\1
const u8 gDexLittenDescription[] = _("A Fire-type Pokémon that is known for its playful nature.");

"""
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open(pokedex_text_file, "w") as f:
                f.write(content)
            print("   ✅ Added Pokédex description")
    
    # 3. Add basic species info
    species_info_file = "src/data/pokemon/species_info.h"
    if os.path.exists(species_info_file):
        print("   Adding species info...")
        with open(species_info_file, "r") as f:
            content = f.read()
        
        if "[SPECIES_LITTEN]" not in content:
            pattern = r"(\[SPECIES_BLAZIKEN\]\s*=\s*\{[^}]+\},)"
            replacement = rf"""\1
    [SPECIES_LITTEN] = {{
        .baseHP        = 45,
        .baseAttack    = 65,
        .baseDefense   = 40,
        .baseSpeed     = 70,
        .baseSpAttack  = 60,
        .baseSpDefense = 40,
        .types = {{ TYPE_FIRE, TYPE_FIRE }},
        .catchRate = 45,
        .expYield = 62,
        .evYield_Speed = 1,
        .genderRatio = PERCENT_FEMALE(12.5),
        .eggCycles = 20,
        .friendship = STANDARD_FRIENDSHIP,
        .growthRate = GROWTH_MEDIUM_SLOW,
        .eggGroups = {{ EGG_GROUP_FIELD, EGG_GROUP_FIELD }},
        .abilities = {{ ABILITY_BLAZE, ABILITY_NONE, ABILITY_INTIMIDATE }},
        .bodyColor = BODY_COLOR_RED,
        .speciesName = _("Litten"),
        .cryId = CRY_LITTEN,
        .natDexNum = NATIONAL_DEX_LITTEN,
        .categoryName = _("Fire Cat"),
        .height = 4,
        .weight = 43,
        .description = COMPOUND_STRING("A Fire-type Pokémon that is known\\n"
                                      "for its playful nature."),
        .pokemonScale = 491,
        .pokemonOffset = 12,
        .trainerScale = 256,
        .trainerOffset = 0,
        FRONT_PIC(Litten, 64, 64),
        .frontPicYOffset = 10,
        .backPic = gMonBackPic_Litten,
        .backPicSize = MON_COORDS_SIZE(64, 64),
        .backPicYOffset = 6,
        .palette = gMonPalette_Litten,
        .shinyPalette = gMonShinyPalette_Litten,
        .iconSprite = gMonIcon_Litten,
        .iconPalIndex = 0,
        FOOTPRINT(Litten)
        OVERWORLD(
            gObjectEventPic_Litten,
            SIZE_32x32,
            SHADOW_SIZE_M,
            TRACKS_FOOT,
            gOverworldPalette_Litten,
            gShinyOverworldPalette_Litten
        )
        .levelUpLearnset = sLittenLevelUpLearnset,
        .teachableLearnset = sLittenTeachableLearnset,
    }},"""
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            with open(species_info_file, "w") as f:
                f.write(content)
            print("   ✅ Added species info")

def main():
    """Main function"""
    print("🔥 Setting up minimal Litten data for compilation...")
    
    if not get_status():
        print("❌ Prerequisites not met - run the basic Litten addition first")
        return False
    
    add_basic_data_entries()
    
    print("\n✅ Minimal Litten data added!")
    print("📝 Note: This adds basic compilation support.")
    print("   Full integration requires more data entries.")
    print("   Try compiling with: make")
    
    return True

if __name__ == "__main__":
    main()
