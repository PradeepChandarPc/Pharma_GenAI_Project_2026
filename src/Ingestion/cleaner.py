import pandas as pd

def remove_empty_abstracts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with missing or empty abstracts.
    """
    df = df.dropna(subset=["abstract"])
    df = df[df["abstract"].str.strip() != ""]
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate papers based on PMID.
    """
    return df.drop_duplicates(subset=["pmid"])
