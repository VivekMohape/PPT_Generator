from pydantic import BaseModel
from typing import List, Dict, Optional

class SlideContent(BaseModel):
    slide_type: str
    title: str
    content: Dict[str, str]
    image_paths: Optional[Dict[str, str]] = None

class PresentationPlan(BaseModel):
    slides: List[SlideContent]
