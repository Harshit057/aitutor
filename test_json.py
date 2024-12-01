import json

try:
    with open("data/content.json") as f:
        knowledge_base = json.load(f)
        print("JSON file loaded successfully!")
        print(knowledge_base)
except FileNotFoundError:
    print("Error: The file 'data/content.json' was not found.")
except json.JSONDecodeError:
    print("Error: There was a problem decoding the JSON file.")
