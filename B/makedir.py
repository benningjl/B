import os

# Define the root directory for the GHNet project
root_dir = "F:/A"  # You can change this path as needed

# Define the directory structure based on the pyramid design
directories = [
    "core",
    "core/governance",
    "core/resource_allocation",
    "ui",
    "utils",
    "tests",
    "docs",
]

# Create directories
def create_directories(base_path, dirs):
    for dir_path in dirs:
        full_path = os.path.join(base_path, dir_path)
        try:
            os.makedirs(full_path, exist_ok=True)
            print(f"Created directory: {full_path}")
        except Exception as e:
            print(f"Error creating directory {full_path}: {e}")

# Create the root directory first
if not os.path.exists(root_dir):
    os.makedirs(root_dir)
    print(f"Created root directory: {root_dir}")

# Create the rest of the directory structure
create_directories(root_dir, directories)

# Example of creating initial placeholder files in the 'docs' folder
files_to_create = [
    ("docs/README.md", "# GHNet\n\nGlobal Harmony Network - Decentralized, AI-powered platform."),
    ("docs/ARCHITECTURE.md", "# Architecture\n\nDetailed architecture of GHNet platform."),
]

# Create initial files
for file_path, content in files_to_create:
    full_file_path = os.path.join(root_dir, file_path)
    try:
        with open(full_file_path, "w") as file:
            file.write(content)
        print(f"Created file: {full_file_path}")
    except Exception as e:
        print(f"Error creating file {full_file_path}: {e}")

print("Directory structure setup complete!")
