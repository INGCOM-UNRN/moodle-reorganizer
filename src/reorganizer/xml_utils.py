"""XML processing utilities for Moodle XML format."""

import re
import sys
import xml.etree.ElementTree as ET


class XMLProcessor:
    """Handles XML-specific processing operations."""
    
    def __init__(self, text_processor):
        self.text_processor = text_processor
    
    def preprocess_xml_file(self, input_file):
        """Pre-process XML file to clean invalid characters before parsing."""
        try:
            with open(input_file, 'rb') as f:
                content = f.read()
            
            if b'\x00' in content:
                print("  ⚠ Warning: File contains null bytes (0x00), cleaning...", file=sys.stderr)
                content = content.replace(b'\x00', b' ')
            
            try:
                xml_string = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    xml_string = content.decode('latin-1')
                    print("  ⚠ Warning: File is not UTF-8, using latin-1", file=sys.stderr)
                except:
                    print("  ✗ Error: Could not decode file", file=sys.stderr)
                    return None
            
            cleaned_chars = []
            invalid_count = 0
            
            for char in xml_string:
                code = ord(char)
                if (code == 0x09 or code == 0x0A or code == 0x0D or 
                    (code >= 0x20 and code <= 0xD7FF) or
                    (code >= 0xE000 and code <= 0xFFFD)):
                    cleaned_chars.append(char)
                else:
                    cleaned_chars.append(' ')
                    invalid_count += 1
            
            if invalid_count > 0:
                print(f"  ⚠ Warning: Cleaned {invalid_count} invalid XML characters", file=sys.stderr)
            
            return ''.join(cleaned_chars)
            
        except Exception as e:
            print(f"  ✗ Error pre-processing XML: {e}", file=sys.stderr)
            return None
    
    def ensure_text_elements_complete(self, xml_string):
        """Ensure all <text/> elements are complete and content is in CDATA."""
        xml_string = re.sub(r'<text\s*/>', '<text></text>', xml_string)
        
        def wrap_text_content(match):
            opening = match.group(1)
            content = match.group(2)
            closing = match.group(3)
            
            if not content or content.strip() == '':
                return f'{opening}{closing}'
            
            content_processed = self.text_processor.replace_html_entities_to_fullwidth(content)
            
            if '<![CDATA[' in content:
                cdata_match = re.search(r'<!\[CDATA\[(.*?)\]\]>', content, re.DOTALL)
                if cdata_match:
                    cdata_content = cdata_match.group(1)
                    cdata_processed = self.text_processor.replace_html_entities_to_fullwidth(cdata_content)
                    return f'{opening}<![CDATA[{cdata_processed}]]>{closing}'
                return match.group(0)
            
            return f'{opening}<![CDATA[{content_processed}]]>{closing}'
        
        xml_string = re.sub(
            r'(<text(?:\s+[^>]*)?>)(.*?)(</text>)',
            wrap_text_content,
            xml_string,
            flags=re.DOTALL
        )
        
        return xml_string
    
    def process_xml_element_text(self, element):
        """Process XML element recursively, replacing HTML entities in <text> elements."""
        if element.tag == 'text' and element.text:
            element.text = self.text_processor.replace_html_entities_to_fullwidth(element.text)
        
        for child in element:
            self.process_xml_element_text(child)
