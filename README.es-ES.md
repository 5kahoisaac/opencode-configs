# Configuración de OpenCode

## Tabla de Contenidos

- [Resumen](#resumen)
- [Hoja de Ruta](#hoja-de-ruta)
- [Comandos de Makefile Disponibles](#comandos-de-makefile-disponibles)
- [Configuración](#configuración)
    - [Proveedores](#proveedores)
        - [Lista de Proveedores](#lista-de-proveedores)
        - [Estrategia de Lista Negra de Proveedores](#estrategia-de-lista-negra-de-proveedores)
        - [Configuración de Modelos](#configuración-de-modelos)
    - [Plugins](#plugins)
    - [MCPs](#mcps)
    - [Comandos](#comandos)
        - [Configuración de TUI](#configuración-de-tui)
    - [Agentes](#agentes)
- [Modo Equipo](#modo-equipo)
- [Enlaces de Referencia](#enlaces-de-referencia)

---

## Resumen

Este proyecto contiene una configuración integral de OpenCode diseñada para mejorar los flujos de trabajo de desarrollo asistidos por IA. OpenCode es un asistente de codificación de IA de código abierto que proporciona completado de código inteligente, capacidades de refactorización e integración fluida con diversas herramientas y plataformas de desarrollo.

La configuración incluye plugins, comandos y agentes cuidadosamente seleccionados que extienden la funcionalidad de OpenCode para soportar tareas de desarrollo complejas, mejorar la calidad del código y optimizar los flujos de trabajo. Esta configuración se enfoca particularmente en proporcionar características de grado empresarial manteniendo la flexibilidad para casos de uso personales y en equipo.

OpenCode sirve como una alternativa poderosa a los asistentes de IA basados en IDE tradicionales, ofreciendo características como generación de código consciente del contexto, refactorización de múltiples archivos, búsqueda inteligente de código e integración con herramientas populares como GitHub, Jira y Figma. Los archivos de configuración de este proyecto personalizan el comportamiento de OpenCode para ajustarse a requisitos y preferencias específicas del flujo de trabajo.

---

## Hoja de Ruta

Este repositorio se está simplificando en tres direcciones:

1. **Mover las habilidades (skills) a Skillless.** Las habilidades y los ajustes preestablecidos de habilidades se están trasladando a [skillless](https://github.com/5kahoisaac/skillless), para que este repositorio pueda mantenerse enfocado en la configuración de OpenCode en lugar de convertirse en un paquete mixto de habilidades y configuración.

2. **Eliminar las rutas de OpenCode específicas de Anthropic.** El proveedor `anthropic` y el plugin `opencode-with-claude` han sido eliminados de esta configuración por una decisión de flujo de trabajo personal. Actualmente, los modelos de Claude funcionan mejor en Claude Code que en OpenCode con Oh-My-OpenAgent, y Claude Code ofrece un control más fluido para el trabajo centrado en Claude.

3. **Centralizar los MCPs a través de MCPProxy y preferir CLIs siempre que sea posible.** Se está eliminando la mayor parte de la configuración directa de MCP para que múltiples agentes de codificación no mantengan cada uno su propia configuración de MCP. Los MCPs compartidos ahora residen detrás de MCPProxy, utilizando el modo de enrutamiento `retrieve_tools` para buscar herramientas bajo demanda y cargar perezosamente solo las herramientas que coincidan con la palabra clave o tarea actual, en lugar de inyectar cada herramienta MCP en el contexto. Con el tiempo, algunos MCPs también están siendo reemplazados por ajustes preestablecidos basados en CLI de Skillless, como la [lista de ajustes CLI](https://github.com/5kahoisaac/skillless/blob/main/lists/cli.csv). El objetivo es reemplazar los flujos de MCP de alto consumo de tokens, como `websearch` de Exa y Context7, con flujos de trabajo CLI donde ahorren tokens y funcionen mejor.

### Transiciones Recientes

El ciclo actual está eliminando superficies heredadas y consolidando la inteligencia de código en backends más rápidos:

- **Proveedores enrutados consolidados detrás de OmniRoute.** Los proveedores directos `nvidia`, `github-copilot`, `codex`, `opencode-zen` y `openai` (y las cuentas separadas y claves API que cada uno requería) han sido eliminados de esta configuración. Su superficie de modelos ahora se sirve a través de un único proveedor OmniRoute (`omni`) declarado en `opencode.json`:
    - `nvidia/*` → `omni/nvidia/*` (compilaciones de MiniMax y GPT-OSS alojadas en NVIDIA)
    - `github-copilot/*` → `omni/github/*` (variantes de GPT y Gemini alojadas en GitHub)
    - `codex/*` → `omni/codex/*` (familia OpenAI GPT-5.x alojada vía Codex)
    - `opencode-zen/*` → `omni/opencode-zen/*` (nivel gratuito de Zen; conservado solo como sub-espacio de respaldo bajo `omni/`)
    - `openai/*` → `omni/openai/*` (modelos directos de OpenAI frontados por OmniRoute)
    - Modelos Google Gemini Flash → `omni/gemini/*`
    - Modelos Zhipu GLM → `omni/glm/*`

  OmniRoute fronta estos múltiples servicios de proveedores ascendentes detrás de un único endpoint y una sola clave API (`OMNI_OPENCODE_API_KEY`) para una gestión centralizada, seguimiento unificado de costes y balanceo de carga entre los límites de tasa por cuenta. También expone un enrutador "combo" `auto/best-free` que selecciona automáticamente el mejor modelo gratuito disponible en el momento de la solicitud. El enrutamiento de agentes y categorías de tareas en `oh-my-openagent.json` ahora hace referencia a cada modelo con el prefijo `omni/` (por ejemplo `omni/nvidia/minimaxai/minimax-m3` y `omni/auto/best-free`), y las categorías `git` y `writing` se apoyan en el enrutador combo para respaldos sin coste.

  **Por qué esto ahorra tokens:** centralizar cada proveedor ascendente detrás de un solo enrutador permite que OmniRoute aplique compresión a nivel de enrutador (poda estilo headroom, filtros de eliminación de tokens estilo RTK en la salida de herramientas y deduplicación de prompts de sistema repetidos) antes de que una solicitud llegue al modelo ascendente. Una configuración directa de múltiples proveedores no puede hacer esto; cada proveedor ve la carga útil bruta completa. La consolidación también significa una única superficie de facturación para el seguimiento de costes y un único grupo de límites de tasa para balancear la carga, en lugar de N cuentas separadas cada una con su propio techo de cuota.

- **Eliminado `opencode-historian`.** El plugin y el agente historian han sido eliminados de esta configuración. El flujo de gestión de memoria que proporcionaba ya no se utiliza en esta configuración, y el plugin no necesita ser re-agregado desde otra fuente.

- **Añadido `codebase-memory-mcp` a MCPProxy.**
  [`codebase-memory-mcp`](https://github.com/DeusData/codebase-memory-mcp) fue añadido como un nuevo ascendente de MCPProxy para un mejor rendimiento en la inteligencia de código semántica. Construye un grafo de conocimiento persistente de tree-sitter y responde a consultas estructurales en menos de un milisegundo. Se ejecuta **junto con** `serena` y `ast_grep`, no como reemplazo; los tres backends son complementarios y se enrutan por intención a través del modo `retrieve_tools` de MCPProxy, con alternancia de encendido/apagado por herramienta para evitar superficies de herramientas duplicadas durante una sesión. Consulta [Inteligencia de Código](#code-intelligence-mcpproxy-retrieve_tools-mode) para las reglas de enrutamiento.

**Acceso a OmniRoute movido a Tailscale MagicDNS.** La URL base de OmniRoute cambió de `https://omniroute.isaac.ng/v1` (Túnel público de Cloudflare) a `http://rk3528:20128/v1` (nombre de host de Tailscale MagicDNS). La tailnet de Tailscale mantiene el tráfico de OpenCode a OmniRoute privado, omite el salto TLS y tiene menor latencia que el viaje de ida y vuelta a través de Cloudflare. El dominio público `omniroute.isaac.ng` se mantiene vía Túnel de Cloudflare para hosts que no estén en Tailscale (ejecutores de CI, servicios externos) y es preferible a abrir puertos de entrada para evitar la exposición directa a internet.
Consulta [Arquitectura de Red](#network-architecture).

---

## Comandos de Makefile Disponibles

Makefile proporciona comandos esenciales para gestionar la configuración de OpenCode:

| Comando      | Descripción                                                                                                                                                                                                                                                                                                                         |
|:-------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `make sync`  | Sincroniza la configuración de OpenCode en `~/.config/opencode/`. Copia `AGENTS.md`, `oh-my-openagent.json`, `opencode.json` y `tui.json`; refleja los directorios raíz `./agents/` y `./commands/` cuando están presentes. |
| `make check` | Valida las referencias cruzadas de la configuración y el desvío utilizando `scripts/check-config.py`.                                                                                                                             |
| `make help`  | Muestra las descripciones de los objetivos disponibles.                                                                                                                                                                 |

**Flujo de trabajo:**

1. Ejecuta `make sync` para copiar los archivos de configuración y cualquier archivo de `agents/` / `commands/` de nivel raíz a la configuración de usuario de OpenCode.
2. Ejecuta `make check` para validar los modelos enrutados, la cobertura de proveedores, las claves de concurrencia y el desvío de la copia desplegada.
3. Usa `make help` para ver todos los comandos disponibles.

El repositorio actual almacena los comandos con alcance de proyecto bajo `.opencode/commands/`; no hay directorios `agents/` o `commands/` de nivel raíz presentes.

---

## Configuración

### Proveedores

La configuración utiliza dos rutas de proveedores habilitadas explícitamente en `opencode.json`: el local `omlx` y el remoto `omni`. El modelo predeterminado es `omni/glm/glm-5.2`; el modelo pequeño es `omni/codex/gpt-5.4-mini`.

Ajustes principales de ejecución:

| Ajuste           | Valor actual                                                                                                                                                  |
|:------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Modelo predeterminado | `omni/glm/glm-5.2`                                                                                                              |
| Modelo pequeño    | `omni/codex/gpt-5.4-mini`                                                                                                       |
| Proveedores habilitados | `omlx`, `omni`                                                                                                                  |
| Permisos de Skills | `*` permitido                                                                                                                     |
| Herramientas Todo | `todoread`, `todowrite` permitidos                                                                                                 |
| Compactación      | `auto: true`, `prune: true`                                                                                                     |
| Ignorados del Watcher | `node_modules/**`, `dist/**`, `.git/**`, `*.lock`, `**/*.log`, `.cache/**`, `build/**`, `__pycache__/**`, `.venv/**`, `venv/**` |

#### Lista de Proveedores

**oMLX**

`omlx` es un proveedor local compatible con OpenAI para modelos alojados en MLX.

| Campo    | Valor                       |
|:---------|:----------------------------|
| Paquete  | `@ai-sdk/openai-compatible` |
| Nombre   | `oMLX`                      |
| URL Base | `http://127.0.0.1:8080/v1`  |
| API Key  | `sk_live_dummy`             |

Modelos configurados:

| ID del Modelo                       | Nombre visible                 | Contexto |  Entrada | Salida |
|:-----------------------------------|:------------------------------|--------:|-------:|-------:|
| `gemma-4-26b-a4b-it-mlx-8bit`     | Gemma 4 26B A4B MLX 8-bit     |  262144 | 160000 |  16384 |
| `qwen3.6-35b-a3b-ud-mlx-4bit`     | Qwen3.6 35B A3B MLX 4-bit     |  262144 | 160000 |  16384 |
| `qwythos-9b-claude-mythos-5-1m`    | Qwythos 9B Claude Mythos 5 1M | 1000000 | 160000 |  16384 |

**OmniRoute**

`omni` es el proveedor principal compatible con OpenAI y enrutado. Centraliza rutas de Codex, GLM, Gemini, GitHub, NVIDIA y modelos gratuitos detrás de un único endpoint.

| Campo    | Valor                         |
|:---------|:------------------------------|
| Paquete  | `@ai-sdk/openai-compatible`   |
| Nombre   | `OmniRoute`                   |
| URL Base | `http://rk3528:20128/v1`      |
| API Key  | `{env:OMNI_OPENCODE_API_KEY}` |

##### Arquitectura de Red

OmniRoute es accesible a través de **Tailscale MagicDNS**, no por la internet pública:

- `rk3528` es el nombre de host de Tailscale MagicDNS del host de OmniRoute (puerto `20128`).
- `omniroute.isaac.ng` es el dominio público; un Túnel de Cloudflare termina el tráfico de internet hacia el host.
- OpenCode accede a `rk3528:20128` directamente sobre la tailnet de Tailscale, omitiendo el Túnel de Cloudflare. El tráfico privado de la tailnet permanece fuera de la internet pública, sin salto de terminación TLS y con menor latencia.
- La puerta de entrada del Túnel de Cloudflare existe solo cuando la tailnet es inalcanzable (ej. ejecutores de CI en hosts que no son de Tailscale). Este es el camino preferido sobre la exposición directa a internet (redireccionamiento de puertos) porque el Túnel de Cloudflare nunca abre puertos de entrada en el host.

##### Catálogo de Modelos de OmniRoute

| ID del Modelo                       | Nombre visible         | Razonamiento | Adjuntos | Contexto |   Entrada | Salida | Variantes                      |
|:-----------------------------------|:-----------------------|:---------:|:-----------:|--------:|--------:|-------:|:------------------------------|
| `auto/best-free`                   | Best Free Combo        |    sí    |     no      |  262144 |  262144 | 131072 | —                             |
| `nvidia/minimaxai/minimax-m2.7`    | MiniMax M2.7           |    sí    |     no      |  204800 |  204800 | 131072 | —                             |
| `nvidia/minimaxai/minimax-m3`      | MiniMax M3             |    sí    |     sí      | 1000000 | 1000000 |  16384 | —                             |
| `nvidia/openai/gpt-oss-120b`      | GPT OSS 120B           |    sí    |     no      |  128000 |  128000 |   8192 | —                             |
| `codex/gpt-5.4`                   | GPT5.4                 |    sí    |     sí      |  200000 |  200000 | 128000 | low, medium, high, xhigh      |
| `codex/gpt-5.4-mini`               | GPT5.4Mini             |    sí    |     sí      |  409600 |  409600 | 131072 | low, medium, high, xhigh      |
| `codex/gpt-5.5`                   | GPT5.5                 |    sí    |     sí      |  400000 |  272000 | 128000 | low, medium, high, xhigh      |
| `codex/gpt-5.6-luna`               | GPT5.6Luna             |    sí    |     no      |  400000 |  400000 | 128000 | low, medium, high, xhigh, max |
| `codex/gpt-5.6-sol`                | GPT5.6Sol              |    sí    |     no      |  400000 |  400000 | 128000 | low, medium, high, xhigh, max |
| `codex/gpt-5.6-terra`              | GPT5.6Terra            |    sí    |     no      |  400000 |  400000 | 128000 | low, medium, high, xhigh, max |
| `github/gpt-4o-mini`               | GPT 4o Mini            |    no     |     sí      |  128000 |  128000 |   4096 | —                             |
| `github/gemini-3.5-flash`          | Gemini3.5Flash         |    sí    |     sí      |  200000 |  128000 |  64000 | low, medium, high, xhigh      |
| `gemini/gemini-2.5-flash`          | Gemini2.5Flash         |    sí    |     sí      | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-2.5-flash-lite`     | Gemini2.5Flash Lite    |    sí    |     sí      | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-3-flash-preview`     | Gemini 3 Flash Preview |    sí    |     sí      | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-3.1-flash-lite`     | Gemini3.1Flash Lite    |    sí    |     sí      | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `gemini/gemini-3.5-flash`          | Gemini3.5Flash         |    sí    |     sí      | 1048576 | 1048576 |  65536 | low, medium, high, xhigh      |
| `glm/glm-4.5`                     | GLM4.5                 |    sí    |     no      |  131072 |  131072 |  98304 | —                             |
| `glm/glm-4.5-air`                 | GLM4.5Air              |    sí    |     no      |  131072 |  131072 |  98304 | —                             |
| `glm/glm-4.6`                     | GLM4.6                 |    sí    |     no      |  204800 |  204800 | 131072 | —                             |
| `glm/glm-4.7`                     | GLM4.7                 |    sí    |     no      |  204800 |  204800 | 131072 | —                             |
| `glm/glm-5`                       | GLM 5                  |    sí    |     no      |  204800 |  204800 | 131072 | —                             |
| `glm/glm-5-turbo`                 | GLM 5 Turbo            |    sí    |     no      |  200000 |  200000 | 131072 | —                             |
| `glm/glm-5.1`                     | GLM5.1                 |    sí    |     no      |  200000 |  200000 | 131072 | —                             |
| `glm/glm-5.2`                     | GLM5.2                 |    sí    |     no      | 1000000 | 1000000 | 131072 | high, max                     |

##### Servicios de Proveedores

OmniRoute es un único endpoint compatible con OpenAI que fronta múltiples servicios de proveedores ascendentes detrás de una sola clave API. Esta es la arquitectura oficial de OmniRoute; cada entrada en el Catálogo de Modelos anterior es un espacio de nombres de servicio ascendente servido a través del proveedor `omni`, no una declaración de proveedor separada en `opencode.json`.

**Servicios de proveedores ascendentes frontados por `omni`:**

| Espacio de nombres    | Servicio ascendente                                              | Origen de la superficie                                            |
|:----------------------|:--------------------------------------------------------------|:-----------------------------------------------------------------|
| `omni/codex/*`        | Familia OpenAI GPT-5.x (alojada vía Codex)                      | Migrado del proveedor directo `codex`                        |
| `omni/github/*`       | Variantes de GPT y Gemini alojadas en GitHub (antiguos modelos Copilot) | Migrado del proveedor directo `github-copilot`               |
| `omni/openai/*`       | Modelos directos de OpenAI frontados por OmniRoute                     | Migrado del proveedor directo `openai`                       |
| `omni/gemini/*`       | Modelos Google Gemini Flash                                    | Migrado del proveedor directo `gemini`                       |
| `omni/glm/*`          | Modelos Zhipu GLM                                              | Migrado del proveedor directo `glm`                          |
| `omni/nvidia/*`       | Compilaciones de MiniMax y GPT-OSS alojadas en NVIDIA                      | Migrado del proveedor directo `nvidia`                       |
| `omni/opencode-zen/*` | Modelos de nivel gratuito de Zen                                          | Migrado del proveedor directo `opencode-zen` (solo respaldo) |
| `omni/auto/best-free` | Enrutador combo — selecciona automáticamente el mejor modelo gratuito disponible         | Enrutador nativo de OmniRoute; sin equivalente ascendente                  |

**Proveedores directos eliminados.** Los siguientes proveedores directos previamente declarados en `opencode.json` han sido eliminados y migrados bajo `omni/` como los espacios de nombres anteriores:

- `nvidia` — se eliminó la cuenta y la clave API de compilación de NVIDIA separadas
- `github-copilot` — se eliminó la cuenta y el token de GitHub Copilot separados
- `codex` — se eliminó la cuenta y la clave API de Codex/OpenAI separadas
- `opencode-zen` — se eliminó la cuenta de Zen separada; conservada solo como referencia de respaldo `omni/opencode-zen/big-pickle` en `oh-my-openagent.json`

`opencode.json` ahora declara solo dos proveedores habilitados: `omlx` (host MLX local) y `omni` (OmniRoute). Cada agente y categoría en `oh-my-openagent.json` hace referencia a modelos usando la forma `omni/<espacio_de_nombres>/<modelo>`.

**Por qué centralizar detrás de OmniRoute:**

- **Ahorro de tokens a nivel de enrutador.** OmniRoute aplica compresión a nivel de enrutador — poda de prompts estilo headroom, filtros de eliminación de tokens estilo RTK en la salida de herramientas y deduplicación de prompts de sistema repetidos — antes de que una solicitud llegue al modelo ascendente. Las configuraciones directas de múltiples proveedores no pueden hacer esto; cada proveedor ve la carga útil bruta completa.
- **Gestión centralizada.** Una sola clave API (`OMNI_OPENCODE_API_KEY`), un endpoint, una sola superficie de autenticación para rotar.
- **Seguimiento de costes.** Una única superficie de facturación para todo el uso de modelos, en lugar de N paneles de facturación separados.
- **Balanceo de carga.** OmniRoute balancea las solicitudes entre cuentas ascendentes detrás del mismo espacio de nombres, por lo que los techos de límites de tasa por cuenta ya no limitan una sola sesión de OpenCode.

#### Estrategia de Lista Negra de Proveedores

El comando del proyecto `/blacklist-sync` mantiene seguro el enrutamiento del nivel gratuito del proveedor Zen actualizando los datos de la lista negra de proveedores/modelos. El `opencode.json` actual utiliza los proveedores directos `omlx` y `omni`, mientras que los IDs de modelos de respaldo de Oh-My-OpenAgent aún pueden hacer referencia a `omni/opencode-zen/big-pickle` como objetivo de respaldo.

#### Configuración de Modelos

`oh-my-openagent.json` contiene asignaciones de modelos para agentes especializados y tareas de fondo enrutadas por categoría. Los IDs de modelos a continuación incluyen su prefijo de proveedor exactamente como están configurados.

**Asignaciones de Modelos Específicos del Agente**

| Agente               | Rol                | Modelo primario                      | Variante  | Modelos de respaldo                                                                                          | Notas                                                                                                            |
|:--------------------|:--------------------|:-----------------------------------|:---------|:---------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------|
| `sisyphus`          | Orquestador        | `omni/glm/glm-5.2`                 | `max`    | `omni/glm/glm-5.1`, `omni/opencode-zen/big-pickle`                                                       | Ultrawork: `omni/codex/gpt-5.5` (`medium`). Prompt: delegar fuertemente en hephaestus y paralelizar la exploración.  |
| `metis`             | Análisis de alcance | `omni/glm/glm-5.2`                 | `max`    | `omni/codex/gpt-5.5` (`high`)                                                                            | Consulta de pre-planificación.                                                                                       |
| `prometheus`        | Planificación            | `omni/codex/gpt-5.5`               | `high`   | `omni/glm/glm-5.2` (`max`)                                                                               | Prompt: mantener los planes concisos y centrarse en la estructura de archivos / decisiones clave.                                             |
| `atlas`             | Mapeo de base de código    | `omni/codex/gpt-5.5`               | `medium` | `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`                                 | Análisis y mapeo amplio de la base de código.                                                                             |
| `hephaestus`        | Implementación      | `omni/codex/gpt-5.6-sol`           | `medium` | `omni/codex/gpt-5.5` (`medium`)                                                                          | Agente de implementación primario. Prompt: adueñarse de la base de código, explorar, decidir, ejecutar; usar LSP y ast-grep agresivamente. |
| `oracle`            | Razonamiento estratégico | `omni/codex/gpt-5.5`               | `high`   | `omni/glm/glm-5.2` (`max`)                                                                               | Arquitectura y razonamiento de alto riesgo.                                                                          |
| `momus`             | Revisión              | `omni/codex/gpt-5.6-sol`           | `xhigh`  | `omni/codex/gpt-5.5` (`xhigh`), `omni/glm/glm-5.2` (`max`)                                               | Crítica del plan y la implementación.                                                                                |
| `explore`           | Análisis de base de código   | `omni/nvidia/minimaxai/minimax-m3` | —        | `omni/nvidia/minimaxai/minimax-m2.7`, `omni/gemini/gemini-3-flash-preview`, `omni/codex/gpt-5.4-mini`    | Búsqueda contextual rápida y navegación de código.                                                                      |
| `librarian`         | Investigación            | `omni/nvidia/minimaxai/minimax-m3` | —        | `omni/nvidia/minimaxai/minimax-m2.7`, `omni/gemini/gemini-3-flash-preview`, `omni/codex/gpt-5.4-mini`    | Investigación de documentación y código externo.                                                                        |
| `multimodal-looker` | Análisis visual     | `omni/codex/gpt-5.5`               | `medium` | `omni/glm/glm-5-turbo`, `omni/codex/gpt-5.4-mini`                                                        | Interpretación de imágenes y multimodal.                                                                             |
| `sisyphus-junior`   | Ejecutor de categoría   | `omni/codex/gpt-5.5`               | `medium` | `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`, `omni/opencode-zen/big-pickle` | Respalda la delegación de la categoría `task()`.                                                                              |

**Asignaciones de Modelos por Categoría de Tarea**

| Categoría             | Modelo primario                        | Variante | Modelos de respaldo                                                                                                                                 | Notas                                                                              |
|:---------------------|:-------------------------------------|:--------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------|
| `visual-engineering` | `omni/glm/glm-5.2`                   | `max`   | `omni/glm/glm-5.1`                                                                                                                              | Frontend, UI/UX, estilos, animación.                                               |
| `artistry`           | `omni/codex/gpt-5.5`                 | `high`  | `omni/glm/glm-5.2` (`max`)                                                                                                                      | Resolución creativa de problemas.                                                          |
| `ultrabrain`         | `omni/codex/gpt-5.6-sol`             | `xhigh` | `omni/codex/gpt-5.5` (`xhigh`), `omni/glm/glm-5.2` (`max`)                                                                                      | Tareas difíciles con mucha lógica.                                                            |
| `deep`               | `omni/codex/gpt-5.6-terra`           | `xhigh` | `omni/codex/gpt-5.6-sol` (`high`), `omni/glm/glm-5.2` (`max`)                                                                                   | Resolución autónoma profunda de problemas.                                                   |
| `quick`              | `omni/codex/gpt-5.4-mini`            | —       | `omni/gemini/gemini-3-flash-preview`, `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`                                  | Ediciones simples y tareas rápidas.                                                       |
| `unspecified-high`   | `omni/codex/gpt-5.5`                 | `high`  | `omni/glm/glm-5.1`, `omni/glm/glm-5.2` (`max`)                                                                                                  | Tareas no categorizadas de mayor esfuerzo.                                                 |
| `unspecified-low`    | `omni/codex/gpt-5.6-luna`            | `xhigh` | `omni/codex/gpt-5.5` (`medium`), `omni/gemini/gemini-3-flash-preview`, `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7` | Tareas no categorizadas de menor esfuerzo.                                                  |
| `writing`            | `omni/gemini/gemini-3-flash-preview` | —       | `omni/nvidia/minimaxai/minimax-m3`, `omni/nvidia/minimaxai/minimax-m2.7`, `omni/auto/best-free`                                                 | Documentación y prosa.                                                           |
| `git`                | `omni/auto/best-free`                | —       | `omni/glm/glm-4.7`, `omni/glm/glm-4.5-air`, `omni/opencode-zen/big-pickle`                                                                      | Todas las operaciones de git. Prompt: enfocarse en commits atómicos, mensajes claros, operaciones seguras. |

**Configuración de Ejecución y Tareas de Fondo**

| Área                         | Configuración actual                                                                                                                                                          |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Modo Equipo                  | Habilitado con visualización de tmux                                                                                                                                                |
| Codegraph                    | Deshabilitado (`enabled: false`, `auto_init: false`, `auto_provision: false`)                                                                                                       |
| MCPs de OMO Deshabilitados    | `context7`, `websearch`, `ast_grep`, `grep_app`, `codegraph`                                                                                                                   |
| Sobrescrituras de plugin Claude Code | `ecc@ecc`, `codex@openai-codex`, `andrej-karpathy-skills@karpathy-skills`, `claude-code-setup@claude-plugins-official`, y `understand-anything@understand-anything` deshabilitados |
| Git master                   | Sin pie de página de commit, sin co-authored-by, prefijo `GIT_MASTER=1`                                                                                                                     |
| Concurrencia de tareas fondo | Predeterminada 5; concurrencia de proveedor `omlx: 1`, `omni: 20`                                                                                                                          |
| Respaldo de ejecución        | Habilitado; reintenta `400`, `401`, `429`, `503`, `529`; máx 3 intentos de respaldo; enfriamiento de 60s; tiempo de espera de 30s; notificaciones habilitadas                                                  |

**Límites de Concurrencia de Modelos**

| Prefijo del Modelo          | Concurrencia |
|:---------------------------|------------:|
| `omni/codex/gpt-5.6-sol`   |           1 |
| `omni/codex/gpt-5.6-terra` |           2 |
| `omni/codex/gpt-5.6-luna`  |           4 |
| `omni/codex/gpt-5.5`       |           2 |
| `omni/codex/gpt-5.4`       |           4 |
| `omni/codex/gpt-5.4-mini`  |           6 |
| `omni/glm/glm-4.5`         |          10 |
| `omni/glm/glm-4.5-air`     |           5 |
| `omni/glm/glm-4.6`         |           3 |
| `omni/glm/glm-4.7`         |           2 |
| `omni/glm/glm-5`           |           2 |
| `omni/glm/glm-5-turbo`     |           1 |
| `omni/glm/glm-5.1`         |          10 |
| `omni/glm/glm-5.2`         |          10 |

### Plugins

`opencode.json` actualmente habilita dos plugins:

| Plugin                                 | Propósito                                                                                                  | Notas                                            |
|:---------------------------------------|:---------------------------------------------------------------------------------------------------------|:-------------------------------------------------|
| `@nick-vi/opencode-type-inject@latest` | Soporte de inyección de tipos para flujos de trabajo de OpenCode.                                                           | Instalado a través de la configuración de plugins de OpenCode. |
| `oh-my-openagent@latest`               | Proporciona Sisyphus, categorías de tareas, modo equipo, tareas de fondo, enrutamiento de modelos y orquestación de agentes. | Configurado a través de `oh-my-openagent.json`.       |

### MCPs

`opencode.json` configura una única entrada manual de MCP:

| MCP         | Habilitado | Tipo     | URL                         | Propósito                                                                      |
|:------------|:-------:|:---------|:----------------------------|:-----------------------------------------------------------------------------|
| `mcp-proxy` |   sí   | `remote` | `http://127.0.0.1:8081/mcp` | Endpoint central de MCPProxy para el descubrimiento de herramientas enrutadas y acceso a MCPs ascendentes. |

La superficie de MCP directa de OpenCode es intencionalmente mínima. Los MCPs compartidos se centralizan detrás de MCPProxy y se descubren a través de `retrieve_tools` / búsqueda de herramientas enrutadas en lugar de inyectar cada herramienta ascendente en cada sesión de OpenCode.

#### MCPs de Oh-My-OpenAgent Deshabilitados

`oh-my-openagent.json` deshabilita estos MCPs proporcionados por el plugin: `context7`, `websearch`, `ast_grep`, `grep_app` y `codegraph`. Esto mantiene el contexto más ligero y evita superficies de MCP duplicadas cuando se prefieren MCPProxy o equivalentes de CLI.

### Comandos

Los comandos con alcance de proyecto residen actualmente en `.opencode/commands/`.

| Comando           | Propósito                                                                                            |
|:------------------|:---------------------------------------------------------------------------------------------------|
| `/blacklist-sync` | Sincroniza dinámicamente la lista negra de OpenCode para el proveedor Zen, preservando el enrutamiento del nivel gratuito. |
| `/readme-sync`    | Sincroniza `README.md` con los archivos de configuración reales.                                           |

Actualmente no hay un directorio `commands/` de nivel raíz. `make sync` todavía admite el reflejo de uno si se añade más adelante.

### Configuración de TUI

`tui.json` actualmente selecciona el tema de terminal estándar de OpenCode:

| Ajuste | Valor      |
|:--------|:-----------|
| Tema   | `opencode` |

Se pueden añadir personalizaciones adicionales de TUI a `tui.json` cuando sea necesario.

### Agentes

OpenCode utiliza agentes proporcionados por el plugin Oh-My-OpenAgent. Actualmente no hay archivos `agents/` o `.opencode/agents/` locales en este proyecto.

#### Agentes de Oh-My-OpenAgent

Agentes y roles configurados:

| Agente               | Rol                                                               |
|:--------------------|:-------------------------------------------------------------------|
| `sisyphus`          | Orquestador primario para tareas complejas, de varios pasos y delegación. |
| `sisyphus-junior`   | Agente de respaldo ligero para la delegación de la categoría `task()`.        |
| `hephaestus`        | Agente enfocado en la implementación para ediciones y ejecución de código.         |
| `oracle`            | Asesor de razonamiento estratégico y arquitectura.                      |
| `momus`             | Agente de revisión y crítica.                                         |
| `metis`             | Agente de análisis de alcance de pre-planificación.                                 |
| `prometheus`        | Agente de planificación para planes de implementación concisos.                   |
| `atlas`             | Mapeo de la base de código y análisis de estructura.                           |
| `explore`           | Búsqueda y navegación de código contextual rápida.                        |
| `librarian`         | Investigación de documentación, fuentes externas y librerías.              |
| `multimodal-looker` | Análisis de imágenes, PDF y multimodal.                               |

Las asignaciones de modelos para estos agentes están documentadas en [Configuración de Modelos](#configuración-de-modelos).

### Modo Equipo

El modo equipo está habilitado por `oh-my-openagent.json`:

| Ajuste                        | Valor  |
|:-------------------------------|:-------|
| `team_mode.enabled`            | `true` |
| `team_mode.tmux_visualization` | `true` |

Esto habilita la orquestación de equipo paralela con visualización de tmux para los flujos de trabajo de los agentes.

### Enlaces de Referencia

#### Plugins

- [Esquema de configuración de OpenCode](https://opencode.ai/config.json)
- [Docs de OpenCode](https://opencode.ai/docs/)
- [@nick-vi/opencode-type-inject en npm](https://www.npmjs.com/package/@nick-vi/opencode-type-inject)
- [Repositorio de Oh-My-OpenAgent](https://github.com/code-yeongyu/oh-my-openagent)
- [Esquema de Oh-My-OpenAgent](https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json)

#### MCPs y Herramientas

- [MCPProxy](https://github.com/sparfenyuk/mcp-proxy)
- [Model Context Protocol](https://modelcontextprotocol.io/)

#### Proveedores y Servicios

- [Paquete de proveedor compatible con OpenAI](https://www.npmjs.com/package/@ai-sdk/openai-compatible)
- [Repositorio de Skillless](https://github.com/5kahoisaac/skillless)
- [Lista de ajustes CLI de Skillless](https://github.com/5kahoisaac/skillless/blob/main/lists/cli.csv)

#### Notas

Los enlaces de referencia reflejan solo las superficies de configuración documentadas actualmente. Los MCPs y proveedores directos eliminados de `opencode.json` no deben reintroducirse aquí a menos que los cambios de configuración los vuelvan a añadir.
