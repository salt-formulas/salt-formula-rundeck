{%- from "rundeck/map.jinja" import client with context %}

{%- if client.enabled|default(False) %}
include:
{%- if client.project is defined %}
  - rundeck.client.project
{%- endif %}
{%- if client.secret is defined %}
  - rundeck.client.secret
{%- endif %}
{%- endif %}

{%- if grains.get('noservices', False) %}
rundeck-client-nop:
  test.nop: []
{%- endif %}
