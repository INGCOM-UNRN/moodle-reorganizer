# Architecture Documentation

## Overview

The Question Bank Reorganizer is a modular Python application designed to handle backup and reorganization of question banks in GIFT and Moodle XML formats. The architecture emphasizes separation of concerns, testability, and maintainability.

## Project Structure

```
reorganizer/
├── src/
│   └── reorganizer/
│       ├── __init__.py           # Package initialization and exports
│       ├── cli.py                # Command-line interface
│       ├── reorganizer.py        # Main coordinator class
│       ├── text_utils.py         # Text processing utilities
│       ├── file_utils.py         # File handling utilities
│       ├── xml_utils.py          # XML processing utilities
│       ├── gift_processor.py     # GIFT format processor
│       └── xml_processor.py      # Moodle XML processor
├── pyproject.toml                # Project configuration
├── README.md                     # Main documentation
├── USAGE.md                      # Usage guide
└── ARCHITECTURE.md               # This file
```

## Module Design

### 1. CLI Module (`cli.py`)

**Purpose**: Command-line interface and argument parsing

**Responsibilities**:
- Parse command-line arguments
- Validate user input
- Route commands to appropriate handlers
- Handle exit codes

**Key Functions**:
- `main()`: Entry point for the CLI

### 2. Reorganizer Module (`reorganizer.py`)

**Purpose**: Main coordinator class that orchestrates operations

**Responsibilities**:
- Initialize all utility classes
- Provide high-level API for export/collect operations
- Coordinate between different processors

**Key Class**: `QuestionBackupReorganizer`

**Methods**:
- `export_gift_to_structure()`
- `collect_gift_from_structure()`
- `export_xml_to_structure()`
- `collect_xml_from_structure()`

### 3. Text Utilities Module (`text_utils.py`)

**Purpose**: Handle text processing and character transformations

**Responsibilities**:
- Fullwidth character conversions
- HTML entity handling
- Escape sequence preservation
- Code block protection

**Key Class**: `TextProcessor`

**Important Methods**:
- `apply_forward_substitutions()`: Convert special chars to fullwidth
- `replace_html_entities_to_fullwidth()`: HTML entity conversion
- `protect_backslashes_in_code()`: Protect backslashes in code blocks
- `clean_xml_text()`: Clean text for XML validity

### 4. File Utilities Module (`file_utils.py`)

**Purpose**: Safe file operations

**Responsibilities**:
- File reading with escape sequence preservation
- File writing with proper encoding
- Filename sanitization
- Directory name sanitization

**Key Class**: `FileHandler`

**Static Methods**:
- `safe_read_preserving_escapes()`: Read files safely
- `safe_write_preserving_escapes()`: Write files safely
- `sanitize_filename()`: Clean filenames
- `sanitize_dirname()`: Clean directory names

### 5. XML Utilities Module (`xml_utils.py`)

**Purpose**: XML-specific processing operations

**Responsibilities**:
- XML preprocessing (clean invalid characters)
- CDATA wrapping
- Element processing
- HTML entity handling in XML context

**Key Class**: `XMLProcessor`

**Methods**:
- `preprocess_xml_file()`: Clean XML before parsing
- `ensure_text_elements_complete()`: Ensure proper CDATA wrapping
- `process_xml_element_text()`: Recursively process elements

### 6. GIFT Processor Module (`gift_processor.py`)

**Purpose**: Handle GIFT format operations

**Responsibilities**:
- Parse GIFT files
- Extract categories and questions
- Format GIFT output
- Manage directory structure for GIFT

**Key Class**: `GIFTProcessor`

**Methods**:
- `export_to_structure()`: Export GIFT to directories
- `collect_from_structure()`: Collect GIFT from directories
- `_format_gift_block()`: Format individual questions

### 7. XML Processor Module (`xml_processor.py`)

**Purpose**: Handle Moodle XML format operations

**Responsibilities**:
- Parse Moodle XML files
- Extract categories and questions
- Build XML output
- Manage directory structure for XML

**Key Class**: `MoodleXMLProcessor`

