# Summary Report Automated Checker

## Overview

The Summary Report Automated Checker is a tool designed to process `.tar.xz` files containing `.txt` files. It classifies data lines into categories such as 'OK', 'Null', and 'Anomaly' based on specific patterns and generates summary reports.

This repository contains two versions of the script:

- **Version 1.0.5**: Stores detailed logs for each individual file processed.
- **Version 2.0.10**: Focuses on storing only the summary of processed files and prints logs to the terminal without saving them.

## Versions

### Version 1.0.5

**Description**: 

This version processes `.tar.xz` files, classifies each line in `.txt` files, and generates detailed log files for each individual file along with a summary report. 

**Features**:
- Classifies data lines into 'OK', 'Null', or 'Anomaly'.
- Saves detailed log files for each processed file.
- Generates a summary report for all processed files.

**Usage**:

1. Place your `.tar.xz` files in a directory.
2. Run the script with the directory path as an argument:
   ```bash
   python3 version_1_file.py /path/to/directory
   ```
3. Check the `Output_Checker` folder for individual log files and the summary report.

**File Structure**:
- `version_1_file.py`: Main script file for version 1.0.10.
- `Output_Checker/`: Directory containing individual log files and the summary report.

---

### Version 2.0.10

**Description**: 

This version is optimized to handle larger datasets by focusing on generating and storing only summary reports. It does not save individual log files but prints the logs to the terminal for real-time monitoring.

**Features**:
- Classifies data lines into 'OK', 'Null', or 'Anomaly'.
- Prints logs to the terminal.
- Saves and updates a summary report of all processed files.

**Usage**:

1. Place your `.tar.xz` files in a directory.
2. Run the script with the directory path as an argument:
   ```bash
   python3 version_2_file.py /path/to/directory
   ```
3. Check the `Output_Checker` folder for the summary report.

**File Structure**:
- `version_2_file.py`: Main script file for version 2.0.10.
- `Output_Checker/`: Directory containing the summary report (`summary_all.txt`).

## Script Details

### `version_1_file.py`

```python
# Script content for version 1.0.10
```

**Key Points**:
- Stores individual log files for each `.tar.xz` file processed.
- Generates a summary report file.

### `version_2_file.py`

```python
# Script content for version 2.0.10
```

**Key Points**:
- Does not save individual log files.
- Updates and stores a summary report in the `Output_Checker` folder.
- Prints logs to the terminal.

## Dependencies

Ensure you have the following Python packages installed:
- `pandas`
- `tarfile` (standard library)
- `re` (standard library)
- `os` (standard library)
- `sys` (standard library)

You can install the required packages using pip:
```bash
pip install pandas
```


## Contact

For any questions or feedback, please contact:

**I Putu Ferry Wistika**  
Email: putuferrywistika@gmail.com



