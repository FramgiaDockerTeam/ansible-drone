### Ansible Drone Plugin

#### Configure deployment

Edit file: `.drone.yml`

```
deploy:
  ssh:
    image: framgia/ansible-drone
    host: {server_ip}
    user: {ssh_user}
    port: 22
    commands:
      - ansible-playbook -i .ansible/staging .ansible/site.yml
```
