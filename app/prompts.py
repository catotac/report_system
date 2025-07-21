import os

def load_template(doc_type: str) -> str:
    path = f"app/templates/{doc_type}_prompt_template.txt"
    with open(path, 'r') as file:
        return file.read()

def load_group_template(doc_type: str, group_id: str, section: str = None, subsection: str = None) -> str:
    # Try most specific to least specific
    candidates = []
    if section and subsection:
        candidates.append(f"app/templates/{group_id}_{section}_{subsection}_prompt_template.txt")
    if section:
        candidates.append(f"app/templates/{group_id}_{section}_prompt_template.txt")
    candidates.append(f"app/templates/{group_id}_prompt_template.txt")
    candidates.append(f"app/templates/{doc_type}_prompt_template.txt")
    for path in candidates:
        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()
    raise FileNotFoundError(f"No prompt template found for {group_id}, {section}, {subsection}, {doc_type}")
