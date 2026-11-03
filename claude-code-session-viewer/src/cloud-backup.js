/* Nothing is uploaded until a reader explicitly requests a backup. */
const CLOUD={enabled:false,user:null,busy:false,backups:[],cursor:null,maxFileBytes:20*1024*1024,message:'',error:false,queue:[]};
const cloudDialog=$('#cloudBackup');
const CLOUD_PENDING_KEY='ccviewer_backup_return:'+location.pathname;
const CLOUD_ERRORS={login_required:'cloudLoginRequired',cloud_unavailable:'cloudUnavailable',file_too_large:'cloudTooLarge',
  invalid_jsonl:'cloudInvalidJsonl',invalid_filename:'cloudInvalidName',not_found:'cloudNotFound',invalid_origin:'cloudOriginError'};
async function cloudApi(path,options={}){
  let response;
  try{response=await fetch('/api/'+path,{...options,credentials:'same-origin',cache:'no-store',
    headers:{'X-CCViewer-Request':'1',...options.headers}});}
  catch(e){throw new Error(t('cloudNetworkError'));}
  if(!response.ok){
    let code='';try{code=(await response.json()).error||'';}catch(e){}
    if(response.status===401){CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;}
    const error=new Error(t(CLOUD_ERRORS[code]||(response.status===404?'cloudUnavailable':'cloudRequestFailed')));
    error.status=response.status;throw error;
  }
  return response;
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
  $('#cloudSaved').hidden=!CLOUD.user||queued;
  $('#cloudViewSaved').hidden=!CLOUD.user||!queued||CLOUD.busy;
  $('#cloudPlan').hidden=!queued;
  $('#cloudPlan').innerHTML='';
  for(const item of CLOUD.queue){
    const row=el('div','cloud-target');row.dataset.state=item.state;
    const name=el('span'),state=el('small');name.textContent=item.file.name;
    state.textContent=t({waiting:'cloudWaiting',uploading:'cloudUploading',done:'cloudDone',error:'cloudFailed'}[item.state]);
    if(item.error){const error=el('em');error.textContent=item.error;name.appendChild(error);}
    row.append(name,state);$('#cloudPlan').appendChild(row);
  }
  $('#cloudSubmit').hidden=!CLOUD.user||!queued||!pending||CLOUD.busy;
  $('#cloudSubmit').textContent=CLOUD.queue.some(item=>item.state==='error')?t('cloudRetry'):t('cloudStart');
  $('#cloudStatus').textContent=CLOUD.message||(CLOUD.busy?t('cloudWorking'):'');
  $('#cloudStatus').classList.toggle('cloud-error',CLOUD.error);
  $('#cloudEmpty').hidden=!CLOUD.user||!!CLOUD.backups.length||CLOUD.busy;
  $('#cloudMore').hidden=!CLOUD.user||!CLOUD.cursor;
  const list=$('#cloudList');list.innerHTML='';
  for(const backup of CLOUD.backups){
    const row=el('div','cloud-row');row.dataset.id=backup.id;
    const info=el('div','cloud-info'),name=el('strong'),meta=el('small');
    name.textContent=backup.name;
    meta.textContent=(backup.size/1024).toLocaleString(LANG,{maximumFractionDigits:1})+' KiB · '+new Date(backup.uploaded).toLocaleString(LANG);
    info.append(name,meta);row.appendChild(info);
    const actions=el('div','cloud-row-actions');
    for(const [action,key] of [['restore','cloudRestore'],['download','cloudDownload'],['delete','deleteBtn']]){
      const button=el('button','btn');button.type='button';button.dataset.action=action;button.textContent=t(key);actions.appendChild(button);
    }
    row.appendChild(actions);list.appendChild(row);
  }
  cloudDialog.setAttribute('aria-busy',String(CLOUD.busy));
  cloudDialog.querySelectorAll('button').forEach(button=>{if(button.id!=='cloudClose')button.disabled=CLOUD.busy;});
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
function cloudValidate(file){
  if(!/\.jsonl$/i.test(file.name)||new TextEncoder().encode(file.name).length>240||/[\x00-\x1f\x7f/\\]/.test(file.name))throw new Error(t('cloudInvalidName'));
  if(!file.size)throw new Error(t('cloudInvalidJsonl'));
  if(file.size>CLOUD.maxFileBytes)throw new Error(t('cloudTooLarge'));
}
async function cloudUpload(file){
  cloudValidate(file);
  await cloudApi('backups?name='+encodeURIComponent(file.name),{method:'POST',headers:{'Content-Type':'application/x-ndjson'},body:file});
}
async function cloudRunQueue(){
  const pending=CLOUD.queue.filter(item=>item.state!=='done');
  for(let i=0;i<pending.length;i++){
    const item=pending[i];item.state='uploading';item.error='';
    CLOUD.message=t('cloudProgress').replace('{n}',i+1).replace('{m}',pending.length);cloudRender();
    try{await cloudUpload(item.file);item.state='done';}
    catch(e){item.state='error';item.error=e.message;if(e.status===401)break;}
    cloudRender();
  }
  const done=CLOUD.queue.filter(item=>item.state==='done').length,failed=CLOUD.queue.length-done;
  CLOUD.error=!!failed;
  CLOUD.message=failed?t('cloudPartial').replace('{n}',done).replace('{m}',failed):t('cloudComplete').replace('{n}',done);
  // Listing errors must never turn completed uploads into retryable uploads.
  if(CLOUD.user){try{await cloudList();}catch(e){CLOUD.message+=' '+e.message;CLOUD.error=true;}}
}
async function openCloud(files=[],auto=true){
  if(CLOUD.busy){if(!cloudDialog.open)cloudDialog.showModal();return;}
  CLOUD.queue=files.map(file=>({file,state:'waiting',error:''}));
  if(!cloudDialog.open)cloudDialog.showModal();
  await cloudTask(async()=>{
    CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;CLOUD.enabled=false;
    if(location.protocol==='file:'){CLOUD.message=t('cloudOnlineOnly');return;}
    const data=await (await cloudApi('auth/session')).json();
    CLOUD.enabled=data.enabled;CLOUD.user=data.user;CLOUD.maxFileBytes=data.maxFileBytes;
    if(!CLOUD.enabled){CLOUD.message=t('cloudUnavailable');return;}
    if(CLOUD.user){if(files.length&&auto)await cloudRunQueue();else await cloudList();}
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
async function cloudLogin(){
  await cloudTask(async()=>{
    let id;try{id=sessionStorage.getItem(CLOUD_PENDING_KEY);}catch(e){}
    id=id||crypto.randomUUID();
    const snapshot={id,createdAt:Date.now(),reading:cloudReadingSnapshot(),library:!$('#library').classList.contains('hide'),
      selected:[...LIB_SELECTED],files:CLOUD.queue.filter(item=>item.state!=='done').map(item=>item.file)};
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
  catch(e){await openCloud(snapshot.files,false);CLOUD.message=t('cloudPreserveFailed');CLOUD.error=true;cloudRender();return;}
  await openCloud(snapshot.files,result==='ready'&&Date.now()-snapshot.createdAt<60*60*1000);
  if(result==='login_failed'){CLOUD.message=t('cloudLoginFailed');CLOUD.error=true;cloudRender();}
}
$('#btnCloudLanding').onclick=()=>openCloud();
$('#btnCloud').onclick=()=>openCloud(CUR?[cloudFile(CUR.text,CUR.name||CUR.sum?.sessionId)]:[]);
$('#btnCloudManageLibrary').onclick=()=>openCloud();
$('#cloudViewSaved').onclick=()=>openCloud();
$('#btnCloudLibrary').onclick=()=>openCloud([...LIB_SELECTED].map(id=>LIB_FULL.get(id)).filter(rec=>rec?.text).map(rec=>cloudFile(rec.text,rec.name||rec.sum?.sessionId)));
$('#cloudClose').onclick=()=>cloudDialog.close();
cloudDialog.addEventListener('click',e=>{if(e.target===cloudDialog)cloudDialog.close();});
$('#cloudLogin').onclick=cloudLogin;
$('#cloudSubmit').onclick=()=>cloudTask(cloudRunQueue);
$('#cloudLogout').onclick=()=>cloudTask(async()=>{
  await cloudApi('auth/logout',{method:'POST'});CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;CLOUD.message=t('cloudLoggedOut');
});
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
      load(text,backup.name,false,null);CUR_ID=id;showView('viewer');renderNav();cloudDialog.close();
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
