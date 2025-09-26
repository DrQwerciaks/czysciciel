# Inv Cleaner - Makefile for building and packaging

.PHONY: all build clean install uninstall snap test lint format

# Variables
APP_NAME = inv-cleaner
VERSION = 1.0.0
PYTHON = python3
PIP = pip3

# Default target
all: build

# Install dependencies
deps:
	@echo "📦 Installing dependencies..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

# Build the application
build: deps
	@echo "🔨 Building Inv Cleaner..."
	$(PYTHON) -m py_compile main.py
	$(PYTHON) -m py_compile daemon.py
	$(PYTHON) -m py_compile test.py
	@echo "✅ Build complete"

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.snap
	@echo "✅ Cleaned"

# Install locally (requires sudo)
install: build
	@echo "📥 Installing Inv Cleaner locally..."
	sudo ./install.sh
	@echo "✅ Installation complete"

# Uninstall (requires sudo)
uninstall:
	@echo "🗑️  Uninstalling Inv Cleaner..."
	sudo ./uninstall.sh
	@echo "✅ Uninstallation complete"

# Build snap package
snap: clean
	@echo "📦 Building snap package..."
	@which snapcraft >/dev/null || (echo "❌ snapcraft not found. Install with: sudo snap install snapcraft --classic" && exit 1)
	@echo "🔧 Trying main snapcraft.yaml..."
	@if snapcraft 2>/dev/null; then \
		echo "✅ Main snapcraft.yaml worked!"; \
	else \
		echo "⚠️  Main failed, trying fallback..."; \
		if [ -f snapcraft-fallback.yaml ]; then \
			cp snapcraft.yaml snapcraft.yaml.bak; \
			cp snapcraft-fallback.yaml snapcraft.yaml; \
			snapcraft; \
			mv snapcraft.yaml.bak snapcraft.yaml; \
			echo "✅ Fallback snapcraft.yaml worked!"; \
		else \
			echo "❌ No fallback available"; \
			exit 1; \
		fi; \
	fi
	@echo "✅ Snap package built: $(APP_NAME)_$(VERSION)_amd64.snap"

# Build snap with fallback
snap-fallback: clean
	@echo "📦 Building snap package with fallback config..."
	@which snapcraft >/dev/null || (echo "❌ snapcraft not found. Install with: sudo snap install snapcraft --classic" && exit 1)
	@if [ -f snapcraft-fallback.yaml ]; then \
		cp snapcraft.yaml snapcraft.yaml.bak; \
		cp snapcraft-fallback.yaml snapcraft.yaml; \
		snapcraft; \
		mv snapcraft.yaml.bak snapcraft.yaml; \
		echo "✅ Snap package built with fallback config"; \
	else \
		echo "❌ snapcraft-fallback.yaml not found"; \
		exit 1; \
	fi

# Install snap package locally
snap-install: snap
	@echo "📥 Installing snap package locally..."
	sudo snap install --dangerous --classic $(APP_NAME)_$(VERSION)_amd64.snap
	@echo "✅ Snap package installed"

# Remove snap package
snap-remove:
	@echo "🗑️  Removing snap package..."
	sudo snap remove $(APP_NAME)
	@echo "✅ Snap package removed"

# Run tests
test:
	@echo "🧪 Running tests..."
	$(PYTHON) test.py info
	$(PYTHON) test.py analyzer
	$(PYTHON) test.py cleaner
	@echo "✅ Tests complete"

# Run GUI test
test-gui:
	@echo "🖥️  Testing GUI..."
	$(PYTHON) test.py gui
	@echo "✅ GUI test complete"

# Lint code
lint:
	@echo "🔍 Linting code..."
	@which pylint >/dev/null || $(PIP) install pylint
	pylint --errors-only main.py daemon.py test.py
	@echo "✅ Linting complete"

# Format code
format:
	@echo "✨ Formatting code..."
	@which black >/dev/null || $(PIP) install black
	black --line-length 88 main.py daemon.py test.py
	@echo "✅ Code formatted"

# Development setup
dev-setup:
	@echo "🚀 Setting up development environment..."
	$(PIP) install -r requirements.txt
	$(PIP) install pylint black
	@echo "✅ Development environment ready"

# Check snap package
snap-info:
	@if [ -f "$(APP_NAME)_$(VERSION)_amd64.snap" ]; then \
		echo "📦 Snap package info:"; \
		snap info ./$(APP_NAME)_$(VERSION)_amd64.snap; \
	else \
		echo "❌ Snap package not found. Run 'make snap' first."; \
	fi

# Generate GitHub release
github-release: snap
	@echo "🚀 Preparing GitHub release..."
	@mkdir -p release/
	@cp $(APP_NAME)_$(VERSION)_amd64.snap release/
	@cp install.sh release/
	@cp uninstall.sh release/
	@cp README.md release/
	@echo "#!/bin/bash" > release/quick-install.sh
	@echo "# Quick install script for Inv Cleaner" >> release/quick-install.sh
	@echo "curl -L https://github.com/YOUR_USERNAME/inv-cleaner/releases/latest/download/install.sh | sudo bash" >> release/quick-install.sh
	@chmod +x release/quick-install.sh
	@echo "✅ Release files prepared in release/ directory"
	@echo "📋 Upload these files to GitHub releases:"
	@ls -la release/

# Run application
run:
	@echo "🚀 Running Inv Cleaner GUI..."
	$(PYTHON) main.py

# Run daemon
daemon:
	@echo "🔄 Running Inv Cleaner daemon..."
	sudo $(PYTHON) daemon.py

# Show status
status:
	@echo "📊 Inv Cleaner Status:"
	@echo "Version: $(VERSION)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Dependencies: $(shell $(PIP) list | grep -E '(matplotlib|numpy|schedule)' | wc -l)/3 installed"
	@if command -v snap >/dev/null 2>&1; then \
		echo "Snap: $(shell snap version | head -1)"; \
		if snap list $(APP_NAME) >/dev/null 2>&1; then \
			echo "Inv Cleaner snap: ✅ Installed"; \
		else \
			echo "Inv Cleaner snap: ❌ Not installed"; \
		fi; \
	else \
		echo "Snap: ❌ Not available"; \
	fi

# Help
help:
	@echo "🔧 Inv Cleaner - Available commands:"
	@echo ""
	@echo "Build & Install:"
	@echo "  make build       - Build the application"
	@echo "  make install     - Install locally (requires sudo)"
	@echo "  make uninstall   - Uninstall from system"
	@echo ""
	@echo "Snap Package:"
	@echo "  make snap        - Build snap package"
	@echo "  make snap-install- Install snap package locally"
	@echo "  make snap-remove - Remove snap package"
	@echo "  make snap-info   - Show snap package info"
	@echo ""
	@echo "Development:"
	@echo "  make test        - Run tests"
	@echo "  make test-gui    - Test GUI"
	@echo "  make lint        - Lint code"
	@echo "  make format      - Format code"
	@echo "  make dev-setup   - Setup development environment"
	@echo ""
	@echo "Run:"
	@echo "  make run         - Run GUI application"
	@echo "  make daemon      - Run background daemon"
	@echo ""
	@echo "Other:"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make status      - Show system status"
	@echo "  make github-release - Prepare GitHub release"
	@echo "  make help        - Show this help"
