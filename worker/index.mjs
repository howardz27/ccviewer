// Private backups and GitHub OAuth. Static/offline viewing never calls this API.
const MAX_FILE_BYTES = 20 * 1024 * 1024;
const MAX_DESCRIPTION_LENGTH = 500;
const SESSION_SECONDS = 7 * 24 * 60 * 60;
const FLOW_SECONDS = 10 * 60;
const APP_PATH = '/claude-code-session-viewer/';
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
const TOKEN = /^[A-Za-z0-9_-]{43}$/;
const encoder = new TextEncoder();

class ApiError extends Error {
  constructor(status, code) { super(code); this.status = status; }
}
function fail(status, code) { throw new ApiError(status, code); }
function json(data, status = 200) {
  return new Response(JSON.stringify(data), {status, headers: {'Content-Type': 'application/json; charset=utf-8'}});
}
function base64url(bytes) {
  return btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function randomToken() { return base64url(crypto.getRandomValues(new Uint8Array(32))); }
async function digest(value) { return base64url(await crypto.subtle.digest('SHA-256', encoder.encode(value))); }
function cookieName(request, kind) {
  return (new URL(request.url).protocol === 'https:' ? '__Host-' : '') + 'ccviewer_' + kind;
}
function cookie(request, kind, value, age) {
  return cookieName(request, kind) + '=' + value + '; Path=/; HttpOnly; SameSite=Lax; Max-Age=' + age +
    (new URL(request.url).protocol === 'https:' ? '; Secure' : '');
}
function readCookie(request, kind) {
  const name = cookieName(request, kind) + '=';
  return (request.headers.get('Cookie') || '').split(';').map(s => s.trim()).find(s => s.startsWith(name))?.slice(name.length) || '';
}
function redirect(location, cookies = []) {
  const headers = new Headers({Location: location});
  for (const value of cookies) headers.append('Set-Cookie', value);
  return new Response(null, {status: 303, headers});
}
function returnPath(value) {
  return /^\/claude-code-session-viewer\/(?:zh\/|ja\/|ko\/|es\/|fr\/|de\/|pt\/|ru\/|hi\/)?$/.test(value || '') ? value : APP_PATH;
}
function enabled(env) { return !!(env.BACKUPS && env.GITHUB_CLIENT_ID && env.GITHUB_CLIENT_SECRET); }
async function readRecord(bucket, key) {
  const object = await bucket.get(key);
  return object ? object.json() : null;
}
async function session(request, env) {
  const token = readCookie(request, 'session');
  if (!TOKEN.test(token) || !env.BACKUPS) return null;
  const key = 'auth/sessions/' + await digest(token);
  const record = await readRecord(env.BACKUPS, key);
  if (!record || record.expires <= Date.now() || !/^\d+$/.test(record.user?.id || '')) return null;
  return {...record, key};
}
function requireMethod(request, methods) {
  if (!methods.includes(request.method)) fail(405, 'method_not_allowed');
}
function requireSameOrigin(request) {
  if (request.headers.get('Origin') !== new URL(request.url).origin || request.headers.get('X-CCViewer-Request') !== '1') {
    fail(403, 'invalid_origin');
  }
}
// Bound the actual streamed body too: Content-Length is not a trusted size limit.
async function boundedBody(request) {
  if (Number(request.headers.get('Content-Length')) > MAX_FILE_BYTES) fail(413, 'file_too_large');
  if (!request.body) fail(400, 'invalid_jsonl');
  const reader = request.body.getReader(), chunks = [];
  let size = 0;
  try {
    while (true) {
      const {done, value} = await reader.read();
      if (done) break;
      size += value.byteLength;
      if (size > MAX_FILE_BYTES) { await reader.cancel(); fail(413, 'file_too_large'); }
      chunks.push(value);
    }
  } finally { reader.releaseLock(); }
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  let text;
  try { text = new TextDecoder('utf-8', {fatal: true}).decode(bytes); }
  catch { fail(400, 'invalid_jsonl'); }
  let records = 0;
  // Scan incrementally: splitting millions of tiny lines would allocate a large array.
  for (let start = 0; start < text.length;) {
    const newline = text.indexOf('\n', start);
    const end = newline === -1 ? text.length : newline;
    const line = text.slice(start, end);
    start = end + 1;
    if (!line.trim()) continue;
    try {
      const value = JSON.parse(line);
      if (!value || typeof value !== 'object' || Array.isArray(value)) fail(400, 'invalid_jsonl');
    } catch { fail(400, 'invalid_jsonl'); }
    records++;
  }
  if (!records) fail(400, 'invalid_jsonl');
  return {bytes, records};
}
async function github(url, options) {
  const response = await fetch(url, {...options, signal: AbortSignal.timeout(15000)});
  if (!response.ok) fail(502, 'login_failed');
  return response.json();
}
async function login(request, env, url) {
  requireMethod(request, ['GET']);
  if (!enabled(env)) fail(503, 'cloud_unavailable');
  const state = randomToken(), verifier = randomToken();
  const flow = {verifier, returnTo: returnPath(url.searchParams.get('returnTo')), expires: Date.now() + FLOW_SECONDS * 1000};
  await env.BACKUPS.put('auth/flows/' + await digest(state), JSON.stringify(flow));
  const auth = new URL('https://github.com/login/oauth/authorize');
  auth.search = new URLSearchParams({client_id: env.GITHUB_CLIENT_ID,
    redirect_uri: url.origin + '/api/auth/github/callback', state, scope: '',
    code_challenge: await digest(verifier), code_challenge_method: 'S256'}).toString();
  return redirect(auth.href, [cookie(request, 'oauth', state, FLOW_SECONDS)]);
}
async function callback(request, env, url) {
  requireMethod(request, ['GET']);
  if (!enabled(env)) fail(503, 'cloud_unavailable');
  const state = readCookie(request, 'oauth');
  const clear = cookie(request, 'oauth', '', 0);
  // The unpredictable state must be present in both this browser and the callback.
  if (!TOKEN.test(state) || state !== url.searchParams.get('state')) return redirect(APP_PATH + '?cloud=login_failed', [clear]);
  const flowKey = 'auth/flows/' + await digest(state);
  const flow = await readRecord(env.BACKUPS, flowKey);
  await env.BACKUPS.delete(flowKey);
  const target = returnPath(flow?.returnTo);
  if (!flow || flow.expires <= Date.now() || !url.searchParams.get('code') || url.searchParams.has('error')) {
    return redirect(target + '?cloud=login_failed', [clear]);
  }
  try {
    const token = await github('https://github.com/login/oauth/access_token', {
      method: 'POST', headers: {Accept: 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
      body: new URLSearchParams({client_id: env.GITHUB_CLIENT_ID, client_secret: env.GITHUB_CLIENT_SECRET,
        code: url.searchParams.get('code'), redirect_uri: url.origin + '/api/auth/github/callback', code_verifier: flow.verifier})
    });
    if (typeof token.access_token !== 'string' || !token.access_token) fail(502, 'login_failed');
    const profile = await github('https://api.github.com/user', {
      headers: {Accept: 'application/vnd.github+json', Authorization: 'Bearer ' + token.access_token, 'User-Agent': 'CCViewer'}
    });
    if (!Number.isSafeInteger(profile.id) || profile.id <= 0 || typeof profile.login !== 'string') fail(502, 'login_failed');
    const value = randomToken();
    const user = {id: String(profile.id), login: profile.login};
    await env.BACKUPS.put('auth/sessions/' + await digest(value), JSON.stringify({user, expires: Date.now() + SESSION_SECONDS * 1000}));
    // Rotate the previous session on login. GitHub access tokens stay server-side and are never stored.
    const previous = readCookie(request, 'session');
    if (TOKEN.test(previous)) await env.BACKUPS.delete('auth/sessions/' + await digest(previous));
    return redirect(target + '?cloud=ready', [clear, cookie(request, 'session', value, SESSION_SECONDS)]);
  } catch {
    return redirect(target + '?cloud=login_failed', [clear]);
  }
}
function backupInfo(object) {
  return {id: object.key.split('/').pop().replace(/\.jsonl$/, ''), name: object.customMetadata?.name || 'session.jsonl',
    size: object.size, uploaded: object.uploaded.toISOString(), records: Number(object.customMetadata?.records || 0),
    description: object.customMetadata?.description || ''};
}
function backupDescription(request) {
  const encoded = request.headers.get('X-CCViewer-Description') || '';
  if (encoded.length > MAX_DESCRIPTION_LENGTH * 9) fail(400, 'invalid_description');
  let description;
  try { description = decodeURIComponent(encoded).trim(); }
  catch { fail(400, 'invalid_description'); }
  if (description.length > MAX_DESCRIPTION_LENGTH || /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(description)) {
    fail(400, 'invalid_description');
  }
  return description;
}
async function api(request, env, url) {
  if (env.APP_ORIGIN && url.origin !== env.APP_ORIGIN) fail(403, 'invalid_origin');
  if (request.headers.get('Sec-Fetch-Site') === 'cross-site' && !url.pathname.startsWith('/api/auth/github/')) fail(403, 'invalid_origin');
  if (url.pathname === '/api/auth/github') return login(request, env, url);
  if (url.pathname === '/api/auth/github/callback') return callback(request, env, url);
  if (url.pathname === '/api/auth/session') {
    requireMethod(request, ['GET']);
    const current = enabled(env) ? await session(request, env) : null;
    return json({enabled: enabled(env), user: current?.user || null, maxFileBytes: MAX_FILE_BYTES});
  }
  if (url.pathname === '/api/auth/logout') {
    requireMethod(request, ['POST']); requireSameOrigin(request);
    const current = await session(request, env);
    if (current) await env.BACKUPS.delete(current.key);
    const response = json({ok: true});
    response.headers.append('Set-Cookie', cookie(request, 'session', '', 0));
    return response;
  }
  if (url.pathname !== '/api/backups' && !url.pathname.startsWith('/api/backups/')) fail(404, 'not_found');
  if (!enabled(env)) fail(503, 'cloud_unavailable');
  requireMethod(request, url.pathname === '/api/backups' ? ['GET', 'POST'] : ['GET', 'DELETE']);
  if (request.method !== 'GET') requireSameOrigin(request);
  const current = await session(request, env);
  if (!current) fail(401, 'login_required');
  const prefix = 'backups/github-' + current.user.id + '/';
  if (url.pathname === '/api/backups' && request.method === 'GET') {
    const cursor = url.searchParams.get('cursor') || undefined;
    if (cursor && cursor.length > 2048) fail(400, 'invalid_request');
    const result = await env.BACKUPS.list({prefix, cursor, limit: 100, include: ['customMetadata']});
    return json({backups: result.objects.map(backupInfo), cursor: result.truncated ? result.cursor : null});
  }
  if (url.pathname === '/api/backups') {
    const name = url.searchParams.get('name') || '';
    if (!/\.jsonl$/i.test(name) || /[\x00-\x1f\x7f/\\]/.test(name) || encoder.encode(name).length > 240) fail(400, 'invalid_filename');
    const description = backupDescription(request);
    const {bytes, records} = await boundedBody(request);
    const key = prefix + crypto.randomUUID() + '.jsonl';
    const object = await env.BACKUPS.put(key, bytes, {httpMetadata: {contentType: 'application/x-ndjson'},
      customMetadata: {name, records: String(records), ...(description ? {description} : {})}});
    if (!object) fail(503, 'cloud_unavailable');
    return json({backup: backupInfo(object)}, 201);
  }
  const id = url.pathname.slice('/api/backups/'.length);
  if (!UUID.test(id)) fail(404, 'not_found');
  // Never accept an owner or object key from the client.
  const key = prefix + id + '.jsonl';
  if (request.method === 'DELETE') {
    await env.BACKUPS.delete(key);
    return json({ok: true});
  }
  const object = await env.BACKUPS.get(key);
  if (!object) fail(404, 'not_found');
  return new Response(object.body, {headers: {'Content-Type': 'application/x-ndjson; charset=utf-8',
    'Content-Length': String(object.size),
    'Content-Disposition': "attachment; filename=\"session.jsonl\"; filename*=UTF-8''" + encodeURIComponent(object.customMetadata?.name || 'session.jsonl')}});
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith('/api/')) return env.ASSETS.fetch(request);
    let response;
    try { response = await api(request, env, url); }
    catch (error) {
      // Do not log session contents, OAuth codes, cookies, or upstream responses.
      if (!(error instanceof ApiError)) console.error(JSON.stringify({event: 'backup_api_error', path: url.pathname}));
      response = json({error: error instanceof ApiError ? error.message : 'server_error'}, error instanceof ApiError ? error.status : 500);
    }
    response.headers.set('Cache-Control', 'no-store');
    response.headers.set('X-Content-Type-Options', 'nosniff');
    response.headers.set('Referrer-Policy', 'no-referrer');
    response.headers.set('X-Frame-Options', 'DENY');
    return response;
  }
};
