from os import stat_result
from pipeline import run_verification_pipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#  uvicorn api:app --host 0.0.0.0 --port 8000
# ngrok http 8000


if __name__ == "__main__":
    text = "Landslide kills 5 in Himachal Pradesh in July 2025"


    result = run_verification_pipeline(text)
    print(stat_result["public"])
    print(result)
