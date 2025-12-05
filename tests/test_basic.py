"""Basic tests for reorganizer package."""

import pytest
from reorganizer import QuestionBackupReorganizer
from reorganizer.text_utils import TextProcessor
from reorganizer.file_utils import FileHandler


def test_package_import():
    """Test that the package imports correctly."""
    assert QuestionBackupReorganizer is not None


def test_reorganizer_instantiation():
    """Test that QuestionBackupReorganizer can be instantiated."""
    r = QuestionBackupReorganizer()
    assert r is not None
    assert r.text_processor is not None
    assert r.file_handler is not None


def test_text_processor_forward_substitutions():
    """Test forward substitutions."""
    tp = TextProcessor()
    
    # Test equals conversion
    result = tp.apply_forward_substitutions("a=b")
    assert "＝" in result
    
    # Test braces conversion
    result = tp.apply_forward_substitutions("{answer}")
    assert "｛" in result
    assert "｝" in result


def test_text_processor_backslash_protection():
    """Test backslash protection in code blocks."""
    tp = TextProcessor()
    
    # Test inline code
    result = tp.protect_backslashes_in_code("Use `\\n` for newline")
    assert "＼" in result
    
    # Test multiline code
    result = tp.protect_backslashes_in_code("```\n\\n\\t\n```")
    assert "＼" in result


def test_file_handler_sanitization():
    """Test filename sanitization."""
    fh = FileHandler()
    
    # Test special characters removal
    result = fh.sanitize_filename("Question: What?")
    assert ":" not in result
    assert "?" not in result
    
    # Test directory sanitization
    result = fh.sanitize_dirname("Category / Subcategory")
    assert "/" not in result


def test_html_entity_to_fullwidth():
    """Test HTML entity conversion."""
    tp = TextProcessor()
    
    result = tp.replace_html_entities_to_fullwidth("&lt;html&gt;")
    assert "＜" in result
    assert "＞" in result
    assert "&lt;" not in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
