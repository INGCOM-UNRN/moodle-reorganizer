# Documentación de Arquitectura

## Visión General

El Reorganizador de Banco de Preguntas es una aplicación modular en Python diseñada para manejar respaldo y reorganización de bancos de preguntas en formatos GIFT y Moodle XML. La arquitectura enfatiza separación de responsabilidades, testabilidad y mantenibilidad.

## Estructura del Proyecto

```
reorganizer/
├── src/
│   └── reorganizer/
│       ├── __init__.py           # Inicialización y exportaciones del paquete
│       ├── cli.py                # Interfaz de línea de comandos
│       ├── reorganizer.py        # Clase coordinadora principal
│       ├── text_utils.py         # Utilidades de procesamiento de texto
│       ├── file_utils.py         # Utilidades de manejo de archivos
│       ├── xml_utils.py          # Utilidades de procesamiento XML
│       ├── gift_processor.py     # Procesador de formato GIFT
│       └── xml_processor.py      # Procesador de Moodle XML
├── pyproject.toml                # Configuración del proyecto
├── README.md                     # Documentación principal
├── USAGE.md / USAGE.es.md        # Guías de uso
├── ARCHITECTURE.md               # Este archivo
└── CHANGELOG.md / CHANGELOG.es.md # Historial de cambios
```

## Diseño de Módulos

### 1. Módulo CLI (`cli.py`)

**Propósito**: Interfaz de línea de comandos y parseo de argumentos

**Responsabilidades**:
- Parsear argumentos de línea de comandos
- Validar entrada del usuario
- Enrutar comandos a manejadores apropiados
- Manejar códigos de salida

**Funciones Clave**:
- `main()`: Punto de entrada para el CLI

### 2. Módulo Reorganizer (`reorganizer.py`)

**Propósito**: Clase coordinadora principal que orquesta operaciones

**Responsabilidades**:
- Inicializar todas las clases de utilidades
- Proveer API de alto nivel para operaciones de exportar/recolectar
- Coordinar entre diferentes procesadores

**Clase Clave**: `QuestionBackupReorganizer`

**Métodos**:
- `export_gift_to_structure()`
- `collect_gift_from_structure()`
- `export_xml_to_structure()`
- `collect_xml_from_structure()`

### 3. Módulo Text Utilities (`text_utils.py`)

**Propósito**: Manejar procesamiento de texto y transformaciones de caracteres

**Responsabilidades**:
- Conversiones de caracteres fullwidth
- Manejo de entidades HTML
- Preservación de secuencias de escape
- Protección de bloques de código

**Clase Clave**: `TextProcessor`

**Métodos Importantes**:
- `apply_forward_substitutions()`: Convertir caracteres especiales a fullwidth
- `replace_html_entities_to_fullwidth()`: Conversión de entidades HTML
- `protect_backslashes_in_code()`: Proteger backslashes en bloques de código
- `clean_xml_text()`: Limpiar texto para validez XML

### 4. Módulo File Utilities (`file_utils.py`)

**Propósito**: Operaciones de archivo seguras

**Responsabilidades**:
- Lectura de archivos con preservación de secuencias de escape
- Escritura de archivos con codificación apropiada
- Sanitización de nombres de archivo
- Sanitización de nombres de directorio

**Clase Clave**: `FileHandler`

**Métodos Estáticos**:
- `safe_read_preserving_escapes()`: Leer archivos de forma segura
- `safe_write_preserving_escapes()`: Escribir archivos de forma segura
- `sanitize_filename()`: Limpiar nombres de archivo
- `sanitize_dirname()`: Limpiar nombres de directorio

### 5. Módulo XML Utilities (`xml_utils.py`)

**Propósito**: Operaciones de procesamiento específicas de XML

**Responsabilidades**:
- Preprocesamiento XML (limpiar caracteres inválidos)
- Envoltura CDATA
- Procesamiento de elementos
- Manejo de entidades HTML en contexto XML

**Clase Clave**: `XMLProcessor`

**Métodos**:
- `preprocess_xml_file()`: Limpiar XML antes de parsear
- `ensure_text_elements_complete()`: Asegurar envoltura CDATA apropiada
- `process_xml_element_text()`: Procesar elementos recursivamente

### 6. Módulo GIFT Processor (`gift_processor.py`)

**Propósito**: Manejar operaciones de formato GIFT

**Responsabilidades**:
- Parsear archivos GIFT
- Extraer categorías y preguntas
- Formatear salida GIFT
- Gestionar estructura de directorio para GIFT

**Clase Clave**: `GIFTProcessor`

**Métodos**:
- `export_to_structure()`: Exportar GIFT a directorios
- `collect_from_structure()`: Recolectar GIFT desde directorios
- `_format_gift_block()`: Formatear preguntas individuales

### 7. Módulo XML Processor (`xml_processor.py`)

**Propósito**: Manejar operaciones de formato Moodle XML

**Responsabilidades**:
- Parsear archivos Moodle XML
- Extraer categorías y preguntas
- Construir salida XML
- Gestionar estructura de directorio para XML

**Clase Clave**: `MoodleXMLProcessor`

