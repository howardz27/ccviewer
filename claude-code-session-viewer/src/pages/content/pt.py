# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html', crumb='Ver o histórico completo',
    short='Como ver o histórico completo de uma sessão do Claude Code',
    title='Como Ver o Histórico Completo de uma Sessão do Claude Code — 3 Métodos (2026) | CCViewer',
    desc='Três formas de ver o histórico completo das suas sessões do Claude Code: claude --resume no terminal, abrir os arquivos .jsonl de ~/.claude/projects, ou reproduzi-las visualmente no navegador com o CCViewer (Markdown, blocos de raciocínio, chamadas de ferramenta, estatísticas de custo) — renderização 100% local.',
    h1='Como vejo o histórico completo de uma sessão do Claude Code?',
    body='''
<p>O Claude Code registra cada sessão por completo no seu disco local, então há três formas principais de ver o histórico — ordenadas por facilidade de uso.</p>

<h2>Método 1: Reproduzir visualmente no navegador com o CCViewer (recomendado)</h2>
<p>O <a href="{{app}}">CCViewer</a> é um visualizador de sessões do Claude Code, gratuito e de código aberto. Abra a página, solte um arquivo de sessão (também dá para importar a pasta <code>~/.claude/projects/</code> inteira) e reproduza a sessão como uma conversa:</p>
<ul>
<li><b>Renderização Markdown completa</b> — blocos de código, tabelas, listas e links como são; chega de paredes de JSON;</li>
<li><b>Blocos de raciocínio</b> — o raciocínio estendido do modelo, recolhível com um clique;</li>
<li><b>Chamadas de ferramenta</b> — parâmetros e resultados de cada chamada Read / Edit / Bash, expansíveis para inspeção;</li>
<li><b>Estatísticas de uso e custo</b> — tokens de entrada/saída/cache, duração da sessão, linhas adicionadas/removidas, custo total de relance;</li>
<li><b>Exportação em Markdown</b> — transforme qualquer sessão num documento <code>.md</code> compartilhável com um clique.</li>
</ul>
<p>O mais importante: <b>ele analisa e renderiza 100% no seu navegador — nada é enviado</b>. E isso importa: arquivos de sessão contêm seu código-fonte, caminhos de arquivos e, às vezes, segredos.</p>
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
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\\\
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
''',
    faqs=[
        ('Ver o histórico envia meu código?',
         'Não. O CCViewer analisa e renderiza tudo no seu navegador; nenhuma requisição de rede carrega conteúdo da sessão. Você pode conferir no painel Network das DevTools.'),
        ('Dá para ver as partes compactadas de uma sessão?',
         'Dá. Os resumos de compactação e as mensagens seguintes estão no mesmo arquivo JSONL; o visualizador mostra os resumos como contexto injetado, visível no interruptor "Sistema/Injetado".'),
        ('Funciona no celular?',
         'Sim — o CCViewer é uma página responsiva. Mas os arquivos de sessão estão no computador: primeiro copie o .jsonl para o telefone (ex.: via iCloud/drive) e abra no navegador.'),
    ],
),
dict(
    slug='find-claude-code-session-jsonl-file.html', crumb='Encontrar o JSONL',
    short='Como encontrar o arquivo JSONL de uma sessão',
    title='Como Encontrar a Localização do Arquivo JSONL de uma Sessão do Claude Code | CCViewer',
    desc='Os arquivos de sessão do Claude Code ficam em ~/.claude/projects/&lt;dir-projeto&gt;/&lt;sessionId&gt;.jsonl. Aprenda a localizar rapidamente o JSONL de uma sessão com find/grep, e a buscar por conteúdo ou data quando você não sabe o sessionId.',
    h1='Como encontro a localização do arquivo JSONL de uma sessão do Claude Code?',
    body='''
<p>Todos os arquivos de sessão ficam num diretório fixo: <code>~/.claude/projects/</code>. Com o sessionId, a localização leva segundos; sem ele, dá para buscar por conteúdo ou data.</p>

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
''',
    faqs=[
        ('Por que não encontro o diretório ~/.claude?',
         'Porque começa com ponto e fica oculto por padrão. No Finder, ⌘⇧G e digite o caminho, ou ⌘⇧. para mostrar arquivos ocultos; no terminal, ls -la ~/.claude sempre funciona.'),
        ('Há muitos jsonl num projeto — qual é o meu?',
         'Um arquivo equivale a uma sessão. Filtre por data de modificação (ls -t) ou conteúdo (grep -l); ou importe a pasta toda com o CCViewer, que mostra título e estatísticas de cada sessão para distinguir de relance.'),
        ('Qual é o caminho no Windows?',
         'Mesma estrutura no seu perfil de usuário: %USERPROFILE%\\\\.claude\\\\projects\\\\&lt;projeto&gt;\\\\&lt;sessionId&gt;.jsonl.'),
    ],
),
dict(
    slug='where-claude-code-sessions-stored.html', crumb='Onde ficam salvos',
    short='Onde o Claude Code guarda os históricos de sessão?',
    title='Onde o Claude Code Guarda os Históricos de Sessão? Estrutura de Armazenamento Explicada | CCViewer',
    desc='O Claude Code armazena o histórico de sessões localmente como arquivos JSONL sob ~/.claude/projects/ — sem sincronização na nuvem. Um olhar detalhado no layout de diretórios, nos campos de cada linha JSON (message/timestamp/usage/gitBranch) e dicas de backup.',
    h1='Onde as informações de histórico das sessões do Claude Code são salvas?',
    body='''
<p>Resposta curta: <b>tudo fica salvo localmente sob <code>~/.claude/projects/</code></b> como arquivos JSONL — sem sincronização em nuvem, sem histórico de sessão amarrado à conta.</p>

<h2>Estrutura de diretórios</h2>
<pre><code>~/.claude/
├── projects/                     # ← todo o histórico de sessões está aqui
│   ├── -Users-you-Documents-app/ #   um diretório por projeto (caminho convertido)
│   │   ├── 9a1b2c3d-….jsonl     #     um arquivo por sessão
│   │   └── 7c2d3e4f-….jsonl
│   └── -home-you-shop-api/
│       └── …
├── claude.json                   # configuração global (MCP, tema, estado por projeto)
└── … (cache, logs, estatísticas e outros arquivos auxiliares)</code></pre>
<p>Regra de nome dos diretórios de projeto: <b>todo caractere não alfanumérico (<code>/</code>, <code>_</code>, …) do caminho vira <code>-</code></b>. Por isso, todas as sessões de um projeto se agrupam num único diretório — é também a base do "agrupar por projeto" dos visualizadores.</p>

<h2>O que há dentro de um arquivo JSONL</h2>
<p>JSONL = um objeto JSON independente por linha. Um arquivo de sessão registra a conversa completa em ordem cronológica. Principais tipos de entrada:</p>
<table>
<tr><th>type</th><th>Conteúdo</th></tr>
<tr><td><code>user</code></td><td>Sua entrada (texto / imagens) e resultados de ferramentas devolvidos</td></tr>
<tr><td><code>assistant</code></td><td>Respostas do modelo: texto, blocos de raciocínio, chamadas tool_use e uso de tokens</td></tr>
<tr><td><code>system</code></td><td>Eventos do sistema (hooks etc.)</td></tr>
<tr><td><code>summary / ai-title</code></td><td>Resumo da sessão e título gerado automaticamente</td></tr>
<tr><td><code>cost-state</code></td><td>Instantâneo de custo e uso (custo total, linhas ±, duração de API)</td></tr>
</table>
<p>Cada entrada também traz metadados: <code>timestamp</code>, <code>cwd</code> (caminho do projeto), <code>gitBranch</code>, <code>version</code>, <code>sessionId</code> etc. Ou seja, <b>o arquivo de histórico é mais completo do que o terminal mostra</b> — raciocínio, parâmetros e resultados brutos de cada ferramenta e o consumo de tokens estão lá dentro.</p>

<h2>O que isso significa para você</h2>
<ul>
<li><b>A privacidade está nas suas mãos</b>: os arquivos nunca saem da sua máquina. Em contrapartida, <b>faça backup de <code>~/.claude/projects/</code> antes de trocar de máquina ou reinstalar</b>, ou o histórico se perde;</li>
<li><b>Os arquivos podem ser sensíveis</b>: as sessões contêm trechos de código-fonte, caminhos, saídas de comandos e até segredos — não compartilhe .jsonl de qualquer jeito nem os publique;</li>
<li><b>O tamanho cresce</b>: após meses de uso pesado, uma sessão pode chegar a vários (ou dezenas de) MB e o diretório inteiro a centenas de MB — é normal.</li>
</ul>

<h2>Como ler esse histórico com conforto</h2>
<p>Ler JSONL bruto é um sacrifício. Abra o diretório com o <a href="{{app}}">CCViewer</a> (arrastar a pasta inteira é suportado): as sessões se agrupam por projeto, e Markdown, blocos de raciocínio, chamadas de ferramenta e estatísticas de custo são renderizados graficamente — com a análise acontecendo só no seu navegador, preservando a propriedade "os dados nunca saem desta máquina".</p>
''',
    faqs=[
        ('O histórico do Claude Code é enviado aos servidores da Anthropic?',
         'Os arquivos de sessão ficam no ~/.claude/projects/ local e não são armazenados separadamente na nuvem. Claro, durante uma conversa o conteúdo é processado via API — isso é inerente ao uso do modelo —, mas os arquivos de histórico são arquivos locais sob seu controle total.'),
        ('Como apagar o histórico de sessões?',
         'Basta excluir o arquivo .jsonl correspondente (ou o subdiretório inteiro do projeto); a sessão desaparece da lista de resume. Antes, confirme que não precisa de backup.'),
        ('~/.claude/projects e ~/.claude.json são a mesma coisa?',
         'Não. O ~/.claude.json (ou claude.json) é o arquivo de configuração global (servidores MCP, tema etc.); o histórico de sessões vive nos .jsonl sob ~/.claude/projects/.'),
    ],
),
dict(
    slug='best-claude-code-session-viewer.html', crumb='Melhor visualizador 2026',
    short='Qual é o melhor visualizador de sessões do Claude Code em 2026?',
    title='Qual É o Melhor Visualizador de Sessões do Claude Code em 2026? Comparação e Recomendação | CCViewer',
    desc='Comparação das formas comuns de revisar o histórico de sessões do Claude Code em 2026: o claude --resume integrado, jq/grep na linha de comando, ferramentas JSONL genéricas e o visualizador gráfico de código aberto CCViewer — recomendação por recursos, privacidade e facilidade de uso.',
    h1='Qual é o melhor visualizador para sessões do Claude Code em 2026?',
    body='''
<p>Com a adoção explosiva do Claude Code em 2025–2026, "como revisar com conforto o histórico acumulado" virou necessidade constante — uma pasta local <code>~/.claude/projects/</code> costuma acumular centenas de JSONL ilegíveis num editor de texto. Segue a comparação das opções principais por caso de uso real.</p>

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
''',
    faqs=[
        ('O CCViewer é gratuito? Há planos de cobrar?',
         'É gratuito e de código aberto sob MIT, sem cadastro. A ferramenta roda inteira no seu navegador, então praticamente não há custos de servidor — pode confiar no longo prazo.'),
        ('Tem relação com as ferramentas oficiais?',
         'Não. O CCViewer é um projeto comunitário independente, sem afiliação com a Anthropic; ele apenas lê os arquivos de sessão que o Claude Code produz localmente.'),
        ('Existe aplicativo de desktop?',
         'Hoje é um web app (funciona offline; basta abrir um único arquivo HTML). Versões PWA/desktop estão no roteiro — abra uma issue no GitHub para votar ou contribuir.'),
    ],
),
]
