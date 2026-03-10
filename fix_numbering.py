#!/usr/bin/env python3
"""
Fix species numbering after adding Litten
"""

import re

def fix_species_numbering():
    """Fix the species numbering after SPECIES_LITTEN"""
    print("🔧 Fixing species numbering...")
    
    with open("include/constants/species.h", "r") as f:
        lines = f.readlines()
    
    # Find where SPECIES_LITTEN is and fix numbering from there
    litten_found = False
    current_number = 283  # LITTEN's number
    
    for i, line in enumerate(lines):
        if "SPECIES_LITTEN" in line:
            litten_found = True
            current_number = 284  # Next number after LITTEN
            continue
        
        if litten_found and line.strip().startswith("#define SPECIES_"):
            # Extract the species name
            match = re.match(r"#define (SPECIES_\w+)\s+\d+", line.strip())
            if match:
                species_name = match.group(1)
                lines[i] = f"#define {species_name} {current_number}\n"
                current_number += 1
    
    with open("include/constants/species.h", "w") as f:
        f.writelines(lines)
    
    print(f"✅ Fixed species numbering up to {current_number - 1}")

if __name__ == "__main__":
    fix_species_numbering()
