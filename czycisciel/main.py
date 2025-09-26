#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inv Cleaner - Advanced disk cleaner and monitoring tool
Advanced disk cleaning and monitoring application for Linux systems
Author: System Administrator
Date: 26 września 2025
"""

import sys
import os
import json
import logging
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import subprocess
import schedule

class TranslationManager:
    """Klasa do zarządzania tłumaczeniami"""
    
    def __init__(self):
        self.current_lang = "pl"  # Default Polish
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Ładuje tłumaczenia z pliku"""
        try:
            # Try different possible paths
            translation_paths = [
                "translations.json",
                "assets/translations.json", 
                "/opt/inv-cleaner/translations.json",
                "/snap/inv-cleaner/current/translations.json"
            ]
            
            for path in translation_paths:
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        self.translations = json.load(f)
                    break
            else:
                # Fallback translations if file not found
                self.translations = {
                    "pl": {"app_title": "Inv Cleaner - Zaawansowane Narzędzie"},
                    "en": {"app_title": "Inv Cleaner - Advanced Tool"}
                }
        except Exception as e:
            print(f"Error loading translations: {e}")
            self.translations = {"pl": {}, "en": {}}
    
    def get(self, key: str, *args) -> str:
        """Pobiera tłumaczenie dla klucza"""
        try:
            text = self.translations.get(self.current_lang, {}).get(key, key)
            if args:
                return text.format(*args)
            return text
        except Exception:
            return key
    
    def set_language(self, lang: str):
        """Ustawia język aplikacji"""
        if lang in self.translations:
            self.current_lang = lang

class DiskAnalyzer:
    """Klasa do analizy wykorzystania dysku"""
    
    def __init__(self):
        self.scan_results = {}
        
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
    
    def analyze_disk_usage(self, root_path: str = "/") -> Dict:
        """Analizuje wykorzystanie dysku"""
        results = {}
        important_dirs = [
            "/var/log", "/tmp", "/var/tmp", "/home", "/usr", 
            "/var", "/opt", "/boot", "/etc"
        ]
        
        for dir_path in important_dirs:
            if os.path.exists(dir_path):
                size = self.get_directory_size(dir_path)
                results[dir_path] = {
                    'size': size,
                    'size_mb': size / (1024 * 1024),
                    'size_gb': size / (1024 * 1024 * 1024)
                }
        
        self.scan_results = results
        return results

