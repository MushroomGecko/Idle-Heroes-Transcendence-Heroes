import csv
import json

"""
This script is used to convert the CSV file to JSON format.
"""

def parse_skill_or_passive(skill_text):
    """Parse skill/passive text with tilde separators into structured format"""
    if not skill_text or skill_text.strip() == "":
        return None
    
    # Strip the input text first
    skill_text = skill_text.strip()
    parts = skill_text.split('~')
    
    if len(parts) < 2:
        return {"raw": skill_text.strip()}
    
    # Remove empty parts and strip whitespace
    parts = [part.strip() for part in parts if part.strip()]
    
    if len(parts) < 4:
        return {"raw": skill_text.strip()}
    
    def clean_sublimation_text(text):
        """Remove sublimation type prefix from text"""
        text = text.strip()
        if "Pure Sublimation:" in text:
            return text.split("Pure Sublimation:", 1)[1].strip()
        elif "Deep Sublimation:" in text:
            return text.split("Deep Sublimation:", 1)[1].strip()
        elif "Noble Sublimation:" in text:
            return text.split("Noble Sublimation:", 1)[1].strip()
        return text.strip()
    
    result = {
        "name": parts[0].strip(),
        "main_effect": parts[1].strip(),
        "sublimations": {
            "pure": clean_sublimation_text(parts[2]) if len(parts) > 2 else "",
            "deep": clean_sublimation_text(parts[3]) if len(parts) > 3 else "",
            "noble": clean_sublimation_text(parts[4]) if len(parts) > 4 else ""
        }
    }
    
    return result

def parse_spiritual_pivot(pivot_text):
    """Parse spiritual pivot text with tilde separators into options"""
    if not pivot_text or pivot_text.strip() == "":
        return []
    
    # Strip the input text first
    pivot_text = pivot_text.strip()
    parts = pivot_text.split('~')
    # Remove empty parts and strip whitespace
    options = [part.strip() for part in parts if part.strip()]
    
    return options

def convert_csv_to_json(csv_file_path, json_file_path):
    """Convert CSV file to JSON format according to specifications"""
    heroes = []
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            hero = {
                "hero": row["Hero"].strip(),
                "class": row["Class"].strip(),
                "hp": row["HP"].strip(),
                "attack": row["Attack"].strip(),
                "armor": row["Armor"].strip(),
                "speed": row["Speed"].strip(),
                "active_skill": parse_skill_or_passive(row["Active Skill"]),
                "passive_1": parse_skill_or_passive(row["Passive 1"]),
                "passive_2": parse_skill_or_passive(row["Passive 2"]),
                "passive_3": parse_skill_or_passive(row["Passive 3"]),
                "core_of_origin": row["Core of Origin"].strip(),
                "transition_skill": row["Transition Skill"].strip(),
                "spiritual_pivots": {
                    "phantom_dawn": parse_spiritual_pivot(row["Spiritual Pivot 1 - Phantom Dawn (Pick 1)"]),
                    "glowed_glory": parse_spiritual_pivot(row["Spiritual Pivot 2 - Glowed Glory (Pick 1)"]),
                    "acheron_barque": parse_spiritual_pivot(row["Spiritual Pivot 3 - Acheron Barque (Pick 1)"]),
                    "comet_hop": parse_spiritual_pivot(row["Spiritual Pivot 4 - Comet Hop (Pick 1)"]),
                    "sun_halo": parse_spiritual_pivot(row["Spiritual Pivot 5 - Sun Halo (Pick 1)"]),
                    "moon_abyss": parse_spiritual_pivot(row["Spiritual Pivot 6 - Moon Abyss (Pick 1)"])
                }
            }
            heroes.append(hero)
    
    # Write to JSON file
    with open(json_file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(heroes, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Successfully converted {len(heroes)} heroes from CSV to JSON format.")
    print(f"Output saved to: {json_file_path}")

if __name__ == "__main__":
    # Convert the CSV file to JSON
    csv_file = "Idle Heroes Transcendence Heroes.csv"
    json_file = "Idle Heroes Transcendence Heroes.json"
    
    try:
        convert_csv_to_json(csv_file, json_file)
        
        # Display a sample of the converted data
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"\nSample of converted data (first hero):")
            print(json.dumps(data[0], indent=2, ensure_ascii=False))
            
    except FileNotFoundError:
        print(f"Error: Could not find the CSV file '{csv_file}'")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
