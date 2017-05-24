"""
VMware vRealize Session implementation and supporting objects.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
import re

from requests.auth import HTTPBasicAuth
from requests.packages import urllib3

from .config import VRO_TCP_PORT


class Session:
    @property
    def basic_auth(self):
        return HTTPBasicAuth(self.username, self.password)

    @property
    def disable_warnings(self):
        return self._disable_warnings

    @property
    def password(self):
        return self._password

    @property
    def url(self):
        return self._url

    @property
    def username(self):
        return self._username

    @property
    def verify_ssl(self):
        return self._verify_ssl

    def __init__(self, url, username, password, verify_ssl=False, disable_warnings=True):
        """
        Returns a new Session object.

        :param url:
         Url of the vRO appliance (i.e. https://vro.mydomain.com:8281).

        :param username:
         Username to authenticate with the vRO appliance.

        :param password:
         Password to authenticate with the vRO appliance.

        :param verify_ssl:
         Verify SSL certification during connections, by default False.

        :param disable_warnings:
         Disable connection warnings, by default True.
        """
        self.log = logging.getLogger(__class__.__name__)

        self._url = url
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl
        self._disable_warnings = disable_warnings

        if re.match(r"^http[s]://", url) is None:
            self._url = "https://" + url
            self.log.info("Added HTTPS protocol to URL: %s" % self.url)

        if re.match(r".*(?:\:\d+)$", url) is None:
            self._url += ":{}".format(VRO_TCP_PORT)
            self.log.info("Added default vRO TCP Port to URL: %s" % self.url)

        if disable_warnings:
            self.log.info("Disabling HTTP warnings in urllib3")
            urllib3.disable_warnings()

        self.log.debug("Base URL = %s" % self.url)
