# Publishing Inv Cleaner to Snap Store

This guide explains how to publish Inv Cleaner to the Snap Store.

## Prerequisites

1. **Snapcraft Account**: Register at https://snapcraft.io/
2. **Snapcraft CLI**: Install with `sudo snap install snapcraft --classic`
3. **Login**: Run `snapcraft login`

## Step-by-Step Publishing

### 1. Build the Snap Package

```bash
# Clean previous builds
make clean

# Build snap package
make snap
```

This creates `inv-cleaner_1.0.0_amd64.snap`

### 2. Test Locally

```bash
# Install locally for testing
sudo snap install --dangerous --classic inv-cleaner_1.0.0_amd64.snap

# Test the application
inv-cleaner

# Remove test installation
sudo snap remove inv-cleaner
```

### 3. Upload to Snap Store

```bash
# Upload to store (first time)
snapcraft upload inv-cleaner_1.0.0_amd64.snap

# Release to stable channel
snapcraft release inv-cleaner 1 stable
```

### 4. Monitor Store Listing

- Visit: https://snapcraft.io/inv-cleaner/listing
- Update description, screenshots, and metadata
- Add keywords: disk, cleaner, monitor, system, storage

## Store Metadata

### App Description

```
Advanced disk cleaner and monitoring tool for Linux systems.

Inv Cleaner provides visual disk usage analysis similar to Baobab and intelligent cleanup of:
• Old log files (>7 days configurable)  
• Large temporary files (>200MB configurable)
• Cached files and thumbnails
• System temporary directories

Features:
🧹 Automatic background cleaning
📊 Visual disk usage charts  
🔔 Desktop notifications
📋 Detailed operation logs
⚙️ Fully configurable
🛡️ Safe file preservation rules

Perfect for system administrators and users who want to keep their Linux systems clean and optimized.
```

### Categories
- Primary: Utilities
- Secondary: System

### Keywords
```
disk, cleaner, monitor, system, storage, cleanup, baobab, analyzer, maintenance, admin
```

## Automatic Publishing via GitHub Actions

The repository includes GitHub Actions workflow that automatically:

1. **On Pull Request**: Run tests and build snap
2. **On Tag Push**: 
   - Build snap package
   - Create GitHub release
   - Upload to Snap Store (stable channel)

### Setup GitHub Secrets

1. Get snapcraft credentials:
   ```bash
   snapcraft export-login --snaps inv-cleaner --channels edge,beta,candidate,stable credentials.txt
   ```

2. Add to GitHub repository secrets:
   - `SNAPCRAFT_STORE_CREDENTIALS`: Content of credentials.txt

### Create Release

```bash
# Tag new version
git tag v1.0.0
git push origin v1.0.0
```

This automatically:
- Builds snap package  
- Creates GitHub release
- Publishes to Snap Store

## Manual Store Management

### Update App Metadata

```bash
# Edit store listing
snapcraft edit-listing inv-cleaner
```

### Manage Releases

```bash
# List revisions
snapcraft list-revisions inv-cleaner

# Promote to channel
snapcraft release inv-cleaner 2 beta

# Close channel
snapcraft close inv-cleaner beta
```

### View Metrics

```bash
# Download metrics
snapcraft metrics inv-cleaner --start 2025-01-01 --end 2025-12-31
```

## Store Listing Best Practices

### Screenshots Needed
1. **Main GUI** - Disk analysis tab with pie chart
2. **Cleaning Tab** - Showing cleaning in progress  
3. **Results** - After cleanup completion with stats
4. **Settings** - Configuration options

### Icon Requirements  
- **256x256 PNG** - High resolution app icon
- **Transparent background** - For different themes
- **Clear at small sizes** - Readable in app lists

### Description Tips
- ✅ Lead with main benefit
- ✅ Use bullet points for features  
- ✅ Include relevant keywords
- ✅ Mention similar tools (Baobab)
- ✅ Highlight safety features
- ❌ Don't exceed character limits

### Contact Information
- **Website**: https://github.com/YOUR_USERNAME/inv-cleaner
- **Issues**: https://github.com/YOUR_USERNAME/inv-cleaner/issues
- **Contact**: your-email@example.com

## Post-Publication

1. **Monitor Reviews**: Respond to user feedback
2. **Update Regularly**: Fix bugs and add features
3. **Promote**: Share on social media, forums
4. **Analytics**: Track downloads and usage

## Troubleshooting

### Common Build Issues

```bash
# Permission errors
sudo snap install snapcraft --classic

# Python dependencies  
snapcraft clean
snapcraft

# Review failed
snapcraft upload --release candidate
```

### Store Rejection Reasons
- **Security**: Classic confinement requires manual review
- **Metadata**: Incomplete store listing  
- **Testing**: App crashes or doesn't start
- **Naming**: Name conflicts with existing snaps

Contact Snapcraft forums for help: https://forum.snapcraft.io/
