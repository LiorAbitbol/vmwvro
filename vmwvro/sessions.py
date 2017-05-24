"""
VMware vRealize Session implementation and supporting objects.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>
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
