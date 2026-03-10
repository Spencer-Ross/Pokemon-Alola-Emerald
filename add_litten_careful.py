#!/usr/bin/env python3
"""
Careful Litten addition script for pokeemerald ROM hack
"""

import re

def add_litten_carefully():
    """Add Litten after SPECIES_BLAZIKEN with careful numbering"""
    print("🔥 Adding Litten carefully...")
    
    with open("include/constants/species.h", "r") as f:
        content = f.read()
    
    # Find SPECIES_BLAZIKEN and its number
    blaziken_match = re.search(r"#define SPECIES_BLAZIKEN\s+(\d+)", content)
    if not blaziken_match:
        print("❌ Could not find SPECIES_BLAZIKEN")
        return False
    
    blaziken_number = int(blaziken_match.group(1))
    litten_number = blaziken_number + 1
    
    print(f"📍 SPECIES_BLAZIKEN is at {blaziken_number}")
    print(f"📍 SPECIES_LITTEN will be at {litten_number}")
    
    # Step 1: Add SPECIES_LITTEN right after SPECIES_BLAZIKEN
    pattern = r"(#define SPECIES_BLAZIKEN\s+\d+\n)"
    replacement = rf"\1#define SPECIES_LITTEN             {litten_number}\n"
    content = re.sub(pattern, replacement, content)
    
    # Step 2: Update all species numbers after LITTEN
    lines = content.split('\n')
    updated_lines = []
    found_litten = False
    current_number = litten_number + 1
    
    for line in lines:
        if "SPECIES_LITTEN" in line:
            found_litten = True
            updated_lines.append(line)
            continue
            
        if found_litten and line.strip().startswith("#define SPECIES_") and "SPECIES_EGG" not in line and "SPECIES_UNOWN" not in line:
            # Extract species name
            match = re.match(r"#define (SPECIES_\w+)\s+\d+", line.strip())
            if match:
                species_name = match.group(1)
                # Skip if it's already been processed or is a special case
                if species_name not in ["SPECIES_LITTEN"]:
                    updated_lines.append(f"#define {species_name} {current_number}")
                    current_number += 1
                    continue
        
        updated_lines.append(line)
    
    # Step 3: Update SPECIES_EGG to be current_number
    content = '\n'.join(updated_lines)
    content = re.sub(r"#define SPECIES_EGG \d+", f"#define SPECIES_EGG {current_number}", content)
    
    print(f"📍 SPECIES_EGG updated to {current_number}")
    
    with open("include/constants/species.h", "w") as f:
        f.write(content)
    
    print("✅ Successfully added Litten with proper numbering!")
    return True

def add_litten_to_species_names():
    """Add Litten to species names"""
    print("📝 Adding Litten to species names...")
    
    with open("src/data/text/species_names.h", "r") as f:
        content = f.read()
    
    # Add after BLAZIKEN
    pattern = r"(\[SPECIES_BLAZIKEN\]\s*=\s*_\([^)]+\),)"
    replacement = r'\1\n    [SPECIES_LITTEN] = _("LITTEN"),'
    content = re.sub(pattern, replacement, content)
    
    with open("src/data/text/species_names.h", "w") as f:
        f.write(content)
    
    print("✅ Added Litten to species names!")

if __name__ == "__main__":
    if add_litten_carefully():
        add_litten_to_species_names()
        print("\n🎉 Litten added successfully!")
        print("📝 Remember: Graphics files should be in graphics/pokemon/litten/")
    else:
        print("❌ Failed to add Litten")
