{% from "rundeck/map.jinja" import server with context %}
{%- from "rundeck/map.jinja" import client with context %}

{%- for name, project in client.project.items() %}

{%- set project_name = project.name|default(name) %}

rundeck_{{ project_name }}_project:
  rundeck_project.present:
    - name: {{ project_name }}
    - description: {{ project.description|default("") }}

rundeck_{{ project_name }}_resources:
  file.managed:
    - name: {{ server.root_dir }}/rundeck/projects/{{ project_name }}/etc/resources.yaml
    - source: salt://rundeck/files/resources.yaml
    - template: jinja
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 640
    - context:
        project_name: {{ project_name }}
    - require:
      - rundeck_project: rundeck_{{ project_name }}_project

{%- endfor %}
