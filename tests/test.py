from verifier import verify_event

claim = {
    "event_type": "Explosion",
    "location": "Kanpur railway station",
    "time": "yesterday"
}

result = verify_event(claim)
print(result)
