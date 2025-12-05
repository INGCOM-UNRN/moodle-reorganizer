"""Main reorganizer class coordinating all operations."""

from .text_utils import TextProcessor
from .file_utils import FileHandler
from .xml_utils import XMLProcessor
from .gift_processor import GIFTProcessor
from .xml_processor import MoodleXMLProcessor


class QuestionBackupReorganizer:
    """Main class for handling backup and reorganization of question banks."""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.file_handler = FileHandler()
        self.xml_utils = XMLProcessor(self.text_processor)
        self.gift_processor = GIFTProcessor(self.text_processor, self.file_handler)
        self.xml_processor = MoodleXMLProcessor(self.text_processor, self.file_handler, self.xml_utils)
    
    def export_gift_to_structure(self, input_file, base_output_dir):
        """Export GIFT questions to directory structure."""
        return self.gift_processor.export_to_structure(input_file, base_output_dir)
    
    def collect_gift_from_structure(self, base_input_dir, output_file):
        """Collect GIFT questions from directory structure."""
        return self.gift_processor.collect_from_structure(base_input_dir, output_file)
    
    def export_xml_to_structure(self, input_file, base_output_dir):
        """Export Moodle XML questions to directory structure."""
        return self.xml_processor.export_to_structure(input_file, base_output_dir)
    
    def collect_xml_from_structure(self, base_input_dir, output_file):
        """Collect Moodle XML questions from directory structure."""
        return self.xml_processor.collect_from_structure(base_input_dir, output_file)
