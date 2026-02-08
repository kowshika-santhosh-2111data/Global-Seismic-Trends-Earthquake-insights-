import pandas as pd
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")
import os

raw_path = "data/raw_earthquake_data.csv"
clean_path = "data/cleaned_earthquake_data.csv"

def clean_data():
    df = pd.read_csv(raw_path)
    #remove duplicates
    df = df.drop_duplicates(subset = "id")

    #convert to time & updated columns to datetime
    df['time'] = pd.to_datetime(df['time'],errors = 'coerce') #errors='coerce'for nat(invalid /messy value)
    df['updated'] = pd.to_datetime(df['updated'],errors= 'coerce')

    #keep only earthquake data
    df = df[df["type"] == "earthquake"]

    #drop rows with critical missing values
    df = df.dropna(subset = ["mag","latitude","longitude","time"]) 

    #using regex to extract country
    df['region'] = df['place'].str.extract(r",\s(.*),")
    df["region"] = df["region"].fillna(df["place"])
#handle missing values
    #fill categorical null
    df["source"] = df["source"].fillna("unknown")
    df["alert"] = df["alert"].fillna("none")
    df['place'] = df['place'].fillna("unknown")

    #all string fields
    string_cols = ["magType", "status", "type", "net", "source", "types"]
    for col in string_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)        # ensure string
                .str.strip()        # remove spaces
                .str.lower()        # standardize case
                .replace("nan",None)
            )
    #convert numeric fields
    for col in ["mag", "depth_km", "nst","dmin", "rms", "gap", "magError", "depthError","magNst", "sig"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col],errors="coerce")

            if col == 'nst':
                df[col] = df[col].fillna(0)
            else:
                df[col] = df[col].fillna(df[col].median())


    #add derived columns
    df['year']=df['time'].dt.year
    df['month']=df['time'].dt.month
    df['day']=df['time'].dt.day
    df['day_of_week']=df['time'].dt.day_name()

    #depth_category
    def depth_category(depth):
        if depth < 70:
            return "shallow"
        elif depth <= 300:
            return "intermediate"
        else:
            return "deep"

    df["depth_category"] = df["depth_km"].apply(depth_category)
    df["is_shallow"] = df["depth_km"] < 70
    df["is_strong"] = df["mag"] >= 6.0

    #magnitude_category
    def magnitude_category(mag):
        if mag < 5.0:
            return "light"
        elif mag < 6.0:
            return "moderate"
        elif mag < 7.0:
            return "strong"
        else:
            return "destructive"

    df["magnitude_category"] = df["mag"].apply(magnitude_category)

    col_to_drop = ["ids", "felt", "cdi", "mmi"]
    df = df.drop(columns=col_to_drop, errors="ignore")

    #save cleaned data
    os.makedirs("data", exist_ok=True)
    df.to_csv(clean_path, index=False)
    print("cleaned data saved")
    print(df.info())
    print(df.shape)
    print(df["type"].value_counts())
    print(df.isnull().sum().head())

    return df

if __name__ == "__main__":
    clean_data()
