import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

EVENT_SYNONYMS = {
    "fire": ["fire", "blaze"],
    "explosion": ["explosion", "blast"],
    "flood": ["flood", "flooding"],
    "earthquake": ["earthquake", "quake"],
    "landslide": ["landslide", "mudslide"],
}


# def check_newsapi(claim: dict) -> dict:
#     event = (claim.get("event_type") or "").lower()
#     location = (claim.get("location") or "").lower()
#     time_ref = (claim.get("time_reference") or "").lower()

#     if not event or not location:
#         return {"found": False, "count": 0, "articles": []}

#     city = location.split()[0]
#     keywords = EVENT_SYNONYMS.get(event, [event])

#     params = {
#         "q": f"{event} {city}",
#         "language": "en",
#         "sortBy": "relevancy",
#         "pageSize": 10,
#         "apiKey": NEWS_API_KEY
#     }

#     try:
#         r = requests.get(NEWS_ENDPOINT, params=params, timeout=10)
#         data = r.json()
#     except Exception:
#         return {"found": False, "count": 0, "articles": []}

#     articles = data.get("articles", [])
#     valid_articles = []

#     for a in articles:
#         title = (a.get("title") or "").lower()
#         desc = (a.get("description") or "").lower()
#         published = a.get("publishedAt")

#         combined_text = f"{title} {desc}"

#         # 🔒 Event match
#         if not any(k in combined_text for k in keywords):
#             continue

#         # 🔒 Location match
#         if city not in combined_text:
#             continue

#         # 🔒 Time window (±48h)
#         if published:
#             try:
#                 pub_time = datetime.fromisoformat(published.replace("Z", ""))
#                 if pub_time < datetime.utcnow() - timedelta(hours=48):
#                     continue
#             except Exception:
#                 continue

#         valid_articles.append({
#             "title": a.get("title"),
#             "description": a.get("description"),
#             "publishedAt": published,
#             "source": a.get("source", {}).get("name")
#         })

#     return {
#         "found": len(valid_articles) > 0,
#         "count": len(valid_articles),
#         "articles": valid_articles
#     }


def check_newsapi(claim: dict) -> dict:
    event = (claim.get("event_type") or "").lower()
    location = (claim.get("location") or "").lower()

    # VERY LOOSE QUERY
    query = f"{event} {location}".strip()

    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    try:
        r = requests.get(NEWS_ENDPOINT, params=params, timeout=10)
        data = r.json()
    except Exception:
        return {"found": False, "count": 0}

    articles = data.get("articles", [])

    # 🔥 ANY ARTICLE COUNTS
    if articles:
        return {
            "found": True,
            "count": len(articles),
            "titles": [a.get("title") for a in articles]
        }

    return {
        "found": False,
        "count": 0
    }
