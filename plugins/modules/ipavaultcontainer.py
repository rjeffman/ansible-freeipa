#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors:
#   Rafael Guterres Jeffman <rjeffman@redhat.com>
#
# Copyright (C) 2019 Red Hat
# see file 'COPYING' for use and warranty information
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {
    "metadata_version": "1.0",
    "supported_by": "community",
    "status": ["preview"],
}

DOCUMENTATION = """
---
module: ipavaultcontainer
short description: Manage vault containers.
description: Manage vault containers. KRA service must be enabled.
options:
  ipaadmin_principal:
    description: The admin principal
    default: admin
  ipaadmin_password:
    description: The admin password
    required: false
  username:
    description: Username of the user vault container.
    required: false
    type: list
  service:
    description: Service name of the service vault container.
    required: false
    type: list
  shared:
    description: Shared vault container.
    required: false
    type: bool
  users:
    description: Users members of the vault container.
    required: false
    type: list
  services:
    description: Services members of the vault container.
    required: false
    type: list
  groups:
    description: Groups members of the vault container.
    required: false
    type: list
  action:
    description: Work on vaultcontainer or member level.
    default: vault
    choices: ["vaultcontainer", "member"]
  state:
    description: State to ensure
    default: present
    choices: ["present", "absent"]
author:
    - Rafael Jeffman
"""

