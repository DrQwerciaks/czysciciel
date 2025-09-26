#!/bin/bash
# run-app.sh - Prosty przewodnik uruchamiania aplikacji

echo "🚀 Inv Cleaner - Jak uruchomić aplikację"
echo "========================================"
echo ""

# Sprawdź czy snap jest zainstalowany
if ! snap list inv-cleaner &>/dev/null; then
    echo "❌ Snap inv-cleaner nie jest zainstalowany!"
    echo ""
    echo "Zainstaluj snap:"
    echo "  sudo snap install --dangerous inv-cleaner_1.0.0_amd64.snap"
    echo ""
    echo "Lub przez Snap Store (gdy będzie opublikowany):"
    echo "  sudo snap install inv-cleaner"
    exit 1
fi

echo "✅ Snap inv-cleaner jest zainstalowany"
echo ""

# Sprawdź czy uruchamiamy jako user
if [[ $EUID -eq 0 ]]; then
    echo "⚠️  UWAGA: Jesteś zalogowany jako root!"
    echo "GUI powinno działać jako zwykły użytkownik."
    echo "Przełącz się na konto użytkownika i uruchom ponownie."
    echo ""
    exit 1
fi

echo "✅ Jesteś zalogowany jako użytkownik ($USER) - dobrze!"
echo ""

# Sprawdź demon
echo "🔄 Sprawdzanie demona..."
if systemctl is-active snap.inv-cleaner.inv-cleaner-daemon &>/dev/null; then
    echo "✅ Demon działa w tle"
else
    echo "⚠️  Demon nie działa - sprawdź status:"
    echo "  sudo systemctl status snap.inv-cleaner.inv-cleaner-daemon"
fi
echo ""

# Sprawdź plugs
echo "🔌 Sprawdzanie uprawnień snap..."
PLUGS_OK=true
if ! snap connections inv-cleaner | grep -q "home.*connected" 2>/dev/null; then
    echo "⚠️  Plug 'home' nie jest podłączony"
    PLUGS_OK=false
fi

if ! snap connections inv-cleaner | grep -q "system-files.*connected" 2>/dev/null; then
    echo "⚠️  Plug 'system-files' nie jest podłączony"
    PLUGS_OK=false
fi

if $PLUGS_OK; then
    echo "✅ Uprawnienia snap są OK"
else
    echo "Podłącz brakujące uprawnienia:"
    echo "  sudo snap connect inv-cleaner:home"
    echo "  sudo snap connect inv-cleaner:system-files"
    echo ""
fi

echo ""
echo "🎯 URUCHOM APLIKACJĘ:"
echo "====================="
echo ""
echo "inv-cleaner"
echo ""
echo "🚫 NIGDY nie uruchamiaj jako root:"
echo "   sudo inv-cleaner  # ❌ ŹLE!"
echo ""
echo "📚 Więcej informacji: cat PERMISSIONS.md"
echo ""

# Zapytaj czy uruchomić
read -p "Uruchomić GUI teraz? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 Uruchamiam GUI..."
    inv-cleaner
else
    echo "👍 OK, uruchom GUI gdy będziesz gotowy: inv-cleaner"
fi
