# Question Bank Reorganizer

A modular Python tool for backing up and reorganizing question banks in GIFT or Moodle XML format.

## Features

- **Export**: Convert monolithic question bank files into organized directory structures based on categories
- **Collect**: Reconstruct monolithic files from organized directory structures
- **Format Support**: Works with both GIFT and Moodle XML formats
- **Question Types**: Supports multiple choice, cloze, matching, numerical, shortanswer, and essay questions
- **Safe Processing**: Preserves escape sequences, special characters, and code blocks
- **Category Management**: Automatically handles category hierarchies

## Installation

Using UV:

```bash
uv pip install -e .
```

## Usage

### Export Questions to Directory Structure

Export GIFT format:
```bash
reorganizer export gift full.gift -o gift_backup
```

Export Moodle XML format:
```bash
reorganizer export xml questions.xml -o xml_backup
```

### Collect Questions from Directory Structure

Collect GIFT format:
```bash
reorganizer collect gift gift_backup -o full_recompiled.gift
```

Collect Moodle XML format:
```bash
reorganizer collect xml xml_backup -o questions_recompiled.xml
```

## Project Structure

The project is modularized into several components:

- `cli.py` - Command-line interface
- `reorganizer.py` - Main coordinator class
- `text_utils.py` - Text processing utilities (escape sequences, special characters)
- `file_utils.py` - File handling utilities (safe read/write, sanitization)
- `xml_utils.py` - XML processing utilities (CDATA, HTML entities)
- `gift_processor.py` - GIFT format export/collect operations
- `xml_processor.py` - Moodle XML format export/collect operations

## Special Character Handling

The tool includes robust handling for:

- **Escape sequences** in code blocks (e.g., `\n`, `\0`, `\\`)
- **Fullwidth characters** for protecting GIFT syntax
- **HTML entities** converted to fullwidth equivalents
- **CDATA sections** for XML safety
- **Markdown code blocks** with backslash protection

## Development

Run tests (if available):
```bash
uv run pytest
```

Format code:
```bash
uv run black src/
```

## License

This project is provided as-is for educational purposes.
