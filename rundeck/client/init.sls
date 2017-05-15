{%- from "rundeck/map.jinja" import client with context %}

{%- if client.enabled|default(False) %}
include:
{%- if client.project is defined %}
  - rundeck.client.project
{%- endif %}
{%- endif %}
