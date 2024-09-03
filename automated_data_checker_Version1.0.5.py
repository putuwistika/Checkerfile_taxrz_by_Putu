"""
Deskripsi:

Summary Report Automated Checker
Generated by: I Putu Ferry Wistika
Version 1.0.10
Last updated: 2024-09-02
----------------------------------------
Skrip ini digunakan untuk memproses file berformat .tar.xz yang berisi file .txt, mengklasifikasikan data dalam file tersebut 
ke dalam tiga kategori: 'OK', 'Null', dan 'Anomaly' berdasarkan pola tertentu, serta menyimpan hasil klasifikasi dalam log file 
dan membuat ringkasan keseluruhan.

Setiap log file akan disimpan di direktori tempat skrip ini dijalankan di dalam folder bernama Output_Checker, 
dengan masing-masing file log dihasilkan untuk setiap file .tar.xz yang diproses. Selain itu, skrip ini juga menghasilkan file 
summary_all.txt yang berisi ringkasan dari semua file yang diproses.

Cara penggunaan:
1. Jalankan skrip ini dengan argumen berupa path ke folder yang berisi file .tar.xz.
2. Skrip akan mengekstrak file .txt dalam .tar.xz dan mengklasifikasikan isinya.
3. Hasil klasifikasi akan disimpan dalam file log individual, dan summary akan disimpan dalam file summary_all.txt 
   di dalam folder Output_Checker.

Usage: python3 file.py folder_path
"""

hello = """Summary Report Automated Checker
Generated by: I Putu Ferry Wistika
Version 1.0.10
Last updated: 2024-09-02
----------------------------------------
"""

import tarfile
import pandas as pd
import re
import os
import sys

class TarXZProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.summary_content = []
        self.output_folder = os.path.join(os.getcwd(), "Output_Checker")
        
        # Buat folder Output_Checker jika belum ada
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def classify_line(self, line):
        # OK pattern with exactly 4 fields
        if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3},\d+(\.\d+)?(,\d+(\.\d+)?){1}$", line):
            return 'OK'
        # Null pattern with missing values
        elif re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3},$", line):
            return 'Null'
        # Anything else is considered an anomaly
        else:
            return 'Anomaly'

    def process_file(self, file_path, file_name):
        log_content = []
        null_count = 0
        anomaly_count = 0
        ok_count = 0

        with tarfile.open(file_path, "r:xz") as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(".txt"):
                    f = tar.extractfile(member)
                    data = f.read().decode('utf-8').splitlines()

                    extracted_data = []
                    line_status = []

                    for line in data:
                        status = self.classify_line(line)
                        columns = line.split(',')

                        if len(columns) == 4:
                            extracted_data.append(columns)
                        elif len(columns) < 4:
                            columns.extend([None] * (4 - len(columns)))
                            extracted_data.append(columns)
                            status = 'Null'
                        else:
                            status = 'Anomaly'
                            extracted_data.append(columns[:4])  # Only take the first 4 columns

                        line_status.append(f"{line} -> {status}")
                        print(f"[{line}] : {status} :")

                        # Update counts
                        if status == 'OK':
                            ok_count += 1
                        elif status == 'Null':
                            null_count += 1
                        elif status == 'Anomaly':
                            anomaly_count += 1

                    df = pd.DataFrame(extracted_data, columns=["datetime", "detik", "humidity", "temperature"])

                    log_content.append(f"Data from {member.name}:\n{df.to_string(index=False)}\n")
                    log_content.append(f"Line Status in {member.name}:\n" + "\n".join(line_status) + "\n")

        # Prepare summary for the individual file
        summary = f"Summary for {file_name}:\nOK Count: {ok_count}\nNull Count: {null_count}\nAnomaly Count: {anomaly_count}\n"
        log_content.insert(0, summary)

        # Write the log file for the individual .tar.xz file
        log_file_path = os.path.join(self.output_folder, f"{file_name}_log.txt")
        with open(log_file_path, "w") as log_file:
            log_file.write("\n".join(log_content))

        # Store summary for the summary file
        self.summary_content.append(summary)

    def process_folder(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".tar.xz"):
                file_path = os.path.join(self.folder_path, file_name)
                self.process_file(file_path, file_name)

        # Write the summary file for all processed .tar.xz files
        summary_file_path = os.path.join(self.output_folder, "summary_all.txt")
        with open(summary_file_path, "w") as summary_file:
            summary_file.write("\n".join(self.summary_content))
            print(hello)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(hello)
        print("Usage: python3 file.py folder_path")
        sys.exit(1)

    folder_path = sys.argv[1]
    processor = TarXZProcessor(folder_path)
    processor.process_folder()
