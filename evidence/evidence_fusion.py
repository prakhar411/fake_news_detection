from datetime import datetime, timedelta
from .newsapi_checker import check_newsapi
from .google_checker import check_google


def text_match(claim_value, text):
    if not claim_value or not text:
        return False
    return claim_value.lower() in text.lower()


# def run_step3_evidence(claim: dict) -> dict:
#     newsapi = check_newsapi(claim)
#     google = check_google(claim)

#     news_found = newsapi.get("found", False)
#     google_found = google.get("count", 0) > 0

#     # BOTH SOURCES
#     if news_found and google_found:
#         return {
#             "public": {
#                 "evidence_strength": "very_strong",
#                 "evidence_score": 0.9,
#                 "message": "Found in news and web search"
#             }
#         }

#     # ANY ONE SOURCE
#     if news_found or google_found:
#         return {
#             "public": {
#                 "evidence_strength": "moderate",
#                 "evidence_score": 0.7,
#                 "message": "Found in at least one external source"
#             }
#         }

#     # NOTHING
#     return {
#         "public": {
#             "evidence_strength": "none",
#             "evidence_score": 0.4,
#             "message": "No external confirmation available"
#         }
#     }

def run_step3_evidence(claim: dict) -> dict:
    newsapi = check_newsapi(claim)
    google = check_google(claim)

    news_found = newsapi.get("found", False)
    google_count = google.get("count", 0)

    # VERY STRONG: authoritative + crowd corroboration
    if news_found and google_count >= 5:
        return {
            "public": {
                "evidence_strength": "very_strong",
                "evidence_score": 0.9,
                "message": (
                    "Confirmed by trusted news outlet and "
                    f"{google_count} independent web sources"
                )
            }
        }

    # STRONG: crowd corroboration alone
    if google_count >= 5:
        return {
            "public": {
                "evidence_strength": "strong",
                "evidence_score": 0.8,
                "message": (
                    f"Reported consistently across "
                    f"{google_count} independent web sources"
                )
            }
        }

    # MODERATE: single authoritative source only
    if news_found and google_count < 5:
        return {
            "public": {
                "evidence_strength": "moderate",
                "evidence_score": 0.6,
                "message": (
                    "Reported by a news outlet but lacks "
                    "sufficient independent corroboration"
                )
            }
        }

    # UNLIKELY: weak or sparse signals
    if google_count > 0:
        return {
            "public": {
                "evidence_strength": "unlikely",
                "evidence_score": 0.45,
                "message": (
                    f"Only {google_count} weak corroborating sources found"
                )
            }
        }

    # VERY UNLIKELY: nothing found
    return {
        "public": {
            "evidence_strength": "very_unlikely",
            "evidence_score": 0.3,
            "message": "No reliable public evidence found"
        }
    }
