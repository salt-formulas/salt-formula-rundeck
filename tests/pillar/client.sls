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
    secret:
      openstack/auth_url:
        type: password
        content: http://openstack.cluster.local/identity/v3/auth/tokens
      openstack/username:
        type: password
        content: admin
      openstack/password:
        type: password
        content: password
      openstack/project_name:
        type: password
        content: admin
      openstack/keypair:
        enabled: false
      ssh/runbook:
        enabled: false
