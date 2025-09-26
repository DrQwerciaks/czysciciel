# 🐧 Instrukcje budowania snapa na Linuxie

## Wymagania
- System Linux (Ubuntu 18.04+, Debian 10+, lub inna dystrybucja z snapd)
- snapcraft zainstalowany

## 1. Instalacja snapcraft

```bash
sudo snap install snapcraft --classic
```

## 2. Przeniesienie projektu

### Opcja A: Przez git (jeśli projekt jest w repozytorium)
```bash
git clone https://github.com/TwojaNazwa/inv-cleaner.git
cd inv-cleaner
```

### Opcja B: Przez rsync/scp (z macOS na Linux)
```bash
# Na macOS:
rsync -avz /Users/drqwerciak/skrypty/czycisciel/ uzytkownik@linux-host:/home/uzytkownik/inv-cleaner/

# Lub scp:
scp -r /Users/drqwerciak/skrypty/czycisciel/ uzytkownik@linux-host:/home/uzytkownik/inv-cleaner/
```

### Opcja C: Archiwum tar
```bash
# Na macOS:
cd /Users/drqwerciak/skrypty
tar -czf inv-cleaner.tar.gz czycisciel/

# Następnie przenieś plik i rozpakuj na Linuxie:
# scp inv-cleaner.tar.gz uzytkownik@linux-host:
# Na Linuxie:
tar -xzf inv-cleaner.tar.gz
cd czycisciel/
```

## 3. Budowanie snapa

```bash
cd inv-cleaner  # lub czycisciel/
snapcraft
```

To utworzy plik `.snap` w tym katalogu (np. `inv-cleaner_1.0.0_amd64.snap`).

## 4. Instalacja snapa lokalnie

```bash
sudo snap install --dangerous inv-cleaner_1.0.0_amd64.snap
```

## 5. Test aplikacji

### Uruchomienie GUI:
```bash
inv-cleaner
```

### Sprawdzenie demona:
```bash
sudo systemctl status snap.inv-cleaner.inv-cleaner-daemon
```

### Test trybu testowego:
```bash
inv-cleaner-test
```

## 6. Sprawdzenie logów

```bash
# Logi GUI:
journalctl --user-unit=snap.inv-cleaner.inv-cleaner

# Logi demona:
sudo journalctl -u snap.inv-cleaner.inv-cleaner-daemon

# Logi aplikacji:
cat ~/.config/inv-cleaner/inv-cleaner.log
```

## 7. Usunięcie (jeśli potrzebne)

```bash
sudo snap remove inv-cleaner
```

## Rozwiązywanie problemów

### Problem z uprawnieniami:
```bash
sudo snap connect inv-cleaner:system-files
sudo snap connect inv-cleaner:home
```

### Problem z GUI:
```bash
export DISPLAY=:0
inv-cleaner
```

### Sprawdzenie statusu snapa:
```bash
snap list | grep inv-cleaner
snap connections inv-cleaner
```

## Publikacja do Snap Store (opcjonalnie)

1. Załóż konto na https://snapcraft.io/
2. Zaloguj się:
   ```bash
   snapcraft login
   ```
3. Wyślij snap:
   ```bash
   snapcraft upload inv-cleaner_1.0.0_amd64.snap
   ```

## Automatyczne budowanie przez GitHub Actions

Projekt zawiera już konfigurację GitHub Actions w `.github/workflows/build.yml` która automatycznie zbuduje snap przy każdym pushu do głównej gałęzi.
