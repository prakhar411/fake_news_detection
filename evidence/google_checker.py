import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
SERP_ENDPOINT = "https://serpapi.com/search"


# def check_google(claim: dict) -> dict:
#     event = (claim.get("event_type") or "").lower()
#     location = (claim.get("location") or "").lower()
#     time_ref = (claim.get("time_reference") or "").lower()

#     if not event or not location:
#         return {"count": 0, "results": []}

#     query = f"{event} {location}"

#     params = {
#         "engine": "google",
#         "q": query,
#         "hl": "en",
#         "gl": "in",
#         "num": 10,
#         "api_key": SERP_API_KEY,
#     }

#     try:
#         r = requests.get(SERP_ENDPOINT, params=params, timeout=10)
#         data = r.json()
#     except Exception:
#         return {"count": 0, "results": []}

#     results = data.get("organic_results", [])
#     qualified_results = []
#     domains = set()

#     for res in results:
#         title = (res.get("title") or "").lower()
#         snippet = (res.get("snippet") or "").lower()
#         link = res.get("link", "")

#         combined_text = f"{title} {snippet}"

#         # 🔒 Location must match
#         if location.split()[0] not in combined_text:
#             continue

#         # 🔒 Time hint match (soft)
#         if time_ref:
#             if time_ref not in combined_text and "today" not in combined_text and "yesterday" not in combined_text:
#                 continue

#         if link:
#             try:
#                 domain = link.split("/")[2]
#                 domains.add(domain)
#             except Exception:
#                 pass

#         qualified_results.append({
#             "title": res.get("title"),
#             "snippet": res.get("snippet"),
#             "link": link
#         })

#     return {
#         "count": len(domains),      # independent corroboration
#         "results": qualified_results
#     }

def check_google(claim: dict) -> dict:
    event = claim.get("event_type", "")
    location = claim.get("location", "")

    query = f"{event} {location}"

    params = {
        "engine": "google",
        "q": query,
        "hl": "en",
        "gl": "in",
        "num": 5,
        "api_key": SERP_API_KEY,
    }

    try:
        r = requests.get(SERP_ENDPOINT, params=params, timeout=10)
        data = r.json()
    except Exception:
        return {"count": 0}

    results = data.get("organic_results", [])

    # 🔥 ANY RESULT COUNTS
    return {
        "count": len(results),
        "titles": [r.get("title") for r in results]
    }
