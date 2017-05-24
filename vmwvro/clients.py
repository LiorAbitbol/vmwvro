"""
VMware vRealize Client implementation and supporting objects.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>
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
