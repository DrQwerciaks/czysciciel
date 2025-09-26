# Developer Guide for Inv Cleaner

This guide explains how to set up development environment and contribute to Inv Cleaner.

## 🛠️ Development Setup

### Prerequisites
- Python 3.6+
- Git
- Linux system (Ubuntu/Debian recommended for development)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/inv-cleaner.git
cd inv-cleaner

# Setup development environment
make dev-setup

# Run tests
make test

# Run application
make run
```

## 📁 Project Structure

```
inv-cleaner/
├── main.py                 # GUI application
├── daemon.py              # Background daemon
├── test.py                # Test suite
├── requirements.txt       # Python dependencies
├── snapcraft.yaml         # Snap package configuration
├── Makefile              # Build automation
├── install.sh            # Installation script
├── uninstall.sh          # Removal script
├── quick-install.sh      # GitHub quick install
├── assets/               # Icons and resources
│   ├── inv-cleaner-logo.svg
│   ├── inv-cleaner-logo.png
│   ├── inv-cleaner.desktop
│   └── inv-cleaner.service
├── .github/workflows/    # GitHub Actions CI/CD
└── docs/                # Documentation
```

## 🧪 Testing

### Run All Tests
```bash
make test
```

### Individual Test Components
```bash
# System info
python3 test.py info

# Disk analyzer
python3 test.py analyzer

# Disk cleaner  
python3 test.py cleaner

# GUI test
python3 test.py gui
```

### Performance Benchmarks
```bash
python3 test.py benchmark
```

## 🏗️ Building

### Local Build
```bash
make build
```

### Snap Package
```bash
make snap
```

### Install Locally
```bash
make install
```

## 🔍 Code Quality

### Linting
```bash
make lint
```

### Code Formatting
```bash
make format
```

### Pre-commit Checks
```bash
# Run before committing
make clean
make lint
make test
make build
```

## 🐛 Debugging

### Debug GUI Application
```bash
# Run with debug output
python3 -u main.py

# Check for GUI issues
python3 -c "import tkinter; tkinter.Tk()"
```

### Debug Daemon
```bash
# Run daemon in foreground
sudo python3 daemon.py

# Check systemd status
systemctl status inv-cleaner
journalctl -u inv-cleaner -f
```

### Common Issues

1. **Permission Errors**
   ```bash
   sudo chown -R $USER:$USER /opt/inv-cleaner
   ```

2. **Missing Dependencies**
   ```bash
   pip3 install -r requirements.txt
   sudo apt install python3-tk libnotify-bin
   ```

3. **GUI Not Starting**
   ```bash
   export DISPLAY=:0
   python3 main.py
   ```

## 📋 Coding Standards

### Python Style Guide
- Follow PEP 8
- Use type hints where possible
- Maximum line length: 88 characters
- Use docstrings for all functions/classes

### Example Code Structure
```python
def analyze_disk_usage(self, path: str = "/") -> Dict[str, Any]:
    """
    Analyzes disk usage for specified path.
    
    Args:
        path: Root path to analyze
        
    Returns:
        Dictionary with usage statistics
        
    Raises:
        OSError: If path doesn't exist or no permissions
    """
    pass
```

### Error Handling
```python
try:
    # Risky operation
    result = dangerous_operation()
except (OSError, IOError) as e:
    self.logger.error(f"Operation failed: {e}")
    return None
```

### Logging
```python
# Use module logger
import logging
logger = logging.getLogger(__name__)

# Log levels
logger.debug("Debug information")
logger.info("General information") 
logger.warning("Warning message")
logger.error("Error occurred")
logger.critical("Critical error")
```

## 🔄 Development Workflow

### Feature Development
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Add tests
4. Update documentation
5. Run quality checks: `make lint && make test`
6. Commit changes: `git commit -m "feat: add new feature"`
7. Push branch: `git push origin feature/new-feature`
8. Create pull request

### Bug Fixes
1. Create bugfix branch: `git checkout -b fix/issue-123`
2. Fix the bug
3. Add regression test
4. Update changelog
5. Commit: `git commit -m "fix: resolve issue #123"`

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix  
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

## 🚀 Release Process

### Version Bumping
1. Update version in `snapcraft.yaml`
2. Update `CHANGELOG.md`
3. Commit changes
4. Create tag: `git tag v1.0.1`
5. Push: `git push origin v1.0.1`

### GitHub Actions automatically:
- Runs tests
- Builds snap package
- Creates GitHub release
- Publishes to Snap Store

### Manual Release
```bash
# Build and test
make clean
make test
make snap

# Test snap package
sudo snap install --dangerous inv-cleaner_*.snap

# Create release
git tag v1.0.1
git push origin v1.0.1
```

## 📚 Adding New Features

### New Cleaning Rule
1. Add to `DiskCleaner` class
2. Update configuration schema
3. Add tests
4. Update documentation

### New GUI Tab
1. Add tab in `setup_ui()`
2. Create setup method
3. Add event handlers
4. Test UI interactions

### New Configuration Option
1. Update `config-example.json`
2. Add validation in daemon
3. Update GUI settings tab
4. Document in README

## 🧩 Architecture

### Core Components
- **DiskAnalyzer**: Scans and analyzes disk usage
- **DiskCleaner**: Performs file cleanup operations  
- **NotificationManager**: Handles system notifications
- **CzyscicielApp**: Main GUI application
- **CzyscicielDaemon**: Background service

### Data Flow
```
User Input → GUI → DiskCleaner → File System
                ↓
Configuration ← JSON Config ← Daemon
                ↓
Notifications ← Results ← Logs
```

## 🤝 Contributing

### Pull Request Checklist
- [ ] Code follows style guidelines
- [ ] Tests pass: `make test`
- [ ] Code is linted: `make lint`  
- [ ] Documentation updated
- [ ] Changelog entry added
- [ ] Commits follow convention

### Review Process
1. Automated tests run via GitHub Actions
2. Code review by maintainers
3. Manual testing on different distributions  
4. Merge after approval

### Getting Help
- 📖 Read existing code and documentation
- 💬 Open issue for questions
- 📧 Contact maintainers
- 🐛 Report bugs with detailed steps

Thank you for contributing to Inv Cleaner! 🧹✨
