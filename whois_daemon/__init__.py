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

__all__ = ["commands", "routing", "objects"]

import sys, daemon, os
from flask import Flask
import commands, routing
from jinja2 import FileSystemLoader

class app(object):
    wsgi = True
    routing = None
    config = None
    app = None

    def __init__(self, configfile = '/etc/whoisd.yaml'):
        """
        Constructor
        Loads config and initialize app (backend)
        """

        # load config
        try:
            self.config = commands.load_config(configfile)

        except Exception, e:
            print "Error occoured while loading configuration file: " + str(e)
            sys.exit(1)

        # allocate instance of Flask
        self.app = Flask(__name__)

        self.app.jinja_loader = FileSystemLoader(self.config['daemon']['template_path'])

        # add routing of our application
        self.routing = routing.route(self.app, self.config)

    def get_context(self):
        return daemon.DaemonContext(working_directory = self.config['daemon']['cwd'],
                                    uid = self.config['daemon']['uid'],
                                    gid = self.config['daemon']['gid'],
                                    chroot_directory = self.config['daemon']['chroot_directory'],
                                    detach_process = self.config['daemon']['detach'],
                                    pidfile = self.config['daemon']['pid'])

    def run(self):
        """
        start standalone daemon
        """
        debug_mode = (self.config['daemon'].has_key('debug') and self.config['daemon']['debug'])
        if self.config['daemon']['detach']:
            context = self.get_context()
            with context:
                self.app.run(self.config['daemon']['bind'],
                             self.config['daemon']['port'],
                             debug = debug_mode)
        else :
            self.app.run(self.config['daemon']['bind'],
                         self.config['daemon']['port'],
                         debug = debug_mode)

    def __call__(self, environ, start_response):
        """
        redirect all calls to local WSGI handler

        @param environ: a WSGI environment
        @param start_response: a callable accepting a status code,
                               a list of headers and an optional
                               exception context to start the response
        """
        return self.wsgi_app(environ, start_response)

    def wsgi_app(self, environ, start_response):
        """
        WSGI application handler.
        Redirect call directly to Flask
        
        @param environ: a WSGI environment
        @param start_response: a callable accepting a status code,
                               a list of headers and an optional
                               exception context to start the response
        """
        return self.app.wsgi_app(environ, start_response)

def application(environ, start_response):
    x = app()
    return x.wsgi_app(environ, start_response)
