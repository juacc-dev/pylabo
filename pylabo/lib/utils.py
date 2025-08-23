import pandas as pd


def set_if_none(value, default):
    return default if value is None else value


def insert_empty_xerr(df):
    df.insert(1, "", pd.Series())
