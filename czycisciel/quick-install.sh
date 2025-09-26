#!/bin/bash
# Quick install script for Inv Cleaner from GitHub
# Usage: curl -L https://raw.githubusercontent.com/YOUR_USERNAME/inv-cleaner/main/quick-install.sh | sudo bash

set -e

# Colors
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

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo_error "This script must be run as root"
   echo "Usage: curl -L https://raw.githubusercontent.com/YOUR_USERNAME/inv-cleaner/main/quick-install.sh | sudo bash"
   exit 1
fi

echo_info "🧹 Inv Cleaner - Quick Install from GitHub 💾"
echo_info "============================================="

# Detect installation method
INSTALL_METHOD=""
TEMP_DIR=$(mktemp -d)

# Check if snap is available
if command -v snap >/dev/null 2>&1; then
    echo_info "Snap detected - will install via Snap Store"
    INSTALL_METHOD="snap"
else
    echo_info "Snap not available - will install from source"
    INSTALL_METHOD="source"
fi

cd "$TEMP_DIR"

if [ "$INSTALL_METHOD" = "snap" ]; then
    echo_info "Installing Inv Cleaner from Snap Store..."
    
    # Try to install from Snap Store first
    if snap install inv-cleaner; then
        echo_success "Inv Cleaner installed from Snap Store!"
    else
        echo_warning "Snap Store installation failed, trying GitHub release..."
        
        # Download latest snap package from GitHub releases
        echo_info "Downloading latest release from GitHub..."
        LATEST_URL=$(curl -s https://api.github.com/repos/YOUR_USERNAME/inv-cleaner/releases/latest | grep "browser_download_url.*\.snap" | cut -d '"' -f 4)
        
        if [ -n "$LATEST_URL" ]; then
            wget -O inv-cleaner.snap "$LATEST_URL"
            echo_info "Installing snap package..."
            snap install --dangerous --classic inv-cleaner.snap
            echo_success "Inv Cleaner installed from GitHub release!"
        else
            echo_error "Could not download snap package, falling back to source installation"
            INSTALL_METHOD="source"
        fi
    fi
fi

if [ "$INSTALL_METHOD" = "source" ]; then
    echo_info "Installing Inv Cleaner from source..."
    
    # Check dependencies
    echo_info "Checking system dependencies..."
    
    # Detect package manager
    if command -v apt >/dev/null 2>&1; then
        PACKAGE_MANAGER="apt"
        PKG_INSTALL="apt update && apt install -y"
        PACKAGES="python3 python3-pip python3-tk libnotify-bin git"
    elif command -v yum >/dev/null 2>&1; then
        PACKAGE_MANAGER="yum"
        PKG_INSTALL="yum install -y"
        PACKAGES="python3 python3-pip tkinter libnotify git"
    elif command -v dnf >/dev/null 2>&1; then
        PACKAGE_MANAGER="dnf"
        PKG_INSTALL="dnf install -y"
        PACKAGES="python3 python3-pip python3-tkinter libnotify git"
    else
        echo_error "Unsupported package manager. Please install manually."
        exit 1
    fi
    
    echo_info "Installing system packages with $PACKAGE_MANAGER..."
    eval "$PKG_INSTALL $PACKAGES"
    
    # Download source code
    echo_info "Downloading Inv Cleaner source code..."
    git clone https://github.com/YOUR_USERNAME/inv-cleaner.git
    cd inv-cleaner
    
    # Run installer
    echo_info "Running installation script..."
    chmod +x install.sh
    ./install.sh
    
    echo_success "Inv Cleaner installed from source!"
fi

# Cleanup
cd /
rm -rf "$TEMP_DIR"

echo_success "🎉 Installation completed successfully!"
echo_info ""
echo_info "🚀 How to use Inv Cleaner:"
echo_info "  • GUI Application: inv-cleaner (or search in applications menu)"
echo_info "  • Command line: inv-cleaner-gui"
echo_info "  • Background daemon: systemctl status inv-cleaner"
echo_info "  • View logs: journalctl -u inv-cleaner -f"
echo_info ""
echo_info "📚 More information:"
echo_info "  • Documentation: https://github.com/YOUR_USERNAME/inv-cleaner"
echo_info "  • Configuration: /etc/inv-cleaner/config.json"
echo_info "  • Report issues: https://github.com/YOUR_USERNAME/inv-cleaner/issues"
echo_info ""
echo_warning "⚠️  Note: The daemon runs with root privileges for full system access"
echo_success "Happy cleaning! 🧹✨"
