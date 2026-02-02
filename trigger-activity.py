import os
import time
from pathlib import Path

# Must match the folder name in main.py
WATCH_DIR = Path("./monitored_folder")

def trigger_events():
    print(f"--- Starting Activity in {WATCH_DIR} ---")
    
    # Ensure folder exists
    WATCH_DIR.mkdir(exist_ok=True)
    
    # 1. Trigger CREATED
    file_path = WATCH_DIR / "evidence_for_assignment.txt"
    print(f"[Action] Creating file: {file_path.name}...")
    with open(file_path, "w") as f:
        f.write("Initial content.\n")
    
    time.sleep(3) # Wait for monitor to catch it

    # 2. Trigger MODIFIED
    print(f"[Action] Modifying file: {file_path.name}...")
    with open(file_path, "a") as f:
        f.write("Adding some new data to trigger modification logic.\n")
    
    time.sleep(3) # Wait for monitor to catch it

    # 3. Trigger DELETED
    print(f"[Action] Deleting file: {file_path.name}...")
    os.remove(file_path)
    
    print("--- Activity Complete. Check your logs now! ---")

if __name__ == "__main__":
    trigger_events()
