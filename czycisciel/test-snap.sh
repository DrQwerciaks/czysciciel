#!/bin/bash
# test-snap.sh - Skrypt do testowania zainstalowanego snapa

echo "🧪 Inv Cleaner - Test zainstalowanego snapa"
echo "============================================"

# Sprawdź czy jesteś userem (nie root)
if [[ $EUID -eq 0 ]]; then
    echo "⚠️  UWAGA: Uruchamiasz test jako root!"
    echo "GUI powinno działać jako zwykły użytkownik."
    echo "Uruchom test bez sudo."
fi

# Sprawdź czy snap jest zainstalowany
if ! snap list inv-cleaner &>/dev/null; then
    echo "❌ Snap inv-cleaner nie jest zainstalowany!"
    echo "Zainstaluj go najpierw: make snap-install"
    exit 1
fi

echo "✅ Snap inv-cleaner jest zainstalowany"

# Sprawdź status snapa
echo ""
echo "📊 Status snapa:"
snap list inv-cleaner
echo ""

# Sprawdź połączenia
echo "🔌 Połączenia snapa:"
snap connections inv-cleaner
echo ""

# Test demona
echo "🔄 Status demona:"
if systemctl is-active snap.inv-cleaner.inv-cleaner-daemon &>/dev/null; then
    echo "✅ Demon działa"
    systemctl status snap.inv-cleaner.inv-cleaner-daemon --no-pager -l
else
    echo "⚠️  Demon nie działa"
    echo "Spróbuj uruchomić: sudo systemctl start snap.inv-cleaner.inv-cleaner-daemon"
fi
echo ""

# Test GUI (tylko sprawdź czy plik istnieje)
echo "🖥️  Test GUI:"
if command -v inv-cleaner &>/dev/null; then
    echo "✅ Komenda inv-cleaner dostępna"
    echo "Możesz uruchomić GUI komendą: inv-cleaner"
else
    echo "❌ Komenda inv-cleaner niedostępna"
fi
echo ""

# Sprawdź logi
echo "📋 Logi aplikacji:"
LOG_DIR="$HOME/.config/inv-cleaner"
if [[ -d "$LOG_DIR" ]]; then
    echo "✅ Katalog logów istnieje: $LOG_DIR"
    if [[ -f "$LOG_DIR/inv-cleaner.log" ]]; then
        echo "📄 Ostatnie 10 linii logu:"
        tail -10 "$LOG_DIR/inv-cleaner.log"
    else
        echo "ℹ️  Plik logu jeszcze nie istnieje"
    fi
else
    echo "ℹ️  Katalog logów jeszcze nie istnieje"
fi
echo ""

# Test konfiguracji
echo "⚙️  Konfiguracja:"
CONFIG_FILE="$HOME/.config/inv-cleaner/config.json"
if [[ -f "$CONFIG_FILE" ]]; then
    echo "✅ Plik konfiguracyjny istnieje: $CONFIG_FILE"
else
    echo "ℹ️  Plik konfiguracyjny nie istnieje, zostanie utworzony przy pierwszym uruchomieniu"
fi
echo ""

echo "🎯 Jak uruchomić aplikację:"
echo "1. GUI (jako zwykły user): inv-cleaner"
echo "2. NIGDY nie używaj: sudo inv-cleaner"
echo "3. Demon działa automatycznie w tle"
echo ""
echo "📚 Przeczytaj PERMISSIONS.md aby zrozumieć uprawnienia"
echo ""
echo "🔍 Sprawdzanie uprawnień:"
if [[ $EUID -eq 0 ]]; then
    echo "❌ Test uruchomiony jako root - GUI powinno działać jako user"
else
    echo "✅ Test uruchomiony jako user - poprawnie dla GUI"
fi
echo ""
echo "✅ Test snapa zakończony!"
