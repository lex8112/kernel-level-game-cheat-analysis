import csv
import sys
import os

# TODO: Add multiprocessing for handling files larger than 1GB.
# TODO: Implement stricter linting rules (PEP8) before CI/CD pipeline integration.

def analyze_procmon_csv(file_path):
    """
    Procmon tarafından dışa aktarılan CSV loglarını okur ve oyunun (Target PID)
    Kernel seviyesinde yaptığı şüpheli dosya ve kayıt defteri (Registry) işlemlerini filtreler.
    """
    print(f"[*] Analyzing Procmon dump: {file_path}")
    
    suspicious_events = []
    
    try:
        with open(file_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Sadece TCP bağlantıları veya Registry değişikliklerine odaklan
                if "RegSetValue" in row.get("Operation", "") or "TCP" in row.get("Operation", ""):
                    suspicious_events.append(row)
                    
        print(f"[+] Found {len(suspicious_events)} interesting kernel/network events.")
        # TODO: Send these events to Elasticsearch or save as JSON for further YARA scanning.
        
    except FileNotFoundError:
        print("[-] ERROR: Dump file not found. Ensure Procmon is running and exporting correctly.")

if __name__ == "__main__":
    # Simüle edilmiş log yolu
    target_log = "../logs/game_procmon_dump.csv"
    if os.path.exists(target_log):
        analyze_procmon_csv(target_log)
    else:
        print("[!] Waiting for live Procmon data injection...")