**Métodos**:
- `export_to_structure()`: Exportar XML a directorios
- `collect_from_structure()`: Recolectar XML desde directorios

## Flujo de Datos

### Operación de Exportación

```
Archivo de Entrada
    ↓
[Preprocesador] → Limpiar caracteres inválidos
    ↓
[Parser] → Dividir en preguntas/categorías
    ↓
[Procesador de Texto] → Aplicar sustituciones
    ↓
[Manejador de Archivos] → Escribir archivos individuales
    ↓
Estructura de Directorios
```

### Operación de Recolección

```
Estructura de Directorios
    ↓
[Escáner de Archivos] → Encontrar todos los archivos de preguntas
    ↓
[Manejador de Archivos] → Leer archivos individuales
    ↓
[Procesador de Texto] → Aplicar protecciones
    ↓
[Constructor de Formato] → Construir formato de salida
    ↓
Archivo de Salida
```

## Patrones de Diseño

### 1. Composición

La clase `QuestionBackupReorganizer` compone múltiples clases de utilidades en lugar de heredar de ellas. Esto proporciona flexibilidad y testabilidad.

### 2. Patrón Strategy

Diferentes procesadores (`GIFTProcessor`, `MoodleXMLProcessor`) implementan operaciones similares para diferentes formatos, permitiendo adición fácil de nuevos formatos.

### 3. Principio de Responsabilidad Única

Cada módulo tiene una responsabilidad clara y única:
- Procesamiento de texto
- Manejo de archivos
- Operaciones XML
- Procesamiento específico de formato

### 4. Inyección de Dependencias

Las clases de utilidades se inyectan en procesadores, haciendo más fácil el testing y mocking.

## Estrategia de Codificación de Caracteres

### Problema

Los bancos de preguntas contienen:
- Ejemplos de código con secuencias de escape (`\n`, `\0`)
- Caracteres de sintaxis GIFT (`{`, `}`, `=`, `#`)
- Entidades HTML en XML
- Formato Markdown

### Solución

1. **Conversión Fullwidth**: Convertir caracteres especiales GIFT a equivalentes fullwidth
2. **Protección de Código**: Proteger backslashes en bloques de código
3. **Manejo de Entidades HTML**: Convertir entidades a fullwidth en XML
4. **Envoltura CDATA**: Envolver contenido de texto XML en secciones CDATA

### Mapeos de Caracteres

```python
"=" → "＝"   # Fullwidth equals
"{" → "｛"   # Fullwidth left brace
"}" → "｝"   # Fullwidth right brace
"&lt;" → "＜" # Entidad HTML a fullwidth
```

## Manejo de Errores

### Estrategia

1. **Validación en Entrada**: CLI valida entradas temprano
2. **Degradación Elegante**: Continuar procesando preguntas válidas incluso si algunas fallan
3. **Logging Detallado**: Proporcionar mensajes de error claros con contexto
4. **Códigos de Retorno**: Usar retornos booleanos para éxito/falla

### Tipos de Error

- **Errores de Archivo**: Archivos faltantes, problemas de permisos
- **Errores de Parseo**: XML inválido, GIFT mal formado
- **Errores de Codificación**: Problemas UTF-8, caracteres inválidos

## Estrategia de Testing

### Tests Unitarios

Cada clase de utilidad debe tener tests unitarios:
- `TextProcessor`: Probar conversiones de caracteres
- `FileHandler`: Probar funciones de sanitización
- `XMLProcessor`: Probar procesamiento XML

### Tests de Integración

Probar flujos de trabajo completos:
- Ida y vuelta Exportar → Recolectar
- Preservación de categorías
- Manejo de caracteres especiales

## Puntos de Extensión

### Agregar Nuevos Formatos

1. Crear nueva clase procesadora (ej., `QTIProcessor`)
2. Implementar `export_to_structure()` y `collect_from_structure()`
3. Registrar en `QuestionBackupReorganizer`
4. Agregar opción CLI

### Agregar Nuevas Transformaciones de Texto

1. Agregar método a `TextProcessor`
2. Llamar desde procesador apropiado
3. Documentar mapeos de caracteres

## Consideraciones de Rendimiento

### Memoria

- Procesamiento en stream para archivos grandes
- No cargar archivo completo en memoria cuando sea posible
- Procesar preguntas incrementalmente

### I/O

- Operaciones de archivo en lote
- Minimizar búsquedas en disco
- Usar detección de codificación eficiente

## Consideraciones de Seguridad

### Seguridad de Archivos

- Sanitizar todos los nombres de archivo
- Validar rutas de directorio
- Prevenir traversal de directorios

### Seguridad de Caracteres

- Remover bytes nulos de XML
- Limpiar caracteres de control
- Validar codificación UTF-8

## Mejoras Futuras

1. **Procesamiento Paralelo**: Procesar múltiples archivos concurrentemente
2. **Barras de Progreso**: Feedback visual para operaciones grandes
3. **Validación**: Validar estructura de pregunta antes de procesar
4. **Herramienta Diff**: Comparar bancos de preguntas
5. **Herramienta Merge**: Fusionar múltiples bancos de preguntas
6. **Formatos de Exportación**: Agregar soporte JSON, QTI
