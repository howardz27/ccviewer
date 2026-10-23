// Regression checks for live refresh without browser or package dependencies.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const template = fs.readFileSync('claude-code-session-viewer/src/template.html', 'utf8');
const parser = template.slice(template.indexOf('function parse('), template.indexOf('function toolArgPreview('));
const refresh = template.slice(template.indexOf('// Keep live access separate'), template.indexOf('const cwdBasename='));
const classes = (names = []) => {
  const items = new Set(names);
  return {contains: name => items.has(name), toggle(name, enabled) { enabled ? items.add(name) : items.delete(name); }};
};
const elements = new Map();
for (const id of ['#drop', '#library', '#content', '#stream', '#refreshbar', '#btnRefresh', '#refreshStatus', '#refreshFile']) {
  elements.set(id, {classList: classes(['hide']), value: '0', textContent: '', disabled: false,
    scrollHeight: 2000, clientHeight: 500, scrollTop: 300, setAttribute() {}, querySelectorAll: () => []});
}
let timer = null, timerDelay = null, rendered = [], rebuilds = 0, writes = [];
const context = {
  CUR: null, CUR_ID: 'session-1', document: {hidden: false, addEventListener() {}},
  window: {}, self: {}, $: key => elements.get(key), t: key => key,
  setTimeout(fn, delay) { timer = fn; timerDelay = delay; return 1; }, clearTimeout() { timer = null; },
  renderEntry: entry => rendered.push(entry), renderAll: () => rebuilds++,
  renderSidebar() {}, applyFname() {}, applyToggles() {}, renderNav() {},
  async saveToLibrary(text, name, source, id) { writes.push({text, id}); return id || 'new-id'; },
};
vm.createContext(context);
vm.runInContext(parser + '\n' + refresh, context);
const run = code => vm.runInContext(code, context);
const record = (text, sessionId = 'session-1') => ({type: 'assistant', sessionId, message: {content: text}});
let contents = JSON.stringify(record('first')) + '\n';
let reads = 0;
const source = {async getFile() { reads++; return {name: 'live.jsonl', text: async () => contents}; }};
function resetSession() {
  context.currentText = JSON.stringify(record('first')) + '\n';
  context.liveSource = source;
  run('CUR={...parse(currentText),sum:summarize(parse(currentText).entries),text:currentText,name:"live.jsonl",source:liveSource};CUR_ID="session-1";');
  rendered = []; rebuilds = 0; writes = [];
}
(async () => {
  resetSession();
  contents += JSON.stringify(record('second')) + '\n';
  await run('refreshSession(true)');
  assert.equal(run('CUR.entries.length'), 2);
  assert.equal(rendered.length, 1, 'Append only new entries so expanded content survives');
  assert.equal(rebuilds, 0);
  assert.equal(elements.get('#content').scrollTop, 300, 'Reading history must keep its scroll position');
  assert.equal(writes[0].id, 'session-1', 'Refresh must update the existing library record');
  const writeCount = writes.length;
  await run('refreshSession(true)');
  assert.equal(writes.length, writeCount, 'Unchanged sources should not render or write again');
  // Incomplete JSONL tails are retried on the next read, without dropping valid records.
  contents += '{"type":"assistant","sessionId":"session-1","message":{"content":"partial';
  await run('refreshSession(true)');
  assert.equal(run('CUR.entries.length'), 2);
  assert.equal(run('CUR.bad'), 1);
  contents += ' complete"}}\n';
  elements.get('#content').scrollTop = 1500;
  await run('refreshSession(true)');
  assert.equal(run('CUR.entries.length'), 3);
  assert.equal(run('CUR.bad'), 0);
  assert.equal(elements.get('#content').scrollTop, 2000, 'Readers at the bottom follow new content');
  // Rewrites replace the rendered transcript, and keep a stable cache key.
  contents = JSON.stringify(record('rewritten'));
  await run('refreshSession(true)');
  assert.equal(rebuilds, 1);
  assert.equal(run('CUR_ID'), 'session-1');
  // Auto refresh runs at a fixed interval for a visible viewer with a live source.
  run('scheduleRefresh()');
  assert.equal(timerDelay, 5000);
  assert.equal(typeof timer, 'function');
  context.document.hidden = true;
  run('scheduleRefresh()');
  assert.equal(timer, null);
  context.document.hidden = false;
  elements.get('#library').classList.toggle('hide', false);
  run('scheduleRefresh()');
  assert.equal(timer, null);
  elements.get('#library').classList.toggle('hide', true);
  // A lost permission stops polling and allows the user to reconnect.
  context.CUR.source = {getFile: async () => { throw new Error('permission revoked'); }};
  await run('refreshSession(true)');
  assert.equal(context.CUR.source, null);
  assert.equal(elements.get('#refreshStatus').textContent, 'refreshFailed');
  // Reconnecting the wrong file must not overwrite a session.
  context.window.showOpenFilePicker = async () => [{getFile: async () => ({name: 'wrong.jsonl', text: async () => JSON.stringify(record('wrong', 'session-2'))})}];
  context.self.isSecureContext = true;
  await run('refreshSession(true)');
  assert.equal(run('CUR.sum.sessionId'), 'session-1');
  assert.equal(elements.get('#refreshStatus').textContent, 'refreshWrongFile');
  // Pending reads are isolated from session switches and duplicate refreshes.
  resetSession();
  let release;
  context.CUR.source = {getFile: () => new Promise(resolve => { release = resolve; })};
  const pending = run('refreshSession(true)');
  await run('refreshSession(true)');
  const switched = {sum: {sessionId: 'session-2'}, source: null};
  context.CUR = switched;
  release({name: 'live.jsonl', text: async () => contents});
  await pending;
  assert.equal(context.CUR, switched);
  assert.equal(writes.length, 0, 'A stale refresh must not update the new session or cache');
  assert.ok(reads >= 5);
  // Base64 images must open in the in-page dialog, without data-URL navigation.
  const listeners = new Map();
  const dialog = {open: false, setAttribute() {}, showModal() { this.open = true; }, close() { this.open = false; },
    addEventListener: (name, fn) => listeners.set('dialog:' + name, fn)};
  const preview = {removeAttribute(name) { delete this[name]; }};
  const closeButton = {};
  elements.set('#imagePreview', dialog);elements.set('#previewImage', preview);elements.set('#closeImagePreview', closeButton);
  elements.get('#stream').addEventListener = (name, fn) => listeners.set('stream:' + name, fn);
  context.el = () => ({setAttribute() {}});
  context.window.open = () => assert.fail('Image preview must not navigate to a data URL');
  run(template.split('\n').find(line => line.startsWith('const safeImg=')));
  run(template.slice(template.indexOf('function imgEl('), template.indexOf('function resultContent(')));
  run(template.slice(template.indexOf('const imagePreview='), template.indexOf('/* 粘贴文本 */')));
  const image = run('imgEl(imageSource({type:"base64",media_type:"image/png",data:"example"}))');
  assert.equal(image.src, 'data:image/png;base64,example');
  listeners.get('stream:click')({target: {closest: () => image}, preventDefault() {}});
  assert.equal(dialog.open, true);
  assert.equal(preview.src, image.src);
  closeButton.onclick();
  listeners.get('dialog:close')();
  assert.equal(dialog.open, false);
  assert.equal(preview.src, undefined);
  assert.equal(run('imageSource({type:"url",url:"https://example.com/image.png"})'), 'https://example.com/image.png');
  console.log('Image preview: base64/URL sources, in-page display, close and resource cleanup passed.');
  console.log('Viewer runtime: append/rewrite, cache identity, unchanged/partial files, scroll, scheduling, revoked access, wrong-file reconnect and session-switch race passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
