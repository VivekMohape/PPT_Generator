
import openai
import instructor
from models.schemas import PresentationPlan
from config import Config

# Use instructor's wrapped client
client = instructor.from_openai(
    openai.OpenAI(api_key=Config.OPENAI_API_KEY)
)

SLIDE_TYPES = ["summary_slide", "data_slide", "image_slide", "conclusion_slide"]

def generate_presentation_plan(raw_text: str, reference_instruction: str = None) -> PresentationPlan:
    system_prompt = f"""
    You are an AI presentation planner.

    Based on input text, output a JSON object following this schema.

    - You must generate multiple slides.
    - Each slide must have a valid slide_type from: {SLIDE_TYPES}
    - Fully fill all required fields according to the schema.

    If reference structure is provided, adapt layout structure accordingly.
    """

    if reference_instruction:
        system_prompt += f"\nReference structure to adapt: {reference_instruction}"

    response = client.chat.completions.create(
        model=Config.MODEL,
        response_model=PresentationPlan,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.3
    )

    return response  # Already returns validated Pydantic object
