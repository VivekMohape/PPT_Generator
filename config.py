import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_API_KEY")
    TEMPLATE_DIR = "templates"
    OUTPUT_PATH = "output_presentation.pptx"
    MAX_RETRIES = 3
    MODEL = "gpt-4o"
