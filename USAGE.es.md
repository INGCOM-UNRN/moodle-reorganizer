# Guía de Uso del Reorganizador

## Inicio Rápido

### Instalación

```bash
# Navegar al directorio del proyecto
cd reorganizer

# Crear entorno virtual e instalar
uv venv
uv pip install -e .

# Activar el entorno virtual
source .venv/bin/activate
```

### Comandos Básicos

#### Exportar (Dividir) Preguntas

Dividir un archivo monolítico de banco de preguntas en archivos individuales organizados por categoría:

**Formato GIFT:**
```bash
reorganizer export gift mis_preguntas.gift -o directorio_salida
```

**Formato Moodle XML:**
```bash
reorganizer export xml mis_preguntas.xml -o directorio_salida
```

#### Recolectar (Fusionar) Preguntas

Fusionar archivos de preguntas individuales de vuelta a un archivo monolítico:

**Formato GIFT:**
```bash
reorganizer collect gift directorio_entrada -o preguntas_fusionadas.gift
```

**Formato Moodle XML:**
```bash
reorganizer collect xml directorio_entrada -o preguntas_fusionadas.xml
```

## Estructura de Directorios

Al exportar preguntas, la herramienta crea una estructura de directorios basada en las categorías de las preguntas:

```
directorio_salida/
├── Categoria1/
│   ├── pregunta1.gift
│   ├── pregunta2.gift
│   └── Subcategoria1/
│       └── pregunta3.gift
└── Categoria2/
    ├── pregunta4.gift
    └── pregunta5.gift
```

Cada archivo contiene una sola pregunta con todos sus metadatos (respuestas, retroalimentación, etiquetas, etc.).

## Uso Avanzado

### Directorio de Salida Personalizado

```bash
reorganizer export gift preguntas.gift -o ruta/respaldo/personalizada
```

### Procesamiento de Categorías Específicas

La herramienta preserva automáticamente la estructura de categorías de tu banco de preguntas. Las categorías se definen en:

- **GIFT**: Usando directivas `$CATEGORY:`
- **XML**: Usando elementos de pregunta de categoría

### Tipos de Preguntas Soportados

La herramienta soporta todos los tipos estándar de preguntas de Moodle:

- **Opción Múltiple**: Preguntas de una o múltiples respuestas
- **Verdadero/Falso**: Preguntas booleanas
- **Respuesta Corta**: Respuestas basadas en texto con variaciones
- **Numérico**: Valores exactos o rangos
- **Ensayo**: Respuestas de texto abierto
- **Cloze**: Llenar espacios en blanco con respuestas embebidas
- **Emparejamiento**: Emparejar elementos de dos listas

Ver `examples/all_question_types.gift` para ejemplos completos de cada tipo.

### Manejo de Caracteres Especiales

La herramienta tiene protección integrada para:

1. **Bloques de código** con comillas invertidas: Protege backslashes y caracteres especiales
2. **Sintaxis GIFT**: Convierte caracteres especiales a equivalentes fullwidth
3. **Entidades XML**: Maneja entidades HTML apropiadamente en formato XML
4. **Secuencias de escape**: Preserva `\n`, `\0`, `\t`, etc. en ejemplos de código
5. **Preguntas cloze**: Detecta y formatea automáticamente respuestas embebidas correctamente

## Ejemplos de Flujo de Trabajo

### 1. Flujo de Trabajo de Respaldo y Edición

```bash
# Paso 1: Exportar a estructura de directorios
reorganizer export xml original.xml -o respaldo

# Paso 2: Editar archivos individuales en el directorio respaldo/
# (usa tu editor favorito o la herramienta mxviz)

# Paso 3: Recolectar de vuelta a XML
reorganizer collect xml respaldo -o editado.xml
```

### 2. Reorganización de Categorías

```bash
# Exportar preguntas
reorganizer export gift todas_preguntas.gift -o temp

# Reorganizar directorios manualmente
# mv temp/CategoriaVieja/* temp/CategoriaNueva/

# Recolectar con nueva estructura
reorganizer collect gift temp -o reorganizado.gift
```

### 3. Conversión de Formato (GIFT ↔ XML)

Nota: La conversión directa de formato requiere pasos intermedios:

```bash
# Exportar desde GIFT
reorganizer export gift preguntas.gift -o temp

# Importar a Moodle, exportar como XML
# (paso manual en la interfaz de Moodle)

# O viceversa
```

## Solución de Problemas

### Problema: "No se encontraron archivos .gift"

**Solución**: Asegúrate de que estás apuntando al directorio correcto y los archivos tienen extensión `.gift`.

### Problema: "No se pudo parsear XML"

**Solución**: La herramienta limpia automáticamente caracteres XML inválidos. Si persiste:
1. Verifica la codificación del archivo de entrada (debe ser UTF-8)
2. Busca bytes nulos o caracteres de control en el archivo original
3. La herramienta proporcionará números de línea para errores de parseo

### Problema: Los caracteres especiales aparecen incorrectos

**Solución**: La herramienta usa caracteres fullwidth para proteger la sintaxis GIFT. Estos son intencionales y serán procesados correctamente por Moodle.

## Integración con mxviz

La herramienta reorganizer funciona perfectamente con mxviz para edición visual:

```bash
# Exportar preguntas a directorio
reorganizer export xml preguntas.xml -o dir_preguntas

# Lanzar mxviz para editar
cd ../mxviz
uv run python -m mxviz ../dir_preguntas

# Después de editar, recolectar de vuelta
cd ../reorganizer
reorganizer collect xml ../dir_preguntas -o preguntas_actualizadas.xml
```

## Consejos de Rendimiento

- **Archivos grandes**: La herramienta maneja bancos de preguntas grandes eficientemente
- **Estructura de categorías**: Las jerarquías de categorías profundas son totalmente soportadas
- **Nomenclatura de archivos**: Los nombres de preguntas duplicados se manejan automáticamente con sufijos numéricos

## Mejores Prácticas

1. **Control de Versiones**: Usa git para rastrear cambios en archivos de preguntas individuales
2. **Respaldar Primero**: Siempre mantén un respaldo antes de reorganizar
3. **Probar Importación**: Prueba el archivo recolectado en Moodle antes de reemplazar bancos de producción
4. **Nomenclatura Consistente**: Usa nombres claros y descriptivos para las preguntas
5. **Planificación de Categorías**: Planifica tu estructura de categorías antes de reorganizar
