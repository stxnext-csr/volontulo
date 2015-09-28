# volontulo

[![Join the chat at https://gitter.im/stxnext-csr/volontulo](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/stxnext-csr/volontulo?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build Status](https://travis-ci.org/stxnext-csr/volontulo.svg)](https://travis-ci.org/stxnext-csr/volontulo)
[![codecov.io](http://codecov.io/github/stxnext-csr/volontulo/coverage.svg?branch=master)](http://codecov.io/github/stxnext-csr/volontulo?branch=master)

![Volontulo logo](/volontulo/static/volontulo/img/volo_logo.png)

Web portal for collaboration of community volunteers with organizations and institutions. 

## Gulp Instalation

Gulp is used to prepare and serve all static files into `/volontulo_org/volontulo/volontulo/static/volontulo` so Django can use them
```
cd /volontulo_org/volontulo/volontulo
npm install
```
Windows can have problems with unix paths, so it is practical to install Gulp globally (with `sudo` on linux)
```
npm install -g gulp
```
### Using Gulp
```
gulp watch
```
