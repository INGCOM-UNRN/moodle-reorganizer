"""GIFT format processor for export and collect operations."""

import os
import re
import sys


class GIFTProcessor:
    """Handles GIFT format export and collection."""
    
    def __init__(self, text_processor, file_handler):
        self.text_processor = text_processor
        self.file_handler = file_handler
    
    def export_to_structure(self, input_file, base_output_dir):
        """Export GIFT questions from monolithic file to directory structure."""
        print(f"Exporting GIFT from: {input_file}")
        print(f"Output directory: {base_output_dir}")
        
        content = self.file_handler.safe_read_preserving_escapes(input_file)
        if content is None:
            print(f"Error: Could not read file '{input_file}'.", file=sys.stderr)
            return False
        
        content = '\n' + content
        blocks = re.split(r'(?=\n(?:^//.*\n)*^::.*::)', content, flags=re.MULTILINE)
        
        current_category = ''
        question_count = 0
        used_filenames = {}
        
        for block in blocks:
            original_block = block.strip()
            if not original_block:
                continue
            
            original_block = self.text_processor.apply_reverse_substitutions(original_block)
            
            category_match = re.search(r'^\$CATEGORY:\s*(.*)', original_block, flags=re.MULTILINE)
            if category_match:
                category_def = category_match.group(1).strip()
                path_parts = [self.file_handler.sanitize_dirname(part) for part in category_def.split('/') 
                             if part.strip() and part != '$course$']
                current_category = os.path.join(*path_parts) if path_parts else ''
                continue
            
            title_match = re.search(r'::(.*?)::', original_block, re.DOTALL)
            if not title_match:
                continue
            
            formatted_block = self._format_gift_block(original_block)
            
            title_text = title_match.group(1).strip()
            category_path_from_title = ''
            actual_title = title_text
            
            if '/' in title_text:
                path_parts = title_text.split('/')
                if len(path_parts) > 1:
                    actual_title = path_parts[-1]
                    category_path_from_title = os.path.join(*[self.file_handler.sanitize_dirname(p) for p in path_parts[:-1]])
            
            final_category_path = category_path_from_title if category_path_from_title else current_category
            
            base_filename = self.file_handler.sanitize_filename(actual_title)
            output_dir = os.path.join(base_output_dir, final_category_path) if final_category_path else base_output_dir
            os.makedirs(output_dir, exist_ok=True)
            
            if output_dir not in used_filenames:
                used_filenames[output_dir] = {}
            
            if base_filename in used_filenames[output_dir]:
                used_filenames[output_dir][base_filename] += 1
                filename = f"{base_filename}_{used_filenames[output_dir][base_filename]}.gift"
            else:
                used_filenames[output_dir][base_filename] = 0
                filename = f"{base_filename}.gift"
            
            output_filepath = os.path.join(output_dir, filename)
            
            if self.file_handler.safe_write_preserving_escapes(output_filepath, formatted_block):
                print(f"  Created: {os.path.relpath(output_filepath, base_output_dir)}")
                question_count += 1
        
        print(f"\n✓ Export completed: {question_count} questions")
        return True
    
    def _format_gift_block(self, block):
        """Format a GIFT block with appropriate line breaks."""
        try:
            title_start_idx = block.index('::')
            title_end_idx = block.index('::', title_start_idx + 2)
            
            title_part = block[title_start_idx : title_end_idx + 2]
            content_after_title = block[title_end_idx + 2:]
            
            # Check if this is a cloze question (has embedded answers in the question text)
            if self._is_cloze_question(content_after_title):
                # For cloze questions, keep everything on the same line after title
                return f"{title_part.strip()}\n{content_after_title.strip()}\n"
            
            # For other question types, find the answer block
            brace_start_idx = block.index('{')
            brace_end_idx = block.rindex('}')
            
            if not (title_end_idx < brace_start_idx < brace_end_idx):
                return block + '\n'
            
            stem_part = block[title_end_idx + 2 : brace_start_idx]
            answer_part = block[brace_start_idx + 1 : brace_end_idx]
            
            return (
                f"{title_part.strip()}\n"
                f"{stem_part.strip()}\n"
                f"{{\n"
                f"{answer_part.strip()}\n"
                f"}}\n"
            )
        except (ValueError, IndexError):
            return block + '\n'
    
    def _is_cloze_question(self, content):
        """Detect if question content is a cloze question (has embedded answers)."""
        # Cloze questions have answer blocks within the question text
        # Look for pattern: text before first brace, then more text after first closing brace
        try:
            first_open = content.index('{')
            first_close = content.index('}', first_open)
            
            # Check if there's more than just whitespace before the first brace
            before_brace = content[:first_open].strip()
            
            # Check if there's more content after the first closing brace (excluding final whitespace)
            after_close = content[first_close + 1:].strip()
            
            # If text exists both before first brace AND after first close,
            # or if there are multiple brace pairs, it's likely a cloze question
            if before_brace and after_close:
                return True
            
            # Also check for multiple brace pairs
            if content.count('{') > 1:
                return True
                
        except (ValueError, IndexError):
            pass
        
        return False
    
    def collect_from_structure(self, base_input_dir, output_file):
        """Collect GIFT questions from directory structure into monolithic file."""
        print(f"Collecting GIFT from: {base_input_dir}")
        print(f"Output file: {output_file}")
        
        if not os.path.isdir(base_input_dir):
            print(f"Error: Directory '{base_input_dir}' does not exist.", file=sys.stderr)
            return False
        
        gift_files = []
        for root, dirs, files in os.walk(base_input_dir):
            for file in files:
                if file.endswith('.gift'):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, base_input_dir)
                    gift_files.append((rel_path, filepath))
        
        if not gift_files:
            print("No .gift files found in the specified directory.")
            return False
        
        gift_files.sort()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as out:
                current_category = None
                question_count = 0
                
                for rel_path, filepath in gift_files:
                    dir_path = os.path.dirname(rel_path)
                    
                    if dir_path != current_category:
                        current_category = dir_path
                        if dir_path:
                            category_path = '/' + dir_path.replace(os.sep, '/')
                            out.write(f"\n$CATEGORY: $course${category_path}\n\n")
                        else:
                            out.write(f"\n$CATEGORY: $course$\n\n")
                    
                    content = self.file_handler.safe_read_preserving_escapes(filepath)
                    if content is not None:
                        content = self.text_processor.protect_backslashes_in_code(content)
                        content = self.text_processor.apply_forward_substitutions(content)
                        
                        out.write(content.strip() + '\n\n')
                        question_count += 1
                        print(f"  Added: {rel_path}")
                
                print(f"\n✓ Collection completed: {question_count} questions in {output_file}")
                return True
        except IOError as e:
            print(f"Error writing output file {output_file}: {e}", file=sys.stderr)
            return False
