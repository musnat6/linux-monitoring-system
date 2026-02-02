import os
import time
import stat
import csv
from pathlib import Path

class DirectoryMonitor:
    def __init__(self, target_dir, log_file):
        self.target_dir = Path(target_dir)
        self.log_file = Path(log_file)
        self.previous_snapshot = {}
        
        # Ensure log directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize CSV with Headers if file is new
        if not self.log_file.exists():
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Event_Type", "Filename", "Metadata"])

    def get_snapshot(self):
        """Scans the directory."""
        snapshot = {}
        if not self.target_dir.exists():
            self.target_dir.mkdir(parents=True, exist_ok=True)
        try:
            for entry in os.scandir(self.target_dir):
                if entry.is_file():
                    snapshot[entry.name] = (entry.stat().st_mtime, entry.stat().st_size)
        except OSError:
            pass
        return snapshot

    def get_metadata(self, filename):
        """Extracts required metadata [cite: 34-39]."""
        filepath = self.target_dir / filename
        try:
            file_stat = filepath.stat()
            # Simplified metadata string for CSV readability
            return f"Size:{file_stat.st_size}B | Perms:{stat.filemode(file_stat.st_mode)}"
        except FileNotFoundError:
            return "File Deleted"

    def log_event(self, event_type, filename, metadata):
        """Logs to CSV and prints to terminal."""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 1. Print to Terminal (Requirement: Visual Execution)
        print(f"[{timestamp}] [DIR_MONITOR] {event_type}: {filename}")

        # 2. Write to CSV (Requirement: Structured Logs)
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, event_type, filename, metadata])

    def run(self, interval=2):
        self.previous_snapshot = self.get_snapshot()
        print(f"--> Directory Monitor Active. Watching: {self.target_dir}")
        
        while True:
            time.sleep(interval)
            current_snapshot = self.get_snapshot()
            
            prev_keys = set(self.previous_snapshot.keys())
            curr_keys = set(current_snapshot.keys())

            # Detect Changes
            for file in curr_keys - prev_keys:
                self.log_event("CREATED", file, self.get_metadata(file))

            for file in prev_keys - curr_keys:
                self.log_event("DELETED", file, "N/A")

            for file in curr_keys & prev_keys:
                if self.previous_snapshot[file] != current_snapshot[file]:
                    self.log_event("MODIFIED", file, self.get_metadata(file))

            self.previous_snapshot = current_snapshot
