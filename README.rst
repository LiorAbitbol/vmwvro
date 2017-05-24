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

Quickstart
==========

This guide will give you an introduction on how to get started with ``vmwvro``.

Interacting with vRO
--------------------

Interacting with VMware vRealize Orchestrator requires a Client object. The Client object exposes methods to manage Workflows. The following code sample illustrates how to create a Client object:

.. code-block:: python

    >>> from vmwvro import Client, Session
    >>> vro_url = "https://my_vro_server:8281"
    >>> vro_usr = "my_username"
    >>> vro_pwd = "my_password"
    >>> client = Client(Session(url=vro_url, username=vro_usr, password=vro_pwd))

The Session object can also except the following optional parameters:

* verify_ssl -- verifies SSL certification, by default it is set to False
* disable_warnings -- disables warnings, by default it is set to True

Once you have a Client instance, you can proceed with the following examples.

Get Workflow Id
---------------

You can retrieve the Workflow Id by name or keywords lookup. The following code illustrates how to get the Workflow:

.. code-block:: python

    >>> wf_id = client.find_workflow_id_by_name("my cool workflow")
    >>> print(wf_id)
    1a20863f-549b-47e4-a9db-361ea4fa2f69
    >>> wf_id = client.find_workflow_id_by_keyword("cool")
    >>> print(wf_id)
    1a20863f-549b-47e4-a9db-361ea4fa2f69

Run a Workflow
--------------

In order to start a Workflow, you will need to know the Workflow Id of the Workflow. You can use the above example to retrieve the Id if you know the name of the Workflow.

.. code-block:: python

    >>> wf_id = "1a20863f-549b-47e4-a9db-361ea4fa2f69"
    >>> wf = client.get_workflow(wf_id)
    >>> wf_run = wf.start()
    >>> print("Workflow state: %s" % wf_run.state)
    Workflow state: running

Passing Workflow Parameters
---------------------------

Many Workflows require one or more input parameters. The following code illustrates how to create and pass parameters to a Workflow:

.. code-block:: python

    >>> from vmwvro.workflows import WorkflowParameters
    >>> param = WorkflowParameters()
    >>> param.add(name="vmname", value="some_vm_name", _type="VC:VirtualMachine")
    >>> param.add(name="user", value="some_user")
    >>> wf_run = wf.start(param)
    >>> print("Workflow state: %s" % wf_run.state)
    Workflow state: running

The add() method requires the name and value of the parameter. You can also specify tye type if it is not a string.

Wait for Workflow to Complete
-----------------------------

After starting a Workflow, it may take a few seconds to a few minutes to complete. The following code illustrates how to wait for the Workflow to finish:

.. code-block:: python

    >>> wf_run.wait_until_complete()
    >>> print("Workflow completed with state: %s" % wf_run.state)
    Workflow completed with state: completed

