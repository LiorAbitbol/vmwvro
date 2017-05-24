"""
VMware vRealize Client implementation and supporting objects.

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
import requests

from .config import URL_GET_WORKFLOW_BY_ID
from .utils import format_url, is_json
from .workflows import Workflow


class Client:
    def __init__(self, session):
        """
        Returns a new Client instance

        :param session:
         Session object containing Url and authentication for vRO.
        """
        self.log = logging.getLogger(__class__.__name__)

        if session.url is None or session.basic_auth is None:
            self.log.error("Session object is invalid, missing Url and/or authentication data.")
            raise ValueError("Session object is invalid!")

        self.session = session

    def get_workflow(self, workflow_id):
        """
        Get a Workflow object by Id lookup.

        :param workflow_id:
         The Id of the Workflow to get.
        """
        url = format_url(URL_GET_WORKFLOW_BY_ID,
                         base_url=self.session.url,
                         id=workflow_id)

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        r = requests.get(url,
                         auth=self.session.basic_auth,
                         verify=self.session.verify_ssl,
                         headers=headers)

        r.raise_for_status()

        if not is_json(r.text):
            raise ValueError("vRO did not return JSON response!")

        wf = Workflow(session=self.session)
        wf.load_from_json(data=r.json())
        return wf
