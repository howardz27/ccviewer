// Regression coverage for actual backup intents across the OAuth page reload.
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const {webcrypto}=require('node:crypto');
const source=fs.readFileSync('claude-code-session-viewer/src/cloud-backup.js','utf8');
const strings=JSON.parse(fs.readFileSync('claude-code-session-viewer/src/i18n/en.json','utf8')).ui;
const tick=()=>new Promise(resolve=>setImmediate(resolve));
function sharedStorage(){
  const records=new Map(),session=new Map();
  const shared={records,session,fail:false};
  shared.sessionStorage={getItem:key=>session.get(key)||null,setItem:(key,value)=>session.set(key,value),removeItem:key=>session.delete(key)};
  shared.indexedDB={open(){
    const request={};setImmediate(()=>{
      if(shared.fail){request.error=new Error('quota');request.onerror();return;}
      request.result={close(){},transaction(){
        const tx={objectStore(){return {
          // structuredClone strips File names on Node 22; snapshots are plain data plus File instances.
          put(value){records.set(value.id,{...value,files:[...(value.files||[])]});return {result:value.id};},
          get(id){const record=records.get(id);return {result:record?{...record,files:[...(record.files||[])]}:record};},delete(id){records.delete(id);return {};}
        };}};setImmediate(()=>tx.oncomplete());return tx;
      }};request.onsuccess();
    });return request;
  }};return shared;
}
function page({protocol='https:',shared=sharedStorage(),result='',user={id:'101',login:'alice'},ready=Promise.resolve()}={}){
  const elements=new Map(),calls=[],saved=[],opened=[],views=[],listeners={},historyUrls=[];
  const history={state:null,replaceState(state){history.state=state;},pushState(state,title,url){history.state=state;historyUrls.push(url);},
    back(){history.state=null;if(listeners.popstate)listeners.popstate({state:null});}};
  function element(tag='div'){
    const classes=new Set();let html='';
    return {tag,dataset:{},children:[],style:{},textContent:'',value:'',hidden:false,disabled:false,open:false,scrollTop:0,
      classList:{toggle(name,value){if(value)classes.add(name);else classes.delete(name);},contains:name=>classes.has(name)},
      set innerHTML(value){html=value;this.children=[];},get innerHTML(){return html;},
      setAttribute(){},addEventListener(name,handler){this['on'+name]=handler;},append(...nodes){this.children.push(...nodes);},appendChild(node){this.children.push(node);},
      click(){this.clicked=true;},blur(){this.onblur?.();},showModal(){this.open=true;},close(){this.open=false;},
      getBoundingClientRect(){return {left:100,right:500,top:100,bottom:500};},
      querySelectorAll(){return [...elements.values()].filter(e=>e.tag==='button');}};
  }
  const $=id=>{if(!elements.has(id)){const e=element(id.includes('cloudList')?'div':'button');e.id=id.slice(1);elements.set(id,e);}return elements.get(id);};
  $('#library').classList.toggle('hide',true);
  let answer=async(path,options)=>{
    if(path==='/api/auth/session')return Response.json({enabled:true,user,maxFileBytes:20*1024*1024});
    if(options.method==='POST')return Response.json({backup:{id:'new'}});
    if(path.startsWith('/api/backups'))return Response.json({backups:[],cursor:null});
    return Response.json({ok:true});
  };
  const context={$,el:element,t:key=>strings[key]||key,LANG:'en',CUR:null,CUR_ID:null,LIB_SELECTED:new Set(),LIB_FULL:new Map(),libraryReady:ready,
    URL,URLSearchParams,File,Blob,TextEncoder,crypto:webcrypto,indexedDB:shared.indexedDB,sessionStorage:shared.sessionStorage,
    location:{protocol,search:result?'?cloud='+result:'',pathname:'/claude-code-session-viewer/',href:'https://ccviewer.test/claude-code-session-viewer/'+(result?'?cloud='+result:'')},
    document:{createElement:element},history,addEventListener:(name,handler)=>{listeners[name]=handler;},setTimeout(){},confirm:()=>true,
    fetch:async(path,options)=>{calls.push({path,options});return answer(path,options);},
    parse:text=>({entries:text.trim()?text.trim().split('\n').map(JSON.parse):[]}),
    saveToLibrary:async(...args)=>{saved.push(args);return args[3]||'restored-id';},
    load:(...args)=>{opened.push(args);context.CUR={text:args[0],name:args[1],pasted:args[2]};},
    showView:view=>views.push(view),showLibrary:()=>views.push('library'),renderNav(){}};
  const template=fs.readFileSync('claude-code-session-viewer/src/template.html','utf8');
  const sessionName=template.slice(template.indexOf('function sessionDisplayName('),template.indexOf('function renderNav('));
  vm.createContext(context);vm.runInContext(sessionName+source,context);
  const p={$,context,calls,saved,opened,views,shared,listeners,historyUrls,run:code=>vm.runInContext(code,context),respond:fn=>{answer=fn;}};
  p.settle=async()=>{for(let i=0;i<100;i++){await tick();if(!p.run('CLOUD.busy')&&(!result||calls.length))return;}throw Error('task did not finish');};
  return p;
}
const text='{"type":"user","message":{"content":"private session"}}\n';
const posts=p=>p.calls.filter(call=>call.options.method==='POST'&&call.path.startsWith('/api/backups'));
const description='优化说明 💡\n<img src=x onerror=alert(1)>';
const backup={id:'new',name:'<img src=x onerror=alert(1)>.jsonl',size:123,uploaded:new Date().toISOString(),description};
(async()=>{
  const p=page();
  assert.equal(p.calls.filter(call=>call.path!=='/api/auth/session').length,0,'local viewing must not contact cloud APIs');
  assert.ok(p.calls.length<=1,'the boot check may only read the session endpoint');
  p.context.CUR={text,name:'example.jsonl',sum:{title:'项目/排查'}};
  await p.$('#btnCloud').onclick();
  assert.equal(posts(p).length,0,'nothing uploads before the user confirms');
  assert.equal(p.$('#cloudNameRow').hidden,false,'single-session backup asks for the name');
  assert.equal(p.$('#cloudName').value,'项目-排查');
  const preview=()=>p.$('#cloudPlan').children[0].children[0].textContent;
  assert.equal(preview(),'项目-排查.jsonl');
  p.$('#cloudName').value='  preview name.jsonl ';
  p.$('#cloudName').oninput();
  assert.equal(preview(),'preview name.jsonl');
  p.$('#cloudName').onkeydown({key:'Enter',isComposing:true,preventDefault(){assert.fail('Enter must still confirm IME composition');}});
  let enterHandled=false;
  p.$('#cloudName').onkeydown({key:'Enter',preventDefault(){enterHandled=true;}});
  assert.equal(enterHandled,true);
  assert.equal(p.$('#cloudName').value,'preview name');
  p.$('#cloudName').value='  renamed session.jsonl ';
  p.$('#cloudName').onblur();
  const dialog=p.$('#cloudBackup');
  dialog.onclick({target:dialog,clientX:120,clientY:120});
  assert.equal(dialog.open,true,'clicking dialog padding keeps the draft open');
  assert.equal(preview(),'renamed session.jsonl');
  assert.equal(posts(p).length,0,'Enter and blur only apply the name');
  p.$('#cloudDescription').value=description;
  await p.$('#cloudSubmit').onclick();
  assert.equal(posts(p).length,1,'the confirm click uploads the current session');
  assert.equal(posts(p)[0].path,'/api/backups?name=renamed%20session.jsonl');assert.equal(await posts(p)[0].options.body.text(),text);
  assert.equal(posts(p)[0].options.headers['X-CCViewer-Request'],'1');
  assert.equal(decodeURIComponent(posts(p)[0].options.headers['X-CCViewer-Description']),description);
  assert.equal(posts(p)[0].options.credentials,'same-origin');assert.equal(posts(p)[0].options.cache,'no-store');
  // Logging in must keep exact raw text, current identity, pasted name, and scroll.
  const shared=sharedStorage(),anonymous=page({shared,user:null});
  anonymous.context.CUR={text,name:'example.jsonl',pasted:true};anonymous.context.CUR_ID='reading-id';anonymous.$('#content').scrollTop=712;
  await anonymous.$('#btnCloud').onclick();assert.equal(posts(anonymous).length,0);
  assert.equal(anonymous.$('#cloudName').value,'example','the original filename is used without a session title');
  anonymous.$('#cloudName').value='name after login';
  anonymous.$('#cloudDescription').value=description;
  assert.equal(anonymous.$('#cloudLogin').textContent,strings.cloudLoginBackup);
  await anonymous.$('#cloudLogin').onclick();
  assert.ok(anonymous.context.location.href.startsWith('/api/auth/github?returnTo='));
  assert.equal(shared.records.size,1);assert.ok([...shared.session.values()][0].length<50,'sessionStorage contains only an opaque intent ID');
  const callback=page({shared,result:'ready'});await callback.settle();
  assert.deepEqual(callback.opened[0],[text,'example.jsonl',true,null]);assert.equal(callback.context.CUR_ID,'reading-id');
  assert.equal(callback.$('#content').scrollTop,712);assert.equal(callback.views[0],'viewer');
  assert.equal(callback.$('#cloudName').value,'name after login');
  assert.equal(callback.$('#cloudDescription').value,description);
  assert.equal(posts(callback).length,0,'the return waits for a confirm click');
  await callback.$('#cloudSubmit').onclick();
  assert.equal(await posts(callback)[0].options.body.text(),text);assert.equal(posts(callback).length,1);
  assert.equal(posts(callback)[0].path,'/api/backups?name=name%20after%20login.jsonl');
  assert.equal(decodeURIComponent(posts(callback)[0].options.headers['X-CCViewer-Description']),description);
  assert.equal(shared.records.size,0);assert.equal(shared.session.size,0);
  const reload=page({shared,result:'ready'});await reload.settle();assert.equal(posts(reload).length,0,'callback reload cannot replay an upload');
  // Snapshot failures must stop navigation instead of losing the active transcript.
  const full=page({user:null});full.context.CUR={text,name:'full.jsonl'};await full.$('#btnCloud').onclick();full.shared.fail=true;
  const previousUrl=full.context.location.href;await full.$('#cloudLogin').onclick();
  assert.equal(full.context.location.href,previousUrl);assert.equal(full.$('#cloudStatus').textContent,strings.cloudPreserveFailed);
  // Cancelled OAuth restores reading but does not upload. The intent remains retryable in the panel.
  const cancelledStorage=sharedStorage(),beforeCancel=page({shared:cancelledStorage,user:null});
  beforeCancel.context.CUR={text,name:'cancel.jsonl'};await beforeCancel.$('#btnCloud').onclick();await beforeCancel.$('#cloudLogin').onclick();
  const cancelled=page({shared:cancelledStorage,result:'login_failed',user:null});await cancelled.settle();
  assert.equal(cancelled.opened[0][0],text);assert.equal(posts(cancelled).length,0);assert.equal(cancelled.run('CLOUD.queue.length'),1);
  assert.equal(cancelled.$('#cloudStatus').textContent,strings.cloudLoginFailed);
  // Library batch selection snapshots the selected transcripts, including a visible current session.
  const batch=page({user:null});batch.context.CUR={text,name:'reading.jsonl'};
  const longTitle='中'.repeat(77)+'💡结束';
  batch.context.LIB_SELECTED=new Set(['one','two']);batch.context.LIB_FULL=new Map([
    ['one',{text,name:'one.jsonl',sum:{title:longTitle}}],['two',{text:text+'\n',name:'two.jsonl',sum:{title:'第二个会话'}}]
  ]);
  batch.$('#library').classList.toggle('hide',false);
  await batch.$('#btnCloudLibrary').onclick();batch.$('#cloudDescription').value=description;await batch.$('#cloudLogin').onclick();
  const batchReturn=page({shared:batch.shared,result:'ready'});batchReturn.context.LIB_FULL=batch.context.LIB_FULL;await batchReturn.settle();
  assert.equal(batchReturn.$('#cloudNameRow').hidden,true,'batch uploads do not show a single-name editor');
  await batchReturn.$('#cloudSubmit').onclick();
  assert.equal(posts(batchReturn).length,2);assert.equal(batchReturn.views.at(-1),'library');
  assert.equal(batchReturn.context.LIB_SELECTED.size,2);assert.equal(await posts(batchReturn)[1].options.body.text(),text+'\n');
  assert.deepEqual(posts(batchReturn).map(call=>new URL(call.path,'https://ccviewer.test').searchParams.get('name')),['中'.repeat(77)+'.jsonl','第二个会话.jsonl']);
  assert.ok(posts(batchReturn).every(call=>decodeURIComponent(call.options.headers['X-CCViewer-Description'])===description));
  // Mixed results continue past a failed item. Retry must never reupload successes.
  const mixed=page();let failedOnce=false;
  mixed.respond(async(path,options)=>{
    if(path==='/api/auth/session')return Response.json({enabled:true,user:{login:'alice'},maxFileBytes:20*1024*1024});
    if(options.method==='POST'){
      if(path.includes('two')&&!failedOnce){failedOnce=true;return Response.json({error:'invalid_jsonl'},{status:400});}
      return Response.json({backup:{id:'new'}});
    }
    return Response.json({backups:[backup],cursor:'next'});
  });
  await mixed.run('openCloud([cloudFile('+JSON.stringify(text)+',"one"),cloudFile('+JSON.stringify(text)+',"two"),cloudFile('+JSON.stringify(text)+',"three")])');
  assert.equal(posts(mixed).length,0,'a batch also waits for the confirm click');
  await mixed.$('#cloudSubmit').onclick();
  assert.equal(posts(mixed).length,3);assert.equal(mixed.run('CLOUD.queue.filter(item=>item.state==="done").length'),2);
  assert.equal(mixed.$('#cloudSubmit').textContent,strings.cloudRetry);
  await mixed.$('#cloudSubmit').onclick();assert.equal(posts(mixed).length,4);assert.ok(posts(mixed)[3].path.includes('two'));
  assert.equal(mixed.run('CLOUD.queue.every(item=>item.state==="done")'),true);
  assert.equal(mixed.$('#cloudList').children[0].children[0].children[0].textContent,backup.name,'filenames render as text');
  assert.equal(mixed.$('#cloudList').children[0].children[0].children[2].textContent,description,'descriptions render as text');
  assert.equal(mixed.$('#cloudMore').hidden,false);
  // A listing failure after upload does not mark successful uploads as failed.
  mixed.respond(async(path,options)=>options.method==='POST'?Response.json({ok:true}):Response.json({error:'bad'},{status:500}));
  await mixed.run('cloudTask(cloudRunQueue)');assert.equal(posts(mixed).length,4);
  // Session expiry during a batch stops later items; signing in resumes only unfinished items.
  const expiry=page();let uploadCount=0;
  expiry.respond(async(path,options)=>{
    if(path==='/api/auth/session')return Response.json({enabled:true,user:{login:'alice'},maxFileBytes:20*1024*1024});
    if(options.method==='POST'&&++uploadCount===2)return Response.json({error:'login_required'},{status:401});
    return Response.json(options.method==='POST'?{ok:true}:{backups:[]});
  });
  await expiry.run('openCloud([cloudFile('+JSON.stringify(text)+',"one"),cloudFile('+JSON.stringify(text)+',"two"),cloudFile('+JSON.stringify(text)+',"three")])');
  await expiry.$('#cloudSubmit').onclick();
  assert.equal(posts(expiry).length,2);assert.equal(expiry.run('CLOUD.user'),null);
  await expiry.$('#cloudLogin').onclick();const afterExpiry=page({shared:expiry.shared,result:'ready'});await afterExpiry.settle();
  assert.equal(posts(afterExpiry).length,0);
  await afterExpiry.$('#cloudSubmit').onclick();
  assert.equal(posts(afterExpiry).length,2);assert.ok(posts(afterExpiry).every(call=>!call.path.includes('one')));
  // File validation is per item; bad files do not block valid siblings.
  const validation=page();await validation.run('openCloud([new File(["bad"],"a.txt"),new File([],"empty.jsonl"),cloudFile('+JSON.stringify(text)+',"valid")])');
  await validation.$('#cloudSubmit').onclick();
  assert.equal(posts(validation).length,1);assert.equal(validation.run('CLOUD.queue.filter(item=>item.state==="error").length'),2);
  // Batch file picker accepts multiple files without needing to reopen a reading session.
  const picker=page();await picker.$('#cloudFile').onchange({target:{files:[new File([text],'one.jsonl'),new File([text],'two.jsonl')],value:'files'}});await picker.settle();await picker.$('#cloudSubmit').onclick();assert.equal(posts(picker).length,2);
  // Duplicate actions cannot replace an in-flight queue or send duplicate requests.
  const busy=page();await busy.run('openCloud()');
  const pending=busy.run('cloudTask(()=>new Promise(resolve=>globalThis.releaseTask=resolve))');
  assert.equal(busy.$('#cloudPick').disabled,true);await busy.$('#btnCloud').onclick();
  await busy.run('cloudTask(()=>{throw Error("duplicate task ran")})');busy.run('releaseTask()');await pending;
  assert.equal(busy.$('#cloudPick').disabled,false);
  // Restore remains a local disconnected snapshot.
  mixed.respond(async()=>new Response(text));
  const target=action=>({closest:selector=>selector==='button[data-action]'?{dataset:{action}}:{dataset:{id:'new'}}});
  await mixed.$('#cloudList').onclick({target:target('restore')});
  assert.deepEqual(mixed.opened[0],[text,backup.name,false,null]);assert.equal(mixed.$('#cloudBackup').open,false);
  for(const protocol of ['file:']){const offline=page({protocol});await offline.run('openCloud()');assert.equal(offline.calls.length,0);assert.equal(offline.$('#cloudStatus').textContent,strings.cloudOnlineOnly);}
  const disabled=page();disabled.respond(async()=>Response.json({enabled:false,user:null}));await disabled.run('openCloud()');assert.equal(disabled.$('#cloudLogin').hidden,true);
  const staticHost=page();staticHost.respond(async()=>new Response('Not found',{status:404}));await staticHost.run('openCloud()');assert.equal(staticHost.$('#cloudStatus').textContent,strings.cloudUnavailable);
  const logout=page();await logout.run('openCloud()');await logout.$('#cloudLogout').onclick();assert.equal(logout.run('CLOUD.user'),null);assert.equal(logout.$('#cloudStatus').textContent,strings.cloudLoggedOut);
  // A busy cloud must answer further clicks with visible feedback, not silence.
  const busyPage=page();await busyPage.run('openCloud()');
  const held=busyPage.run('cloudTask(()=>new Promise(resolve=>globalThis.releaseTask2=resolve))');
  await busyPage.run('openCloudPage()');
  assert.equal(busyPage.$('#cloudStatus').textContent,strings.cloudWorking);
  busyPage.run('releaseTask2()');await held;
  // The cloud page behaves like a route: pushed to history, closed by Back, reopened by Forward.
  const route=page();
  await route.run('openCloudPage()');
  assert.equal(route.$('#cloudPage').classList.contains('hide'),false,'cloud page shows');
  assert.ok(route.historyUrls.at(-1).endsWith('#cloud'),'a #cloud history entry is pushed');
  assert.equal(route.run('history.state.ccvCloud'),true);
  route.listeners.popstate({state:null});
  assert.equal(route.$('#cloudPage').classList.contains('hide'),true,'Back closes the cloud page');
  route.listeners.popstate({state:{ccvCloud:true}});
  assert.equal(route.$('#cloudPage').classList.contains('hide'),false,'Forward reopens it');
  route.run('history.state={ccvCloud:true}');route.$('#btnCloudClose').onclick();
  assert.equal(route.$('#cloudPage').classList.contains('hide'),true,'the close button pops the history entry');
  assert.equal(route.run('history.state'),null);
  // Invalid session names never upload.
  const invalid=page();invalid.context.CUR={text,name:'example.jsonl'};
  await invalid.$('#btnCloud').onclick();
  invalid.$('#cloudName').value='a/b';await invalid.$('#cloudSubmit').onclick();
  assert.equal(posts(invalid).length,0);assert.equal(invalid.$('#cloudStatus').textContent,strings.cloudInvalidName);
  invalid.$('#cloudName').value='   ';await invalid.$('#cloudSubmit').onclick();
  assert.equal(posts(invalid).length,0,'empty names are rejected too');
  for(const file of fs.readdirSync('claude-code-session-viewer/src/i18n')){
    const ui=JSON.parse(fs.readFileSync('claude-code-session-viewer/src/i18n/'+file,'utf8')).ui;
    for(const key of Object.keys(strings).filter(key=>key.startsWith('cloud')))assert.ok(ui[key],file+': '+key);
  }
  console.log('Cloud UI: name-confirm backup, OAuth intent/scroll restore, cancellation, quota failure, batch selection/files, partial retry, expiry, replay prevention, XSS, duplicate actions, busy feedback, history routing, restore, offline and 10 locales passed.');
})().catch(error=>{console.error(error);process.exitCode=1;});
