import csv
from pathlib import Path
import time

# Define Paths relative to this module
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
SYS_LOG = LOG_DIR / "sys_metrics.csv"
DIR_LOG = LOG_DIR / "dir_events.csv"
OUTPUT_REPORT = BASE_DIR / "reports" / "final_summary.txt"

def generate_report():
    print("\n[Processing] Formatting Final Report...")
    
    # --- 1. System Metrics Analysis ---
    cpu, ram, procs = [], [], []
    if SYS_LOG.exists():
        with open(SYS_LOG, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cpu.append(float(row['CPU_Usage(%)']))
                    ram.append(float(row['RAM_Used(%)']))
                    procs.append(int(row['Process_Count']))
                except (ValueError, KeyError): continue

    total_checks = len(cpu)
    avg_cpu = sum(cpu)/total_checks if total_checks else 0
    avg_ram = sum(ram)/total_checks if total_checks else 0
    max_proc = max(procs) if procs else 0

    # --- 2. Directory Events Analysis ---
    created, deleted, modified = 0, 0, 0
    if DIR_LOG.exists():
        with open(DIR_LOG, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                evt = row.get("Event_Type", "").strip().upper()
                if evt == "CREATED": created += 1
                elif evt == "DELETED": deleted += 1
                elif evt == "MODIFIED": modified += 1

    total_events = created + deleted + modified
    gen_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # --- 3. Generate "Beautified" Report Text ---
    report_content = f"""
======================================================================
               AAC6164 - LINUX MONITORING SYSTEM REPORT               
======================================================================
Generated On: {gen_time}
Status      : SUCCESS
----------------------------------------------------------------------

[1] SYSTEM PERFORMANCE METRICS
=========================================
Total Observations      : {total_checks}
-----------------------------------------
| Metric                | Average       | Status        |
|-----------------------|---------------|---------------|
| CPU Usage             | {avg_cpu:>5.2f} %       | {'OK' if avg_cpu < 80 else 'HIGH'}          |
| RAM Usage             | {avg_ram:>5.2f} %       | {'OK' if avg_ram < 90 else 'HIGH'}          |
| Peak Process Count    | {max_proc:<5}         | Normal        |
=========================================

[2] DIRECTORY SECURITY LOG
=========================================
Monitored Events Detected: {total_events}
-----------------------------------------
| Event Type            | Count         |
|-----------------------|---------------|
| [+] Files Created     | {created:<5}         |
| [-] Files Deleted     | {deleted:<5}         |
| [~] Files Modified    | {modified:<5}         |
=========================================

[3] AUTOMATED ANALYSIS
-----------------------------------------
The system has successfully monitored the target directory and 
performance metrics. Use the attached CSV logs for granular detail.
======================================================================
"""
    
    # Ensure reports folder exists
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to file
    with open(OUTPUT_REPORT, "w") as f:
        f.write(report_content)
    
    print(f"[Success] Professional report generated.")
    print(f"[Output] Saved to: {OUTPUT_REPORT}")
    print(report_content)

if __name__ == "__main__":
    generate_report()

