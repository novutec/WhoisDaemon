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

import os, yaml, objects, flask, re, werkzeug
from pwd import getpwnam
from flask import request
import backends
from formater import *

base_config = {
    'daemon' : {
        'bind': '0.0.0.0',
        'port': 5000,
        'debug': 1,
        'detach': 1, # start daemonized
        'template_path' : 'templates/',
        'umask' : 002,
        'chroot_directory' : None,
        'uid': os.getuid(), # run with current user
        'gid': os.getgid(), # run with current group
        'cwd': os.getcwd(),
        'pid' : '/var/run/whoisd.pid',
        'logging': {
            'module':   'file',
            'dest':     '/var/log/whoisd.log',
            'level':    'error',
            'format':   '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
        }
    },

    'backend': { # configuration of the used backend handler
        'module': None
    }
}

def load_config(fname):
    """
    load config yaml encoded config file by given filename
    
    @param fname: config filename
    
    @return: loaded config as dict
    """
    f = open(fname)
    loaded_config = yaml.load(f)
    f.close()
    config = base_config
    for ky in config.keys() :
        config[ky].update(loaded_config[ky])

    if config['daemon'].has_key('user') :
        config['daemon']['uid'] = getpwnam(config['daemon']['user']).pw_uid

    return config

class appCall(object):
    """
    main class to handle all calls by protocol handler
    """
    app = None      # flask protocol handler
    config = None   # main config
    dbh = None      # database backend handler instance

    """
    needed for matching requests like /host/127.0.0.1 or /host/2001:500:88:200::1
    """
    __ipv4_match = re.compile('^(\d+)\.(\d+)\.(\d+)\.(\d+)$')
    __ipv6_match = re.compile('^\s*((([0-9A-Fa-f]{1,4}:){7}(([0-9A-Fa-f]{1,4})|:))|(([0-9A-Fa-f]{1,4}:){6}(:|((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})|(:[0-9A-Fa-f]{1,4})))|(([0-9A-Fa-f]{1,4}:){5}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:){4}(:[0-9A-Fa-f]{1,4}){0,1}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:){3}(:[0-9A-Fa-f]{1,4}){0,2}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:){2}(:[0-9A-Fa-f]{1,4}){0,3}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(([0-9A-Fa-f]{1,4}:)(:[0-9A-Fa-f]{1,4}){0,4}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(:(:[0-9A-Fa-f]{1,4}){0,5}((:((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})?)|((:[0-9A-Fa-f]{1,4}){1,2})))|(((25[0-5]|2[0-4]\d|[01]?\d{1,2})(\.(25[0-5]|2[0-4]\d|[01]?\d{1,2})){3})))(%.+)?\s*$')

    def __init__(self, app, config):
        """
        Constructor
        
        @param app: flask app instance
        @param config: global config dict 
        """
        self.app = app
        self.config = config

    def init(self):
        """
        loads active backend handler (for example MySQL)
        """
        self.dbh = backends.factory(self.config['backend'])

    def object_not_found(self, e):
        """
        global error handler
        
        @param e: exception that caused the error
        """
        return "Object not found", 404

    def invalid_request(self, e):
        """
        global error handler
        
        @param e: exception that caused the error
        """
        return "Invalid request", 50

    def __get_requested_formater(self):
        """
        helper method to return the requested formater by client http request header
        
        search in Client request header in 'Accept' for the allowed format types.
        If non matching or no Accept header given, use html.  
        
        @return: instance of selected formater
        """
        allowed_types = {
            'application/xml'  : xmlFrm,
            'application/json' : jsonFrm,
            'application/yaml' : yamlFrm,
            'text/html'        : htmlFrm,
            'text/plain'       : textFrm
        }

        default = htmlFrm

        if not request.headers['Accept'] :
            return default

        for (mime_type, quality) in werkzeug.http.parse_accept_header(request.headers['Accept']) :
            if allowed_types.has_key(mime_type) :
                return allowed_types[mime_type]
        return default

    @staticmethod
    def validate_ascii(valstr):
        """
        helper method to validate if given string is ASCII only
        
        @param valstr: string to validate
        
        @return: Boolean value if string is ASCII
        """
        try:
            valstr.decode('ascii')
        except UnicodeEncodeError:
            return False
        except UnicodeDecodeError:
            return False
        return True

    @staticmethod
    def get_domain_ascii(name):
        """
        checks if domain is ASCII only or convert to puny encoded string
        
        @param name: domain name to validate/convert
        
        @return: validated/converted domain name
        """
        if appCall.validate_ascii(name) :
            return name
        return name.encode('idna')

    @staticmethod
    def get_domain_idn(name):
        """
        checks if domain is non-ASCII or convert to encoded string

        @param name: domain name to validate/convert
        
        @return: validated/converted domain name
        """
        if not appCall.validate_ascii(name) and name[:4] != 'xn--' :
            return name
        return name.decode('idna')

    def __format_result(self, result):
        """
        helper method to format given result object by the requested formater
        
        @param result: instance of result object
        
        @return: output of formater instance
        """
        return self.__get_requested_formater().format(result)

    def __get_host(self, filter):
        """
        helper method to get host object by given filter
        
        @param filter: dict with filter paramters
        
        @return: fetched object 
        """
        host = self.dbh.get_host(filter)
        if not host :
            flask.abort(404)

        return host

    def __get_hosts_by_ip(self, filter):
        """
        helper method to get host objects by given filter
        
        @param filter: dict with filter paramters
        
        @return: fetched objects
        """
        hosts = self.dbh.get_hosts_by_ip(filter)
        if not hosts :
            flask.abort(404)

        return hosts

    def __check_name_for_ip(self, name):
        """
        helper method to get host by ipv4/ipv6 IP address
        
        @param name: IP as string to search for
        
        @return: result Object with fetched hosts
        """
        m_v4 = self.__ipv4_match.match(name)
        m_v6 = self.__ipv6_match.match(name)

        if m_v4 :
            ip_parts = m_v4.groups()
            """Validate IP"""
            if (len(ip_parts) == 4 and
                int(ip_parts[0]) <= 255 and
                int(ip_parts[1]) <= 255 and
                int(ip_parts[2]) <= 255 and
                int(ip_parts[3]) <= 255) :
                return objects.Result(
                    items = self.__get_hosts_by_ip({'ip' : name, 'type' : 4})
                )
        elif m_v6 :
            return objects.Result(
                items = self.__get_hosts_by_ip({'ip' : name, 'type' : 6})
            )
        # invalid IP format given
        flask.abort(500)

    def get_host(self, name) :
        """
        handling of /host/<name> requests
        
        @param name: name of host to search for
        
        @return: matching object(s) + additionals data by given name / ipv4 / ipv6 
        """
        name = appCall.get_domain_ascii(name)
        result = self.__check_name_for_ip(name)
        if not result :
            host = self.__get_host({'name' : name})
            result = objects.Result(
                items = [ host ]
            )

        result.additional = []
        registrar_ids = []
        for registrar in host.registrar :
            if not registrar.id in registrar_ids :
                registrar_ids.append(registrar.id)

        for registrar_id in registrar_ids :
            result.additional.append(self.dbh.get_registrar({'registrar_id' : registrar_id}))

        return self.__format_result(result)

    def get_host_registration(self, name) :
        """
        handling of /host/<name>/registration requests
        
        @param name: name of host to search for
        
        @return: matching registration object(s) by given name / ipv4 / ipv6
        """
        name = appCall.get_domain_ascii(name)
        result = self.__check_name_for_ip(name)
        if result :
            return result
        return self.__format_result(objects.Result(
            items = [ self.__get_host({'name' : name}) ]
        ))

    def get_host_registrar(self, name) :
        """
        handling of /host/<name>/registrar requests
        fail if IP is used in more than one host object (no reference to host)
        
        @param name: name of host to search for
        
        @return: matching sponsoring registrar object by given name / ipv4 / ipv6
        """
        name = appCall.get_domain_ascii(name)
        result = self.__check_name_for_ip(name)
        if result :
            if len(result.items) > 1 :
                flask.abort(500)
            for registrar in result.items[0].registrar :
                if registrar.type == 'sponsor' :
                    return self.get_registrar_roid(registrar.roid)
            flask.abort(404)

        host = self.__get_host({ 'name' : name })
        for registrar in host.registrar :
            if registrar.type == 'sponsor' :
                return self.get_registrar_roid(registrar.roid)

        flask.abort(404)

    def __get_contact_data(self, roid):
        """
        helper method to get contact data by given roid
        
        @param roid: ROID to fetch
        
        @return: matching contact
        """
        contact = self.dbh.get_contact({
            'roid'   : roid
        })

        if not contact :
            flask.abort(404)

        return contact

    def get_contact(self, roid) :
        """
        handling of /contact/<name> requests
        
        @param roid: ROID to fetch
                
        @return: matching object + additionals data by given roid 
        """
        contact = self.__get_contact_data(roid)
        result = objects.Result(
            items = [ contact ]
        )

        result.additional = []
        registrar_ids = []
        for registrar in contact.registrar :
            if not registrar.id in registrar_ids :
                registrar_ids.append(registrar.id)

        for registrar_id in registrar_ids :
            result.additional.append(self.dbh.get_registrar({'registrar_id' : registrar_id}))

        return self.__format_result(result)

    def get_contact_registration(self, roid):
        """
        handling of /contact/<name>/registration requests
        
        @param roid: ROID to fetch
                
        @return: matching registration object by given roid
        """
        return self.__format_result(objects.Result(
            items = [ self.__get_contact_data(roid) ]
        ))

    def get_contact_registrar(self, roid) :
        """
        handling of /contact/<name>/registrar requests
        
        @param roid: ROID to fetch
                
        @return: sponsoring registrar object by given contact roid
        """
        contact = self.dbh.get_contact({
            'roid'   : roid
        })

        if not contact :
            flask.abort(404)

        for registrar in contact.registrar :
            if registrar.type == 'sponsor' :
                return self.get_registrar_roid(registrar.roid)

        flask.abort(404)

    def get_registrar_roid(self, roid) :
        """
        handling of /registrar/<name> requests

        @param roid: ROID to fetch                
        
        @return: registrar object by given roid
        """
        registrar = self.dbh.get_registrar({
            'roid'   : roid
        })

        if not registrar :
            flask.abort(404)

        return self.__format_result(objects.Result(
            items = [ registrar ]
        ))

    def get_registrar_name(self, name) :
        """
        handling of /registrar/"<name>" requests

        @param name: name of registrar to fetch
                        
        @return: registrar object by given name
        """
        registrar = self.dbh.get_registrar({
            'name'   : name
        })

        if not registrar :
            flask.abort(404)

        return self.__format_result(objects.Result(
            items = [ registrar ]
        ))

    def __get_domain_registration_data(self, name):
        """
        helper function to get domain object

        @param name: name of domain to fetch
        
        @return: domain object
        """
        domain = self.dbh.get_domain({ 'name' : name })
        if not domain :
            flask.abort(404)

        return domain

    def __get_domain_contacts_data(self, domain):
        """
        helper function to get additionals for given domain 
        
        @param domain: name of domain to fetch contacts of
        
        @return: array of Contact Objects
        """
        contact_ids = [
            domain.registrant.id
        ]

        for contact in domain.contact :
            if not contact.id in contact_ids :
                contact_ids.append(contact.id)

        items = []
        for contact_id in contact_ids :
            items.append(self.dbh.get_contact({'contact_id' : contact_id}))

        return items

    def get_domain(self, name):
        """
        handling of /domain/<name> requests
        
        @param name: name of domain 
        
        @return: domain object + additionals (contacts, registrar, hosts) by given name
        """
        name = appCall.get_domain_ascii(name)
        domain = self.dbh.get_domain({ 'name' : name })

        if not domain :
            flask.abort(404)

        domain.name_idn = appCall.get_domain_idn(name)
        result = objects.Result(
            items = [ domain ],
            additional = self.__get_domain_contacts_data(domain)
        )

        for ns in domain.ns :
            if isinstance(ns, objects.DomainHostObj) :
                result.additional.append(self.dbh.get_host({'host_id' : ns.id}))

        registrar_ids = []
        for registrar in domain.registrar :
            if not registrar.id in registrar_ids :
                registrar_ids.append(registrar.id)

        for registrar_id in registrar_ids :
            result.additional.append(self.dbh.get_registrar({'registrar_id' : registrar_id}))

        return self.__format_result(result)

    def get_domain_hosts(self, name):
        """
        handling of /domain/<name>/hosts requests
        
        @param name: name of domain
        
        @return: host objects connected to given domain
        """
        name = appCall.get_domain_ascii(name)
        hosts = self.dbh.get_domain_hosts({ 'domain_name' : name })

        if len(hosts) < 1 :
            flask.abort(404)

        return self.__format_result(objects.Result(
            items = hosts
        ))

    def get_domain_registration(self, name):
        """
        handling of /domain/<name>/registration requests
        
        @param name: name of domain
        
        @return: domain object by given name
        """
        name = appCall.get_domain_ascii(name)
        domain = self.__get_domain_registration_data(name)
        domain.name_idn = appCall.get_domain_idn(name)

        return self.__format_result(objects.Result(
            items = [ domain ]
        ))

    def get_domain_contacts(self, name, filter = None):
        """
        handling of /domain/<name>/contacts requests
        
        @param name: name of domain
        @param filter: dict of filter options
        
        @return: contact objects connected to given domain
        """
        name = appCall.get_domain_ascii(name)
        domain = self.__get_domain_registration_data(name)
        if filter :
            if filter == 'registrant' :
                return self.get_contact(domain.registrant.roid)
            else :
                for contact in domain.contact :
                    if contact.type == filter :
                        return self.get_contact(contact.roid)
                flask.abort(404)

        return self.__format_result(objects.Result(
            items = self.__get_domain_contacts_data(domain)
        ))

    def get_domain_registrar(self, name):
        """
        handling of /domain/<name>/registrar requests
        
        @param name: name of domain
        
        @return: sponsoring registrar object by given domain
        """
        name = appCall.get_domain_ascii(name)
        domain = self.dbh.get_domain({ 'name' : name })
        for registrar in domain.registrar :
            if registrar.type == 'sponsor' :
                return self.get_registrar_roid(registrar.roid)
        flask.abort(404)
