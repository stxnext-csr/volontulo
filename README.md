# volontulo

[![Join the chat at https://gitter.im/stxnext-csr/volontulo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/stxnext-csr/volontulo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/stxnext-csr/volontulo.svg)](https://travis-ci.org/stxnext-csr/volontulo)
[![codecov.io](http://codecov.io/github/stxnext-csr/volontulo/coverage.svg?branch=master)](http://codecov.io/github/stxnext-csr/volontulo?branch=master)

![Volontulo logo](/volontulo/frontend/img/volo_logo.png)

Web portal for collaboration of community volunteers with organizations and institutions. 

## Project Set Up

Usage of virtualenv is recommended. Assuming you use Virtualenvwrapper:
```
mkvirtualenv --no-site-packages venv_name
```
To install project dependencies use pip and choose the correct file (production, development, etc.)
```
pip install -r requirements/development.txt
```

Copy the Local Configuration file:
```
cp local_config.yaml.sample local_config.yaml
vim local_config.yaml
```

Fill the Local Configuration Values.
To generate "secret_key", you can use
```head -c 64 /dev/urandom | base64 -w 0```

If the site is supposed to be served under different domain than volontulo.org or volontuloapp.org
and you are not in development environment, fiil the "allowed_host" value. Otherwise
it can be left blank.

### Gulp Instalation

Gulp is used to prepare and serve all static files into `/volontulo_org/volontulo/volontulo/static/volontulo` so Django can use them
```
cd /apps/volontulo
npm install
```
Windows can have problems with unix paths, so it is practical to install Gulp globally (with `sudo` on linux)
```
npm install -g gulp
```
### Using Gulp
In development
```
gulp watch
```
Otherwise
```
gulp build
```

### Running the App in development mode
Choose the appriopriate settings file
```
python manage runserver --settings=volontulo_org.settings.dev
```
Now you able to access the development site:
[http://localhost:8000](http://localhost:8000)

### Running tests
To run the project tests:
```
coverage run --source='.' manage.py test --settings=volontulo_org.settings.test_settings -v 3
```

