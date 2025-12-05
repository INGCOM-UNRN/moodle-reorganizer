# Guía de Migración

## De `backup_reorganize.py` a `reorganizer` Modular

Este documento explica las diferencias entre el script monolítico original y el nuevo proyecto UV modular.

## Diferencias Clave

### 1. Estructura

**Antiguo (backup_reorganize.py):**
- Archivo único de 787 líneas
- Toda la funcionalidad en una clase
- Ejecución directa de script

**Nuevo (reorganizer):**
- Estructura de paquete modular
- Responsabilidades separadas en 8 módulos
- Instalable con `uv`
- Herramienta de línea de comandos disponible en todo el sistema

### 2. Instalación

**Antiguo:**
```bash
# Ejecución directa
python backup_reorganize.py export gift preguntas.gift -o respaldo
```

**Nuevo:**
```bash
# Instalar una vez
cd reorganizer
uv venv
uv pip install -e .

# Usar en cualquier lugar
reorganizer export gift preguntas.gift -o respaldo
```

### 3. Organización de Módulos

| Clase/Función Original | Nueva Ubicación | Módulo |
|------------------------|----------------|--------|
| `QuestionBackupReorganizer.__init__` | `TextProcessor.__init__` | `text_utils.py` |
| Sustituciones de caracteres | `TextProcessor` | `text_utils.py` |
| Lectura/escritura de archivos | `FileHandler` | `file_utils.py` |
| Sanitización de nombres | `FileHandler` | `file_utils.py` |
| Preprocesamiento XML | `XMLProcessor` | `xml_utils.py` |
| Exportar/recolectar GIFT | `GIFTProcessor` | `gift_processor.py` |
| Exportar/recolectar XML | `MoodleXMLProcessor` | `xml_processor.py` |
| Coordinador principal | `QuestionBackupReorganizer` | `reorganizer.py` |
| CLI | `main()` | `cli.py` |

### 4. Compatibilidad de API

La API pública permanece igual:

```python
# Tanto antiguo como nuevo soportan la misma interfaz
from reorganizer import QuestionBackupReorganizer

r = QuestionBackupReorganizer()
r.export_gift_to_structure("entrada.gift", "dir_salida")
r.collect_gift_from_structure("dir_entrada", "salida.gift")
r.export_xml_to_structure("entrada.xml", "dir_salida")
r.collect_xml_from_structure("dir_entrada", "salida.xml")
```

### 5. Cambios de Funcionalidad

**Preservado:**
- Todos los mecanismos de protección de caracteres
- Manejo de secuencias de escape
- Preprocesamiento y limpieza XML
- Preservación de estructura de categorías
- Manejo de colisiones de nombres de archivo

**Mejorado:**
- Mejores mensajes de error
- Arquitectura modular para testing
- Separación más clara de responsabilidades
- Estructura de documentación

## Mapeo de Comandos

| Comando Antiguo | Comando Nuevo |
|----------------|---------------|
| `python backup_reorganize.py export gift entrada.gift -o respaldo` | `reorganizer export gift entrada.gift -o respaldo` |
| `python backup_reorganize.py collect gift respaldo -o salida.gift` | `reorganizer collect gift respaldo -o salida.gift` |
| `python backup_reorganize.py export xml entrada.xml -o respaldo` | `reorganizer export xml entrada.xml -o respaldo` |
| `python backup_reorganize.py collect xml respaldo -o salida.xml` | `reorganizer collect xml respaldo -o salida.xml` |

## Beneficios de la Nueva Estructura

### 1. Testabilidad
Cada módulo puede ser testeado independientemente:
```python
# Probar procesamiento de texto en aislamiento
from reorganizer.text_utils import TextProcessor
tp = TextProcessor()
assert tp.protect_backslashes_in_code('`\\n`') == '`＼n`'
```

### 2. Mantenibilidad
- Límites claros de módulos
- Responsabilidad única por módulo
- Fácil de localizar funcionalidad

### 3. Extensibilidad
Agregar nuevos formatos es sencillo:
```python
# Crear nuevo procesador
class QTIProcessor:
    def __init__(self, text_processor, file_handler):
        ...
    
    def export_to_structure(self, input_file, output_dir):
        ...

# Registrar en reorganizer.py
self.qti_processor = QTIProcessor(self.text_processor, self.file_handler)
```

### 4. Reusabilidad
Las utilidades pueden importarse por separado:
```python
from reorganizer.file_utils import FileHandler
from reorganizer.text_utils import TextProcessor

# Usar en otros proyectos
fh = FileHandler()
nombre_seguro = fh.sanitize_filename("Mi Pregunta?")
```

### 5. Distribución
- Puede publicarse en PyPI
- Instalación fácil vía `uv` o `pip`
- Gestión de versiones vía `pyproject.toml`

## Pasos de Migración

### Para Usuarios

1. **Instalar la nueva herramienta:**
   ```bash
   cd reorganizer
   uv venv
   uv pip install -e .
   ```

2. **Actualizar scripts:**
   Reemplazar `python backup_reorganize.py` con `reorganizer`

3. **Probar:**
   Ejecutar con tus bancos de preguntas existentes para verificar compatibilidad

### Para Desarrolladores

1. **Actualizar imports:**
   ```python
   # Antiguo
   from backup_reorganize import QuestionBackupReorganizer
   
   # Nuevo
   from reorganizer import QuestionBackupReorganizer
   ```

2. **Usar submódulos si es necesario:**
   ```python
   from reorganizer.text_utils import TextProcessor
   from reorganizer.file_utils import FileHandler
   ```

3. **Ejecutar tests:**
   ```bash
   uv run pytest
   ```

## Compatibilidad Hacia Atrás

El script antiguo `backup_reorganize.py` permanece disponible en el directorio padre para compatibilidad hacia atrás. Sin embargo, recomendamos migrar a la nueva versión modular para:

- Mejor mantenibilidad
- Testing mejorado
- Mejoras futuras
- Mejor documentación

## Rendimiento

No se espera regresión de rendimiento. La estructura modular agrega overhead mínimo (instanciación de clases) que es negligible comparado con operaciones de I/O de archivos.

## Soporte

- **Script antiguo**: Continúa funcionando tal cual, pero no se mantiene activamente
- **Módulo nuevo**: Desarrollo activo, correcciones de bugs y mejoras

## Ejemplos

### Usar como Biblioteca

**Antiguo:**
```python
import sys
sys.path.append('/ruta/a/backup_reorganize.py')
from backup_reorganize import QuestionBackupReorganizer
```

**Nuevo:**
```python
from reorganizer import QuestionBackupReorganizer
```

### Procesamiento Personalizado

**Antiguo:**
Modificar el archivo grande único.

**Nuevo:**
Extender módulos específicos:
```python
from reorganizer.text_utils import TextProcessor

class CustomTextProcessor(TextProcessor):
    def custom_transformation(self, text):
        # Agregar lógica personalizada
        return super().apply_forward_substitutions(text)
```

## Línea de Tiempo

- **Actual**: Ambas versiones disponibles
- **Recomendado**: Comenzar a usar versión modular para nuevos proyectos
- **Futuro**: Deprecar script antiguo después de período de estabilización

## ¿Preguntas?

Ver USAGE.md/USAGE.es.md para ejemplos detallados de uso o ARCHITECTURE.md/ARCHITECTURE.es.md para detalles técnicos.
