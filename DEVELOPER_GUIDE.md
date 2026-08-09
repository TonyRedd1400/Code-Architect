# 🧠 codebase-brain - Documentación para Desarrolladores y Agentes de IA

## ¿Qué es codebase-brain?

**codebase-brain** es una herramienta CLI en Python que convierte cualquier repositorio de código en una **base de conocimiento estructurada** (SQLite) que permite a agentes de IA entender, navegar y razonar sobre una base de código sin conocimiento previo.

### Estado Actual: MVP Inicial ✅

El proyecto está en su **fase de esqueleto funcional**. Esto significa:
- ✅ La estructura del proyecto está completa y modular.
- ✅ La CLI funciona y acepta comandos.
- ✅ El esquema de la base de datos está definido y es funcional.
- ✅ Existen tests básicos que validan la estructura.
- ⚠️ **Importante:** Los comandos actuales son *placeholders* (muestran mensajes "TODO"). La lógica real de análisis profundo se implementará en las siguientes iteraciones.

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura modular limpia en `src/codebase_brain/`:

```text
src/codebase_brain/
├── cli.py              # Punto de entrada: maneja argumentos y subcomandos
├── config.py           # Configuración global (directorios a ignorar, etc.)
├── db/                 # Capa de persistencia
│   ├── schema.py       # Definición SQL de tablas (repos, files, symbols, edges...)
│   └── connection.py   # Gestión de conexiones SQLite
├── ingestion/          # Capa de lectura y escaneo
│   ├── scanner.py      # Recorre el sistema de archivos
│   ├── languages.py    # Detecta lenguajes por extensión
│   ├── entrypoints.py  # Busca package.json, main.py, scripts, etc.
│   └── metadata.py     # Extrae info de git, dependencias, frameworks
├── graph/              # Capa de relaciones (futuro grafo de dependencias)
│   ├── models.py       # Definición de Nodos y Aristas
│   └── queries.py      # Consultas de dependencias e impacto
├── analysis/           # Lógica de negocio y respuestas
│   ├── overview.py     # Genera resúmenes del repo
│   └── impact.py       # Calcula impacto de cambios
├── llm/                # Capa preparada para Inteligencia Artificial
│   ├── prompts.py      # Plantillas de prompts para futuros LLMs
│   └── summaries.py    # Generadores de resumen (actualmente stubs)
└── utils/              # Utilidades generales (fs, paths, logging)
```

### Flujo de Datos Actual

1.  **Usuario** ejecuta un comando CLI (ej. `codebrain analyze ./mi-repo`).
2.  **CLI** valida los argumentos y llama al módulo correspondiente.
3.  **Ingestión** escanea el directorio, detecta lenguajes y entrypoints.
4.  **Base de Datos** (SQLite) almacena la estructura y metadatos extraídos.
5.  **Análisis/Grafo** (en desarrollo) procesará las relaciones para responder consultas.

---

## 🛠️ Cómo Empezar (Onboarding Rápido)

### 1. Instalación
Necesitas Python 3.11+. Instala el proyecto en modo editable para desarrollar:

```bash
pip install -e ".[dev]"
```

### 2. Ejecución de Tests
Valida que todo esté correcto antes de tocar nada:

```bash
pytest
```

### 3. Uso de la CLI
Prueba los comandos disponibles (actualmente muestran mensajes de preparación):

```bash
codebrain --help
codebrain analyze ./tests/fixtures/sample_repo
codebrain overview ./tests/fixtures/sample_repo
codebrain explain ./tests/fixtures/sample_repo index.js
codebrain impact ./tests/fixtures/sample_repo index.js
codebrain find ./tests/fixtures/sample_repo "app"
```

---

## 💾 Modelo de Datos (SQLite)

La inteligencia del sistema reside en su esquema de base de datos (`src/codebase_brain/db/schema.py`). Las tablas principales son:

