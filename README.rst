===============
Rundeck Formula
===============

Rundeck is open source software that helps you automate routine operational
procedures in data center or cloud environments.

Sample pillars
==============

Configure Server
~~~~~~~~~~~~~~~~

Rundeck is suppose to be configure for running in Docker Swarm and the server
state prepares only configuration files, including binding parameters, system
user, Rundeck users and API tokens:

.. code-block:: yaml

    rundeck:
      server:
        enabled: true
        user:
          uid: 550
          gid: 550
        api:
          host: 10.20.0.2
          port: 4440
          https: false
        ssh:
          user: runbook
          private_key: <private>
          public_key: <public>

        users:
          admin:
            name: admin
            password: password
            roles:
              - user
              - admin
              - architect
              - deploy
              - build
          john:
            name: John
            password: johnspassword
            roles:
              - user
              - admin
              - architect
              - deploy
              - build
          kate:
            name: Kate
            password: katespassword
            roles:
              - user
              - admin
              - architect
              - deploy
              - build

        tokens:
          admin: EcK8zhQw


To configure Rundeck to use PostgreSQL instead of H2:


.. code-block:: yaml

    rundeck:
      server:
        datasource:
          engine: postgresql
          host: 10.20.0.2
          port: 5432
          username: ${_param:rundeck_postgresql_username}
          password: ${_param:rundeck_postgresql_password}
          database: ${_param:rundeck_postgresql_database}


Configure Client
~~~~~~~~~~~~~~~~

Configure Secret Keys
^^^^^^^^^^^^^^^^^^^^^

It is possible to configure secret items in Key Storage in Rundeck:

.. code-block:: yaml

     rundeck:
       client:
         enabled: true
         secret:
           openstack/username:
             type: password
             content: admin
           openstack/password:
             type: password
             content: password
           openstack/keypair/private:
             type: private
             content: <private>
           openstack/keypair/public:
             type: public
             content: <public>

It is possible to disable keys to be sure that they are not present in Rundeck:

.. code-block:: yaml

    rundeck:
       client:
         secret:
           openstack/username:
             enabled: false

Configure Projects
^^^^^^^^^^^^^^^^^^

Projects can be configured with a set of nodes which are available to run jobs
within them. Rundeck uses `rundeck:server:ssh` credentials to access nodes.
Jobs can be configured from a separate GIT repository using the SCM Import
plugin.


.. code-block:: yaml

    rundeck:
      client:
        enabled: true
        project:
          project0:
            description: project
            node:
              node01:
                nodename: node01
                hostname: node01.cluster.local
                username: runbook
                tags: [ubuntu, docker]
              node02:
                nodename: node02
                hostname: node02.cluster.local
                username: runbook
                tags: [centos, docker]
            plugin:
              import:
                address: http://gerrit.cluster.local/jobs/rundeck-jobs.git
                branch: master


Documentation and Bugs
======================

To learn how to install and update salt-formulas, consult the documentation
available online at:

    http://salt-formulas.readthedocs.io/

For feature requests, bug reports or blueprints affecting entire ecosystem,
use Launchpad salt-formulas project:

    https://launchpad.net/salt-formulas

You can also join salt-formulas-users team and subscribe to mailing list:

    https://launchpad.net/~salt-formulas-users

Developers wishing to work on the salt-formulas projects should always base
their work on master branch and submit change request against specific formula.

    https://gerrit.mcp.mirantis.net/#/admin/projects/salt-formulas/rundeck

Any questions or feedback is always welcome so feel free to join our IRC
channel:

    #salt-formulas @ irc.freenode.net
