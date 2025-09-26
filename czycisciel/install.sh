#!/bin/bash
# -*- coding: utf-8 -*-
# Skrypt instalacyjny dla Czysciciela Dysku
# Autor: System Administrator

set -e

# Kolory dla output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

echo_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

echo_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Sprawdź uprawnienia root
if [[ $EUID -ne 0 ]]; then
   echo_error "Ten skrypt musi być uruchomiony jako root"
   echo "Użyj: sudo $0"
   exit 1
fi

echo_info "=== Instalator Czysciciela Dysku ==="
echo_info "Rozpoczynam instalację..."

# Sprawdź system operacyjny
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo_info "Wykryto system Linux"
else
    echo_warning "System nie jest w pełni wspierany, kontynuuję instalację..."
fi

# Sprawdź czy Python3 jest zainstalowany
if ! command -v python3 &> /dev/null; then
    echo_error "Python3 nie jest zainstalowany!"
    echo_info "Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo_info "CentOS/RHEL: sudo yum install python3 python3-pip tkinter"
    echo_info "Fedora: sudo dnf install python3 python3-pip python3-tkinter"
    exit 1
fi

# Sprawdź czy pip jest zainstalowany
if ! command -v pip3 &> /dev/null; then
    echo_error "pip3 nie jest zainstalowany!"
    echo_info "Ubuntu/Debian: sudo apt install python3-pip"
    echo_info "CentOS/RHEL: sudo yum install python3-pip"
    exit 1
fi

# Utwórz katalogi
echo_info "Tworzenie katalogów..."
mkdir -p /opt/czysciciel
mkdir -p /etc/czysciciel
mkdir -p /var/log
mkdir -p /var/run

# Kopiuj pliki
echo_info "Kopiowanie plików..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cp "$SCRIPT_DIR/main.py" /opt/czysciciel/
cp "$SCRIPT_DIR/daemon.py" /opt/czysciciel/
cp "$SCRIPT_DIR/requirements.txt" /opt/czysciciel/
cp "$SCRIPT_DIR/czysciciel.service" /etc/systemd/system/

# Nadaj uprawnienia
echo_info "Ustawianie uprawnień..."
chmod +x /opt/czysciciel/main.py
chmod +x /opt/czysciciel/daemon.py
chmod 644 /etc/systemd/system/czysciciel.service

# Zainstaluj zależności Python
echo_info "Instalowanie zależności Python..."
pip3 install -r /opt/czysciciel/requirements.txt

# Sprawdź czy systemd jest dostępny
if command -v systemctl &> /dev/null; then
    echo_info "Konfigurowanie usługi systemd..."
    systemctl daemon-reload
    systemctl enable czysciciel.service
    
    echo_info "Uruchamianie usługi..."
    systemctl start czysciciel.service
    
    echo_success "Usługa została uruchomiona!"
    systemctl status czysciciel.service --no-pager
else
    echo_warning "systemd nie jest dostępny, uruchom demon ręcznie:"
    echo "sudo python3 /opt/czysciciel/daemon.py &"
fi

# Utwórz skrypt uruchamiający GUI
echo_info "Tworzenie skryptu uruchamiającego GUI..."
cat > /usr/local/bin/czysciciel-gui << 'EOF'
#!/bin/bash
# Uruchamiacz GUI Czysciciela Dysku

if [[ $EUID -ne 0 ]]; then
   echo "Aplikacja wymaga uprawnień root dla pełnej funkcjonalności"
   echo "Uruchamianie z sudo..."
   exec sudo python3 /opt/czysciciel/main.py "$@"
else
   exec python3 /opt/czysciciel/main.py "$@"
fi
EOF

chmod +x /usr/local/bin/czysciciel-gui

# Utwórz plik desktop dla GUI
echo_info "Tworzenie pliku .desktop..."
cat > /usr/share/applications/czysciciel.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Name=Czysciciel Dysku
Comment=Monitor i czyszczenie dysku
Exec=sudo /usr/local/bin/czysciciel-gui
Icon=applications-system
Terminal=false
Type=Application
Categories=System;Utility;
Keywords=disk;cleaner;monitor;system;
EOF

# Utwórz konfigurację logrotate
echo_info "Konfigurowanie logrotate..."
cat > /etc/logrotate.d/czysciciel << 'EOF'
/var/log/czysciciel*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
    maxage 30
}
EOF

# Utwórz domyślną konfigurację
echo_info "Tworzenie domyślnej konfiguracji..."
cat > /etc/czysciciel/config.json << 'EOF'
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
EOF

# Zainstaluj notify-send jeśli nie istnieje
if ! command -v notify-send &> /dev/null; then
    echo_info "Instalowanie notify-send..."
    if command -v apt &> /dev/null; then
        apt install -y libnotify-bin
    elif command -v yum &> /dev/null; then
        yum install -y libnotify
    elif command -v dnf &> /dev/null; then
        dnf install -y libnotify
    else
        echo_warning "Nie można zainstalować notify-send automatycznie"
    fi
fi

echo_success "=== Instalacja zakończona pomyślnie! ==="
echo
echo_info "Dostępne komendy:"
echo "  • GUI aplikacja: czysciciel-gui"
echo "  • Status usługi: systemctl status czysciciel"
echo "  • Logi demona: journalctl -u czysciciel -f"
echo "  • Logi aplikacji: tail -f /var/log/czysciciel*.log"
echo "  • Konfiguracja: /etc/czysciciel/config.json"
echo
echo_info "Demon działa w tle i będzie czyścił dysk co godzinę"
echo_info "Uruchom 'czysciciel-gui' aby otworzyć interfejs graficzny"
echo

# Test powiadomienia
echo_info "Testowanie powiadomień..."
if command -v notify-send &> /dev/null; then
    notify-send "Czysciciel Dysku" "Instalacja zakończona pomyślnie!" 2>/dev/null || true
    echo_success "Powiadomienia działają"
else
    echo_warning "Powiadomienia mogą nie działać poprawnie"
fi

echo_success "Gotowe!"
