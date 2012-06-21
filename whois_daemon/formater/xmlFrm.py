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

import xml.dom.minidom, flask, codecs
from whois_daemon import objects, formater
from xml.dom.minidom import Document

class Frame(Document):
    """
    simple Frame for all RWS result objects
    """
    RWS_URN = 'urn:ietf:params:xml:ns:rws-1.0'
    encoding = 'UTF-8'
    result_node = None
    rws = None

    def __init__(self):
        """
        Constructor
        initialize base elements
        """
        Document.__init__(self)
        self.standalone = 'no'
        self.rws = self.createElementNS(self.RWS_URN, 'rws')
        self.rws.setAttribute('xmlns', self.RWS_URN)
        self.appendChild(self.rws)
        self.result_node = self.createElement('result')
        self.rws.appendChild(self.result_node)

    def toxml(self):
        """
        convert document to string
        
        @return: string of converted xml docoment
        """
        writer = xml.dom.minidom._get_StringIO()
        if self.encoding is not None:
            # Can't use codecs.getwriter to preserve 2.0 compatibility
            writer = codecs.lookup(self.encoding)[3](writer)

        self.writexml(writer, "", "", "", self.encoding)
        return writer.getvalue()

    def __str__(self):
        """
        convert to printable xml string (pretty format with indenting
        
        @return: converted string
        """
        return self.toprettyxml(encoding = self.encoding)

    def _addElement(self, name, node, vl = None):
        """
        create new element and add to existing node in document
        
        @param name: name of new element
        @param node: node to add Child to
        @param vl: value of new element
        
        @return: new created element
        """
        newelement = self.createElement(str(name))
        if vl is not None :
            txt = self.createTextNode(str(vl))
            newelement.appendChild(txt)
        node.appendChild(newelement)
        return newelement

def format_domain(d, domain, parent):
    """
    format object of type domain
    add additional domain:object node to given parent
    
    @param d: Frame object
    @param domain: Domain object
    @param parent: parent node in Frame object    
    """
    domainEl = d._addElement('domain:object', parent)
    domainEl.setAttribute('xmlns:domain', 'urn:ietf:params:xml:ns:rwsDomain-1.0')
    domainEl.setAttribute('href', '/domain/' + domain.name)
    d._addElement('domain:name', domainEl, domain.name)
    d._addElement('domain:roid', domainEl, domain.roid)

    for status in domain.status :
        statusEl = d._addElement('domain:status', domainEl)
        statusEl.setAttribute('s', status)

    registrantEl = d._addElement('domain:registrant', domainEl, domain.registrant.roid)
    registrantEl.setAttribute('href', '/contact/' + domain.registrant.roid)

    for contact in domain.contact :
        contactEl = d._addElement('domain:contact', domainEl, contact.roid)
        contactEl.setAttribute('href', '/contact/' + contact.roid)

    if domain.ns :
        nsEl = d._addElement('domain:ns', domainEl)
        for ns in domain.ns :
            if isinstance(ns, objects.DomainHostObj) :
                domainhostEl = d._addElement('domain:hostObj', nsEl, ns.name)
                domainhostEl.setAttribute('href', '/host/' + ns.name)
            else :
                hostAttrEl = d._addElement('domain:hostAttr', nsEl)
                d._addElement('domain:hostName', hostAttrEl, ns.hostname)
                for addr in ns.hostAddr :
                    hostAddrEl = d._addElement('domain:hostAddr', hostAttrEl, addr.ip)
                    hostAddrEl.setAttribute('ip', addr.type)

    for registrar in domain.registrar :
        registrarEl = d._addElement('domain:registrar', domainEl, registrar.roid)
        registrarEl.setAttribute('type', registrar.type)
        registrarEl.setAttribute('href', '/registrar/' + registrar.roid)

    if domain.crDate :
        d._addElement('domain:crDate', domainEl, domain.crDate)

    if domain.exDate :
        d._addElement('domain:exDate', domainEl, domain.exDate)

    if domain.upDate :
        d._addElement('domain:upDate', domainEl, domain.upDate)

    if domain.trDate :
        d._addElement('domain:trDate', domainEl, domain.trDate)

