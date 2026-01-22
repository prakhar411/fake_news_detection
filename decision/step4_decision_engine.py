def final_decision(step2: dict, step3_public: dict) -> dict:
    """
    FINAL ULTRA-LOOSE DECISION ENGINE
    (Recall-first, demo-safe, realistic)
    """

    logical_score = step2.get("score", 0.0)

    evidence_strength = step3_public.get("evidence_strength", "none")
    evidence_score = step3_public.get("evidence_score", 0.4)

    # ------------------------------------------------
    # ONLY block absolute nonsense
    # ------------------------------------------------
    if logical_score < 0.15:
        return {
            "final_label": "unverified",
            "confidence_score": logical_score,
            "explanation": "Claim is logically implausible",
            "status_color": "grey"
        }

    # ------------------------------------------------
    # BOTH sources → VERIFIED
    # ------------------------------------------------
    if evidence_strength == "very_strong":
        return {
            "final_label": "verified",
            "confidence_score": max(evidence_score, 0.9),
            "explanation": "Confirmed by multiple independent reliable sources",
            "status_color": "green"
        }

    # ------------------------------------------------
    # ANY external evidence → LIKELY REAL
    # ------------------------------------------------
    if evidence_strength in {
        "moderate",
        "strong",
        "crowd",
        "news",
        "google"
    }:
        return {
            "final_label": "likely_real",
            "confidence_score": max(evidence_score, 0.7),
            "explanation": "Reported by external sources",
            "status_color": "light_green"
        }

    # ------------------------------------------------
    # NOTHING FOUND → UNCERTAIN
    # ------------------------------------------------
    return {
        "final_label": "uncertain",
        "confidence_score": min(evidence_score, 0.5),
        "explanation": "No external confirmation available",
        "status_color": "orange"
    }
