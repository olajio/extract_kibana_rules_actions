import json
import csv
import sys

def extract_rules_to_csv(input_json, output_csv):
    # 1. Load JSON file
    with open(input_json, 'r') as f:
        data = json.load(f)

    # 2. Safely navigate into the "data" list
    rules = data.get("data", [])
    if not rules:
        print("No 'data' array found in JSON.")
        return

    # 3. Prepare CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "actions"])

        # 4. Iterate through rules
        for entry in rules:
            alert = entry.get("alert", {})
            attrs = alert.get("attributes", {})
            name = attrs.get("name", "")

            # 5. Extract actions, serialize as JSON string
            actions_list = attrs.get("actions", [])
            actions_str = json.dumps(actions_list, ensure_ascii=False)

            writer.writerow([name, actions_str])

    print(f"✅ Extracted {len(rules)} rules to '{output_csv}'")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_rules.py <input.json> <output.csv>")
        sys.exit(1)

    extract_rules_to_csv(sys.argv[1], sys.argv[2])
