"""Moodle XML format processor for export and collect operations."""

import os
import sys
import xml.etree.ElementTree as ET


class MoodleXMLProcessor:
    """Handles Moodle XML format export and collection."""
    
    def __init__(self, text_processor, file_handler, xml_utils):
        self.text_processor = text_processor
        self.file_handler = file_handler
        self.xml_utils = xml_utils
    
    def export_to_structure(self, input_file, base_output_dir):
        """Export Moodle XML questions to directory structure."""
        print(f"Exporting Moodle XML from: {input_file}")
        print(f"Output directory: {base_output_dir}")
        
        try:
            cleaned_xml = self.xml_utils.preprocess_xml_file(input_file)
            
            if cleaned_xml is None:
                print(f"Error: Could not read file '{input_file}'.", file=sys.stderr)
                return False
            
            root = ET.fromstring(cleaned_xml)
        except ET.ParseError as e:
            print(f"Error: Could not parse XML: {e}", file=sys.stderr)
            print(f"Suggestion: File may contain invalid XML characters", file=sys.stderr)
            return False
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.", file=sys.stderr)
            return False
        
        current_category = ''
        question_count = 0
        used_filenames = {}
        
        for question in root.findall('question'):
            qtype = question.get('type')
            
            if qtype == 'category':
                category_elem = question.find('category/text')
                if category_elem is not None and category_elem.text:
                    category_path = category_elem.text
                    path_parts = [self.file_handler.sanitize_dirname(part) for part in category_path.split('/') 
                                 if part.strip() and part != '$course$']
                    current_category = os.path.join(*path_parts) if path_parts else ''
                continue
            
            name_elem = question.find('name/text')
            if name_elem is None or not name_elem.text:
                continue
            
            question_name = name_elem.text.strip()
            base_filename = self.file_handler.sanitize_filename(question_name)
            
            output_dir = os.path.join(base_output_dir, current_category) if current_category else base_output_dir
            os.makedirs(output_dir, exist_ok=True)
            
            if output_dir not in used_filenames:
                used_filenames[output_dir] = {}
            
            if base_filename in used_filenames[output_dir]:
                used_filenames[output_dir][base_filename] += 1
                filename = f"{base_filename}_{used_filenames[output_dir][base_filename]}.xml"
            else:
                used_filenames[output_dir][base_filename] = 0
                filename = f"{base_filename}.xml"
            
            output_filepath = os.path.join(output_dir, filename)
            
            try:
                quiz_root = ET.Element('quiz')
                self.xml_utils.process_xml_element_text(question)
                quiz_root.append(question)
                
                xml_string = ET.tostring(quiz_root, encoding='unicode', method='xml')
                xml_string = self.xml_utils.ensure_text_elements_complete(xml_string)
                xml_final = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'
                
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write(xml_final)
                
                print(f"  Created: {os.path.relpath(output_filepath, base_output_dir)}")
                question_count += 1
            except IOError as e:
                print(f"  Error writing {output_filepath}: {e}", file=sys.stderr)
        
        print(f"\n✓ Export completed: {question_count} questions")
        return True
    
    def collect_from_structure(self, base_input_dir, output_file):
        """Collect Moodle XML questions from directory structure."""
        print(f"Collecting Moodle XML from: {base_input_dir}")
        print(f"Output file: {output_file}")
        
        if not os.path.isdir(base_input_dir):
            print(f"Error: Directory '{base_input_dir}' does not exist.", file=sys.stderr)
            return False
        
        xml_files = []
        for root, dirs, files in os.walk(base_input_dir):
            # Filter out hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            for file in files:
                # Filter out hidden files and only include .xml files
                if file.endswith('.xml') and not file.startswith('.'):
                    filepath = os.path.join(root, file)
                    rel_path = os.path.relpath(filepath, base_input_dir)
                    xml_files.append((rel_path, filepath))
        
        if not xml_files:
            print("No .xml files found in the specified directory.")
            return False
        
        xml_files.sort()
        
        quiz_root = ET.Element('quiz')
        current_category = None
        question_count = 0
        
        for rel_path, filepath in xml_files:
            dir_path = os.path.dirname(rel_path)
            
            if dir_path != current_category:
                current_category = dir_path
                category_elem = ET.SubElement(quiz_root, 'question', type='category')
                category_text = ET.SubElement(ET.SubElement(category_elem, 'category'), 'text')
                
                if dir_path:
                    category_path = '$course$/' + dir_path.replace(os.sep, '/')
                else:
                    category_path = '$course$'
                
                category_text.text = category_path
            
            try:
                tree = ET.parse(filepath)
                question_root = tree.getroot()
                
                for question in question_root.findall('question'):
                    self.xml_utils.process_xml_element_text(question)
                    quiz_root.append(question)
                    question_count += 1
                    print(f"  Added: {rel_path}")
            except ET.ParseError as e:
                print(f"  Error parsing {filepath}: {e}", file=sys.stderr)
            except Exception as e:
                print(f"  Error reading {filepath}: {e}", file=sys.stderr)
        
        xml_string = ET.tostring(quiz_root, encoding='unicode', method='xml')
        xml_string = self.xml_utils.ensure_text_elements_complete(xml_string)
        xml_final = f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_string}'
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_final)
            
            print(f"\n✓ Collection completed: {question_count} questions in {output_file}")
            return True
        except IOError as e:
            print(f"Error writing output file {output_file}: {e}", file=sys.stderr)
            return False
