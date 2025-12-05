# Changelog

All notable changes to the Question Bank Reorganizer project will be documented in this file.

## [Unreleased]

### Improved
- Enhanced GIFT question formatting to properly handle cloze questions
- Added automatic detection of cloze questions (questions with embedded answers)
- Improved support for multiple question types: cloze, matching, numerical, shortanswer, and essay

## [1.0.0] - 2025-11-12

### Added
- Initial modular release
- Separated monolithic `backup_reorganize.py` into 8 focused modules
- Added comprehensive documentation (README, USAGE, ARCHITECTURE, MIGRATION, QUICKREF)
- Added pytest-based test suite
- Added UV project configuration with pyproject.toml
- Added command-line tool via entry point
- Added examples directory with usage scripts
- Added .gitignore for Python project

### Module Structure
- `cli.py` - Command-line interface and argument parsing
- `reorganizer.py` - Main coordinator class
- `text_utils.py` - Text processing utilities
- `file_utils.py` - File handling utilities  
- `xml_utils.py` - XML processing utilities
- `gift_processor.py` - GIFT format export/collect operations
- `xml_processor.py` - Moodle XML format export/collect operations

### Features
- Export GIFT and Moodle XML to directory structures
- Collect individual files back to monolithic formats
- Preserve escape sequences in code blocks
- Protect GIFT special characters with fullwidth equivalents
- Handle HTML entities in XML
- Clean invalid XML characters automatically
- Sanitize filenames and directory names
- Handle filename collisions with numeric suffixes
- Category-based organization

### Documentation
- README.md - Project overview
- USAGE.md - Detailed usage guide with examples
- ARCHITECTURE.md - Technical design documentation
- MIGRATION.md - Migration guide from old script
- QUICKREF.md - Quick reference for common commands
- CHANGELOG.md - This file

### Testing
- 6 unit tests covering core functionality
- Tests for text processing
- Tests for file handling
- Tests for HTML entity conversion
- Tests for backslash protection
- All tests passing

### Compatibility
- Python 3.10+
- Maintains API compatibility with original script
- CLI command structure unchanged (just different invocation)

## [Pre-1.0.0] - Original Script

### Features (from backup_reorganize.py)
- GIFT and Moodle XML export/collect
- Category-based organization
- Special character handling
- Escape sequence preservation
- XML preprocessing
- Filename sanitization
