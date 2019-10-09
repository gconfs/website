## GConfs Website

### Dependencies
* python3
* python3-dev
* libmysql

### Optional dependencies
* pipenv

### Installation - Using pipenv
* `pipenv install -r requirements.txt`
* `pipenv shell`
* `python manage.py migrate`

### Running a local copy
* `pipenv shell` (If not done already)
* `python manage.py runserver`
* Go to [http://127.0.0.1:8000](http://127.0.0.1:8000) using your web browser
