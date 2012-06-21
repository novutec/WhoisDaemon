"""
Copyright (c) 2007 - 2012 Novutec Inc. (http://www.novutec.com)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

@category   Novutec
@package    whois_daemon
@copyright  Copyright (c) 2007 - 2012 Novutec Inc. (http://www.novutec.com)
@license    http://www.apache.org/licenses/LICENSE-2.0
"""

from logging.handlers import SysLogHandler
import logging
import commands

class route(object):
    """
    class to define routing of http daemon.
    """
    app = None
    config = None
    appCall = None

    error_levels = {
        'ERROR'   : logging.ERROR,
        'WARNING' : logging.WARNING,
        'INFO'    : logging.INFO,
        'DEBUG'   : logging.DEBUG
    }

    def __init__(self, app, config):
        """
        Initializer of application.
        Create new instance of call handler and starts backend handler (database)
        
        @param app: flask app instance
        @param config: global config dict 
        """
        self.app = app
        self.config = config

        logging_handler = None
        if config['daemon']['logging']['module'] == 'syslog' :
            if (not config['daemon']['logging'].has_key('dest') or
                not config['daemon']['logging']['dest'] or
                config['daemon']['logging']['dest'] == 'localhost') :
                logging_handler = SysLogHandler('/dev/log')
            else :
                logging_handler = SysLogHandler(config['daemon']['logging']['dest'])
        elif config['daemon']['logging']['module'] == 'file' :
            if (not config['daemon']['logging'].has_key('dest') or
                not config['daemon']['logging']['dest']) :
                raise Exception('Invalid logging destination defined in config!')

            logging_handler = logging.FileHandler(config['daemon']['logging']['dest'])
        else :
            raise Exception('Invalid logging module defined in config!')

        for (level_str, level) in self.error_levels.iteritems() :
            if (config['daemon']['logging']['level'].upper() == level_str) :
                logging_handler.setLevel(level)

        app.logger.addHandler(logging_handler)

        self.appCall = commands.appCall(app, config)
        self.appCall.init()
        app.error_handler_spec[None][404] = self.appCall.object_not_found
        app.error_handler_spec[None][500] = self.appCall.invalid_request
        self.add_routes()

    def add_routes(self):
        """
        defines routes that available in this service and link them to method in appCall
        """
        self.app.add_url_rule('/domain/<name>', 'get_domain', self.appCall.get_domain)
        self.app.add_url_rule('/domain/<name>/', 'get_domain', self.appCall.get_domain)
        self.app.add_url_rule('/domain/<name>/hosts', 'get_domain_hosts', self.appCall.get_domain_hosts)
        self.app.add_url_rule('/domain/<name>/registration', 'get_domain_registration', self.appCall.get_domain_registration)
        self.app.add_url_rule('/domain/<name>/registrar', 'get_domain_registrar', self.appCall.get_domain_registrar)
        self.app.add_url_rule('/domain/<name>/contacts', 'get_domain_contacts', self.appCall.get_domain_contacts)
        self.app.add_url_rule('/domain/<name>/contacts/<filter>', 'get_domain_contacts_filtered', self.appCall.get_domain_contacts)
        self.app.add_url_rule('/contact/<roid>', 'get_contact', self.appCall.get_contact)
        self.app.add_url_rule('/contact/<roid>/', 'get_contact', self.appCall.get_contact)
        self.app.add_url_rule('/contact/<roid>/registration', 'get_contact_registration', self.appCall.get_contact_registration)
        self.app.add_url_rule('/contact/<roid>/registrar', 'get_contact_registrar', self.appCall.get_contact_registrar)
        self.app.add_url_rule('/host/<name>', 'get_host', self.appCall.get_host)
        self.app.add_url_rule('/host/<name>/', 'get_host', self.appCall.get_host)
        self.app.add_url_rule('/host/<name>/registration', 'get_host_registration', self.appCall.get_host_registration)
        self.app.add_url_rule('/host/<name>/registrar', 'get_host_registrar', self.appCall.get_host_registrar)
        self.app.add_url_rule('/registrar/<roid>', 'get_registrar_roid', self.appCall.get_registrar_roid)
        self.app.add_url_rule('/registrar/"<name>"', 'get_registrar_name', self.appCall.get_registrar_name)
