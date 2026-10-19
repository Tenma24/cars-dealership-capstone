"""Start all three services. Use --setup to install/build first."""
import json, os, secrets, subprocess, sys, time
from pathlib import Path
root=Path(__file__).resolve().parents[1]
server=root/'server'
config_file=root/'.local-config.json'
if not config_file.exists():
    config_file.write_text(json.dumps({'SERVICE_TOKEN':secrets.token_urlsafe(32),'ADMIN_PASSWORD':secrets.token_urlsafe(18),'DEMO_PASSWORD':secrets.token_urlsafe(18)}))
config=json.loads(config_file.read_text())
env={**os.environ,**config,'DJANGO_DEBUG':'1','DATA_MODE':'file','PYTHONUNBUFFERED':'1'}
if '--setup' in sys.argv:
    npm='npm.cmd' if os.name=='nt' else 'npm'
    for folder in ['database','frontend']:
        subprocess.run([npm,'ci'],cwd=server/folder,check=True)
    subprocess.run([npm,'run','build'],cwd=server/'frontend',check=True)
for args in [['migrate','--noinput'],['seed_cars'],['collectstatic','--noinput']]:
    subprocess.run([sys.executable,'manage.py',*args],cwd=server,env=env,check=True)
code="from django.contrib.auth.models import User; import os; u,_=User.objects.get_or_create(username='root'); u.is_staff=True; u.is_superuser=True; u.set_password(os.environ['ADMIN_PASSWORD']); u.save(); d,_=User.objects.get_or_create(username='capstone'); d.first_name='Alex'; d.last_name='Morgan'; d.set_password(os.environ['DEMO_PASSWORD']); d.save()"
subprocess.run([sys.executable,'manage.py','shell','-c',code],cwd=server,env=env,check=True)
(root/'LOCAL_ACCESS.txt').write_text('Local demonstration only — do not upload this file.\nURL: http://127.0.0.1:8000\nUsername: capstone\nPassword: '+config['DEMO_PASSWORD']+'\nAdmin URL: http://127.0.0.1:8000/admin/\nUsername: root\nPassword: '+config['ADMIN_PASSWORD']+'\n')
evidence=root/'evidence';evidence.mkdir(exist_ok=True)
processes=[];handles=[]
try:
    for name,command,cwd in [
      ('node_server',['node','app.js'],server/'database'),
      ('sentiment_server',[sys.executable,'app.py'],server/'djangoapp/microservices'),
      ('django_server',[sys.executable,'manage.py','runserver','127.0.0.1:8000','--noreload'],server)]:
        handle=(evidence/name).open('w');handles.append(handle)
        processes.append(subprocess.Popen(command,cwd=cwd,env=env,stdout=handle,stderr=subprocess.STDOUT))
    print('Running: http://127.0.0.1:8000 — credentials in LOCAL_ACCESS.txt',flush=True)
    while all(p.poll() is None for p in processes): time.sleep(1)
    raise RuntimeError('A service stopped; inspect evidence service logs')
except KeyboardInterrupt:
    pass
finally:
    for process in processes: process.terminate()
    for handle in handles: handle.close()
