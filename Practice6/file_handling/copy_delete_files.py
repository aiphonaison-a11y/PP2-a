import shutil
import os

# Copy file
shutil.copy("sample.txt", "copy_sample.txt")

# Copy with metadata
shutil.copy2("sample.txt", "copy_with_meta.txt")

# Delete file safely
if os.path.exists("copy_sample.txt"):
    os.remove("copy_sample.txt")

# Rename file
if os.path.exists("copy_with_meta.txt"):
    os.rename("copy_with_meta.txt", "renamed.txt")