# Historial de Cambios

Todos los cambios notables al proyecto Reorganizador de Banco de Preguntas serán documentados en este archivo.

## [Sin Liberar]

### Mejorado
- Formato mejorado de preguntas GIFT para manejar apropiadamente preguntas cloze
- Detección automática añadida de preguntas cloze (preguntas con respuestas embebidas)
- Soporte mejorado para múltiples tipos de preguntas: cloze, emparejamiento, numérico, respuesta corta y ensayo

### Documentación
- Traducción completa de documentación al español
- Actualización de USAGE.md con ejemplos más detallados
- Nueva estructura de documentación bilingüe (español/inglés)

## [1.0.0] - 2025-11-12

### Agregado
- Lanzamiento modular inicial
- Separado `backup_reorganize.py` monolítico en 8 módulos enfocados
- Documentación comprehensiva añadida (README, USAGE, ARCHITECTURE, MIGRATION, QUICKREF)
- Suite de tests basada en pytest añadida
- Configuración de proyecto UV con pyproject.toml
- Herramienta de línea de comandos vía entry point
- Directorio de ejemplos con scripts de uso
- .gitignore para proyecto Python

### Estructura de Módulos
- `cli.py` - Interfaz de línea de comandos y parseo de argumentos
- `reorganizer.py` - Clase coordinadora principal
- `text_utils.py` - Utilidades de procesamiento de texto
- `file_utils.py` - Utilidades de manejo de archivos  
- `xml_utils.py` - Utilidades de procesamiento XML
- `gift_processor.py` - Operaciones de exportar/recolectar formato GIFT
- `xml_processor.py` - Operaciones de exportar/recolectar formato Moodle XML

### Características
- Exportar GIFT y Moodle XML a estructuras de directorios
- Recolectar archivos individuales de vuelta a formatos monolíticos
- Preservar secuencias de escape en bloques de código
- Proteger caracteres especiales GIFT con equivalentes fullwidth
- Manejar entidades HTML en XML
- Limpiar caracteres XML inválidos automáticamente
- Sanitizar nombres de archivos y directorios
- Manejar colisiones de nombres de archivo con sufijos numéricos
- Organización basada en categorías

### Documentación
- README.md - Visión general del proyecto
- USAGE.md - Guía detallada de uso con ejemplos
- ARCHITECTURE.md - Documentación de diseño técnico
- MIGRATION.md - Guía de migración desde script antiguo
- QUICKREF.md - Referencia rápida para comandos comunes
- CHANGELOG.md - Este archivo

### Testing
- 6 tests unitarios cubriendo funcionalidad core
- Tests para procesamiento de texto
- Tests para manejo de archivos
- Tests para conversión de entidades HTML
- Tests para protección de backslashes
- Todos los tests pasando

### Compatibilidad
- Python 3.10+
- Mantiene compatibilidad de API con script original
- Estructura de comandos CLI sin cambios (solo invocación diferente)

## [Pre-1.0.0] - Script Original

### Características (desde backup_reorganize.py)
- Exportar/recolectar GIFT y Moodle XML
- Organización basada en categorías
- Manejo de caracteres especiales
- Preservación de secuencias de escape
- Preprocesamiento de XML
- Sanitización de nombres de archivo
