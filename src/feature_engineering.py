import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def create_patient_features(df):
    for col in ["KronikHastalik","Alerji","Tanilar","UygulamaYerleri","TedaviAdi","Bolum"]:
        temp = df.groupby("HastaNo")[col].unique().apply(lambda x: ", ".join(x) if len(x)>0 else "")
        df = df.merge(temp.reset_index(), on="HastaNo", suffixes=("","_Total"))

    df["TedaviAdi_Count"] = df.groupby("HastaNo")["TedaviAdi"].transform("nunique")
    df["Bolum_Count"] = df.groupby("HastaNo")["Bolum"].transform("nunique")
    df["HASTA_SESSION_COUNT"] = df.groupby("HastaNo")["HastaNo"].transform("count")
    df["AVERAGE_UYGULAMA_SURESI_DURATION"] = df.groupby("HastaNo")["UygulamaSuresi"].transform("mean")
    df["TANI_COUNT"] = df["Tanilar_Total"].apply(lambda x: len(str(x).split(",")))
    df["UYGULAMA_YERI_COUNT"] = df["UygulamaYerleri_Total"].apply(lambda x: len(str(x).split(",")))
    return df

def tfidf_features(df, column, prefix, max_features=100):
    tfidf = TfidfVectorizer(max_features=max_features)
    matrix = tfidf.fit_transform(df[column].fillna(""))
    tfidf_df = pd.DataFrame(matrix.toarray(),
                            columns=[f"{prefix}_{w}" for w in tfidf.get_feature_names_out()],
                            index=df.index)
    return tfidf_df
