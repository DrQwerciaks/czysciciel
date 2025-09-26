#!/bin/bash
# -*- coding: utf-8 -*-
# Skrypt odinstalowujący Czysciciel Dysku

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

echo_info "=== Odinstalowywanie Czysciciela Dysku ==="

# Zatrzymaj i wyłącz usługę
if command -v systemctl &> /dev/null; then
    echo_info "Zatrzymywanie usługi..."
    systemctl stop czysciciel.service 2>/dev/null || true
    systemctl disable czysciciel.service 2>/dev/null || true
    rm -f /etc/systemd/system/czysciciel.service
    systemctl daemon-reload
fi

# Usuń pliki
echo_info "Usuwanie plików..."
rm -rf /opt/czysciciel
rm -f /usr/local/bin/czysciciel-gui
rm -f /usr/share/applications/czysciciel.desktop
rm -f /etc/logrotate.d/czysciciel

# Usuń konfigurację (opcjonalnie)
read -p "Czy chcesz usunąć konfigurację i logi? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf /etc/czysciciel
    rm -f /var/log/czysciciel*.log
    rm -f /var/log/czysciciel-stats.json
    echo_info "Konfiguracja i logi zostały usunięte"
fi

# Usuń PID file
rm -f /var/run/czysciciel.pid

echo_success "Odinstalowywanie zakończone!"
echo_info "Zależności Python (matplotlib, numpy, schedule) pozostały zainstalowane"
