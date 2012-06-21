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

import oursql
from whois_daemon import objects

class Error(Exception) :
    """
    global mysql exception class
    """
    def __init__(self, e):
        self.what = e[1]
        self.code = e[0]

    def __str__(self):
        return str(self.code) + ': ' + self.what

class InvalidFilter(Error):
    """
    exception thrown if an invalid filter given
    """
    def __init__(self):
        self.what = 'Invalid filter given'

class cl(object):
    """
    class to communicate with backend service directly
    abstraction of oursql
    """

    config = None

    def __init__(self, cf):
        """
        Constructor.
        load config and try to connect to database
        
        @param cf: client config
        """
        self.config = cf
        self.__connect()

    def __connect(self):
        """
        connect to database
        """
        try :
            self.conn = oursql.connect(host = self.config['host'],
                                user = self.config['user'],
                                passwd = self.config['password'],
                                db = self.config['db'],
                                port = self.config['port'],
                                use_unicode = False,
                                autoping = True,
                                autoreconnect = True,
                                default_cursor = oursql.DictCursor,
                                charset = 'utf8',
                                init_command = 'SET NAMES utf8')
        except oursql.Error, e:
            raise Error(e.args)

    def __call__(self, sqlstr, argv = (), fetch = 1) :
        """
        start a SQL call and return as dict or cursor

        fetch = 0: return only last inserted id
        fetch = 1: return one row as dict
        fetch > 1 || fetch < 0: return cursor
        
        @param sqlstr: SQL Query as String
        @param argv: Array of Arguments to Replace+Escape in SQL Query
        @param fetch: fetch option
        
        @return: requested format
        """
        if not isinstance(argv, tuple) and not isinstance(argv, list):
            # Auto convert argv if no tuple
            argv = (argv,)

        # try to get cursor of backend and execute query with given parameters
        try :
            cursor = self.conn.cursor()
            cursor.execute(sqlstr, argv)

        except oursql.Error, e:
            cursor.close()
            raise Error(e.args)

        result = cursor

        if (fetch == 0) :
            result = cursor.lastrowid
        elif (fetch == 1) :
            result = cursor.fetchone()

        if fetch == 0 or fetch == 1 :
            cursor.close()

        return result

