# Reorganizador de Banco de Preguntas

Herramienta modular en Python para respaldar y reorganizar bancos de preguntas en formato GIFT o Moodle XML.

## Características

- **Exportar**: Convierte archivos monolíticos de bancos de preguntas en estructuras de directorios organizadas por categorías
- **Recolectar**: Reconstruye archivos monolíticos desde estructuras de directorios organizadas
- **Soporte de Formatos**: Funciona con formatos GIFT y Moodle XML
- **Tipos de Preguntas**: Soporta opción múltiple, cloze, emparejamiento, numérico, respuesta corta y ensayo
- **Procesamiento Seguro**: Preserva secuencias de escape, caracteres especiales y bloques de código
- **Gestión de Categorías**: Maneja automáticamente jerarquías de categorías

## Instalación

Usando UV:

```bash
uv pip install -e .
```

## Uso

### Exportar Preguntas a Estructura de Directorios

Exportar formato GIFT:
```bash
reorganizer export gift full.gift -o gift_backup
```

Exportar formato Moodle XML:
```bash
reorganizer export xml questions.xml -o xml_backup
```

### Recolectar Preguntas desde Estructura de Directorios

Recolectar formato GIFT:
```bash
reorganizer collect gift gift_backup -o full_recompiled.gift
```

Recolectar formato Moodle XML:
```bash
reorganizer collect xml xml_backup -o questions_recompiled.xml
```

## Estructura del Proyecto

El proyecto está modularizado en varios componentes:

- `cli.py` - Interfaz de línea de comandos
- `reorganizer.py` - Clase coordinadora principal
- `text_utils.py` - Utilidades de procesamiento de texto (secuencias de escape, caracteres especiales)
- `file_utils.py` - Utilidades de manejo de archivos (lectura/escritura segura, sanitización)
- `xml_utils.py` - Utilidades de procesamiento XML (CDATA, entidades HTML)
- `gift_processor.py` - Operaciones de exportar/recolectar formato GIFT
- `xml_processor.py` - Operaciones de exportar/recolectar formato Moodle XML

## Manejo de Caracteres Especiales

La herramienta incluye manejo robusto para:

- **Secuencias de escape** en bloques de código (ej., `\n`, `\0`, `\\`)
- **Caracteres fullwidth** para proteger sintaxis GIFT
- **Entidades HTML** convertidas a equivalentes fullwidth
- **Secciones CDATA** para seguridad XML
- **Bloques de código Markdown** con protección de backslashes

## Desarrollo

Ejecutar tests (si están disponibles):
```bash
uv run pytest
```

Formatear código:
```bash
uv run black src/
```

## Licencia

Este proyecto se proporciona tal cual para fines educativos.

## Documentación Adicional

- `USAGE.md` - Guía detallada de uso con ejemplos
- `ARCHITECTURE.md` - Documentación de diseño técnico
- `MIGRATION.md` - Guía de migración desde el script antiguo
- `QUICKREF.md` - Referencia rápida de comandos comunes
- `CHANGELOG.md` - Historial de cambios
