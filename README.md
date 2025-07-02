# Duplicate File Detector (Spanish Output)
A simple and efficient Python script that scans a directory recursively, detects duplicate files based on SHA-256 hash comparison, and exports the results to a CSV file.
- ✨ Features

    Scans folders recursively

    Detects duplicate files by content (not filename)

    Generates a CSV report with all duplicates

    Calculates total space that could be reclaimed

    Console output in Spanish

- 📦 Output

    duplicados.csv: Contains file hashes and duplicate file paths

    Console summary showing:

        Number of duplicate files found

        Total potential disk space savings

- 🔧 Requirements

    Python 3.6 or later

    No external dependencies

- 📌 Usage

python duplicate_file_detector.py

Follow the prompt to enter a directory path.