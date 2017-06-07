{%- from "rundeck/map.jinja" import server with context %}
{%- from "rundeck/map.jinja" import client with context %}

{%- for name, project in client.project.items() %}

{%- set project_name = project.name|default(name) %}

rundeck-{{ project_name }}-project:
  rundeck_project.present:
    - name: {{ project_name }}
    - description: {{ project.description|default('') }}
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

rundeck-{{ project_name }}-resources:
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
      - rundeck_project: rundeck-{{ project_name }}-project
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

{%- set plugin = project.plugin|default({}) %}

{%- if plugin.import is defined %}

{%- set _import = plugin.import %}

rundeck-{{ project_name }}-scm-import:
  rundeck_scm.present_import:
    - name: git-import
    - address: {{ _import.address }}
    - project_name: {{ project_name }}
{%- if _import.format is defined %}
    - format: {{ _import.format }}
{%- endif %}
{%- if _import.branch is defined %}
    - branch: {{ _import.branch }}
{%- endif %}
{%- if _import.import_uuid_behavior is defined %}
    - import_uuid_behavior: {{ _import.import_uuid_behavior }}
{%- endif %}
{%- if _import.path_template is defined %}
    - path_template: {{ _import.path_template }}
{%- endif %}
    - require:
      - rundeck_project: rundeck-{{ project_name }}-project
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

rundeck-{{ project_name }}-scm-import-enable:
  rundeck_scm.enabled_import:
    - name: git-import
    - project_name: {{ project_name }}
    - require:
      - rundeck_scm: rundeck-{{ project_name }}-scm-import
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

rundeck-{{ project_name }}-scm-import-sync:
  rundeck_scm.sync_import:
    - name: git-import
    - project_name: {{ project_name }}
{%- if _import.file_pattern is defined %}
    - file_pattern: {{ _import.file_pattern }}
{%- endif %}
    - require:
      - rundeck_scm: rundeck-{{ project_name }}-scm-import
    - watch:
      - rundeck_scm: rundeck-{{ project_name }}-scm-import-enable
    {%- if grains.get('noservices', False) %}
    - onlyif: 'false'
    {%- endif %}

{%- endif %}

{%- endfor %}
