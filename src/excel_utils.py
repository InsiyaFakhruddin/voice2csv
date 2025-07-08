# src/excel_utils.py

import pandas as pd

def load_csv(path):
    return pd.read_csv(path)

def update_review(df, unique_id, new_review):
    df.loc[df["uniqueID"] == int(unique_id), "review"] = new_review
    return df

def save_csv(df, path):
    df.to_csv(path, index=False)
