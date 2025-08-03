import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IPO_CSV_PATH = os.path.join(BASE_DIR, "data", "ipo.csv")
NEWS_CSV_PATH = os.path.join(BASE_DIR, "data", "training_data_26000.csv")

def get_ipo_data():
    ipo_df = pd.read_csv(IPO_CSV_PATH)
    ipo_df.columns = [col.strip() for col in ipo_df.columns]

    news_df = pd.read_csv(NEWS_CSV_PATH)
    news_df = news_df[news_df['Content'].str.contains("IPO", case=False, na=False)]

    articles = []
    seen_urls = set()  # Track seen URLs to prevent duplicates
    ipo_details_dict = {}

    for _, row in ipo_df.iterrows():
        ipo_name = str(row["IPO_Name"]).strip()
        ipo_name_lower = ipo_name.lower()

        # Calculate total subscription from QIB, HNI, and RII
        qib = row.get("QIB", "N/A")
        hni = row.get("HNI", "N/A")
        rii = row.get("RII", "N/A")
        
        # Try to calculate total subscription if all values are numeric
        total_subscription = "N/A"
        try:
            if qib != "N/A" and hni != "N/A" and rii != "N/A":
                qib_val = float(str(qib).replace(',', ''))
                hni_val = float(str(hni).replace(',', ''))
                rii_val = float(str(rii).replace(',', ''))
                total_val = qib_val + hni_val + rii_val
                total_subscription = f"{total_val:.2f}x"
        except (ValueError, TypeError):
            pass
        
        ipo_details_dict[ipo_name] = {
            "Date": row.get("Date", "N/A"),
            "Issue Size (Cr)": row.get("Issue_Size(crores)", "N/A"),
            "QIB": qib,
            "HNI": hni,
            "Retail": rii,
            "Total Subscription": total_subscription,
            "Issue Price": row.get("Issue_price", "N/A"),
            "Listing Open": row.get("Listing_Open", "N/A"),
            "Listing Close": row.get("Listing_Close", "N/A"),
            "Listing Gain (%)": row.get("Listing_Gains(%)", "N/A"),
            "CMP": row.get("CMP", "N/A"),
            "Current Gain (%)": row.get("Current_gains", "N/A")
        }

        matching_articles = news_df[news_df['Content'].str.lower().str.contains(ipo_name_lower)]
        for _, art in matching_articles.iterrows():
            article_url = art.get('URL', '')
            # Only add article if we haven't seen this URL before
            if article_url not in seen_urls:
                seen_urls.add(article_url)
                articles.append({
                    'IPO': ipo_name,  # ✅ Use 'IPO' key for compatibility
                    'URL': article_url,
                    'Content': art.get('Content', ''),
                    'Summary': art.get('Summary', ''),
                    'Sentiment': art.get('Sentiment', 'neutral').lower()
                })

    return articles, ipo_details_dict


def extract_ipo_names(articles):
    return sorted(set(article["IPO"] for article in articles if "IPO" in article))


def filter_articles_by_ipo(articles, ipo_name):
    return [a for a in articles if a.get('IPO', '').lower() == ipo_name.lower()]
