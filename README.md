# flask-webtable
A very simple variant of the Flask tutorial to show and edit a single table.

This is mainly for my own reference.
Known limitations:
- not properly refactored
- no tests

## How to run

Windows CMD

cd flask-webtable
(first time: py -3 -m venv venv)
venv\Scripts\activate
(first time: pip install Flask)
set FLASK_APP=flaskwebtable
set FLASK_ENV=development
(first time: flask init-db)
flask run
