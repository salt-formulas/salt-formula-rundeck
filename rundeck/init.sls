include:
  {%- if pillar.rundeck.server is defined %}
  - rundeck.server
  {%- endif %}
  {%- if pillar.rundeck.client is defined %}
  - rundeck.client
  {%- endif %}
