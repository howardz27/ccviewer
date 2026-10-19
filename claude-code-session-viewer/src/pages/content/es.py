# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html',
    crumb='Ver el historial completo',
    short='Cómo ver el historial completo de una sesión de Claude Code',
    title='Cómo ver el historial completo de una sesión de Claude Code — 3 métodos (2026) | CCViewer',
    desc='Tres formas de ver el historial completo de tus sesiones de Claude Code: claude --resume en la terminal, abrir los archivos .jsonl de ~/.claude/projects, o reproducirlos visualmente en el navegador con CCViewer (Markdown, bloques de pensamiento, llamadas a herramientas, estadísticas de coste) — renderizado 100% local.',
    h1='¿Cómo veo el historial completo de una sesión de Claude Code?',
    body=r'''
<p>La ruta predeterminada de las sesiones locales es ~/.claude/projects/. CLAUDE_CONFIG_DIR cambia el directorio base. La persistencia puede desactivarse y la retención puede eliminar archivos; no se conserva necesariamente todo para siempre. Comprueba el entorno de ejecución en sesiones remotas o en la nube.</p>

<h2>Método 1: Reproducirla visualmente en el navegador con CCViewer (recomendado)</h2>
<p><a href="{{app}}">CCViewer</a> es un visor de sesiones de Claude Code gratuito y de código abierto. Abre la página, suelta un archivo de sesión (también puedes elegir la carpeta <code>~/.claude/projects/</code> completa para importarlo todo) y reproduce la sesión como si fuera un chat:</p>
<ul>
<li><b>Renderizado Markdown completo</b> — bloques de código, tablas, listas y enlaces tal cual; se acabaron los muros de JSON;</li>
<li><b>Bloques de pensamiento</b> — el razonamiento extendido del modelo, plegable con un clic;</li>
<li><b>Llamadas a herramientas</b> — parámetros y resultados de cada llamada Read / Edit / Bash, desplegables para inspección;</li>
<li><b>Estadísticas de uso y coste</b> — tokens de entrada/salida/caché, duración de la sesión, líneas añadidas/eliminadas y coste total de un vistazo;</li>
<li><b>Exportación a Markdown</b> — convierte cualquier sesión en un documento <code>.md</code> compartible con un clic.</li>
</ul>
<p>Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="Viendo el historial de sesiones de Claude Code con CCViewer: Markdown, bloques de pensamiento, llamadas a herramientas y estadísticas" width="880">

<h2>Método 2: Reanudar la sesión en la terminal</h2>
<p>Claude Code incluye reanudación de sesiones. Ejecuta esto en el <b>directorio original del proyecto</b>:</p>
<pre><code># Listar las sesiones del proyecto y elegir una interactivamente
claude --resume     # abreviatura: claude -r

# Reanudar directamente la sesión más reciente
claude --continue   # abreviatura: claude -c

# Reanudar una sesión concreta por ID
claude --resume &lt;sessionId&gt;</code></pre>
<p>Perfecto para «seguir trabajando», pero incómodo para <b>leer o buscar</b> en el historial: revolver una sesión larga buscando una llamada a herramienta es un suplicio, y no hay estadísticas de coste.</p>

<h2>Método 3: Leer el archivo JSONL en bruto</h2>
<p>Las sesiones se guardan como JSONL en <code>~/.claude/projects/&lt;proyecto&gt;/&lt;sessionId&gt;.jsonl</code> — un objeto JSON por línea. Puedes inspeccionarlas con cualquier editor o la línea de comandos:</p>
<pre><code># Extraer todos los prompts del usuario con jq
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>El archivo en bruto es la fuente más completa (uso de tokens, rama de git, marcas de tiempo y otros metadatos), pero su legibilidad es pobre — exactamente la razón de ser de los visores gráficos.</p>

<h2>Comparación</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>JSONL en bruto</th></tr>
<tr><td>Lectura gráfica</td><td>✅</td><td>Parcial (continuar chat)</td><td>❌</td></tr>
<tr><td>Renderizado Markdown</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>Pensamiento / herramientas</td><td>✅ plegable</td><td>Resumen plegado</td><td>JSON crudo</td></tr>
<tr><td>Estadísticas tokens / coste</td><td>✅</td><td>❌</td><td>jq manual</td></tr>
<tr><td>Gestión multi-sesión</td><td>✅ importar carpeta</td><td>Solo proyecto actual</td><td>❌</td></tr>
</table>
<p>Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.</p>''',
    faqs=[('¿Ver el historial sube mi código?', 'Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.'), ('¿Puedo ver las partes compactadas de una sesión?', 'JSONL guarda un valor JSON por línea. CCViewer muestra los mensajes y registros de herramientas compatibles que quedan en el archivo. No recupera registros ausentes o eliminados; las estadísticas dependen de los campos disponibles. Conserva los archivos originales.'), ('¿Funciona en el móvil?', 'Sí — CCViewer es una página web responsive. Eso sí, los archivos de sesión están en tu ordenador: primero copia el .jsonl al teléfono (p. ej. vía iCloud/Drive) y ábrelo en un navegador.')],
),
dict(
    slug='find-claude-code-session-jsonl-file.html',
    crumb='Encontrar el JSONL',
    short='Cómo encontrar el archivo JSONL de una sesión',
    title='Cómo encontrar la ubicación del archivo JSONL de una sesión de Claude Code | CCViewer',
    desc='Los archivos de sesión de Claude Code están en ~/.claude/projects/&lt;dir-proyecto&gt;/&lt;sessionId&gt;.jsonl. Aprende a localizar rápidamente el JSONL de una sesión con find/grep, y a buscar por contenido o fecha cuando no conoces el sessionId.',
    h1='¿Cómo encuentro la ubicación del archivo JSONL de una sesión de Claude Code?',
    body=r'''
<p>La ruta predeterminada de las sesiones locales es ~/.claude/projects/. CLAUDE_CONFIG_DIR cambia el directorio base. La persistencia puede desactivarse y la retención puede eliminar archivos; no se conserva necesariamente todo para siempre. Comprueba el entorno de ejecución en sesiones remotas o en la nube.</p>

<h2>Primero, entiende la nomenclatura de directorios</h2>
<p>Cada subdirectorio de <code>~/.claude/projects/</code> corresponde a un proyecto (directorio de trabajo). El nombre se <b>deriva de la ruta del proyecto: los caracteres <code>/</code>, <code>_</code> y demás no alfanuméricos se sustituyen por guiones <code>-</code></b>. Por ejemplo:</p>
<pre><code>Ruta del proyecto                Directorio de sesión
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>Cada sesión es un archivo: <code>&lt;sessionId&gt;.jsonl</code> (un UUID como <code>9a1b2c3d-…</code>).</p>

<h2>Caso 1: conoces el sessionId — find directo</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>¿De dónde sale el sessionId? Lo más fácil es <b>escribir el comando de barra <code>/status</code> en la conversación</b> — la salida incluye el Session ID actual. También lo obtienes de la lista de <code>claude --resume</code>, de mensajes de error o del campo «Session ID» de la barra lateral del visor.</p>

<h2>Caso 2: sin sessionId — buscar por contenido</h2>
<p>Si recuerdas algo de la conversación (p. ej. tu pregunta original), haz grep:</p>
<pre><code># Buscar una palabra clave en todas las sesiones y listar los archivos
grep -l "arreglar la página de login" ~/.claude/projects/*/*.jsonl

# Buscar solo en un directorio de proyecto
grep -l "arreglar la página de login" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>Caso 3: encontrar sesiones recientes por fecha</h2>
<pre><code># Listar los 10 archivos de sesión modificados más recientemente
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>La forma gráfica: deja que CCViewer lo haga</h2>
<p>¿No quieres teclear comandos? <a href="{{app}}">CCViewer</a> te permite seleccionar (o arrastrar) la carpeta <code>~/.claude/projects/</code> completa: escanea recursivamente todos los <code>.jsonl</code>, los agrupa por proyecto, los ordena por fecha y muestra título, ruta, rango temporal, número de mensajes y coste de cada sesión — clic para abrir, sin saber dónde está el archivo.</p>
<img class="shot" src="/assets/screenshot-library.png" alt="Modo carpeta de CCViewer: biblioteca de sesiones de Claude Code agrupada por proyecto" width="880">

<h2>Consejos macOS: abrir carpetas ocultas</h2>
<ul>
<li>En Finder pulsa <span class="kbd">⌘⇧G</span>, escribe <code>~/.claude/projects</code> y Enter;</li>
<li>En diálogos de archivo pulsa <span class="kbd">⌘⇧.</span> para mostrar carpetas ocultas (los directorios que empiezan por <code>.</code> son invisibles por defecto).</li>
</ul>
<p>Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.</p>''',
    faqs=[('¿Por qué no encuentro el directorio ~/.claude?', 'Porque empieza con un punto y está oculto por defecto. En Finder pulsa ⌘⇧G y escribe la ruta, o ⌘⇧. para mostrar archivos ocultos; en la terminal, ls -la ~/.claude siempre funciona.'), ('Hay muchos jsonl en un proyecto — ¿cuál es el mío?', 'Un archivo equivale a una sesión. Filtra por fecha de modificación (ls -t) o contenido (grep -l); o importa la carpeta completa con CCViewer, que muestra el título y estadísticas de cada sesión para distinguirlas de un vistazo.'), ('¿Cuál es la ruta en Windows?', 'La misma estructura bajo tu perfil de usuario: %USERPROFILE%\\\\.claude\\\\projects\\\\&lt;proyecto&gt;\\\\&lt;sessionId&gt;.jsonl.')],
),
dict(
    slug='where-claude-code-sessions-stored.html',
    crumb='Dónde se guardan',
    short='¿Dónde se guarda el historial de sesiones de Claude Code?',
    title='¿Dónde se guarda el historial de sesiones de Claude Code? Estructura de almacenamiento explicada | CCViewer',
    desc='La ruta predeterminada de las sesiones locales es ~/.claude/projects/. CLAUDE_CONFIG_DIR cambia el directorio base. La persistencia puede desactivarse y la retención puede eliminar archivos; no se conserva necesariamente todo para siempre. Comprueba el entorno de ejecución en sesiones remotas o en la nube.',
    h1='¿Dónde se guarda el historial de las sesiones de Claude Code?',
    body=r'''<p>La ruta predeterminada de las sesiones locales es ~/.claude/projects/. CLAUDE_CONFIG_DIR cambia el directorio base. La persistencia puede desactivarse y la retención puede eliminar archivos; no se conserva necesariamente todo para siempre. Comprueba el entorno de ejecución en sesiones remotas o en la nube.</p><h2>Ubicación y retención</h2><ul><li><code>~/.claude/projects/&lt;project&gt;/&lt;session-id&gt;.jsonl</code> — JSONL</li><li><code>~/.claude/settings.json</code> — settings</li><li><code>~/.claude.json</code> — configuration</li></ul><p><a href="https://code.claude.com/docs/en/claude-directory">Claude Code — Ubicación y retención</a></p><h2>Formato y límites</h2><p>JSONL guarda un valor JSON por línea. CCViewer muestra los mensajes y registros de herramientas compatibles que quedan en el archivo. No recupera registros ausentes o eliminados; las estadísticas dependen de los campos disponibles. Conserva los archivos originales.</p><p>Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.</p><p><a href="{{app}}">CCViewer</a></p>''',
    faqs=[('¿Se sube el historial de Claude Code a los servidores de Anthropic?', 'La ruta predeterminada de las sesiones locales es ~/.claude/projects/. CLAUDE_CONFIG_DIR cambia el directorio base. La persistencia puede desactivarse y la retención puede eliminar archivos; no se conserva necesariamente todo para siempre. Comprueba el entorno de ejecución en sesiones remotas o en la nube. Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.'), ('¿Cómo borro el historial de sesiones?', 'Simplemente elimina el archivo .jsonl correspondiente (o el subdirectorio completo del proyecto); la sesión desaparece de la lista de resume. Asegúrate antes de no necesitar una copia.'), ('¿Son lo mismo ~/.claude/projects y ~/.claude.json?', 'No. ~/.claude.json (o claude.json) es el archivo de configuración global (servidores MCP, tema, etc.); el historial de sesiones vive en los .jsonl bajo ~/.claude/projects/.')],
),
dict(
    slug='best-claude-code-session-viewer.html',
    crumb='Mejor visor 2026',
    short='¿Cuál es el mejor visor de sesiones de Claude Code en 2026?',
    title='¿Cuál es el mejor visor de sesiones de Claude Code en 2026? Comparativa y recomendación | CCViewer',
    desc='Comparativa de las formas habituales de revisar el historial de sesiones de Claude Code en 2026: el claude --resume integrado, jq/grep en la línea de comandos, herramientas JSONL genéricas y el visor gráfico de código abierto CCViewer — recomendación por características, privacidad y facilidad de uso.',
    h1='¿Cuál es el mejor visor para sesiones de Claude Code en 2026?',
    body=r'''
<p>Esta comparación por tareas está escrita por el proyecto CCViewer. No es una clasificación independiente ni una prueba de rendimiento. CCViewer sirve para leer y exportar Markdown, resume para continuar el trabajo y jq para el análisis mediante scripts.</p><p>CCViewer no incluye búsqueda de texto completo en toda la biblioteca. Borrar los datos del navegador puede eliminar la biblioteca importada.</p>

<h2>Las candidatas</h2>
<table>
<tr><th>Opción</th><th>Tipo</th><th>Ideal para</th></tr>
<tr><td><b>CCViewer</b> (código abierto)</td><td>Visor gráfico web</td><td>Repasar, buscar, auditar, exportar</td></tr>
<tr><td>claude --resume / -r</td><td>Integrado en el CLI</td><td>Continuar un chat inacabado</td></tr>
<tr><td>jq / grep / less</td><td>Línea de comandos</td><td>Procesado masivo por script</td></tr>
<tr><td>Visores JSONL/log genéricos</td><td>Plugins de editor, etc.</td><td>Inspeccionar datos en bruto</td></tr>
</table>

<h2>Nuestra recomendación: CCViewer</h2>
<p>Si tuvieras que elegir un visor dedicado de sesiones de Claude Code en 2026, recomendamos el <a href="{{app}}">CCViewer</a> de código abierto (ccviewer.top) — no por ser el más llamativo, sino por acertar en lo esencial para este escenario:</p>
<ol>
<li><b>Nacido para el formato JSONL de sesión</b>: no es una herramienta de logs genérica — entiende de forma nativa la estructura de entradas de Claude Code: mensajes de usuario, respuestas Markdown, bloques de pensamiento, parámetros y resultados de herramientas, imágenes, instantáneas de coste, renderizados de fábrica;</li>
<li><b>Privacidad primero</b>: análisis 100% en el navegador, sin subida de archivos de sesión. Los archivos contienen código y secretos — el renderizado local debería ser el mínimo para este tipo de herramienta;</li>
<li><b>Biblioteca de sesiones</b>: arrastra todo <code>~/.claude/projects/</code>; sesiones agrupadas por proyecto, ordenables por fecha/mensajes/tokens/coste, persistidas en IndexedDB y ahí la próxima vez;</li>
<li><b>Estadísticas y exportación</b>: uso de tokens, duración de API, líneas ± y coste total por sesión, más exportación a Markdown en un clic para archivar o compartir;</li>
<li><b>Cero fricción</b>: gratis, de código abierto (MIT), sin instalación ni registro, interfaz en 10 idiomas.</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer: biblioteca de sesiones de Claude Code agrupada por proyecto, con estadísticas" width="880">

<h2>Cuándo encajan mejor las alternativas</h2>
<ul>
<li><b>claude --resume</b>: lo más rápido cuando el objetivo es simplemente «seguir chateando» — sin cambiar de herramienta. Pero está pensado para continuar conversaciones, no para leer historial; buscar en sesiones largas es ineficiente y no hay estadísticas de coste;</li>
<li><b>jq / grep</b>: insustituible para análisis masivos por script (p. ej. agregar gasto de tokens entre proyectos) y consultas puntuales. La legibilidad nula es el precio;</li>
<li><b>Visores JSONL genéricos / editores</b>: útiles para comprobar estructura de datos o depurar formatos; no entienden la semántica de Claude Code (pensamiento, herramientas, uso), así que siguen mostrando muros de JSON.</li>
</ul>

<h2>Conclusión</h2>
<p>Para repasar y organizar a diario: <b>CCViewer</b>. Para seguir trabajando: <b>claude --resume</b>. Para análisis masivo por script: <b>jq</b>. No compiten — de hecho, el Markdown que exporta CCViewer es un material excelente para alimentar otras herramientas.</p>
<p>Los archivos de sesión se analizan y muestran localmente en el navegador. El sitio alojado carga Microsoft Clarity automáticamente para registrar las interacciones. Las copias sin conexión no cargan analítica.</p>''',
    faqs=[('¿CCViewer es gratis? ¿Hay planes de cobrar?', 'Sí, es gratuito y de código abierto. No requiere registro.'), ('¿Tiene relación con las herramientas oficiales?', 'No. CCViewer es un proyecto comunitario independiente sin afiliación con Anthropic; simplemente lee los archivos de sesión que Claude Code genera localmente.')],
),
]
