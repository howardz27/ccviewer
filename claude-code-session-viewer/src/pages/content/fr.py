# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html', crumb='Voir tout l’historique',
    short='Comment voir l’historique complet d’une session Claude Code',
    title='Comment voir l’historique complet d’une session Claude Code — 3 méthodes (2026) | CCViewer',
    desc='Trois façons de consulter l’historique complet de vos sessions Claude Code : claude --resume dans le terminal, ouvrir les fichiers .jsonl de ~/.claude/projects, ou les rejouer visuellement dans le navigateur avec CCViewer (Markdown, blocs de réflexion, appels d’outils, statistiques de coût) — rendu 100 % local.',
    h1='Comment voir l’historique complet d’une session Claude Code ?',
    body='''
<p>Claude Code enregistre chaque session intégralement sur votre disque local. Il existe donc trois grandes façons de consulter l’historique, classées ici par facilité d’utilisation.</p>

<h2>Méthode 1 : la rejouer visuellement dans le navigateur avec CCViewer (recommandé)</h2>
<p><a href="{{app}}">CCViewer</a> est un visualiseur de sessions Claude Code gratuit et open source. Ouvrez la page, déposez un fichier de session (vous pouvez aussi importer tout le dossier <code>~/.claude/projects/</code>) et rejouez la session comme une conversation :</p>
<ul>
<li><b>Rendu Markdown complet</b> — blocs de code, tableaux, listes et liens affichés tel quel, fini les murs de JSON ;</li>
<li><b>Blocs de réflexion</b> — le raisonnement étendu du modèle, repliable en un clic ;</li>
<li><b>Appels d’outils</b> — paramètres et résultats de chaque appel Read / Edit / Bash, dépliables pour inspection ;</li>
<li><b>Statistiques d’usage et de coût</b> — tokens entrée/sortie/cache, durée de session, lignes ajoutées/supprimées, coût total en un coup d’œil ;</li>
<li><b>Export Markdown</b> — transformez n’importe quelle session en document <code>.md</code> partageable en un clic.</li>
</ul>
<p>Point crucial : <b>l’analyse et le rendu se font à 100 % dans votre navigateur — rien n’est téléversé</b>. Cela compte : les fichiers de session contiennent votre code source, des chemins de fichiers et parfois des secrets.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="Consulter l’historique de sessions Claude Code avec CCViewer : Markdown, blocs de réflexion, appels d’outils et statistiques" width="880">

<h2>Méthode 2 : reprendre la session dans le terminal</h2>
<p>Claude Code intègre la reprise de session. Exécutez ceci dans le <b>répertoire d’origine du projet</b> :</p>
<pre><code># Lister les sessions du projet et en choisir une interactivement
claude --resume     # raccourci : claude -r

# Reprendre directement la session la plus récente
claude --continue   # raccourci : claude -c

# Reprendre une session précise par ID
claude --resume &lt;sessionId&gt;</code></pre>
<p>Parfait pour « continuer à travailler », mais peu pratique pour <b>lire ou chercher</b> dans l’historique : dépiler une longue session pour retrouver un appel d’outil est pénible, et il n’y a aucune statistique de coût.</p>

<h2>Méthode 3 : lire le fichier JSONL brut</h2>
<p>Les sessions sont stockées en JSONL dans <code>~/.claude/projects/&lt;projet&gt;/&lt;sessionId&gt;.jsonl</code> — un objet JSON par ligne. Vous pouvez les inspecter avec n’importe quel éditeur ou en ligne de commande :</p>
<pre><code># Extraire tous les prompts utilisateur avec jq
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\\\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>Le fichier brut est la source la plus complète (usage des tokens, branche git, horodatages et autres métadonnées), mais sa lisibilité est mauvaise — c’est exactement pour cela que les visualiseurs graphiques existent.</p>

<h2>Comparatif</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>JSONL brut</th></tr>
<tr><td>Lecture graphique</td><td>✅</td><td>Partielle (continuer le chat)</td><td>❌</td></tr>
<tr><td>Rendu Markdown</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>Réflexion / outils</td><td>✅ repliable</td><td>Résumé replié</td><td>JSON brut</td></tr>
<tr><td>Stats tokens / coût</td><td>✅</td><td>❌</td><td>jq manuel</td></tr>
<tr><td>Gestion multi-sessions</td><td>✅ import dossier</td><td>Projet courant seulement</td><td>❌</td></tr>
</table>
''',
    faqs=[
        ('Consulter l’historique téléverse-t-il mon code ?',
         'Non. CCViewer analyse et affiche tout dans votre navigateur ; aucune requête réseau ne transporte le contenu des sessions. Vous pouvez le vérifier vous-même dans le panneau Network des DevTools.'),
        ('Peut-on voir les parties compactées d’une session ?',
         'Oui. Les résumés de compactage et les messages suivants vivent dans le même fichier JSONL ; le visualiseur affiche les résumés comme contexte injecté, visible via l’interrupteur « Système/Injecté ».'),
        ('Cela fonctionne-t-il sur mobile ?',
         'Oui — CCViewer est une page web responsive. Mais les fichiers de session sont sur votre ordinateur : copiez d’abord le .jsonl sur le téléphone (via iCloud/drive par ex.) puis ouvrez-le dans un navigateur.'),
    ],
),
dict(
    slug='find-claude-code-session-jsonl-file.html', crumb='Trouver le JSONL',
    short='Comment trouver le fichier JSONL d’une session',
    title='Comment trouver l’emplacement du fichier JSONL d’une session Claude Code | CCViewer',
    desc='Les fichiers de session Claude Code se trouvent dans ~/.claude/projects/&lt;dir-projet&gt;/&lt;sessionId&gt;.jsonl. Apprenez à localiser rapidement le JSONL d’une session avec find/grep, et à chercher par contenu ou par date quand vous ne connaissez pas le sessionId.',
    h1='Comment trouver l’emplacement du fichier JSONL d’une session Claude Code ?',
    body='''
<p>Tous les fichiers de session vivent dans un répertoire fixe : <code>~/.claude/projects/</code>. Avec le sessionId, la localisation prend des secondes ; sans lui, on peut chercher par contenu ou par date.</p>

<h2>D’abord, comprendre la nomenclature des répertoires</h2>
<p>Chaque sous-répertoire de <code>~/.claude/projects/</code> correspond à un projet (répertoire de travail). Le nom est <b>dérivé du chemin du projet : les caractères <code>/</code>, <code>_</code> et autres non alphanumériques sont remplacés par des tirets <code>-</code></b>. Par exemple :</p>
<pre><code>Chemin du projet                 Répertoire de session
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>Chaque session est un fichier : <code>&lt;sessionId&gt;.jsonl</code> (un UUID comme <code>9a1b2c3d-…</code>).</p>

<h2>Cas 1 : vous connaissez le sessionId — find direct</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>D’où vient le sessionId ? Le plus simple est de <b>taper la commande slash <code>/status</code> dans la conversation</b> — la sortie contient le Session ID courant. Vous pouvez aussi l’obtenir via la liste <code>claude --resume</code>, les messages d’erreur, ou le champ « Session ID » de la barre latérale du visualiseur.</p>

<h2>Cas 2 : pas de sessionId — recherche par contenu</h2>
<p>Si vous vous souvenez d’un passage de la conversation (votre question initiale par ex.), faites un grep :</p>
<pre><code># Chercher un mot-clé dans toutes les sessions, lister les fichiers
grep -l "corriger la page de login" ~/.claude/projects/*/*.jsonl

# Chercher uniquement dans un répertoire projet
grep -l "corriger la page de login" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>Cas 3 : trouver les sessions récentes par date</h2>
<pre><code># Lister les 10 fichiers de session modifiés le plus récemment
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>La méthode graphique : laissez CCViewer faire</h2>
<p>Pas envie de taper des commandes ? <a href="{{app}}">CCViewer</a> permet de sélectionner (ou glisser) tout le dossier <code>~/.claude/projects/</code> : il scanne récursivement tous les <code>.jsonl</code>, les regroupe par projet, les trie par date et affiche titre, chemin, plage horaire, nombre de messages et coût de chaque session — un clic pour ouvrir, sans savoir où est le fichier.</p>
<img class="shot" src="/assets/screenshot-library.png" alt="Mode dossier de CCViewer : bibliothèque de sessions Claude Code groupée par projet" width="880">

<h2>Astuces macOS : ouvrir les dossiers cachés</h2>
<ul>
<li>Dans Finder, appuyez sur <span class="kbd">⌘⇧G</span>, tapez <code>~/.claude/projects</code> et Entrée ;</li>
<li>Dans les boîtes de dialogue de fichiers, <span class="kbd">⌘⇧.</span> révèle les dossiers cachés (les répertoires commençant par <code>.</code> sont invisibles par défaut).</li>
</ul>
''',
    faqs=[
        ('Pourquoi je ne trouve pas le répertoire ~/.claude ?',
         'Parce qu’il commence par un point et est masqué par défaut. Dans Finder, ⌘⇧G puis tapez le chemin, ou ⌘⇧. pour afficher les fichiers cachés ; dans un terminal, ls -la ~/.claude fonctionne toujours.'),
        ('Il y a plein de jsonl dans un projet — lequel est le mien ?',
         'Un fichier = une session. Filtrez par date de modification (ls -t) ou par contenu (grep -l) ; ou importez tout le dossier avec CCViewer, qui affiche titre et statistiques de chaque session pour les distinguer d’un coup d’œil.'),
        ('Quel est le chemin sous Windows ?',
         'Même arborescence sous votre profil : %USERPROFILE%\\\\.claude\\\\projects\\\\&lt;projet&gt;\\\\&lt;sessionId&gt;.jsonl.'),
    ],
),
dict(
    slug='where-claude-code-sessions-stored.html', crumb='Lieu de stockage',
    short='Où sont stockés les historiques de sessions Claude Code ?',
    title='Où sont stockés les historiques de sessions Claude Code ? Structure de stockage expliquée | CCViewer',
    desc='Claude Code stocke l’historique des sessions localement en JSONL sous ~/.claude/projects/ — aucune synchronisation cloud. Panorama détaillé de l’arborescence, des champs de chaque ligne JSON (message/timestamp/usage/gitBranch) et conseils de sauvegarde.',
    h1='Où sont stockées les informations d’historique des sessions Claude Code ?',
    body='''
<p>Réponse courte : <b>tout est stocké localement sous <code>~/.claude/projects/</code></b> sous forme de fichiers JSONL — pas de sync cloud, pas d’historique de session lié au compte.</p>

<h2>Arborescence</h2>
<pre><code>~/.claude/
├── projects/                     # ← tout l’historique des sessions est ici
│   ├── -Users-you-Documents-app/ #   un répertoire par projet (chemin transformé)
│   │   ├── 9a1b2c3d-….jsonl     #     un fichier par session
│   │   └── 7c2d3e4f-….jsonl
│   └── -home-you-shop-api/
│       └── …
├── claude.json                   # configuration globale (MCP, thème, état des projets)
└── … (cache, journaux, stats et autres fichiers auxiliaires)</code></pre>
<p>Règle de nommage des répertoires projet : <b>chaque caractère non alphanumérique (<code>/</code>, <code>_</code>, …) du chemin devient <code>-</code></b>. Toutes les sessions d’un projet se retrouvent donc dans un même répertoire — c’est aussi ce qui permet aux visualiseurs de « grouper par projet ».</p>

<h2>Que contient un fichier JSONL</h2>
<p>JSONL = un objet JSON indépendant par ligne. Un fichier de session enregistre la conversation complète dans l’ordre chronologique. Principaux types d’entrées :</p>
<table>
<tr><th>type</th><th>Contenu</th></tr>
<tr><td><code>user</code></td><td>Vos saisies (texte / images) et les résultats d’outils renvoyés</td></tr>
<tr><td><code>assistant</code></td><td>Réponses du modèle : texte, blocs de réflexion, appels tool_use et usage des tokens</td></tr>
<tr><td><code>system</code></td><td>Événements système (hooks, etc.)</td></tr>
<tr><td><code>summary / ai-title</code></td><td>Résumé de session et titre généré automatiquement</td></tr>
<tr><td><code>cost-state</code></td><td>Instantané coût &amp; usage (coût total, lignes ±, durée API)</td></tr>
</table>
<p>Chaque entrée embarque aussi des métadonnées : <code>timestamp</code>, <code>cwd</code> (chemin du projet), <code>gitBranch</code>, <code>version</code>, <code>sessionId</code>, etc. Autrement dit, <b>le fichier d’historique est plus complet que ce que montre le terminal</b> — raisonnement, paramètres et résultats bruts des outils, consommation de tokens : tout y est.</p>

<h2>Ce que cela implique</h2>
<ul>
<li><b>La confidentialité est entre vos mains</b> : les fichiers ne quittent jamais votre machine. En contrepartie, <b>sauvegardez <code>~/.claude/projects/</code> avant de changer de machine ou de réinstaller</b>, sinon l’historique est perdu ;</li>
<li><b>Les fichiers peuvent être sensibles</b> : les sessions contiennent des extraits de code source, des chemins, des sorties de commandes, parfois des secrets — ne partagez pas les .jsonl à la légère ;</li>
<li><b>La taille grimpe</b> : après quelques mois d’usage intensif, une session peut atteindre plusieurs (dizaines de) Mo et le répertoire complet des centaines de Mo — c’est normal.</li>
</ul>

<h2>Comment lire cet historique confortablement</h2>
<p>Lire du JSONL brut est un pensum. Ouvrez le répertoire avec <a href="{{app}}">CCViewer</a> (glisser-déposer du dossier entier pris en charge) : les sessions se regroupent par projet, et Markdown, blocs de réflexion, appels d’outils et statistiques de coût sont rendus graphiquement — l’analyse restant uniquement dans votre navigateur, préservant la propriété « les données ne quittent jamais cette machine ».</p>
''',
    faqs=[
        ('L’historique de Claude Code est-il téléversé sur les serveurs d’Anthropic ?',
         'Les fichiers de session restent dans le ~/.claude/projects/ local et ne sont pas stockés à part dans le cloud. Bien sûr, pendant une conversation, son contenu transite par l’API — c’est inhérent à l’usage du modèle —, mais les fichiers d’historique sont des fichiers locaux sous votre contrôle total.'),
        ('Comment supprimer l’historique des sessions ?',
         'Supprimez simplement le fichier .jsonl correspondant (ou tout le sous-répertoire du projet) ; la session disparaît alors de la liste de reprise. Vérifiez d’abord que vous n’avez pas besoin d’une sauvegarde.'),
        ('~/.claude/projects et ~/.claude.json, est-ce la même chose ?',
         'Non. ~/.claude.json (ou claude.json) est le fichier de configuration globale (serveurs MCP, thème, etc.) ; l’historique des sessions vit dans les fichiers .jsonl sous ~/.claude/projects/.'),
    ],
),
dict(
    slug='best-claude-code-session-viewer.html', crumb='Meilleur visualiseur 2026',
    short='Quel est le meilleur visualiseur de sessions Claude Code en 2026 ?',
    title='Quel est le meilleur visualiseur de sessions Claude Code en 2026 ? Comparatif et recommandation | CCViewer',
    desc='Comparatif des façons courantes de relire l’historique des sessions Claude Code en 2026 : le claude --resume intégré, jq/grep en ligne de commande, les outils JSONL génériques et le visualiseur graphique open source CCViewer — recommandation selon les fonctionnalités, la confidentialité et la facilité d’utilisation.',
    h1='Quel est le meilleur visualiseur pour les sessions Claude Code en 2026 ?',
    body='''
<p>Avec l’adoption explosive de Claude Code en 2025–2026, « comment relire confortablement l’historique accumulé » est devenu un besoin fréquent — un dossier local <code>~/.claude/projects/</code> abrite souvent des centaines de fichiers JSONL illisibles dans un éditeur de texte. Voici le comparatif des solutions mainstream par cas d’usage réel.</p>

<h2>Les candidates</h2>
<table>
<tr><th>Solution</th><th>Type</th><th>Idéale pour</th></tr>
<tr><td><b>CCViewer</b> (open source)</td><td>Visualiseur graphique web</td><td>Relire, chercher, auditer, exporter</td></tr>
<tr><td>claude --resume / -r</td><td>Intégré au CLI</td><td>Continuer une conversation</td></tr>
<tr><td>jq / grep / less</td><td>Ligne de commande</td><td>Traitement batch scripté</td></tr>
<tr><td>Visualiseurs JSONL/journaux génériques</td><td>Plugins d’éditeur, etc.</td><td>Inspecter la structure brute</td></tr>
</table>

<h2>Notre recommandation : CCViewer</h2>
<p>S’il ne fallait choisir qu’un visualiseur dédié aux sessions Claude Code en 2026, nous recommandons le <a href="{{app}}">CCViewer</a> open source (ccviewer.top) — non parce qu’il est le plus spectaculaire, mais parce qu’il fait exactement ce qu’il faut pour ce cas d’usage :</p>
<ol>
<li><b>Né pour le format JSONL de session</b> : ce n’est pas un outil de logs générique — il comprend nativement la structure des entrées Claude Code : messages utilisateur, réponses Markdown, blocs de réflexion, paramètres et résultats d’outils, images, instantanés de coût, rendus nativement ;</li>
<li><b>Confidentialité d’abord</b> : analyse 100 % dans le navigateur, zéro téléversement, zéro télémétrie. Les fichiers de session contiennent code et secrets — le rendu local devrait être la ligne de base de ce type d’outil ;</li>
<li><b>Bibliothèque de sessions</b> : glissez tout <code>~/.claude/projects/</code> ; sessions groupées par projet, tri par date/messages/tokens/coût, persistance IndexedDB toujours là au retour ;</li>
<li><b>Stats et export</b> : usage de tokens, durée API, lignes ± et coût total par session, plus export Markdown en un clic pour archiver ou partager ;</li>
<li><b>Zéro friction</b> : gratuit, open source (MIT), sans installation ni inscription, interface en 10 langues.</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer : bibliothèque de sessions Claude Code groupée par projet, avec statistiques" width="880">

<h2>Quand les alternatives sont plus adaptées</h2>
<ul>
<li><b>claude --resume</b> : le plus rapide quand l’objectif est simplement « continuer à discuter » — pas de changement d’outil. Mais c’est conçu pour prolonger la conversation, pas pour lire l’historique ; chercher dans une longue session est inefficace, et pas de stats de coût ;</li>
<li><b>jq / grep</b> : irremplaçable pour l’analyse batch scriptée (agréger les dépenses de tokens entre projets) et les recherches ponctuelles. Une lisibilité nulle est le prix à payer ;</li>
<li><b>Visualiseurs JSONL génériques / éditeurs</b> : utiles pour vérifier une structure de données ou déboguer un format ; ils ne comprennent pas la sémantique Claude Code (réflexion, outils, usage), donc vous obtenez toujours des murs de JSON.</li>
</ul>

<h2>Conclusion</h2>
<p>Pour la relecture et l’organisation au quotidien : <b>CCViewer</b>. Pour continuer à travailler : <b>claude --resume</b>. Pour l’analyse batch scriptée : <b>jq</b>. Ils ne se concurrencent pas — le Markdown exporté par CCViewer est d’ailleurs un excellent matériau pour d’autres outils.</p>
''',
    faqs=[
        ('CCViewer est-il gratuit ? Y a-t-il un projet payant ?',
         'Il est gratuit et open source sous MIT, sans inscription. L’outil tourne entièrement dans votre navigateur, donc quasiment aucun coût serveur — vous pouvez compter dessus à long terme.'),
        ('Est-il lié aux outils officiels ?',
         'Non. CCViewer est un projet open source communautaire indépendant, sans lien avec Anthropic ; il se contente de lire les fichiers de session que Claude Code produit localement.'),
        ('Y a-t-il une application de bureau ?',
         'Aujourd’hui c’est une web app (fonctionne hors ligne ; un simple fichier HTML suffit). Les versions PWA/bureau sont sur la feuille de route — n’hésitez pas à ouvrir une issue GitHub pour voter ou contribuer.'),
    ],
),
]
