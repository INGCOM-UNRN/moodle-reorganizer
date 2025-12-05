# Migration Guide

## From `backup_reorganize.py` to Modular `reorganizer`

This document explains the differences between the original monolithic script and the new modular UV project.

## Key Differences

### 1. Structure

**Old (backup_reorganize.py):**
- Single 787-line file
- All functionality in one class
- Direct script execution

**New (reorganizer):**
- Modular package structure
- Separated concerns across 8 modules
- Installable with `uv`
- Command-line tool available system-wide

### 2. Installation

**Old:**
```bash
# Direct execution
python backup_reorganize.py export gift questions.gift -o backup
```

**New:**
```bash
# Install once
cd reorganizer
uv venv
uv pip install -e .

# Use anywhere
reorganizer export gift questions.gift -o backup
```

### 3. Module Organization

| Original Class/Function | New Location | Module |
|------------------------|--------------|--------|
| `QuestionBackupReorganizer.__init__` | `TextProcessor.__init__` | `text_utils.py` |
| Character substitutions | `TextProcessor` | `text_utils.py` |
| File reading/writing | `FileHandler` | `file_utils.py` |
| Filename sanitization | `FileHandler` | `file_utils.py` |
| XML preprocessing | `XMLProcessor` | `xml_utils.py` |
| GIFT export/collect | `GIFTProcessor` | `gift_processor.py` |
| XML export/collect | `MoodleXMLProcessor` | `xml_processor.py` |
| Main coordinator | `QuestionBackupReorganizer` | `reorganizer.py` |
| CLI | `main()` | `cli.py` |

### 4. API Compatibility

The public API remains the same:

```python
# Both old and new support the same interface
from reorganizer import QuestionBackupReorganizer

r = QuestionBackupReorganizer()
r.export_gift_to_structure("input.gift", "output_dir")
r.collect_gift_from_structure("input_dir", "output.gift")
r.export_xml_to_structure("input.xml", "output_dir")
r.collect_xml_from_structure("input_dir", "output.xml")
```

### 5. Functionality Changes

**Preserved:**
- All character protection mechanisms
- Escape sequence handling
- XML preprocessing and cleaning
- Category structure preservation
- Filename collision handling

**Enhanced:**
- Better error messages
- Modular architecture for testing
- Clearer separation of concerns
- Documentation structure

## Command Mapping

| Old Command | New Command |
|------------|-------------|
| `python backup_reorganize.py export gift input.gift -o backup` | `reorganizer export gift input.gift -o backup` |
| `python backup_reorganize.py collect gift backup -o output.gift` | `reorganizer collect gift backup -o output.gift` |
| `python backup_reorganize.py export xml input.xml -o backup` | `reorganizer export xml input.xml -o backup` |
| `python backup_reorganize.py collect xml backup -o output.xml` | `reorganizer collect xml backup -o output.xml` |

## Benefits of New Structure

### 1. Testability
Each module can be tested independently:
```python
# Test text processing in isolation
from reorganizer.text_utils import TextProcessor
tp = TextProcessor()
assert tp.protect_backslashes_in_code('`\\n`') == '`＼n`'
```

### 2. Maintainability
- Clear module boundaries
- Single responsibility per module
- Easy to locate functionality

### 3. Extensibility
Adding new formats is straightforward:
```python
# Create new processor
class QTIProcessor:
    def __init__(self, text_processor, file_handler):
        ...
    
    def export_to_structure(self, input_file, output_dir):
        ...

# Register in reorganizer.py
self.qti_processor = QTIProcessor(self.text_processor, self.file_handler)
```

### 4. Reusability
Utilities can be imported separately:
```python
from reorganizer.file_utils import FileHandler
from reorganizer.text_utils import TextProcessor

# Use in other projects
fh = FileHandler()
safe_name = fh.sanitize_filename("My Question?")
```

### 5. Distribution
- Can be published to PyPI
- Easy installation via `uv` or `pip`
- Version management via `pyproject.toml`

## Migration Steps

### For Users

1. **Install the new tool:**
   ```bash
   cd reorganizer
   uv venv
   uv pip install -e .
   ```

2. **Update scripts:**
   Replace `python backup_reorganize.py` with `reorganizer`

3. **Test:**
   Run with your existing question banks to verify compatibility

### For Developers

1. **Update imports:**
   ```python
   # Old
   from backup_reorganize import QuestionBackupReorganizer
   
   # New
   from reorganizer import QuestionBackupReorganizer
   ```

2. **Use submodules if needed:**
   ```python
   from reorganizer.text_utils import TextProcessor
   from reorganizer.file_utils import FileHandler
   ```

3. **Run tests:**
   ```bash
   uv run pytest
   ```

## Backwards Compatibility

The old `backup_reorganize.py` script remains available in the parent directory for backwards compatibility. However, we recommend migrating to the new modular version for:

- Better maintainability
- Improved testing
- Future enhancements
- Better documentation

## Performance

No performance regression expected. The modular structure adds minimal overhead (class instantiation) which is negligible compared to file I/O operations.

## Support

- **Old script**: Continue to work as-is, but not actively maintained
- **New module**: Active development, bug fixes, and enhancements

## Examples

### Using as Library

**Old:**
```python
import sys
sys.path.append('/path/to/backup_reorganize.py')
from backup_reorganize import QuestionBackupReorganizer
```

**New:**
```python
from reorganizer import QuestionBackupReorganizer
```

### Custom Processing

**Old:**
Modify the single large file.

**New:**
Extend specific modules:
```python
from reorganizer.text_utils import TextProcessor

class CustomTextProcessor(TextProcessor):
    def custom_transformation(self, text):
        # Add custom logic
        return super().apply_forward_substitutions(text)
```

## Timeline

- **Current**: Both versions available
- **Recommended**: Start using modular version for new projects
- **Future**: Deprecate old script after stabilization period

## Questions?

See USAGE.md for detailed usage examples or ARCHITECTURE.md for technical details.
