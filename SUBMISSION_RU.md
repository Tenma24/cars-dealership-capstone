# Что сдавать — Cars Dealership

Репозиторий: https://github.com/Tenma24/cars-dealership-capstone

Работа основана на исходнике IBM. Ниже перечислены реальные файлы. Ссылка на учебный исходник IBM не заменяет ссылку на вашу выполненную работу.

| № | Что вставить / загрузить |
|---|---|
| 1 | https://github.com/Tenma24/cars-dealership-capstone/blob/main/README.md |
| 2 | Содержимое `evidence/django_server` |
| 3 | https://github.com/Tenma24/cars-dealership-capstone/blob/main/server/frontend/static/About.html |
| 4 | https://github.com/Tenma24/cars-dealership-capstone/blob/main/server/frontend/static/Contact.html |
| 5 | Содержимое `evidence/loginuser` |
| 6 | Содержимое `evidence/logoutuser` |
| 7 | https://github.com/Tenma24/cars-dealership-capstone/blob/main/server/frontend/src/components/Register/Register.jsx |
| 8 | Содержимое `evidence/getdealerreviews` |
| 9 | Содержимое `evidence/getalldealers` |
| 10 | Содержимое `evidence/getdealerbyid` |
| 11 | Содержимое `evidence/getdealersbyState` |
| 12 | `evidence/admin_login.png` |
| 13 | `evidence/admin_logout.png` |
| 14–15 | Содержимое `evidence/getallcarmakes` |
| 16 | Содержимое `evidence/analyzereview` |
| 17 | `evidence/get_dealers.png` |
| 18 | `evidence/get_dealers_loggedin.png` — переснять с адресной строкой |
| 19 | `evidence/dealersbystate.png` — переснять с адресной строкой |
| 20 | `evidence/dealer_id_reviews.png` — переснять с адресной строкой и видимым отзывом |
| 21 | `evidence/dealership_review_submission.png` |
| 22 | `evidence/added_review.png` |
| 23 | Содержимое `evidence/CICD`; [успешный запуск GitHub Actions](https://github.com/Tenma24/cars-dealership-capstone/actions/runs/39302067786) |
| 24–28 | Ожидают облачного развёртывания; локальный URL не заменяет публичный |

## Как переснять пункты 18–20

Запустите приложение по README и откройте Chrome. Войдите под `capstone`; локальный пароль находится в `LOCAL_ACCESS.txt`. Для 18 откройте `/dealers`: на снимке должны быть имя пользователя, Review Dealer и адресная строка. При необходимости уменьшите масштаб браузера до 80%. Для 19 выберите Kansas: URL станет `/dealers?state=Kansas`. Для 20 откройте `/dealer/8`, где уже добавлен отзыв в ходе проверки. Сохраняйте снимок всего окна браузера, а не только страницы. Замените соответствующие файлы в `evidence/`.

## cURL

В `SUBMISSION_ANSWERS.txt` собраны ссылки и фактические выводы команд по порядку задания, включая журнал успешного CI.

Файлы получены настоящими вызовами curl. В командах входа CSRF_TOKEN и login.json — обозначения временных файлов/переменных: `login.json` содержит userName и password, cookie jar получается запросом `/djangoapp/session`. Сам пароль и cookie jar не опубликованы. В ответе входа есть новый csrfToken для выхода. Повторный сбор: `python scripts/collect_curl.py` при запущенном приложении.

## Что ещё не завершено

- Снимки 18–20 с видимой адресной строкой: автоматический захват окна Windows остановлен инструментом; имеющиеся файлы — настоящие снимки содержимого страниц.
- IBM Cloud / Skills Network и пункты 24–28: пользователь сообщит доступ позже.
- Финальная отправка в Coursera не выполнялась.
