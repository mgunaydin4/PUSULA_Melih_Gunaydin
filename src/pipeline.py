from .preprocessing import convert_to_integer, fill_missing, regulate_tanilar, knn_impute
from .feature_engineering import create_patient_features, tfidf_features
import pandas as pd

class TalentPipeline:
    def __init__(self, knn_neighbors=3, tfidf_features=100, tanilar_threshold=70):
        self.knn_neighbors = knn_neighbors
        self.tfidf_features = tfidf_features
        self.tanilar_threshold = tanilar_threshold

    def fit_transform(self, df):
        df = convert_to_integer(df, ["TedaviSuresi","UygulamaSuresi"], ["Seans","Dakika"])
        df = fill_missing(df)
        df = regulate_tanilar(df, threshold=self.tanilar_threshold)
        df = knn_impute(df, n_neighbors=self.knn_neighbors)
        df = create_patient_features(df)

        tfidf_tanilar_df = tfidf_features(df, "Tanilar_Total","tfidf_tanilar",self.tfidf_features)
        tfidf_uyg_df = tfidf_features(df, "UygulamaYerleri_Total","tfidf_uyg",self.tfidf_features)
        tfidf_tedavi_df = tfidf_features(df, "TedaviAdi","tfidf_tedavi",self.tfidf_features)

        df_final = pd.concat([df.reset_index(drop=True),
                              tfidf_tanilar_df.reset_index(drop=True),
                              tfidf_uyg_df.reset_index(drop=True),
                              tfidf_tedavi_df.reset_index(drop=True)], axis=1)

        df_final = df_final.drop(["TedaviAdi","Tanilar_Total","UygulamaYerleri_Total"], axis=1)
        return df_final
