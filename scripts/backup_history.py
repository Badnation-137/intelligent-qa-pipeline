# scripts/backup_history.py

import os
import shutil
from datetime import datetime

def backup_history():
    """Backup folder history/ ke backup/"""
    
    if not os.path.exists("history"):
        print("❌ Folder 'history/' tidak ditemukan.")
        return

    # Buat folder backup
    backup_dir = f"backup/history_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copytree("history", backup_dir)

    print(f"✅ Backup berhasil: {backup_dir}")

if __name__ == "__main__":
    backup_history()