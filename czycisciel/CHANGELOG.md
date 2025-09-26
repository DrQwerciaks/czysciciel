# Changelog

All notable changes to Inv Cleaner will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Snap package support
- GitHub Actions CI/CD pipeline
- Quick install script from GitHub
- Professional logo and branding

### Changed
- Renamed from "Czysciciel Dysku" to "Inv Cleaner"
- Updated UI with modern icons and styling
- Improved error handling and logging

### Fixed
- Icon loading in different environments
- Notification formatting

## [1.0.0] - 2025-09-26

### Added
- 🧹 **Disk Cleaning Features**
  - Automatic removal of old log files (>7 days configurable)
  - Large file cleanup (>200MB configurable)
  - Temporary file cleanup from `/tmp` and `/var/tmp`
  - Smart file preservation (config files, keys, etc.)

- 📊 **Disk Analysis**
  - Visual disk usage analysis with pie charts
  - Directory size scanning and reporting
  - Real-time disk usage monitoring
  - Similar functionality to Baobab disk analyzer

- 🖥️ **Modern GUI Interface**
  - Tabbed interface (Analysis, Cleaning, Logs, Settings)
  - Real-time progress indicators
  - Detailed cleaning results display
  - Configurable cleaning parameters

- 🔄 **Background Daemon**
  - Systemd service integration
  - Hourly automatic cleanup (configurable)
  - Runs with root privileges for system access
  - Comprehensive logging

- 🔔 **Notifications**
  - Desktop notifications for cleaning results
  - Detailed logging of all operations
  - Configurable notification settings

- ⚙️ **Configuration**
  - JSON-based configuration file
  - Customizable cleaning criteria
  - Directory inclusion/exclusion patterns
  - File preservation patterns

- 🛠️ **Installation & Management**
  - Automated installation script
  - Systemd service management
  - Log rotation configuration
  - Easy uninstallation

### Technical Details
- **Language**: Python 3.6+
- **GUI Framework**: Tkinter with ttk styling
- **Visualization**: Matplotlib for disk usage charts
- **Scheduling**: Schedule library for automated tasks
- **Logging**: Python logging with rotation
- **Platform**: Linux (Ubuntu, Debian, CentOS, Fedora)

### System Requirements
- Linux operating system
- Python 3.6 or newer
- Root privileges (for full system access)
- Minimum 50MB disk space
- Desktop environment (for GUI)

### Installation Methods
1. **Snap Package**: `sudo snap install inv-cleaner`
2. **Quick Install**: `curl -L <github-url>/quick-install.sh | sudo bash`
3. **Manual Install**: Download and run `install.sh`
4. **From Source**: Clone repository and run installer

### Security Features
- ✅ Safe file deletion with existence checks
- ✅ Configurable file preservation patterns
- ✅ Comprehensive audit logging
- ✅ Root privilege requirement for system access
- ⚠️ Requires careful configuration for production use
