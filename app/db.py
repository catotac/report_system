import sqlite3
from app.models import DocumentRequest, DocumentResult
import json

def get_connection():
    conn = sqlite3.connect("documents.db")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        doc_type TEXT,
        result TEXT
    )
    """)
    return conn

def save_document(request: DocumentRequest, result: DocumentResult):
    conn = get_connection()
    conn.execute("INSERT INTO documents (title, doc_type, result) VALUES (?, ?, ?)",
                 (request.title, result.document_type, json.dumps(result.dict())))
    conn.commit()
    conn.close()

def get_prompt_template(doc_type: str):
    from app.prompts import load_template
    return {"template": load_template(doc_type)}
