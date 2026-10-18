// Run without dependencies: node tests/analytics.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('claude-code-session-viewer/src/analytics.js', 'utf8');

function page(options = {}) {
  const scripts = [];
  const listeners = {};
  const window = {};
  const anchor = {parentNode: {insertBefore(script) { scripts.push(script); }}};
  const context = {
    window,
    document: {
      createElement: tag => ({tag}),
      getElementsByTagName: () => [anchor],
      addEventListener(name, handler) { listeners[name] = handler; }
    },
    location: {protocol: options.protocol || 'https:', hostname: options.host || 'ccviewer.top', search: options.search || '', hash: options.hash || ''},
    navigator: {doNotTrack: '1', globalPrivacyControl: true},
    get localStorage() { throw Error('Analytics must not depend on a saved consent choice'); }
  };
  vm.runInNewContext(source.replace('__CONFIG__', JSON.stringify({projectId: options.id ?? 'test123', allowedHosts: ['ccviewer.top']})), context);
  return {window, scripts, listeners, calls: () => Array.from(window.clarity?.q || [], x => Array.from(x))};
}

const p = page();
assert.equal(p.scripts.length, 1, 'load immediately without consent UI or DOM ready');
assert.equal(p.scripts[0].src, 'https://www.clarity.ms/tag/test123');
assert.equal(p.scripts[0].async, 1);
assert.equal(p.calls().length, 0, 'do not manufacture consent signals');
p.window.ccviewerAnalytics.event('file_picker_open');
p.window.ccviewerAnalytics.event('folder_picker_open');
p.window.ccviewerAnalytics.event('paste_open');
const link = {hostname: 'github.com', hasAttribute: () => true};
p.listeners.click({target: {closest: () => link}});
assert.deepEqual(p.calls().map(x => x[1]), ['file_picker_open', 'folder_picker_open', 'paste_open', 'help_open', 'github_open']);
p.window.ccviewerAnalytics.event('/Users/secret/project');
assert.equal(p.calls().length, 5);
assert.equal(page({search: '?utm_source=test', hash: '#session'}).scripts.length, 1, 'query strings and fragments do not disable analytics');
for (const options of [{id: ''}, {id:'invalid/id'}, {host:'localhost'}, {host:'preview.example'}, {protocol:'file:'}, {protocol:'http:'}]) {
  const other = page(options);
  assert.equal(other.scripts.length, 0);
  other.window.ccviewerAnalytics.event('paste_open');
  assert.equal(other.window.clarity, undefined, 'local viewer event calls remain safe without SDK');
}
console.log('Analytics: automatic tag loading, entry events and deployment configuration passed.');
