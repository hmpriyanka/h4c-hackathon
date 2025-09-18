import re
def extract_json(text:str)->str:
    match=re.search(r"\[.*\]",text,re.DOTALL)
    if not match:
        raise ValueError("No JSON found in response")
    return match.group(0)