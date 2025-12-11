# Backup Guide for Prompt Library Database

This guide explains how to backup and restore your `prompts.db` file to protect your precious prompts.

## Table of Contents
- [Quick Backup](#quick-backup)
- [Backup Locations](#backup-locations)
- [Automated Backups](#automated-backups)
- [Restoring from Backup](#restoring-from-backup)
- [Best Practices](#best-practices)

---

## Quick Backup

### Manual Backup (Simple Method)

The easiest way to backup your database is to simply copy the `prompts.db` file:

**On Linux/macOS:**
```bash
cp prompts.db ./database-backups/prompts.db.backup.$(date +%Y%m%d_%H%M%S)
```

**On Windows (Command Prompt):**
```bash
copy prompts.db ./database-backups/prompts.db.backup.%date:~-4%%date:~-10,2%%date:~-7,2%
```

**On Windows (PowerShell):**
```powershell
Copy-Item prompts.db "./database-backups/prompts.db.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
```

This creates a timestamped backup file like: `prompts.db.backup.20251211_143022`

---

## Backup Locations

### Option 1: Local `backups/` Directory (Recommended)

Create a dedicated backups folder in your project:

```bash
mkdir -p backups
cp prompts.db backups/prompts.db.backup.$(date +%Y%m%d_%H%M%S)
```

**Advantages:**
- ✅ Organized and easy to find
- ✅ Already in `.gitignore` (safe from accidental commits)
- ✅ Easy to see backup history

**Disadvantages:**
- ❌ Backups are on the same machine (not disaster-proof)

### Option 2: Cloud Storage (Recommended for Important Data)

Back up to cloud services for extra safety:

**Google Drive / Dropbox / OneDrive:**
- Copy `prompts.db` to your cloud drive manually
- Or use sync tools like Syncthing

**AWS S3 / Azure Blob Storage:**
```bash
# Example: Upload to AWS S3
aws s3 cp prompts.db s3://my-backups/prompts.db.backup.$(date +%Y%m%d_%H%M%S)
```

**Advantages:**
- ✅ Safe from local machine failures
- ✅ Accessible from anywhere
- ✅ Multiple versions kept

### Option 3: External Hard Drive

- Plug in an external drive
- Copy `prompts.db` to the drive periodically
- Label backups with dates

**Advantages:**
- ✅ Physical backup (no internet needed)
- ✅ Large storage capacity

---

## Automated Backups

### Bash Script (Linux/macOS)

Create a file `backup.sh`:

```bash
#!/bin/bash

# Backup Configuration
DB_FILE="prompts.db"
BACKUP_DIR="backups"
BACKUP_COUNT=10  # Keep last 10 backups

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/prompts.db.backup.$TIMESTAMP"

# Copy database to backup
cp "$DB_FILE" "$BACKUP_FILE"
echo "✅ Backup created: $BACKUP_FILE"

# Remove old backups (keep only the last 10)
cd "$BACKUP_DIR"
ls -t prompts.db.backup.* | tail -n +$((BACKUP_COUNT + 1)) | xargs -r rm
echo "🧹 Old backups cleaned up (keeping last $BACKUP_COUNT)"
```

**Make it executable:**
```bash
chmod +x backup.sh
```

**Run manually:**
```bash
./backup.sh
```

### Schedule Automatic Backups with Cron (Linux/macOS)

Edit your crontab:
```bash
crontab -e
```

Add this line to backup daily at 2 AM:
```
0 2 * * * cd ~/projects/Prompt_Library_Database && ./backup.sh
```

Or weekly on Sundays:
```
0 2 * * 0 cd ~/projects/Prompt_Library_Database && ./backup.sh
```

### PowerShell Script (Windows)

Create a file `backup.ps1`:

```powershell
# Backup Configuration
$DbFile = "prompts.db"
$BackupDir = "backups"
$BackupCount = 10  # Keep last 10 backups

# Create backup directory if it doesn't exist
if (!(Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Path $BackupDir | Out-Null
}

# Create timestamped backup
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = "$BackupDir\prompts.db.backup.$Timestamp"

# Copy database to backup
Copy-Item $DbFile $BackupFile
Write-Host "✅ Backup created: $BackupFile"

# Remove old backups (keep only the last 10)
$BackupFiles = Get-ChildItem "$BackupDir\prompts.db.backup.*" -File | Sort-Object LastWriteTime -Descending
if ($BackupFiles.Count -gt $BackupCount) {
    $FilesToDelete = $BackupFiles | Select-Object -Skip $BackupCount
    $FilesToDelete | Remove-Item
    Write-Host "🧹 Old backups cleaned up (keeping last $BackupCount)"
}
```

**Schedule with Task Scheduler:**
1. Open "Task Scheduler"
2. Create New Task
3. Set trigger: Daily at 2:00 AM
4. Set action: Run PowerShell script
5. Specify: `powershell.exe -ExecutionPolicy Bypass -File "C:\path\to\backup.ps1"`

---

## Restoring from Backup

### Restore from Backup File

**If your current database is corrupted or lost:**

**On Linux/macOS:**
```bash
# Stop the app first!
# Then restore
cp backups/prompts.db.backup.20251211_143022 prompts.db
```

**On Windows:**
```bash
REM Stop the app first!
REM Then restore
copy backups\prompts.db.backup.20251211_143022 prompts.db
```

### List Available Backups

**On Linux/macOS:**
```bash
ls -lh backups/prompts.db.backup.*
```

**On Windows (PowerShell):**
```powershell
Get-ChildItem "backups\prompts.db.backup.*" | Sort-Object LastWriteTime -Descending
```

---

## Best Practices

### 🎯 Backup Strategy (3-2-1 Rule)

The industry-standard backup strategy:

- **3** copies of your data (original + 2 backups)
- **2** different storage types (local + cloud)
- **1** offsite backup (cloud or external drive)

**Example Implementation:**
1. Original: `prompts.db` on your machine
2. Backup 1: `backups/` folder on same machine
3. Backup 2: Cloud storage (Google Drive, Dropbox, etc.)

### 📋 Backup Frequency

- **Daily:** If you add/edit prompts frequently
- **Weekly:** If you add prompts occasionally
- **Before major changes:** Always backup before updating the app

### 🔍 Test Your Backups

Regularly verify your backups work:

```bash
# List backup files
ls backups/

# Try restoring to a test file
cp backups/prompts.db.backup.latest prompts.db.test
```

### 🗂️ Organize Backups

Create a backup naming convention:

```
prompts.db.backup.20251211_143022    # Date and time format
prompts.db.backup.before-export      # Descriptive names
prompts.db.backup.v1.0               # Version numbers
```

### 🚨 Important Notes

1. **Stop the app before restoring** - Close the Streamlit app before replacing the database
2. **Verify backup integrity** - Ensure backup files are actually created and have size > 0
3. **Keep backups outside `.gitignore`'s .git folder** - Backups in `backups/` folder are safe
4. **Cloud sync caution** - If using cloud sync (OneDrive, iCloud), disable it during backups to avoid conflicts

---

## Backup Checklist

Before making major changes to your prompts:

- [ ] Run backup: `./backup.sh` (or manual backup)
- [ ] Verify backup was created: `ls -lh backups/`
- [ ] Check backup file size (should match prompts.db size)
- [ ] Document what you're about to do
- [ ] Keep at least 3 recent backups at all times

---

## Emergency Recovery

If you accidentally delete or corrupt your database:

1. **Stop the Streamlit app** (Ctrl+C in terminal)
2. **List available backups:**
   ```bash
   ls -lh backups/prompts.db.backup.*
   ```
3. **Restore the most recent backup:**
   ```bash
   cp backups/prompts.db.backup.20251211_143022 prompts.db
   ```
4. **Restart the app:**
   ```bash
   streamlit run app.py
   ```

Your prompts should be restored!

---

## Need More Help?

- Check SQLite documentation: https://www.sqlite.org/backup.html
- For cloud backup questions, see your cloud provider's docs
- Consider using automated backup tools like Duplicati or Restic for advanced needs
