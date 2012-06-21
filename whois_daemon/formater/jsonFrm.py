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

import json, flask
from whois_daemon import objects, formater

def format_domain(domain):
    """
    format object of type domain
    add type as '!type' key and filters all internal id data  
    
    @param domain: Domain object to format
    
    @return: formated domain as dict
    """
    x = objects.objref.todict(domain)
    x['!type'] = 'Domain'
    if x['registrant'] :
        x['registrant'] = x['registrant']['roid']

    formater.filterROID(x)
    return x

def format_contact(contact):
    """
    format object of type contact
    add type as '!type' key and filters all internal id data  
    
    @param contact: Contact object to format
    
    @return: formated contact as dict
    """
    formater.filterDisclosed(contact)
    x = objects.objref.todict(contact)
    x['!type'] = 'Contact'
    formater.filterROID(x)
    return x

def format_host(host):
    """
    format object of type host
    add type as '!type' key and filters all internal id data  
    
    @param host: Host object to format
    
    @return: formated host as dict
    """
    x = objects.objref.todict(host)
    x['!type'] = 'Host'
    del x['id']
    formater.filterROID(x)
    return x

def format_registrar(registrar):
    """
    format object of type registrar    
    add type as '!type' key and filters all internal id data  
    
    @param registrar: Registrar object to format
    
    @return: formated registrar as dict
    """
    x = objects.objref.todict(registrar)
    x['!type'] = 'Registrar'
    formater.filterROID(x)
    return x

def format_items(result):
    """
    calls format_<type> function by object instance in result.items / result.additional
    
    @param result: Result object
    
    @return: formated dict
    """
    output = {
        'rws' : {
            'result' : []
        }
    }

    # reformat result items
    for item in result.items :
        if isinstance(item, objects.Domain) :
            output['rws']['result'].append(format_domain(item))
        elif isinstance(item, objects.Contact) :
            output['rws']['result'].append(format_contact(item))
        elif isinstance(item, objects.Host) :
            output['rws']['result'].append(format_host(item))
        elif isinstance(item, objects.Registrar) :
            output['rws']['result'].append(format_registrar(item))
        else :
            raise formater.Error('Unknown object given: ' + str(item))


    # reformat additional linked items
    if result.additional :
        output['rws']['additional'] = []
        for item in result.additional :
            if isinstance(item, objects.Domain) :
                output['rws']['additional'].append(format_domain(item))
            elif isinstance(item, objects.Contact) :
                output['rws']['additional'].append(format_contact(item))
            elif isinstance(item, objects.Host) :
                output['rws']['additional'].append(format_host(item))
            elif isinstance(item, objects.Registrar) :
                output['rws']['additional'].append(format_registrar(item))
            else :
                raise formater.Error('Unknown object given: ' + str(item))

    return output

def format(result):
    """
    format given result object in requested format
    
    @param result: Result Object
    
    @return: Flask Response Object of converted Result object
    """
    output = format_items(result)
    resp = flask.make_response(json.dumps(output), 200)
    resp.headers['Content-Type'] = 'text/plain'
    return resp