**Methods**:
- `export_to_structure()`: Export XML to directories
- `collect_from_structure()`: Collect XML from directories

## Data Flow

### Export Operation

```
Input File
    ↓
[Preprocessor] → Clean invalid characters
    ↓
[Parser] → Split into questions/categories
    ↓
[Text Processor] → Apply substitutions
    ↓
[File Handler] → Write individual files
    ↓
Directory Structure
```

### Collect Operation

```
Directory Structure
    ↓
[File Scanner] → Find all question files
    ↓
[File Handler] → Read individual files
    ↓
[Text Processor] → Apply protections
    ↓
[Format Builder] → Construct output format
    ↓
Output File
```

## Design Patterns

### 1. Composition

The `QuestionBackupReorganizer` class composes multiple utility classes rather than inheriting from them. This provides flexibility and testability.

### 2. Strategy Pattern

Different processors (`GIFTProcessor`, `MoodleXMLProcessor`) implement similar operations for different formats, allowing easy addition of new formats.

### 3. Single Responsibility Principle

Each module has a clear, single responsibility:
- Text processing
- File handling
- XML operations
- Format-specific processing

### 4. Dependency Injection

Utility classes are injected into processors, making testing and mocking easier.

## Character Encoding Strategy

### Problem

Question banks contain:
- Code examples with escape sequences (`\n`, `\0`)
- GIFT syntax characters (`{`, `}`, `=`, `#`)
- HTML entities in XML
- Markdown formatting

### Solution

1. **Fullwidth Conversion**: Convert GIFT special characters to fullwidth equivalents
2. **Code Protection**: Protect backslashes in code blocks
3. **HTML Entity Handling**: Convert entities to fullwidth in XML
4. **CDATA Wrapping**: Wrap XML text content in CDATA sections

### Character Mappings

```python
"=" → "＝"   # Fullwidth equals
"{" → "｛"   # Fullwidth left brace
"}" → "｝"   # Fullwidth right brace
"&lt;" → "＜" # HTML entity to fullwidth
```

## Error Handling

### Strategy

1. **Validation at Entry**: CLI validates inputs early
2. **Graceful Degradation**: Continue processing valid questions even if some fail
3. **Detailed Logging**: Provide clear error messages with context
4. **Return Codes**: Use boolean returns for success/failure

### Error Types

- **File Errors**: Missing files, permission issues
- **Parse Errors**: Invalid XML, malformed GIFT
- **Encoding Errors**: UTF-8 issues, invalid characters

## Testing Strategy

### Unit Tests

Each utility class should have unit tests:
- `TextProcessor`: Test character conversions
- `FileHandler`: Test sanitization functions
- `XMLProcessor`: Test XML processing

### Integration Tests

Test full workflows:
- Export → Collect roundtrip
- Category preservation
- Special character handling

### Test Data

Include test files with:
- Various question types
- Special characters
- Code blocks
- Deep category hierarchies

## Extension Points

### Adding New Formats

1. Create new processor class (e.g., `QTIProcessor`)
2. Implement `export_to_structure()` and `collect_from_structure()`
3. Register in `QuestionBackupReorganizer`
4. Add CLI option

### Adding New Text Transformations

1. Add method to `TextProcessor`
2. Call from appropriate processor
3. Document character mappings

## Performance Considerations

### Memory

- Stream processing for large files
- Don't load entire file into memory when possible
- Process questions incrementally

### I/O

- Batch file operations
- Minimize disk seeks
- Use efficient encoding detection

## Security Considerations

### File Safety

- Sanitize all filenames
- Validate directory paths
- Prevent directory traversal

### Character Safety

- Remove null bytes from XML
- Clean control characters
- Validate UTF-8 encoding

## Future Enhancements

1. **Parallel Processing**: Process multiple files concurrently
2. **Progress Bars**: Visual feedback for large operations
3. **Validation**: Validate question structure before processing
4. **Diff Tool**: Compare question banks
5. **Merge Tool**: Merge multiple question banks
6. **Export Formats**: Add JSON, QTI support
