/* Deterministic tutorial animation overlay for the built English landing page.
 * Injected by tools/make_tutorial.py via Playwright add_script_tag.
 * Everything is a pure function of the frame number: window.__seek(rawFrame).
 * The timeline below is written in LOGICAL frames; SCALE converts to real
 * frames so the whole animation can be re-timed from one constant.
 * make_tutorial.py injects window.__tutDemo (contents of
 * assets/example-session.jsonl) before this script runs.
 */
(function () {
  'use strict';
  if (window.__seek) return;
  const SCALE = 1.5;          // real frames per logical frame (1.5x slower)
  const LOGICAL_TOTAL = 150;  // logical timeline length
  window.__tutTotal = Math.round(LOGICAL_TOTAL * SCALE);

  const clamp01 = v => (v < 0 ? 0 : v > 1 ? 1 : v);
  const ease = t => { t = clamp01(t); return t * t * (3 - 2 * t); };
  const seg = (f, a, b) => clamp01((f - a) / (b - a));

  const DEMO = window.__tutDemo || '';

  window.__tutOpenDemo = async function () {
    if (!DEMO) { console.error('tutorial: window.__tutDemo missing'); return; }
    const file = new File([DEMO], 'ccviewer-fictional-example.jsonl', { type: 'application/json' });
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
    #tut-dialog{position:fixed;left:170px;top:70px;width:620px;height:470px;background:#f5f5f7;border-radius:12px;box-shadow:0 26px 70px rgba(0,0,0,.55),0 0 0 .5px rgba(0,0,0,.25);display:flex;flex-direction:column;overflow:hidden;opacity:0;transform:scale(.96);transform-origin:center;color:#1d1d1f}
    #tut-dialog .td-title{height:38px;display:flex;align-items:center;justify-content:center;font-size:13.5px;font-weight:700;border-bottom:1px solid #e3e3e8}
    #tut-dialog .td-toolbar{height:34px;display:flex;align-items:center;gap:8px;padding:0 12px;border-bottom:1px solid #e3e3e8;background:#f5f5f7}
    #tut-dialog .td-toolbar .nav{display:flex;gap:2px}
    #tut-dialog .td-toolbar .nav b{display:flex;align-items:center;justify-content:center;width:24px;height:22px;border-radius:5px;color:#8e8e93;font-size:15px;font-weight:700}
    #tut-dialog .td-toolbar .views{display:flex;gap:2px;margin-left:6px}
    #tut-dialog .td-toolbar .views b{display:flex;align-items:center;justify-content:center;width:26px;height:22px;border-radius:5px;color:#aeaeb2}
    #tut-dialog .td-toolbar .views b.on{background:#e3e3e8;color:#1d1d1f}
    #tut-dialog .td-toolbar .grow{flex:1}
    #tut-dialog .td-search{display:flex;align-items:center;gap:6px;width:150px;height:22px;border-radius:6px;background:#e9e9ee;border:1px solid #dddde3;padding:0 8px;color:#8e8e93;font-size:11.5px}
    #tut-dialog .td-body{flex:1;display:flex;min-height:0}
    #tut-dialog .td-side{width:140px;border-right:1px solid #e3e3e8;background:#ececf1;padding:6px}
    #tut-dialog .td-side .h{font-size:10.5px;font-weight:700;color:#8e8e93;padding:4px 8px 5px}
    #tut-dialog .td-srow{display:flex;align-items:center;gap:7px;height:24px;padding:0 8px;border-radius:6px;font-size:12px;font-weight:500;color:#28282c}
    #tut-dialog .td-srow.sel{background:#0a84ff;color:#fff}
    #tut-dialog .td-main{flex:1;display:flex;flex-direction:column;min-width:0}
    #tut-dialog .td-path{height:28px;display:flex;align-items:center;padding:0 12px;font-size:12px;color:#6e6e73;background:#eeeef2;border-bottom:1px solid #e3e3e8}
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
    <div class="td-toolbar">
      <div class="nav"><b>‹</b><b>›</b></div>
      <div class="views"><b class="on"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/></svg></b><b><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="18" rx="1"/><rect x="14" y="3" width="7" height="18" rx="1"/></svg></b></div>
      <div class="grow"></div>
      <div class="td-search"><svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg><span>Search</span></div>
    </div>
    <div class="td-body">
      <div class="td-side">
        <div class="h">Favorites</div>
        <div class="td-srow"><svg width="14" height="14" viewBox="0 0 24 24" fill="#5ba9f0"><path d="M2 6a2 2 0 0 1 2-2h4.6l2 2H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/></svg><span>Desktop</span></div>
        <div class="td-srow"><svg width="14" height="14" viewBox="0 0 24 24" fill="#5ba9f0"><path d="M2 6a2 2 0 0 1 2-2h4.6l2 2H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/></svg><span>Documents</span></div>
        <div class="td-srow"><svg width="14" height="14" viewBox="0 0 24 24" fill="#5ba9f0"><path d="M2 6a2 2 0 0 1 2-2h4.6l2 2H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/></svg><span>Downloads</span></div>
        <div class="td-srow"><svg width="14" height="14" viewBox="0 0 24 24" fill="#5ba9f0"><path d="M2 6a2 2 0 0 1 2-2h4.6l2 2H20a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2z"/></svg><span>Pictures</span></div>
        <div class="td-srow sel"><svg width="14" height="14" viewBox="0 0 24 24" fill="#fff"><path d="M3 12l9-9 9 9h-3v8a1 1 0 0 1-1 1h-4v-6h-2v6H7a1 1 0 0 1-1-1v-8z"/></svg><span>demo</span></div>
      </div>
      <div class="td-main">
        <div class="td-path" id="td-path"></div>
        <div class="td-list" id="td-home"></div>
        <div class="td-list" id="td-claude" style="display:none"></div>
        <div class="td-list" id="td-projects" style="display:none"></div>
      </div>
    </div>
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
    row('ccviewer-fictional-example.jsonl', 'jsonl sel') +
    row('9d2f6a41-0b7c-4e3a-9f1d-2a8e5c7b6d10.jsonl', 'jsonl') +
    row('c47e88b2-51d9-4f60-a1b3-77e0d92c4f85.jsonl', 'jsonl') +
    row('e02f9a7c-3b48-41de-bb66-90d15f8a3c27.jsonl', 'jsonl') +
    row('f8a31d60-c9e2-47b5-8d44-12ce6b9f0a41.jsonl', 'jsonl');
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

  /* Cursor keyframes (logical frames; selector strings resolve live). */
  const PATH = [
    { f: 0, p: { x: 648, y: 415 } },
    { f: 16, s: '#btnPick' },
    { f: 44, r: () => homeRow(9) },
    { f: 58, r: () => { const e = $t('td-claude').querySelector('.td-row'); return e.getBoundingClientRect(); } },
    { f: 68, r: () => { const e = $t('td-projects').querySelector('.td-row'); return e.getBoundingClientRect(); } },
    { f: 76, s: '#td-open' },
    { f: 92, s: '#sidebar' },
    { f: 107, s: '#stream .turn.assistant' },
    { f: 122, s: '#topbar label.toggle' },
    { f: 137, s: '#btnExportMd' },
    { f: 148, p: { x: 480, y: 545 } }
  ];
  const CLICKS = [
    { f: 16, s: '#btnPick' },
    { f: 44, r: () => homeRow(9) }, { f: 47, r: () => homeRow(9) },
    { f: 58, r: () => $t('td-claude').querySelector('.td-row').getBoundingClientRect() },
    { f: 61, r: () => $t('td-claude').querySelector('.td-row').getBoundingClientRect() },
    { f: 68, r: () => $t('td-projects').querySelector('.td-row').getBoundingClientRect() },
    { f: 76, s: '#td-open' }
  ];
  const LABELS = [
    { a: 20, b: 32, t: 'Press  ⌘ ⇧ .  to reveal hidden folders in the Open dialog' },
    { a: 34, b: 44, t: 'Hidden folders appear — open  ~/.claude' },
    { a: 46, b: 56, t: 'Open  ~/.claude/projects/' },
    { a: 64, b: 76, t: 'Select the session file, then click  Open' },
    { a: 86, b: 100, t: 'Session stats — turns, tokens, cost & metadata at a glance' },
    { a: 102, b: 114, t: 'Thinking blocks, tool calls and results rendered inline' },
    { a: 116, b: 128, t: 'Toggle thinking, tools and metadata with one click' },
    { a: 130, b: 146, t: 'Export the whole conversation to Markdown' }
  ];

  const rectOf = k => {
    if (k.p) return { x: k.p.x, y: k.p.y };
    if (k.s) { const c = center(k.s); return c || null; }
    if (k.r) { const r = k.r(); return r ? { x: r.left + r.width / 2, y: r.top + r.height / 2 } : null; }
    return null;
  };

  window.__seek = function (raw) {
    const f = raw / SCALE; /* logical frame */

    /* stage fade: intro only — the GIF plays once and rests on the final viewer */
    fade.style.opacity = f < 7 ? String(1 - ease(seg(f, 0, 7))) : '0';

    /* dialog presence */
    const dIn = ease(seg(f, 18, 24)), dOut = 1 - ease(seg(f, 78, 83));
    const dOp = Math.min(dIn, dOut);
    dialog.style.opacity = String(dOp);
    dialog.style.transform = 'scale(' + (0.96 + 0.04 * dIn) + ')';
    dialog.style.visibility = dOp > 0.01 ? 'visible' : 'hidden';

    /* dialog content: which folder listing */
    const stage = f < 50 ? 0 : f < 62 ? 1 : 2;
    $t('td-home').style.display = stage === 0 ? 'block' : 'none';
    $t('td-claude').style.display = stage === 1 ? 'block' : 'none';
    $t('td-projects').style.display = stage === 2 ? 'block' : 'none';
    pathEl.textContent = PATHS[stage];

    /* hidden rows fade in after the shortcut (visibility keeps layout stable) */
    $t('td-home').querySelectorAll('[data-hidden]').forEach((e, i) => {
      const p = ease(seg(f, 32 + i, 37 + i));
      e.style.opacity = String(p);
      e.style.visibility = p > 0.02 ? 'visible' : 'hidden';
    });

    /* keyboard shortcut badges */
    const kOp = ease(seg(f, 15, 18)) * (1 - ease(seg(f, 32, 36)));
    keys.style.opacity = String(kOp);
    const dr = dialog.getBoundingClientRect();
    keys.style.left = (dr.left + dr.width / 2 - 61) + 'px';
    keys.style.top = (dr.top - 54) + 'px';
    const kb = keys.querySelectorAll('b');
    kb[0].className = (f >= 22 && f < 26) ? 'on' : '';
    kb[1].className = (f >= 25 && f < 29) ? 'on' : '';
    kb[2].className = (f >= 28 && f < 32) ? 'on' : '';

    /* label pill */
    const lb = LABELS.find(l => f >= l.a && f <= l.b);
    if (lb) {
      label.textContent = lb.t;
      label.style.opacity = String(Math.min(ease(seg(f, lb.a, lb.a + 2)), 1 - ease(seg(f, lb.b - 1, lb.b))));
    } else label.style.opacity = '0';

    /* highlight box beats */
    const beats = [
      { a: 85, b: 100, s: '#sidebar' },
      { a: 101, b: 114, s: '#stream .turn.assistant' },
      { a: 115, b: 128, s: '#topbar label.toggle' },
      { a: 130, b: 144, s: '#btnExportMd' }
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
    const dblOn = (f >= 42 && f <= 52) || (f >= 56 && f <= 64);
    dbl.style.opacity = dblOn ? '0.95' : '0';
    if (dblOn) { dbl.style.left = (x + 20) + 'px'; dbl.style.top = (y + 16) + 'px'; }
  };
})();
