# tests/test_utils.py
import pytest
from app.utils import extract_json

def test_extract_json_valid():
    text = """
    Sure, here is your quiz:
    [
        {"question": "What is OOP?", "answer": "Object Oriented Programming", "options": ["OOP", "POP"]}
    ]
    Extra explanation...
    """
    result = extract_json(text)
    assert result.startswith("[")
    assert result.endswith("]")
    assert '"question": "What is OOP?"' in result

def test_extract_json_multiline():
    text = "Random stuff\n[\n{\"q\":1}\n]\nMore stuff"
    result = extract_json(text)
    assert result == '[\n{"q":1}\n]'

def test_extract_json_invalid():
    text = "No JSON here!"
    with pytest.raises(ValueError, match="No JSON found in response"):
        extract_json(text)
