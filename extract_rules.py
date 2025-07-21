import json
import csv

def extract_rules_to_csv(input_file, output_csv):
    # Read the JSON response file
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Ensure expected structure
    # Assuming each rule is under data['data'] or 'results'—adjust if different
    rules = data.get('data') or data.get('results') or data.get('rules') or []

    # Prepare output
    rows = []
    for rule in rules:
        # Navigate into saved object structure: adjust based on actual structure
        attrs = rule.get('alert', {}).get('attributes') if 'alert' in rule else rule.get('attributes')
        if not attrs:
            continue

        name = attrs.get('name', '')
        # Actions might be under attrs['actions']—adjust path if different
        actions = attrs.get('actions', [])
        # Store as JSON string to preserve structure
        actions_str = json.dumps(actions)

        rows.append({'name': name, 'actions': actions_str})

    # Write CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'actions'])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == '__main__':
    extract_rules_to_csv('response.json', 'rules_actions.csv')
    print("✅ Exported rule names and actions to rules_actions.csv")
