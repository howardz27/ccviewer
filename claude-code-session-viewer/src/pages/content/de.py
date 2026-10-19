# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html',
    crumb='Gesamten Verlauf ansehen',
    short='Wie man den vollständigen Verlauf einer Claude-Code-Session ansieht',
    title='Wie man den vollständigen Verlauf einer Claude-Code-Session ansieht — 3 Methoden (2026) | CCViewer',
    desc='Drei Wege, den vollständigen Verlauf deiner Claude-Code-Sessions einzusehen: claude --resume im Terminal, die .jsonl-Dateien unter ~/.claude/projects öffnen oder sie mit CCViewer visuell im Browser abspielen (Markdown, Thinking-Blöcke, Tool-Aufrufe, Kostenstatistiken) — 100 % lokales Rendering.',
    h1='Wie sehe ich den vollständigen Verlauf einer Claude-Code-Session?',
    body=r'''
<p>Lokale Sitzungen liegen standardmäßig unter ~/.claude/projects/. CLAUDE_CONFIG_DIR ändert das Basisverzeichnis. Speicherung kann deaktiviert sein und Aufbewahrungsregeln können Dateien löschen; nicht jeder Verlauf bleibt dauerhaft verfügbar. Prüfe bei Cloud- oder Remote-Sitzungen die Ausführungsumgebung.</p>

<h2>Methode 1: Visuell im Browser mit CCViewer abspielen (empfohlen)</h2>
<p><a href="{{app}}">CCViewer</a> ist ein kostenloser Open-Source-Session-Viewer für Claude Code. Seite öffnen, Session-Datei hineinziehen (auch der ganze Ordner <code>~/.claude/projects/</code> funktioniert) und die Session wie ein Chat-Protokoll abspielen:</p>
<ul>
<li><b>Volles Markdown-Rendering</b> — Code-Blöcke, Tabellen, Listen und Links wie im Original, Schluss mit JSON-Mauern;</li>
<li><b>Thinking-Blöcke</b> — das erweiterte Reasoning des Modells, per Klick einklappbar;</li>
<li><b>Tool-Aufrufe</b> — Parameter und Ergebnisse jedes Read-/Edit-/Bash-Aufrufs, aufklappbar zur Prüfung;</li>
<li><b>Nutzungs- und Kostenstatistiken</b> — Input/Output/Cache-Tokens, Sitzungsdauer, hinzugefügte/entfernte Zeilen, Gesamtkosten auf einen Blick;</li>
<li><b>Markdown-Export</b> — jede Session per Klick in ein teilbares <code>.md</code>-Dokument verwandeln.</li>
</ul>
<p>Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="Claude-Code-Sessions-Verlauf mit CCViewer ansehen: Markdown, Thinking-Blöcke, Tool-Aufrufe und Statistiken" width="880">

<h2>Methode 2: Die Session im Terminal fortsetzen</h2>
<p>Claude Code hat eine eingebaute Sitzungsfortsetzung. Führe dies im <b>Original-Projektverzeichnis</b> aus:</p>
<pre><code># Sessions dieses Projekts auflisten und interaktiv wählen
claude --resume     # Kurzform: claude -r

# Direkt die letzte Session fortsetzen
claude --continue   # Kurzform: claude -c

# Eine bestimmte Session per ID fortsetzen
claude --resume &lt;sessionId&gt;</code></pre>
<p>Super zum „Weiterarbeiten“, aber unpraktisch zum <b>Lesen oder Durchsuchen</b> des Verlaufs: In einer langen Session einen einzelnen Tool-Aufruf zu finden ist mühsam, Kostenstatistiken gibt es keine.</p>

<h2>Methode 3: Die rohe JSONL-Datei lesen</h2>
<p>Sessions liegen als JSONL unter <code>~/.claude/projects/&lt;projekt&gt;/&lt;sessionId&gt;.jsonl</code> — ein JSON-Objekt pro Zeile. Mit jedem Editor oder der Kommandozeile prüfbar:</p>
<pre><code># Alle User-Prompts mit jq extrahieren
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>Die Rohdatei ist die vollständigste Quelle (Token-Nutzung, Git-Branch, Zeitstempel und weitere Metadaten), aber schlecht lesbar — genau der Grund, warum grafische Viewer existieren.</p>

<h2>Vergleich</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>Rohes JSONL</th></tr>
<tr><td>Grafisches Lesen</td><td>✅</td><td>Teilweise (Chat fortsetzen)</td><td>❌</td></tr>
<tr><td>Markdown-Rendering</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>Thinking / Tool-Aufrufe</td><td>✅ einklappbar</td><td>Eingeklappte Zusammenfassung</td><td>Roh-JSON</td></tr>
<tr><td>Token-/Kostenstatistiken</td><td>✅</td><td>❌</td><td>Manuelles jq</td></tr>
<tr><td>Multi-Session-Verwaltung</td><td>✅ Ordner-Import</td><td>Nur aktuelles Projekt</td><td>❌</td></tr>
</table>
<p>Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.</p>''',
    faqs=[('Wird beim Ansehen des Verlaufs mein Code hochgeladen?', 'Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.'), ('Sehe ich auch die komprimierten (compact) Teile einer Session?', 'JSONL enthält einen JSON-Wert pro Zeile. CCViewer zeigt unterstützte Nachrichten und Tool-Einträge, die in der Datei vorhanden sind. Fehlende oder gelöschte Daten lassen sich nicht wiederherstellen; Statistiken hängen von den verfügbaren Feldern ab. Bewahre Originaldateien auf.'), ('Funktioniert das auf dem Handy?', 'Ja — CCViewer ist eine responsive Web-Seite. Die Session-Dateien liegen allerdings auf dem Rechner: erst das .jsonl aufs Handy kopieren (z. B. via iCloud/Cloud-Drive) und im Browser öffnen.')],
),
dict(
    slug='find-claude-code-session-jsonl-file.html',
    crumb='JSONL-Datei finden',
    short='Wie man die JSONL-Datei einer Session findet',
    title='Wie man den Speicherort der JSONL-Datei einer Claude-Code-Session findet | CCViewer',
    desc='Claude-Code-Session-Dateien liegen unter ~/.claude/projects/&lt;projekt-verz&gt;/&lt;sessionId&gt;.jsonl. So lokalisierst du die JSONL-Datei einer Session schnell mit find/grep — und suchst per Inhalt oder Zeit, wenn du die sessionId nicht kennst.',
    h1='Wie finde ich den Speicherort der JSONL-Datei einer Claude-Code-Session?',
    body=r'''
<p>Lokale Sitzungen liegen standardmäßig unter ~/.claude/projects/. CLAUDE_CONFIG_DIR ändert das Basisverzeichnis. Speicherung kann deaktiviert sein und Aufbewahrungsregeln können Dateien löschen; nicht jeder Verlauf bleibt dauerhaft verfügbar. Prüfe bei Cloud- oder Remote-Sitzungen die Ausführungsumgebung.</p>

<h2>Zuerst das Namensschema der Verzeichnisse verstehen</h2>
<p>Jedes Unterverzeichnis von <code>~/.claude/projects/</code> entspricht einem Projekt (Arbeitsverzeichnis). Der Name wird <b>aus dem Projektpfad abgeleitet: <code>/</code>, <code>_</code> und andere nicht-alphanumerische Zeichen werden durch Bindestriche <code>-</code> ersetzt</b>. Beispiel:</p>
<pre><code>Projektpfad                        Session-Verzeichnis
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>Jede Session ist eine Datei: <code>&lt;sessionId&gt;.jsonl</code> (eine UUID wie <code>9a1b2c3d-…</code>).</p>

<h2>Fall 1: sessionId bekannt — einfach find</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>Woher kommt die sessionId? Am einfachsten: <b>in der Konversation den Slash-Befehl <code>/status</code> eingeben</b> — die Ausgabe enthält die aktuelle Session ID. Alternativ die Session-Liste von <code>claude --resume</code>, Fehlermeldungen oder das Feld „Session ID“ in der Seitenleiste des Viewers.</p>

<h2>Fall 2: keine sessionId — per Inhalt suchen</h2>
<p>Wenn du dich an einen Ausschnitt der Konversation erinnerst (z. B. deine damalige Frage), greife zu grep:</p>
<pre><code># Alle Sessions nach Stichwort durchsuchen, Treffer auflisten
grep -l "Login-Seite reparieren" ~/.claude/projects/*/*.jsonl

# Nur ein Projektverzeichnis durchsuchen
grep -l "Login-Seite reparieren" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>Fall 3: neueste Sessions nach Zeit finden</h2>
<pre><code># Die 10 zuletzt geänderten Session-Dateien auflisten
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>Der grafische Weg: CCViewer übernehmen lassen</h2>
<p>Keine Lust auf Kommandos? <a href="{{app}}">CCViewer</a> erlaubt das Auswählen (oder Hineinziehen) des gesamten Ordners <code>~/.claude/projects/</code>: Es scannt rekursiv alle <code>.jsonl</code>, gruppiert nach Projekt, sortiert nach Zeit und zeigt Titel, Pfad, Zeitraum, Nachrichtenanzahl und Kosten jeder Session — anklicken und öffnen, ganz ohne zu wissen, wo die Datei liegt.</p>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer-Ordnermodus: nach Projekt gruppierte Claude-Code-Session-Bibliothek" width="880">

<h2>macOS-Tipps: versteckte Ordner öffnen</h2>
<ul>
<li>Im Finder <span class="kbd">⌘⇧G</span> drücken, <code>~/.claude/projects</code> eingeben, Enter;</li>
<li>In Dateidialogen mit <span class="kbd">⌘⇧.</span> versteckte Ordner einblenden (Verzeichnisse mit führendem <code>.</code> sind standardmäßig unsichtbar).</li>
</ul>
<p>Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.</p>''',
    faqs=[('Warum finde ich das Verzeichnis ~/.claude nicht?', 'Weil es mit einem Punkt beginnt und standardmäßig versteckt ist. Im Finder ⌘⇧G mit Pfad, oder ⌘⇧. für versteckte Dateien; im Terminal klappt ls -la ~/.claude immer.'), ('Unter einem Projekt liegen viele jsonl-Dateien — welche ist meine?', 'Eine Datei = eine Session. Nach Änderungszeit (ls -t) oder Inhalt (grep -l) filtern ist am effektivsten; mit CCViewer den ganzen Ordner importieren — Titel und Statistiken jeder Session machen sie auf einen Blick unterscheidbar.'), ('Wie lautet der Pfad unter Windows?', 'Gleiche Struktur im Nutzerprofil: %USERPROFILE%\\\\.claude\\\\projects\\\\&lt;projekt&gt;\\\\&lt;sessionId&gt;.jsonl.')],
),
dict(
    slug='where-claude-code-sessions-stored.html',
    crumb='Speicherort',
    short='Wo werden Claude-Code-Sitzungsverläufe gespeichert?',
    title='Wo werden Claude-Code-Sitzungsverläufe gespeichert? Speicherstruktur erklärt | CCViewer',
    desc='Lokale Sitzungen liegen standardmäßig unter ~/.claude/projects/. CLAUDE_CONFIG_DIR ändert das Basisverzeichnis. Speicherung kann deaktiviert sein und Aufbewahrungsregeln können Dateien löschen; nicht jeder Verlauf bleibt dauerhaft verfügbar. Prüfe bei Cloud- oder Remote-Sitzungen die Ausführungsumgebung.',
    h1='Wo werden die Verlaufsinformationen von Claude-Code-Sessions gespeichert?',
    body=r'''<p>Lokale Sitzungen liegen standardmäßig unter ~/.claude/projects/. CLAUDE_CONFIG_DIR ändert das Basisverzeichnis. Speicherung kann deaktiviert sein und Aufbewahrungsregeln können Dateien löschen; nicht jeder Verlauf bleibt dauerhaft verfügbar. Prüfe bei Cloud- oder Remote-Sitzungen die Ausführungsumgebung.</p><h2>Speicherort und Aufbewahrung</h2><ul><li><code>~/.claude/projects/&lt;project&gt;/&lt;session-id&gt;.jsonl</code> — JSONL</li><li><code>~/.claude/settings.json</code> — settings</li><li><code>~/.claude.json</code> — configuration</li></ul><p><a href="https://code.claude.com/docs/en/claude-directory">Claude Code — Speicherort und Aufbewahrung</a></p><h2>Format und Grenzen</h2><p>JSONL enthält einen JSON-Wert pro Zeile. CCViewer zeigt unterstützte Nachrichten und Tool-Einträge, die in der Datei vorhanden sind. Fehlende oder gelöschte Daten lassen sich nicht wiederherstellen; Statistiken hängen von den verfügbaren Feldern ab. Bewahre Originaldateien auf.</p><p>Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.</p><p><a href="{{app}}">CCViewer</a></p>''',
    faqs=[('Wird der Claude-Code-Verlauf auf Anthropic-Server hochgeladen?', 'Lokale Sitzungen liegen standardmäßig unter ~/.claude/projects/. CLAUDE_CONFIG_DIR ändert das Basisverzeichnis. Speicherung kann deaktiviert sein und Aufbewahrungsregeln können Dateien löschen; nicht jeder Verlauf bleibt dauerhaft verfügbar. Prüfe bei Cloud- oder Remote-Sitzungen die Ausführungsumgebung. Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.'), ('Wie lösche ich den Sitzungsverlauf?', 'Einfach die betreffende .jsonl-Datei (oder das ganze Projekt-Unterverzeichnis) löschen; die Session verschwindet dann auch aus der Resume-Liste. Vorher sichergehen, dass kein Backup gebraucht wird.'), ('Sind ~/.claude/projects und ~/.claude.json dasselbe?', 'Nein. ~/.claude.json (bzw. claude.json) ist die globale Konfigurationsdatei (MCP-Server, Theme usw.); der Sitzungsverlauf liegt in den .jsonl-Dateien unter ~/.claude/projects/.')],
),
dict(
    slug='best-claude-code-session-viewer.html',
    crumb='Bester Viewer 2026',
    short='Was ist der beste Claude-Code-Session-Viewer 2026?',
    title='Was ist der beste Claude-Code-Session-Viewer 2026? Vergleich und Empfehlung | CCViewer',
    desc='Vergleich der gängigen Wege, 2026 Claude-Code-Sitzungsverläufe zu sichten: das eingebaute claude --resume, jq/grep auf der Kommandozeile, generische JSONL-Tools und der Open-Source-Viewer CCViewer — Empfehlung nach Funktionen, Privatsphäre und Bedienung.',
    h1='Was ist 2026 der beste Viewer für Claude-Code-Sessions?',
    body=r'''
<p>Dieser Vergleich nach Aufgaben stammt vom CCViewer-Projekt. Er ist weder eine unabhängige Rangliste noch ein Leistungstest. CCViewer eignet sich zum Lesen und Markdown-Export, resume zum Fortsetzen der Arbeit und jq für Skriptanalysen.</p><p>CCViewer bietet keine integrierte Volltextsuche über die gesamte Bibliothek. Das Löschen von Browserdaten kann die importierte Bibliothek entfernen.</p>

<h2>Die Kandidaten</h2>
<table>
<tr><th>Option</th><th>Typ</th><th>Am besten für</th></tr>
<tr><td><b>CCViewer</b> (Open Source)</td><td>Grafischer Web-Viewer</td><td>Sichten, Suchen, Auditing, Export</td></tr>
<tr><td>claude --resume / -r</td><td>Im CLI integriert</td><td>Ein Gespräch fortsetzen</td></tr>
<tr><td>jq / grep / less</td><td>Kommandozeile</td><td>Skriptgesteuerte Massenverarbeitung</td></tr>
<tr><td>Generische JSONL/Log-Viewer</td><td>Editor-Plugins etc.</td><td>Rohdatenstruktur prüfen</td></tr>
</table>

<h2>Unsere Empfehlung: CCViewer</h2>
<p>Wenn 2026 ein dedizierter Claude-Code-Session-Viewer gewählt werden muss, empfehlen wir das Open-Source-Projekt <a href="{{app}}">CCViewer</a> (ccviewer.top) — nicht weil es das Flashigste ist, sondern weil es für genau dieses Szenario das Wesentliche richtig macht:</p>
<ol>
<li><b>Für das JSONL-Session-Format gebaut</b>: kein generisches Log-Werkzeug, sondern natives Verständnis der Claude-Code-Eintragsstruktur — Nutzernachrichten, Markdown-Antworten, Thinking-Blöcke, Tool-Parameter und -Ergebnisse, Bilder, Kosten-Snapshots werden sofort gerendert;</li>
<li><b>Privatsphäre zuerst</b>: 100 % Parsing im Browser, null Upload, null Telemetrie. Session-Dateien enthalten Quellcode und Secrets — lokales Rendering sollte für solche Tools die Grundlinie sein;</li>
<li><b>Session-Bibliothek</b>: den ganzen Ordner <code>~/.claude/projects/</code> hineinziehen; Gruppierung nach Projekt, Sortierung nach Zeit/Nachrichten/Tokens/Kosten, Persistenz via IndexedDB — beim nächsten Mal noch da;</li>
<li><b>Statistiken und Export</b>: Token-Nutzung, API-Dauer, Zeilen ± und Gesamtkosten pro Session, plus Markdown-Export per Klick zum Archivieren oder Teilen;</li>
<li><b>Null Hürden</b>: kostenlos, Open Source (MIT), ohne Installation oder Registrierung, UI in 10 Sprachen.</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer: nach Projekt gruppierte Claude-Code-Session-Bibliothek mit Statistiken" width="880">

<h2>Wann die Alternativen besser passen</h2>
<ul>
<li><b>claude --resume</b>: am schnellsten, wenn es nur ums „Weiterchatten“ geht — kein Toolwechsel. Gebaut zum Fortsetzen von Gesprächen, nicht zum Lesen von Verläufen; die Suche in langen Sessions ist ineffizient, Kostenstatistiken fehlen;</li>
<li><b>jq / grep</b>: unverzichtbar für skriptgesteuerte Massenanalyse (z. B. Token-Ausgaben über Projekte aggregieren) und schnelle Einzelnachfragen. Lesbarkeit null ist der Preis;</li>
<li><b>Generische JSONL-Viewer/Editoren</b>: nützlich zum Prüfen von Datenstrukturen oder Format-Debugging; sie verstehen Claude-Code-Semantik (Thinking, Tools, Nutzung) nicht — heraus kommt wieder ein JSON-Mauerwerk.</li>
</ul>

<h2>Fazit</h2>
<p>Für tägliches Sichten und Ordnen: <b>CCViewer</b>. Zum Weiterarbeiten: <b>claude --resume</b>. Für skriptgesteuerte Massenanalyse: <b>jq</b>. Sie konkurrieren nicht — das von CCViewer exportierte Markdown ist sogar bestes Futter für andere Tools.</p>
<p>Sitzungsdateien werden lokal im Browser verarbeitet und angezeigt. Die gehostete Website lädt Microsoft Clarity automatisch, um Seiteninteraktionen aufzuzeichnen. Offline-Kopien laden keine Analyse.</p>''',
    faqs=[('Ist CCViewer kostenlos? Gibt es Pläne, Geld zu verlangen?', 'Ja, kostenlos und Open Source. Keine Registrierung nötig.'), ('Steht es in Verbindung zu den offiziellen Tools?', 'Nein. CCViewer ist ein unabhängiges Community-Projekt ohne Verbindung zu Anthropic; es liest lediglich die Session-Dateien, die Claude Code lokal erzeugt.')],
),
]
