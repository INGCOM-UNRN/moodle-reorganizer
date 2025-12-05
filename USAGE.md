# Reorganizer Usage Guide

## Quick Start

### Installation

```bash
# Navigate to the project directory
cd reorganizer

# Create virtual environment and install
uv venv
uv pip install -e .

# Activate the virtual environment
source .venv/bin/activate
```

### Basic Commands

#### Export (Split) Questions

Split a monolithic question bank file into individual files organized by category:

**GIFT Format:**
```bash
reorganizer export gift my_questions.gift -o output_directory
```

**Moodle XML Format:**
```bash
reorganizer export xml my_questions.xml -o output_directory
```

#### Collect (Merge) Questions

Merge individual question files back into a monolithic file:

**GIFT Format:**
```bash
reorganizer collect gift input_directory -o merged_questions.gift
```

**Moodle XML Format:**
```bash
reorganizer collect xml input_directory -o merged_questions.xml
```

## Directory Structure

When exporting questions, the tool creates a directory structure based on question categories:

```
output_directory/
├── Category1/
│   ├── question1.gift
│   ├── question2.gift
│   └── Subcategory1/
│       └── question3.gift
└── Category2/
    ├── question4.gift
    └── question5.gift
```

Each file contains a single question with all its metadata (answers, feedback, tags, etc.).

## Advanced Usage

### Custom Output Directory

```bash
reorganizer export gift questions.gift -o custom/backup/path
```

### Processing Specific Categories

The tool automatically preserves the category structure from your question bank. Categories are defined in:

- **GIFT**: Using `$CATEGORY:` directives
- **XML**: Using category question elements

### Supported Question Types

The tool supports all standard Moodle question types:

- **Multiple Choice**: Single and multiple answer questions
- **True/False**: Boolean questions
- **Short Answer**: Text-based answers with variations
- **Numerical**: Exact values or ranges
- **Essay**: Open-ended text responses
- **Cloze**: Fill-in-the-blank with embedded answers
- **Matching**: Pair items from two lists

See `examples/all_question_types.gift` for comprehensive examples of each type.

### Handling Special Characters

The tool has built-in protection for:

1. **Code blocks** with backticks: Protects backslashes and special characters
2. **GIFT syntax**: Converts special characters to fullwidth equivalents
3. **XML entities**: Handles HTML entities properly in XML format
4. **Escape sequences**: Preserves `\n`, `\0`, `\t`, etc. in code examples
5. **Cloze questions**: Automatically detects and formats embedded answers correctly

## Workflow Examples

### 1. Backup and Edit Workflow

```bash
# Step 1: Export to directory structure
reorganizer export xml original.xml -o backup

# Step 2: Edit individual files in backup/ directory
# (use your favorite editor or the mxviz tool)

# Step 3: Collect back to XML
reorganizer collect xml backup -o edited.xml
```

### 2. Category Reorganization

```bash
# Export questions
reorganizer export gift all_questions.gift -o temp

# Manually reorganize directories
# mv temp/OldCategory/* temp/NewCategory/

# Collect with new structure
reorganizer collect gift temp -o reorganized.gift
```

### 3. Format Conversion (GIFT ↔ XML)

Note: Direct format conversion requires intermediate steps:

```bash
# Export from GIFT
reorganizer export gift questions.gift -o temp

# Import to Moodle, export as XML
# (manual step in Moodle interface)

# Or vice versa
```

## Troubleshooting

### Issue: "No .gift files found"

**Solution**: Ensure you're pointing to the correct directory and files have `.gift` extension.

### Issue: "Could not parse XML"

**Solution**: The tool automatically cleans invalid XML characters. If this persists:
1. Check the input file encoding (should be UTF-8)
2. Look for null bytes or control characters in the original file
3. The tool will provide line numbers for parsing errors

### Issue: Special characters appear wrong

**Solution**: The tool uses fullwidth characters to protect GIFT syntax. These are intentional and will be processed correctly by Moodle.

## Integration with mxviz

The reorganizer tool works seamlessly with mxviz for visual editing:

```bash
# Export questions to directory
reorganizer export xml questions.xml -o questions_dir

# Launch mxviz to edit
cd ../mxviz
uv run python -m mxviz ../questions_dir

# After editing, collect back
cd ../reorganizer
reorganizer collect xml ../questions_dir -o questions_updated.xml
```

## Performance Tips

- **Large files**: The tool handles large question banks efficiently
- **Category structure**: Deep category hierarchies are fully supported
- **File naming**: Duplicate question names are automatically handled with numeric suffixes

## Best Practices

1. **Version Control**: Use git to track changes to individual question files
2. **Backup First**: Always keep a backup before reorganizing
3. **Test Import**: Test the collected file in Moodle before replacing production banks
4. **Consistent Naming**: Use clear, descriptive names for questions
5. **Category Planning**: Plan your category structure before reorganizing
