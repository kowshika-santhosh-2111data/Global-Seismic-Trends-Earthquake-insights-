import sqlalchemy
import pandas as pd
from urllib.parse import quote_plus

password = quote_plus("Kowshika*1999")

engine = sqlalchemy.create_engine(
    f"mysql+pymysql://root:{password}@localhost/earthquake_db",echo = True)

def main():
    #Load csv file
    df = pd.read_csv("cleaned_earthquake_data.csv")
    print(df.head())
    print(df.info())
    print(df.shape)
    #insert into sql
    df.to_sql(
        name = "earthquake",
        con = engine,
        if_exists = "replace",
        index = False
    )
    print("Data inserted into Mysql successfully")

if __name__ == "__main__":

    main()
