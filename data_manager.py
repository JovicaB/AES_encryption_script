import pandas as pd
import os


class DataManager:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self._create_file()

    def _create_file(self):
        df = pd.DataFrame(columns=["id", "document"])
        df.to_parquet(self.file_path, index=False)

    def get_data(self):
        return pd.read_parquet(self.file_path)

    def save_data(self, data: dict):
        df = self.get_data()
        new_row = pd.DataFrame([data])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_parquet(self.file_path, index=False)

    def generate_new_id(self):
        df = self.get_data()
        if df.empty:
            return 1
        return int(df["id"].max()) + 1


