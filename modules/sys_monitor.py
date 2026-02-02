import psutil
import time
import csv
from pathlib import Path

class SystemMonitor:
    def __init__(self, log_file):
        self.log_file = Path(log_file)
        # Initialize CSV headers if file doesn't exist
        if not self.log_file.exists():
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "CPU_Usage(%)", "RAM_Used(%)", "Disk_Free(GB)", "Process_Count"])

    def get_top_processes(self):
        """Finds top 3 processes by CPU usage[cite: 63]."""
        # Get list of processes sorted by CPU
        procs = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                       key=lambda p: p.info['cpu_percent'], 
                       reverse=True)[:3]
        
        return ", ".join([f"{p.info['name']}({p.info['cpu_percent']}%)" for p in procs])

    def run(self, interval=10):
        """Main loop for system monitoring."""
        print(f"--> System Performance Monitor Active. logging to {self.log_file}")
        
        while True:
            try:
                # 1. CPU Metrics [cite: 43]
                cpu_usage = psutil.cpu_percent(interval=1) # Measures over 1 second
                
                # 2. Memory Metrics [cite: 47]
                ram = psutil.virtual_memory()
                
                # 3. Disk Metrics [cite: 50]
                disk = psutil.disk_usage('/')
                
                # 4. Process Metrics [cite: 56]
                proc_count = len(psutil.pids())
                top_procs = self.get_top_processes()

                # Prepare data for logging
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                disk_free_gb = round(disk.free / (1024**3), 2)
                
                # Log to CSV
                with open(self.log_file, 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([timestamp, cpu_usage, ram.percent, disk_free_gb, proc_count])
                
                # Print summary to terminal (Requirement: Terminal Output)
                print(f"[{timestamp}] [SYS_MONITOR] CPU: {cpu_usage}% | RAM: {ram.percent}% | Top: {top_procs}")
                
                # Sleep for the remainder of the interval
                time.sleep(interval - 1) 
                
            except Exception as e:
                print(f"[Error] System Monitor: {e}")
