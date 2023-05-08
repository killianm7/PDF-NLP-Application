import pytest
import os
from FileHandler import extract_keywords, extract_paragraphs

# Test data
sample_text = """This is a sample text for testing purposes.

It contains two paragraphs, and it's meant to test the extract_paragraphs function."""

sample_keywords = {'this': 1, 'is': 1, 'a': 1, 'sample': 1, 'text': 1, 'for': 1, 'testing': 1, 'purposes': 1, 'it': 2, 'contains': 1, 'two': 1, 'paragraphs': 1, 'and': 1, 's': 1, 'meant': 1, 'to': 1, 'test': 1, 'the': 1, 'extract': 1, 'paragraphs': 1, 'function': 1}

def test_extract_keywords():
    keywords = extract_keywords(sample_text)
    assert keywords == sample_keywords, f"Expected {sample_keywords}, but got {keywords}"

def test_extract_paragraphs():
    paragraphs = extract_paragraphs(sample_text)
    assert len(paragraphs) == 2, f"Expected 2 paragraphs, but got {len(paragraphs)}"
    assert paragraphs[0] == "This is a sample text for testing purposes.", f"Expected 'This is a sample text for testing purposes.', but got '{paragraphs[0]}'"
    assert paragraphs[1] == "It contains two paragraphs, and it's meant to test the extract_paragraphs function.", f"Expected 'It contains two paragraphs, and it's meant to test the extract_paragraphs function.', but got '{paragraphs[1]}'"