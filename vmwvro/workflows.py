"""
VMware vRealize Workflow implementation and supporting objects.

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
import time

from .config import URL_RUN_WORKFLOW_BY_ID
from .utils import format_url


class WorkflowRunError(Exception):
    """Workflow Run Exception."""
    pass


class Workflow:

    @property
    def description(self):
        return self._description

    @property
    def has_input_parameters(self):
        if len(self._input_parameters) > 0:
            return True
        return False

    @property
    def href(self):
        return self._href

    @property
    def id(self):
        return self._id

    @property
    def input_parameters(self):
        return self._input_parameters

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    def __init__(self, session):
        """
        Returns a new Workflow instance.

        :param session:
         Session object contains vRO appliance and authentication data.
        """
        self.log = logging.getLogger(__class__.__name__)

        self._jdata = None
        self._description = None
        self._name = None
        self._href = None
        self._id = None
        self._version = None
        self._input_parameters = WorkflowParameters()

        if session.url is None or session.basic_auth is None:
            self.log.error("Session object is invalid, it is missing Url and/or authentication data.")
            raise ValueError("Session object is invalid!")

        self.session = session

    def _get_input_parameters(self):
        coll = WorkflowParameters()
        if self._jdata.get("input-parameters"):
            for p in self._jdata.get("input-parameters"):
                coll.add(name=p.get("name"),
                         value=p.get("value"),
                         _type=p.get("type"),
                         description=p.get("description"))
        return coll

    def load_from_json(self, data):
        """
        Loads Workflow data into this instance from JSON.

        :param data:
         A JSON representation of a vRO Workflow.
        """
        self._jdata = data

        try:
            self._description = data.get("description")
            self._name = data.get("name")
            self._href = data.get("href")
            self._id = data.get("id")
            self._version = data.get("version")
            self._input_parameters = self._get_input_parameters()
        except Exception as ex:
            self.log.error("Error reading JSON attributes: %s" % ex)

    def json(self):
        """Returns this instance in JSON."""
        return self._jdata

    def start(self, params=None):
        """
        Starts the Workflow.

        :param params:
         A WorkflowParameters object.
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        if params is None:
            data = "{}"
        else:
            if type(params) is not WorkflowParameters:
                raise ValueError("Expected a WorkflowParameters object!")
            data = params.to_json()

        url = format_url(URL_RUN_WORKFLOW_BY_ID,
                         base_url=self.session.url,
                         id=self.id)

        r = requests.post(url,
                          auth=self.session.basic_auth,
                          verify=self.session.verify_ssl,
                          headers=headers,
                          data=data)

        r.raise_for_status()

        if r.status_code == 202:
            print(r.headers.get("Location"))
            run = WorkflowRun(session=self.session)
            run.href = r.headers.get("Location")
            run.update()
            return run

        raise WorkflowRunError("Failed to start Workflow!")


class _WorkflowParameter:

    def __init__(self, name=None, value=None, _type=None, scope=None, description=None):
        """
        Returns a new _WorkflowParameter instance.

        :param name: parameter name
        :param value:  parameter value
        :param _type: parameter value
        :param scope: parameter scope
        :param description: parameter description
        """
        self.name = name
        self.value = value
        self.type = _type
        self.scope = scope
        self.description = description


class WorkflowParameters:

    def __init__(self):
        """Returns a new WorkflowParameters instance.

        This collection object holds one or more vRO parameters.
        """
        self._params = list()

    def __len__(self):
        return len(self._params)

    def __iter__(self):
        for param in self._params:
            yield param

    def add(self, name, value, _type="string", scope="local", description=None):
        """
        Add a parameter to the collection.

        :param name: parameter name
        :param value: parameter value
        :param _type: parameter type, default is 'string'
        :param scope: parameter scope, default is 'local'
        :param description: parameter description, default is None
        """
        self._params.append(_WorkflowParameter(name, value, _type, scope, description))

    def to_json(self):
        """Returns this instance in JSON format."""
        data = '{"parameters":['

        num_of_params = len(self._params)
        cur_param = 1

        for param in self._params:
            data += '{"type":"%s","scope":"%s","name":"%s","description":"%s","value":{"%s":{"value":"%s"}}}' % (
                param.type, param.scope, param.name, param.description, param.type, param.value
            )
            if cur_param < num_of_params:
                data += ","
            cur_param += 1

        data += "]}"

        return data

    def to_xml(self):
        """Returns this instance in XML format."""
        data = '<execution-context xmlns="http://www.vmware.com/vco"><parameters>'

        for param in self._parameters:
            data += '<parameter name="%s" type="%s"><%s>%s</%s></parameter>' % (
                param.name, param.type, param.type, param.value, param.type
            )

        data += '</parameters></execution-context>'

        return data


