// Frontend state and network regression checks, without browser dependencies.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync('claude-code-session-viewer/src/cloud-backup.js','utf8');
const strings=JSON.parse(fs.readFileSync('claude-code-session-viewer/src/i18n/en.json','utf8')).ui;
function page(protocol='https:'){
  const elements=new Map(),calls=[],saved=[],opened=[];
  function element(tag='div'){
    return {tag,dataset:{},children:[],style:{},textContent:'',hidden:false,disabled:false,open:false,
      classList:{toggle(){}},setAttribute(){},addEventListener(){},append(...nodes){this.children.push(...nodes);},
      appendChild(node){this.children.push(node);},click(){this.clicked=true;},
      showModal(){this.open=true;},close(){this.open=false;},querySelectorAll(){return [...elements.values()].filter(e=>e.tag==='button');}};
  }
  const $=id=>{if(!elements.has(id))elements.set(id,element(id.includes('cloudList')?'div':'button'));return elements.get(id);};
  let answer=async path=>{
    if(path==='/api/auth/session')return Response.json({enabled:true,user:{id:'101',login:'alice'},maxFileBytes:20*1024*1024});
    if(path.startsWith('/api/backups'))return Response.json({backups:[],cursor:null});
    return Response.json({ok:true});
  };
  const context={$,el:element,t:key=>strings[key]||key,LANG:'en',CUR:null,CUR_ID:null,URL,URLSearchParams,File,Blob,
    location:{protocol,search:'',pathname:'/claude-code-session-viewer/',href:'https://ccviewer.test/claude-code-session-viewer/'},
    document:{createElement:element},history:{replaceState(){}},setTimeout(){},confirm:()=>true,
    fetch:async(path,options)=>{calls.push({path,options});return answer(path,options);},
    parse:text=>({entries:text.trim()?text.trim().split('\n').map(JSON.parse):[]}),
    saveToLibrary:async(...args)=>{saved.push(args);return 'restored-id';},
    load:(...args)=>{opened.push(args);},showView(){},renderNav(){}};
  vm.createContext(context);vm.runInContext(source,context);
  return {$,context,calls,saved,opened,run:code=>vm.runInContext(code,context),respond:fn=>{answer=fn;}};
}
(async()=>{
  const p=page();assert.equal(p.calls.length,0,'local viewing must not contact cloud APIs');
  await p.run('openCloud()');assert.equal(p.$('#cloudBackup').open,true);assert.equal(p.$('#cloudLogin').hidden,true);
  assert.equal(p.$('#cloudLogout').hidden,false);assert.equal(p.$('#cloudAccount').textContent,'GitHub · @alice');
  assert.equal(p.$('#cloudEmpty').hidden,false);assert.equal(p.calls.length,2);
  assert.equal(p.calls[0].options.credentials,'same-origin');assert.equal(p.calls[0].options.cache,'no-store');
  let upload;
  p.respond(async(path,options)=>{
    if(options.method==='POST'){upload={path,options};return Response.json({backup:{id:'new'}});}
    return Response.json({backups:[{id:'new',name:'<img src=x onerror=alert(1)>.jsonl',size:123,uploaded:new Date().toISOString()}],cursor:'next'});
  });
  const text='{"type":"user","message":{"content":"private"}}\n';
  p.context.CUR={text,name:'example.jsonl'};
  await p.$('#cloudUploadCurrent').onclick();
  // onclick starts a promise via cloudTask; settle the task through its network microtasks.
  while(p.run('CLOUD.busy'))await new Promise(resolve=>setImmediate(resolve));
  assert.equal(upload.path,'/api/backups?name=example.jsonl');assert.equal(await upload.options.body.text(),text);
  assert.equal(upload.options.headers['X-CCViewer-Request'],'1');assert.equal(p.$('#cloudStatus').textContent,strings.cloudUploaded);
  const name=p.$('#cloudList').children.at(-1).children[0].children[0];
  assert.equal(name.textContent,'<img src=x onerror=alert(1)>.jsonl','filenames render as text');
  assert.equal(p.$('#cloudMore').hidden,false);
  // File errors should not send an upload request.
  const before=p.calls.length;
  await p.run('cloudTask(()=>cloudUpload(new File(["bad"],"a.txt")))');
  assert.equal(p.calls.length,before);assert.equal(p.$('#cloudStatus').textContent,strings.cloudInvalidName);
  await p.run('cloudTask(()=>cloudUpload(new File([],"empty.jsonl")))');
  assert.equal(p.calls.length,before);assert.equal(p.$('#cloudStatus').textContent,strings.cloudInvalidJsonl);
  // Duplicate submissions remain disabled while an operation is in flight.
  let release;
  const pending=p.run('cloudTask(()=>new Promise(resolve=>globalThis.releaseTask=resolve))');
  assert.equal(p.$('#cloudPick').disabled,true);
  await p.run('cloudTask(()=>{throw Error("duplicate task ran")})');
  p.run('releaseTask()');await pending;assert.equal(p.$('#cloudPick').disabled,false);
  // Restore keeps raw text and creates a disconnected local snapshot.
  p.respond(async()=>new Response(text));
  const target=action=>({closest:selector=>selector==='button[data-action]'?{dataset:{action}}:{dataset:{id:'new'}}});
  p.$('#cloudList').onclick({target:target('restore')});
  while(p.run('CLOUD.busy'))await new Promise(resolve=>setImmediate(resolve));
  assert.deepEqual(p.saved[0],[text,'<img src=x onerror=alert(1)>.jsonl','cloud']);
  assert.deepEqual(p.opened[0],[text,'<img src=x onerror=alert(1)>.jsonl',false,null]);
  assert.equal(p.context.CUR_ID,'restored-id');assert.equal(p.$('#cloudBackup').open,false);
  // Expired sessions clear cached account data and expose sign-in again.
  p.respond(async()=>Response.json({error:'login_required'},{status:401}));
  await p.$('#cloudRefresh').onclick();
  assert.equal(p.run('CLOUD.user'),null);assert.equal(p.run('CLOUD.backups.length'),0);
  assert.equal(p.$('#cloudLogin').hidden,false);assert.equal(p.$('#cloudStatus').textContent,strings.cloudLoginRequired);
  const offline=page('file:');await offline.run('openCloud()');
  assert.equal(offline.calls.length,0);assert.equal(offline.$('#cloudStatus').textContent,strings.cloudOnlineOnly);
  const disabled=page();disabled.respond(async()=>Response.json({enabled:false,user:null,maxFileBytes:20*1024*1024}));
  await disabled.run('openCloud()');assert.equal(disabled.calls.length,1);assert.equal(disabled.$('#cloudLogin').hidden,true);
  assert.equal(disabled.$('#cloudStatus').textContent,strings.cloudUnavailable);
  const staticHost=page();staticHost.respond(async()=>new Response('<h1>Not found</h1>',{status:404}));
  await staticHost.run('openCloud()');assert.equal(staticHost.$('#cloudStatus').textContent,strings.cloudUnavailable);
  const logout=page();await logout.run('openCloud()');await logout.$('#cloudLogout').onclick();
  assert.equal(logout.run('CLOUD.user'),null);assert.equal(logout.$('#cloudStatus').textContent,strings.cloudLoggedOut);
  for(const file of fs.readdirSync('claude-code-session-viewer/src/i18n')){
    const ui=JSON.parse(fs.readFileSync('claude-code-session-viewer/src/i18n/'+file,'utf8')).ui;
    for(const key of Object.keys(strings).filter(key=>key.startsWith('cloud')))assert.ok(ui[key],file+': '+key);
  }
  console.log('Cloud UI: opt-in network, offline/unconfigured hosts, authenticated upload, filename escaping, duplicate submissions, restore, expiry, logout and 10 locales passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
