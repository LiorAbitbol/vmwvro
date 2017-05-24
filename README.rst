vmwvro
======

A simple api library to interface with VMware vRealize Orchestrator (vRO).

Features
--------

What you can do with ``vmwvro``:

* get workflow information
* start a workflow
* monitor a workflow run

Dependencies
------------

* Python 3.x
* `requests v2.14.2 <http://docs.python-requests.org/en/master/>`_

Installation
------------

``vmwvro`` is available on the
`Python Package Index <http://pypi.python.org/pypi/vmwvro/>`_

.. code-block:: python

    $ pip install vmwvro

Usage
-----

Create a Session object. Session object contains the Url and authentication information for the VMware vRealize Orchestrator appliance.

.. code-block:: python

    from vmwvro import Session

    vro_url = 'https://some_vro_server:8281'
    vro_usr = 'some_user'
    vro_pwd = 'some_password'

    session = Session(url=vro_url, username=vro_usr, password=vro_pwd)

Create a Client object and pass in the session object. Client object exposes methods to interact with VMware vRealize Orchestrator.

.. code-block:: python

    from vmwvro import Client

    client = Client(session)

Start a workflow - without any parameters.

.. code-block:: python

    wf = client.get_workflow(workflow_id)

    wf_run = wf.start()
    print("Workflow state: %s" % wf_run.state)

Start a workflow - with parameters.

.. code-block:: python

    from vmwvro.workflows import WorkflowParameters

    param = WorkflowParameters()
    param.add(name="vmname", value="some_vm_name", _type="VC:VirtualMachine")
    param.add(name="user", "some_user")

    wf_run = wf.start(param)
    print("Workflow state: %s" % wf_run.state)

Wait for a workflow to complete.

.. code-block:: python

    wf_run.wait_until_complete()
    print("Workflow completed with state: %s" % wf_run.state)

License
-------

| Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>
|
| Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
|
| The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
|
| THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
