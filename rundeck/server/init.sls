{% from "rundeck/map.jinja" import server with context %}
{%- if server.enabled|default(False) %}

rundeck_group:
  group.present:
    - name: {{ server.user.group }}
    {%- if server.user.gid is defined %}
    - gid: {{ server.user.gid }}
    {%- endif %}
    - system: True

rundeck_user:
  user.present:
    - name: {{ server.user.name }}
    - home: {{ server.home_dir }}
    - shell: /bin/bash
    {%- if server.user.uid is defined %}
    - uid: {{ server.user.uid }}
    {%- endif %}
    {%- if server.user.gid is defined %}
    - gid: {{ server.user.gid }}
    {%- endif %}
    - system: True
    - groups:
      - rundeck
    - require:
      - group: rundeck_group

rundeck_home_dir:
  file.directory:
    - name: {{ server.home_dir }}
    - user: rundeck
    - group: rundeck
    - mode: 755
    - require:
      - user: rundeck_user

rundeck_root_dir:
  file.directory:
    - name: {{ server.root_dir }}
    - user: rundeck
    - group: rundeck
    - mode: 755
    - require:
      - user: rundeck_user

rundeck_etc_dir:
  file.directory:
    - name: {{ server.root_dir }}/etc
    - user: rundeck
    - group: rundeck
    - mode: 755
    - require:
      - user: rundeck_user

rundeck_framework_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/framework.properties
    - source: salt://rundeck/files/framework.properties
    - template: jinja
    - user: rundeck
    - group: rundeck
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_tokens_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/tokens.properties
    - source: salt://rundeck/files/tokens.properties
    - template: jinja
    - user: rundeck
    - group: rundeck
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_realm_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/realm.properties
    - source: salt://rundeck/files/realm.properties
    - template: jinja
    - user: rundeck
    - group: rundeck
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_rundeck_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/rundeck-config.properties
    - source: salt://rundeck/files/rundeck-config.properties
    - template: jinja
    - user: rundeck
    - group: rundeck
    - mode: 640
    - require:
      - file: rundeck_etc_dir

{%- endif %}
