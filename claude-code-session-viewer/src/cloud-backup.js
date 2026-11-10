/* Nothing is uploaded until a reader explicitly requests a backup. */
const CLOUD={enabled:false,user:null,busy:false,backups:[],cursor:null,maxFileBytes:20*1024*1024,message:'',error:false,queue:[]};
const cloudDialog=$('#cloudBackup');
const cloudName=$('#cloudName'),cloudDescription=$('#cloudDescription');
const CLOUD_PENDING_KEY='ccviewer_backup_return:'+location.pathname;
const CLOUD_ERRORS={login_required:'cloudLoginRequired',cloud_unavailable:'cloudUnavailable',file_too_large:'cloudTooLarge',
  invalid_jsonl:'cloudInvalidJsonl',invalid_filename:'cloudInvalidName',invalid_description:'cloudInvalidDescription',
  not_found:'cloudNotFound',invalid_origin:'cloudOriginError'};
async function cloudApi(path,options={}){
  let response;const timer=cloudTimeoutSignal();
  try{response=await fetch('/api/'+path,{...options,credentials:'same-origin',cache:'no-store',
    headers:{'X-CCViewer-Request':'1',...options.headers},...(timer?{signal:timer.signal}:{})});}
  catch(e){throw new Error(t('cloudNetworkError'));}
  finally{if(timer)timer.clear();}
  if(!response.ok){
    let code='';try{code=(await response.json()).error||'';}catch(e){}
    if(response.status===401){CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;}
    const error=new Error(t(CLOUD_ERRORS[code]||(response.status===404?'cloudUnavailable':'cloudRequestFailed')));
    error.status=response.status;throw error;
  }
  return response;
}
/* A single hung request must never freeze CLOUD.busy and deaden every cloud button. */
function cloudTimeoutSignal(){
  if(typeof AbortController!=='function')return null;
  const controller=new AbortController();
  let timer=-1;
  if(typeof setTimeout==='function')timer=setTimeout(()=>controller.abort(),10000);
  return {signal:controller.signal,clear(){if(timer!==-1&&typeof clearTimeout==='function')clearTimeout(timer);}};
}
function cloudNameValue(){
  return cloudName.value.trim().replace(/(?:\s*\.jsonl)+$/i,'').trimEnd();
}
function cloudRenderPlan(){
  const plan=$('#cloudPlan');
  plan.hidden=!CLOUD.queue.length;
  plan.innerHTML='';
  const stem=cloudNameValue();
  for(const item of CLOUD.queue){
    const row=el('div','cloud-target');row.dataset.state=item.state;
    const name=el('span'),state=el('small');
    name.textContent=CLOUD.queue.length===1?(stem?stem+'.jsonl':'—'):item.file.name;
    state.textContent=t({waiting:'cloudWaiting',uploading:'cloudUploading',done:'cloudDone',error:'cloudFailed'}[item.state]);
    if(item.error){const error=el('em');error.textContent=item.error;name.appendChild(error);}
    row.append(name,state);plan.appendChild(row);
  }
}
function cloudRender(){
  const queued=CLOUD.queue.length>0,pending=CLOUD.queue.some(item=>item.state!=='done');
  $('#cloudTitle').textContent=queued?(CLOUD.queue.length===1?t('cloudTitle'):t('cloudBatchTitle').replace('{n}',CLOUD.queue.length)):t('cloudTitle');
  $('#cloudAccount').textContent=CLOUD.user?'GitHub · @'+CLOUD.user.login:'';
  $('#cloudLogin').hidden=!CLOUD.enabled||!!CLOUD.user;
  $('#cloudLogin').textContent=queued?t('cloudLoginBackup'):t('cloudLogin');
  $('#cloudLoginHint').hidden=!CLOUD.enabled||!!CLOUD.user;
  $('#cloudLoginHint').textContent=queued?t('cloudLoginContinue'):t('cloudLoginRequired');
  $('#cloudLogout').hidden=!CLOUD.user;
  $('#cloudViewSaved').hidden=!CLOUD.user||!queued||CLOUD.busy;
  cloudRenderPlan();
  $('#cloudNameRow').hidden=CLOUD.queue.length!==1;
  $('#cloudDescriptionRow').hidden=!queued;
  cloudName.disabled=cloudDescription.disabled=CLOUD.busy||!pending;
  $('#cloudSubmit').hidden=!CLOUD.user||!queued||!pending||CLOUD.busy;
  $('#cloudSubmit').textContent=CLOUD.queue.some(item=>item.state==='error')?t('cloudRetry'):t('cloudStart');
  $('#cloudStatus').textContent=CLOUD.message||(CLOUD.busy?t('cloudWorking'):'');
  $('#cloudStatus').classList.toggle('cloud-error',CLOUD.error);
  const pageStatus=$('#cloudStatusPage');
  if(pageStatus){pageStatus.textContent=$('#cloudStatus').textContent;pageStatus.classList.toggle('cloud-error',CLOUD.error);}
  $('#cloudCount').textContent=CLOUD.user&&CLOUD.backups.length?String(CLOUD.backups.length):'';
  $('#cloudEmpty').hidden=!CLOUD.user||!!CLOUD.backups.length||CLOUD.busy;
  $('#cloudMore').hidden=!CLOUD.user||!CLOUD.cursor;
  const list=$('#cloudList');list.innerHTML='';
  for(const backup of CLOUD.backups){
    const row=el('div','cloud-row');row.dataset.id=backup.id;
    const info=el('div','cloud-info'),name=el('strong'),meta=el('small');
    name.textContent=backup.name;
    meta.textContent=(backup.size/1024).toLocaleString(LANG,{maximumFractionDigits:1})+' KiB · '+new Date(backup.uploaded).toLocaleString(LANG)
      +(backup.records?' · '+t('cloudRecords').replace('{n}',backup.records):'');
    info.append(name,meta);
    if(backup.description){
      const description=el('p','cloud-description');
      description.textContent=backup.description;info.appendChild(description);
    }
    row.appendChild(info);
    const actions=el('div','cloud-row-actions');
    for(const [action,key] of [['restore','cloudRestore'],['download','cloudDownload'],['delete','deleteBtn']]){
      const button=el('button','btn');button.type='button';button.dataset.action=action;button.textContent=t(key);actions.appendChild(button);
    }
    row.appendChild(actions);list.appendChild(row);
  }
  cloudDialog.setAttribute('aria-busy',String(CLOUD.busy));
  cloudDialog.querySelectorAll('button').forEach(button=>{if(button.id!=='cloudClose')button.disabled=CLOUD.busy;});
  const cloudPageEl=$('#cloudPage');
  if(cloudPageEl&&cloudPageEl.querySelectorAll)cloudPageEl.querySelectorAll('button').forEach(button=>{if(button.id!=='btnCloudClose')button.disabled=CLOUD.busy;});
}
async function cloudTask(action){
  if(CLOUD.busy)return;
  CLOUD.busy=true;CLOUD.message='';CLOUD.error=false;cloudRender();
  try{await action();}
  catch(e){CLOUD.message=e.message||t('cloudRequestFailed');CLOUD.error=true;}
  finally{CLOUD.busy=false;cloudRender();}
}
async function cloudList(append=false){
  const data=await (await cloudApi('backups'+(append&&CLOUD.cursor?'?cursor='+encodeURIComponent(CLOUD.cursor):''))).json();
  CLOUD.backups=append?[...CLOUD.backups,...data.backups]:data.backups;CLOUD.cursor=data.cursor;
}
function cloudFile(text,name){
  return new File([text],(name||'session').replace(/\.(jsonl|json|txt)$/i,'')+'.jsonl',{type:'application/x-ndjson'});
}
function cloudSessionFile(session){
  const name=String(sessionDisplayName(session));
  if(!session.sum?.title)return cloudFile(session.text,name);
  const title=name.replace(/\s+/g,' ').replace(/[\x00-\x1f\x7f<>:"/\\|?*]/g,'-').trim();
  const encoder=new TextEncoder();
  let stem='',bytes=0;
  for(const character of title.replace(/\.(jsonl|json|txt)$/i,'')){
    bytes+=encoder.encode(character).length;
    if(bytes>234)break; // Leave six bytes for .jsonl.
    stem+=character;
  }
  return cloudFile(session.text,stem.trimEnd()||session.name||session.sum.sessionId);
}
function cloudValidateName(name){
  if(!/.+\.jsonl$/i.test(name)||new TextEncoder().encode(name).length>240||/[\x00-\x1f\x7f/\\]/.test(name))throw new Error(t('cloudInvalidName'));
}
async function cloudUpload(file,name,description){
  cloudValidateName(name);
  if(!file.size)throw new Error(t('cloudInvalidJsonl'));
  if(file.size>CLOUD.maxFileBytes)throw new Error(t('cloudTooLarge'));
  const headers={'Content-Type':'application/x-ndjson'};
  if(description)headers['X-CCViewer-Description']=encodeURIComponent(description);
  await cloudApi('backups?name='+encodeURIComponent(name),{method:'POST',headers,body:file});
}
async function cloudRunQueue(){
  const pending=CLOUD.queue.filter(item=>item.state!=='done');
  const name=CLOUD.queue.length===1?cloudNameValue()+'.jsonl':null;
  if(name)cloudValidateName(name);
  const description=cloudDescription.value.trim();
  if(description.length>500)throw new Error(t('cloudInvalidDescription'));
  for(let i=0;i<pending.length;i++){
    const item=pending[i];item.state='uploading';item.error='';
    CLOUD.message=t('cloudProgress').replace('{n}',i+1).replace('{m}',pending.length);cloudRender();
    try{await cloudUpload(item.file,name||item.file.name,description);item.state='done';}
    catch(e){item.state='error';item.error=e.message;if(e.status===401)break;}
    cloudRender();
  }
  const done=CLOUD.queue.filter(item=>item.state==='done').length,failed=CLOUD.queue.length-done;
  CLOUD.error=!!failed;
  CLOUD.message=failed?t('cloudPartial').replace('{n}',done).replace('{m}',failed):t('cloudComplete').replace('{n}',done);
  // Listing errors must never turn completed uploads into retryable uploads.
  if(CLOUD.user){try{await cloudList();}catch(e){CLOUD.message+=' '+e.message;CLOUD.error=true;}}
}
/* Nothing uploads until the user confirms the plan in the dialog. */
async function openCloud(files=[],draft={}){
  if(CLOUD.busy){if(!cloudDialog.open)cloudDialog.showModal();return;}
  CLOUD.queue=files.map(file=>({file,state:'waiting',error:''}));
  cloudName.value=files.length===1?(draft.name??files[0].name.replace(/\.jsonl$/i,'')):'';
  cloudDescription.value=draft.description||'';
  if(!cloudDialog.open)cloudDialog.showModal();
  await cloudTask(async()=>{
    CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;CLOUD.enabled=false;
    if(location.protocol==='file:'){CLOUD.message=t('cloudOnlineOnly');return;}
    const data=await (await cloudApi('auth/session')).json();
    CLOUD.enabled=data.enabled;CLOUD.user=data.user;CLOUD.maxFileBytes=data.maxFileBytes;
    if(!CLOUD.enabled){CLOUD.message=t('cloudUnavailable');return;}
    if(CLOUD.user)await cloudList();
  });
}
/* Save exact transcript/File bytes before leaving the page for OAuth. This store
   is separate from the library, whose quota fallback may keep only summaries. */
async function cloudPendingStore(mode,action){
  const db=await new Promise((resolve,reject)=>{
    const request=indexedDB.open('ccviewer-backup-return',1);
    request.onupgradeneeded=()=>request.result.createObjectStore('pending',{keyPath:'id'});
    request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error);
    request.onblocked=()=>reject(new Error('blocked'));
  });
  try{return await new Promise((resolve,reject)=>{
    const tx=db.transaction('pending',mode),request=action(tx.objectStore('pending'));
    tx.oncomplete=()=>resolve(request.result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error);
  });}finally{db.close();}
}
function cloudReadingSnapshot(){
  return CUR?{text:CUR.text,name:CUR.name,pasted:CUR.pasted,id:CUR_ID,scroll:$('#content').scrollTop}:null;
}
async function cloudLogin(intent){
  await cloudTask(async()=>{
    let id;try{id=sessionStorage.getItem(CLOUD_PENDING_KEY);}catch(e){}
    id=id||crypto.randomUUID();
    const snapshot={id,createdAt:Date.now(),intent:intent||'',reading:cloudReadingSnapshot(),library:!$('#library').classList.contains('hide'),
      selected:[...LIB_SELECTED],files:CLOUD.queue.filter(item=>item.state!=='done').map(item=>item.file),
      draft:{name:CLOUD.queue.length===1?cloudName.value:undefined,description:cloudDescription.value}};
    try{
      await cloudPendingStore('readwrite',store=>store.put(snapshot));
      sessionStorage.setItem(CLOUD_PENDING_KEY,id);
    }catch(e){CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;return;}
    location.href='/api/auth/github?returnTo='+encodeURIComponent(location.pathname);
  });
}
async function cloudResume(result){
  let id;try{id=sessionStorage.getItem(CLOUD_PENDING_KEY);}catch(e){}
  if(!id){
    if(result)await openCloud();
    if(result==='login_failed'){CLOUD.message=t('cloudLoginFailed');CLOUD.error=true;cloudRender();}
    return;
  }
  let snapshot;
  try{snapshot=await cloudPendingStore('readonly',store=>store.get(id));}
  catch(e){await openCloud();CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;cloudRender();return;}
  if(!snapshot){sessionStorage.removeItem(CLOUD_PENDING_KEY);await openCloud();CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;cloudRender();return;}
  // Wait for startup to finish so loadLibrary cannot erase restored state.
  await libraryReady;
  const reading=snapshot.reading;
  if(reading){
    const restored=await saveToLibrary(reading.text,reading.name,reading.pasted?'paste':'file',reading.id);
    load(reading.text,reading.name,reading.pasted,null);CUR_ID=restored;showView('viewer');renderNav();$('#content').scrollTop=reading.scroll||0;
  }
  LIB_SELECTED.clear();for(const selected of snapshot.selected||[])if(LIB_FULL.has(selected))LIB_SELECTED.add(selected);
  if(snapshot.library)showLibrary();
  // Consume the intent before uploading; reloading the callback must not duplicate backups.
  try{await cloudPendingStore('readwrite',store=>store.delete(id));sessionStorage.removeItem(CLOUD_PENDING_KEY);}
  catch(e){await openCloud(snapshot.files,snapshot.draft);CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;cloudRender();return;}
  if(snapshot.intent==='page'&&!snapshot.files.length){
    await openCloudPage();
    if(result==='login_failed'){CLOUD.message=t('cloudLoginFailed');CLOUD.error=true;cloudRender();}
    return;
  }
  await openCloud(snapshot.files,snapshot.draft);
  if(result==='login_failed'){CLOUD.message=t('cloudLoginFailed');CLOUD.error=true;cloudRender();}
}
/* Full-page cloud session list, reachable from anywhere once signed in.
   It behaves like a real page: a #cloud entry is pushed to history so the
   browser Back button closes it, and reload or a direct link reopens it. */
function cloudPageActive(){return !$('#cloudPage').classList.contains('hide');}
function showCloudOverlay(){
  $('#cloudPage').classList.toggle('hide',false);
  CLOUD.message=t('cloudWorking');CLOUD.error=false;cloudRender();
}
function cloudPushHistory(){
  if(history.pushState&&!(history.state&&history.state.ccvCloud))
    history.pushState({ccvCloud:true},'',location.pathname+location.search+'#cloud');
}
async function openCloudPage(){
  if(CLOUD.busy){
    // Never swallow the click silently: tell the user why nothing happens yet.
    CLOUD.message=t('cloudWorking');
    if(!cloudPageActive()&&!cloudDialog.open)cloudDialog.showModal();
    cloudRender();return;
  }
  cloudPushHistory();
  if(CLOUD.user){showCloudOverlay();await cloudTask(async()=>{await cloudList();CLOUD.message='';});return;}
  let shown=false;
  await cloudTask(async()=>{
    CLOUD.enabled=false;
    if(location.protocol==='file:'){CLOUD.message=t('cloudOnlineOnly');return;}
    const data=await (await cloudApi('auth/session')).json();
    CLOUD.enabled=data.enabled;CLOUD.user=data.user;CLOUD.maxFileBytes=data.maxFileBytes;
    renderAvatar();
    if(!CLOUD.enabled){CLOUD.message=t('cloudUnavailable');CLOUD.error=true;return;}
    if(!CLOUD.user)return;
    $('#cloudPage').classList.toggle('hide',false);shown=true;
    await cloudList();CLOUD.message='';
  });
  if(!shown&&!cloudPageActive()&&!cloudDialog.open)cloudDialog.showModal();
  cloudRender();
}
function hideCloudPage(){
  if(history.state&&history.state.ccvCloud){if(history.back)history.back();return;}
  $('#cloudPage').classList.toggle('hide',true);
}
if(typeof addEventListener==='function'){
  addEventListener('popstate',e=>{
    const entry=e.state&&e.state.ccvCloud;
    if(entry&&!cloudPageActive())showCloudOverlay();
    else if(!entry&&cloudPageActive())$('#cloudPage').classList.toggle('hide',true);
    // A same-document jump to #cloud (e.g. a bookmark) also opens the page.
    else if(!entry&&!cloudPageActive()&&location.hash==='#cloud'&&CLOUD.user)showCloudOverlay();
  });
  addEventListener('keydown',e=>{
    if(e.key!=='Escape'||cloudDialog.open||!cloudPageActive())return;
    hideCloudPage();
  });
}
/* Avatar chip (topbar + landing header) with cloud page / sign-out menu. */
const GITHUB_MARK='<svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>';
function closeAvatarMenus(){
  for(const id of ['#avatarTop','#avatarLanding']){const wrap=$(id);if(wrap)wrap.classList.toggle('open',false);}
}
function renderAvatar(){
  for(const id of ['#avatarTop','#avatarLanding']){
    const wrap=$(id);if(!wrap)continue;
    wrap.classList.toggle('open',false);
    if(!CLOUD.enabled){wrap.hidden=true;continue;}
    wrap.innerHTML='';wrap.textContent='';
    if(CLOUD.user){
      wrap.hidden=false;
      const btn=el('button','avatar-btn');btn.type='button';
      btn.setAttribute('aria-label','@'+CLOUD.user.login);btn.title='@'+CLOUD.user.login;
      if(CLOUD.user.id&&/^\d+$/.test(CLOUD.user.id)){
        const img=document.createElement('img');
        img.src='https://avatars.githubusercontent.com/u/'+CLOUD.user.id+'?s=64&v=4';img.alt='';
        img.referrerPolicy='no-referrer';img.loading='lazy';
        img.onerror=()=>{btn.textContent=(CLOUD.user.login[0]||'?').toUpperCase();};
        btn.appendChild(img);
      }else btn.textContent=(CLOUD.user.login[0]||'?').toUpperCase();
      const menu=el('div','avatar-menu');
      const who=el('span','avatar-who');who.textContent='@'+CLOUD.user.login;
      const pageBtn=el('button','btn');pageBtn.type='button';pageBtn.textContent=t('cloudPageTitle');
      const logoutBtn=el('button','btn');logoutBtn.type='button';logoutBtn.textContent=t('cloudLogout');
      menu.append(who,pageBtn,logoutBtn);
      btn.onclick=e=>{if(e&&e.stopPropagation)e.stopPropagation();const open=wrap.classList.contains('open');closeAvatarMenus();wrap.classList.toggle('open',!open);};
      pageBtn.onclick=()=>{closeAvatarMenus();openCloudPage();};
      logoutBtn.onclick=()=>{closeAvatarMenus();cloudLogoutAction();};
      wrap.append(btn,menu);
    }else{
      if(id!=='#avatarLanding'){wrap.hidden=true;continue;}
      wrap.hidden=false;
      const login=el('button','btn');login.type='button';
      login.innerHTML=GITHUB_MARK;
      const label=el('span');label.textContent=t('loginBtn');login.appendChild(label);
      login.onclick=()=>{login.disabled=true;label.textContent=t('cloudWorking');cloudLogin('page');};
      wrap.appendChild(login);
    }
  }
}
if(typeof document.addEventListener==='function'){
  document.addEventListener('click',e=>{if(!(e.target&&e.target.closest&&e.target.closest('.avatar-wrap')))closeAvatarMenus();});
}
async function cloudLogoutAction(){
  return cloudTask(async()=>{
    await cloudApi('auth/logout',{method:'POST'});CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;CLOUD.message=t('cloudLoggedOut');
    renderAvatar();
  });
}
$('#btnCloudLanding').onclick=openCloudPage;
$('#btnCloud').onclick=()=>openCloud(CUR?[cloudSessionFile(CUR)]:[]);
$('#btnCloudManageLibrary').onclick=openCloudPage;
$('#cloudViewSaved').onclick=()=>{cloudDialog.close();openCloudPage();};
$('#btnCloudClose').onclick=hideCloudPage;
$('#btnCloudLibrary').onclick=()=>openCloud([...LIB_SELECTED].map(id=>LIB_FULL.get(id)).filter(rec=>rec?.text).map(cloudSessionFile));
$('#cloudClose').onclick=()=>cloudDialog.close();
cloudDialog.addEventListener('click',e=>{
  if(e.target!==cloudDialog)return;
  const {left,right,top,bottom}=cloudDialog.getBoundingClientRect();
  if(e.clientX<left||e.clientX>right||e.clientY<top||e.clientY>bottom)cloudDialog.close();
});
cloudName.oninput=cloudRenderPlan;
cloudName.onblur=()=>{cloudName.value=cloudNameValue();cloudRenderPlan();};
cloudName.onkeydown=e=>{
  if(e.key!=='Enter'||e.isComposing||e.keyCode===229)return;
  e.preventDefault();cloudName.blur();
};
$('#cloudLogin').onclick=()=>cloudLogin();
$('#cloudSubmit').onclick=()=>cloudTask(cloudRunQueue);
$('#cloudLogout').onclick=cloudLogoutAction;
$('#cloudRefresh').onclick=()=>cloudTask(()=>cloudList());
$('#cloudMore').onclick=()=>cloudTask(()=>cloudList(true));
$('#cloudPick').onclick=()=>$('#cloudFile').click();
$('#cloudFile').onchange=e=>{const files=[...e.target.files];e.target.value='';if(files.length)openCloud(files);};
$('#cloudList').onclick=e=>{
  const button=e.target.closest('button[data-action]'),row=e.target.closest('.cloud-row');
  if(!button||!row||CLOUD.busy)return;
  const backup=CLOUD.backups.find(item=>item.id===row.dataset.id);if(!backup)return;
  const action=button.dataset.action;
  if(action==='delete'&&!confirm(t('cloudConfirmDelete').replace('{name}',backup.name)))return;
  return cloudTask(async()=>{
    const path='backups/'+encodeURIComponent(backup.id);
    if(action==='delete'){
      await cloudApi(path,{method:'DELETE'});await cloudList();CLOUD.message=t('cloudDeleted');return;
    }
    const response=await cloudApi(path);
    if(action==='download'){
      const url=URL.createObjectURL(await response.blob()),link=document.createElement('a');
      link.href=url;link.download=backup.name;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);return;
    }
    if(action==='restore'){
      const text=await response.text();
      if(!parse(text).entries.length)throw new Error(t('cloudInvalidJsonl'));
      const id=await saveToLibrary(text,backup.name,'cloud');
      load(text,backup.name,false,null);CUR_ID=id;showView('viewer');renderNav();cloudDialog.close();hideCloudPage();
    }
  });
};
const cloudResult=new URLSearchParams(location.search).get('cloud');
if(cloudResult==='ready'||cloudResult==='login_failed'){
  const cleanUrl=new URL(location.href);cleanUrl.searchParams.delete('cloud');history.replaceState(null,'',cleanUrl.href);
  cloudResume(cloudResult).catch(()=>{if(!cloudDialog.open)cloudDialog.showModal();CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;cloudRender();});
}else{
  // Returning with the browser Back button restores the session without uploading.
  let pending=false;try{pending=!!sessionStorage.getItem(CLOUD_PENDING_KEY);}catch(e){}
  if(pending)cloudResume(null).catch(()=>{if(!cloudDialog.open)cloudDialog.showModal();CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;cloudRender();});
}
/* Know the signed-in state up front so the avatar can render without a click.
   This only reads the session; nothing about local files is ever sent. */
if(location.protocol!=='file:'){
  const cloudBoot=()=>cloudApi('auth/session').then(response=>response.json())
    .then(data=>{
      CLOUD.enabled=data.enabled;CLOUD.user=data.user;CLOUD.maxFileBytes=data.maxFileBytes;renderAvatar();
      // A reload or direct link to the cloud page reopens it without a new entry.
      if(location.hash==='#cloud'){
        if(CLOUD.user){if(history.replaceState)history.replaceState({ccvCloud:true},'',location.href);openCloudPage();}
        else if(history.replaceState)history.replaceState(null,'',location.pathname+location.search);
      }
    })
    .catch(()=>{});
  if(typeof setTimeout==='function')setTimeout(cloudBoot,0);else cloudBoot();
}
