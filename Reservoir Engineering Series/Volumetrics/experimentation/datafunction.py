import pandas as pd

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        if not {'x', 'y', 'depth'}.issubset(data.columns):
            raise ValueError("CSV file must contain 'x', 'y', and 'depth' columns.")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise e
