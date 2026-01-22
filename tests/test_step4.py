from step4_decision_engine import final_decision

step2_result = {
    "verdict": "likely_real",
    "score": 0.75
}

step3_public = {
    "verdict": "not_confirmed",
    "evidence_score": 0.25,
    "evidence_strength": "weak",
    "sources_count": 1,
    "message": "No reliable external confirmation found yet"
}

final = final_decision(step2_result, step3_public)
print(final)
