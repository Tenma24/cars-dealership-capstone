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

## GitHub Actions

Successful run: https://github.com/Tenma24/cars-dealership-capstone/actions/runs/39302067786

Commit tested: `56807712df9ed3ae87d6d1c17463689ae3be31be`. All workflow steps passed, including the Node integration tests against actual MongoDB and all three Playwright scenarios on Linux. Full original job output is saved in `evidence/CICD` (ANSI color sequences removed for readability).

The first CI run encountered MongoDB SERVER-121912 on the ubuntu-latest kernel. Pinning Ubuntu 22.04 and adding the MongoDB health check resolved this environment issue. No test was skipped to obtain the passing result. See https://jira.mongodb.org/browse/SERVER-125742 for compatibility details.

After formatting the frontend, the local Django process briefly retained the old template/asset hash; restarting the launcher and collecting static files restored the build. All three local browser tests passed again. Restart the launcher after rebuilding frontend assets.

## Remaining limits

Docker/Kubernetes runtime and IBM Cloud deployment were not run locally: Docker/ibmcloud CLIs were unavailable. There is no static type-check setup for this JavaScript/Python starter. Backend tests cover validation, CSRF rejection, session login/logout, trusted author identity, purchase date/car validation and upstream failure responses. Playwright screenshots omit browser chrome, so task 18–20 address-bar captures require manual completion. Local secrets and runtime databases are excluded from Git and deliverable ZIPs.