class WorkflowRun:

    @property
    def end_date(self):
        return self._end_date

    @property
    def href(self):
        return self._href

    @href.setter
    def href(self, value):
        self._href = value

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def start_date(self):
        return self._start_date

    @property
    def started_by(self):
        return self._started_by

    @property
    def state(self):
        return self._state

    def __init__(self, session):
        """Returns a new WorkflowRun instance.

        WorkflowRun objects are returned by Workflow when they are started.

        :param session:
        """
        self.log = logging.getLogger(__class__.__name__)

        if session.url is None or session.basic_auth is None:
            self.log.error("Session object is invalid, missing Url and/or basic authentication!")
            raise ValueError("Session object is invalid!")

        self.session = session
        self.log.debug("Session.url = %s" % session.url)

        # Initialize instance attributes
        self._jdata = None
        self._end_date = None
        self._href = None
        self._id = None
        self._name = None
        self._start_date = None
        self._started_by = None
        self._state = None

    def load_from_json(self, data):
        """Load Workflow Run data from JSON."""
        self._jdata = data

        self._end_date = self._jdata.get("end-date")
        self._href = self._jdata.get("href")
        self._id = self._jdata.get("id")
        self._name = self._jdata.get("name")
        self._start_date = self._jdata.get("start-date")
        self._started_by = self._jdata.get("started-by")
        self._state = self._jdata.get("state")

    def wait_until_complete(self, timeout=300, poll=10, states=[]):
        """Wait until this Workflow Run instance completes, cancels or fails.

        :param timeout:
         The timeout (in seconds) to wait before giving up.
         By default, timeout is 300 seconds. Timeout rate must be 5
         or more seconds, and greater than poll rate.

        :param poll:
         The poll rate (in seconds) to check the Workflow run state.
         By default, poll rate is 10 seconds. Poll rate must be 1 or
         more seconds, and less than timeout rate.

        :param states:
         A list of Workflow states to check against while waiting.
         If the state matches the Workflow Run State, this method
         will complete.
         By default, this method will check for the following states:
         - completed
         - canceled
         - failed
        """
        if timeout < 5:
            raise ValueError("Timeout must be 5 or more seconds!")
        if poll < 1:
            raise ValueError("Poll rate must be 1 or more seconds!")
        if poll > timeout:
            raise ValueError("Poll rate cannot be greater than timeout!")

        finished_states = ["completed", "canceled", "failed"]

        current_try = 0
        retries = int(timeout/poll)
        end = False

        self.log.debug("Wait settings: Timeout=%s | Poll=%s | Retry=%s of %s" %
                       (timeout, poll, current_try, retries))

        while end is not True:
            current_try += 1
            self.update()

            if self.state in finished_states:
                end = True
            elif len(states) > 0 and self.state in states:
                end = True
            elif current_try >= retries:
                end = True
            else:
                time.sleep(poll)

    def update(self):
        """Update the state, logs and content of this Workflow Run."""
        if self.href is None:
            raise ValueError("Cannot update Workflow Run, 'href' data is not defined!")

        r = requests.get(self.href,
                         auth=self.session.basic_auth,
                         verify=self.session.verify_ssl,
                         headers={"Content-Type": "application/json"})

        r.raise_for_status()

        self.load_from_json(r.json())

