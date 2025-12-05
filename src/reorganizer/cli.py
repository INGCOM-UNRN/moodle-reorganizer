"""Command-line interface for the question backup reorganizer."""

import sys
import argparse
from .reorganizer import QuestionBackupReorganizer


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Backup and reorganization of question banks in GIFT or Moodle XML format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Usage examples:

  # Export GIFT to directory structure
  %(prog)s export gift full.gift -o gift_backup

  # Collect GIFT from directories to single file
  %(prog)s collect gift gift_backup -o full_recompiled.gift

  # Export Moodle XML to directory structure
  %(prog)s export xml questions.xml -o xml_backup

  # Collect Moodle XML from directories
  %(prog)s collect xml xml_backup -o questions_recompiled.xml
        """
    )
    
    subparsers = parser.add_subparsers(dest='action', help='Action to perform', required=True)
    
    # Subcommand: export
    export_parser = subparsers.add_parser('export', help='Export questions to directory structure')
    export_parser.add_argument('format', choices=['gift', 'xml'], help='Input file format')
    export_parser.add_argument('input', help='Input file (GIFT or XML)')
    export_parser.add_argument('-o', '--output', default='backup', help='Output directory (default: backup)')
    
    # Subcommand: collect
    collect_parser = subparsers.add_parser('collect', help='Collect questions from directory structure')
    collect_parser.add_argument('format', choices=['gift', 'xml'], help='Output file format')
    collect_parser.add_argument('input', help='Input directory with file structure')
    collect_parser.add_argument('-o', '--output', help='Output file', required=True)
    
    args = parser.parse_args()
    
    reorganizer = QuestionBackupReorganizer()
    
    if args.action == 'export':
        if args.format == 'gift':
            success = reorganizer.export_gift_to_structure(args.input, args.output)
        else:  # xml
            success = reorganizer.export_xml_to_structure(args.input, args.output)
    
    elif args.action == 'collect':
        if args.format == 'gift':
            success = reorganizer.collect_gift_from_structure(args.input, args.output)
        else:  # xml
            success = reorganizer.collect_xml_from_structure(args.input, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
