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

from whois_daemon import objects, formater
import flask

spacer_len = 25
LF = "\n"

def header():
    """
    return some kind of header - legal stuff for example
    
    @return: string
    """
    return "# Some kind of legal stuff" + LF + LF

def format_domain(domain, additional):
    """
    format domain object
    
    @param domain: domain object
    @param additinal: array of additional objects
    
    @return: formated string  
    """
    out = ''
    out += 'Domain:'.ljust(spacer_len) + domain.name + LF
    out += 'Name IDN:'.ljust(spacer_len) + domain.name_idn + LF
    out += LF
    if domain.status :
        for status in domain.status :
            out += 'Status:'.ljust(spacer_len) + status + LF
    else :
        out += 'Status:'.ljust(spacer_len) + 'OK' + LF

    if domain.crDate :
        out += 'Created:'.ljust(spacer_len) + domain.crDate + LF
    if domain.upDate :
        out += 'Last Update:'.ljust(spacer_len) + domain.upDate + LF
    if domain.exDate :
        out += 'Expiration Date:'.ljust(spacer_len) + domain.exDate + LF

    if domain.ns :
        for ns in domain.ns :
            if isinstance(ns, objects.DomainHostAttr) :
                out += 'Name Server:'.ljust(spacer_len)
                if ns.hostAddr :
                    ips = []
                    for hostaddr in ns.hostAddr :
                        ips.append(hostaddr.ip)
                    out += ns.hostname.ljust(spacer_len) + (' '.join(ips))
                else :
                    out += ns.hostname
                out += LF
            else :
                out += 'Name Server:'.ljust(spacer_len) + ns.name + LF
    else :
        out += 'Name Server:'.ljust(spacer_len) + 'No nameserver' + LF


    if domain.registrant :
        out += 'Registrant:'.ljust(spacer_len) + domain.registrant.roid + LF

    for contact in domain.contact :
        label = contact.type[0:1].upper() + contact.type[1:] + ' Contact:'
        out += label.ljust(spacer_len) + contact.roid + LF

    for registrar in domain.registrar :
        label = registrar.type[0:1].upper() + registrar.type[1:] + ' Registrar:'
        out += label.ljust(spacer_len) + registrar.roid + LF
    return out

def format_contact(contact, additional):
    """
    format contact object
    
    @param contact: contact object
    @param additinal: array of additional objects
    
    @return: formated string  
    """
    out = ''
    out += 'Contact:'.ljust(spacer_len) + contact.roid + LF
    for post in contact.postalInfo:
        if post.type == 'int':
            if post.name :
                out += 'Name:'.ljust(spacer_len) + post.name + LF
            if post.org :
                out += 'Organization:'.ljust(spacer_len) + post.org + LF
            if post.addr :
                for street in post.addr.street :
                    out += 'Address:'.ljust(spacer_len) + street + LF
                out += 'Address:'.ljust(spacer_len) + post.addr.city
                if post.addr.sp :
                    out += ' ' + post.addr.sp
                out += ' ' + post.addr.pc + LF
                out += 'Address:'.ljust(spacer_len) + post.addr.cc + LF

    if contact.voice :
        out += 'Voice:'.ljust(spacer_len) + contact.voice.number
        if contact.voice.extension :
            out += 'x' + contact.voice.extension
        out += LF

    if contact.fax :
        out += 'Fax:'.ljust(spacer_len) + contact.fax.number
        if contact.fax.extension :
            out += 'x' + contact.fax.extension
        out += LF

    if contact.email :
        out += 'Fax:'.ljust(spacer_len) + contact.email + LF

    if contact.status :
        for status in contact.status :
            out += 'Status:'.ljust(spacer_len) + status + LF
    else :
        out += 'Status:'.ljust(spacer_len) + 'OK' + LF

    if contact.crDate :
        out += 'Created:'.ljust(spacer_len) + contact.crDate + LF
    if contact.upDate :
        out += 'Last Update:'.ljust(spacer_len) + contact.upDate + LF

    for registrar in contact.registrar :
        label = registrar.type[0:1].upper() + registrar.type[1:] + ' Registrar:'
        out += label.ljust(spacer_len) + registrar.roid + LF
    return out

def format_host(host, additional):
    """
    format host object
    
    @param host: host object
    @param additinal: array of additional objects
    
    @return: formated string  
    """
    out = ''
    out += 'Hostname:'.ljust(spacer_len) + host.name + LF
    if host.addr :
        for addr in host.addr :
            ip_str = 'IP ' + addr.type + ':'
            out += ip_str.ljust(spacer_len) + addr.ip + LF

    if host.status :
        for status in host.status :
            out += 'Status:'.ljust(spacer_len) + status + LF
    else :
        out += 'Status:'.ljust(spacer_len) + 'OK' + LF

    if host.crDate :
        out += 'Created:'.ljust(spacer_len) + host.crDate + LF
    if host.upDate :
        out += 'Last Update:'.ljust(spacer_len) + host.upDate + LF

    for registrar in host.registrar :
        label = registrar.type[0:1].upper() + registrar.type[1:] + ' Registrar:'
        out += label.ljust(spacer_len) + registrar.roid + LF
    return out

def format_registrar(registrar, additional):
    """
    format registrar object
    
    @param registrar: registrar object
    @param additinal: array of additional objects
    
    @return: formated string  
    """
    out = ''
    out += 'Registrar Name:'.ljust(spacer_len) + registrar.name + LF
    if registrar.href :
        out += 'URL:'.ljust(spacer_len) + registrar.href + LF
    return out

def format(result):
    """
    function to format given Result object to HTML
    iterate over given Result object and format objects.
    
    @param result: Result object
    
    @return: Flask Response Object of converted Result object
    """
    out = header()
    for item in result.items :
        if isinstance(item, objects.Domain) :
            out += format_domain(item, result.additional)
        elif isinstance(item, objects.Contact) :
            formater.filterDisclosed(item)
            out += format_contact(item, result.additional)
        elif isinstance(item, objects.Host) :
            out += format_host(item, result.additional)
        elif isinstance(item, objects.Registrar) :
            out += format_registrar(item, result.additional)
        else :
            raise formater.Error('Unknown object given: ' + str(item))
        out += LF

    out += LF

    for item in result.additional :
        if isinstance(item, objects.Domain) :
            out += format_domain(item, result.additional)
        elif isinstance(item, objects.Contact) :
            formater.filterDisclosed(item)
            out += format_contact(item, result.additional)
        elif isinstance(item, objects.Host) :
            out += format_host(item, result.additional)
        elif isinstance(item, objects.Registrar) :
            out += format_registrar(item, result.additional)
        else :
            raise formater.Error('Unknown object given: ' + str(item))
        out += LF

    resp = flask.make_response(out, 200)
    resp.headers['Content-Type'] = 'text/plain'
    return resp
