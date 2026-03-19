# Read full file
with open("sample.txt", "r") as f:
    print(f.read())

# Read one line
with open("sample.txt", "r") as f:
    print(f.readline())

# Read all lines as list
with open("sample.txt", "r") as f:
    lines = f.readlines()
    print(lines)

# Loop through file
with open("sample.txt", "r") as f:
    for line in f:
        print(line.strip())