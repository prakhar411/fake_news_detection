import pytest
from extractor.extractor import extract_claim


# --------------------------------------------------
# TEST 1: Question input (must be gated)
# --------------------------------------------------
def test_question_input():
    text = "landslide in mussoorie on September 2025?"
    result = extract_claim(text)

    assert result.get("is_question") is True
    assert result.get("event_type") is None
    assert result.get("location") is None


# --------------------------------------------------
# TEST 2: Valid factual claim (layer 1)
# --------------------------------------------------
def test_valid_event_location_time():
    text = "Fire broke out in a textile factory in Surat city yesterday"
    result = extract_claim(text)

    assert result.get("event_type") == "fire"
    assert result.get("time_reference") == "yesterday"
    assert result.get("source") == "layer1"


# --------------------------------------------------
# TEST 3: Missing location (should be incomplete)
# --------------------------------------------------
def test_missing_location():
    text = "Major flood reported yesterday"
    result = extract_claim(text)

    # Event may exist
    assert result.get("event_type") == "flood"

    # Location missing
    assert result.get("location") is None


# --------------------------------------------------
# TEST 4: Completely irrelevant text
# --------------------------------------------------
def test_irrelevant_text():
    text = "I like pizza and watching movies"
    result = extract_claim(text)

    assert result.get("event_type") is None
    assert result.get("location") is None


# --------------------------------------------------
# TEST 5: Gemini fallback does NOT crash
# --------------------------------------------------
def test_gemini_fallback_safe():
    text = "Something happened somewhere"

    result = extract_claim(text)

    # Gemini may fail or succeed, but must NEVER crash
    assert "source" in result
    assert result.get("source") in {
        "layer1",
        "gemini_fallback",
        "gemini_rate_limited",
        "gemini_error",
        "gemini_disabled",
        "question_gate"
    }
