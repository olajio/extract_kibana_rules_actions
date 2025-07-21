import json
import csv

# Input and output files are hardcoded
INPUT_FILE = 'response.json'
OUTPUT_FILE = 'rules_actions.csv'

def extract_rules_to_csv():
    # 1. Load the JSON response from Kibana API
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)  # May throw if response.json isn't valid
    
    # 2. Get the list of rules
    rules = data.get("data", [])
    if not isinstance(rules, list):
        print("ERROR: 'data' field is missing or not a list.")
        return
    
    # 3. Open CSV for writing
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "actions"])  # Header
        
        # 4. Iterate over each rule entry
        for entry in rules:
            # Safely extract nested fields
            attrs = entry.get("alert", {}).get("attributes", {})
            name = attrs.get("name", "")
            actions = attrs.get("actions", [])
            
            # Convert actions list to a JSON string for storage in CSV
            actions_str = json.dumps(actions, ensure_ascii=False)
            
            writer.writerow([name, actions_str])
    
    print(f"✅ Successfully wrote {len(rules)} rules to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    extract_rules_to_csv()
