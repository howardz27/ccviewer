// Markdown export must retain images without separate asset downloads.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const template = fs.readFileSync('claude-code-session-viewer/src/template.html', 'utf8');
const context = {CUR: null, SHOW_TOOL: true, SHOW_THINK: true, t: key => key};
vm.createContext(context);
vm.runInContext([
  template.split('\n').find(line => line.startsWith('const safeImg=')),
  template.slice(template.indexOf('function imageSource('), template.indexOf('function resultContent(')),
  template.slice(template.indexOf('function isInjectedText('), template.indexOf('const PLACEHOLDER_RENDER=')),
  template.slice(template.indexOf('/* ---------- 导出 Markdown'), template.indexOf('function exportMd(')),
].join('\n'), context);
const run = code => vm.runInContext(code, context);
const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=';
const embedded = {type: 'image', source: {type: 'base64', media_type: 'image/png', data: png}};
const remote = {type: 'image', source: {type: 'url', url: 'https://example.com/image.png'}};
const entry = (type, content) => ({type, message: {content}});
function markdown(entries) {
  context.CUR = {name: 'images.jsonl', sum: {tokens: {in: 0, out: 0}}, entries};
  return run('buildMd()');
}
const dataImage = /!\[[^\]]*\]\(data:image\/png;base64,[^)]+\)/;
assert.equal(run('buildMd()'), null);
let output = markdown([entry('user', [embedded])]);
assert.match(output, /## 🧑 you/);
assert.match(output, dataImage, 'An image-only user message must be exported');
assert.ok(output.includes(png), 'Base64 bytes must be preserved');
output = markdown([entry('user', [{type: 'text', text: 'before'}, embedded, {type: 'text', text: 'after'}, remote])]);
assert.ok(output.indexOf('before') < output.indexOf('data:image/png'));
assert.ok(output.indexOf('data:image/png') < output.indexOf('after'));
assert.match(output, /!\[[^\]]*\]\(https:\/\/example.com\/image.png\)/);
output = markdown([entry('assistant', [embedded, {type: 'text', text: 'description'}, remote])]);
assert.match(output, dataImage, 'Assistant images must be exported');
assert.ok(output.indexOf('data:image/png') < output.indexOf('description'));
assert.ok(output.indexOf('description') < output.indexOf('https://example.com/image.png'));
output = markdown([entry('assistant', [embedded])]);
assert.match(output, /## 🤖 reply/);
assert.match(output, dataImage);
const result = {type: 'tool_result', content: [{type: 'text', text: 'screenshot'}, embedded, remote]};
output = markdown([entry('user', [result])]);
assert.match(output, dataImage, 'Successful tool results must retain images');
assert.ok(output.includes('https://example.com/image.png'));
output = markdown([entry('user', [{...result, is_error: true, content: [{type: 'text', text: 'x'.repeat(3000)}, embedded]}])]);
assert.match(output, /❌ error/);
assert.match(output, dataImage, 'Error preview truncation must not truncate image data');
assert.equal(output.split(png).length - 1, 1, 'Images must not also appear as raw JSON');
context.SHOW_TOOL = false;
context.SHOW_THINK = false;
output = markdown([entry('user', [embedded]), entry('assistant', [embedded]), entry('user', [result])]);
assert.equal((output.match(/data:image\/png/g) || []).length, 2, 'Tool visibility must not hide user/assistant images');
context.SHOW_TOOL = true;
output = markdown([entry('user', [{type: 'image', source: {type: 'url', url: 'https://example.com/a (1).png'}}])]);
assert.match(output, /https:\/\/example.com\/a%20%281%29.png/, 'URL punctuation must not break Markdown image syntax');
output = markdown([entry('user', [{type: 'image', source: {type: 'url', url: 'javascript:alert(1)'}}])]);
assert.ok(!output.includes('javascript:'));
output = markdown([entry('user', 'plain prompt'), entry('assistant', 'plain reply')]);
assert.match(output, /## 🧑 you\n\nplain prompt/);
assert.match(output, /## 🤖 reply\n\nplain reply/);
console.log('Markdown export: user/assistant/tool images, image-only messages, ordering, complete base64 data, URL escaping and visibility passed.');
