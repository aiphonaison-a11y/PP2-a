# Write (overwrite)
with open("sample.txt", "w") as f:
    f.write("Hello\n")

# Write multiple lines
with open("sample.txt", "w") as f:
    f.write("Line 1\nLine 2\n")

# Append
with open("sample.txt", "a") as f:
    f.write("Appended line\n")

# Create file if not exists (x mode)
try:
    with open("newfile.txt", "x") as f:
        f.write("Created safely")
except FileExistsError:
    print("File already exists")