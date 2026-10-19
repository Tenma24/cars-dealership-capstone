# Verification evidence

User journeys derived from the supplied 28-task rubric and the IBM starter repository.

## RED / GREEN

- RED: `python manage.py test djangoapp` executed 8 acceptance tests against the original starter. All 8 failed with 404 responses because required API routes were absent. Checkpoint commit: `67bde8a`.
- GREEN: the same account tests pass after implementation. The expanded Django suite has 15 passing tests.
- Coverage: `coverage run --source=djangoapp --omit='*/tests.py,*/migrations/*,*/microservices/*,*/management/*,*/populate.py' manage.py test djangoapp`; `coverage report --fail-under=80`: 169 executable statements, 100% statement coverage. This is backend coverage only, not a claim of frontend or branch coverage.
- Flask: 2 tests pass (positive/negative/neutral classification and invalid input).
- Node: 2 tests pass locally in explicit file mode (queries, protected writes, persistence). MongoDB integration is configured in GitHub Actions.
- React production build: Vite build succeeded.
- Browser: 3 Playwright scenarios pass: register/filter/review/logout; admin login/logout; mobile and informational pages. An initial test selector matched a select label too narrowly; corrected to match the actual label text and reran successfully.
- Both npm dependency audits reported zero vulnerabilities at install time.

## Limits

Docker/Kubernetes runtime and IBM Cloud deployment were not run locally: Docker/ibmcloud CLIs were unavailable. There is no static type-check setup for this JavaScript/Python starter. Backend tests cover validation, CSRF rejection, session login/logout, trusted author identity, purchase date/car validation and upstream failure responses. Playwright screenshots omit browser chrome, so task 18–20 address-bar captures require manual completion. Local secrets and runtime databases are excluded from Git and deliverable ZIPs.
