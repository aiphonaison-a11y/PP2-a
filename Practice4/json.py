import json


# 1. Convert Python to JSON

data = {
    "name": "Ali",
    "age": 17,
    "subjects": ["Math", "ICT", "Physics"]
}

json_string = json.dumps(data, indent=4)
print("Python to JSON:")
print(json_string)



# 2. Convert JSON to Python

parsed_data = json.loads(json_string)
print("\nJSON to Python:")
print(parsed_data["name"])



# 3. Write JSON to File

with open("output.json", "w") as file:
    json.dump(data, file, indent=4)

print("\nData written to output.json")



# 4. Read JSON from File

with open("output.json", "r") as file:
    loaded_data = json.load(file)

print("Loaded from file:", loaded_data)