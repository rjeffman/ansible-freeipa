#!/bin/bash

topdir=`dirname $(dirname $0)`

echo "Running 'flake8'."
flake8 .
echo "Running 'pydocstyle'."
pydocstyle .

ANSIBLE_LIBRARY=${ANSIBLE_LIBRARY:-"${topdir}/plugins/modules"}
ANSIBLE_MODULE_UTILS=${ANSIBLE_MODULE_UTILS:-"${topdir}/plugins/module_utils"}

export ANSIBLE_LIBRARY ANSIBLE_MODULE_UTILS

yaml_dirs=(
    "${topdir}/tests/*.yml"
    "${topdir}/tests/*/*.yml"
    "${topdir}/tests/*/*/*.yml"
    "${topdir}/playbooks/*.yml"
    "${topdir}/playbooks/*/*.yml"
    "${topdir}/molecule/*/*.yml"
    "${topdir}/molecule/*/*/*.yml"
    "${topdir}/roles/*/*/*.yml"
)

echo "Missing file warnings are expected and can be ignored."

echo "Running 'ansible-lint'."
ansible-lint --force-color ${yaml_dirs[@]}

echo "Running 'yamllint'."
yamllint -f colored ${yaml_dirs[@]}
