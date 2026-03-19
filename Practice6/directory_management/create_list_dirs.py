import os

# Create single directory
os.mkdir("test_dir")

# Create nested directories
os.makedirs("parent/child/grandchild", exist_ok=True)

# List directory contents
print(os.listdir("."))

# Get current directory
print(os.getcwd())