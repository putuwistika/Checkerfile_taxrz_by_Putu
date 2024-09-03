import tarfile
import pandas as pd
import re
import os
import sys
from sqlalchemy import create_engine

class TarXZProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        
        # Hard-coded PostgreSQL connection URL
        self.db_url = 'postgresql+psycopg2://putuwistika:Dev!!@localhost:5432/weather_data'
        self.engine = create_engine(self.db_url)
        
        self.ok_data = []

    def classify_line(self, line):
        if re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+,\d+(\.\d+)?,\d+(\.\d+)?$", line):
            return 'OK'
        elif re.match(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},$", line):
            return 'Null'
        else:
            return 'Anomaly'

    def process_file(self, file_path):
        null_count = 0
        anomaly_count = 0
        ok_count = 0

        with tarfile.open(file_path, "r:xz") as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith(".txt"):
                    f = tar.extractfile(member)
                    data = f.read().decode('utf-8').splitlines()

                    for line in data:
                        status = self.classify_line(line)
                        if status == 'OK':
                            columns = line.split(',')
                            if len(columns) == 4:
                                self.ok_data.append(columns)
                            ok_count += 1
                        elif status == 'Null':
                            null_count += 1
                        elif status == 'Anomaly':
                            anomaly_count += 1

        # Check if the file has all OK data and no Null or Anomaly
        if ok_count > 0 and null_count == 0 and anomaly_count == 0:
            print(f"File {os.path.basename(file_path)} memiliki semua data OK tanpa Null atau Anomaly.")
            # Convert the data to DataFrame and insert it into PostgreSQL
            self.save_to_db()
        else:
            print(f"File {os.path.basename(file_path)} tidak memenuhi syarat.")

    def process_folder(self):
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith(".tar.xz"):
                file_path = os.path.join(self.folder_path, file_name)
                self.process_file(file_path)
                # Reset ok_data after each file is processed
                self.ok_data = []

    def save_to_db(self):
        if self.ok_data:
            df = pd.DataFrame(self.ok_data, columns=["datetime", "detik", "humidity", "temperature"])
            df['datetime'] = pd.to_datetime(df['datetime'])  # Convert datetime column to pandas datetime type
            df['detik'] = pd.to_numeric(df['detik'])  # Convert detik column to numeric type
            df['humidity'] = pd.to_numeric(df['humidity'])  # Convert humidity column to numeric type
            df['temperature'] = pd.to_numeric(df['temperature'])  # Convert temperature column to numeric type

            try:
                df.to_sql('sensor_readings', self.engine, if_exists='append', index=False)
                print(f"{len(df)} baris data berhasil dimasukkan ke dalam database.")
            except Exception as e:
                print(f"Terjadi kesalahan saat memasukkan data ke database: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 version_3_file.py folder_path")
        sys.exit(1)

    folder_path = sys.argv[1]
    processor = TarXZProcessor(folder_path)
    processor.process_folder()
