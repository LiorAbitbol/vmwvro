"""
Configuration parameters.

Copyright (c) 2017, Lior P. Abitbol <liorabitbol@gmail.com>
"""

#
# vRO Default TCP Port
#
VRO_TCP_PORT = 8281

#
# vRO URL templates
#
URL_GET_WORKFLOW_BY_ID = "{{base_url}}/vco/api/workflows/{{id}}"
URL_RUN_WORKFLOW_BY_ID = "{{base_url}}/vco/api/workflows/{{id}}/executions/"
