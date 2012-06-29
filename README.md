Novutec WhoisDaemon
====================

Novutec WhoisDaemon is a implementation of the RESTful Web Service for 
Domain Name Registration Data DRAFT.

See: http://tools.ietf.org/html/draft-sheng-weirds-icann-rws-dnrd-01

Copyright (c) 2007 - 2012 Novutec Inc. (http://www.novutec.com)
Licensed under the Apache License, Version 2.0 (the "License").

Installation
------------

Install using pip: `pip install -e git+git://github.com/novutec/WhoisDaemon.git`

Installing from source: `git clone git://github.com/novutec/WhoisDaemon.git; cd WhoisDaemon; python setup.py install`
    
Create your own configuration based on the example configuration file in example/config.yaml.
To use existing backend handlers, import existing structure SQL file to your database.

Usage
-----

* start in standalone daemon mode (only for debugging / testing):
`./whoisd -c <path_to_config>` 

* run as fcgi
`./whoisd.fcgi -c <path_to_config>`

* run by gunicorn (config should be /etc/whoisd.yaml)
`gunicorn whoisd`

For more deployment options, see http://flask.pocoo.org/docs/deploying/

3rd Party Libraries
-------------------

Thanks to developers of following used libraries:
 
* Flask: http://flask.pocoo.org
* Werkzeug: http://werkzeug.pocoo.org
* Jinja 2: http://jinja.pocoo.org
* oursql: http://packages.python.org/oursql/

in fcgi mode:
* flup.server: http://trac.saddi.com/flup

Issues
------

Please report any issues via https://github.com/novutec/WhoisDaemon/issues

LICENSE and COPYRIGHT
-----------------------

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
