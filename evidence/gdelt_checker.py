import requests

GDELT_ENDPOINT = "https://api.gdeltproject.org/api/v2/doc/doc"

EVENT_SYNONYMS = {
    "fire": ["fire", "blaze"],
    "explosion": ["explosion", "blast"],
    "flood": ["flood", "flooding"],
    "earthquake": ["earthquake", "quake"],
}


def check_gdelt(claim: dict) -> dict:
    """
    STRICT GDELT checker.
    Only returns True if the SAME event at the SAME location is reported.
    """

    event = (claim.get("event_type") or "").lower()
    location = (claim.get("location") or "").lower()

    city = location.split()[0] if location else ""
    keywords = EVENT_SYNONYMS.get(event, [event])

    query = f"{event} {city}"

    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": 10,
        "sort": "HybridRel",
    }

    try:
        r = requests.get(GDELT_ENDPOINT, params=params, timeout=10)
        data = r.json()
    except Exception:
        return {"direct_found": False}

    articles = data.get("articles", [])

    for a in articles:
        title = a.get("title", "").lower()

        # 🔒 STRICT EVENT MATCH
        if not any(k in title for k in keywords):
            continue

        # 🔒 STRICT LOCATION MATCH
        if city not in title:
            continue

        # ✅ REAL MATCH FOUND
        return {
            "direct_found": True,
            "count": 1,
            "titles": [a.get("title")]
        }

    # ❌ No strict match
    return {
        "direct_found": False
    }
