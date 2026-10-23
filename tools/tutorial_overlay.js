/* Deterministic tutorial animation overlay for the built English landing page.
 * Injected by tools/make_tutorial.py via Playwright add_script_tag.
 * Everything is a pure function of the frame number: window.__seek(f).
 */
(function () {
  'use strict';
  if (window.__seek) return;
  const FPS = 10, TOTAL = 150, W = 960, H = 600;
  const clamp01 = v => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = t => { t = clamp01(t); return t * t * (3 - 2 * t); };
  const seg = (f, a, b) => clamp01((f - a) / (b - a));

  const DEMO = [
    {"type":"user","sessionId":"9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10","cwd":"/Users/demo/projects/web-app","gitBranch":"main","version":"2.1.9","timestamp":"2026-10-21T09:14:02Z","message":{"role":"user","content":"The login page fails on Safari — find the bug and fix it."}},
    {"type":"assistant","sessionId":"9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10","timestamp":"2026-10-21T09:14:05Z","message":{"role":"assistant","model":"claude-opus-4-6","content":[{"type":"thinking","thinking":"Safari-only failure points to an unsupported API in the auth flow. Let me inspect src/auth.js first, then check how the promise from login() is consumed."},{"type":"tool_use","id":"tu1","name":"Read","input":{"file_path":"src/auth.js"}}]}},
    {"type":"user","sessionId":"9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10","timestamp":"2026-10-21T09:14:07Z","message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"tu1","content":"1  export async function login(creds) {\n2    const res = await fetch('/api/login', {method:'POST'});\n3    return Promise.withResolvers().promise; // Safari < 18 lacks this\n4  }"}]}},
    {"type":"assistant","sessionId":"9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10","timestamp":"2026-10-21T09:14:12Z","message":{"role":"assistant","model":"claude-opus-4-6","content":[{"type":"tool_use","id":"tu2","name":"Edit","input":{"file_path":"src/auth.js","old_string":"Promise.withResolvers().promise","new_string":"new Promise(resolve => res.json().then(resolve))"}}]}},
    {"type":"user","sessionId":"9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10","timestamp":"2026-10-21T09:14:14Z","message":{"role":"user","content":[{"type":"tool_result","tool_use_id":"tu2","content":"The file src/auth.js has been updated."}]}},
    {"type":"assistant","sessionId":"9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10","timestamp":"2026-10-21T09:14:20Z","message":{"role":"assistant","model":"claude-opus-4-6","content":[{"type":"text","text":"Fixed. `Promise.withResolvers()` is unavailable on older Safari, so I replaced it with a plain `new Promise(...)` wrapper. Reload the login page in Safari to confirm."}],"usage":{"input_tokens":1215,"output_tokens":184,"cache_read_input_tokens":9482}}}
  ].map(o => JSON.stringify(o)).join('\n') + '\n';

  window.__tutOpenDemo = async function () {
    const file = new File([DEMO], '9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10.jsonl', { type: 'application/json' });
    await openLocalFile(file, null);
    window.scrollTo(0, 0);
  };

  /* ---------- DOM ---------- */
  const root = document.createElement('div');
  root.id = 'tut';
  root.style.cssText = 'position:fixed;inset:0;z-index:2147483000;pointer-events:none;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif';
  root.innerHTML = `
  <style>
    #tut *{box-sizing:border-box;margin:0;padding:0}
    #tut-cursor{position:fixed;left:0;top:0;width:26px;height:26px;will-change:transform;opacity:0}
    #tut-ripple{position:fixed;left:0;top:0;width:8px;height:8px;border-radius:50%;border:2.5px solid #ffb28c;will-change:transform;opacity:0}
    #tut-hl{position:fixed;border:2.5px solid #ff9d6b;border-radius:10px;box-shadow:0 0 0 4px rgba(255,157,107,.22),0 0 26px rgba(255,157,107,.35);opacity:0;will-change:transform}
    #tut-label{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);max-width:86%;padding:9px 18px;border-radius:99px;background:rgba(13,17,23,.92);border:1px solid rgba(255,255,255,.16);color:#f0f6fc;font-size:14.5px;font-weight:600;letter-spacing:.2px;opacity:0;white-space:nowrap}
    #tut-keys{position:fixed;display:flex;gap:8px;opacity:0;will-change:transform}
    #tut-keys b{display:flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:8px;background:#fff;color:#1d1d1f;font-size:19px;font-weight:600;border:1px solid #d2d2d7;box-shadow:0 2px 0 #d2d2d7;transition:none}
    #tut-keys b.on{background:#0a84ff;color:#fff;border-color:#0a84ff;box-shadow:0 2px 0 #0060df;transform:translateY(2px)}
    #tut-dbl{position:fixed;padding:4px 10px;border-radius:6px;background:rgba(13,17,23,.92);color:#fff;font-size:12px;font-weight:600;opacity:0;white-space:nowrap}
    #tut-fade{position:fixed;inset:0;background:#0d1117;opacity:1}
    #tut-dialog{position:fixed;left:200px;top:76px;width:560px;height:446px;background:#f5f5f7;border-radius:12px;box-shadow:0 26px 70px rgba(0,0,0,.55),0 0 0 .5px rgba(0,0,0,.25);display:flex;flex-direction:column;overflow:hidden;opacity:0;transform:scale(.96);transform-origin:center;color:#1d1d1f}
    #tut-dialog .td-title{height:38px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700;border-bottom:1px solid #e3e3e8}
    #tut-dialog .td-path{height:32px;display:flex;align-items:center;padding:0 14px;font-size:12px;color:#6e6e73;background:#eeeef2;border-bottom:1px solid #e3e3e8}
    #tut-dialog .td-list{flex:1;overflow:hidden;padding:5px 8px}
    #tut-dialog .td-row{display:flex;align-items:center;gap:9px;height:28px;padding:0 9px;border-radius:6px;font-size:12.5px;font-weight:500;color:#28282c}
    #tut-dialog .td-row svg{flex:0 0 auto}
    #tut-dialog .td-row.folder{color:#1d1d1f}
    #tut-dialog .td-row.sel{background:#0a84ff;color:#fff}
    #tut-dialog .td-row.hl{outline:2.5px solid #ff9d6b;outline-offset:-2.5px}
    #tut-dialog .td-foot{height:52px;display:flex;align-items:center;justify-content:flex-end;gap:10px;padding:0 14px;border-top:1px solid #e3e3e8;background:#f5f5f7}
    #tut-dialog .td-btn{min-width:76px;height:28px;border-radius:7px;font-size:13px;font-weight:600;display:flex;align-items:center;justify-content:center;border:1px solid #d2d2d7;background:#fff;color:#1d1d1f}
    #tut-dialog .td-btn.primary{background:#0a84ff;border-color:#0a84ff;color:#fff}
  </style>
  <div id="tut-fade"></div>
  <div id="tut-hl"></div>
  <div id="tut-dialog">
    <div class="td-title">Open</div>
    <div class="td-path" id="td-path"></div>
    <div class="td-list" id="td-home"></div>
    <div class="td-list" id="td-claude" style="display:none"></div>
    <div class="td-list" id="td-projects" style="display:none"></div>
    <div class="td-foot"><div class="td-btn">Cancel</div><div class="td-btn primary" id="td-open">Open</div></div>
  </div>
  <div id="tut-keys"><b>⌘</b><b>⇧</b><b>.</b></div>
  <div id="tut-label"></div>
  <div id="tut-dbl">Double-click</div>
  <div id="tut-ripple"></div>
  <div id="tut-cursor"><svg width="26" height="26" viewBox="0 0 24 24"><path d="M5 2l13.5 10.6-5.9.9 3.4 6.8-2.7 1.3-3.4-6.9-4.9 4z" fill="#0d1117" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg></div>`;
  document.body.appendChild(root);
  const $t = id => root.querySelector('#' + id);
  const cursor = $t('tut-cursor'), ripple = $t('tut-ripple'), hl = $t('tut-hl'),
    label = $t('tut-label'), keys = $t('tut-keys'), dbl = $t('tut-dbl'),
    fade = $t('tut-fade'), dialog = $t('tut-dialog');

  const folderSvg = '<svg width="19" height="19" viewBox="0 0 24 24" fill="#5ba9f0"><path d="M2 6a2 2 0 0 1 2-2h4.6l2 2H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/></svg>';
  const fileSvg = '<svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="#9a9aa0" stroke-width="1.8"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/></svg>';
  const row = (name, cls, hidden) => `<div class="td-row ${cls || ''}" ${hidden ? 'data-hidden="1"' : ''}>${cls === 'jsonl' || cls === 'jsonl sel' ? fileSvg : folderSvg}<span>${name}</span></div>`;

  $t('td-home').innerHTML =
    row('Desktop') + row('Documents') + row('Downloads') + row('Movies') + row('Music') + row('Pictures') +
    row('.Trash', 'hidden', 1) + row('.config', 'hidden', 1) + row('.DS_Store', 'hidden', 1) + row('.claude', 'folder hl', 1);
  $t('td-claude').innerHTML =
    row('projects', 'hl') + row('todos') + row('statsig') + row('shell-snapshots') + row('settings.json', 'jsonl') + row('CLAUDE.md', 'jsonl');
  $t('td-projects').innerHTML =
    row('9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10.jsonl', 'jsonl sel') +
    row('c47e88b2-51d9-4f60-a1b3-77e0d92c4f85.jsonl', 'jsonl') +
    row('e02f9a7c-3b48-41de-bb66-90d15f8a3c27.jsonl', 'jsonl') +
    row('f8a31d60-c9e2-47b5-8d44-12ce6b9f0a41.jsonl', 'jsonl') +
    row('ccviewer-fictional-example.jsonl', 'jsonl');
  const pathEl = $t('td-path');
  const PATHS = ['macHD  ›  demo', 'macHD  ›  demo  ›  .claude', 'macHD  ›  demo  ›  .claude  ›  projects'];

  /* ---------- helpers ---------- */
  const center = sel => {
    const e = document.querySelector(sel);
    if (!e) return null;
    const r = e.getBoundingClientRect();
    if (r.width < 2) return null;
    return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
  };
  const homeRow = i => { const rows = $t('td-home').querySelectorAll('.td-row'); return rows[i] ? rows[i].getBoundingClientRect() : null; };

  /* Cursor keyframes: selector strings resolve live. */
  const PATH = [
    { f: 0, p: { x: 648, y: 415 } },
    { f: 11, s: '#btnPick' },
    { f: 28, r: () => homeRow(9) },
    { f: 42, r: () => { const e = $t('td-claude').querySelector('.td-row'); return e.getBoundingClientRect(); } },
    { f: 55, r: () => { const e = $t('td-projects').querySelector('.td-row'); return e.getBoundingClientRect(); } },
    { f: 62, s: '#td-open' },
    { f: 76, s: '#sidebar' },
    { f: 92, s: '#stream .turn.assistant' },
    { f: 107, s: '#btnExportMd' },
    { f: 132, p: { x: 480, y: 545 } }
  ];
  const CLICKS = [
    { f: 11, s: '#btnPick' },
    { f: 36, r: () => homeRow(9) }, { f: 39, r: () => homeRow(9) },
    { f: 48, r: () => $t('td-claude').querySelector('.td-row').getBoundingClientRect() },
    { f: 51, r: () => $t('td-claude').querySelector('.td-row').getBoundingClientRect() },
    { f: 57, r: () => $t('td-projects').querySelector('.td-row').getBoundingClientRect() },
    { f: 67, s: '#td-open' },
    { f: 109, s: '#btnExportMd' }
  ];
  const LABELS = [
    { a: 13, b: 26, t: 'Press  ⌘ ⇧ .  to reveal hidden folders in the Open dialog' },
    { a: 27, b: 40, t: 'Hidden folders appear — open  ~/.claude' },
    { a: 41, b: 54, t: 'Open  ~/.claude/projects/  and pick a  <sessionId>.jsonl' },
    { a: 55, b: 72, t: 'Select the session file, then click  Open' },
    { a: 75, b: 89, t: 'Session stats — turns, tokens, cost & metadata at a glance' },
    { a: 91, b: 105, t: 'Thinking blocks, tool calls and results rendered inline' },
    { a: 107, b: 121, t: 'Export the whole conversation to Markdown' },
    { a: 123, b: 141, t: 'Runs 100% locally — your files never leave the browser' }
  ];

  const rectOf = k => {
    if (k.p) return { x: k.p.x, y: k.p.y };
    if (k.s) { const c = center(k.s); return c || null; }
    if (k.r) { const r = k.r(); return r ? { x: r.left + r.width / 2, y: r.top + r.height / 2 } : null; }
    return null;
  };

  window.__seek = function (f) {
    /* stage fade for a clean loop */
    fade.style.opacity = f < 7 ? String(1 - ease(seg(f, 0, 7))) : String(ease(seg(f, 143, 149)));

    /* dialog presence */
    const dIn = ease(seg(f, 12, 18)), dOut = 1 - ease(seg(f, 68, 73));
    const dOp = Math.min(dIn, dOut);
    dialog.style.opacity = String(dOp);
    dialog.style.transform = 'scale(' + (0.96 + 0.04 * dIn) + ')';
    dialog.style.visibility = dOp > 0.01 ? 'visible' : 'hidden';

    /* dialog content: which folder listing */
    const stage = f < 44 ? 0 : f < 52 ? 1 : 2;
    $t('td-home').style.display = stage === 0 ? 'block' : 'none';
    $t('td-claude').style.display = stage === 1 ? 'block' : 'none';
    $t('td-projects').style.display = stage === 2 ? 'block' : 'none';
    pathEl.textContent = PATHS[stage];

    /* hidden rows fade in after the shortcut (visibility keeps layout stable) */
    $t('td-home').querySelectorAll('[data-hidden]').forEach((e, i) => {
      const p = ease(seg(f, 26 + i, 31 + i));
      e.style.opacity = String(p);
      e.style.visibility = p > 0.02 ? 'visible' : 'hidden';
    });

    /* keyboard shortcut badges */
    const kOp = ease(seg(f, 14, 17)) * (1 - ease(seg(f, 30, 34)));
    keys.style.opacity = String(kOp);
    const dr = dialog.getBoundingClientRect();
    keys.style.left = (dr.left + dr.width / 2 - 61) + 'px';
    keys.style.top = (dr.top - 54) + 'px';
    const kb = keys.querySelectorAll('b');
    kb[0].className = (f >= 18 && f < 22) ? 'on' : '';
    kb[1].className = (f >= 21 && f < 25) ? 'on' : '';
    kb[2].className = (f >= 24 && f < 28) ? 'on' : '';

    /* label pill */
    const lb = LABELS.find(l => f >= l.a && f <= l.b);
    if (lb) {
      label.textContent = lb.t;
      label.style.opacity = String(Math.min(ease(seg(f, lb.a, lb.a + 2)), 1 - ease(seg(f, lb.b - 1, lb.b))));
    } else label.style.opacity = '0';

    /* highlight box beats */
    const beats = [
      { a: 74, b: 89, s: '#sidebar' },
      { a: 91, b: 105, s: '#stream .turn.assistant' },
      { a: 106, b: 121, s: '#btnExportMd' }
    ];
    const bt = beats.find(b => f >= b.a && f <= b.b);
    let hlShown = false;
    if (bt) {
      const e = document.querySelector(bt.s);
      if (e) {
        const r = e.getBoundingClientRect();
        if (r.width > 2) {
          const pad = 7;
          hl.style.left = (r.left - pad) + 'px'; hl.style.top = (r.top - pad) + 'px';
          hl.style.width = (r.width + pad * 2) + 'px'; hl.style.height = (r.height + pad * 2) + 'px';
          hl.style.opacity = String(Math.min(ease(seg(f, bt.a, bt.a + 2)), 1 - ease(seg(f, bt.b - 1, bt.b))));
          hlShown = true;
        }
      }
    }
    if (!hlShown) hl.style.opacity = '0';

    /* cursor along keyframes */
    const P = [];
    for (const k of PATH) {
      const pt = rectOf(k) || (P.length ? P[P.length - 1].pt : { x: 0, y: 0 });
      P.push({ f: k.f, pt });
    }
    let x = P[0].pt.x, y = P[0].pt.y, set = false;
    for (let i = 0; i < P.length - 1; i++) {
      if (f < P[i + 1].f) {
        const A = P[i].pt, B = P[i + 1].pt;
        if (f > P[i].f) {
          const t = ease(seg(f, P[i].f, P[i + 1].f));
          x = A.x + (B.x - A.x) * t; y = A.y + (B.y - A.y) * t;
        } else { x = A.x; y = A.y; }
        set = true; break;
      }
    }
    if (!set) { x = P[P.length - 1].pt.x; y = P[P.length - 1].pt.y; }
    const pressed = CLICKS.some(c => f >= c.f && f <= c.f + 2);
    cursor.style.opacity = String(ease(seg(f, 1, 6)));
    const scale = pressed ? 0.8 : 1;
    cursor.style.transform = `translate(${x - 3}px,${y - 2}px) scale(${scale})`;

    /* click ripple */
    let rOp = 0, rx = 0, ry = 0, rr = 8;
    for (const c of CLICKS) {
      const age = f - c.f;
      if (age >= 0 && age <= 4) {
        const p = rectOf(c); if (p) { rx = p.x; ry = p.y; }
        rr = 7 + age * 9; rOp = 0.9 * (1 - age / 4);
      }
    }
    ripple.style.opacity = String(rOp);
    ripple.style.transform = `translate(${rx - 4}px,${ry - 4}px) scale(${rr / 8})`;

    /* double-click tooltip */
    const dblOn = (f >= 34 && f <= 42) || (f >= 46 && f <= 53);
    dbl.style.opacity = dblOn ? '0.95' : '0';
    if (dblOn) { dbl.style.left = (x + 20) + 'px'; dbl.style.top = (y + 16) + 'px'; }
  };
})();
