import pandas as pd
from datetime import datetime
import requests
import os
start_year = datetime.now().year - 5
end_year = datetime.now().year
all_records= []
for year in range(start_year, end_year + 1):
    params = {
        "format": "geojson",
        "starttime": f"{year}-01-01",
        "endtime": f"{year}-12-31",
        "minmagnitude": 4
    }
#fetch data from USGS API 
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query",
        params=params 
    )

    if response.status_code != 200:
        print(f"failed for {year}: Error {response.status_code}")
        continue

    data = response.json()
    for eq in data["features"]:
        p = eq["properties"] #incl mag, place, ststus
        g = eq["geometry"]["coordinates"] #incl long,latit,dep

        all_records.append({    #store as row
            "id": eq.get("id"),
            "time": pd.to_datetime(p.get("time"), unit="ms"),
            "updated": pd.to_datetime(p.get("updated"), unit="ms"),
            "latitude": g[1] if g else None,
            "longitude": g[0] if g else None,
            "depth_km": g[2] if g else None,
            "mag": p.get("mag"),
            "magType":p.get("magType"),
            "place" :p.get("place"),
            "status": p.get("status"),
            "tsunami":p.get("tsunami"),
            "alert":p.get("alert"),
            "felt":p.get("felt"),
            "cdi":p.get("cdi"),
            "mmi":p.get("mmi"),
            "sig":p.get("sig"),
            "net":p.get("net"),
            "code":p.get("code"),
            "ids":p.get("ids"),
            "source":p.get("source"),
            "types":p.get("types"),
            "nst":p.get("nst"),
            "dmin":p.get("dmin"),
            "rms":p.get("rms"),
            "gap":p.get("gap"),
            "type":p.get("type")
        })
    

    print(f"{year} → {len(data['features'])} records added")

print("Total records collected:", len(all_records))
df = pd.DataFrame(all_records)
df.head()
df.info()
df.columns
df.shape
os.makedirs("data", exist_ok=True)
df.to_csv("data/raw_earthquake_data.csv", index=False)
