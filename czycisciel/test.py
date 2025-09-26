#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test i przykłady użycia Czysciciela Dysku
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime, timedelta

def create_test_environment():
    """Tworzy środowisko testowe z plikami do czyszczenia"""
    test_dir = "/tmp/czysciciel_test"
    
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    os.makedirs(test_dir)
    
    # Utwórz stare pliki
    old_files_dir = os.path.join(test_dir, "old_files")
    os.makedirs(old_files_dir)
    
    for i in range(5):
        file_path = os.path.join(old_files_dir, f"old_log_{i}.log")
        with open(file_path, 'w') as f:
            f.write("Test log content " * 100)
        
        # Ustaw starą datę modyfikacji (10 dni temu)
        old_time = (datetime.now() - timedelta(days=10)).timestamp()
        os.utime(file_path, (old_time, old_time))
    
    # Utwórz duże pliki
    large_files_dir = os.path.join(test_dir, "large_files")
    os.makedirs(large_files_dir)
    
    # Duży plik 300MB (symulowany)
    large_file = os.path.join(large_files_dir, "large_temp.tmp")
    with open(large_file, 'w') as f:
        # Napisz dużo danych (symulacja dużego pliku)
        for _ in range(1000):
            f.write("X" * 1024)  # 1KB na iterację
    
    # Nowe pliki (nie powinny być usunięte)
    new_files_dir = os.path.join(test_dir, "new_files")
    os.makedirs(new_files_dir)
    
    for i in range(3):
        file_path = os.path.join(new_files_dir, f"new_log_{i}.log")
        with open(file_path, 'w') as f:
            f.write("Recent log content")
    
    print(f"Środowisko testowe utworzone w: {test_dir}")
    return test_dir

def test_disk_analyzer():
    """Test analizy dysku"""
    print("=== Test Analizatora Dysku ===")
    
    # Import tylko jeśli potrzebny
    sys.path.append('/opt/czysciciel')
    try:
        from main import DiskAnalyzer
    except ImportError:
        print("Nie można zaimportować DiskAnalyzer - upewnij się, że aplikacja jest zainstalowana")
        return
    
    analyzer = DiskAnalyzer()
    
    # Test na katalogu testowym
    test_dir = create_test_environment()
    
    results = analyzer.analyze_disk_usage(test_dir)
    
    print("Wyniki analizy:")
    for path, data in results.items():
        print(f"  {path}: {data['size_mb']:.2f} MB")
    
    # Cleanup
    shutil.rmtree(test_dir)
    print("Test zakończony")

def test_disk_cleaner():
    """Test czyszczenia dysku"""
    print("=== Test Czyszczenia Dysku ===")
    
    sys.path.append('/opt/czysciciel')
    try:
        from main import DiskCleaner
    except ImportError:
        print("Nie można zaimportować DiskCleaner")
        return
    
    # Użyj tymczasowego pliku logów
    temp_log = tempfile.mktemp(suffix='.log')
    cleaner = DiskCleaner(log_file=temp_log)
    
    test_dir = create_test_environment()
    
    # Test znajdowania starych plików
    old_files = cleaner.find_old_files(test_dir, 7)
    print(f"Znalezione stare pliki: {len(old_files)}")
    for file_path in old_files:
        print(f"  - {file_path}")
    
    # Test znajdowania dużych plików
    large_files = cleaner.find_large_files(test_dir, 1)  # 1MB threshold
    print(f"Znalezione duże pliki: {len(large_files)}")
    for file_path, size in large_files:
        print(f"  - {file_path}: {size / 1024:.2f} KB")
    
    # Cleanup
    shutil.rmtree(test_dir)
    if os.path.exists(temp_log):
        os.remove(temp_log)
    print("Test zakończony")

def benchmark_scan():
    """Benchmark skanowania dysku"""
    print("=== Benchmark Skanowania ===")
    
    import time
    
    # Skanuj różne katalogi i zmierz czas
    test_dirs = ['/tmp', '/var/log', '/etc']
    
    for directory in test_dirs:
        if not os.path.exists(directory):
            continue
            
        start_time = time.time()
        total_size = 0
        file_count = 0
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.exists(file_path):
                            total_size += os.path.getsize(file_path)
                            file_count += 1
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            continue
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Katalog: {directory}")
        print(f"  Rozmiar: {total_size / (1024*1024):.2f} MB")
        print(f"  Pliki: {file_count}")
        print(f"  Czas: {duration:.2f}s")
        print(f"  Szybkość: {file_count/duration:.0f} plików/s")

def show_system_info():
    """Pokazuje informacje systemowe"""
    print("=== Informacje Systemowe ===")
    
    # Python version
    print(f"Python: {sys.version}")
    
    # Dostępne moduły
    modules = ['matplotlib', 'numpy', 'tkinter', 'schedule']
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}: dostępny")
        except ImportError:
            print(f"✗ {module}: BRAK")
    
    # Uprawnienia
    print(f"Użytkownik: {os.getenv('USER', 'unknown')}")
    print(f"UID: {os.getuid()}")
    print(f"GID: {os.getgid()}")
    
    if os.getuid() == 0:
        print("✓ Uprawnienia root")
    else:
        print("⚠ Brak uprawnień root - niektóre funkcje mogą nie działać")
    
    # Dostępne komendy systemowe
    commands = ['notify-send', 'systemctl', 'journalctl']
    for cmd in commands:
        if shutil.which(cmd):
            print(f"✓ {cmd}: dostępny")
        else:
            print(f"✗ {cmd}: BRAK")

def run_gui_test():
    """Test GUI"""
    print("=== Test GUI ===")
    
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Test GUI")
        
        label = tk.Label(root, text="Czysciciel Dysku działa!")
        label.pack(pady=20)
        
        def close_test():
            print("GUI test zakończony")
            root.quit()
        
        button = tk.Button(root, text="Zamknij Test", command=close_test)
        button.pack(pady=10)
        
        root.after(3000, close_test)  # Auto-close po 3 sekundach
        root.mainloop()
        
    except ImportError:
        print("✗ tkinter nie jest dostępny")
    except Exception as e:
        print(f"✗ Błąd GUI: {e}")

def main():
    """Główna funkcja testowa"""
    print("🧹 TESTY CZYSCICIELA DYSKU 💾")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == 'analyzer':
            test_disk_analyzer()
        elif test_type == 'cleaner':
            test_disk_cleaner()
        elif test_type == 'benchmark':
            benchmark_scan()
        elif test_type == 'info':
            show_system_info()
        elif test_type == 'gui':
            run_gui_test()
        else:
            print(f"Nieznany test: {test_type}")
    else:
        print("Dostępne testy:")
        print("  python3 test.py info      - informacje systemowe")
        print("  python3 test.py analyzer  - test analizatora")
        print("  python3 test.py cleaner   - test czyszczenia")
        print("  python3 test.py benchmark - benchmark skanowania")
        print("  python3 test.py gui       - test GUI")
        
        # Uruchom podstawowe testy
        show_system_info()

if __name__ == "__main__":
    main()
