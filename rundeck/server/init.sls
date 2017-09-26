{%- from "rundeck/map.jinja" import server with context %}
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
    - shell: /bin/false
    {%- if server.user.uid is defined %}
    - uid: {{ server.user.uid }}
    {%- endif %}
    {%- if server.user.gid is defined %}
    - gid: {{ server.user.gid }}
    {%- endif %}
    - system: True
    - groups:
      - {{ server.user.group }}
    - require:
      - group: rundeck_group

rundeck_home_dir:
  file.directory:
    - name: {{ server.home_dir }}
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 755
    - require:
      - user: rundeck_user

rundeck_root_dir:
  file.directory:
    - name: {{ server.root_dir }}
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 755
    - require:
      - user: rundeck_user

rundeck_lib_dirs:
  file.directory:
    - names:
      - {{ server.root_dir }}/log
      - {{ server.root_dir }}/logs
      - {{ server.root_dir }}/plugins
      - {{ server.root_dir }}/rundeck
      - {{ server.root_dir }}/storage
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 755
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: rundeck_root_dir

rundeck_os_credentials_dir:
  file.directory:
    - names:
      - {{ server.root_dir }}/storage/content/keys/cis/openstack
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 755
    - makedirs: True
    - recurse:
      - user
      - group
      - mode
    - require:
      - file: rundeck_root_dir

rundeck_etc_dir:
  file.directory:
    - name: {{ server.root_dir }}/etc
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 755
    - require:
      - user: rundeck_user

rundeck_framework_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/framework.properties
    - source: salt://rundeck/files/framework.properties
    - template: jinja
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_tokens_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/tokens.properties
    - source: salt://rundeck/files/tokens.properties
    - template: jinja
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_realm_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/realm.properties
    - source: salt://rundeck/files/realm.properties
    - template: jinja
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_rundeck_properties:
  file.managed:
    - name: {{ server.root_dir }}/etc/rundeck-config.properties
    - source: salt://rundeck/files/rundeck-config.properties
    - template: jinja
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 640
    - require:
      - file: rundeck_etc_dir

rundeck_ssh_dir:
  file.directory:
    - name: {{ server.root_dir }}/rundeck/.ssh
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 700
    - require:
      - file: rundeck_root_dir

rundeck_ssh_private_key:
  file.managed:
    - name: {{ server.root_dir }}/rundeck/.ssh/id_rsa
    - source: salt://rundeck/files/private_key
    - template: jinja
    - user: {{ server.user.name }}
    - group: {{ server.user.group }}
    - mode: 600
    - require:
      - file: rundeck_ssh_dir

{%- endif %}
