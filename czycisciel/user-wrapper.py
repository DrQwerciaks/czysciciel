#!/usr/bin/env python3
# user-wrapper.py - Wrapper dla GUI użytkownika

import os
import sys
import subprocess
import tkinter as tk
from pathlib import Path

def check_user_permissions():
    """Sprawdza i konfiguruje uprawnienia użytkownika"""
    
    # Sprawdź czy GUI działa jako user (nie root)
    if os.getuid() == 0:
        print("⚠️  UWAGA: GUI nie powinno działać jako root!")
        print("Uruchom jako zwykły użytkownik: inv-cleaner")
        return False
    
    # Utwórz katalogi użytkownika
    user_config_dir = Path.home() / ".config" / "inv-cleaner"
    user_config_dir.mkdir(parents=True, exist_ok=True)
    
    # Skopiuj przykładową konfigurację jeśli nie istnieje
    user_config = user_config_dir / "config.json"
    if not user_config.exists():
        try:
            # Spróbuj skopiować z snap
            snap_config = Path(os.environ.get('SNAP', '/')) / "etc" / "inv-cleaner" / "config-example.json"
            if snap_config.exists():
                import shutil
                shutil.copy(snap_config, user_config)
                print(f"✅ Skopiowano konfigurację do {user_config}")
        except Exception as e:
            print(f"ℹ️  Nie udało się skopiować konfiguracji: {e}")
    
    return True

def main():
    """Uruchom GUI jako user"""
    if not check_user_permissions():
        sys.exit(1)
    
    # Uruchom główną aplikację
    sys.path.insert(0, os.path.dirname(__file__))
    import main
    main.main()

if __name__ == "__main__":
    main()
