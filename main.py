import threading
import time
import os
from pathlib import Path

# Import the modules
from modules.dir_monitor import DirectoryMonitor
from modules.sys_monitor import SystemMonitor

# Configuration
WATCH_DIR = "./monitored_folder"
LOG_DIR = "./logs"

def setup_environment():
    """Creates necessary folders."""
    Path(WATCH_DIR).mkdir(exist_ok=True)
    Path(LOG_DIR).mkdir(exist_ok=True)

def main():
    print("=== Linux Monitoring System (AAC6164) ===")
    setup_environment()

    # Create instances
    # CRITICAL FIX: Ensure this points to .csv, not .txt
    dir_mon = DirectoryMonitor(
        target_dir=WATCH_DIR, 
        log_file=f"{LOG_DIR}/dir_events.csv" 
    )
    
    sys_mon = SystemMonitor(
        log_file=f"{LOG_DIR}/sys_metrics.csv"
    )

    # Run in threads
    t1 = threading.Thread(target=dir_mon.run, args=(2,), daemon=True)
    t2 = threading.Thread(target=sys_mon.run, args=(10,), daemon=True)

    print("Starting threads... Press Ctrl+C to stop.")
    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping System...")
        print("Logs saved. Now run 'python3 generate_report.py' to see results.")

if __name__ == "__main__":
    main()
