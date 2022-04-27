[![Build Status](https://dev.azure.com/ansible-freeipa/ansible-freeipa/_apis/build/status/Nightly?branchName=master&label=Nightly)](https://dev.azure.com/ansible-freeipa/ansible-freeipa/_build/latest?definitionId=3&branchName=master)

FreeIPA Ansible collection
==========================

This repository contains [Ansible](https://www.ansible.com/) roles and playbooks to install and uninstall [FreeIPA](https://www.freeipa.org/) `servers`, `replicas` and `clients`, and manage FreeIPA installlations.


Key Features
------------

* [Server](/roles/ipaserver/README.md), [replica](/roles/ipareplica/README.md) and [client](/roles/ipaclient/README.md) deployment
* Server [backup and restore](/roles/ipareplica/README.md)
* User, groups, hosts and hostgroup management
* Serivce management
* HBAC and RBAC rule management
* Automount management
* IPA configuration management
* Embedded DNS nameserver management
* Sudo management
* Server and topology management
* Active Directory trust management
* Vault management

A complete least of features can be found in the [release README](/README.md).


Supported FreeIPA Versions
--------------------------

FreeIPA versions 4.6 and up are supported by all modules.

The client role supports versions 4.4 and up. The server role supports versions 4.5 and up. The replica role is requires versions 4.6 and up.

Some roles or module features or attributes may require newer versions of FreeIPA, and are reported on the role or module specific README file.


Supported Distributions
-----------------------

* RHEL/CentOS 7.4+
* Fedora 26+
* Ubuntu LTS (ipaserver and ipareplica roles only on 16.04, ipaclient on 16.04 and up)
* Debian 10+ (ipaclient only)


Requirements
------------

**Controller Node**
* Ansible version: 2.8+ (ansible-freeipa is an Ansible Collection)
* /usr/bin/kinit is required on the controller if a one time password (OTP) is used

**Target Node**
* Supported FreeIPA version (see above)
* Supported distribution (needed for package installation only, see above)


Limitations
-----------

See the [release README](/README.md) and roles and modules READMEs for current limitations.


Usage
=====

`ansible-freeipa` can be used from the git repository, installed from RPM packages (Fedora, CentOS, RHEL), or [Ansible Galaxy](https://galaxy.ansible.com).

Assuming you use Ansible 2.9 or later, install `ansible-freeipa` collection with (see the [release README](/README.md) for other installation/usage methods):

```bash
$ ansible-galaxy collection install freeipa.ansible_freeipa
```
