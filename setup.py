#!/usr/bin/env python
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
from setuptools import setup, find_packages

setup(
    name = 'whois_daemon',
    version = '0.1',
    description = 'REST Whois Service',
    author = 'Novutec Inc.',
    author_email = '',
    url = 'http://github.com/novutec/whois_daemon',
    packages = ['whois_daemon', 'example', 'templates'],
    long_description = open('README.txt').read(),
    classifiers = [
      "License :: OSI Approved :: Apache Software License (ASF), Version 2.0",
      'Environment :: Console',
      "Programming Language :: Python",
      "Development Status :: 4 - Beta",
      'Operating System :: POSIX',
      "Intended Audience :: Developers",
      "Topic :: Internet",
    ],
    keywords = 'networking internet whois rwsdnrd rest',
    license = 'Apache Software License (ASF)',
    scripts = ['whoisd', 'whoisd.fcgi'],
    install_requires = [
                        'setuptools',
                        'flask>=0.8',
                        'oursql>=0.9.3.1'
    ],
    include_package_data = True,
    package_data = {
        'config' : ['config.yaml']
    }
)
