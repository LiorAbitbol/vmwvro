"""
Utilities and helper functions.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>
"""

import json
import re
import xml.etree.ElementTree as ET


def is_json(obj):
    """
    Returns True if object is JSON.

    :param obj:
     An object, preferably a JSON object.

    :return:
     True if JSON.
     False is Not-JSON
    """

    try:
        json.loads(obj)
    except ValueError:
        return False
    return True


def is_xml(obj):
    """
    Returns True if object is XML.

    :param obj:
     An object, preferably a XML object.

    :return:
     True if XML
     False if Not-XML
    """

    try:
        ET.fromstring(obj)
    except ValueError:
        return False
    return True


def format_url(url, **kwargs):
    """
    Formats URL template with keyword values.

    :param url:
     URL template. i.e. https://{{host}}/

    :param kwargs:
     Keyword-Values to replace URL template.

    :return:
     A formatted URL.
    """

    # Count place holders in URL so we can validate against
    # number of parameters provided.
    num_of_placeholders = len(re.findall("{{[^}}]", url))

    if len(kwargs) != num_of_placeholders:
        raise ValueError("Number of place holders in string does not match number of parameters!")

    # User regex to replace place holders with parameter values
    found = 0
    for arg in kwargs:
        pattern = "{{%s}}" % arg
        if re.search(pattern, url, re.IGNORECASE):
            url = url.replace(pattern, kwargs[arg])
            found += 1

    if found != len(kwargs):
        raise ValueError("Not all place holders matched the parameters!")

    return url
