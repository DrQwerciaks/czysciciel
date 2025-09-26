# Inv Cleaner 🧹💾

**Advanced disk cleaner and monitoring tool for Linux systems**

[![Build Status](https://github.com/YOUR_USERNAME/inv-cleaner/workflows/Build%20and%20Release/badge.svg)](https://github.com/YOUR_USERNAME/inv-cleaner/actions)
[![Snap Store](https://snapcraft.io/inv-cleaner/badge.svg)](https://snapcraft.io/inv-cleaner)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Inv Cleaner is a powerful disk cleaning and monitoring application for Linux systems, similar to Baobab but with advanced automatic cleanup features. It provides visual disk usage analysis and intelligent cleanup of old logs, temporary files, and large unused files.

![Inv Cleaner Screenshot](assets/screenshot.png)

## 🌟 Key Features

### 📊 Analiza Dysku
- **Wizualizacja wykorzystania dysku** - wykres kołowy podobny do Baobab
- **Szczegółowa analiza katalogów** - rozmiary w MB/GB
- **Lista największych plików i folderów**

### 🛠️ Automatyczne Czyszczenie
- **Pliki logów** - usuwa pliki starsze niż 7 dni z `/var/log`
- **Pliki tymczasowe** - czyści `/tmp` i `/var/tmp`
- **Duże pliki** - usuwa pliki większe niż 200MB z katalogów temp
- **Konfigurowalne kryteria** - dostosuj wiek plików i rozmiar

### 🔔 Powiadomienia
- **Powiadomienia systemowe** - informacje o wyczyszczonych plikach
- **Szczegółowe logi** - wszystkie operacje zapisywane do logów
- **Statystyki** - ile MB/GB zostało wyczyszczone

### ⚙️ Działanie w Tle
- **Demon systemd** - działa jako usługa systemowa
- **Harmonogram** - automatyczne czyszczenie co godzinę
- **Działanie jako root** - pełny dostęp do plików systemowych

### 🖥️ Interfejs Graficzny
- **Nowoczesny GUI** - intuicyjny interfejs użytkownika
- **Zakładki** - analiza, czyszczenie, logi, ustawienia
- **Monitoring w czasie rzeczywistym** - obserwuj działanie aplikacji

## � Quick Installation

### Option 1: Snap Store (Recommended)
```bash
sudo snap install inv-cleaner
```

### Option 2: Quick Install from GitHub
```bash
curl -L https://raw.githubusercontent.com/YOUR_USERNAME/inv-cleaner/main/quick-install.sh | sudo bash
```

### Option 3: Download and Install
```bash
# Download latest release
wget https://github.com/YOUR_USERNAME/inv-cleaner/releases/latest/download/install.sh
chmod +x install.sh
sudo ./install.sh
```

## 📋 Requirements

- **System operacyjny**: Linux (Ubuntu, Debian, CentOS, Fedora)
- **Python**: 3.6 lub nowszy
- **Uprawnienia**: root (dla pełnej funkcjonalności)
- **Pakiety systemowe**: python3, python3-pip, python3-tk, libnotify-bin

## 🚀 Instalacja

### Automatyczna Instalacja

```bash
# Sklonuj repozytorium
git clone <repo-url>
cd czycisciel

# Uruchom instalator (wymaga root)
sudo chmod +x install.sh
sudo ./install.sh
```

### Ręczna Instalacja

```bash
# Zainstaluj zależności systemowe
# Ubuntu/Debian:
sudo apt update
sudo apt install python3 python3-pip python3-tk libnotify-bin

# CentOS/RHEL:
sudo yum install python3 python3-pip tkinter libnotify

# Fedora:
sudo dnf install python3 python3-pip python3-tkinter libnotify

# Zainstaluj zależności Python
pip3 install matplotlib numpy schedule

# Skopiuj pliki
sudo mkdir -p /opt/czysciciel
sudo cp *.py /opt/czysciciel/
sudo chmod +x /opt/czysciciel/*.py

# Zainstaluj usługę systemd
sudo cp czysciciel.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable czysciciel.service
sudo systemctl start czysciciel.service
```

## 💻 Użytkowanie

### GUI Aplikacja

```bash
# Uruchom interfejs graficzny
czysciciel-gui

# Lub bezpośrednio
sudo python3 /opt/czysciciel/main.py
```

### Funkcje GUI:
- **Analiza Dysku**: Skanuj i zobacz wykres wykorzystania
- **Czyszczenie**: Ręczne lub automatyczne czyszczenie
- **Logi**: Przeglądaj historię operacji
- **Ustawienia**: Dostosuj parametry czyszczenia

### Demon w Tle

```bash
# Status usługi
sudo systemctl status czysciciel

# Uruchom/zatrzymaj usługę
sudo systemctl start czysciciel
sudo systemctl stop czysciciel

# Logi demona
journalctl -u czysciciel -f

# Logi aplikacji
sudo tail -f /var/log/czysciciel*.log
```

### Konfiguracja

Edytuj `/etc/czysciciel/config.json`:

```json
{
    "cleaning_enabled": true,
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
    "notifications_enabled": true,
    "preserve_files": [
        "*.conf",
        "*.cfg",
        "*.config",
        "*.json"
    ]
}
```

## 📊 Parametry Konfiguracji

| Parametr | Opis | Domyślna wartość |
|----------|------|------------------|
| `cleaning_enabled` | Włącza/wyłącza czyszczenie | `true` |
| `scan_interval_hours` | Częstotliwość skanowania (godz.) | `1` |
| `days_old` | Wiek plików do usunięcia (dni) | `7` |
| `large_file_mb` | Rozmiar "dużych" plików (MB) | `200` |
| `directories_to_clean` | Katalogi do czyszczenia | `/var/log`, `/tmp`, `/var/tmp` |
| `directories_to_scan` | Katalogi do skanowania | Rozszerzona lista |
| `notifications_enabled` | Włącza powiadomienia | `true` |
| `preserve_files` | Wzorce plików do zachowania | `*.conf`, `*.cfg`, etc. |

## 📈 Logi i Monitoring

### Lokalizacje Logów

- **Demon**: `/var/log/czysciciel-daemon.log`
- **Główne logi**: `/var/log/czysciciel.log`
- **Statystyki**: `/var/log/czysciciel-stats.json`
- **Systemd**: `journalctl -u czysciciel`

### Przykładowe Powiadomienia

```
🧹 Czysciciel Dysku
Wyczyszczono 938 MB z folderu /var/log
Usunięto 156 plików logów starszych niż 7 dni
```

## 🔧 Rozwiązywanie Problemów

### Aplikacja nie uruchamia się
```bash
# Sprawdź zależności
python3 -c "import matplotlib, numpy, tkinter"

# Sprawdź uprawnienia
sudo python3 /opt/czysciciel/main.py
```

### Demon nie działa
```bash
# Sprawdź status
sudo systemctl status czysciciel

# Sprawdź logi
journalctl -u czysciciel -n 50

# Uruchom ręcznie w trybie debug
sudo python3 /opt/czysciciel/daemon.py
```

### Brak powiadomień
```bash
# Sprawdź notify-send
notify-send "Test" "Test powiadomienia"

# Zainstaluj libnotify
sudo apt install libnotify-bin  # Ubuntu/Debian
```

### Problemy z uprawnieniami
```bash
# Sprawdź czy działa jako root
whoami

# Sprawdź uprawnienia plików
ls -la /opt/czysciciel/
ls -la /var/log/czysciciel*
```

## 🗑️ Odinstalowanie

```bash
# Użyj skryptu odinstalowującego
sudo chmod +x uninstall.sh
sudo ./uninstall.sh

# Lub ręcznie
sudo systemctl stop czysciciel
sudo systemctl disable czysciciel
sudo rm -rf /opt/czysciciel
sudo rm -f /etc/systemd/system/czysciciel.service
sudo systemctl daemon-reload
```

## 🛡️ Bezpieczeństwo

- ✅ **Bezpieczne usuwanie** - sprawdza czy pliki istnieją przed usunięciem
- ✅ **Zachowywanie konfiguracji** - nie usuwa ważnych plików systemowych
- ✅ **Logi wszystkich operacji** - pełna audytowalność
- ✅ **Konfigurowalne wzorce** - możesz określić co zachować
- ⚠️ **Wymaga root** - potrzebne do dostępu do katalogów systemowych

## 📝 Przykłady Użycia

### Jednorazowe czyszczenie
```bash
# Uruchom GUI i kliknij "Wyczyść Teraz"
czysciciel-gui
```

### Monitoring w czasie rzeczywistym
```bash
# Obserwuj logi na żywo
sudo tail -f /var/log/czysciciel-daemon.log
```

### Dostosowanie czyszczenia
```bash
# Edytuj konfigurację
sudo nano /etc/czysciciel/config.json

# Zrestartuj usługę
sudo systemctl restart czysciciel
```

## 🏗️ Architektura

```
Czysciciel Dysku
├── main.py           # GUI aplikacja
├── daemon.py         # Demon działający w tle
├── install.sh        # Skrypt instalacyjny
├── uninstall.sh      # Skrypt odinstalowujący
├── czysciciel.service # Plik usługi systemd
└── requirements.txt   # Zależności Python

/opt/czysciciel/       # Pliki aplikacji
/etc/czysciciel/       # Konfiguracja
/var/log/czysciciel*   # Logi
```

## 🤝 Wkład

Zgłaszaj błędy i sugestie przez Issues. Pull requesty są mile widziane!

## 📄 Licencja

MIT License - możesz swobodnie używać, modyfikować i dystrybuować.

---

**Uwaga**: Aplikacja działa jako root i może usuwać pliki systemowe. Zawsze testuj na środowisku testowym przed użyciem na serwerach produkcyjnych.

🧹 **Czyść z głową, nie z problemami!** 💾

## 🔧 Building from Source

### Prerequisites
- Linux system (Ubuntu 18.04+, Debian 10+, etc.)
- Python 3.8+
- snapcraft (for building snap packages)

### Quick Build Commands

```bash
# Build and test locally
make build
make test
make run

# Build snap package (Linux only)
make snap

# Install snap locally
make snap-install

# Test snap installation
./test-snap.sh
```

### Manual Build Process

#### 1. Clone and Setup
```bash
git clone https://github.com/YOUR_USERNAME/inv-cleaner.git
cd inv-cleaner

# Install dependencies
pip3 install -r requirements.txt
```

#### 2. Build Snap Package
```bash
# Install snapcraft
sudo snap install snapcraft --classic

# Build snap
./build-snap.sh
# or
snapcraft
```

#### 3. Install and Test
```bash
# Install snap locally
sudo snap install --dangerous inv-cleaner_1.0.0_amd64.snap

# Run GUI
inv-cleaner

# Test daemon
sudo systemctl status snap.inv-cleaner.inv-cleaner-daemon

# Run tests
./test-snap.sh
```

### All Available Make Commands

```bash
make help           # Show all available commands
make build          # Build application
make clean          # Clean build artifacts
make test           # Run tests
make snap           # Build snap package
make snap-install   # Install snap locally
make snap-remove    # Remove snap
make format         # Format code
make lint           # Lint code
make dev-setup      # Setup development environment
```

### Traditional Installation