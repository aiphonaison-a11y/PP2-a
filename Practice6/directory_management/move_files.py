import shutil
import os

# Prepare file
with open("example.txt", "w") as f:
    f.write("Hello")

# Move file
shutil.move("example.txt", "test_dir/example.txt")

# Copy file to another directory
shutil.copy("test_dir/example.txt", "parent/example_copy.txt")

# Move and rename
shutil.move("test_dir/example.txt", "test_dir/renamed_example.txt")

# Find .txt files
txt_files = [f for f in os.listdir("test_dir") if f.endswith(".txt")]
print(txt_files)