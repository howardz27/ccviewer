// Run without dependencies: node tests/analytics.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('claude-code-session-viewer/src/analytics.js', 'utf8');
const strings = Object.fromEntries(['Settings', 'Accept', 'Reject', 'Notice', 'Privacy'].map(x => ['analytics' + x, x]));

function page(options = {}) {
  const listeners = {};
  const store = new Map();
  const nodes = [];
  if (options.choice) store.set('ccviewer_analytics_v1', JSON.stringify({choice: options.choice, at: options.at ?? Date.now()}));
  const element = tag => ({tag, children: [], hidden: false, setAttribute() {}, focus() {},
    appendChild(child) { this.children.push(child); nodes.push(child); }});
  const head = element('head');
  const body = element('body');
  let reloads = 0;
  const window = {addEventListener(name, fn) { listeners[name] = fn; }};
  const context = {window, document: {head, body, createElement: element, addEventListener(name, fn) {listeners[name] = fn;}},
    location: {protocol: options.protocol || 'https:', hostname: options.host || 'ccviewer.top', search: options.search || '', hash: options.hash || '', reload() {reloads++;}},
    navigator: {doNotTrack: options.dnt, globalPrivacyControl: options.gpc},
    localStorage: {getItem(k) {if(options.blockStorage) throw Error('blocked'); return store.get(k) ?? null;}, setItem(k,v) {if(options.blockStorage) throw Error('blocked'); store.set(k,v);}}};
  vm.runInNewContext(source.replace('__CONFIG__', JSON.stringify({projectId: options.id ?? 'test123', allowedHosts: ['ccviewer.top']})).replace('__STRINGS__', JSON.stringify(strings)), context);
  if(options.privateFirst) window.ccviewerAnalytics.privateView();
  listeners.DOMContentLoaded();
  return {window, nodes, head, listeners, store,
    scripts: () => head.children.filter(x => x.tag === 'script'),
    click: text => {const btn = nodes.find(n => n.tag === 'button' && n.textContent === text); assert.ok(btn, text); btn.onclick();},
    calls: () => Array.from(window.clarity?.q || [], x => Array.from(x)),
    reloads: () => reloads};
}

for (const config of [{id: ''}, {host:'localhost'}, {protocol:'file:'}, {protocol:'http:'}, {dnt:'1'}, {gpc:true}, {search:'?secret=value'}, {hash:'#private'}, {host:'preview.example'}]) {
  const p = page({...config, choice:'granted'});
  assert.equal(p.scripts().length, 0);
  assert.equal(p.nodes.some(x => x.className === 'analytics-banner'), false);
}
const p = page();
assert.equal(p.scripts().length, 0, 'no SDK before permission');
p.click('Accept');
assert.equal(p.scripts().length, 1);
assert.equal(p.scripts()[0].src, 'https://www.clarity.ms/tag/test123');
assert.equal(p.calls()[0][0], 'consentv2');
assert.equal(p.calls()[0][1].ad_Storage, 'denied');
assert.equal(p.calls()[0][1].analytics_Storage, 'granted');
p.window.ccviewerAnalytics.event('file_picker_open');
p.window.ccviewerAnalytics.event('/Users/secret/project');
assert.equal(p.calls().filter(x => x[0] === 'event').length, 1, 'only allowlisted event names');
p.window.ccviewerAnalytics.privateView();
assert.equal(p.calls().at(-1)[0], 'stop');
const count = p.calls().length;
p.window.ccviewerAnalytics.event('github_open');
p.click('Settings'); p.click('Accept');
assert.equal(p.calls().length, count, 'private view never restarts recording');
assert.equal(p.scripts().length, 1, 'no duplicate tag');
p.click('Settings'); p.click('Reject');
assert.equal(p.reloads(), 1, 'withdrawal unloads downloaded code, including after private mode');
assert.equal(p.calls().at(-1)[1].analytics_Storage, 'denied');

const rejected = page(); rejected.click('Reject');
assert.equal(rejected.scripts().length, 0);
assert.equal(JSON.parse(rejected.store.get('ccviewer_analytics_v1')).choice, 'denied');
assert.equal(page({choice:'denied'}).scripts().length, 0);
assert.equal(page({choice:'granted'}).scripts().length, 1);
assert.equal(page({choice:'granted', at:0}).scripts().length, 0, 'expired consent');
assert.equal(page({choice:'granted', at:Date.now()+100000}).scripts().length, 0, 'invalid future consent');
assert.equal(page({choice:'granted', privateFirst:true}).scripts().length, 0, 'private mode before DOM ready');
const blocked = page({blockStorage:true}); blocked.click('Accept');
assert.equal(blocked.scripts().length, 1, 'blocked localStorage does not break the page');
const sibling = page({choice:'granted'}); sibling.store.clear(); sibling.listeners.storage({key:'ccviewer_analytics_v1'});
assert.equal(sibling.reloads(), 1, 'cross-tab withdrawal');
console.log('Analytics: consent, production guards, event allowlist, private mode, expiry and withdrawal passed.');