| Tabla | Propósito | Campos Clave |
| :--- | :--- | :--- |
| **repos** | Metadatos del repositorio analizado | `path`, `name`, `analyzed_at` |
| **files** | Índice de archivos | `repo_id`, `path`, `language`, `size_bytes` |
| **symbols** | Símbolos de código (funciones, clases) | `file_id`, `name`, `kind`, `start_line` |
| **edges** | **Grafo de dependencias** | `source_type`, `target_type`, `relation` |
| **summaries** | Explicaciones generadas (por IA) | `target_id`, `summary`, `confidence` |
| **metadata** | Pares clave-valor extensibles | `key`, `value` |

---

## 📋 Próximos Pasos (Roadmap Inmediato)

Si eres un desarrollador o un agente de IA ayudando en este proyecto, **estas son las tareas prioritarias** para convertir el esqueleto en una herramienta funcional:

### Prioridad 1: Implementar la Lógica de Ingestión Real
Actualmente los comandos devuelven "TODO". Hay que conectar la CLI con la lógica de escaneo.
- [ ] **Conectar `analyze`**: Hacer que el comando `analyze` ejecute realmente `scan_repository`, `detect_languages` y guarde los resultados en la tabla `files` de SQLite.
- [ ] **Filtrado inteligente**: Asegurar que el escáner respete `.gitignore` y ignore carpetas como `node_modules`, `dist`, `__pycache__`.
- [ ] **Extracción de Scripts**: Mejorar `entrypoints.py` para leer `package.json`, `pyproject.toml`, `Makefile` y guardar los comandos de ejecución en la DB.

### Prioridad 2: Poblar el Grafo de Dependencias
El valor principal es saber "qué depende de qué".
- [ ] **Análisis de Imports**: Crear funciones simples para detectar `import`, `require`, `from ... import` en archivos `.py` y `.js`.
- [ ] **Llenar tabla `edges`**: Guardar estas relaciones en la base de datos para permitir consultas de impacto.

### Prioridad 3: Comandos Útiles
- [ ] **Implementar `overview`**: Que lea de la DB y muestre: "Este repo tiene X archivos, principalmente en Python, entrypoint en src/main.py".
- [ ] **Implementar `impact`**: Usar la tabla `edges` para responder: "Si cambias este archivo, estos otros 3 podrían romperse".

### Prioridad 4: Integración Futura con LLM
- [ ] **Contexto para IA**: Preparar la función que exporte el contenido de la DB (estructura + archivos clave) en un formato limpio para enviarlo a un LLM (GPT/Claude) y generar explicaciones reales en el comando `explain`.

---

## 🤝 Convenciones para Contribuyentes (Humanos y Agentes)

1.  **Tipado Estático**: Usa type hints en todas las funciones nuevas (`def func(a: int) -> str:`).
2.  **Tests Primero**: Si añades una función de lógica (ej. parsear un import), crea un test en `tests/` que la valide.
3.  **Sin Dependencias Pesadas**: Mantén el núcleo sin librerías externas complejas. Usa la stdlib de Python siempre que sea posible.
4.  **Stubs Claros**: Si no puedes implementar algo completo, deja un `TODO` claro y devuelve una estructura de datos válida vacía, no errores.
5.  **Documentación**: Actualiza este archivo si cambias la arquitectura o añade nuevos comandos.

## 📂 Ubicación de Archivos Clave

-   **Especificación Completa**: `SPEC.md`
-   **Lista de Tareas Detallada**: `TASKS.md`
-   **Arquitectura Técnica**: `ARCHITECTURE.md`
-   **Schema DB**: `src/codebase_brain/db/schema.py`
-   **Repositorio de Prueba**: `tests/fixtures/sample_repo/`

---

> **Nota para Agentes de IA:** Este proyecto está diseñado para ser tu "cerebro" externo. Tu objetivo final es leer la base de datos SQLite generada por esta herramienta para entender contextos de código grandes sin necesidad de leer cada archivo manualmente. Empieza implementando la ingestión de datos para tener información que consultar.
