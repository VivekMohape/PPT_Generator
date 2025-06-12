import openai
import json
from models.schemas import PresentationPlan, SlideContent
from config import Config
from retrying import retry

openai.api_key = Config.OPENAI_API_KEY

SLIDE_TYPES = ["summary_slide", "data_slide", "image_slide", "conclusion_slide"]

@retry(stop_max_attempt_number=Config.MAX_RETRIES, wait_fixed=1000)
def call_openai(system_prompt, raw_text):
    response = openai.ChatCompletion.create(
        model=Config.MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

def generate_presentation_plan(raw_text: str, reference_instruction: str = None) -> PresentationPlan:
    base_instruction = f"""
    You are an AI presentation planner.

    Based on input text, output a JSON object with following schema:

    {{
        \"slides\": [
            {{
                \"slide_type\": <one of {SLIDE_TYPES}>,
                \"title\": <string>,
                \"content\": <dictionary of key-value pairs for placeholders>,
                \"image_paths\": (optional dictionary of placeholder name to image path)
            }}
        ]
    }}

    Output only valid JSON, nothing else.
    """
    full_prompt = base_instruction
    if reference_instruction:
        full_prompt += f"\nHere is an example slide structure to adapt: {reference_instruction}"

    try:
        raw_output = call_openai(full_prompt, raw_text)
        data = json.loads(raw_output)
        slides = [SlideContent(**slide) for slide in data["slides"]]
        return PresentationPlan(slides=slides)
    except Exception as e:
        raise ValueError(f"AI generation failed after retries: {str(e)}")
