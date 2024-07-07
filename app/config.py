import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID')