class DiskCleaner:
    """Klasa do czyszczenia dysku"""
    
    def __init__(self, log_file: str = "/var/log/czysciciel.log"):
        self.log_file = log_file
        self.setup_logging()
        self.cleaned_files = []
        self.total_cleaned = 0
        self.test_mode = False
        self.test_callback = None
        
    def set_test_mode(self, enabled: bool, callback=None):
        """Ustawia tryb testowy"""
        self.test_mode = enabled
        self.test_callback = callback
    
    def _log_or_callback(self, message: str, level: str = "info"):
        """Loguje wiadomość lub wywołuje callback w trybie testowym"""
        if self.test_mode and self.test_callback:
            self.test_callback(message)
        else:
            if level == "info":
                self.logger.info(message)
            elif level == "error":
                self.logger.error(message)
        
    def setup_logging(self):
        """Konfiguruje system logowania"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
    
    def find_old_files(self, directory: str, days_old: int = 7) -> List[str]:
        """Znajduje pliki starsze niż określona liczba dni"""
        old_files = []
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.exists(file_path):
                            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                            if file_time < cutoff_date:
                                old_files.append(file_path)
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
            
        return old_files
    
    def find_large_files(self, directory: str, size_mb: int = 200) -> List[Tuple[str, int]]:
        """Znajduje pliki większe niż określony rozmiar"""
        large_files = []
        size_bytes = size_mb * 1024 * 1024
        
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            if file_size > size_bytes:
                                large_files.append((file_path, file_size))
                    except (OSError, IOError):
                        continue
        except (OSError, IOError):
            pass
            
        return large_files
    
    def clean_log_files(self) -> int:
        """Czyści stare pliki logów"""
        cleaned_size = 0
        log_directories = ["/var/log", "/tmp", "/var/tmp"]
        
        for log_dir in log_directories:
            if os.path.exists(log_dir):
                self._log_or_callback(f"🔍 Skanowanie katalogu: {log_dir}")
                old_files = self.find_old_files(log_dir, 7)
                
                if old_files:
                    self._log_or_callback(f"📅 Znaleziono {len(old_files)} starych plików w {log_dir}")
                
                for file_path in old_files:
                    try:
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            
                            if self.test_mode:
                                self._log_or_callback(f"🗑️  SYMULACJA: {file_path} ({file_size} bajtów)")
                            else:
                                os.remove(file_path)
                                cleaned_size += file_size
                                self.cleaned_files.append(file_path)
                                self._log_or_callback(f"✅ Usunięto: {file_path} ({file_size} bajtów)")
                            
                            if self.test_mode:
                                cleaned_size += file_size  # Count for simulation
                                
                    except (OSError, IOError) as e:
                        self._log_or_callback(f"❌ Błąd: {file_path}: {e}", "error")
        
        return cleaned_size
    
    def clean_large_files(self) -> int:
        """Czyści duże pliki tymczasowe"""
        cleaned_size = 0
        temp_directories = ["/tmp", "/var/tmp"]
        
        for temp_dir in temp_directories:
            if os.path.exists(temp_dir):
                self._log_or_callback(f"🔍 Skanowanie dużych plików w: {temp_dir}")
                large_files = self.find_large_files(temp_dir, 200)
                
                if large_files:
                    self._log_or_callback(f"📏 Znaleziono {len(large_files)} dużych plików w {temp_dir}")
                
                for file_path, file_size in large_files:
                    try:
                        if os.path.exists(file_path):
                            if self.test_mode:
                                self._log_or_callback(f"🗑️  SYMULACJA: {file_path} ({file_size / (1024*1024):.2f} MB)")
                            else:
                                os.remove(file_path)
                                cleaned_size += file_size
                                self.cleaned_files.append(file_path)
                                self._log_or_callback(f"✅ Usunięto duży plik: {file_path} ({file_size / (1024*1024):.2f} MB)")
                            
                            if self.test_mode:
                                cleaned_size += file_size  # Count for simulation
                                
                    except (OSError, IOError) as e:
                        self._log_or_callback(f"❌ Błąd: {file_path}: {e}", "error")
        
        return cleaned_size
    
    def perform_cleanup(self) -> Dict:
        """Wykonuje pełne czyszczenie"""
        self.cleaned_files = []
        start_time = datetime.now()
        
        log_cleaned = self.clean_log_files()
        large_cleaned = self.clean_large_files()
        
        total_cleaned = log_cleaned + large_cleaned
        self.total_cleaned = total_cleaned
        
        result = {
            'total_cleaned': total_cleaned,
            'total_cleaned_mb': total_cleaned / (1024 * 1024),
            'files_cleaned': len(self.cleaned_files),
            'log_cleaned': log_cleaned,
            'large_cleaned': large_cleaned,
            'start_time': start_time,
            'end_time': datetime.now()
        }
        
        self.logger.info(f"Czyszczenie zakończone: {result}")
        return result

class NotificationManager:
    """Klasa do zarządzania powiadomieniami"""
    
    @staticmethod
    def send_notification(title: str, message: str):
        """Wysyła powiadomienie systemowe"""
        try:
            # Linux - używa notify-send
            subprocess.run(['notify-send', title, message], check=False)
        except (subprocess.SubprocessError, FileNotFoundError):
            print(f"Powiadomienie: {title} - {message}")

class TestConsole:
    """Okno konsoli testowej do podglądu operacji na żywo"""
    
    def __init__(self, parent, translator):
        self.parent = parent
        self.translator = translator
        self.window = None
        self.console_text = None
        self.is_open = False
        
    def open_console(self):
        """Otwiera okno konsoli testowej"""
        if self.is_open:
            return
            
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.translator.get("test_console_title"))
        self.window.geometry("800x600")
        self.window.transient(self.parent)
        
        # Make it stay on top
        self.window.attributes('-topmost', True)
        
        # Console text area
        self.console_text = scrolledtext.ScrolledText(
            self.window,
            height=30,
            width=100,
            bg='black',
            fg='lime',
            font=('Courier', 10)
        )
        self.console_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        close_btn = ttk.Button(
            self.window,
            text=self.translator.get("close_console"),
            command=self.close_console
        )
        close_btn.pack(pady=5)
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.close_console)
        
        self.is_open = True
        self.add_message("=== 🧪 INV CLEANER TEST MODE ===")
        self.add_message(self.translator.get("test_scanning"))
        
    def add_message(self, message: str):
        """Dodaje wiadomość do konsoli"""
        if self.console_text and self.is_open:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"
            
            self.console_text.insert(tk.END, formatted_message)
            self.console_text.see(tk.END)
            self.console_text.update()
            
    def close_console(self):
        """Zamyka okno konsoli"""
        if self.window:
            self.is_open = False
            self.window.destroy()
            self.window = None

class CzyscicielApp:
    """Główna aplikacja z interfejsem graficznym"""
    
    def __init__(self):
        self.root = tk.Tk()
        
        # Initialize translator
        self.translator = TranslationManager()
        
        self.root.title(self.translator.get("app_title"))
        self.root.geometry("1200x800")
        
        # Set app icon if available
        try:
            # Try to load icon from snap environment or local assets
            icon_paths = [
                "/snap/inv-cleaner/current/usr/share/icons/hicolor/256x256/apps/inv-cleaner-logo.png",
                "assets/inv-cleaner-logo.png",
                "/usr/share/icons/hicolor/256x256/apps/inv-cleaner-logo.png"
            ]
            for icon_path in icon_paths:
                if os.path.exists(icon_path):
                    icon = tk.PhotoImage(file=icon_path)
                    self.root.iconphoto(False, icon)
                    break
        except Exception:
            pass  # Continue without icon if loading fails
        
        self.analyzer = DiskAnalyzer()
        self.cleaner = DiskCleaner()
        self.notification_manager = NotificationManager()
        self.test_console = TestConsole(self.root, self.translator)
        
        self.is_monitoring = False
        self.monitoring_thread = None
        
        self.setup_ui()
        self.setup_scheduler()
        
    def update_language(self):
        """Aktualizuje interfejs po zmianie języka"""
        self.root.title(self.translator.get("app_title"))
        
        # Update tab names
        self.notebook.tab(0, text=self.translator.get("disk_analysis"))
        self.notebook.tab(1, text=self.translator.get("cleaning"))
        self.notebook.tab(2, text=self.translator.get("logs"))
        self.notebook.tab(3, text=self.translator.get("settings"))
        
        # Update buttons and labels
        self.scan_btn.config(text=self.translator.get("scan_disk"))
        self.clean_btn.config(text=self.translator.get("clean_now"))
        self.test_btn.config(text=self.translator.get("test_clean"))
        
        if self.is_monitoring:
            self.monitor_btn.config(text=self.translator.get("stop_monitoring"))
        else:
            self.monitor_btn.config(text=self.translator.get("start_monitoring"))
            
        self.refresh_logs_btn.config(text=self.translator.get("refresh_logs"))
        self.clear_logs_btn.config(text=self.translator.get("clear_logs"))
        
        # Update status
        self.status_var.set(self.translator.get("status_ready"))
        
        # Update tree headers
        self.results_tree.heading('Path', text=self.translator.get("path"))
        self.results_tree.heading('Size_MB', text=self.translator.get("size_mb"))
        self.results_tree.heading('Size_GB', text=self.translator.get("size_gb"))
        
    def setup_ui(self):
        """Konfiguruje interfejs użytkownika"""
        # Notebook dla zakładek
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Zakładka analizy dysku
        self.disk_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.disk_frame, text=self.translator.get("disk_analysis"))
        
        # Zakładka czyszczenia
        self.clean_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clean_frame, text=self.translator.get("cleaning"))
        
        # Zakładka logów
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text=self.translator.get("logs"))
        
        # Zakładka ustawień
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text=self.translator.get("settings"))
        
        self.setup_disk_analysis_tab()
        self.setup_cleaning_tab()
        self.setup_log_tab()
        self.setup_settings_tab()
        
    def setup_disk_analysis_tab(self):
        """Konfiguruje zakładkę analizy dysku"""
        # Przycisk skanowania
        self.scan_btn = ttk.Button(
            self.disk_frame, 
            text=self.translator.get("scan_disk"), 
            command=self.scan_disk
        )
        self.scan_btn.pack(pady=10)
        
        # Ramka na wykres
        self.chart_frame = ttk.Frame(self.disk_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Lista wyników
        self.results_tree = ttk.Treeview(
            self.disk_frame, 
            columns=('Path', 'Size_MB', 'Size_GB'), 
            show='headings'
        )
        self.results_tree.heading('Path', text=self.translator.get("path"))
        self.results_tree.heading('Size_MB', text=self.translator.get("size_mb"))
        self.results_tree.heading('Size_GB', text=self.translator.get("size_gb"))
        self.results_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_cleaning_tab(self):
        """Konfiguruje zakładkę czyszczenia"""
        # Przyciski
        btn_frame = ttk.Frame(self.clean_frame)
        btn_frame.pack(pady=10)
        
        self.clean_btn = ttk.Button(
            btn_frame, 
            text=self.translator.get("clean_now"), 
            command=self.manual_cleanup
        )
        self.clean_btn.pack(side=tk.LEFT, padx=5)
        
        self.test_btn = ttk.Button(
            btn_frame, 
            text=self.translator.get("test_clean"), 
            command=self.test_cleanup
        )
        self.test_btn.pack(side=tk.LEFT, padx=5)
        
        self.monitor_btn = ttk.Button(
            btn_frame, 
            text=self.translator.get("start_monitoring"), 
            command=self.toggle_monitoring
        )
        self.monitor_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set(self.translator.get("status_ready"))
        status_label = ttk.Label(self.clean_frame, textvariable=self.status_var)
        status_label.pack(pady=10)
        
        # Wyniki czyszczenia
        self.clean_results = scrolledtext.ScrolledText(
            self.clean_frame, 
            height=20, 
            width=80
        )
        self.clean_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_log_tab(self):
        """Konfiguruje zakładkę logów"""
        # Przyciski
        log_btn_frame = ttk.Frame(self.log_frame)
        log_btn_frame.pack(pady=10)
        
        self.refresh_logs_btn = ttk.Button(
            log_btn_frame, 
            text=self.translator.get("refresh_logs"), 
            command=self.refresh_logs
        )
        self.refresh_logs_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_logs_btn = ttk.Button(
            log_btn_frame, 
            text=self.translator.get("clear_logs"), 
            command=self.clear_logs
        )
        self.clear_logs_btn.pack(side=tk.LEFT, padx=5)
        
        # Obszar logów
        self.log_text = scrolledtext.ScrolledText(
            self.log_frame, 
            height=30, 
            width=100
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def setup_settings_tab(self):
        """Konfiguruje zakładkę ustawień"""
        # Ustawienia
        ttk.Label(self.settings_frame, text=self.translator.get("cleaning_settings")).pack(pady=10)
        
        # Język
        lang_frame = ttk.Frame(self.settings_frame)
        lang_frame.pack(pady=5)
        ttk.Label(lang_frame, text=self.translator.get("language")).pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value=self.translator.current_lang)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, values=["pl", "en"], state="readonly", width=10)
        lang_combo.pack(side=tk.LEFT, padx=5)
        lang_combo.bind("<<ComboboxSelected>>", self.on_language_change)
        
        # Dni do usunięcia
        days_frame = ttk.Frame(self.settings_frame)
        days_frame.pack(pady=5)
        ttk.Label(days_frame, text=self.translator.get("remove_files_older")).pack(side=tk.LEFT)
        self.days_var = tk.IntVar(value=7)
        ttk.Spinbox(days_frame, from_=1, to=30, textvariable=self.days_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Rozmiar plików
        size_frame = ttk.Frame(self.settings_frame)
        size_frame.pack(pady=5)
        ttk.Label(size_frame, text=self.translator.get("remove_files_larger")).pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=200)
        ttk.Spinbox(size_frame, from_=50, to=1000, textvariable=self.size_var, width=10).pack(side=tk.LEFT, padx=5)
        
        # Częstotliwość skanowania
        freq_frame = ttk.Frame(self.settings_frame)
        freq_frame.pack(pady=5)
        ttk.Label(freq_frame, text=self.translator.get("scan_frequency")).pack(side=tk.LEFT)
        self.freq_var = tk.IntVar(value=1)
        ttk.Spinbox(freq_frame, from_=1, to=24, textvariable=self.freq_var, width=10).pack(side=tk.LEFT, padx=5)
    
    def on_language_change(self, event):
        """Zmienia język aplikacji"""
        new_lang = self.lang_var.get()
        self.translator.set_language(new_lang)
        self.update_language()
        
    def setup_scheduler(self):
        """Konfiguruje harmonogram czyszczenia"""
        schedule.every().hour.do(self.scheduled_cleanup)
        
    def scan_disk(self):
        """Skanuje dysk i wyświetla wyniki"""
        self.status_var.set(self.translator.get("status_scanning"))
        self.root.update()
        
        # Uruchom skanowanie w osobnym wątku
        threading.Thread(target=self._scan_disk_thread, daemon=True).start()
        
    def _scan_disk_thread(self):
        """Wątek skanowania dysku"""
        try:
            results = self.analyzer.analyze_disk_usage()
            
            # Aktualizuj UI w głównym wątku
            self.root.after(0, lambda: self._update_disk_results(results))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Błąd: {str(e)}"))
    
    def _update_disk_results(self, results):
        """Aktualizuje wyniki skanowania dysku"""
        # Wyczyść poprzednie wyniki
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Dodaj nowe wyniki
        for path, data in results.items():
            self.results_tree.insert('', 'end', values=(
                path, 
                f"{data['size_mb']:.2f}", 
                f"{data['size_gb']:.2f}"
            ))
        
        # Stwórz wykres
        self.create_disk_chart(results)
        self.status_var.set(self.translator.get("status_scan_complete"))
    
    def create_disk_chart(self, results):
        """Tworzy wykres kołowy wykorzystania dysku"""
        # Wyczyść poprzedni wykres
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if not results:
            return
        
        # Przygotuj dane
        labels = []
        sizes = []
        colors = plt.cm.Set3(np.linspace(0, 1, len(results)))
        
        for path, data in results.items():
            if data['size_mb'] > 1:  # Pokaż tylko foldery > 1MB
                labels.append(path)
                sizes.append(data['size_mb'])
        
        # Stwórz wykres
        fig, ax = plt.subplots(figsize=(10, 8))
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        
        ax.set_title(self.translator.get("disk_usage_title"))
        plt.setp(autotexts, size=8, weight="bold")
        plt.setp(texts, size=8)
        
        # Dodaj wykres do GUI
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def test_cleanup(self):
        """Testowe czyszczenie z konsolą"""
        self.status_var.set(self.translator.get("status_testing"))
        
        # Otwórz konsolę testową
        self.test_console.open_console()
        
        # Uruchom test w osobnym wątku
        threading.Thread(target=self._test_cleanup_thread, daemon=True).start()
        
    def _test_cleanup_thread(self):
        """Wątek testowego czyszczenia"""
        try:
            # Ustaw tryb testowy
            self.cleaner.set_test_mode(True, self.test_console.add_message)
            
            # Wykonaj symulację czyszczenia
            result = self.cleaner.perform_cleanup()
            
            # Pokaż podsumowanie w konsoli
            total_mb = result['total_cleaned_mb']
            files_count = result['files_cleaned']
            
            if total_mb > 0:
                self.test_console.add_message("")
                self.test_console.add_message(f"💾 RAZEM DO WYCZYSZCZENIA: {total_mb:.2f} MB ({files_count} plików)")
                self.test_console.add_message("")
                self.test_console.add_message("✅ " + self.translator.get("test_complete"))
            else:
                self.test_console.add_message("✅ " + self.translator.get("test_no_files"))
            
            # Aktualizuj UI w głównym wątku
            self.root.after(0, lambda: self._update_test_results(result))
            
        except Exception as e:
            self.test_console.add_message(f"❌ Błąd: {str(e)}")
            self.root.after(0, lambda: self.status_var.set(f"Błąd testowania: {str(e)}"))
        finally:
            # Wyłącz tryb testowy
            self.cleaner.set_test_mode(False)
    
    def _update_test_results(self, result):
        """Aktualizuje wyniki testu"""
        cleaned_mb = result['total_cleaned_mb']
        files_count = result['files_cleaned']
        
        message = f"""
{self.translator.get('test_complete')}
{self.translator.get('time')}: {result['start_time'].strftime('%H:%M:%S')} - {result['end_time'].strftime('%H:%M:%S')}
SYMULACJA - {self.translator.get('cleaned_size')}: {cleaned_mb:.2f} MB
{self.translator.get('files_count')}: {files_count}
{self.translator.get('log_files')}: {result['log_cleaned'] / (1024*1024):.2f} MB
{self.translator.get('large_files')}: {result['large_cleaned'] / (1024*1024):.2f} MB
        """
        
        self.clean_results.insert(tk.END, message + "\n" + "="*50 + "\n")
        self.clean_results.see(tk.END)
        
        self.status_var.set(f"Test: {cleaned_mb:.2f} MB do wyczyszczenia")
    
    def manual_cleanup(self):
        """Ręczne czyszczenie"""
        self.status_var.set(self.translator.get("status_cleaning"))
        threading.Thread(target=self._cleanup_thread, daemon=True).start()
        
    def _cleanup_thread(self):
        """Wątek czyszczenia"""
        try:
            # Wyłącz tryb testowy dla rzeczywistego czyszczenia
            self.cleaner.set_test_mode(False)
            result = self.cleaner.perform_cleanup()
            self.root.after(0, lambda: self._update_cleanup_results(result))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Błąd czyszczenia: {str(e)}"))
    
    def _update_cleanup_results(self, result):
        """Aktualizuje wyniki czyszczenia"""
        cleaned_mb = result['total_cleaned_mb']
        files_count = result['files_cleaned']
        
        message = f"""
{self.translator.get('cleaning_complete')}
{self.translator.get('time')}: {result['start_time'].strftime('%H:%M:%S')} - {result['end_time'].strftime('%H:%M:%S')}
{self.translator.get('cleaned_size')}: {cleaned_mb:.2f} MB
{self.translator.get('files_count')}: {files_count}
{self.translator.get('log_files')}: {result['log_cleaned'] / (1024*1024):.2f} MB
{self.translator.get('large_files')}: {result['large_cleaned'] / (1024*1024):.2f} MB
        """
        
        self.clean_results.insert(tk.END, message + "\n" + "="*50 + "\n")
        self.clean_results.see(tk.END)
        
        self.status_var.set(self.translator.get("status_cleaned", cleaned_mb))
        
        # Wyślij powiadomienie
        if cleaned_mb > 0:
            self.notification_manager.send_notification(
                "Inv Cleaner",
                self.translator.get("notification_cleaned", cleaned_mb, files_count)
            )
    
    def scheduled_cleanup(self):
        """Zaplanowane czyszczenie"""
        if self.is_monitoring:
            self._cleanup_thread()
    
    def toggle_monitoring(self):
        """Włącza/wyłącza monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitor_btn.config(text=self.translator.get("stop_monitoring"))
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            self.status_var.set(self.translator.get("status_monitoring_on"))
        else:
            self.is_monitoring = False
            self.monitor_btn.config(text=self.translator.get("start_monitoring"))
            self.status_var.set(self.translator.get("status_monitoring_off"))
    
    def _monitoring_loop(self):
        """Pętla monitorowania"""
        while self.is_monitoring:
            schedule.run_pending()
            time.sleep(60)  # Sprawdź co minutę
    
    def refresh_logs(self):
        """Odświeża logi"""
        try:
            if os.path.exists(self.cleaner.log_file):
                with open(self.cleaner.log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.log_text.delete(1.0, tk.END)
                    self.log_text.insert(tk.END, content)
                    self.log_text.see(tk.END)
            else:
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, self.translator.get("no_log_file"))
        except Exception as e:
            messagebox.showerror(
                self.translator.get("error"), 
                self.translator.get("cannot_read_logs", str(e))
            )
    
    def clear_logs(self):
        """Czyści logi"""
        if messagebox.askyesno(
            self.translator.get("confirmation"), 
            self.translator.get("clear_logs_confirm")
        ):
            try:
                open(self.cleaner.log_file, 'w').close()
                self.log_text.delete(1.0, tk.END)
                self.log_text.insert(tk.END, self.translator.get("logs_cleared"))
            except Exception as e:
                messagebox.showerror(
                    self.translator.get("error"), 
                    self.translator.get("cannot_clear_logs", str(e))
                )
    
    def run(self):
        """Uruchamia aplikację"""
        self.root.mainloop()

def main():
    """Główna funkcja programu"""
    # Sprawdź uprawnienia root
    if os.geteuid() != 0:
        print("⚠️  WARNING: Application should be run as root for full functionality")
        print("Use: sudo python3 main.py")
        print()
        print("🧹 Starting Inv Cleaner in limited mode...")
    
    # Utwórz i uruchom aplikację
    try:
        app = CzyscicielApp()
        app.run()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
