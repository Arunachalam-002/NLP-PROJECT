import pandas as pd
import os

DATA_PATH = os.path.join("data", "ipo.csv")

def get_ipo_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.iloc[0]
    df = df[1:]
    df.reset_index(drop=True, inplace=True)

    articles = [
        f"{row['IPO Name']} IPO opened on {row['Date']} with issue size ₹{row['Issue Size  (in crores)']} Cr and listed at ₹{row['Listing Open']}"
        for _, row in df.iterrows()
    ]

    ipo_details = {}
    for _, row in df.iterrows():
        ipo_name = str(row["IPO Name"]).strip()
        ipo_details[ipo_name] = {
            "Date": row["Date"],
            "Issue Size (Cr)": row["Issue Size  (in crores)"],
            "QIB": row["QIB"],
            "HNI": row["HNI"],
            "Retail": row["RII"],
            "Total Subscription": row["Total"],
            "Issue Price": row["Issue"],
            "Listing Open": row["Listing Open"],
            "Listing Close": row["Listing Close"],
            "Listing Gain (%)": row["Listing Gains(%)"],
            "CMP": row["CMP"],
            "Current Gain (%)": row["Current  Gains (%)"]
        }

    return articles, ipo_details

def extract_ipo_names(articles):
    return sorted([line.split(" IPO")[0] for line in articles])

def filter_articles_by_ipo(articles, ipo_name):
    return [a for a in articles if ipo_name.lower() in a.lower()]
