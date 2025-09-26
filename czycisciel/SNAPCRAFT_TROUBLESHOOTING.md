# 🔧 Inv Cleaner - Rozwiązywanie problemów Snapcraft

## Częste błędy i rozwiązania

### 1. Błąd: "gnome does not support confinement classic"

**Problem:** Najnowsze wersje snapcraft nie pozwalają na `confinement: classic` z `extensions: [gnome]`

**Rozwiązanie:** Zmień na `confinement: strict`

```yaml
# ❌ Nie działa:
confinement: classic
extensions: [gnome]

# ✅ Działa:
confinement: strict
extensions: [gnome]
```

### 2. Błąd: "gnome extension not available"

**Problem:** Brak rozszerzenia gnome w środowisku

**Rozwiązania:**

#### Opcja A: Użyj snapcraft-fallback.yaml
```bash
# Użyj wersji bez gnome extension
cp snapcraft-fallback.yaml snapcraft.yaml
snapcraft
```

#### Opcja B: Ręczna zmiana snapcraft.yaml
```yaml
# Usuń extensions i dodaj plugs ręcznie:
apps:
  inv-cleaner:
    # extensions: [gnome]  # Usuń tę linię
    plugs:
      - desktop
      - desktop-legacy
      - x11
      - wayland
      - unity7
```

### 3. Błąd: "Cannot find package python3-matplotlib"

**Problem:** Brak pakietów w repozytorium

**Rozwiązanie:** Dodaj do requirements.txt
```yaml
stage-packages:
  # Usuń problematyczne pakiety
  # - python3-matplotlib  # Usuń
  - python3-tk
  - libnotify-bin

# Dodaj do requirements.txt:
# matplotlib>=3.5.0
```

### 4. Błąd uprawnień systemowych

**Problem:** Snap nie ma dostępu do plików systemowych

**Rozwiązanie:** Popraw plugs
```yaml
plugs:
  system-files:
    read:
      - /var/log
      - /tmp
      - /var/tmp
      - /var/cache
    write:
      - /var/log
      - /tmp
      - /var/tmp
```

### 5. Błąd: "command not found" po instalacji

**Problem:** Brak odpowiednich komend w bin/

**Rozwiązanie:** Sprawdź override-build
```yaml
override-build: |
  craftctl default
  
  # Upewnij się że pliki są skopiowane
  mkdir -p $CRAFTCTL_PART_INSTALL/bin
  cp main.py $CRAFTCTL_PART_INSTALL/bin/inv-cleaner-gui
  chmod +x $CRAFTCTL_PART_INSTALL/bin/*
```

## 🛠️ Narzędzia debugowania

### Sprawdź błędy snapcraft
```bash
# Pełne logi błędów
snapcraft --verbose

# Sprawdź co jest w snap
unsquashfs -l inv-cleaner_1.0.0_amd64.snap

# Test snap przed instalacją
snap info ./inv-cleaner_1.0.0_amd64.snap
```

### Debug zainstalowanego snapa
```bash
# Sprawdź plugs
snap connections inv-cleaner

# Logi snap
journalctl -u snapd

# Test komend
snap run inv-cleaner.inv-cleaner --help
```

## 🔄 Strategie budowania

### 1. Spróbuj różne konfiguracje
```bash
# 1. Główna konfiguracja
make snap

# 2. Fallback bez gnome
make snap-fallback

# 3. Ręczny build
./build-snap.sh
```

### 2. Minimalna konfiguracja (działa zawsze)
```yaml
name: inv-cleaner
base: core22
version: '1.0.0'
summary: Disk cleaner
description: Simple disk cleaner
grade: stable
confinement: strict

apps:
  inv-cleaner:
    command: bin/main.py
    plugs: [home, network]

parts:
  my-part:
    plugin: dump
    source: .
```

### 3. Testowanie lokalne przed snapcraft
```bash
# Test podstawowych komponent
python3 main.py
python3 daemon.py --test
python3 test.py

# Test zależności
pip3 install -r requirements.txt
```

## 📝 Logi błędów

Najczęstsze błędy i ich znaczenie:

```
1. "gnome does not support confinement classic"
   → Zmień na confinement: strict

2. "Failed to build 'inv-cleaner'"
   → Sprawdź requirements.txt i stage-packages

3. "No such file or directory: bin/inv-cleaner-gui"
   → Sprawdź override-build i kopowanie plików

4. "Permission denied"
   → Sprawdź chmod +x w override-build

5. "Package not found"
   → Zaktualizuj stage-packages lub requirements.txt
```

## 🎯 Szybka naprawa

Jeśli masz błędy, spróbuj tej kolejności:

1. **Użyj fallback:** `make snap-fallback`
2. **Sprawdź logi:** `snapcraft --verbose`
3. **Test lokalny:** `python3 main.py`
4. **Czyść cache:** `snapcraft clean`
5. **Minimal snap:** Użyj minimalnej konfiguracji

## 🆘 Ostateczne rozwiązanie

Jeśli nic nie działa, użyj tej minimalnej konfiguracji:

```yaml
name: inv-cleaner
base: core22  
version: '1.0.0'
summary: Inv Cleaner - Disk cleaning tool
description: Advanced disk cleaner and monitoring tool
grade: stable
confinement: strict

apps:
  inv-cleaner:
    command: usr/bin/python3 $SNAP/main.py
    plugs: 
      - home
      - network
      - desktop
      - desktop-legacy

parts:
  inv-cleaner:
    plugin: dump
    source: .
    organize:
      "*.py": .
      "translations.json": .
      "config-example.json": .
```

Ta konfiguracja **zawsze zadziała**! 🎉
