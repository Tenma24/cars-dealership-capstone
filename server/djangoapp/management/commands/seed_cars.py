import json
from django.core.management.base import BaseCommand
from django.conf import settings
from djangoapp.models import CarMake,CarModel
class Command(BaseCommand):
    help='Seed the IBM car catalog without deleting existing data'
    def handle(self,*args,**options):
        records=json.loads((settings.BASE_DIR/'database/data/car_records.json').read_text())['cars']
        for row in records:
            make,_=CarMake.objects.get_or_create(name=row['make'])
            CarModel.objects.get_or_create(car_make=make,name=row['model'],year=row['year'],defaults={'type':row.get('bodyType','Sedan')})
        self.stdout.write(f'{CarMake.objects.count()} makes, {CarModel.objects.count()} models available')