class queryHandler(object):
    """
    class to abstract all SQL calls and return results as objects
    """
    dbh = None
    cache = {
        'status' : {},
        'domain_contact_type' : {},
        'contact_postalInfo_type' : {
            1 : 'int',
            2 : 'loc'
        }
    }

    def __init__(self, dbh):
        """
        Constructor:
        set database handler and load cache
        
        @param dbh: database handler instance (cl)
        """
        self.dbh = dbh
        self.__loadCache()

    def __loadCache(self):
        """
        fill local cache with static values like available status and contact_types
        """
        for row in self.dbh('SELECT id, name FROM status', (), -1).fetchall() :
            self.cache['status'][row['id']] = row['name']

        for row in self.dbh('SELECT id, name FROM domain_contact_type', (), -1).fetchall() :
            self.cache['domain_contact_type'][row['id']] = row['name']

    def get_registrar(self, filter):
        """
        Get Registrar object by given filter options
        
        @param filter: by id (internal database id), ROID (public id) or name
        
        @return: None or Registrar Object
        """
        sql_param = ()
        sql = """SELECT id, roid, name, href FROM registrar WHERE """

        if filter.has_key('registrar_id') and filter['registrar_id'] :
            sql += """ id = ? """
            sql_param = (filter['registrar_id'])
        elif filter.has_key('roid') and filter['roid'] :
            sql += """ roid = ? """
            sql_param = (filter['roid'])
        elif filter.has_key('name') and filter['name'] :
            sql += """ name = ? """
            sql_param = (filter['name'])
        else :
            raise InvalidFilter()

        row = self.dbh(sql, sql_param, 1)

        if not row: return None
        return objects.Registrar(row)

    def get_hosts_by_ip(self, filter):
        """
        get host objects by given IP
        
        @param filter: by ip + type
        
        @return: Array of Host Objects 
        """
        sql = """
            SELECT
                host_ip.host_id
            FROM
                host_ip
            WHERE
        """

        if filter.has_key('ip') and filter['ip'] :
            sql += """ host_ip.ip = ? """
            sql_param = (filter['ip'])
            if filter.has_key('type') and filter['type'] :
                sql += """ AND host_ip.type = ? """
                sql_param = (filter['ip'], filter['type'])
        else :
            raise InvalidFilter()

        sql += 'GROUP BY host_ip.host_id'

        result = []
        for row in self.dbh(sql, sql_param, -1).fetchall() :
            result.append(self.get_host({'host_id' : row['host_id']}))

        return result

    def get_host(self, filter):
        """
        get host object by given filter options
        
        @param filter: by id (internal database id) or hostname
        
        @return: Host Object
        """
        sql = """
            SELECT
                host.id,
                host.name,
                host.crID,
                registrar_cr.roid crROID,
                host.clID,
                registrar_cl.roid clROID,
                host.upID,
                registrar_up.roid upROID,
                host.crDate,
                host.upDate,
                host.trDate,
                GROUP_CONCAT(host_ip.ip) host_ips,
                GROUP_CONCAT(host_ip.type) host_ip_types,
                GROUP_CONCAT(DISTINCT host_status.status_id) status_ids
            FROM
                host
                LEFT JOIN host_ip ON (host.id = host_ip.host_id)
                LEFT JOIN host_status ON (host.id = host_status.host_id)
                LEFT JOIN registrar registrar_cr ON (host.crID = registrar_cr.id) 
                LEFT JOIN registrar registrar_cl ON (host.clID = registrar_cl.id) 
                LEFT JOIN registrar registrar_up ON (host.upID = registrar_up.id) 
            WHERE
        """

        if filter.has_key('host_id') and filter['host_id'] :
            sql += """ host.id = ? """
            sql_param = (filter['host_id'])
        elif filter.has_key('name') and filter['name'] :
            sql += """ host.name like ? """
            sql_param = (filter['name'])
        else :
            raise InvalidFilter()

        sql += 'GROUP BY host.id'

        row = self.dbh(sql, sql_param, 1)
        if not row: return None

        host = objects.Host(
            id = row['id'],
            name = row['name'],
            crDate = row['crDate'],
            upDate = row['upDate'],
            trDate = row['trDate']
        )

        # split joined status ids in status_ids field
        host.status = []
        if row['status_ids'] :
            for status_id in row['status_ids'].split(','):
                host.status.append(self.cache['status'][long(status_id)])

        # add linked registrars
        host.registrar = []
        if row['crID'] :
            host.registrar.append(
                objects.DomainLinkedObj(
                    id = row['crID'],
                    type = 'created',
                    roid = row['crROID']
                )
            )

        if row['upID'] :
            host.registrar.append(
                objects.DomainLinkedObj(
                    id = row['upID'],
                    type = 'updated',
                    roid = row['upROID']
                )
            )

        if row['clID'] :
            host.registrar.append(
                objects.DomainLinkedObj(
                    id = row['clID'],
                    type = 'sponsor',
                    roid = row['clROID']
                )
            )

        # add linked ips as HostAddr Object
        if row['host_ips'] :
            host.addr = []
            host_ip_types = row['host_ip_types'].split(',')
            x = 0
            for ip in row['host_ips'].split(',') :
                host.addr.append(
                    objects.HostAddr(
                        ip = ip,
                        type = 'v' + str(host_ip_types[x])
                    )
                )
                x += 1

        return host

    def get_contact(self, filter):
        """
        get contact object by given filter options
        
        @param filter: by id (internal database id) or roid (public id)
        
        @return: Contact Object
        """
        sql = """
            SELECT
                contact.id,
                contact.roid,
                contact.email,
                contact.voice,
                contact.voice_x,
                contact.fax,
                contact.fax_x,
                contact.crID,
                registrar_cr.roid crROID,
                contact.clID,
                registrar_cl.roid clROID,
                contact.upID,
                registrar_up.roid upROID,
                contact.crDate,
                contact.upDate,
                contact.trDate,
                contact_postalinfo.name,
                contact_postalinfo.org,
                contact_postalinfo.addr1,
                contact_postalinfo.addr2,
                contact_postalinfo.addr3,
                contact_postalinfo.city,
                contact_postalinfo.sp,
                contact_postalinfo.pc,
                contact_postalinfo.cc,
                contact_postalinfo.type,
                GROUP_CONCAT(DISTINCT contact_status.status_id) status_ids,
                GROUP_CONCAT(DISTINCT CONCAT(contact_disclose.field, ';', contact_disclose.type)) disclose
            FROM
                contact
                LEFT JOIN contact_postalinfo ON (contact.id = contact_postalinfo.contact_id)
                LEFT JOIN contact_status ON (contact.id = contact_status.contact_id)
                LEFT JOIN contact_disclose ON (contact.id = contact_disclose.contact_id AND contact_disclose.flag = 1)
                LEFT JOIN registrar registrar_cr ON (contact.crID = registrar_cr.id) 
                LEFT JOIN registrar registrar_cl ON (contact.clID = registrar_cl.id) 
                LEFT JOIN registrar registrar_up ON (contact.upID = registrar_up.id) 
            WHERE
        """

        if filter.has_key('contact_id') and filter['contact_id'] :
            sql += """ contact.id = ? """
            sql_param = (filter['contact_id'])
        elif filter.has_key('roid') and filter['roid'] :
            sql += """ contact.roid = ? """
            sql_param = (filter['roid'])
        else :
            raise InvalidFilter()

        sql += ' GROUP BY contact.id, contact_postalinfo.type'

        x = 0
        contact = None
        rows = self.dbh(sql, sql_param, -1).fetchall()

        postalInfoDisclose = {
            1 : None,
            2 : None
        }

        for row in rows :
            # check if there is any result (contact found?)
            if not row['id'] :
                break

            # only use first result row for building initial contact object
            if x < 1 :
                contact = objects.Contact(
                    id = row['id'],
                    roid = row['roid'],
                    email = row['email'],
                    crDate = row['crDate'],
                    upDate = row['upDate'],
                    trDate = row['trDate'],
                    postalInfo = [],
                    voice = objects.Phone(number = row['voice'], extension = row['voice_x']),
                    fax = objects.Phone(number = row['fax'], extension = row['fax_x'])
                )

                # disclose field has both disclose infos - for contact itself and postalInfo object
                if row['disclose'] :
                    """so, split disclose by ','"""
                    for item in row['disclose'].split(',') :
                        """and disclose type (int or loc) by ';'"""
                        (disclose_field_name, disclose_postInfo_type) = item.split(';')
                        disclose_postInfo_type = int(disclose_postInfo_type)

                        # only add disclose fields to main contact if type is 0
                        if disclose_postInfo_type == 0:
                            if disclose_field_name not in contact.disclose :
                                if not contact.disclose :
                                    contact.disclose = []
                                contact.disclose.append(disclose_field_name)
                        else :
                            if not postalInfoDisclose[disclose_postInfo_type] :
                                postalInfoDisclose[disclose_postInfo_type] = []
                            postalInfoDisclose[disclose_postInfo_type].append(disclose_field_name)

                # split joined status IDs in status_ids field
                contact.status = []
                if row['status_ids'] :
                    for status_id in row['status_ids'].split(','):
                        contact.status.append(self.cache['status'][long(status_id)])

                # add linked registrars
                contact.registrar = []
                if row['crID'] :
                    contact.registrar.append(
                        objects.DomainLinkedObj(
                            id = row['crID'],
                            type = 'created',
                            roid = row['crROID']
                        )
                    )

                if row['upID'] :
                    contact.registrar.append(
                        objects.DomainLinkedObj(
                            id = row['upID'],
                            type = 'updated',
                            roid = row['upROID']
                        )
                    )

                if row['clID'] :
                    contact.registrar.append(
                        objects.DomainLinkedObj(
                            id = row['clID'],
                            type = 'sponsor',
                            roid = row['clROID']
                        )
                    )

            # and finally generate postalInfo objects
            street = []
            street.append(row['addr1'])
            if row['addr2'] :
                street.append(row['addr2'])

            if row['addr3'] :
                street.append(row['addr3'])

            contact.postalInfo.append(objects.PostalInfo(
                name = row['name'],
                org = row['org'],
                addr = objects.Address(
                    street = street,
                    city = row['city'],
                    sp = row['sp'],
                    pc = row['pc'],
                    cc = row['cc']
                ),
                type = self.cache['contact_postalInfo_type'][row['type']],
                disclose = postalInfoDisclose[int(row['type'])]
            ))
            x += 1

        return contact

    def __get_domain_nameserver(self, filter):
        """
        helper function to get linked Nameserver by given filter options
        
        @param filter: by domain_id (internal database id)
        
        @return: Array of Nameservers as dict 
        """
        sql = """
            SELECT
                domain_ns.id,
                domain_ns.hostname,
                domain_ns.host_id,
                GROUP_CONCAT(domain_ns_ip.ip) ns_ips,
                GROUP_CONCAT(domain_ns_ip.type) ns_types,
                host.name
            FROM
                domain_ns
                LEFT JOIN domain_ns_ip ON (domain_ns.id = domain_ns_ip.domain_ns_id)
                LEFT JOIN host ON (domain_ns.host_id = host.id)
            WHERE
        """

        if filter.has_key('domain_id') and filter['domain_id'] :
            sql += """ domain_ns.domain_id = ? """
            sql_param = (filter['domain_id'])
        else :
            raise InvalidFilter()

        sql += 'GROUP BY domain_ns.id'

        rows = self.dbh(sql, sql_param, -1)
        return rows.fetchall()

    def __get_domain_contacts(self, filter):
        """
        helper function to get linked contacts by given filter options
        
        @param filter: by domain_id (internal database id) and type (contact_type_id)
        
        @return: Array of Contacts as dict
        """
        sql = """
            SELECT
                domain_contact.domain_contact_type_id,
                domain_contact.contact_id,
                contact.roid
            FROM
                domain_contact
                LEFT JOIN contact ON (domain_contact.contact_id = contact.id) 
            WHERE
        """

        if filter.has_key('type') and filter['type'] :
            sql += """ domain_contact.domain_contact_type_id = ? AND """
            sql_param = (filter['type'])

        if filter.has_key('domain_id') and filter['domain_id'] :
            sql += """ domain_contact.domain_id = ? """
            sql_param = (filter['domain_id'])
        else :
            raise InvalidFilter()

        rows = self.dbh(sql, sql_param, -1)
        return rows.fetchall()

    def get_domain_hosts(self, filter):
        """
        get connected host objects by given filter options
        
        @param filter: by domain_id (internal database id) or domain name
        
        @return: Array of Hosts as dict
        """
        sql = """
            SELECT
                domain_host.host_id
            FROM
                domain_host
        """

        if filter.has_key('domain_id') and filter['domain_id'] :
            sql += """WHERE domain_host.domain_id = ? """
            sql_param = (filter['domain_id'])
        elif filter.has_key('domain_name') and filter['domain_name'] :
            sql += """, domain WHERE domain_host.domain_id = domain.id AND domain.name LIKE ? """
            sql_param = (filter['domain_name'])
        else :
            raise InvalidFilter()

        rows = self.dbh(sql, sql_param, -1)

        result = []
        for row in rows.fetchall() :
            result.append(
                self.get_host({
                    'host_id' : row['host_id']
                })
            )
        return result

    def get_domain(self, filter):
        """
        get full domain object + additional by given filter options
        
        @param filter: by domain_id (internal database id), roid (public id) or domain name
        
        @return: Domain Object
        """
        sql = """
            SELECT
                domain.id,
                domain.roid,
                domain.name,
                domain.registrant_contact_id,
                domain.crID,
                registrar_cr.roid crROID,
                domain.clID,
                registrar_cl.roid clROID,
                domain.upID,
                registrar_up.roid upROID,
                domain.crDate,
                domain.upDate,
                domain.exDate,
                domain.trDate,
                GROUP_CONCAT(DISTINCT domain_status.status_id) as status_ids,
                contact.roid registrant_roid
            FROM
                domain
                LEFT JOIN domain_status ON (domain.id = domain_status.domain_id)
                LEFT JOIN contact ON (domain.registrant_contact_id = contact.id)
                LEFT JOIN registrar registrar_cr ON (domain.crID = registrar_cr.id) 
                LEFT JOIN registrar registrar_cl ON (domain.clID = registrar_cl.id) 
                LEFT JOIN registrar registrar_up ON (domain.upID = registrar_up.id) 
            WHERE
        """

        if filter.has_key('name') and filter['name'] :
            sql += """ domain.name LIKE ? """
            sql_param = (filter['name'])
        elif filter.has_key('domain_id') and filter['domain_id'] :
            sql += """ domain.id = ? """
            sql_param = (filter['domain_id'])
        elif filter.has_key('roid') and filter['roid'] :
            sql += """ domain.roid = ? """
            sql_param = (filter['roid'])
        else :
            raise InvalidFilter()

        sql += ' GROUP BY domain.id'

        row = self.dbh(sql, sql_param, 1)
        if not row: return None

        domain = objects.Domain(
            id = row['id'],
            roid = row['roid'],
            name = row['name'],
            registrant = objects.DomainLinkedObj(
                id = row['registrant_contact_id'],
                roid = row['registrant_roid']
            ),
            crDate = row['crDate'],
            upDate = row['upDate'],
            trDate = row['trDate'],
            exDate = row['exDate']
        )

        """split joined status ids in status_ids field"""
        domain.status = []
        if row['status_ids'] :
            for status_id in row['status_ids'].split(','):
                domain.status.append(self.cache['status'][long(status_id)])

        """add linked registrars"""
        domain.registrar = []
        if row['crID'] :
            domain.registrar.append(
                objects.DomainLinkedObj(
                    id = row['crID'],
                    type = 'created',
                    roid = row['crROID']
                )
            )

        if row['upID'] :
            domain.registrar.append(
                objects.DomainLinkedObj(
                    id = row['upID'],
                    type = 'updated',
                    roid = row['upROID']
                )
            )

        if row['clID'] :
            domain.registrar.append(
                objects.DomainLinkedObj(
                    id = row['clID'],
                    type = 'sponsor',
                    roid = row['clROID']
                )
            )


        """add linked contacts"""
        domain.contact = []
        for contact in self.__get_domain_contacts({ 'domain_id' : domain.id }):
            domain.contact.append(
                objects.DomainLinkedObj(
                    id = contact['contact_id'],
                    type = self.cache['domain_contact_type'][contact['domain_contact_type_id']],
                    roid = contact['roid']
                )
            )

        """
        add linked nameservers
        
        if linked nameserver is a host object - add directly its hostname
        if linked nameserver is a hostAttr - add hostname + ips
        """
        domain.ns = []
        for ns in self.__get_domain_nameserver({'domain_id' : domain.id }):
            if ns['hostname'] :
                hostattr = objects.DomainHostAttr(
                    hostname = ns['hostname']
                )
                if ns['ns_ips'] :
                    hostattr.hostAddr = []
                    ns_types = ns['ns_types'].split(',')
                    x = 0
                    for ip in ns['ns_ips'].split(',') :
                        hostattr.hostAddr.append(
                            objects.HostAddr(
                                ip = ip,
                                type = 'v' + str(ns_types[x])
                            )
                        )
                        x += 1

                domain.ns.append(hostattr)
            else :
                domain.ns.append(objects.DomainHostObj(
                    id = ns['id'],
                    name = ns['name']
                ))

        return domain

def init(config):
    """
    Initialize backend module
    Loads database handler
    
    @param config: config to load 
    
    @return: instance of queryHandlers
    """
    dbh = cl(config)
    return queryHandler(dbh)
