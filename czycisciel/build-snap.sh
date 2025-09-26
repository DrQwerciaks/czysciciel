#!/bin/bash
# build-snap.sh - Skrypt pomocniczy do budowania snapa

set -e

echo "🔧 Inv Cleaner - Budowanie paczki snap"
echo "======================================"

# Sprawdź czy jesteś na Linuxie
if [[ "$(uname)" != "Linux" ]]; then
    echo "❌ Błąd: Snap może być zbudowany tylko na Linuxie!"
    echo "Proszę przenieść projekt na system Linux i uruchomić tam ten skrypt."
    exit 1
fi

# Sprawdź czy snapcraft jest zainstalowany
if ! command -v snapcraft &> /dev/null; then
    echo "📦 Instaluję snapcraft..."
    sudo snap install snapcraft --classic
fi

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [[ ! -f "snapcraft.yaml" ]]; then
    echo "❌ Błąd: Nie znaleziono pliku snapcraft.yaml"
    echo "Uruchom skrypt z katalogu głównego projektu."
    exit 1
fi

echo "🏗️  Rozpoczynam budowanie snapa..."

# Najpierw spróbuj z głównym snapcraft.yaml
echo "📄 Próbuję z głównym snapcraft.yaml..."
if snapcraft 2>/dev/null; then
    echo "✅ Budowanie z głównym snapcraft.yaml zakończone sukcesem!"
else
    echo "⚠️  Główny snapcraft.yaml nie zadziałał, próbuję z fallback..."
    
    # Spróbuj z fallback
    if [[ -f "snapcraft-fallback.yaml" ]]; then
        echo "📄 Używam snapcraft-fallback.yaml..."
        cp snapcraft.yaml snapcraft.yaml.bak
        cp snapcraft-fallback.yaml snapcraft.yaml
        
        if snapcraft; then
            echo "✅ Budowanie z fallback snapcraft.yaml zakończone sukcesem!"
        else
            echo "❌ Również fallback nie zadziałał"
            # Przywróć oryginalny plik
            mv snapcraft.yaml.bak snapcraft.yaml
            exit 1
        fi
        
        # Przywróć oryginalny plik
        mv snapcraft.yaml.bak snapcraft.yaml
    else
        echo "❌ Brak pliku fallback"
        exit 1
    fi
fi

# Znajdź zbudowany plik snap
SNAP_FILE=$(ls *.snap 2>/dev/null | head -n 1)

if [[ -n "$SNAP_FILE" ]]; then
    echo "✅ Snap zbudowany pomyślnie: $SNAP_FILE"
    echo ""
    echo "🚀 Następne kroki:"
    echo "1. Zainstaluj snap lokalnie:"
    echo "   sudo snap install --dangerous $SNAP_FILE"
    echo ""
    echo "2. Uruchom aplikację:"
    echo "   inv-cleaner"
    echo ""
    echo "3. Sprawdź demon:"
    echo "   sudo systemctl status snap.inv-cleaner.inv-cleaner-daemon"
    echo ""
    echo "4. Sprawdź logi:"
    echo "   cat ~/.config/inv-cleaner/inv-cleaner.log"
else
    echo "❌ Błąd: Nie znaleziono zbudowanego pliku snap"
    exit 1
fi
