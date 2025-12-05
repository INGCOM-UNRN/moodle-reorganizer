"""Convert Markdown format questions to HTML for Moodle compatibility."""

import re


def convert_markdown_to_html(text):
    """
    Convert markdown formatting to HTML.
    
    Handles:
    - Code blocks with triple backticks
    - Inline code with single backticks
    - Bold text with **
    - Lists and paragraphs
    """
    if not text:
        return text
    
    # Convert code blocks (```lang\ncode\n```)
    def replace_code_block(match):
        lang = match.group(1) if match.group(1) else ''
        code = match.group(2)
        return f'<pre><code>{code}</code></pre>'
    
    text = re.sub(r'```(\w*)\n(.*?)\n```', replace_code_block, text, flags=re.DOTALL)
    
    # Convert inline code (`code`)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Convert bold (**text**)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # Convert italic (*text*)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # Wrap paragraphs (lines separated by blank lines)
    # Split by double newlines
    paragraphs = text.split('\n\n')
    result = []
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        # Skip if already wrapped in HTML tags
        if para.startswith('<pre>') or para.startswith('<ul>') or para.startswith('<ol>'):
            result.append(para)
        elif para.startswith('<p>'):
            result.append(para)
        else:
            # Wrap in paragraph tags
            result.append(f'<p>{para}</p>')
    
    return '\n'.join(result)


def needs_conversion(text):
    """Check if text contains markdown that needs conversion."""
    if not text:
        return False
    
    # Check for markdown patterns
    patterns = [
        r'```',           # Code blocks
        r'`[^`]+`',      # Inline code
        r'\*\*[^*]+\*\*', # Bold
    ]
    
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    
    return False
