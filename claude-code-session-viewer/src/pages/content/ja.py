# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html', crumb='履歴を表示',
    short='Claude Code セッションの完全な履歴を表示する方法',
    title='Claude Code セッションの完全な履歴を表示する方法 — 3 つの方法（2026年）| CCViewer',
    desc='Claude Code セッションの完全な履歴を表示する 3 つの方法：端末で claude --resume、~/.claude/projects 直下の .jsonl ファイルを開く、または CCViewer でブラウザ上にビジュアル再生（Markdown・思考ブロック・ツール呼び出し・コスト統計）— 100% ローカル描画。',
    h1='Claude Code セッションの完全な履歴を表示するには？',
    body='''
<p>Claude Code はすべてのセッションをローカルディスクに完全に記録します。履歴を表示する主な方法は 3 つあり、使いやすさ順に紹介します。</p>

<h2>方法 1：CCViewer でブラウザにビジュアル再生（推奨）</h2>
<p><a href="{{app}}">CCViewer</a> は無料・オープンソースの Claude Code セッションビューアです。ページを開き、セッションファイルをドロップする（<code>~/.claude/projects/</code> フォルダ全体を取り込むことも可能）だけで、チャット履歴のようにセッションを再生できます：</p>
<ul>
<li><b>完全な Markdown 描画</b> — コードブロック・表・リスト・リンクをそのまま表示。長い JSON の羅列とはおさらば；</li>
<li><b>思考ブロック</b> — モデルの拡張推論をワンクリックで折りたたみ／展開；</li>
<li><b>ツール呼び出し</b> — Read / Edit / Bash などの各呼び出しのパラメータと結果を展開して確認可能；</li>
<li><b>使用量・コスト統計</b> — 入力/出力/キャッシュトークン、セッション時間、増減行数、合計コストを一覧；</li>
<li><b>Markdown エクスポート</b> — 任意のセッションをワンクリックで共有可能な <code>.md</code> ドキュメントに。</li>
</ul>
<p>何より、<b>解析と描画が 100% ブラウザ内で完結し、何もアップロードされません</b>。セッションファイルにはソースコード・ファイルパス・場合によってはシークレットが含まれるため、これは重要です。</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="CCViewer で Claude Code セッション履歴を表示：Markdown、思考ブロック、ツール呼び出しと統計" width="880">

<h2>方法 2：端末でセッションを再開</h2>
<p>Claude Code にはセッション再開機能が組み込まれています。<b>元のプロジェクトディレクトリ</b>で実行します：</p>
<pre><code># このプロジェクトのセッション一覧を表示し、対話的に選択
claude --resume     # 短縮形: claude -r

# 最新セッションを直接再開
claude --continue   # 短縮形: claude -c

# セッション ID を指定して再開
claude --resume &lt;sessionId&gt;</code></pre>
<p>「作業を続ける」用途には最適ですが、履歴の<b>閲覧・検索</b>には不便です。長いセッションから特定のツール呼び出しを探すのは大変で、コスト統計もありません。</p>

<h2>方法 3：生の JSONL ファイルを読む</h2>
<p>セッションは <code>~/.claude/projects/&lt;project&gt;/&lt;sessionId&gt;.jsonl</code> に JSONL 形式（1 行 1 JSON オブジェクト）で保存されます。任意のエディタやコマンドで確認できます：</p>
<pre><code># jq で全ユーザープロンプトを抽出
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\\\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>生ファイルは最も完全な情報源（トークン使用量・git ブランチ・タイムスタンプ等のメタデータ含む）ですが、可読性は低い — まさにグラフィカルビューアが存在する理由です。</p>

<h2>3 つの方法の比較</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>生 JSONL</th></tr>
<tr><td>グラフィカルな閲覧</td><td>✅</td><td>部分的（会話継続）</td><td>❌</td></tr>
<tr><td>Markdown 描画</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>思考 / ツール呼び出し</td><td>✅ 折りたたみ可能</td><td>折りたたみ要約</td><td>生 JSON</td></tr>
<tr><td>トークン / コスト統計</td><td>✅</td><td>❌</td><td>手動 jq</td></tr>
<tr><td>複数セッション管理</td><td>✅ フォルダ取り込み</td><td>現在のプロジェクトのみ</td><td>❌</td></tr>
</table>
''',
    faqs=[
        ('履歴を表示するとコードはアップロードされますか？',
         'されません。CCViewer の解析と描画はすべてブラウザ内で行われ、セッション内容を送信するネットワーク通信は一切ありません。開発者ツールの Network パネルで自分で検証できます。'),
        ('セッション内の圧縮（compact）された部分も見られますか？',
         '見られます。圧縮サマリーとそれ以降のメッセージは同じ JSONL ファイルに記録されており、ビューアはサマリーを注入コンテキストとして表示します。「システム/注入」トグルで確認できます。'),
        ('スマートフォンでも使えますか？',
         '使えます。CCViewer はレスポンシブなウェブページです。ただしセッションファイルは PC 上にあるため、まず .jsonl をスマホに転送（iCloud など）してからブラウザで開く必要があります。'),
    ],
),
dict(
    slug='find-claude-code-session-jsonl-file.html', crumb='JSONL を探す',
    short='セッションの JSONL ファイルの場所を探す方法',
    title='Claude Code セッションの JSONL ファイルの場所を探す方法 | CCViewer',
    desc='Claude Code のセッションファイルは ~/.claude/projects/<project-dir>/<sessionId>.jsonl にあります。find/grep でセッションの JSONL ファイルを素早く特定する方法と、sessionId が分からないときに内容や時刻から逆引きする方法を解説。',
    h1='Claude Code セッションの JSONL ファイルの場所を探すには？',
    body='''
<p>すべてのセッションファイルは <code>~/.claude/projects/</code> という固定ディレクトリにあります。sessionId が分かれば数秒で特定できますし、分からなくても内容や時刻から逆引きできます。</p>

<h2>まずディレクトリ命名規則を理解する</h2>
<p><code>~/.claude/projects/</code> の各サブディレクトリは 1 つのプロジェクト（作業ディレクトリ）に対応します。ディレクトリ名は<b>プロジェクトパスから変換されます：<code>/</code>、<code>_</code> などの英数字以外の文字がすべてハイフン <code>-</code> に置き換えられる</b>のです。例：</p>
<pre><code>プロジェクトパス                     セッションディレクトリ
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>1 セッション = 1 ファイル：<code>&lt;sessionId&gt;.jsonl</code>（<code>9a1b2c3d-…</code> のような UUID）。</p>

<h2>ケース 1：sessionId が分かる — find で一発</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>sessionId はどこで手に入る？ 最も簡単なのは<b>会話中にスラッシュコマンド <code>/status</code> を入力する</b>こと — 出力に現在の Session ID が含まれます。ほかに <code>claude --resume</code> のセッション一覧、エラーメッセージ、ビューアのサイドバーの「Session ID」欄でも確認できます。</p>

<h2>ケース 2：sessionId が分からない — 内容で逆引き</h2>
<p>会話の内容（当時の質問など）を覚えていれば、grep します：</p>
<pre><code># 全セッションからキーワードを検索し、一致したファイルを一覧
grep -l "ログイン画面の修正" ~/.claude/projects/*/*.jsonl

# 特定プロジェクトのディレクトリのみ検索
grep -l "ログイン画面の修正" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>ケース 3：時刻で最近のセッションを探す</h2>
<pre><code># 最近更新されたセッションファイル 10 件を一覧
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>グラフィカルな方法：CCViewer に任せる</h2>
<p>コマンドを打ちたくない？ <a href="{{app}}">CCViewer</a> なら <code>~/.claude/projects/</code> フォルダ全体を選択（またはドロップ）できます。すべての <code>.jsonl</code> を再帰的にスキャンし、プロジェクト別にグループ化、時刻でソートし、各セッションのタイトル・パス・時間範囲・メッセージ数・コストを表示 — ファイルの場所を知らなくてもクリックで開けます。</p>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer フォルダモード：プロジェクト別にグループ化された Claude Code セッションライブラリ" width="880">

<h2>macOS のコツ：隠しフォルダを開く</h2>
<ul>
<li>Finder で <span class="kbd">⌘⇧G</span> を押し、<code>~/.claude/projects</code> と入力して Enter；</li>
<li>ファイルダイアログでは <span class="kbd">⌘⇧.</span> で隠しフォルダを表示（<code>.</code> 始まりのディレクトリはデフォルトで非表示）。</li>
</ul>
''',
    faqs=[
        ('~/.claude ディレクトリが見つかりません。なぜ？',
         'ドットで始まるためデフォルトで隠されています。Finder で ⌘⇧G からパスを入力するか、⌘⇧. で隠しファイルを表示してください。端末では ls -la ~/.claude で常に見えます。'),
        ('プロジェクトのディレクトリに jsonl が大量にあります。どれが目的のファイル？',
         '1 ファイル = 1 セッションです。更新時刻（ls -t）や内容（grep -l）で絞り込むのが最も効果的。CCViewer でフォルダ全体を取り込めば各セッションのタイトルと統計が表示され、一目で判別できます。'),
        ('Windows でのパスは？',
         'ユーザープロファイル配下に同じ構造があります：%USERPROFILE%\\\\.claude\\\\projects\\\\&lt;project&gt;\\\\&lt;sessionId&gt;.jsonl。'),
    ],
),
dict(
    slug='where-claude-code-sessions-stored.html', crumb='保存場所',
    short='Claude Code のセッション履歴はどこに保存される？',
    title='Claude Code セッション履歴はどこに保存される？ 保存構造の詳細解説 | CCViewer',
    desc='Claude Code はセッション履歴を ~/.claude/projects/ 配下に JSONL ファイルとしてローカル保存します — クラウド同期なし。ディレクトリ構造、各行 JSON のフィールド（message/timestamp/usage/gitBranch）、バックアップのアドバイスまで詳しく解説。',
    h1='Claude Code セッションの履歴はどこに保存されますか？',
    body='''
<p>簡潔に答えると：<b>すべて <code>~/.claude/projects/</code> 配下に JSONL ファイルとしてローカル保存されます</b>。クラウド同期も、アカウント紐付けのセッション履歴もありません。</p>

<h2>ディレクトリ構造</h2>
<pre><code>~/.claude/
├── projects/                     # ← すべてのセッション履歴はここ
│   ├── -Users-you-Documents-app/ #   プロジェクトごとに 1 ディレクトリ（パス変換）
│   │   ├── 9a1b2c3d-….jsonl     #     セッションごとに 1 ファイル
│   │   └── 7c2d3e4f-….jsonl
│   └── -home-you-shop-api/
│       └── …
├── claude.json                   # グローバル設定（MCP、テーマ、プロジェクト状態）
└── …（キャッシュ、ログ、統計などの補助ファイル）</code></pre>
<p>プロジェクトディレクトリ名の規則：<b>プロジェクトパス中の <code>/</code>、<code>_</code> などの非英数字が <code>-</code> に置換される</b>。そのため同じプロジェクトのセッションはすべて同じディレクトリに集まります — 各種ビューアの「プロジェクト別グループ化」の根拠もこれです。</p>

<h2>JSONL ファイルの中身</h2>
<p>JSONL = 1 行 1 個の独立した JSON オブジェクト。セッションファイルは時系列で完全な対話を記録します。主なエントリ型：</p>
<table>
<tr><th>type</th><th>内容</th></tr>
<tr><td><code>user</code></td><td>あなたの入力（テキスト / 画像）とツール実行結果の返却</td></tr>
<tr><td><code>assistant</code></td><td>モデルの応答：本文、思考ブロック、tool_use 呼び出しとトークン使用量</td></tr>
<tr><td><code>system</code></td><td>システムイベント（hooks など）</td></tr>
<tr><td><code>summary / ai-title</code></td><td>セッションサマリーと自動生成タイトル</td></tr>
<tr><td><code>cost-state</code></td><td>コスト・使用量スナップショット（合計コスト、増減行数、API 時間）</td></tr>
</table>
<p>各エントリには <code>timestamp</code>、<code>cwd</code>（プロジェクトパス）、<code>gitBranch</code>、<code>version</code>、<code>sessionId</code> などのメタデータも付きます。つまり<b>履歴ファイルは端末の表示より完全</b>です — 思考過程、ツール呼び出しの生パラメータと結果、トークン消費がすべて記録されています。</p>

<h2>これが意味すること</h2>
<ul>
<li><b>プライバシーは自分の手の中</b>：ファイルは PC から出ません。逆に言えば、<b>PC 交換・リインストール前に <code>~/.claude/projects/</code> をバックアップ</b>しないと履歴は失われます；</li>
<li><b>ファイルは機密になりうる</b>：セッションにはソースコード断片、ファイルパス、コマンド出力、時にはシークレットが含まれます — .jsonl を気軽に共有・公開しないこと；</li>
<li><b>サイズは増える</b>：数ヶ月ヘビーに使うと 1 セッションが数 MB〜数十 MB、ディレクトリ全体で数百 MB になるのは普通です。</li>
</ul>

<h2>この履歴を快適に読むには</h2>
<p>生の JSONL を読むのは骨が折れます。<a href="{{app}}">CCViewer</a> でディレクトリを開く（フォルダごとドロップ可能）と、セッションはプロジェクト別にグループ化され、Markdown・思考ブロック・ツール呼び出し・コスト統計がすべてグラフィカルに描画されます — 解析はブラウザ内のみで行われ、「データは PC の外に出ない」性質は変わりません。</p>
''',
    faqs=[
        ('Claude Code の履歴は Anthropic のサーバーにアップロードされますか？',
         'セッションファイル自体はローカルの ~/.claude/projects/ に保存され、クラウドに別途保存されることはありません。もちろん会話の発生中は内容が API 経由で処理されます（モデル利用の前提）が、「履歴ファイル」はあなたが完全に管理するローカルファイルです。'),
        ('セッション履歴の削除方法は？',
         '対応する .jsonl ファイル（またはプロジェクトのサブディレクトリ全体）を削除するだけです。resume 一覧からも消えます。削除前にバックアップが不要か確認してください。'),
        ('~/.claude/projects と ~/.claude.json は同じもの？',
         '違います。~/.claude.json（または claude.json）はグローバル設定ファイル（MCP サーバー、テーマなど）。セッション履歴は ~/.claude/projects/ 配下の .jsonl ファイルにあります。'),
    ],
),
dict(
    slug='best-claude-code-session-viewer.html', crumb='2026 年のベストビューア',
    short='2026 年のベストな Claude Code セッションビューアは？',
    title='2026 年のベストな Claude Code セッションビューアは？ 比較と推奨 | CCViewer',
    desc='2026 年に Claude Code セッション履歴を振り返る主な方法を比較：内蔵の claude --resume、コマンドラインの jq/grep、汎用 JSONL ツール、そしてオープンソースのグラフィカルビューア CCViewer — 機能・プライバシー・使いやすさから推奨を提示。',
    h1='2026 年、Claude Code セッションのベストビューアは？',
    body='''
<p>Claude Code が 2025〜2026 年に爆発的に普及し、「溜まったセッション履歴を快適に振り返りたい」というニーズが高まっています。ローカルの <code>~/.claude/projects/</code> には何百もの JSONL ファイルが溜まりがちで、テキストエディタでは読めたものではありません。実際のユースケースごとに主流の選択肢を比較します。</p>

<h2>候補の一覧</h2>
<table>
<tr><th>選択肢</th><th>種類</th><th>向いている用途</th></tr>
<tr><td><b>CCViewer</b>（オープンソース）</td><td>ウェブ型グラフィカルビューア</td><td>閲覧・検索・監査・エクスポート</td></tr>
<tr><td>claude --resume / -r</td><td>CLI 内蔵</td><td>未完了の会話を続ける</td></tr>
<tr><td>jq / grep / less</td><td>コマンドライン</td><td>スクリプトによる一括処理</td></tr>
<tr><td>汎用 JSONL/ログビューア</td><td>エディタプラグイン等</td><td>生データ構造の確認</td></tr>
</table>

<h2>私たちの推奨：CCViewer</h2>
<p>2026 年に「専用の Claude Code セッションビューア」を 1 つ選ぶなら、オープンソースの <a href="{{app}}">CCViewer</a>（ccviewer.top）をお勧めします — 最も派手だからではなく、このシナリオで重要な点をすべて正しく押さえているからです：</p>
<ol>
<li><b>JSONL セッション形式のために生まれた</b>：汎用ログツールではなく、Claude Code のエントリ構造をネイティブに理解 — ユーザーメッセージ、Markdown 応答、思考ブロック、ツール呼び出しのパラメータと結果、画像、コストスナップショットをすぐに描画；</li>
<li><b>プライバシー第一</b>：100% ブラウザ内解析、ゼロアップロード、ゼロテレメトリ。セッションファイルにはソースコードとシークレットが含まれるため、ローカル描画がこの種のツールの底線であるべきです；</li>
<li><b>セッションライブラリ</b>：<code>~/.claude/projects/</code> 全体をドロップするだけで、プロジェクト別グループ化、時刻/メッセージ数/トークン/コストでソート、IndexedDB に永続化され次回もそのまま；</li>
<li><b>統計とエクスポート</b>：セッションごとのトークン使用量、API 時間、増減行数、合計コスト。ワンクリックで Markdown エクスポートしアーカイブ・共有；</li>
<li><b>ゼロ摩擦</b>：無料・オープンソース（MIT）・インストールも登録も不要、UI は 10 言語対応。</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer：プロジェクト別にグループ化された Claude Code セッションライブラリと統計" width="880">

<h2>代替手段が適する場面</h2>
<ul>
<li><b>claude --resume</b>：単に「会話を続けたい」なら最速。ツール切替不要。ただし会話継続向けの設計で、履歴閲覧には向かず、長いセッションの検索は非効率、コスト統計もありません；</li>
<li><b>jq / grep</b>：スクリプトで一括分析（全プロジェクトのトークン消費集計など）や単発検索では代替不能。可読性ゼロが代償；</li>
<li><b>汎用 JSONL ビューア / エディタ</b>：データ構造の確認やフォーマットのデバッグには有用。ただし Claude Code の意味論（思考、ツール呼び出し、使用量）を理解できないため、表示されるのはやはり JSON の塊です。</li>
</ul>

<h2>結論</h2>
<p>日常の振り返りと整理：<b>CCViewer</b>。作業継続：<b>claude --resume</b>。一括スクリプト分析：<b>jq</b>。三者は競合しません — むしろ CCViewer のエクスポート機能が生成する Markdown は、他ツールへの入力として好適です。</p>
''',
    faqs=[
        ('CCViewer は無料ですか？ 有料化の予定は？',
         'MIT ライセンスの無料・オープンソースで、登録不要です。ツール自体がブラウザ内で動くためサーバーコストはほぼゼロで、長期的に安心して利用できます。'),
        ('公式ツールと関係がありますか？',
         'ありません。CCViewer は Anthropic に属さない独立したコミュニティのオープンソースプロジェクトで、Claude Code がローカルに生成するセッションファイルを読むだけです。'),
        ('デスクトップアプリはありますか？',
         '現在はウェブアプリです（オフライン利用可、単一 HTML ファイルを開くだけ）。PWA/デスクトップ版はロードマップにあり、GitHub の issue で投票・貢献を歓迎します。'),
    ],
),
]
