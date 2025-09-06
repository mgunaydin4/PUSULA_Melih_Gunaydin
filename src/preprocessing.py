import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from rapidfuzz import process

def convert_to_integer(df, cols, values):
    for col in cols:
        for value in values:
            df[col] = df[col].astype(str).str.replace(value, "")
        df[col] = df[col].astype(int)
    return df

def fill_missing(df):
    for col in ["KanGrubu", "KronikHastalik", "Cinsiyet"]:
        df[col] = df.groupby("HastaNo")[col].transform(lambda x: x.fillna(method="ffill").fillna(method="bfill"))
    df["Alerji"] = df["Alerji"].fillna("yok")
    df["Cinsiyet"]= df["Cinsiyet"].fillna("Bilinmiyor")
    df["KronikHastalik"] = df["KronikHastalik"].fillna("yok")
    df["Tanilar"] = df["Tanilar"].fillna("bilinmiyor")
    df["KanGrubu"] = df["KanGrubu"].fillna("bilinmiyor")
    df["UygulamaYerleri"] = df["UygulamaYerleri"].fillna("bilinmiyor")
    return df

def regulate_tanilar(df, group_col="HastaNo", target_col="Tanilar", threshold=70):
    for hasta, group in df.groupby(group_col):
        first_val = group[target_col].dropna().iloc[0] if not group[target_col].dropna().empty else np.nan
        if pd.isna(first_val): continue
        def replace_val(val):
            if pd.isna(val): return val
            score = process.extractOne(val, [first_val])[1]
            return first_val if score >= threshold else val
        df.loc[group.index, target_col] = group[target_col].apply(replace_val)
    return df

def knn_impute(df, col="Bolum", n_neighbors=3):
    le = LabelEncoder()
    non_null = df[col].dropna()
    le.fit(non_null)
    df[col+"_enc"] = df[col].map(lambda x: le.transform([x])[0] if pd.notna(x) else None)
    imputer = KNNImputer(n_neighbors=n_neighbors)
    df[col+"_enc"] = imputer.fit_transform(df[[col+"_enc"]])
    df[col+"_filled"] = df[col+"_enc"].round().astype(int).map(lambda x: le.inverse_transform([x])[0])
    df[col] = df[col+"_filled"]
    df.drop([col+"_enc", col+"_filled"], axis=1, inplace=True)
    return df
