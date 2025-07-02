# Duplicate File Detector (Spanish Output)

A simple and efficient Python application that scans directories recursively, detects duplicate files based on SHA-256 hash comparison, and exports the results to a CSV file. Now available with both command-line interface and graphical user interface.

## ✨ Features

- **Two Interface Options:**
  - Command-line interface for advanced users
  - Graphical user interface (GUI) for easy visual interaction
- Scans folders recursively
- Detects duplicate files by content (not filename) using SHA-256 hashing
- Generates a CSV report with all duplicates
- Calculates total space that could be reclaimed
- Console and GUI output in Spanish
- Multi-threaded GUI analysis to keep interface responsive

## 📦 Output

- `duplicados.csv`: Contains file hashes and duplicate file paths
- Summary showing:
  - Number of duplicate files found
  - Total potential disk space savings formatted in human-readable units (B, KB, MB, GB, TB)

## 🔧 Requirements

- Python 3.8 or later (required for walrus operator `:=`)
- **Built-in libraries only:**
  - `tkinter` (for GUI - included with most Python installations)
  - `hashlib` (for SHA-256 hashing)
  - `csv` (for report generation)
  - `os` (for file system operations)
  - `threading` (for responsive GUI)
  - `collections` (for defaultdict)

## 📌 Usage

### Command Line Interface
```bash
python duplicate_file_detector.py
```
Follow the prompt to enter a directory path.

### Graphical User Interface
```bash
python duplicate_detector_gui.py
```
- Click "📁 Buscar" to select a directory
- Click "🔍 Analizar duplicados" to start the analysis
- View results directly in the application window

## 📁 Project Structure

```
duplicateFileDetector/
├── duplicate_file_detector.py    # Core detection logic and CLI
├── duplicate_detector_gui.py     # GUI interface using Tkinter
├── README.md                     # This file
└── duplicados.csv               # Generated output file
```

## 🖥️ GUI Features

- **User-friendly interface:** Easy directory selection with file browser
- **Real-time status updates:** Visual feedback during analysis
- **Non-blocking operation:** Analysis runs in background thread
- **Formatted results:** Human-readable space calculations
- **Error handling:** Clear error messages for invalid directories

## 🔍 How it Works

1. **File Discovery:** Recursively scans the selected directory
2. **Hash Calculation:** Computes SHA-256 hash for each file's content
3. **Duplicate Detection:** Groups files with identical hashes
4. **Space Calculation:** Determines reclaimable space (keeping one copy per group)
5. **Report Generation:** Exports results to CSV and displays summary

## 🚀 Getting Started

1. Clone or download the repository
2. Ensure Python 3.8+ is installed
3. Choose your preferred interface:
   - For GUI: Run `python duplicate_detector_gui.py`
   - For CLI: Run `python duplicate_file_detector.py`
4. Select a directory to analyze
5. Review results in the application or check `duplicados.csv`