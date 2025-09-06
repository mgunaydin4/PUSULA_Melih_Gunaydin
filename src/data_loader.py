import os
import pandas as pd

def load_data(data_path: str, file_name: str) -> pd.DataFrame:
    """Load Excel File."""
    file_path = os.path.join(data_path, file_name)
    df = pd.read_excel(file_path)
    return df
