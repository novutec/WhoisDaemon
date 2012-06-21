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

from flask import render_template
from whois_daemon import objects, formater
import flask

def __format_additionals(additional):
    """
    helper function to "reformat" linked objects as named dict
    
    @param additional: Array of additional items
    
    @return: dict of additional objects
    """
    formated_additional = {
        'contacts' : {},
        'hosts' : {},
        'registrars' : {}
    }

    if additional :
        for item in additional :
            if isinstance(item, objects.Contact) :
                formater.filterDisclosed(item)
                formated_additional['contacts'][item.roid] = item
            elif isinstance(item, objects.Host) :
                formated_additional['hosts'][item.name] = item
            elif isinstance(item, objects.Registrar) :
                formated_additional['registrars'][item.roid] = item

    return formated_additional

def format_domain(domain):
    """
    helper function to format domain object for html output
    auto convert HostAttr and HostObj as one Array
    
    @param domain: domain object
    
    @return: formated domain object
    """
    domain.ns_converted = []
    for ns in domain.ns :
        if isinstance(ns, objects.DomainHostAttr) :
            ns_item = {
                'hostname' : ns.hostname,
                'ips' : []
            }

            for hostaddr in ns.hostAddr :
                ns_item['ips'].append(hostaddr.ip)
        else :
            ns_item = {
                'hostname' : ns.name,
                'ips' : [],
                'hostobj' : 1
            }
        domain.ns_converted.append(ns_item)

    return domain

def format(result):
    """
    function to format given Result object to HTML
    iterate over given Result object and preformat objects.
    render to HTML by jinja2
    
    @param result: Result object
    
    @return: Flask Response Object of converted Result object
    """
    domains = []
    contacts = []
    hosts = []
    registrars = []

    for item in result.items :
        if isinstance(item, objects.Domain) :
            domains.append(format_domain(item))
        elif isinstance(item, objects.Contact) :
            formater.filterDisclosed(item)
            contacts.append(item)
        elif isinstance(item, objects.Host) :
            hosts.append(item)
        elif isinstance(item, objects.Registrar) :
            registrars.append(item)
        else :
            raise formater.Error('Unknown object given: ' + str(item))

    formated_additional = __format_additionals(result.additional)
    out = render_template('view.html', domains = domains, contacts = contacts,
                                       hosts = hosts, registrars = registrars,
                                       additional = formated_additional)

    resp = flask.make_response(out, 200)
    resp.headers['Content-Type'] = 'text/html'
    return resp
