import re

VALID_EVENTS = {
    "explosion", "fire", "flood",
    "earthquake", "landslide",
    "cyclone", "accident", "blast"
}

LOCATION_HINTS = {
    "station", "city", "district",
    "village", "area", "road"
}

TIME_PATTERNS = [
    r"\byesterday\b",
    r"\btoday\b",
    r"\blast night\b",
    r"\b\d{1,2}\s(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b"
]

def verify_event(claim: dict) -> dict:
    signals = {}

    # 1. Event validity
    event = (claim.get("event_type") or "").lower()
    signals["event_valid"] = event in VALID_EVENTS

    # 2. Location plausibility
    location = (claim.get("location") or "").lower()
    signals["location_valid"] = any(hint in location for hint in LOCATION_HINTS)

    # 3. Time plausibility
    time = (claim.get("time") or "").lower()
    signals["time_valid"] = any(re.search(p, time) for p in TIME_PATTERNS)

    # 4. Semantic coherence (simple rule)
    signals["semantic_coherence"] = not (
        event == "earthquake" and "station" in location
    )

    # -----------------------------
    # Final score
    # -----------------------------
    score = sum(signals.values()) / len(signals)

    verdict = (
        "likely_real" if score >= 0.7
        else "uncertain" if score >= 0.4
        else "likely_fake"
    )

    return {
        "verdict": verdict,
        "score": round(score, 2),
        "signals": signals
    }
