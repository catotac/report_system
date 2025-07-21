from fastapi import APIRouter, Request, Body, HTTPException, Query
from fastapi.responses import FileResponse
from app.models import DocumentRequest, PromptTemplate
from app.llm_utils import generate_document_with_loop, self_reflect_and_improve, evaluate_generation, export_to_docx
from app.db import save_document, get_prompt_template
import os

router = APIRouter()

doc_types = ["report", "review", "assessment", "document_checker"]

@router.post("/generate/{doc_type}")
async def generate_doc(doc_type: str, request: DocumentRequest):
    assert doc_type in doc_types, "Invalid doc type"
    doc_result = generate_document_with_loop(doc_type, request)
    save_document(request, doc_result)
    return doc_result

@router.get("/prompt_template/{doc_type}")
async def get_prompt(doc_type: str, group_id: str = Query("default"), section: str = Query(None), subsection: str = Query(None)):
    from app.prompts import load_group_template
    return {"template": load_group_template(doc_type, group_id, section, subsection)}

@router.post("/prompt_template/{doc_type}")
async def update_prompt_template(doc_type: str, template: str = Body(..., embed=True), group_id: str = Query("default"), section: str = Query(None), subsection: str = Query(None)):
    # Only allow known doc types
    if doc_type not in doc_types:
        raise HTTPException(status_code=400, detail="Invalid doc type")
    # Determine file path
    if section and subsection:
        path = f"app/templates/{group_id}_{section}_{subsection}_prompt_template.txt"
    elif section:
        path = f"app/templates/{group_id}_{section}_prompt_template.txt"
    elif group_id != "default":
        path = f"app/templates/{group_id}_prompt_template.txt"
    else:
        path = f"app/templates/{doc_type}_prompt_template.txt"
    try:
        with open(path, 'w') as f:
            f.write(template)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save template: {e}")
    return {"status": "success"}

@router.post("/self_reflect")
async def self_reflect_endpoint(request: dict):
    """Endpoint for self-reflection and improvement based on evaluation scores."""
    section = request.get("section")
    subsection = request.get("subsection")
    current_text = request.get("text", "")
    context = request.get("context", "")
    group_id = request.get("group_id", "default")
    
    if not section or not subsection:
        raise HTTPException(status_code=400, detail="Section and subsection are required")
    
    # Evaluate current text
    evaluation = evaluate_generation(current_text)
    
    # Generate improved version through self-reflection
    improved_text = self_reflect_and_improve(current_text, evaluation, section, subsection, context, group_id)
    
    return {
        "original_text": current_text,
        "improved_text": improved_text,
        "evaluation": evaluation.dict()
    }

@router.post("/export_docx/{doc_type}")
async def export_docx(doc_type: str, request: DocumentRequest):
    assert doc_type in doc_types, "Invalid doc type"
    doc_result = generate_document_with_loop(doc_type, request)
    file_path = export_to_docx(doc_result)
    return FileResponse(file_path, filename=f"{request.title or 'report'}.docx", media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
