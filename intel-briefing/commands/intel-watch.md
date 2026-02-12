# /intel-watch - Watch Folder Management

Check and process files in the designated watch folder where intelligence documents are dropped for ingestion. Shows pending files, processed files, and can trigger batch ingestion.

## Usage

```
/intel-briefing:intel-watch                        # Show pending files status
/intel-briefing:intel-watch status                 # Same as no args
/intel-briefing:intel-watch process                # Process all pending files
/intel-briefing:intel-watch process --skip-validation  # Process without per-file validation
/intel-briefing:intel-watch clean                  # Clean up processed folder (files older than 30 days)
```

### Parameters
- **status** (default) - Show watch folder status and pending files
- **process** - Process all pending files via ingestion pipeline
- **--skip-validation** - Skip per-document validation (validate all at end)
- **clean** - Remove files from processed/ subfolder older than 30 days

Initial request: $ARGUMENTS

## Watch Folder Paths

```
Watch folder:     /mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/
Processed folder: /mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed/
```

Windows paths:
```
Watch folder:     C:\Users\RonKlatt_3qsjg34\Desktop\PlugIn-Intel-Inputs\
Processed folder: C:\Users\RonKlatt_3qsjg34\Desktop\PlugIn-Intel-Inputs\processed\
```

## Execution Steps

### Mode: Status (default or "status")

1. Check if watch folder exists:
   ```bash
   ls "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/" 2>/dev/null
   ```
   If it does not exist:
   ```
   Watch folder not found. Creating...
   ```
   ```bash
   mkdir -p "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed"
   ```

2. List all files in the watch folder (not in processed/):
   ```bash
   # List files with details, excluding processed/ directory and hidden files
   ls -la "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/" | grep -v "^d" | grep -v "^\." | grep -v "^total"
   ```

3. Filter to supported extensions (.md, .txt, .pdf) and exclude hidden/system files

4. Count processed files:
   ```bash
   ls "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed/" 2>/dev/null | wc -l
   ```

5. Display status:
   ```
   =========================================
   WATCH FOLDER STATUS
   =========================================
   Path: C:\Users\RonKlatt_3qsjg34\Desktop\PlugIn-Intel-Inputs\

   Pending Files ([N]):
   -----------------------------------------
   # | Filename                           | Type | Size     | Modified
   --|-------------------------------------|------|----------|------------------
   1 | [filename.md]                       | MD   | [size]   | [date]
   2 | [filename.txt]                      | TXT  | [size]   | [date]
   3 | [filename.pdf]                      | PDF  | [size]   | [date]
   ...

   Processed: [N] files in processed/ folder
   Unsupported: [N] files skipped (not .md, .txt, or .pdf)

   =========================================

   COMMANDS:
     /intel-briefing:intel-watch process            # Process all pending files
     /intel-briefing:intel-ingest [filename]         # Process a specific file
   ```

   If no pending files:
   ```
   =========================================
   WATCH FOLDER STATUS
   =========================================
   Path: C:\Users\RonKlatt_3qsjg34\Desktop\PlugIn-Intel-Inputs\

   No pending files.

   Drop .md, .txt, or .pdf files into the watch folder to ingest them.
   Processed: [N] files in processed/ folder
   =========================================
   ```

### Mode: Process (if "process")

1. Scan the watch folder for pending files (same as status mode)

2. Filter to supported extensions, skip hidden files

3. If no pending files:
   ```
   No pending files to process. Watch folder is empty.
   ```
   Stop here.

4. Display processing plan and ask for confirmation:
   ```
   BATCH PROCESSING PLAN
   =========================================
   Files to process: [N]

   1. [filename.md]  (MD, [size])
   2. [filename.txt]  (TXT, [size])
   3. [filename.pdf]  (PDF, [size])

   Processing mode:
     - Per-document validation: [Yes / Skipped (--skip-validation)]
     - Master briefing update: Once at end (not per file)

   Proceed? (yes/no/select)
   ```

   - If "select", allow user to pick specific files by number
   - If "no", stop