def format_contact(d, contact, parent):
    """
    format object of type contact
    add additional contact:object node to given parent
    
    @param d: Frame object
    @param contact: Contact object
    @param parent: parent node in Frame object    
    """
    formater.filterDisclosed(contact)
    contactEl = d._addElement('contact:object', parent)
    contactEl.setAttribute('xmlns:contact', 'urn:ietf:params:xml:ns:rwsContact-1.0')
    contactEl.setAttribute('href', '/domain/' + contact.roid)
    d._addElement('contact:id', contactEl, contact.roid)
    for status in contact.status :
        statusEl = d._addElement('contact:status', contactEl)
        statusEl.setAttribute('s', status)

    for postalInfo in contact.postalInfo :
        postalInfoEl = d._addElement('contact:postalInfo', contactEl)
        postalInfoEl.setAttribute('type', postalInfo.type)
        if 'name' not in postalInfo.disclose and postalInfo.name :
            d._addElement('contact:name', postalInfoEl, postalInfo.name)

        if 'org' not in postalInfo.disclose and postalInfo.org :
            d._addElement('contact:org', postalInfoEl, postalInfo.org)

        if 'addr' not in postalInfo.disclose :
            addrEl = d._addElement('contact:addr', postalInfoEl)
            if 'street' not in postalInfo.disclose :
                for street in postalInfo.addr.street :
                    d._addElement('contact:street', addrEl, street)

            if 'city' not in postalInfo.disclose :
                d._addElement('contact:city', addrEl, postalInfo.addr.city)

            if 'sp' not in postalInfo.disclose :
                d._addElement('contact:sp', addrEl, postalInfo.addr.sp)

            if 'pc' not in postalInfo.disclose :
                d._addElement('contact:pc', addrEl, postalInfo.addr.pc)

            if 'cc' not in postalInfo.disclose :
                d._addElement('contact:cc', addrEl, postalInfo.addr.cc)

            if not addrEl.hasChildNodes() :
                addrEl.unlink()

    if not postalInfoEl.hasChildNodes() :
        postalInfoEl.unlink()

    if 'voice' not in contact.disclose and contact.voice :
        voiceEl = d._addElement('contact:voice', contactEl, contact.voice.number)
        if contact.voice.extension:
            voiceEl.setAttribute('x', contact.voice.extension)

    if 'fax' not in contact.disclose and contact.fax :
        faxEl = d._addElement('contact:fax', contactEl, contact.fax.number)
        if contact.fax.extension:
            faxEl.setAttribute('x', contact.fax.extension)

    if 'email' not in contact.disclose and contact.email :
        d._addElement('contact:email', contactEl, contact.email)

    for registrar in contact.registrar :
        registrarEl = d._addElement('contact:registrar', contactEl, registrar.roid)
        registrarEl.setAttribute('type', registrar.type)
        registrarEl.setAttribute('href', '/registrar/' + registrar.roid)

    if contact.crDate :
        d._addElement('contact:crDate', contactEl, contact.crDate)

    if contact.upDate :
        d._addElement('contact:upDate', contactEl, contact.upDate)

    if contact.trDate :
        d._addElement('contact:trDate', contactEl, contact.trDate)

def format_host(d, host, parent):
    """
    format object of type host
    add additional host:object node to given parent
    
    @param d: Frame object
    @param host: Host object
    @param parent: parent node in Frame object    
    """
    hostEl = d._addElement('host:object', parent)
    hostEl.setAttribute('xmlns:host', 'urn:ietf:params:xml:ns:rwsHost-1.0')
    hostEl.setAttribute('href', '/host/' + host.name)
    d._addElement('host:name', hostEl, host.name)
    for status in host.status :
        statusEl = d._addElement('host:status', hostEl)
        statusEl.setAttribute('s', status)

    for addr in host.addr :
        hostAddrEl = d._addElement('host:addr', hostEl, addr.ip)
        hostAddrEl.setAttribute('ip', addr.type)

    for registrar in host.registrar :
        registrarEl = d._addElement('host:registrar', hostEl, registrar.roid)
        registrarEl.setAttribute('type', registrar.type)
        registrarEl.setAttribute('href', '/registrar/' + registrar.roid)

    if host.crDate :
        d._addElement('host:crDate', hostEl, host.crDate)

    if host.upDate :
        d._addElement('host:upDate', hostEl, host.upDate)

    if host.trDate :
        d._addElement('host:trDate', hostEl, host.trDate)

def format_registrar(d, registrar, parent):
    """
    format object of type Registrar
    add additional registrar:object node to given parent
    
    @param d: Frame object
    @param registrar: Registrar object
    @param parent: parent node in Frame object    
    """
    registrarEl = d._addElement('registrar:object', parent)
    registrarEl.setAttribute('xmlns:registrar', 'urn:ietf:params:xml:ns:rwsRegistrar-1.0')
    registrarEl.setAttribute('href', '/registrar/' + registrar.roid)
    d._addElement('registrar:id', registrarEl, registrar.roid)
    d._addElement('registrar:name', registrarEl, registrar.name)

def format_items(result):
    """
    calls format_<type> function by object instance in result.items / result.additional
    
    @param result: Result object
    
    @return: created Frame object
    """
    d = Frame()

    for item in result.items :
        if isinstance(item, objects.Domain) :
            format_domain(d, item, d.result_node)
        if isinstance(item, objects.Contact) :
            format_contact(d, item, d.result_node)
        elif isinstance(item, objects.Host) :
            format_host(d, item, d.result_node)
        elif isinstance(item, objects.Registrar) :
            format_registrar(d, item, d.result_node)
        else :
            raise formater.Error('Unknown object given: ' + str(item))

    if result.additional :
        additionalEl = d._addElement('additional', d.rws)
        for item in result.additional :
            if isinstance(item, objects.Contact) :
                format_contact(d, item, additionalEl)
            elif isinstance(item, objects.Host) :
                format_host(d, item, additionalEl)
            elif isinstance(item, objects.Registrar) :
                format_registrar(d, item, additionalEl)
            else :
                raise formater.Error('Unknown object given: ' + str(item))

    return d

def format(result):
    """
    format given result object in requested format

    @param result: Result Object
    
    @return: Flask Response Object of converted Result object
    """
    d = format_items(result)
    res = flask.make_response(d.toxml(), 200)
    res.headers['Content-Type'] = 'application/xml'
    return res
