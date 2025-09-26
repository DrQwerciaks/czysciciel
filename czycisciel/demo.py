#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo - Test Inv Cleaner z nową funkcjonalnością
"""

import os
import sys
import tempfile
import time
from datetime import datetime, timedelta

def create_demo_files():
    """Tworzy pliki demo do testowania"""
    demo_dir = "/tmp/inv_cleaner_demo"
    
    if os.path.exists(demo_dir):
        import shutil
        shutil.rmtree(demo_dir)
    
    os.makedirs(demo_dir, exist_ok=True)
    
    print(f"📁 Tworzenie plików demo w: {demo_dir}")
    
    # Stare pliki logów
    old_logs_dir = os.path.join(demo_dir, "old_logs")
    os.makedirs(old_logs_dir)
    
    for i in range(5):
        file_path = os.path.join(old_logs_dir, f"old_system_{i}.log")
        with open(file_path, 'w') as f:
            f.write("Old log content " * 1000)  # ~16KB każdy
        
        # Ustaw starą datę (10 dni temu)
        old_time = (datetime.now() - timedelta(days=10)).timestamp()
        os.utime(file_path, (old_time, old_time))
    
    # Duże pliki tymczasowe
    large_dir = os.path.join(demo_dir, "large_temp")
    os.makedirs(large_dir)
    
    # Duży plik (symulacja 5MB)
    large_file = os.path.join(large_dir, "big_temp_file.tmp")
    with open(large_file, 'w') as f:
        for _ in range(5000):  # 5000 linii po ~1KB = ~5MB
            f.write("X" * 1000 + "\n")
    
    # Nowe pliki (nie powinny być usunięte)
    new_dir = os.path.join(demo_dir, "recent_files")
    os.makedirs(new_dir)
    
    for i in range(3):
        file_path = os.path.join(new_dir, f"recent_{i}.log")
        with open(file_path, 'w') as f:
            f.write("Recent content")
    
    print("✅ Pliki demo utworzone:")
    print(f"   📅 Stare logi (10 dni): {len(os.listdir(old_logs_dir))} plików")
    print(f"   📏 Duże pliki: {len(os.listdir(large_dir))} plików")
    print(f"   🆕 Nowe pliki: {len(os.listdir(new_dir))} plików")
    print()
    return demo_dir

def run_translation_test():
    """Test systemu tłumaczeń"""
    print("🌐 Test wielojęzyczności")
    print("=" * 30)
    
    sys.path.append('.')
    try:
        from main import TranslationManager
        
        translator = TranslationManager()
        
        # Test polskich tłumaczeń
        print("🇵🇱 Polski:")
        translator.set_language("pl")
        print(f"   Tytuł: {translator.get('app_title')}")
        print(f"   Przycisk: {translator.get('clean_now')}")
        print(f"   Status: {translator.get('status_ready')}")
        
        # Test angielskich tłumaczeń
        print("\n🇬🇧 English:")
        translator.set_language("en")
        print(f"   Title: {translator.get('app_title')}")
        print(f"   Button: {translator.get('clean_now')}")
        print(f"   Status: {translator.get('status_ready')}")
        
        print("✅ Tłumaczenia działają!")
        
    except ImportError as e:
        print(f"❌ Błąd importu: {e}")
    except Exception as e:
        print(f"❌ Błąd testu: {e}")
    
    print()

def run_cleaner_test():
    """Test trybu testowego cleanera"""
    print("🧪 Test trybu testowego")
    print("=" * 30)
    
    # Utwórz pliki demo
    demo_dir = create_demo_files()
    
    try:
        sys.path.append('.')
        from main import DiskCleaner
        
        # Stwórz instancję cleanera
        cleaner = DiskCleaner("/tmp/test_cleaner.log")
        
        # Lista do zbierania wiadomości z testu
        test_messages = []
        
        def collect_message(msg):
            test_messages.append(msg)
            print(f"[TEST] {msg}")
        
        # Włącz tryb testowy
        cleaner.set_test_mode(True, collect_message)
        
        print("🔍 Uruchamianie symulacji czyszczenia...")
        
        # Sprawdź stare pliki
        old_files = cleaner.find_old_files(demo_dir, 7)
        large_files = cleaner.find_large_files(demo_dir, 1)  # 1MB threshold
        
        print(f"📅 Znaleziono {len(old_files)} starych plików")
        print(f"📏 Znaleziono {len(large_files)} dużych plików")
        
        # Wykonaj test czyszczenia
        result = cleaner.perform_cleanup()
        
        print(f"\n📊 Wyniki testu:")
        print(f"   💾 Do wyczyszczenia: {result['total_cleaned_mb']:.2f} MB")
        print(f"   📁 Liczba plików: {result['files_cleaned']}")
        print(f"   ⏱️  Czas: {result['end_time'] - result['start_time']}")
        
        print("✅ Test trybu testowego zakończony!")
        
    except Exception as e:
        print(f"❌ Błąd testu cleanera: {e}")
    
    # Cleanup
    try:
        import shutil
        shutil.rmtree(demo_dir)
        if os.path.exists("/tmp/test_cleaner.log"):
            os.remove("/tmp/test_cleaner.log")
    except:
        pass
    
    print()

def show_demo_menu():
    """Pokazuje menu demo"""
    print("🧹 INV CLEANER - DEMO NOWYCH FUNKCJI 💾")
    print("=" * 50)
    print()
    print("Nowe funkcje w tej wersji:")
    print("  🌐 Wielojęzyczność (Polski/Angielski)")
    print("  🧪 Tryb testowy z konsolą na żywo") 
    print("  🎨 Ulepszone UI z emoji")
    print("  📊 Lepsze raporty i statystyki")
    print()
    print("Dostępne testy:")
    print("  1. 🌐 Test wielojęzyczności")
    print("  2. 🧪 Test trybu testowego")
    print("  3. 🖥️  Uruchom aplikację GUI")
    print("  4. 📋 Pokaż informacje o aplikacji")
    print("  0. ❌ Wyjście")
    print()

def show_app_info():
    """Pokazuje informacje o aplikacji"""
    print("📋 INFORMACJE O APLIKACJI")
    print("=" * 30)
    print("Nazwa: Inv Cleaner")
    print("Wersja: 1.0.0")
    print("Autor: System Administrator")
    print("Data: 26 września 2025")
    print()
    print("Funkcje:")
    print("  🧹 Automatyczne czyszczenie plików")
    print("  📊 Analiza wykorzystania dysku (jak Baobab)")
    print("  🔔 Powiadomienia systemowe")
    print("  ⚙️  Działanie w tle jako demon")
    print("  🌐 Interfejs dwujęzyczny (PL/EN)")
    print("  🧪 Tryb testowy z podglądem na żywo")
    print()
    print("Instalacja:")
    print("  📦 Snap Store: sudo snap install inv-cleaner")
    print("  🐙 GitHub: curl -L <url>/quick-install.sh | sudo bash")
    print("  💻 Lokalnie: make install")
    print()

def main():
    """Główna funkcja demo"""
    while True:
        show_demo_menu()
        
        try:
            choice = input("Wybierz opcję (0-4): ").strip()
            print()
            
            if choice == "0":
                print("👋 Do widzenia!")
                break
            elif choice == "1":
                run_translation_test()
            elif choice == "2":
                run_cleaner_test()
            elif choice == "3":
                print("🖥️  Uruchamianie GUI...")
                os.system("python3 main.py")
                print()
            elif choice == "4":
                show_app_info()
            else:
                print("❌ Nieprawidłowa opcja. Spróbuj ponownie.")
            
            if choice != "0":
                input("Naciśnij Enter aby kontynuować...")
                print()
                
        except KeyboardInterrupt:
            print("\n\n👋 Do widzenia!")
            break
        except Exception as e:
            print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    main()
