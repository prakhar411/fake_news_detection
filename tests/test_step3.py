from evidence_fusion import run_step3_evidence

claim = {
    "event_type": "Explosion",
    "location": "Kanpur railway station",
    "time": "yesterday"
}

result = run_step3_evidence(claim)
print(result)
