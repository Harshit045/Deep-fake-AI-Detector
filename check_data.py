import os

base_dir = "dataset/deepfake"
real_dir = os.path.join(base_dir, "real")
fake_dir = os.path.join(base_dir, "fake")

print(f"Checking project structure from: {os.getcwd()}")
print("-" * 20)

if not os.path.isdir(base_dir):
    print(f"ERROR: The main data directory '{base_dir}' does not exist.")
    exit()
else:
    print(f"OK: Found main data directory '{base_dir}'.")

if not os.path.isdir(real_dir):
    print(f"ERROR: The 'real' subdirectory '{real_dir}' does not exist.")
else:
    print(f"OK: Found 'real' subdirectory '{real_dir}'.")
    real_files = os.listdir(real_dir)
    if not real_files:
        print("  -> WARNING: The 'real' directory is empty.")
    else:
        print(f"  -> Found {len(real_files)} files in '{real_dir}'. First 5: {real_files[:5]}")

if not os.path.isdir(fake_dir):
    print(f"ERROR: The 'fake' subdirectory '{fake_dir}' does not exist.")
else:
    print(f"OK: Found 'fake' subdirectory '{fake_dir}'.")
    fake_files = os.listdir(fake_dir)
    if not fake_files:
        print("  -> WARNING: The 'fake' directory is empty.")
    else:
        print(f"  -> Found {len(fake_files)} files in '{fake_dir}'. First 5: {fake_files[:5]}")

print("-" * 20)
print("If you see 'WARNING: ... directory is empty', you need to place your image files into those folders.")
print("If you see 'ERROR: ... does not exist', you need to create the folder structure.")