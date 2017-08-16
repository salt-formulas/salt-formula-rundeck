{%- from "rundeck/map.jinja" import client with context %}

{%- for name, secret in client.get('secret', {}).items() %}

{%- set path = secret.path|default(name) %}

{%- if secret.enabled|default(True) %}

rundeck-key-{{ path|replace('/', '-') }}-create:
  rundeck_secret.present:
    - name: {{ path }}
    - type: {{ secret['type'] }}
    - content: {{ secret['content'] | yaml_encode }}
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

{%- else %}

rundeck-key-{{ path|replace('/', '-') }}-delete:
  rundeck_secret.absent:
    - name: {{ path }}
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

{%- endif %}

{%- endfor %}
