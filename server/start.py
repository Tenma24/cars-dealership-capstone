import os,subprocess,sys
for args in [('migrate','--noinput'),('seed_cars',)]:
    subprocess.run([sys.executable,'manage.py',*args],check=True)
from waitress import serve
from djangoproj.wsgi import application
serve(application,host='0.0.0.0',port=int(os.getenv('PORT','8000')))