5. Ensure processed/ subfolder exists:
   ```bash
   mkdir -p "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed"
   ```

6. For each file, run the ingestion pipeline:
   - Call the `/intel-briefing:intel-ingest` workflow internally with the file path
   - Use `--skip-briefing` flag for each file (briefing update happens once at end)
   - If `--skip-validation` is specified, also pass that flag per file

7. Display progress after each file:
   ```
   Processing [X] of [N]: [filename]
   [Phase 1-5 output from intel-ingest]
   ...
   Document stored. Moving to processed/
   ```

8. After successful ingestion, move file to processed/ with timestamp prefix:
   ```bash
   mv "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/[filename]" \
      "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed/$(date +%Y-%m-%dT%H%M)_[filename]"
   ```

9. If a file fails during ingestion, log the error and continue with next file. Do NOT move failed files to processed/.

10. After all files processed, if `--skip-validation` was used, run batch validation on all new claims:
    ```
    Running batch validation on [N] new claims...
    ```
    Trigger `/intel-briefing:intel-validate` workflow internally for the new claims.

11. After all files processed, trigger a single master briefing update:
    ```
    All files processed. Update master briefing? (yes/no)
    ```
    If yes, trigger `/intel-briefing:intel-briefing refresh`

12. Display cumulative summary:
    ```
    =========================================
    BATCH PROCESSING COMPLETE
    =========================================
    Files Processed: [N] of [total]
    Documents Stored: [N]
    Moved to Processed: [N]
    Failed: [N] (list filenames if any)

    Cumulative Results:
      Total Claims Extracted: [N]
        Financial: [n] | Geopolitical: [n] | Technology: [n] | Other: [n]
      Total Predictions Extracted: [N]
      Validated Claims: [N] (if validation was run)
      Alert Matches: [N]

    Master Briefing: [Updated to v[N] / Skipped]
    =========================================

    NEXT STEPS:
      /intel-briefing:intel-briefing                # View updated briefing
      /intel-briefing:intel-library stats            # View library statistics
      /intel-briefing:intel-predict review           # Review due predictions
    ```

### Mode: Clean (if "clean")

1. List files in processed/ folder with dates:
   ```bash
   ls -la "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed/"
   ```

2. Identify files older than 30 days

3. If no old files:
   ```
   No files older than 30 days in processed/ folder.
   Total processed files: [N]
   ```

4. If old files found:
   ```
   CLEANUP PLAN
   =========================================
   Files older than 30 days: [N]

   1. [timestamp_filename.md]  (processed [date])
   2. [timestamp_filename.txt]  (processed [date])
   ...

   Remove these files? (yes/no)
   ```

5. If confirmed, remove the old files:
   ```bash
   rm "/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/processed/[filename]"
   ```

6. Display cleanup results:
   ```
   CLEANUP COMPLETE
   Removed: [N] files
   Remaining in processed/: [N] files
   ```

## Important Rules

- **Watch folder path**: `/mnt/c/Users/RonKlatt_3qsjg34/Desktop/PlugIn-Intel-Inputs/` -- always use this exact path
- **Processed subfolder**: `processed/` under the watch folder -- create it if it does not exist
- **Supported extensions**: `.md`, `.txt`, `.pdf` only. Ignore all other file types.
- **Skip hidden files**: Any file starting with `.` is ignored
- **Skip system files**: Ignore `desktop.ini`, `Thumbs.db`, and similar Windows system files
- **Maximum batch size**: 20 files. If more than 20 pending files, warn the user and suggest processing in batches of 20.
- **Timestamp prefix**: When moving to processed/, use format `YYYY-MM-DDTHHMM_` (e.g., `2026-02-11T1430_filename.md`)
- For batch processing, use `--skip-validation` per document and validate all new claims at the end for efficiency -- this saves API calls
- Only trigger one master briefing update at the end, not per file
- If the watch folder path does not exist, create it along with the processed/ subfolder
- Failed files stay in the watch folder so they can be retried
