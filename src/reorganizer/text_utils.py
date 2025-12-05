"""Text processing utilities for handling escape sequences and special characters."""

import re
import sys


class TextProcessor:
    """Handles text processing for escape sequences and special characters."""
    
    def __init__(self):
        self.reverse_substitutions = {
            "⩵": "==", "＝": "=", ";": ";", "＃": "#",
            "｛": "{", "｝": "}", " ": " ", "↵": "",
            "＞": ">", "＜": "<", "［": "[", "］": "]",
        }
        
        self.html_entities_to_fullwidth = {
            "&lt;": "＜",
            "&gt;": "＞",
            "&amp;": "＆",
            "&quot;": "＂",
            "&apos;": "＇",
            "&#39;": "＇",
            "&#34;": "＂",
            "&#60;": "＜",
            "&#62;": "＞",
            "&#38;": "＆",
            "&nbsp;": "　",
        }
    
    def apply_reverse_substitutions(self, text):
        """DISABLED: No longer converts fullwidth to conventional."""
        return text
    
    def replace_html_entities_to_fullwidth(self, text):
        """Replace HTML entities with their fullwidth equivalents."""
        if text is None:
            return None
        
        for entity, fullwidth in self.html_entities_to_fullwidth.items():
            text = text.replace(entity, fullwidth)
        
        return text
    
    def apply_forward_substitutions(self, text):
        """Apply forward substitutions (conventional -> fullwidth/special)."""
        critical_substitutions = {
            "==": "⩵",
            "=": "＝",
            ";": ";",
            "#": "＃",
            "{": "｛",
            "}": "｝",
            ">": "＞",
            "<": "＜",
        }
        
        if "==" in text:
            text = text.replace("==", "⩵")
        
        for conventional, special in critical_substitutions.items():
            if conventional != "==" and conventional != "=":
                text = text.replace(conventional, special)
        
        text = text.replace("=", "＝")
        
        return text
    
    def protect_backslashes_in_code(self, text):
        r"""Replace backslashes (\) with fullwidth (＼) inside code blocks."""
        def replace_in_multiline_code(match):
            code_block = match.group(0)
            return code_block.replace('\\', '＼')
        
        text = re.sub(r'```[^`]*```', replace_in_multiline_code, text, flags=re.DOTALL)
        
        def replace_in_inline_code(match):
            code_inline = match.group(0)
            return code_inline.replace('\\', '＼')
        
        text = re.sub(r'(?<!`)(`[^`\n]+`)(?!`)', replace_in_inline_code, text)
        
        return text
    
    def clean_xml_text(self, text):
        """Clean text to be valid in XML, preserving escape sequences."""
        if text is None:
            return None
        
        cleaned = []
        for char in text:
            code = ord(char)
            if code == 0x09 or code == 0x0A or code == 0x0D or code >= 0x20:
                if code < 0xFFFE:
                    cleaned.append(char)
                else:
                    cleaned.append(' ')
            else:
                cleaned.append(' ')
        
        return ''.join(cleaned)
