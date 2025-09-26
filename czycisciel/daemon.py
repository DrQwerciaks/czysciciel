#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Czysciciel Daemon - Demon działający w tle
Automatyczne czyszczenie dysku co godzinę
"""

import os
import sys
import time
import json
import logging
import schedule
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Dodaj ścieżkę do głównego modułu
sys.path.append('/opt/czysciciel')

class CzyscicielDaemon:
    """Demon do automatycznego czyszczenia dysku"""
    
    def __init__(self):
        self.log_file = "/var/log/czysciciel-daemon.log"
        self.config_file = "/etc/czysciciel/config.json"
        self.pid_file = "/var/run/czysciciel.pid"
        
        self.setup_logging()
        self.load_config()
        self.create_pid_file()
        
    def setup_logging(self):
        """Konfiguruje system logowania"""
        # Utwórz katalog logów jeśli nie istnieje
        os.makedirs("/var/log", exist_ok=True)
        
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Dodaj również logowanie do konsoli
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        logger = logging.getLogger()
        logger.addHandler(console_handler)
        
        self.logger = logger
        
    def load_config(self):
        """Ładuje konfigurację"""
        default_config = {
            "cleaning_enabled": True,
            "scan_interval_hours": 1,
            "days_old": 7,
            "large_file_mb": 200,
            "directories_to_clean": [
                "/var/log",
                "/tmp", 
                "/var/tmp"
            ],
            "directories_to_scan": [
                "/var/log",
                "/tmp",
                "/var/tmp",
                "/home",
                "/usr/share",
                "/var/cache"
            ],
            "notifications_enabled": True,
            "preserve_files": [
                "*.conf",
                "*.cfg", 
                "*.config"
            ]
        }
        
        try:
            # Utwórz katalog konfiguracji
            os.makedirs("/etc/czysciciel", exist_ok=True)
            
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
                
        except Exception as e:
            self.logger.error(f"Błąd ładowania konfiguracji: {e}")
            self.config = default_config
            
    def save_config(self):
        """Zapisuje konfigurację"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            self.logger.error(f"Błąd zapisywania konfiguracji: {e}")
    
    def create_pid_file(self):
        """Tworzy plik PID"""
        try:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        except Exception as e:
            self.logger.error(f"Błąd tworzenia pliku PID: {e}")
    
    def remove_pid_file(self):
        """Usuwa plik PID"""
        try:
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
        except Exception as e:
            self.logger.error(f"Błąd usuwania pliku PID: {e}")
    
    def get_directory_size(self, path: str) -> int:
        """Pobiera rozmiar katalogu w bajtach"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for file in filenames:
                    try:
                        file_path = os.path.join(dirpath, file)
                        if os.path.exists(file_path):
                            total_size += os.path.getsize(file_path)
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
        return total_size
    
    def find_old_files(self, directory: str, days_old: int) -> list:
        """Znajduje pliki starsze niż określona liczba dni"""
        old_files = []
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.exists(file_path):
                            # Sprawdź czy plik nie jest na liście do zachowania
                            if not self.should_preserve_file(file_path):
                                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                                if file_time < cutoff_date:
                                    old_files.append(file_path)
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
            
        return old_files
    
    def find_large_files(self, directory: str, size_mb: int) -> list:
        """Znajduje pliki większe niż określony rozmiar"""
        large_files = []
        size_bytes = size_mb * 1024 * 1024
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.exists(file_path):
                            if not self.should_preserve_file(file_path):
                                file_size = os.path.getsize(file_path)
                                if file_size > size_bytes:
                                    large_files.append((file_path, file_size))
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
            
        return large_files
    
    def should_preserve_file(self, file_path: str) -> bool:
        """Sprawdza czy plik powinien być zachowany"""
        import fnmatch
        
        filename = os.path.basename(file_path)
        for pattern in self.config.get('preserve_files', []):
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False
    
    def send_notification(self, title: str, message: str):
        """Wysyła powiadomienie systemowe"""
        if not self.config.get('notifications_enabled', True):
            return
            
        try:
            # Linux - używa notify-send dla wszystkich użytkowników
            subprocess.run([
                'su', '-c', 
                f'DISPLAY=:0 notify-send "{title}" "{message}"',
                'root'
            ], check=False)
            
            # Alternatywnie wyślij przez systemd-notify
            subprocess.run([
                'systemd-notify', 
                f'STATUS={title}: {message}'
            ], check=False)
            
        except (subprocess.SubprocessError, FileNotFoundError):
            self.logger.info(f"Powiadomienie: {title} - {message}")
    
    def perform_cleanup(self) -> dict:
        """Wykonuje czyszczenie dysku"""
        if not self.config.get('cleaning_enabled', True):
            self.logger.info("Czyszczenie wyłączone w konfiguracji")
            return {'total_cleaned': 0}
        
        self.logger.info("Rozpoczynam czyszczenie dysku")
        start_time = datetime.now()
        
        total_cleaned = 0
        files_cleaned = 0
        cleaned_files = []
        
        directories = self.config.get('directories_to_clean', ['/var/log', '/tmp'])
        days_old = self.config.get('days_old', 7)
        large_file_mb = self.config.get('large_file_mb', 200)
        
        for directory in directories:
            if not os.path.exists(directory):
                continue
                
            self.logger.info(f"Czyszczenie katalogu: {directory}")
            
            # Usuń stare pliki
            old_files = self.find_old_files(directory, days_old)
            for file_path in old_files:
                try:
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        os.remove(file_path)
                        total_cleaned += file_size
                        files_cleaned += 1
                        cleaned_files.append(file_path)
                        self.logger.info(f"Usunięto stary plik: {file_path} ({file_size} B)")
                except Exception as e:
                    self.logger.error(f"Błąd usuwania {file_path}: {e}")
            
            # Usuń duże pliki z /tmp
            if directory in ['/tmp', '/var/tmp']:
                large_files = self.find_large_files(directory, large_file_mb)
                for file_path, file_size in large_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            total_cleaned += file_size
                            files_cleaned += 1
                            cleaned_files.append(file_path)
                            self.logger.info(f"Usunięto duży plik: {file_path} ({file_size} B)")
                    except Exception as e:
                        self.logger.error(f"Błąd usuwania {file_path}: {e}")
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        result = {
            'total_cleaned': total_cleaned,
            'total_cleaned_mb': total_cleaned / (1024 * 1024),
            'files_cleaned': files_cleaned,
            'cleaned_files': cleaned_files,
            'start_time': start_time,
            'end_time': end_time,
            'duration': duration
        }
        
        # Loguj wyniki
        self.logger.info(f"Czyszczenie zakończone w {duration}")
        self.logger.info(f"Wyczyszczono: {result['total_cleaned_mb']:.2f} MB w {files_cleaned} plikach")
        
        # Wyślij powiadomienie jeśli coś wyczyszczono
        if total_cleaned > 0:
            cleaned_mb = result['total_cleaned_mb']
            self.send_notification(
                "Czysciciel Dysku",
                f"Wyczyszczono {cleaned_mb:.0f} MB z {files_cleaned} plików"
            )
        
        return result
    
    def analyze_disk_usage(self) -> dict:
        """Analizuje wykorzystanie dysku"""
        results = {}
        directories = self.config.get('directories_to_scan', [])
        
        for directory in directories:
            if os.path.exists(directory):
                try:
                    size = self.get_directory_size(directory)
                    results[directory] = {
                        'size': size,
                        'size_mb': size / (1024 * 1024),
                        'size_gb': size / (1024 * 1024 * 1024)
                    }
                    self.logger.debug(f"{directory}: {size / (1024*1024):.2f} MB")
                except Exception as e:
                    self.logger.error(f"Błąd skanowania {directory}: {e}")
        
        return results
    
    def scheduled_task(self):
        """Zaplanowane zadanie czyszczenia"""
        self.logger.info("Uruchamianie zaplanowanego czyszczenia")
        
        try:
            # Analiza dysku
            disk_usage = self.analyze_disk_usage()
            
            # Czyszczenie
            cleanup_result = self.perform_cleanup()
            
            # Zapisz statystyki
            stats = {
                'timestamp': datetime.now().isoformat(),
                'disk_usage': disk_usage,
                'cleanup_result': cleanup_result
            }
            
            stats_file = "/var/log/czysciciel-stats.json"
            try:
                with open(stats_file, 'a') as f:
                    json.dump(stats, f)
                    f.write('\n')
            except Exception as e:
                self.logger.error(f"Błąd zapisywania statystyk: {e}")
                
        except Exception as e:
            self.logger.error(f"Błąd podczas zaplanowanego zadania: {e}")
    
    def setup_schedule(self):
        """Konfiguruje harmonogram zadań"""
        interval = self.config.get('scan_interval_hours', 1)
        
        # Wyczyść poprzednie harmonogramy
        schedule.clear()
        
        # Ustaw nowy harmonogram
        schedule.every(interval).hours.do(self.scheduled_task)
        
        self.logger.info(f"Harmonogram ustawiony na {interval} godzin(y)")
    
    def run(self):
        """Główna pętla demona"""
        self.logger.info("Demon Czysciciela rozpoczął pracę")
        
        # Ustaw harmonogram
        self.setup_schedule()
        
        # Pierwsze uruchomienie po 5 minutach
        schedule.every(5).minutes.do(self.scheduled_task).tag('initial')
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Sprawdzaj co minutę
                
                # Po pierwszym uruchomieniu usuń zadanie inicjalne
                if schedule.get_jobs('initial'):
                    schedule.clear('initial')
                    
        except KeyboardInterrupt:
            self.logger.info("Otrzymano sygnał przerwania")
        except Exception as e:
            self.logger.error(f"Błąd w głównej pętli: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Sprzątanie przed zakończeniem"""
        self.logger.info("Zatrzymuję demona...")
        self.remove_pid_file()

def main():
    """Główna funkcja demona"""
    if os.geteuid() != 0:
        print("Demon musi być uruchomiony jako root!")
        sys.exit(1)
    
    daemon = CzyscicielDaemon()
    
    try:
        daemon.run()
    except Exception as e:
        daemon.logger.error(f"Krytyczny błąd demona: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
