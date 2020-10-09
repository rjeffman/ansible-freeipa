FreeIPA Ansible Collection
==========================

The FreeIPA Ansible Collection provides [Ansible](https://www.ansible.com/) roles and playbooks to install and uninstall [FreeIPA](https://www.freeipa.org/) `servers`, `replicas` and `clients`. It also provides modules and playbooks to manage FreeIPA installations.

> **Note**: A configured Ansible environment where the Ansible nodes are reachable and are properly set up is required for both roles and modules, and it might be required a properly configure IP address. The Ansible roles require a working package manager.


Roles and Modules
=================

These are the roles and modules currently available. If you want to write a new module please read [writing a new module](plugins/modules/README.md).


Roles
-----

Roles for server, replica and client deployment, with support for cluster deployments in a single playbook. Client role supports one-time-password (OTP) for installation, and repair mode.

* [Server](docs/roles/README-ipaserver.md)
* [Replica](docs/roles/README-ipareplica.md)
* [Client](docs/roles/README-ipaclient.md)


Modules
-------

All modules can be found under `plugins/modules`.

* [ipaconfig](docs/modules/config.md): global server configuration
* [ipadelegation](docs/modules/delegation.md): delegation management
* [ipadnsconfig](docs/modules/dnsconfig.md): dns configuration
* [ipadnsforwardzone](docs/modules/dnsforwardzone.md): dns forwarder management
* [ipadnsrecord](docs/modules/dnsrecord.md): dns record management
* [ipadnszone](docs/modules/dnszone.md): dns zone management
* [ipagroup](docs/modules/group.md): group management
* [ipahbacrule](docs/modules/hbacrule.md): hbacrule management
* [ipahbacsvc](docs/modules/hbacsvc.md): hbacsvc management
* [ipahbacsvcgroup](docs/modules/hbacsvc.md): hbacsvcgroup management
* [ipahost](docs/modules/host.md): host management
* [ipahostgroup](docs/modules/hostgroup.md): hostgroup management
* [ipalocation](docs/modules/location.md): location management
* [ipaprivilege](docs/modules/privilege.md): privilege management
* [ipapwpolicy](docs/modules/pwpolicy.md): pwpolicy management
* [iparole](docs/modules/role.md): role management
* [ipaselfservice](docs/modules/selfservice.md): selfservice management
* [ipaservice](docs/modules/service.md): service management
* [ipasudocmd](docs/modules/sudocmd.md): sudocmd management
* [ipasudocmdgroup](docs/modules/sudocmdgroup.md): sudocmdgroup management
* [ipasudorule](docs/modules/sudorule.md): sudorule management
* [ipatopologysegment](docs/modules/topology.md): topology management
* [ipatopologysuffix](docs/modules/topology.md): topology management
* [ipatrust](docs/modules/trust.md): trust management
* [ipauser](docs/modules/user.md): user management
* [ipavault](docs/modules/vault.md): vault management


System Requirements and Limitations
===================================


Supported FreeIPA Versions
--------------------------

FreeIPA versions 4.6 and up are supported by all roles.

The client role supports versions 4.4 and up, the server role is working with versions 4.5 and up, the replica role is currently only working with versions 4.6 and up.


Supported Distributions
-----------------------

* RHEL/CentOS 7.4+
* Fedora 26+
* Ubuntu
* Debian 10+ (ipaclient only, no server or replica!)


Requirements
------------

**Controller**
* Ansible version: 2.8+ (ansible-freeipa is an Ansible Collection)
* /usr/bin/kinit is required on the controller if a one time password
(OTP) is used
* python3-gssapi is required on the controller if a one time password
(OTP) is used with keytab to install the client.

**Node**
* Supported FreeIPA version (see above)
* Supported distribution (needed for package installation only, see above)


Limitations
-----------

**External signed CA**

External signed CA is now supported. But the currently needed two step process is an issue for the processing in a simple playbook.

Work is planned to have a new method to handle CSR for external signed CAs in a separate step before starting the server installation.


Usage
=====


How to use ansible-freeipa
--------------------------

**GIT repo**

The simplest method for now is to clone this repository on the controller from github directly and to start the deployment from the ansible-freeipa directory:

```
git clone https://github.com/freeipa/ansible-freeipa.git
cd ansible-freeipa
```

You can use the roles directly within the top directory of the git repo, but to be able to use the management modules in the plugins subdirectory, you have to either adapt `ansible.cfg` or create links for the roles, modules or directories.

You can either adapt ansible.cfg:

```
roles_path   = /my/dir/ansible-freeipa/roles
library      = /my/dir/ansible-freeipa/plugins/modules
module_utils = /my/dir/ansible-freeipa/plugins/module_utils
```

Or you can link the directories:

```
ansible-freeipa/roles to ~/.ansible/
ansible-freeipa/plugins/modules to ~/.ansible/plugins/
ansible-freeipa/plugins/module_utils to ~/.ansible/plugins/
```

**RPM package**

There are RPM packages available for Fedora 29+. These are installing the roles and modules into the global Ansible directories for `roles`, `plugins/modules` and `plugins/module_utils` in the `/usr/share/ansible` directory. Therefore is it possible to use the roles and modules without adapting the names like it is done in the example playbooks.

**Ansible galaxy**

This command will get the whole collection from galaxy:

```
ansible-galaxy collection install freeipa.ansible_freeipa
```

Installing collections using the ansible-galaxy command is only supported with ansible 2.9+.

The mazer tool can be used for to install the collection for ansible 2.8:

```
mazer install freeipa.ansible_freeipa
```

Ansible galaxy does not support the use of dash ('-') in a name and is automatically replacing this with an underscore ('\_'). Therefore the name is `ansible_freeipa`. The ansible_freeipa collection will be placed in the directory `~/.ansible/collections/ansible_collections/freeipa/ansible_freeipa` where it will be automatically be found for this user.

The needed adaptions of collection prefixes for `modules` and `module_utils` will be done with ansible-freeipa release `0.1.6` for galaxy.


Ansible inventory file
----------------------

The most important parts of the inventory file is the definition of the nodes, settings and the management modules. Please remember to use [Ansible vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) for passwords. The examples here are not using vault for better readability.

**Master server**

The master server is defined within the `[ipaserver]` group:

```
[ipaserver]
ipaserver.test.local
```

There are variables that need to be set like `domain`, `realm`, `admin password` and `dm password`. These can be set in the `[ipaserver:vars]` section:

```
[ipaserver:vars]
ipaadmin_password=ADMPassword1
ipadm_password=DMPassword1
ipaserver_domain=test.local
ipaserver_realm=TEST.LOCAL
```

The admin principle is `admin` by default. Please set `ipaadmin_principal` if you need to change it.

You can also add more setting here, like for example to enable the DNS
server or to set auto-forwarders:
```
[ipaserver:vars]
ipaserver_setup_dns=yes
ipaserver_auto_forwarders=yes
```

But also to skip package installation or firewalld configuration:

```
[ipaserver:vars]
ipaserver_install_packages=no
ipaserver_setup_firewalld=no
```
The installation of packages and also the configuration of the firewall are by default enabled. Note that it is not enough to mask systemd firewalld service to skip the firewalld configuration. You need to set the variable to `no`.

For more server settings, please have a look at the [server role documentation](roles/ipaserver/README.md).

**Replica**

The replicas are defined within the `[ipareplicas]` group:

```
[ipareplicas]
ipareplica1.test.local
ipareplica2.test.local
```

If the master server is already deployed and there are DNS txt records to be able to auto-detect the server, then it is not needed to set `domain` or `realm` for the replica deployment. But it might be needed to set the master server of a replica because of the topology. If this is needed, it can be set either in the `[ipareplicas:vars]` section if it will apply to all the replicas in the `[ipareplicas]` group or it is possible to set this also per replica in the
`[ipareplicas]` group:

```
[ipareplicas]
ipareplica1.test.local
ipareplica2.test.local ipareplica_servers=ipareplica1.test.local
```

This will create a chain from `ipaserver.test.local <- ipareplica1.test.local <- ipareplica2.test.local`.

If you need to set more than one server for a replica (for fallbacks etc.), simply use a comma separated list for `ipareplica_servers`:

```
[ipareplicas_tier1]
ipareplica1.test.local

[ipareplicas_tier2]
ipareplica2.test.local
ipareplica_servers=ipareplica1.test.local,ipaserver.test.local
```
The first entry in `ipareplica_servers` will be used as the master.

In this case you need to have separate tasks in the playbook to first deploy replicas from tier1 and then replicas from tier2:

```yaml
---
- name: Playbook to configure IPA replicas (tier1)
  hosts: ipareplicas_tier1
  become: true

  roles:
  - role: ipareplica
    state: present

- name: Playbook to configure IPA replicas (tier2)
  hosts: ipareplicas_tier2
  become: true

  roles:
  - role: ipareplica
    state: present
```

You can add settings for replica deployment:

```
[ipareplicas:vars]
ipaadmin_password=ADMPassword1
ipadm_password=DMPassword1
ipaserver_domain=test.local
ipaserver_realm=TEST.LOCAL
```

You can also add more setting here, like for example to setup DNS or to enable auto-forwarders:
```
[ipareplica:vars]
ipaserver_setup_dns=yes
ipaserver_auto_forwarders=yes
```

If you need to skip package installation or firewalld configuration:

```
[ipareplicas:vars]
ipareplica_install_packages=no
ipareplica_setup_firewalld=no
```

The installation of packages and also the configuration of the firewall are by default enabled. Note that it is not enough to mask systemd firewalld service to skip the firewalld configuration. You need to set the variable to `no`.

For more replica settings, please have a look at the [replica role documentation](roles/ipareplica/README.md).


**Client**

Clients are defined within the `[ipaclients]` group:

```
[ipaclients]
ipaclient1.test.local
ipaclient2.test.local
ipaclient3.test.local
ipaclient4.test.local
```

For simple setups or in defined client environments it might not be needed to set domain or realm for the replica deployment. But it might be needed to set the master server of a client because of the topology. If this is needed, it can be set either in the `[ipaclients:vars]`section if it will apply to all the clients in the `[ipaclients]` group or it is possible to set this also per client in the `[ipaclients]` group:

```
[ipaclients]
ipaclient1.test.local ipaclient_servers=ipareplica1.test.local
ipaclient2.test.local ipaclient_servers=ipareplica1.test.local
ipaclient3.test.local ipaclient_servers=ipareplica2.test.local
ipaclient4.test.local ipaclient_servers=ipareplica2.test.local
```

If you need to set more than one server for a client (for fallbacks etc.), simply use a comma separated list for `ipaclient_servers`.

You can add settings for client deployment:

```
[ipaclients:vars]
ipaadmin_password=ADMPassword1
ipaserver_domain=test.local
ipaserver_realm=TEST.LOCAL
```

For enhanced security it is possible to use a auto-generated one-time-password (OTP). This will be generated on the controller using the (first) server. It is needed to have the Python `gssapi` bindings installed on the controller for this. To enable the generation of the one-time-password:

```
[ipaclients:vars]
ipaclient_use_otp=yes
```

For more client settings, please have a look at the [client role documentation](roles/ipaclient/README.md).

**Cluster**

If you want to deploy more than a master server at once, then it will be good to define a new group like `[ipacluster]` that contains all the other groups `[ipaserver]`, `[ipareplicas]` and `[ipaclients]`. This way it is not needed to set `domain`, `realm`, `admin password` or `dm password` for the single groups:

```
[ipacluster:children]
ipaserver
ipareplicas
ipaclients

[ipacluster:vars]
ipaadmin_password=ADMPassword1
ipadm_password=DMPassword1
ipaserver_domain=test.local
ipaserver_realm=TEST.LOCAL
```
All these settings will be available in the `[ipaserver]`, `[ipareplicas]` and `[ipaclient]` groups.

**Topology**

With this playbook it is possible to add a list of topology segments using the `ipatopologysegment` module.

```yaml
---
- name: Add topology segments
  hosts: ipaserver
  become: true
  gather_facts: false

  vars:
    ipaadmin_password: password1
    ipatopology_segments:
    - {suffix: domain, left: replica1.test.local, right: replica2.test.local}
    - {suffix: domain, left: replica2.test.local, right: replica3.test.local}
    - {suffix: domain, left: replica3.test.local, right: replica4.test.local}
    - {suffix: domain+ca, left: replica4.test.local, right: replica1.test.local}

  tasks:
  - name: Add topology segment
    ipatopologysegment:
      password: "{{ ipaadmin_password }}"
      suffix: "{{ item.suffix }}"
      name: "{{ item.name | default(omit) }}"
      left: "{{ item.left }}"
      right: "{{ item.right }}"
      #state: present
      #state: absent
      #state: checked
      state: reinitialized
    loop: "{{ ipatopology_segments | default([]) }}"
```


Example Playbooks
=================

The playbooks needed to deploy or undeploy server, replicas and clients are part of the repository and placed in the playbooks folder. There are also playbooks to deploy and undeploy clusters. With them it is only needed to add an inventory file:

```
playbooks/
        install-client.yml
        install-cluster.yml
        install-replica.yml
        install-server.yml
        uninstall-client.yml
        uninstall-cluster.yml
        uninstall-replica.yml
        uninstall-server.yml
```

Under [playbooks](playbooks/) there are also example playbooks for common tasks for each provided module.


How to deploy a master server
-----------------------------

This will deploy the master server defined in the inventory file:

```bash
ansible-playbook -v -i inventory/hosts install-server.yml
```

If Ansible vault is used for passwords, then it is needed to adapt the playbooks in this way:

```yaml
---
- name: Playbook to configure IPA servers
  hosts: ipaserver
  become: true
  vars_files:
  - playbook_sensitive_data.yml

  roles:
  - role: ipaserver
    state: present
```

It is also needed to provide the Ansible vault password file on the ansible-playbook command line:

```
ansible-playbook -v -i inventory/hosts --vault-password-file .vault_pass.txt install-server.yml
```

How to deploy a replica
-----------------------

This will deploy the replicas defined in the inventory file:

```
ansible-playbook -v -i inventory/hosts install-replica.yml
```


How to setup a client
---------------------

This will deploy the clients defined in the inventory file:

```
ansible-playbook -v -i inventory/hosts install-client.yml
```


How to deploy a cluster
-----------------------

This will deploy the server, replicas and clients defined in the inventory file:

```
ansible-playbook -v -i inventory/hosts install-cluster.yml
```
