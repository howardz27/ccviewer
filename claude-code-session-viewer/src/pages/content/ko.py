# -*- coding: utf-8 -*-
PAGES = [
dict(
    slug='how-to-view-claude-code-session-history.html',
    crumb='전체 기록 보기',
    short='Claude Code 세션의 전체 기록을 보는 방법',
    title='Claude Code 세션의 전체 기록을 보는 방법 — 3가지 방법(2026) | CCViewer',
    desc='Claude Code 세션의 전체 기록을 보는 3가지 방법: 터미널에서 claude --resume, ~/.claude/projects 아래의 .jsonl 파일 열기, 또는 CCViewer로 브라우저에서 시각적으로 재생(Markdown/사고 블록/도구 호출/비용 통계) — 100% 로컬 렌더링.',
    h1='Claude Code 세션의 전체 기록을 어떻게 확인하나요?',
    body=r'''
<p>로컬 세션의 기본 위치는 ~/.claude/projects/입니다. CLAUDE_CONFIG_DIR를 설정하면 기본 디렉터리가 바뀝니다. 저장 비활성화나 보존 기간에 따른 정리로 모든 기록이 영구 보관되지는 않습니다. 클라우드나 원격 세션은 실행 환경을 확인하세요.</p>

<h2>방법 1: CCViewer로 브라우저에서 시각적으로 재생(권장)</h2>
<p><a href="{{app}}">CCViewer</a>는 무료 오픈소스 Claude Code 세션 뷰어입니다. 페이지를 열고 세션 파일을 드롭하기만 하면(<code>~/.claude/projects/</code> 폴더 전체를 가져올 수도 있음) 채팅 기록처럼 세션을 재생할 수 있습니다:</p>
<ul>
<li><b>완전한 Markdown 렌더링</b> — 코드 블록, 표, 목록, 링크를 그대로 표시. 긴 JSON 나열과는 이별;</li>
<li><b>사고 블록(thinking)</b> — 모델의 확장 추론을 접었다 펼 수 있음;</li>
<li><b>도구 호출</b> — Read / Edit / Bash 등 모든 호출의 파라미터와 결과를 펼쳐서 확인;</li>
<li><b>사용량·비용 통계</b> — 입력/출력/캐시 토큰, 세션 시간, 코드 줄 증감, 총 비용을 한눈에;</li>
<li><b>Markdown 내보내기</b> — 어떤 세션이든 클릭 한 번으로 공유 가능한 <code>.md</code> 문서로.</li>
</ul>
<p>세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.</p>
<img class="shot" src="/assets/screenshot-viewer.png" alt="CCViewer로 Claude Code 세션 기록 보기: Markdown, 사고 블록, 도구 호출 및 통계" width="880">

<h2>방법 2: 터미널에서 세션 재개</h2>
<p>Claude Code에는 세션 재개 기능이 내장되어 있습니다. <b>원래 프로젝트 디렉터리</b>에서 실행하세요:</p>
<pre><code># 이 프로젝트의 세션 목록을 표시하고 대화형으로 선택
claude --resume     # 약칭: claude -r

# 가장 최근 세션을 바로 재개
claude --continue   # 약칭: claude -c

# 세션 ID로 특정 세션 재개
claude --resume &lt;sessionId&gt;</code></pre>
<p>「계속 작업하기」에는 좋지만, 기록을 <b>읽거나 검색</b>하기엔 불편합니다. 긴 세션에서 특정 도구 호출을 찾는 건 고역이고 비용 통계도 없습니다.</p>

<h2>방법 3: 원본 JSONL 파일 직접 읽기</h2>
<p>세션은 <code>~/.claude/projects/&lt;project&gt;/&lt;sessionId&gt;.jsonl</code>에 JSONL 형식(한 줄에 JSON 객체 하나)으로 저장됩니다. 아무 에디터나 명령줄로 확인할 수 있습니다:</p>
<pre><code># jq로 모든 사용자 프롬프트 추출
cat ~/.claude/projects/-Users-you-myproject/&lt;sessionId&gt;.jsonl \\
  | jq -r 'select(.type=="user") | .message.content'</code></pre>
<p>원본 파일이 가장 완전한 정보원(토큰 사용량, git 브랜치, 타임스탬프 등 메타데이터 포함)이지만 가독성은 낮습니다 — 바로 이래서 그래픽 뷰어가 존재합니다.</p>

<h2>세 가지 방법 비교</h2>
<table>
<tr><th></th><th>CCViewer</th><th>claude --resume</th><th>원본 JSONL</th></tr>
<tr><td>그래픽 읽기</td><td>✅</td><td>부분적(대화 계속)</td><td>❌</td></tr>
<tr><td>Markdown 렌더링</td><td>✅</td><td>✅</td><td>❌</td></tr>
<tr><td>사고 / 도구 호출</td><td>✅ 접기 가능</td><td>접힌 요약</td><td>원본 JSON</td></tr>
<tr><td>토큰 / 비용 통계</td><td>✅</td><td>❌</td><td>수동 jq</td></tr>
<tr><td>다중 세션 관리</td><td>✅ 폴더 가져오기</td><td>현재 프로젝트만</td><td>❌</td></tr>
</table>
<p>세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.</p>''',
    faqs=[('기록을 보면 내 코드가 업로드되나요?', '세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.'), ('세션에서 압축(compact)된 부분도 볼 수 있나요?', 'JSONL은 한 줄에 하나의 JSON 값을 저장합니다. CCViewer는 파일에 남아 있는 지원 메시지와 도구 기록을 읽습니다. 누락되거나 삭제된 기록을 복원하지 못하며 사용량은 제공된 필드에 따라 달라집니다. 원본 파일을 보관하세요.'), ('모바일에서도 되나요?', '됩니다. CCViewer는 반응형 웹 페이지입니다. 다만 세션 파일은 컴퓨터에 있으므로 먼저 .jsonl을 폰으로 전송(iCloud/클라우드 등)한 뒤 브라우저로 열어야 합니다.')],
),
dict(
    slug='find-claude-code-session-jsonl-file.html',
    crumb='JSONL 찾기',
    short='세션의 JSONL 파일 위치를 찾는 방법',
    title='Claude Code 세션의 JSONL 파일 위치를 찾는 방법 | CCViewer',
    desc='Claude Code 세션 파일은 ~/.claude/projects/<project-dir>/<sessionId>.jsonl에 저장됩니다. find/grep으로 세션의 JSONL 파일을 빠르게 찾는 방법과 sessionId를 모를 때 내용이나 시간으로 역추적하는 방법을 소개.',
    h1='Claude Code 세션의 JSONL 파일 위치를 어떻게 찾나요?',
    body=r'''
<p>로컬 세션의 기본 위치는 ~/.claude/projects/입니다. CLAUDE_CONFIG_DIR를 설정하면 기본 디렉터리가 바뀝니다. 저장 비활성화나 보존 기간에 따른 정리로 모든 기록이 영구 보관되지는 않습니다. 클라우드나 원격 세션은 실행 환경을 확인하세요.</p>

<h2>먼저 디렉터리 이름 규칙 이해하기</h2>
<p><code>~/.claude/projects/</code>의 각 하위 디렉터리는 프로젝트(작업 디렉터리) 하나에 해당합니다. 이름은 <b>프로젝트 경로에서 변환됩니다: 경로의 <code>/</code>, <code>_</code> 등 영숫자가 아닌 문자가 모두 하이픈 <code>-</code>으로 치환됩니다</b>. 예:</p>
<pre><code>프로젝트 경로                      세션 디렉터리
/Users/you/Documents/my_app      →  -Users-you-Documents-my-app
/home/you/projects/shop-api      →  -home-you-projects-shop-api</code></pre>
<p>세션 하나는 파일 하나: <code>&lt;sessionId&gt;.jsonl</code>(<code>9a1b2c3d-…</code> 같은 UUID).</p>

<h2>경우 1: sessionId를 안다 — 바로 find</h2>
<pre><code>find ~/.claude/projects -name "&lt;sessionId&gt;.jsonl"</code></pre>
<p>sessionId는 어디서 얻나요? 가장 쉬운 방법은 <b>대화 중에 슬래시 명령 <code>/status</code>를 입력하는 것</b> — 출력에 현재 Session ID가 포함됩니다. 그 외에 <code>claude --resume</code> 세션 목록, 오류 메시지, 뷰어 사이드바의「Session ID」필드에서도 확인할 수 있습니다.</p>

<h2>경우 2: sessionId를 모른다 — 내용으로 역추적</h2>
<p>대화 내용(당시 질문 등)이 기억난다면 grep하세요:</p>
<pre><code># 모든 세션에서 키워드 검색, 일치하는 파일 나열
grep -l "로그인 페이지 수정" ~/.claude/projects/*/*.jsonl

# 특정 프로젝트 디렉터리만 검색
grep -l "로그인 페이지 수정" ~/.claude/projects/-Users-you-Documents-my-app/*.jsonl</code></pre>

<h2>경우 3: 시간으로 최근 세션 찾기</h2>
<pre><code># 가장 최근에 수정된 세션 파일 10개 나열
ls -t ~/.claude/projects/*/*.jsonl | head -10</code></pre>

<h2>그래픽 방법: CCViewer에 맡기기</h2>
<p>명령어를 치고 싶지 않다면? <a href="{{app}}">CCViewer</a>는 <code>~/.claude/projects/</code> 폴더 전체를 선택(또는 드롭)할 수 있습니다. 모든 <code>.jsonl</code>을 재귀적으로 스캔해 프로젝트별로 그룹화하고 시간순으로 정렬하며, 각 세션의 제목·경로·시간 범위·메시지 수·비용을 표시합니다 — 파일 위치를 몰라도 클릭하면 열립니다.</p>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer 폴더 모드: 프로젝트별로 그룹화된 Claude Code 세션 라이브러리" width="880">

<h2>macOS 팁: 숨김 폴더 열기</h2>
<ul>
<li>파인더에서 <span class="kbd">⌘⇧G</span>를 누르고 <code>~/.claude/projects</code> 입력 후 Enter;</li>
<li>파일 대화상자에서 <span class="kbd">⌘⇧.</span>를 누르면 숨김 폴더 표시(<code>.</code>으로 시작하는 디렉터리는 기본적으로 보이지 않음).</li>
</ul>
<p>세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.</p>''',
    faqs=[('~/.claude 디렉터리를 찾을 수 없는 이유는?', '점으로 시작해서 기본적으로 숨겨져 있기 때문입니다. 파인더에서 ⌘⇧G로 경로를 직접 입력하거나 ⌘⇧.로 숨김 파일을 표시하세요. 터미널에서는 ls -la ~/.claude로 항상 보입니다.'), ('프로젝트 디렉터리에 jsonl 파일이 많은데 어느 것이 내 세션인가요?', '파일 하나 = 세션 하나입니다. 수정 시간(ls -t)이나 내용(grep -l)으로 필터링하는 것이 가장 효과적입니다. CCViewer로 폴더 전체를 가져오면 각 세션의 제목과 통계가 표시되어 한눈에 구분됩니다.'), ('Windows에서 경로는?', '사용자 프로필 아래에 동일한 구조입니다: %USERPROFILE%\\\\.claude\\\\projects\\\\&lt;project&gt;\\\\&lt;sessionId&gt;.jsonl.')],
),
dict(
    slug='where-claude-code-sessions-stored.html',
    crumb='저장 위치',
    short='Claude Code 세션 기록은 어디에 저장되나?',
    title='Claude Code 세션 기록은 어디에 저장되나? 저장 구조 상세 해설 | CCViewer',
    desc='로컬 세션의 기본 위치는 ~/.claude/projects/입니다. CLAUDE_CONFIG_DIR를 설정하면 기본 디렉터리가 바뀝니다. 저장 비활성화나 보존 기간에 따른 정리로 모든 기록이 영구 보관되지는 않습니다. 클라우드나 원격 세션은 실행 환경을 확인하세요.',
    h1='Claude Code 세션의 기록은 어디에 저장되나요?',
    body=r'''<p>로컬 세션의 기본 위치는 ~/.claude/projects/입니다. CLAUDE_CONFIG_DIR를 설정하면 기본 디렉터리가 바뀝니다. 저장 비활성화나 보존 기간에 따른 정리로 모든 기록이 영구 보관되지는 않습니다. 클라우드나 원격 세션은 실행 환경을 확인하세요.</p><h2>저장 위치와 보존</h2><ul><li><code>~/.claude/projects/&lt;project&gt;/&lt;session-id&gt;.jsonl</code> — JSONL</li><li><code>~/.claude/settings.json</code> — settings</li><li><code>~/.claude.json</code> — configuration</li></ul><p><a href="https://code.claude.com/docs/en/claude-directory">Claude Code — 저장 위치와 보존</a></p><h2>형식과 한계</h2><p>JSONL은 한 줄에 하나의 JSON 값을 저장합니다. CCViewer는 파일에 남아 있는 지원 메시지와 도구 기록을 읽습니다. 누락되거나 삭제된 기록을 복원하지 못하며 사용량은 제공된 필드에 따라 달라집니다. 원본 파일을 보관하세요.</p><p>세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.</p><p><a href="{{app}}">CCViewer</a></p>''',
    faqs=[('Claude Code 기록이 Anthropic 서버로 업로드되나요?', '로컬 세션의 기본 위치는 ~/.claude/projects/입니다. CLAUDE_CONFIG_DIR를 설정하면 기본 디렉터리가 바뀝니다. 저장 비활성화나 보존 기간에 따른 정리로 모든 기록이 영구 보관되지는 않습니다. 클라우드나 원격 세션은 실행 환경을 확인하세요. 세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.'), ('세션 기록을 삭제하려면?', '해당 .jsonl 파일(또는 프로젝트 하위 디렉터리 전체)을 삭제하면 됩니다. resume 목록에서도 사라집니다. 삭제 전 백업이 필요 없는지 확인하세요.'), ('~/.claude/projects와 ~/.claude.json은 같은 건가요?', '아닙니다. ~/.claude.json(또는 claude.json)은 전역 설정 파일(MCP 서버, 테마 등)이고, 세션 기록은 ~/.claude/projects/ 아래의 .jsonl 파일에 있습니다.')],
),
dict(
    slug='best-claude-code-session-viewer.html',
    crumb='2026년 최고의 뷰어',
    short='2026년 최고의 Claude Code 세션 뷰어는?',
    title='2026년 최고의 Claude Code 세션 뷰어는? 비교와 추천 | CCViewer',
    desc='2026년 Claude Code 세션 기록을 돌아보는 주요 방법 비교: 내장 claude --resume, 명령줄 jq/grep, 범용 JSONL 도구, 오픈소스 그래픽 뷰어 CCViewer — 기능·프라이버시·사용성 관점에서 추천.',
    h1='2026년 Claude Code 세션에 가장 좋은 뷰어는 무엇인가요?',
    body=r'''
<p>이 글은 CCViewer 프로젝트가 작성한 작업별 비교이며 독립 순위나 성능 측정이 아닙니다. CCViewer는 읽기와 Markdown 내보내기, resume은 작업 계속하기, jq는 스크립트 분석에 적합합니다.</p><p>CCViewer에는 세션 라이브러리 전체의 내장 전문 검색이 없습니다. 브라우저 데이터를 지우면 가져온 라이브러리가 삭제될 수 있습니다.</p>

<h2>후보 한눈에 보기</h2>
<table>
<tr><th>선택지</th><th>유형</th><th>적합한 용도</th></tr>
<tr><td><b>CCViewer</b>(오픈소스)</td><td>웹 기반 그래픽 뷰어</td><td>열람·검색·감사·내보내기</td></tr>
<tr><td>claude --resume / -r</td><td>CLI 내장</td><td>미완료 대화 계속하기</td></tr>
<tr><td>jq / grep / less</td><td>명령줄</td><td>스크립트 일괄 처리</td></tr>
<tr><td>범용 JSONL/로그 뷰어</td><td>에디터 플러그인 등</td><td>원본 데이터 구조 확인</td></tr>
</table>

<h2>우리의 추천: CCViewer</h2>
<p>2026년 「전용 Claude Code 세션 뷰어」 하나를 고른다면 오픈소스 <a href="{{app}}">CCViewer</a>(ccviewer.top)를 추천합니다 — 가장 화려해서가 아니라 이 시나리오에서 핵심을 모두 제대로 잡았기 때문입니다:</p>
<ol>
<li><b>JSONL 세션 형식을 위해 태어남</b>: 범용 로그 도구가 아니라 Claude Code의 항목 구조를 네이티브로 이해 — 사용자 메시지, Markdown 응답, 사고 블록, 도구 호출 파라미터와 결과, 이미지, 비용 스냅샷을 바로 렌더링;</li>
<li><b>프라이버시 최우선</b>: 100% 브라우저 내 파싱, 세션 파일 업로드 없음. 세션 파일에는 소스 코드와 시크릿이 있으므로 로컬 렌더링이 이런 도구의 최소 요건이어야 합니다;</li>
<li><b>세션 라이브러리</b>: <code>~/.claude/projects/</code> 전체를 드롭하면 프로젝트별 그룹화, 시간/메시지 수/토큰/비용 정렬, IndexedDB 영속화로 다음에 열어도 그대로;</li>
<li><b>통계와 내보내기</b>: 세션별 토큰 사용량, API 소요 시간, 줄 증감, 총 비용. 클릭 한 번으로 Markdown 내보내기해 보관·공유;</li>
<li><b>장벽 없음</b>: 무료, 오픈소스(MIT), 설치·가입 불필요, UI는 10개 언어 지원.</li>
</ol>
<img class="shot" src="/assets/screenshot-library.png" alt="CCViewer: 프로젝트별로 그룹화된 Claude Code 세션 라이브러리와 통계" width="880">

<h2>대안이 더 나은 때</h2>
<ul>
<li><b>claude --resume</b>: 단순히 「이어서 대화」가 목적이면 가장 빠릅니다. 도구 전환이 없죠. 하지만 대화 계속에 최적화되어 있어 기록 읽기에는 부적합하고, 긴 세션 검색이 비효율적이며 비용 통계도 없습니다;</li>
<li><b>jq / grep</b>: 스크립트로 일괄 분석(전 프로젝트 토큰 소비 집계 등)이나 간단한 조회에는 대체 불가능합니다. 가독성 제로가 그 대가죠;</li>
<li><b>범용 JSONL 뷰어/에디터</b>: 데이터 구조 확인이나 포맷 디버깅에 유용합니다. 다만 Claude Code의 의미(사고, 도구 호출, 사용량)를 이해하지 못해 결국 JSON 덩어리로 표시됩니다.</li>
</ul>

<h2>결론</h2>
<p>일상적인 열람과 정리: <b>CCViewer</b>. 작업 계속: <b>claude --resume</b>. 일괄 스크립트 분석: <b>jq</b>. 셋은 경쟁하지 않습니다 — 오히려 CCViewer의 내보내기가 만들어내는 Markdown은 다른 도구에 넣기 좋은 재료입니다.</p>
<p>세션 파일은 브라우저에서 로컬로 분석하고 표시합니다. 온라인 사이트는 Microsoft Clarity를 자동으로 로드하여 페이지 상호작용을 기록합니다. 오프라인 사본은 분석을 로드하지 않습니다.</p>''',
    faqs=[('CCViewer는 무료인가요? 유료화 계획은?', '무료이며 오픈소스입니다. 가입이나 로그인 없이 브라우저에서 바로 사용할 수 있습니다.'), ('공식 도구와 관련이 있나요?', '없습니다. CCViewer는 Anthropic과 무관한 독립 커뮤니티 오픈소스 프로젝트이며, Claude Code가 로컬에 생성하는 세션 파일을 읽을 뿐입니다.')],
),
]
