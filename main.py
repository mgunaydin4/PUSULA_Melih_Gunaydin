import os
import pandas as pd
from src.pipeline import TalentPipeline
from src.data_loader import load_data
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_colwidth", None)


DATA_PATH = "data"
DATA_FILE = "Talent_Academy_Case_DT_2025.xlsx"

df = load_data(DATA_PATH, DATA_FILE)

pipeline = TalentPipeline(knn_neighbors=3, tfidf_features=100, tanilar_threshold=70)
df_final = pipeline.fit_transform(df)

print(df_final)
