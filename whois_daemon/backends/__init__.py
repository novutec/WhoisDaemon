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

__all__ = [ 'mysql' ]

def factory(config):
    """
    load given backend module and return initialize instance
    
    @param config: global config dict
    
    @return: new instance of backend handler
    """
    mod = __import__("whois_daemon.backends.%s" % config['module'], fromlist = ["whois_daemon.backends"])
    return mod.init(config['connection'])
