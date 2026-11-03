/* Cloud backups are opt-in: no requests until the panel opens or OAuth returns. */
const CLOUD={enabled:false,user:null,busy:false,backups:[],cursor:null,maxFileBytes:20*1024*1024,message:'',error:false};
const cloudDialog=$('#cloudBackup');
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
    throw new Error(t(CLOUD_ERRORS[code]||(response.status===404?'cloudUnavailable':'cloudRequestFailed')));
  }
  return response;
}
function cloudRender(){
  $('#cloudAccount').textContent=!CLOUD.enabled?'':CLOUD.user?'GitHub · @'+CLOUD.user.login:t('cloudLoginRequired');
  $('#cloudLogin').hidden=!CLOUD.enabled||!!CLOUD.user;
  $('#cloudLogout').hidden=!CLOUD.user;
  $('#cloudActions').hidden=!CLOUD.user;
  $('#cloudCurrent').hidden=!CUR||!CLOUD.user;
  $('#cloudCurrentName').textContent=CUR?(CUR.name||t('pastedContent')):'';
  $('#cloudStatus').textContent=CLOUD.busy?t('cloudWorking'):CLOUD.message;
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
  CLOUD.backups=append?[...CLOUD.backups,...data.backups]:data.backups;
  CLOUD.cursor=data.cursor;
}
async function openCloud(){
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
async function cloudUpload(file){
  if(!/\.jsonl$/i.test(file.name))throw new Error(t('cloudInvalidName'));
  if(!file.size)throw new Error(t('cloudInvalidJsonl'));
  if(file.size>CLOUD.maxFileBytes)throw new Error(t('cloudTooLarge'));
  await cloudApi('backups?name='+encodeURIComponent(file.name),{method:'POST',headers:{'Content-Type':'application/x-ndjson'},body:file});
  await cloudList();CLOUD.message=t('cloudUploaded');
}
$('#btnCloudLanding').onclick=openCloud;
$('#btnCloud').onclick=openCloud;
$('#btnCloudLibrary').onclick=openCloud;
$('#cloudClose').onclick=()=>cloudDialog.close();
cloudDialog.addEventListener('click',e=>{if(e.target===cloudDialog)cloudDialog.close();});
$('#cloudLogin').onclick=()=>{location.href='/api/auth/github?returnTo='+encodeURIComponent(location.pathname);};
$('#cloudLogout').onclick=()=>cloudTask(async()=>{
  await cloudApi('auth/logout',{method:'POST'});CLOUD.user=null;CLOUD.backups=[];CLOUD.cursor=null;CLOUD.message=t('cloudLoggedOut');
});
$('#cloudRefresh').onclick=()=>cloudTask(()=>cloudList());
$('#cloudMore').onclick=()=>cloudTask(()=>cloudList(true));
$('#cloudPick').onclick=()=>$('#cloudFile').click();
$('#cloudFile').onchange=e=>{const file=e.target.files[0];e.target.value='';if(file)cloudTask(()=>cloudUpload(file));};
$('#cloudUploadCurrent').onclick=()=>{
  if(!CUR)return;
  const name=(CUR.name||'session').replace(/\.(jsonl|json|txt)$/i,'')+'.jsonl';
  const file=new File([CUR.text],name,{type:'application/x-ndjson'});
  cloudTask(()=>cloudUpload(file));
};
$('#cloudList').onclick=e=>{
  const button=e.target.closest('button[data-action]'),row=e.target.closest('.cloud-row');
  if(!button||!row||CLOUD.busy)return;
  const backup=CLOUD.backups.find(item=>item.id===row.dataset.id);if(!backup)return;
  const action=button.dataset.action;
  if(action==='delete'&&!confirm(t('cloudConfirmDelete').replace('{name}',backup.name)))return;
  cloudTask(async()=>{
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
      // Save before opening so a session switch cannot redirect the cache write.
      const id=await saveToLibrary(text,backup.name,'cloud');
      load(text,backup.name,false,null);CUR_ID=id;showView('viewer');renderNav();cloudDialog.close();
    }
  });
};
const cloudResult=new URLSearchParams(location.search).get('cloud');
if(cloudResult==='ready'||cloudResult==='login_failed'){
  const cleanUrl=new URL(location.href);cleanUrl.searchParams.delete('cloud');history.replaceState(null,'',cleanUrl.href);
  openCloud().then(()=>{if(cloudResult==='login_failed'){CLOUD.message=t('cloudLoginFailed');CLOUD.error=true;cloudRender();}});
}
