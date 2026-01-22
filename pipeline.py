from extractor.extractor import extract_claim
from verifier.verifier import verify_event
from evidence.evidence_fusion import run_step3_evidence
from decision.step4_decision_engine import final_decision


def run_verification_pipeline(text: str) -> dict:
    """
    End-to-end verification pipeline.
    """

    # STEP 1: Extraction
    claim = extract_claim(text)

    if not claim or not claim.get("event_type"):
        return {
            "final_label": "uncertain",
            "confidence_score": 0.0,
            "explanation": "Insufficient information to verify this report",
            "status_color": "orange"
        }

    # STEP 2: Logical verification
    step2 = verify_event(claim)

    # STEP 3: External evidence
    step3 = run_step3_evidence(claim)["public"]

    # STEP 4: Final decision
    final = final_decision(
        step2={"score": step2["score"]},
        step3_public=step3
    )

    return final
