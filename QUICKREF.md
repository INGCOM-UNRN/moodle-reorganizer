# Quick Reference

## Installation

```bash
cd reorganizer
uv venv
uv pip install -e .
source .venv/bin/activate
```

## Basic Commands

### Export (Split)

```bash
# GIFT format
reorganizer export gift questions.gift -o output_dir

# XML format  
reorganizer export xml questions.xml -o output_dir
```

### Collect (Merge)

```bash
# GIFT format
reorganizer collect gift input_dir -o output.gift

# XML format
reorganizer collect xml input_dir -o output.xml
```

## Common Workflows

### Backup and Edit
```bash
reorganizer export xml original.xml -o backup
# Edit files in backup/
reorganizer collect xml backup -o edited.xml
```

### Reorganize Categories
```bash
reorganizer export gift all.gift -o temp
# Move directories around
reorganizer collect gift temp -o reorganized.gift
```

### Work with mxviz
```bash
reorganizer export xml questions.xml -o workspace
cd ../mxviz
uv run python -m mxviz ../reorganizer/workspace
# Edit in browser, then:
cd ../reorganizer
reorganizer collect xml workspace -o updated.xml
```

## Python API

```python
from reorganizer import QuestionBackupReorganizer

r = QuestionBackupReorganizer()

# Export
r.export_gift_to_structure("input.gift", "output_dir")
r.export_xml_to_structure("input.xml", "output_dir")

# Collect
r.collect_gift_from_structure("input_dir", "output.gift")
r.collect_xml_from_structure("input_dir", "output.xml")
```

## Module Imports

```python
# Utilities
from reorganizer.text_utils import TextProcessor
from reorganizer.file_utils import FileHandler
from reorganizer.xml_utils import XMLProcessor

# Processors
from reorganizer.gift_processor import GIFTProcessor
from reorganizer.xml_processor import MoodleXMLProcessor
```

## Help

```bash
reorganizer --help
reorganizer export --help
reorganizer collect --help
```

## Documentation

- `README.md` - Overview and features
- `USAGE.md` - Detailed usage guide
- `ARCHITECTURE.md` - Technical design
- `MIGRATION.md` - Migration from old script
- `QUICKREF.md` - This file

## Troubleshooting

**Import Error:**
```bash
source .venv/bin/activate
```

**No files found:**
Check file extensions (.gift or .xml)

**Parse error:**
Check file encoding (UTF-8)

**Special characters wrong:**
This is normal - fullwidth chars protect GIFT syntax
