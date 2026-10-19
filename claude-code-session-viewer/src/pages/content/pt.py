# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html',
    crumb='Ver o histórico completo',
    short='Como ver o histórico completo de uma sessão do Claude Code',
    title='Como Ver o Histórico Completo de uma Sessão do Claude Code — 3 Métodos (2026) | CCViewer',
    desc='Três formas de ver o histórico completo das suas sessões do Claude Code: claude --resume no terminal, abrir os arquivos .jsonl de ~/.claude/projects, ou reproduzi-las visualmente no navegador com o CCViewer (Markdown, blocos de raciocínio, chamadas de ferramenta, estatísticas de custo) — renderização 100% local.',
    h1='Como vejo o histórico completo de uma sessão do Claude Code?',
    body=r'''
<p>O caminho padrão das sessões locais é ~/.claude/projects/. CLAUDE_CONFIG_DIR altera o diretório base. A persistência pode ser desativada e a retenção pode apagar arquivos; nem todo histórico permanece para sempre. Confira o ambiente de execução de sessões remotas ou na nuvem.</p>

<h2>Método 1: Reproduzir visualmente no navegador com o CCViewer (recomendado)</h2>
<p>O <a href="{{app}}">CCViewer</a> é um visualizador de sessões do Claude Code, gratuito e de código aberto. Abra a página, solte um arquivo de sessão (também dá para importar a pasta <code>~/.claude/projects/</code> inteira) e reproduza a sessão como uma conversa:</p>
<ul>
<li><b>Renderização Markdown completa</b> — blocos de código, tabelas, listas e links como são; chega de paredes de JSON;</li>
<li><b>Blocos de raciocínio</b> — o raciocínio estendido do modelo, recolhível com um clique;</li>
<li><b>Chamadas de ferramenta</b> — parâmetros e resultados de cada chamada Read / Edit / Bash, expansíveis para inspeção;</li>
<li><b>Estatísticas de uso e custo</b> — tokens de entrada/saída/cache, duração da sessão, linhas adicionadas/removidas, custo total de relance;</li>
<li><b>Exportação em Markdown</b> — transforme qualquer sessão num documento <code>.md</code> compartilhável com um clique.</li>
</ul>
<p>Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="Vendo o histórico de sessões do Claude Code com o CCViewer: Markdown, blocos de raciocínio, chamadas de ferramenta e estatísticas" width="880">

<h2>Método 2: Retomar a sessão no terminal</h2>
<p>O Claude Code tem retomada de sessão integrado. Execute isto no <b>diretório original do projeto</b>:</p>
<pre><code># Listar as sessões do projeto e escolher uma interativamente
claude --resume     # forma curta: claude -r

# Retomar diretamente a sessão mais recente
claude --continue   # forma curta: claude -c

# Retomar uma sessão específica por ID
claude --resume &lt;sessionId&gt;</code></pre>
<p>Ótimo para "continuar trabalhando", mas desconfortável para <b>ler ou pesquisar</b> o histórico: garimpar numa sessão longa por uma chamada de ferramenta é um sofrimento, e não há estatísticas de custo.</p>

<h2>Método 3: Ler o arquivo JSONL bruto</h2>
<p>As sessões ficam em JSONL em <code>~/.claude/projects/&lt;projeto&gt;/&lt;sessionId&gt;.jsonl</code> — um objeto JSON por linha. Dá para inspecionar com qualquer editor ou linha de comando:</p>
<pre><code># Extrair todos os prompts do usuário com jq
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>O arquivo bruto é a fonte mais completa (uso de tokens, branch do git, timestamps e outros metadados), mas a legibilidade é ruim — exatamente por isso existem visualizadores gráficos.</p>

<h2>Comparação</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>JSONL bruto</th></tr>
<tr><td>Leitura gráfica</td><td>✅</td><td>Parcial (continuar chat)</td><td>❌</td></tr>
<tr><td>Renderização Markdown</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>Raciocínio / ferramentas</td><td>✅ recolhível</td><td>Resumo recolhido</td><td>JSON bruto</td></tr>
<tr><td>Estatísticas tokens / custo</td><td>✅</td><td>❌</td><td>jq manual</td></tr>
<tr><td>Gestão de várias sessões</td><td>✅ importar pasta</td><td>Só projeto atual</td><td>❌</td></tr>
</table>
<p>Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.</p>''',
    faqs=[('Ver o histórico envia meu código?', 'Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.'), ('Dá para ver as partes compactadas de uma sessão?', 'JSONL contém um valor JSON por linha. O CCViewer mostra mensagens e registros de ferramentas compatíveis que permanecem no arquivo. Não recupera registros ausentes ou apagados; as estatísticas dependem dos campos disponíveis. Guarde os arquivos originais.'), ('Funciona no celular?', 'Sim — o CCViewer é uma página responsiva. Mas os arquivos de sessão estão no computador: primeiro copie o .jsonl para o telefone (ex.: via iCloud/drive) e abra no navegador.')],
),
dict(
    slug='find-claude-code-session-jsonl-file.html',
    crumb='Encontrar o JSONL',
    short='Como encontrar o arquivo JSONL de uma sessão',
    title='Como Encontrar a Localização do Arquivo JSONL de uma Sessão do Claude Code | CCViewer',
    desc='Os arquivos de sessão do Claude Code ficam em ~/.claude/projects/&lt;dir-projeto&gt;/&lt;sessionId&gt;.jsonl. Aprenda a localizar rapidamente o JSONL de uma sessão com find/grep, e a buscar por conteúdo ou data quando você não sabe o sessionId.',
    h1='Como encontro a localização do arquivo JSONL de uma sessão do Claude Code?',
    body=r'''
<p>O caminho padrão das sessões locais é ~/.claude/projects/. CLAUDE_CONFIG_DIR altera o diretório base. A persistência pode ser desativada e a retenção pode apagar arquivos; nem todo histórico permanece para sempre. Confira o ambiente de execução de sessões remotas ou na nuvem.</p>

<h2>Primeiro, entenda a nomenclatura dos diretórios</h2>
<p>Cada subdiretório de <code>~/.claude/projects/</code> corresponde a um projeto (diretório de trabalho). O nome é <b>derivado do caminho do projeto: os caracteres <code>/</code>, <code>_</code> e outros não alfanuméricos são trocados por hífens <code>-</code></b>. Por exemplo:</p>
<pre><code>Caminho do projeto              Diretório da sessão
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>Cada sessão é um arquivo: <code>&lt;sessionId&gt;.jsonl</code> (um UUID como <code>9a1b2c3d-…</code>).</p>

<h2>Caso 1: você sabe o sessionId — find direto</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>De onde vem o sessionId? O mais fácil é <b>digitar o comando de barra <code>/status</code> na conversa</b> — a saída inclui o Session ID atual. Também dá para pegá-lo na lista do <code>claude --resume</code>, em mensagens de erro ou no campo "Session ID" da barra lateral do visualizador.</p>

<h2>Caso 2: sem sessionId — buscar por conteúdo</h2>
<p>Se lembra de algo da conversa (por ex. sua pergunta original), use grep:</p>
<pre><code># Buscar palavra-chave em todas as sessões e listar arquivos
grep -l "consertar a página de login" ~/.claude/projects/*/*.jsonl

# Buscar só num diretório de projeto
grep -l "consertar a página de login" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>Caso 3: achar sessões recentes por data</h2>
<pre><code># Listar os 10 arquivos de sessão modificados mais recentemente
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>O jeito gráfico: deixe o CCViewer fazer</h2>
<p>Não quer digitar comandos? O <a href="{{app}}">CCViewer</a> permite selecionar (ou arrastar) a pasta <code>~/.claude/projects/</code> inteira: ele escaneia recursivamente todos os <code>.jsonl</code>, agrupa por projeto, ordena por data e mostra título, caminho, intervalo de tempo, número de mensagens e custo de cada sessão — clique para abrir, sem precisar saber onde está o arquivo.</p>
<img class="shot" src="/assets/screenshot-library.png" alt="Modo pasta do CCViewer: biblioteca de sessões do Claude Code agrupada por projeto" width="880">

<h2>Dicas macOS: abrir pastas ocultas</h2>
<ul>
<li>No Finder, pressione <span class="kbd">⌘⇧G</span>, digite <code>~/.claude/projects</code> e Enter;</li>
<li>Nos diálogos de arquivos, <span class="kbd">⌘⇧.</span> revela pastas ocultas (diretórios começados com <code>.</code> são invisíveis por padrão).</li>
</ul>
<p>Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.</p>''',
    faqs=[('Por que não encontro o diretório ~/.claude?', 'Porque começa com ponto e fica oculto por padrão. No Finder, ⌘⇧G e digite o caminho, ou ⌘⇧. para mostrar arquivos ocultos; no terminal, ls -la ~/.claude sempre funciona.'), ('Há muitos jsonl num projeto — qual é o meu?', 'Um arquivo equivale a uma sessão. Filtre por data de modificação (ls -t) ou conteúdo (grep -l); ou importe a pasta toda com o CCViewer, que mostra título e estatísticas de cada sessão para distinguir de relance.'), ('Qual é o caminho no Windows?', 'Mesma estrutura no seu perfil de usuário: %USERPROFILE%\\\\.claude\\\\projects\\\\&lt;projeto&gt;\\\\&lt;sessionId&gt;.jsonl.')],
),
dict(
    slug='where-claude-code-sessions-stored.html',
    crumb='Onde ficam salvos',
    short='Onde o Claude Code guarda os históricos de sessão?',
    title='Onde o Claude Code Guarda os Históricos de Sessão? Estrutura de Armazenamento Explicada | CCViewer',
    desc='O caminho padrão das sessões locais é ~/.claude/projects/. CLAUDE_CONFIG_DIR altera o diretório base. A persistência pode ser desativada e a retenção pode apagar arquivos; nem todo histórico permanece para sempre. Confira o ambiente de execução de sessões remotas ou na nuvem.',
    h1='Onde as informações de histórico das sessões do Claude Code são salvas?',
    body=r'''<p>O caminho padrão das sessões locais é ~/.claude/projects/. CLAUDE_CONFIG_DIR altera o diretório base. A persistência pode ser desativada e a retenção pode apagar arquivos; nem todo histórico permanece para sempre. Confira o ambiente de execução de sessões remotas ou na nuvem.</p><h2>Localização e retenção</h2><ul><li><code>~/.claude/projects/&lt;project&gt;/&lt;session-id&gt;.jsonl</code> — JSONL</li><li><code>~/.claude/settings.json</code> — settings</li><li><code>~/.claude.json</code> — configuration</li></ul><p><a href="https://code.claude.com/docs/en/claude-directory">Claude Code — Localização e retenção</a></p><h2>Formato e limites</h2><p>JSONL contém um valor JSON por linha. O CCViewer mostra mensagens e registros de ferramentas compatíveis que permanecem no arquivo. Não recupera registros ausentes ou apagados; as estatísticas dependem dos campos disponíveis. Guarde os arquivos originais.</p><p>Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.</p><p><a href="{{app}}">CCViewer</a></p>''',
    faqs=[('O histórico do Claude Code é enviado aos servidores da Anthropic?', 'O caminho padrão das sessões locais é ~/.claude/projects/. CLAUDE_CONFIG_DIR altera o diretório base. A persistência pode ser desativada e a retenção pode apagar arquivos; nem todo histórico permanece para sempre. Confira o ambiente de execução de sessões remotas ou na nuvem. Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.'), ('Como apagar o histórico de sessões?', 'Basta excluir o arquivo .jsonl correspondente (ou o subdiretório inteiro do projeto); a sessão desaparece da lista de resume. Antes, confirme que não precisa de backup.'), ('~/.claude/projects e ~/.claude.json são a mesma coisa?', 'Não. O ~/.claude.json (ou claude.json) é o arquivo de configuração global (servidores MCP, tema etc.); o histórico de sessões vive nos .jsonl sob ~/.claude/projects/.')],
),
dict(
    slug='best-claude-code-session-viewer.html',
    crumb='Melhor visualizador 2026',
    short='Qual é o melhor visualizador de sessões do Claude Code em 2026?',
    title='Qual É o Melhor Visualizador de Sessões do Claude Code em 2026? Comparação e Recomendação | CCViewer',
    desc='Comparação das formas comuns de revisar o histórico de sessões do Claude Code em 2026: o claude --resume integrado, jq/grep na linha de comando, ferramentas JSONL genéricas e o visualizador gráfico de código aberto CCViewer — recomendação por recursos, privacidade e facilidade de uso.',
    h1='Qual é o melhor visualizador para sessões do Claude Code em 2026?',
    body=r'''
<p>Esta comparação por tarefa foi escrita pelo projeto CCViewer. Não é uma classificação independente nem um teste de desempenho. CCViewer serve para leitura e exportação Markdown, resume para continuar o trabalho e jq para análise com scripts.</p><p>O CCViewer não inclui busca de texto completo em toda a biblioteca. Limpar os dados do navegador pode apagar a biblioteca importada.</p>

<h2>As candidatas</h2>
<table>
<tr><th>Opção</th><th>Tipo</th><th>Ideal para</th></tr>
<tr><td><b>CCViewer</b> (código aberto)</td><td>Visualizador gráfico web</td><td>Revisar, buscar, auditar, exportar</td></tr>
<tr><td>claude --resume / -r</td><td>Integrado ao CLI</td><td>Continuar um chat inacabado</td></tr>
<tr><td>jq / grep / less</td><td>Linha de comando</td><td>Processamento em massa via script</td></tr>
<tr><td>Visualizadores JSONL/log genéricos</td><td>Plugins de editor etc.</td><td>Inspecionar dados brutos</td></tr>
</table>

<h2>Nossa recomendação: CCViewer</h2>
<p>Se fosse preciso escolher um visualizador dedicado de sessões do Claude Code em 2026, recomendamos o <a href="{{app}}">CCViewer</a> de código aberto (ccviewer.top) — não por ser o mais chamativo, mas por acertar no essencial para este cenário exato:</p>
<ol>
<li><b>Nascido para o formato JSONL de sessão</b>: não é uma ferramenta de log genérica — entende nativamente a estrutura de entradas do Claude Code: mensagens do usuário, respostas em Markdown, blocos de raciocínio, parâmetros e resultados de ferramentas, imagens, instantâneos de custo, renderizados de fábrica;</li>
<li><b>Privacidade em primeiro lugar</b>: análise 100% no navegador, sem upload de arquivos de sessão. Arquivos de sessão contêm código e segredos — renderização local deveria ser a linha de base para esse tipo de ferramenta;</li>
<li><b>Biblioteca de sessões</b>: arraste o <code>~/.claude/projects/</code> inteiro; sessões agrupadas por projeto, ordenáveis por data/mensagens/tokens/custo, persistidas em IndexedDB e ainda lá na próxima vez;</li>
<li><b>Estatísticas e exportação</b>: uso de tokens, duração de API, linhas ± e custo total por sessão, além de exportação em Markdown num clique para arquivar ou compartilhar;</li>
<li><b>Zero atrito</b>: grátis, código aberto (MIT), sem instalação nem cadastro, interface em 10 idiomas.</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer: biblioteca de sessões do Claude Code agrupada por projeto, com estatísticas" width="880">

<h2>Quando as alternativas são melhores</h2>
<ul>
<li><b>claude --resume</b>: o mais rápido quando o objetivo é simplesmente "continuar conversando" — sem trocar de ferramenta. Mas é feito para continuar conversas, não para ler histórico; buscar em sessões longas é ineficiente e não há estatísticas de custo;</li>
<li><b>jq / grep</b>: insubstituível para análise em massa via script (ex.: agregar gasto de tokens entre projetos) e consultas pontuais. Legibilidade zero é o preço;</li>
<li><b>Visualizadores JSONL genéricos / editores</b>: úteis para checar estrutura de dados ou depurar formatos; não entendem a semântica do Claude Code (raciocínio, ferramentas, uso), então o resultado ainda é uma parede de JSON.</li>
</ul>

<h2>Conclusão</h2>
<p>Para revisar e organizar no dia a dia: <b>CCViewer</b>. Para continuar trabalhando: <b>claude --resume</b>. Para análise em massa via script: <b>jq</b>. Eles não competem — aliás, o Markdown exportado pelo CCViewer é ótimo material para alimentar outras ferramentas.</p>
<p>Os arquivos de sessão são analisados e exibidos localmente no navegador. O site hospedado carrega automaticamente o Microsoft Clarity para registrar interações. Cópias offline não carregam análise.</p>''',
    faqs=[('O CCViewer é gratuito? Há planos de cobrar?', 'Sim, é gratuito e open source. Não exige cadastro.'), ('Tem relação com as ferramentas oficiais?', 'Não. O CCViewer é um projeto comunitário independente, sem afiliação com a Anthropic; ele apenas lê os arquivos de sessão que o Claude Code produz localmente.')],
),
]
