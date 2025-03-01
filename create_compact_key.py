import json

# Read the key.json file
with open('key.json', 'r') as f:
    key_data = json.load(f)

# Write the compact JSON to a new file
with open('github_secret.txt', 'w') as f:
    json.dump(key_data, f, separators=(',', ':'))

print("Compact JSON has been written to 'github_secret.txt'")
print("Please open this file, copy its ENTIRE contents, and use that for your GitHub secret.")
