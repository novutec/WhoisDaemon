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

__all__ = [ 'xmlFrm', 'jsonFrm', 'htmlFrm', 'yamlFrm', 'textFrm' ]

from whois_daemon import objects

class Error(Exception) :
    """
    global mysql exception class
    """
    def __init__(self, msg):
        self.what = msg

    def __str__(self):
        return self.what


def filterROID(x):
    """
    check if given object has internal id and overwrite it by its defined roid
    
    @param x: dict to filter
    """

    if x.has_key('roid') and x['roid'] :
        x['id'] = x['roid']
        del x['roid']

    for check_name in ('registrar', 'ns', 'contact') :
        if x.has_key(check_name) and x[check_name] :
            res = []
            for item in x[check_name] :
                if item.has_key('roid') and item['roid'] :
                    item['id'] = item['roid']
                    del item['roid']
                if check_name == 'ns' and item.has_key('id') :
                    del item['id']
                res.append(item)
            x[check_name] = res

def filterDisclosed(obj):
    """
    set all disclosed values in given object to None and remove disclose field itself
    
    @param obj: Object to filter
    """
    if not isinstance(obj, objects.Contact) and not isinstance(obj, objects.PostalInfo) :
        return obj

    if obj.disclose :
        for field in obj.disclose :
            if field in obj.__dict__ :
                obj.__dict__[field] = None
    del obj.disclose

    if isinstance(obj, objects.Contact) :
        newPostalIinfo = []
        for item in obj.postalInfo :
            if item.disclose :
                filterDisclosed(item)
            newPostalIinfo.append(item)
        obj.postalInfo = newPostalIinfo
