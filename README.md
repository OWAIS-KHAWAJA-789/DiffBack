# DiffBack Backup Comparison Tool

## Overview

The Backup Comparison Tool is a Python utility designed to compare files between a source folder and a backup folder. It checks for discrepancies in file names, sizes, and contents, and generates a detailed report highlighting files that are missing, have different sizes, or have different hashes between the source and backup directories.

## Features

- Compares files based on names, sizes, and SHA-256 hashes.
- Generates a detailed report including:
  - Files in source but missing in backup.
  - Files in backup but missing in source.
  - Files present in both but with different sizes or hashes.
  - Files present in both and similar.
- Provides a summary line in the report indicating the overall comparison status and counts of discrepancies.

## Prerequisites

- Python 3.6 or later

## Installation

. **Clone the repository:**

    ```sh
    git clone https://github.com/MohammadOwaisData/DiffBack.git
    cd DiffBack
    ```

## Usage

1. **Run the tool:**

    ```sh
    python app.py
    ```

2. **Input folder paths:**
   - When prompted, enter the path to the original folder (source).
   - When prompted, enter the path to the backup folder (backup).

3. **Review the report:**
   - The tool generates a report file in the `backup_reports` directory.
   - The report file is named with a timestamp (e.g., `20240912_120000_report.txt`), format is (`YYYYMMDD_HOUR_MINUTES_SECONDS_report.txt`).

## Report Format

The report file is formatted as follows:

1. **First Line:**
   - **Pass/Fail Status**: 1 (pass) if both source and backup have the same files and data; otherwise, 0 (fail).
   - **Counts:**
     - Count of files in source but missing in backup.
     - Count of files in backup but missing in source.
     - Count of files in both source and backup but with different sizes or hashes.
     - Count of files in both source and backup and similar.

   Example:
   1#1#0#1#5


2. **Detailed Report:**
- **Files in source but missing in backup:**
  - Count and names.
- **Files in backup but missing in source:**
  - Count and names.
- **Files in both source and backup but different sizes or hashes:**
  - Count and names.
- **Files in both source and backup and similar:**
  - Count and names.

## Error Handling

- Logs errors to `tool.log` for troubleshooting.
- Handles cases where directories do not exist or cannot be accessed.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This tool is released under the MIT License. See the [LICENSE](https://github.com/MohammadOwaisData/DiffBack/blob/main/LICENSE) file for details.

## Contact

For any questions or feedback, please send a mail at proton address [[link](https://mohammad-owais.netlify.app/#contact)].
