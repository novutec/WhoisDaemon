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

import datetime

class objref(object):
    """
    abstract base class for all used objected
    
    automatically formats datetime objects to result format.
    """
    def __init__(self, *args, **kwargs):
        """
        set instance __dict__ object by class attributes as template
        
        dict object or directly names as arguments possible
        """
        self.update(self.__class__.__dict__)
        data = {}
        if isinstance(args, tuple) and len(args) > 0 and isinstance(args[0], dict) :
            data = args[0]
        else :
            data = kwargs

        self.update(data)

    @staticmethod
    def format_DateTime_str(dateObj):
        """
        static method to format datetime objects to standard result format (ex. 2012-01-01T00:00:00Z)
        
        @param dateObj: datetime object to format to string
        
        @return: formated datetime string
        """
        return dateObj.strftime('%Y-%m-%dT%H:%M:%SZ')

    def __setattr__(self, ky, vl):
        """
        overloaded __setattr__ to remove unused __doc__ and __module__ objects
        calls format_DateTime_str to convert datetime objects automatically
        
        @param ky: named key
        @param vl: named value
        """
        if ky not in ('__doc__', '__module__') :
            if isinstance(vl, datetime.datetime) :
                vl = objref.format_DateTime_str(vl)
            self.__dict__[ky] = vl

    @staticmethod
    def todict(obj, classkey = None):
        """
        return recursive converted object as dict
        
        @param obj: object to convert to dict
        @param classkey: in recursion, need to convert subelements
        
        @return: converted dict   
        """
        if isinstance(obj, dict):
            for (k, v) in obj.iteritems():
                obj[k] = objref.todict(v, classkey)
            return obj
        elif hasattr(obj, "__iter__"):
            return [objref.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, objref.todict(value, classkey))
                for key, value in obj.__dict__.iteritems()
                if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj

    def update(self, data) :
        """
        iterates over given dict to update local values
        
        @param data: dict to use for update 
        """
        for (ky, vl) in data.iteritems() :
            self.__setattr__(ky, vl)

class DomainLinkedObj(objref) :
    """
    Object to link two object
    """
    id = 0
    type = ''
    roid = ''

class HostAddr(objref):
    """
    Object to hold ip + type (v4/v6) informations of a host or hostAttr
    """
    ip = ''
    type = 'v4'

class DomainHostAttr(objref) :
    """
    Object to hold hostname + ip informations for nameserver without host object
    """
    hostname = ''
    hostAddr = []

class DomainHostObj(objref) :
    """
    Object to link domain nameserver to host object
    """
    id = 0
    name = ''

class Domain(objref):
    """
    Object with all subinformations of a domain
    """
    id = 0
    roid = None
    name = ''
    name_idn = ''
    status = []
    registrant = ''
    contact = []
    ns = []
    registrar = []
    crDate = ''
    upDate = None
    trDate = None
    exDate = ''

class Address(objref):
    """
    Object with all address informations for a PostalInfo object
    """
    street = []
    city = ''
    sp = ''
    pc = ''
    cc = ''

class PostalInfo(objref):
    """
    Object to hold all informations for public PostalInfo
    
    disclose list in this object only disclose fields used in this object
    """
    name = ''
    org = None
    addr = Address()
    type = None
    disclose = []

class Phone(objref):
    """
    Object to hold phone number + extension
    """
    number = None
    extension = None

class Contact(objref):
    """
    Object to hold contact informations including list of postalInfo

    disclose list in this object only disclose fields used in this object
    """
    id = 0
    roid = None
    status = []
    postalInfo = []
    voice = Phone()
    fax = Phone()
    email = ''
    registrar = []
    crDate = ''
    upDate = None
    trDate = None
    disclose = []

class Host(objref):
    """
    Object to hold host informations
    """
    id = 0
    name = ''
    status = []
    addr = []
    registrar = []
    crDate = ''
    upDate = None
    trDate = None

class Registrar(objref):
    """
    Object to hold registrar informations
    """
    id = 0
    roid = None
    name = ''
    href = ''

class Result(objref):
    """
    used to hold all items directly resulted out of customer request and all additional (referenced) objects
    """
    items = None
    additional = None
