# Referencia Rápida

## Instalación

```bash
cd reorganizer
uv venv
uv pip install -e .
source .venv/bin/activate
```

## Comandos Básicos

### Exportar (Dividir)

```bash
# Formato GIFT
reorganizer export gift preguntas.gift -o dir_salida

# Formato XML  
reorganizer export xml preguntas.xml -o dir_salida
```

### Recolectar (Fusionar)

```bash
# Formato GIFT
reorganizer collect gift dir_entrada -o salida.gift

# Formato XML
reorganizer collect xml dir_entrada -o salida.xml
```

## Flujos de Trabajo Comunes

### Respaldar y Editar
```bash
reorganizer export xml original.xml -o respaldo
# Editar archivos en respaldo/
reorganizer collect xml respaldo -o editado.xml
```

### Reorganizar Categorías
```bash
reorganizer export gift todo.gift -o temp
# Mover directorios
reorganizer collect gift temp -o reorganizado.gift
```

### Trabajar con mxviz
```bash
reorganizer export xml preguntas.xml -o workspace
cd ../mxviz
uv run python -m mxviz ../reorganizer/workspace
# Editar en navegador, luego:
cd ../reorganizer
reorganizer collect xml workspace -o actualizado.xml
```

## API Python

```python
from reorganizer import QuestionBackupReorganizer

r = QuestionBackupReorganizer()

# Exportar
r.export_gift_to_structure("entrada.gift", "dir_salida")
r.export_xml_to_structure("entrada.xml", "dir_salida")

# Recolectar
r.collect_gift_from_structure("dir_entrada", "salida.gift")
r.collect_xml_from_structure("dir_entrada", "salida.xml")
```

## Importar Módulos

```python
# Utilidades
from reorganizer.text_utils import TextProcessor
from reorganizer.file_utils import FileHandler
from reorganizer.xml_utils import XMLProcessor

# Procesadores
from reorganizer.gift_processor import GIFTProcessor
from reorganizer.xml_processor import MoodleXMLProcessor
```

## Ayuda

```bash
reorganizer --help
reorganizer export --help
reorganizer collect --help
```

## Documentación

- `README.md` - Visión general y características
- `USAGE.md` / `USAGE.es.md` - Guía detallada de uso
- `ARCHITECTURE.md` / `ARCHITECTURE.es.md` - Diseño técnico
- `MIGRATION.md` / `MIGRATION.es.md` - Migración desde script antiguo
- `QUICKREF.md` / `QUICKREF.es.md` - Este archivo
- `CHANGELOG.md` / `CHANGELOG.es.md` - Historial de cambios

## Solución de Problemas

**Error de Importación:**
```bash
source .venv/bin/activate
```

**No se encontraron archivos:**
Verifica las extensiones de archivo (.gift o .xml)

**Error de parseo:**
Verifica la codificación del archivo (UTF-8)

**Caracteres especiales incorrectos:**
Es normal - caracteres fullwidth protegen sintaxis GIFT
