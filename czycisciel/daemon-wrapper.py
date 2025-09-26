#!/usr/bin/env python3
# daemon-wrapper.py - Wrapper dla demona z odpowiednimi uprawnieniami

import os
import sys
import pwd
import grp
from pathlib import Path

def setup_daemon_permissions():
    """Konfiguruje uprawnienia demona"""
    
    # Sprawdź czy demon działa jako root
    if os.getuid() != 0:
        print("❌ BŁĄD: Demon musi działać jako root!")
        print("Snap automatycznie uruchomi demon z odpowiednimi uprawnieniami")
        return False
    
    # Utwórz katalogi systemowe
    system_config_dir = Path("/etc/inv-cleaner")
    system_config_dir.mkdir(parents=True, exist_ok=True)
    
    system_log_dir = Path("/var/log/inv-cleaner")
    system_log_dir.mkdir(parents=True, exist_ok=True)
    
    # Skopiuj konfigurację jeśli nie istnieje
    system_config = system_config_dir / "config.json"
    if not system_config.exists():
        try:
            snap_config = Path(os.environ.get('SNAP', '/')) / "etc" / "inv-cleaner" / "config-example.json"
            if snap_config.exists():
                import shutil
                shutil.copy(snap_config, system_config)
                print(f"✅ Skopiowano konfigurację systemową do {system_config}")
        except Exception as e:
            print(f"⚠️  Nie udało się skopiować konfiguracji: {e}")
    
    return True

def main():
    """Uruchom demon jako root"""
    if not setup_daemon_permissions():
        sys.exit(1)
    
    # Uruchom demon
    sys.path.insert(0, os.path.dirname(__file__))
    import daemon
    daemon.main()

if __name__ == "__main__":
    main()
