#!/usr/bin/env python
"""
Novutec Whois Daemon
Implementation of the RWS-DNRD Draft
http://tools.ietf.org/html/draft-sheng-weirds-icann-rws-dnrd-01

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
import getopt, sys, os
from flup.server.fcgi import WSGIServer
from whois_daemon import app

def usage():
    print """Usage:  """ + os.path.basename(sys.argv[0]) + """ [OPTION]

Options:
  -h,  --help          show this help
  -c   --configfile    load specified configuration file
"""

def main():
    configfile = None

    try :
        opts, args = getopt.getopt(sys.argv[1:], 'hc:', ['help', 'configfile='])
    except getopt.GetoptError, err :
        print str(err)
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ('-c', '--configfile') :
            configfile = a
        else :
            assert False, "unhandled option"

    if not configfile :
        print "No configuration file defined."
        usage()
        sys.exit(2)

    x = app(configfile)
    if x.config['daemon']['detach'] :
        context = x.get_context()
        with context:
            WSGIServer(x, bindAddress = x.config['daemon']['bind']).run()
    else :
        WSGIServer(x,
                   bindAddress = x.config['daemon']['bind'],
                   debug = x.config['daemon']['debug'],
                   umask = x.config['daemon']['umask']).run()

if __name__ == '__main__':
    main()
