
# # Event Detection

# EVENT_KEYWORDS = {
#     "fire": ["fire", "burning", "blaze", "flames"],
#     "flood": ["flood", "waterlogging", "overflow"],
#     "earthquake": ["earthquake", "tremor", "quake"],
#     "accident": ["accident", "crash", "collision"],
#     "explosion": ["blast", "explosion", "bomb"]
# }

# def extract_event_type(text: str):
#     text = text.lower()
#     for event, keywords in EVENT_KEYWORDS.items():
#         for k in keywords:
#             if k in text:
#                 return event
#     return None


# # LOCATION & TIME EXTRACTION USING spaCy
# import spacy
# nlp = spacy.load("en_core_web_sm")

# def extract_location_time(text: str):
#     doc = nlp(text)

#     location = None
#     time_ref = None

#     for ent in doc.ents:
#         if ent.label_ in ["GPE", "LOC"]:
#             location = ent.text
#         elif ent.label_ in ["DATE", "TIME"]:
#             time_ref = ent.text

#     return location, time_ref



# def layer1_extract(text: str):
#     event = extract_event_type(text)
#     location, time_ref = extract_location_time(text)

#     return {
#         "event_type": event,
#         "location": location,
#         "time_reference": time_ref,
#         "source": "layer1"
#     }

# def is_incomplete(extracted):
#     return (
#         extracted["event_type"] is None or
#         extracted["location"] is None
#     )


# from .gemini_fallback import gemini_extract

# def extract_claim(text: str):
#     layer1 = layer1_extract(text)

#     if not is_incomplete(layer1):
#         return layer1

#     # Fallback to Gemini
#     layer2 = gemini_extract(text)
#     layer2["source"] = "gemini_fallback"
#     return layer2



# extractor/extractor.py

# --------------------------------------------------
# Event keywords
# --------------------------------------------------
EVENT_KEYWORDS = {
    "fire": ["fire", "burning", "blaze", "flames"],
    "flood": ["flood", "waterlogging", "overflow"],
    "earthquake": ["earthquake", "tremor", "quake"],
    "accident": ["accident", "crash", "collision"],
    "explosion": ["blast", "explosion", "bomb"],
    "landslide": ["landslide", "mudslide"]
}


def extract_event_type(text: str):
    text = text.lower()
    for event, keywords in EVENT_KEYWORDS.items():
        for k in keywords:
            if k in text:
                return event
    return None


# --------------------------------------------------
# Location & time extraction using spaCy
# --------------------------------------------------
import spacy
nlp = spacy.load("en_core_web_sm")


def extract_location_time(text: str):
    doc = nlp(text)

    location = None
    time_ref = None

    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            location = ent.text
        elif ent.label_ in ["DATE", "TIME"]:
            time_ref = ent.text

    return location, time_ref


# --------------------------------------------------
# Layer 1 extraction
# --------------------------------------------------
def layer1_extract(text: str):
    event = extract_event_type(text)
    location, time_ref = extract_location_time(text)

    return {
        "event_type": event,
        "location": location,
        "time_reference": time_ref,
        "source": "layer1"
    }


# --------------------------------------------------
# Incompleteness check
# --------------------------------------------------
def is_incomplete(extracted: dict):
    return (
        extracted.get("event_type") is None or
        extracted.get("location") is None
    )


# --------------------------------------------------
# SINGLE extract_claim (Gemini REMOVED)
# --------------------------------------------------
def extract_claim(text: str):
    # 🔒 Question gate
    if text.strip().endswith("?"):
        return {
            "is_question": True,
            "event_type": None,
            "location": None,
            "time_reference": None,
            "source": "question_gate"
        }

    layer1 = layer1_extract(text)

    # No Gemini fallback anymore
    return layer1
