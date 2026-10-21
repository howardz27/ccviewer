// Markdown exports must bundle image files that ordinary Markdown readers can resolve.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const {spawnSync} = require('node:child_process');
const template = fs.readFileSync('claude-code-session-viewer/src/template.html', 'utf8');
const context = {CUR: null, SHOW_TOOL: true, SHOW_THINK: true, t: key => key, atob, Blob, TextEncoder};
vm.createContext(context);
vm.runInContext([
  template.split('\n').find(line => line.startsWith('const safeImg=')),
  template.slice(template.indexOf('function imageSource('), template.indexOf('function resultContent(')),
  template.slice(template.indexOf('function isInjectedText('), template.indexOf('const PLACEHOLDER_RENDER=')),
  template.slice(template.indexOf('/* ---------- 导出 Markdown'), template.indexOf('function exportMd(')),
].join('\n'), context);
const run = code => vm.runInContext(code, context);
const png = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNQXlDwHwAEUAIzrIcBOQAAAABJRU5ErkJggg==';
const embedded = {type: 'image', source: {type: 'base64', media_type: 'image/png', data: png}};
const remote = {type: 'image', source: {type: 'url', url: 'https://example.com/image.png'}};
const entry = (type, content) => ({type, message: {content}});
function markdown(entries) {
  context.CUR = {name: 'images.jsonl', sum: {tokens: {in: 0, out: 0}}, entries};
  context.exportImages = [];
  return run('buildMd(exportImages)');
}
const fileImage = /!\[[^\]]*\]\(images\/image-\d+\.png\)/;
assert.equal(run('buildMd()'), null);
let output = markdown([entry('user', [embedded])]);
assert.match(output, /## 🧑 you/);
assert.match(output, fileImage, 'An image-only user message must be exported');
assert.deepEqual(Buffer.from(context.exportImages[0].data), Buffer.from(png, 'base64'), 'Decoded image bytes must be preserved');
assert.ok(!output.includes('data:image'), 'The Markdown must use file paths, not data URLs');
output = markdown([entry('user', [{type: 'text', text: 'before'}, embedded, {type: 'text', text: 'after'}, remote])]);
assert.ok(output.indexOf('before') < output.indexOf('images/image-1.png'));
assert.ok(output.indexOf('images/image-1.png') < output.indexOf('after'));
assert.match(output, /!\[[^\]]*\]\(https:\/\/example.com\/image.png\)/);
output = markdown([entry('assistant', [embedded, {type: 'text', text: 'description'}, remote])]);
assert.match(output, fileImage, 'Assistant images must be exported');
assert.ok(output.indexOf('images/image-1.png') < output.indexOf('description'));
assert.ok(output.indexOf('description') < output.indexOf('https://example.com/image.png'));
output = markdown([entry('assistant', [embedded])]);
assert.match(output, /## 🤖 reply/);
assert.match(output, fileImage);
const result = {type: 'tool_result', content: [{type: 'text', text: 'screenshot'}, embedded, remote]};
output = markdown([entry('user', [result])]);
assert.match(output, fileImage, 'Successful tool results must retain images');
assert.ok(output.includes('https://example.com/image.png'));
output = markdown([entry('user', [{...result, is_error: true, content: [{type: 'text', text: 'x'.repeat(3000)}, embedded]}])]);
assert.match(output, /❌ error/);
assert.match(output, fileImage, 'Error preview truncation must not truncate image data');
assert.ok(!output.includes(png), 'Images must not also appear as raw JSON');
assert.deepEqual(Buffer.from(context.exportImages[0].data), Buffer.from(png, 'base64'));
context.SHOW_TOOL = false;
context.SHOW_THINK = false;
output = markdown([entry('user', [embedded]), entry('assistant', [embedded]), entry('user', [result])]);
assert.equal((output.match(/images\/image-\d+\.png/g) || []).length, 2, 'Tool visibility must not hide user/assistant images');
context.SHOW_TOOL = true;
output = markdown([entry('user', [{type: 'image', source: {type: 'url', url: 'https://example.com/a (1).png'}}])]);
assert.match(output, /https:\/\/example.com\/a%20%281%29.png/, 'URL punctuation must not break Markdown image syntax');
output = markdown([entry('user', [{type: 'image', source: {type: 'url', url: 'javascript:alert(1)'}}])]);
assert.ok(!output.includes('javascript:'));
output = markdown([entry('user', 'plain prompt'), entry('assistant', 'plain reply')]);
assert.match(output, /## 🧑 you\n\nplain prompt/);
assert.match(output, /## 🤖 reply\n\nplain reply/);

// Exercise the download handler and validate the archive with an independent ZIP reader.
const downloads = [], blobs = [], revoked = [], deferred = [];
context.document = {
  createElement: () => ({click() { downloads.push(this.download); }, remove() {}}),
  body: {appendChild() {}},
};
context.URL = {
  createObjectURL(blob) { blobs.push(blob); return 'blob:export-' + blobs.length; },
  revokeObjectURL(url) { revoked.push(url); },
};
context.setTimeout = fn => deferred.push(fn);
context.alert = () => assert.fail('A valid session should export successfully');
vm.runInContext(template.slice(template.indexOf('function exportMd('), template.indexOf("$('#btnExportMd').onclick")), context);
(async () => {
  markdown([
    entry('user', [{type: 'text', text: 'before image'}, embedded]),
    entry('assistant', [embedded, remote]),
    entry('user', [result]),
  ]);
  context.CUR.sum.title = '图片会话';
  run('exportMd()');
  assert.equal(downloads.at(-1), '图片会话.zip');
  assert.equal(blobs.at(-1).type, 'application/zip');
  const validation = spawnSync('python3', ['-c', `
import base64, io, re, sys, zipfile
with zipfile.ZipFile(io.BytesIO(sys.stdin.buffer.read())) as archive:
    assert archive.testzip() is None, 'ZIP integrity check failed'
    assert archive.namelist() == ['图片会话.md', 'images/image-1.png', 'images/image-2.png', 'images/image-3.png']
    md = archive.read('图片会话.md').decode('utf-8')
    refs = re.findall(r'!\\[Image\\]\\((images/[^)]+)\\)', md)
    assert len(refs) == 3
    for path in refs:
        assert archive.read(path) == base64.b64decode('${png}'), 'Image bytes differ'
    assert 'data:image' not in md
    assert 'https://example.com/image.png' in md
print('ZIP contents, UTF-8 filenames, CRCs, relative image links and decoded image bytes passed.')
`], {input: Buffer.from(await blobs.at(-1).arrayBuffer()), encoding: 'utf8'});
  assert.equal(validation.status, 0, validation.stderr);
  process.stdout.write(validation.stdout);

  markdown([entry('user', 'plain prompt'), entry('assistant', 'plain reply')]);
  run('exportMd()');
  assert.equal(downloads.at(-1), 'images.md', 'Text-only exports stay as a single Markdown file');
  assert.equal(blobs.at(-1).type, 'text/markdown;charset=utf-8');
  assert.match(await blobs.at(-1).text(), /plain reply/);
  markdown([entry('user', [remote])]);
  run('exportMd()');
  assert.equal(downloads.at(-1), 'images.md', 'Network images retain their original URLs');
  assert.match(await blobs.at(-1).text(), /https:\/\/example.com\/image.png/);
  deferred.forEach(fn => fn());
  assert.equal(revoked.length, downloads.length, 'Download object URLs must be released');
  console.log('Markdown export: image files, user/assistant/tool images, ordering, visibility and download behavior passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
