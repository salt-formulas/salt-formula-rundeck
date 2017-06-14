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
