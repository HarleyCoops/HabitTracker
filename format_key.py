import json

# Read the key.json file
with open('key.json', 'r') as f:
    key_data = json.load(f)

# Write the formatted JSON to a new file
with open('formatted_key.json', 'w') as f:
    json.dump(key_data, f)

print("Formatted key has been written to 'formatted_key.json'")
print("Please open this file, copy its ENTIRE contents, and use that for your GitHub secret.")
