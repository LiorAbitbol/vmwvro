"""
Utilities and helper functions.

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