EXAMPLES = """
# Ensure vaultcontainer for user01 is present
- ipavaultcontainer:
    ipaadmin_password: MyPassword123
    username: user01

# Ensure vaultcontainer for user01 is present with users, groups and services.
- ipavaultcontainer:
    ipaadmin_password: MyPassword123
    username: user01
    user:
    - admin, user01, user02
    groups:
    - ipausers
    services:
    - HTTP/example.com
    action: member

# Ensure vaultcontainer is absent
- ipavaultcontainer:
    ipaadmin_password: MyPassword123
    username: user01
    state: absent

# Ensure shared vaultcontainer is present
- ipavaultcontainer:
    ipaadmin_password: MyPassword123
    shared: True

# Ensure service vaultcontainer is present
- ipavaultcontainer:
    ipaadmin_password: MyPassword123
    service: HTTP/example.com
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible.module_utils.ansible_freeipa_module import temp_kinit, \
    temp_kdestroy, valid_creds, api_connect, api_command, gen_add_del_lists, \
    api_command_no_name, module_params_get
import os
import base64


def find_vaultcontainer(module, username, service, shared):
    _args = {
        "all": True,
    }
    if username is not None:
        _args['username'] = username
    elif service is not None:
        _args['service'] = service
    else:
        _args['shared'] = shared

    try:
        _result = api_command_no_name(module, "vaultcontainer_show", _args)
    except Exception:
        return None

    if "result" in _result and len(_result["result"]) > 0:
        return _result["result"]
    else:
        return None


def gen_args(username, service, shared, users, groups, services):
    _args = {}

    if username is not None:
        _args['username'] = username
    elif service is not None:
        _args['service'] = service
    else:
        _args['shared'] = shared

    if users is not None:
        _args['user'] = users
    if groups is not None:
        _args['group'] = groups
    if services is not None:
        _args['services'] = services

    return _args


def gen_vault_args(username, service, shared):
    _args = {'ipavaulttype': 'standard'}

    if username is not None:
        _args = {'username': username}
    elif service is not None:
        _args = {'service': service}
    else:
        _args = {'shared': shared}

    # create a random name for a vault.
    _name = base64.b64encode(os.urandom(12))
    _name = _name.replace(b"+", b"").replace(b"/", b"")

    return to_text(_name), _args


def main():
    ansible_module = AnsibleModule(
        argument_spec=dict(
            # general
            ipaadmin_principal=dict(type="str", default="admin"),
            ipaadmin_password=dict(type="str", required=False, no_log=True),

            # present
            username=dict(type="str", default=None, required=False),
            service=dict(type="str", required=False, default=None),
            shared=dict(type="bool", required=False, default=None),

            users=dict(required=False, type='list', default=None),
            groups=dict(required=False, type='list', default=None),
            services=dict(required=False, type='list', default=None),

            # state
            action=dict(type="str", default="vaultcontainer",
                        choices=["vaultcontainer", "member"]),
            state=dict(type="str", default="present",
                       choices=["present", "absent"]),
        ),
        supports_check_mode=True,
        mutually_exclusive=[['username', 'service', 'shared']],
        required_one_of=[['username', 'service', 'shared']]
    )

    ansible_module._ansible_debug = True

    # Get parameters

    # general
    ipaadmin_principal = module_params_get(ansible_module,
                                           "ipaadmin_principal")
    ipaadmin_password = module_params_get(ansible_module, "ipaadmin_password")

    # present
    # The 'noqa' variables are not used here, but required for vars().
    # The use of 'noqa' ensures flake8 does not complain about them.
    username = module_params_get(ansible_module, "username")
    service = module_params_get(ansible_module, "service")
    shared = module_params_get(ansible_module, "shared")
    services = module_params_get(ansible_module, "services")
    users = module_params_get(ansible_module, "users")
    groups = module_params_get(ansible_module, "groups")

    action = module_params_get(ansible_module, "action")
    # state
    state = module_params_get(ansible_module, "state")

    # Check parameters

    if state == "present":

        invalid = []

        if action == "member":
            invalid = ['shared']

        for x in invalid:
            if x in vars() and vars()[x] is not None:
                ansible_module.fail_json(
                    msg="Argument '%s' can not be used with action "
                    "'%s'" % (x, action))

    elif state == "absent":
        invalid = []

        if action == "member":
            invalid = ['shared']

        for x in invalid:
            if vars()[x] is not None:
                ansible_module.fail_json(
                    msg="Argument '%s' can not be used with state '%s'" %
                    (x, state))

    else:
        ansible_module.fail_json(msg="Invalid state '%s'" % state)

    # Init

    changed = False
    exit_args = {}
    ccache_dir = None
    ccache_name = None
    try:
        if not valid_creds(ansible_module, ipaadmin_principal):
            ccache_dir, ccache_name = temp_kinit(ipaadmin_principal,
                                                 ipaadmin_password)
        api_connect('ansible-ipa')

        commands = []

        res_find = find_vaultcontainer(ansible_module,
                                       username, service, shared)

        # Create command
        if state == "present":
            if res_find is None:
                res_find = {}

                args = gen_args(username, service, shared,
                                users, groups, services)

                name, vault_args = gen_vault_args(username, service, shared)
                # create temporary vault to add a container.
                commands.append(["vault_add_internal", name, vault_args])
                commands.append(["vault_del", name, vault_args])

                commands.append(["vaultcontainer_add_owner", args])

            else:
                if action == "member":
                    ansible_module.warn("RES: %s" % res_find)

                    # Generate adittion and removal lists
                    user_add, user_del = \
                        gen_add_del_lists(
                            users, res_find.get('member_user', []))
                    group_add, group_del = \
                        gen_add_del_lists(
                            groups, res_find.get('member_group', []))
                    service_add, service_del = \
                        gen_add_del_lists(
                            services, res_find.get('member_service', []))

                    # Add users, groups and services
                    if len(user_add) > 0 or len(group_add) > 0 \
                       or len(service_add) > 0:
                        member_add = gen_args(username, service, shared,
                                              user_add, group_add, service_add)
                        ansible_module.warn("MEMBER_ADD: %s" % member_add)
                        commands.append(
                            ["vaultcontainer_add_owner", member_add])

                    # Remove users and groups
                    if len(user_del) > 0 or len(group_del) > 0 \
                       or len(service_del) > 0:
                        member_del = \
                            gen_args(username, service, shared,
                                     user_del, group_del, service_del)
                        ansible_module.warn("MEMBER_DEL: %s" % member_del)
                        commands.append(
                            ["vaultcontainer_remove_owner", member_del])

        elif state == "absent":
            if res_find is not None:
                if action == "vaultcontainer":
                    if username is not None:
                        args = {'username': username}
                    elif service is not None:
                        args = {'service': service}
                    else:
                        args = {'shared': shared}
                    commands.append(["vaultcontainer_del", args])

                elif action == "member":
                    # Generate args
                    member_del = gen_args(username, service, shared,
                                          users, groups, services)
                    commands.append(["vaultcontainer_remove_owner",
                                     member_del])

        # TODO: states enable and disable - rafasgj
        else:
            ansible_module.fail_json(msg="Unkown state '%s'" % state)

        # Execute commands

        errors = []
        for configuration in commands:
            try:
                if len(configuration) == 2:
                    command, args = configuration
                    result = api_command_no_name(ansible_module, command, args)
                else:
                    command, name, args = configuration
                    result = api_command(ansible_module, command, name, args)

                if "completed" in result:
                    if result["completed"] > 0:
                        changed = True
                else:
                    changed = True
            except Exception as e:
                ansible_module.fail_json(msg="%s: %s" % (command, str(e)))

            # RAFASGJ - This MUST change.
            # Get all errors
            # All "already a member" and "not a member" failures in the
            # result are ignored. All others are reported.
            if "failed" in result and len(result["failed"]) > 0:
                for item in result["failed"]:
                    failed_item = result["failed"][item]
                    for member_type in failed_item:
                        for member, failure in failed_item[member_type]:
                            if "already a member" in failure \
                               or "not a member" in failure:
                                continue
                            errors.append("%s: %s %s: %s" % (
                                command, member_type, member, failure))
        if len(errors) > 0:
            ansible_module.fail_json(msg=", ".join(errors))

    except Exception as e:
        ansible_module.fail_json(msg=str(e))

    finally:
        temp_kdestroy(ccache_dir, ccache_name)

    # Done

    ansible_module.exit_json(changed=changed, **exit_args)


if __name__ == "__main__":
    main()
