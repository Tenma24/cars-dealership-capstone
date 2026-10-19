"""Collect actual cURL output from the running local services."""
import json, os, subprocess, tempfile
from pathlib import Path
root=Path(__file__).resolve().parents[1]
config=json.loads((root/'.local-config.json').read_text())
base=os.getenv('BASE_URL','http://127.0.0.1:8000')
evidence=root/'evidence';evidence.mkdir(exist_ok=True)
curl='curl.exe' if os.name=='nt' else 'curl'
def run(args):
    return subprocess.run([curl,'--silent','--show-error','--fail-with-body',*args],capture_output=True,text=True,check=True).stdout
def save(name,command,output):
    (evidence/name).write_text('$ '+command+'\n'+output+'\n',encoding='utf-8')
with tempfile.TemporaryDirectory(prefix='capstone-curl-') as temporary:
    cookies=str(Path(temporary)/'cookies.txt')
    session=json.loads(run(['-c',cookies,base+'/djangoapp/session']))
    payload=Path(temporary)/'login.json'
    payload.write_text(json.dumps({'userName':'capstone','password':config['DEMO_PASSWORD']}))
    output=run(['-b',cookies,'-c',cookies,'-H','Content-Type: application/json','-H','X-CSRFToken: '+session['csrfToken'],'--data-binary','@'+str(payload),base+'/djangoapp/login'])
    save('loginuser','curl -b cookies.txt -c cookies.txt -H "Content-Type: application/json" -H "X-CSRFToken: $CSRF_TOKEN" --data-binary @login.json '+base+'/djangoapp/login',output)
    csrf=json.loads(output)['csrfToken']
    output=run(['-b',cookies,'-X','POST','-H','X-CSRFToken: '+csrf,base+'/djangoapp/logout'])
    save('logoutuser','curl -b cookies.txt -X POST -H "X-CSRFToken: $CSRF_TOKEN" '+base+'/djangoapp/logout',output)
for name,endpoint in [('getdealerreviews','reviews/dealer/1'),('getalldealers','get_dealers'),('getdealerbyid','dealer/1'),('getdealersbyState','get_dealers/Kansas'),('getallcarmakes','get_cars')]:
    url=base+'/djangoapp/'+endpoint
    save(name,'curl '+url,run([url]))
url=os.getenv('SENTIMENT_URL','http://127.0.0.1:5050')+'/analyze/Fantastic%20services'
save('analyzereview','curl "'+url+'"',run([url]))
print('Saved eight actual cURL command outputs in evidence/. Password and session cookie files were temporary.')
