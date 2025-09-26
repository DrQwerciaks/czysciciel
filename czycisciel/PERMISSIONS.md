# 🔐 Inv Cleaner - Uprawnienia i Bezpieczeństwo

## Jak działa system uprawnień?

### 👤 GUI (Interfejs Użytkownika)
- **Działa jako zwykły użytkownik** (nie root)
- **Nie potrzebuje sudo** - uruchamiasz normalnie: `inv-cleaner`
- **Dostęp tylko do katalogu użytkownika**: `~/.config/inv-cleaner/`
- **Bezpieczne** - nie może uszkodzić systemu

### 🤖 Daemon (Usługa w Tle)
- **Działa jako root** - automatycznie przez snap
- **Uruchamiany przez systemd** - nie musisz nic robić
- **Dostęp do katalogów systemowych**: `/var/log`, `/tmp`, itp.
- **Działanie w tle** - stale monitoruje i czyści dysk

## 🚀 Jak uruchomić aplikację?

### Po zainstalowaniu snap:

```bash
# 1. Uruchom GUI (jako zwykły user - NIE SUDO!)
inv-cleaner

# 2. Demon działa automatycznie w tle
# (nie musisz go uruchamiać - snap się tym zajmuje)
```

### ⚠️ WAŻNE - NIE UŻYWAJ SUDO dla GUI!

```bash
# ✅ DOBRZE:
inv-cleaner

# ❌ ŹLE:
sudo inv-cleaner  # GUI nie powinno działać jako root!
```

## 🔍 Sprawdzanie statusu

### Sprawdź czy wszystko działa:

```bash
# Status całego snapa
snap list inv-cleaner

# Status demona
systemctl status snap.inv-cleaner.inv-cleaner-daemon

# Logi demona (działa jako root)
sudo journalctl -u snap.inv-cleaner.inv-cleaner-daemon -f

# Logi GUI (plik użytkownika)
tail -f ~/.config/inv-cleaner/inv-cleaner.log
```

## 📁 Gdzie co jest zapisane?

### Pliki użytkownika:
```
~/.config/inv-cleaner/
├── config.json          # Twoja konfiguracja
├── inv-cleaner.log       # Logi GUI
└── cache/               # Cache aplikacji
```

### Pliki systemowe (demon):
```
/etc/inv-cleaner/
├── config.json          # Konfiguracja demona

/var/log/inv-cleaner/
├── daemon.log            # Logi demona
└── cleanup.log          # Logi czyszczenia
```

## 🛡️ Bezpieczeństwo

### Co może GUI?
- ✅ Wyświetlać analizę dysku
- ✅ Pokazywać logi
- ✅ Edytować ustawienia użytkownika
- ❌ NIE może czyścić plików systemowych
- ❌ NIE ma dostępu do `/var/log` itp.

### Co może demon?
- ✅ Czyścić pliki systemowe (`/var/log`, `/tmp`)
- ✅ Usuwać duże pliki tymczasowe
- ✅ Zapisywać logi systemowe
- ✅ Wysyłać powiadomienia systemowe

## 🔧 Rozwiązywanie problemów

### Problem: GUI prosi o hasło sudo
```bash
# To oznacza że uruchamiasz GUI jako root - nie rób tego!
# Uruchom jako zwykły user:
inv-cleaner  # bez sudo
```

### Problem: Demon nie działa
```bash
# Sprawdź status
systemctl status snap.inv-cleaner.inv-cleaner-daemon

# Uruchom ponownie
sudo systemctl restart snap.inv-cleaner.inv-cleaner-daemon

# Sprawdź logi
sudo journalctl -u snap.inv-cleaner.inv-cleaner-daemon --no-pager -l
```

### Problem: Brak uprawnień
```bash
# Podłącz plugs snap
sudo snap connect inv-cleaner:system-files
sudo snap connect inv-cleaner:home
sudo snap connect inv-cleaner:log-observe
```

### Problem: GUI nie widzi plików
```bash
# To normalne! GUI jako user nie może widzieć plików systemowych
# Demon w tle robi czyszczenie - sprawdź logi demona
```

## 📊 Monitorowanie działania

### Sprawdź co się dzieje:
```bash
# 1. Czy demon czyści pliki?
sudo tail -f /var/log/inv-cleaner/cleanup.log

# 2. Ile miejsca zwolniono?
grep "Cleaned" /var/log/inv-cleaner/cleanup.log | tail -10

# 3. Czy GUI działa?
tail -f ~/.config/inv-cleaner/inv-cleaner.log

# 4. Powiadomienia systemowe
journalctl --user -f | grep notify
```

## ✅ Normalny przepływ pracy

1. **Instalujesz snap** - demon automatycznie się uruchamia
2. **Demon pracuje w tle** - czyści co godzinę automatycznie
3. **Uruchamiasz GUI** jako user - `inv-cleaner`
4. **GUI pokazuje statystyki** tego co demon wyczyścił
5. **Wszystko działa bezpiecznie** - każdy komponent ma swoje uprawnienia

To jest **bezpieczny i przemyślany system** gdzie GUI i demon działają z odpowiednimi uprawnieniami!
