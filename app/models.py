from pydantic import BaseModel
from typing import List, Dict

class PromptTemplate(BaseModel):
    section: str
    subsection: str
    template: str

class EvaluationResult(BaseModel):
    groundedness: float
    completeness: float
    coherence: float

class SectionOutput(BaseModel):
    section: str
    subsection: str
    generated_text: str
    evaluation: EvaluationResult

class DocumentRequest(BaseModel):
    title: str
    sections: Dict[str, List[str]]
    custom_prompts: Dict[str, str] = {}
    user_feedback: Dict[str, str] = {}
    group_id: str = "default"  # New field for group support

class DocumentResult(BaseModel):
    document_type: str
    title: str
    sections: List[SectionOutput]
