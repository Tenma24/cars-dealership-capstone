let csrfToken='';
export async function api(path, data) {
  const response=await fetch('/djangoapp/'+path,{credentials:'same-origin',headers:data?{'Content-Type':'application/json','X-CSRFToken':csrfToken}:{},method:data?'POST':'GET',body:data?JSON.stringify(data):undefined});
  let result;
  try { result=await response.json(); } catch { throw new Error('Unable to load this page. Please try again.'); }
  if(!response.ok) throw new Error(result.error||'Request failed. Please try again.');
  if(result.csrfToken) csrfToken=result.csrfToken;
  return result;
}
