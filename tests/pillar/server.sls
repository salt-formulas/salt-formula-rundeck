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
      private_key: private
      public_key: public
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
