// No dependencies: node --test tests/cloud-backup.mjs
import {test} from 'node:test';
import assert from 'node:assert/strict';
import worker from '../worker/index.mjs';
const MAX_FILE_BYTES = 20 * 1024 * 1024;

class Bucket {
  values = new Map();
  async put(key, value, options = {}) {
    const bytes = typeof value === 'string' ? new TextEncoder().encode(value) : value.slice();
    const object = {key, size: bytes.length, uploaded: new Date(), customMetadata: options.customMetadata || {}, bytes};
    this.values.set(key, object);
    return object;
  }
  async get(key) {
    const object = this.values.get(key);
    return object ? {...object, body: new Blob([object.bytes]).stream(), json: async () => JSON.parse(new TextDecoder().decode(object.bytes))} : null;
  }
  async delete(key) { this.values.delete(key); }
  async list({prefix, cursor, limit}) {
    const objects = [...this.values.values()].filter(o => o.key.startsWith(prefix)).sort((a, b) => a.key.localeCompare(b.key));
    const offset = Number(cursor || 0), truncated = offset + limit < objects.length;
    return {objects: objects.slice(offset, offset + limit), truncated, cursor: truncated ? String(offset + limit) : undefined};
  }
}
const origin = 'https://ccviewer.test';
const fixture = '{"type":"user","message":{"content":"你好"}}\r\n{"type":"assistant","message":{"content":"hello"}}\n';
function environment() {
  return {BACKUPS: new Bucket(), GITHUB_CLIENT_ID: 'test-client', GITHUB_CLIENT_SECRET: 'test-secret', APP_ORIGIN: origin,
    ASSETS: {fetch: async () => new Response('static viewer')}};
}
function request(env, path, {token, method = 'GET', body, headers = {}, sameOrigin = true} = {}) {
  const options = {method, headers: {...(token ? {Cookie: '__Host-ccviewer_session=' + token} : {}), ...headers}};
  if (method !== 'GET' && sameOrigin) { options.headers.Origin = origin; options.headers['X-CCViewer-Request'] = '1'; }
  if (body !== undefined) { options.body = body; options.duplex = 'half'; }
  return worker.fetch(new Request(origin + path, options), env);
}
async function sha(value) {
  return Buffer.from(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value))).toString('base64url');
}
async function signIn(env, id = '101', expires = Date.now() + 60000) {
  const token = Buffer.from(crypto.getRandomValues(new Uint8Array(32))).toString('base64url');
  await env.BACKUPS.put('auth/sessions/' + await sha(token), JSON.stringify({user: {id, login: 'user-' + id}, expires}));
  return token;
}
async function upload(env, token, body = fixture, name = '会话.jsonl', headers) {
  return request(env, '/api/backups?name=' + encodeURIComponent(name), {token, method: 'POST', body, headers});
}
test('static viewer and disabled cloud remain usable without credentials', async () => {
  const env = environment(); delete env.GITHUB_CLIENT_SECRET;
  assert.equal(await (await request(env, '/claude-code-session-viewer/')).text(), 'static viewer');
  assert.deepEqual(await (await request(env, '/api/auth/session')).json(), {enabled: false, user: null, maxFileBytes: MAX_FILE_BYTES});
  assert.equal((await request(env, '/api/auth/github')).status, 503);
});
test('all backup operations require authentication; tampered and expired sessions fail', async () => {
  const env = environment(), expired = await signIn(env, '101', Date.now() - 1);
  for (const token of [undefined, 'a'.repeat(43), expired]) {
    assert.equal((await request(env, '/api/backups', {token})).status, 401);
    assert.equal((await upload(env, token)).status, 401);
    assert.equal((await request(env, '/api/backups/' + crypto.randomUUID(), {token})).status, 401);
    assert.equal((await request(env, '/api/backups/' + crypto.randomUUID(), {token, method: 'DELETE'})).status, 401);
  }
});
test('round trip preserves original UTF-8 bytes, metadata, owner privacy and deletion', async () => {
  const env = environment(), alice = await signIn(env), bob = await signIn(env, '202');
  const description = '排查记录 💡\n第二行';
  const response = await upload(env, alice, fixture, '会话.jsonl', {'X-CCViewer-Description': encodeURIComponent(description)});
  assert.equal(response.status, 201);
  const {backup} = await response.json();
  assert.equal(backup.name, '会话.jsonl'); assert.equal(backup.records, 2);
  assert.equal(backup.description, description);
  assert.equal(backup.size, new TextEncoder().encode(fixture).length);
  assert.deepEqual((await (await request(env, '/api/backups', {token: alice})).json()).backups, [backup]);
  assert.equal((await (await request(env, '/api/backups', {token: bob})).json()).backups.length, 0);
  const file = await request(env, '/api/backups/' + backup.id, {token: alice});
  assert.equal(await file.text(), fixture);
  assert.equal(file.headers.get('Cache-Control'), 'no-store');
  assert.match(file.headers.get('Content-Disposition'), /filename\*=UTF-8''%E4/);
  assert.equal((await request(env, '/api/backups/' + backup.id, {token: bob})).status, 404);
  await request(env, '/api/backups/' + backup.id, {token: bob, method: 'DELETE'});
  assert.equal((await request(env, '/api/backups/' + backup.id, {token: alice})).status, 200, 'another account cannot delete Alice’s backup');
  assert.equal((await request(env, '/api/backups/' + backup.id + '?owner=101', {token: bob})).status, 404);
  await request(env, '/api/backups/' + backup.id, {token: alice, method: 'DELETE'});
  assert.equal((await request(env, '/api/backups/' + backup.id, {token: alice})).status, 404);
});
test('mutations reject cross-origin requests and requests missing the custom header', async () => {
  const env = environment(), token = await signIn(env);
  for (const headers of [{}, {Origin: 'https://evil.test', 'X-CCViewer-Request': '1'}, {Origin: origin}, {'X-CCViewer-Request': '1'}]) {
    assert.equal((await request(env, '/api/backups?name=a.jsonl', {token, method: 'POST', body: fixture, sameOrigin: false, headers})).status, 403);
    assert.equal((await request(env, '/api/auth/logout', {token, method: 'POST', sameOrigin: false, headers})).status, 403);
  }
  assert.equal((await request(env, '/api/backups', {token, headers: {'Sec-Fetch-Site': 'cross-site'}})).status, 403);
});
test('server validates JSONL, UTF-8, filename and description before storing any file', async () => {
  const env = environment(), token = await signIn(env);
  for (const body of ['', ' \n ', '[]', '[{}]', 'null', 'true', '1', '{}\n{broken', new Uint8Array([0xff])]) {
    assert.equal((await upload(env, token, body)).status, 400);
  }
  for (const name of ['session.txt', '../session.jsonl', 'a\\b.jsonl', 'a\n.jsonl', '中'.repeat(80) + '.jsonl']) {
    assert.equal((await upload(env, token, fixture, name)).status, 400);
  }
  for (const encoded of ['%ZZ', 'a%00b', 'a'.repeat(501), encodeURIComponent('中'.repeat(501))]) {
    const response = await upload(env, token, fixture, '会话.jsonl', {'X-CCViewer-Description': encoded});
    assert.equal(response.status, 400);
    assert.equal((await response.json()).error, 'invalid_description');
  }
  assert.equal((await env.BACKUPS.list({prefix: 'backups/', limit: 100})).objects.length, 0);
});
test('size checks include bodies with no Content-Length or an incorrect length', async () => {
  const env = environment(), token = await signIn(env);
  assert.equal((await request(env, '/api/backups?name=a.jsonl', {token, method: 'POST', body: fixture,
    headers: {'Content-Length': String(MAX_FILE_BYTES + 1)}})).status, 413);
  let cancelled = false;
  const stream = new ReadableStream({start(controller) { controller.enqueue(new Uint8Array(MAX_FILE_BYTES)); controller.enqueue(new Uint8Array(1)); }, cancel() { cancelled = true; }});
  assert.equal((await upload(env, token, stream)).status, 413);
  assert.equal(cancelled, true);
});
test('pagination follows cursors and never returns another account’s objects', async () => {
  const env = environment(), token = await signIn(env);
  for (let i = 0; i < 105; i++) await env.BACKUPS.put('backups/github-101/' + crypto.randomUUID() + '.jsonl', '{}', {customMetadata: {name: 'a.jsonl'}});
  await env.BACKUPS.put('backups/github-202/' + crypto.randomUUID() + '.jsonl', '{}');
  const first = await (await request(env, '/api/backups', {token})).json();
  assert.equal(first.backups.length, 100); assert.ok(first.cursor);
  assert.equal(first.backups[0].description, '', 'backups without a stored description still list normally');
  const next = await (await request(env, '/api/backups?cursor=' + first.cursor, {token})).json();
  assert.equal(next.backups.length, 5); assert.equal(next.cursor, null);
  assert.equal(new Set([...first.backups, ...next.backups].map(b => b.id)).size, 105);
});
test('logout revokes the session on the server and clears its secure cookie', async () => {
  const env = environment(), token = await signIn(env);
  assert.ok((await (await request(env, '/api/auth/session', {token})).json()).user);
  const logout = await request(env, '/api/auth/logout', {token, method: 'POST'});
  assert.match(logout.headers.get('Set-Cookie'), /Max-Age=0/);
  assert.match(logout.headers.get('Set-Cookie'), /HttpOnly; SameSite=Lax/);
  assert.match(logout.headers.get('Set-Cookie'), /Secure/);
  assert.equal((await request(env, '/api/backups', {token})).status, 401);
});
test('OAuth binds state to the browser, uses PKCE and accepts only local return paths', async () => {
  const env = environment();
  const login = await request(env, '/api/auth/github?returnTo=https://evil.test/');
  const auth = new URL(login.headers.get('Location'));
  assert.equal(auth.origin, 'https://github.com');
  assert.equal(auth.searchParams.get('scope'), '');
  assert.equal(auth.searchParams.get('code_challenge_method'), 'S256');
  assert.equal(auth.searchParams.get('redirect_uri'), origin + '/api/auth/github/callback');
  const state = auth.searchParams.get('state');
  const flow = await (await env.BACKUPS.get('auth/flows/' + await sha(state))).json();
  assert.equal(flow.returnTo, '/claude-code-session-viewer/');
  assert.equal(await sha(flow.verifier), auth.searchParams.get('code_challenge'));
  for (const headers of [{}, {Cookie: '__Host-ccviewer_oauth=' + 'b'.repeat(43)}]) {
    const result = await request(env, '/api/auth/github/callback?code=test&state=' + state, {headers});
    assert.match(result.headers.get('Location'), /cloud=login_failed/);
  }
});
test('OAuth callback creates a fresh revocable session without persisting provider tokens', async () => {
  const env = environment(), old = await signIn(env);
  const login = await request(env, '/api/auth/github?returnTo=/claude-code-session-viewer/zh/');
  const state = new URL(login.headers.get('Location')).searchParams.get('state');
  const fetchOriginal = globalThis.fetch;
  const calls = [];
  globalThis.fetch = async (url, options) => {
    calls.push({url, options});
    return Response.json(url.includes('access_token') ? {access_token: 'provider-secret-token'} : {id: 303, login: 'new-user'});
  };
  try {
    const headers = {Cookie: '__Host-ccviewer_oauth=' + state + '; __Host-ccviewer_session=' + old};
    const response = await request(env, '/api/auth/github/callback?code=test&state=' + state, {headers});
    assert.equal(response.headers.get('Location'), '/claude-code-session-viewer/zh/?cloud=ready');
    const value = response.headers.get('Set-Cookie').match(/__Host-ccviewer_session=([A-Za-z0-9_-]{43})/)[1];
    assert.equal((await (await request(env, '/api/auth/session', {token: value})).json()).user.id, '303');
    assert.equal((await request(env, '/api/backups', {token: old})).status, 401);
    assert.ok(calls[0].options.body.get('code_verifier'));
    assert.equal(calls[1].options.headers.Authorization, 'Bearer provider-secret-token');
    assert.ok([...env.BACKUPS.values.values()].every(o => !new TextDecoder().decode(o.bytes).includes('provider-secret-token')));
    const replay = await request(env, '/api/auth/github/callback?code=test&state=' + state, {headers});
    assert.match(replay.headers.get('Location'), /cloud=login_failed/);
    assert.equal(calls.length, 2, 'a consumed OAuth flow must not exchange again');
  } finally { globalThis.fetch = fetchOriginal; }
});
test('expired OAuth flow, provider denial and upstream failure return to the local app', async () => {
  for (const scenario of ['expired', 'denied', 'upstream']) {
    const env = environment();
    const login = await request(env, '/api/auth/github?returnTo=/claude-code-session-viewer/ja/');
    const state = new URL(login.headers.get('Location')).searchParams.get('state');
    if (scenario === 'expired') {
      const key = 'auth/flows/' + await sha(state), flow = await (await env.BACKUPS.get(key)).json();
      await env.BACKUPS.put(key, JSON.stringify({...flow, expires: Date.now() - 1}));
    }
    const original = globalThis.fetch; globalThis.fetch = async () => { throw Error('upstream failed'); };
    try {
      const response = await request(env, '/api/auth/github/callback?state=' + state + (scenario === 'denied' ? '&error=access_denied' : '&code=test'),
        {headers: {Cookie: '__Host-ccviewer_oauth=' + state}});
      assert.equal(response.headers.get('Location'), '/claude-code-session-viewer/ja/?cloud=login_failed');
      assert.equal((await env.BACKUPS.list({prefix: 'auth/sessions/', limit: 100})).objects.length, 0);
    } finally { globalThis.fetch = original; }
  }
});
