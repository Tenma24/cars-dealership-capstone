from pathlib import Path
root=Path(__file__).resolve().parents[1]
repo='https://github.com/Tenma24/cars-dealership-capstone/blob/main/'
entries=[
('1',repo+'README.md'),('2','@django_server'),
('3',repo+'server/frontend/static/About.html'),('4',repo+'server/frontend/static/Contact.html'),
('5','@loginuser'),('6','@logoutuser'),('7',repo+'server/frontend/src/components/Register/Register.jsx'),
('8','@getdealerreviews'),('9','@getalldealers'),('10','@getdealerbyid'),('11','@getdealersbyState'),
('12','Upload evidence/admin_login.png'),('13','Upload evidence/admin_logout.png'),('14–15','@getallcarmakes'),('16','@analyzereview'),
('17','Upload evidence/get_dealers.png'),
('18','Retake evidence/get_dealers_loggedin.png with the browser address bar, username and Review Dealer option visible.'),
('19','Retake evidence/dealersbystate.png with the browser address bar visible.'),
('20','Retake evidence/dealer_id_reviews.png with the browser address bar visible. Use /dealer/8 to include the posted review.'),
('21','Upload evidence/dealership_review_submission.png'),('22','Upload evidence/added_review.png'),('23','@CICD'),
('24–28','Pending IBM Cloud / Skills Network deployment. Do not submit a local URL as a deployed URL.')]
parts=['CARS DEALERSHIP — SUBMISSION ANSWERS\nActual local evidence. Items requiring additional work are explicitly marked.\n']
for number,value in entries:
    if value.startswith('@'):
        path=root/'evidence'/value[1:]
        value=path.read_text(encoding='utf-8',errors='replace') if path.exists() else 'PENDING: '+path.name
    parts.append('\n'+'='*60+'\nTASK '+number+'\n'+'='*60+'\n'+value+'\n')
(root/'SUBMISSION_ANSWERS.txt').write_text(''.join(parts),encoding='utf-8')
