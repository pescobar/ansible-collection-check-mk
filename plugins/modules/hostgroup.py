#!/usr/bin/python

# Copyright: (c) 2020, Pablo Escobar <pablo.escobarlopez@unibas.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
from datetime import datetime

from ansible_collections.pescobar.check_mk.plugins.module_utils.check_mk_api import WebApi, \
            NoNoneValueDict, WebApi, CheckMkWebApiException, CheckMkWebApiResponseException, \
            CheckMkWebApiAuthenticationException

from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: hostgroup

short_description: Administer check_mk hostgroups using the http API

version_added: "2.10"

description:
    - "Administer check_mk hostgroups using the http API"

options:
    base_url:
        description:
            - Url to access the check_mk server. e.g. http://mymonitoring-server.com/mysite
        required: true
        aliases: ['url']
        type: str

    auth_username:
        description:
            - User to login to the API
        aliases: ['username']
        required: true
        type: str

    auth_password:
        description:
            - Password to login to the API
        aliases: ['password']
        required: true
        type: str

    validate_certs:
        description:
            - Validate ssl certs?
        default: true
        type: bool

    hostgroup:
        description:
            - Name of the group to add/delete/update
        required: true
        type: str

    alias:
        description:
            - Alias for the hostgroup
        type: str

    activate_changes:
        description:
            - Should we activate the changes on execution?
        default: true
        type: bool

    state:
        description:
            - Create or delete the host?
        default: 'present'
        type: str
        choices:
            - present
            - absent

author:
    - Pablo Escobar Lopez (@pescobar)
'''

EXAMPLES = '''

- name: Add a hostgroup
  scicore.guacamole.guacamole_connection:
    base_url: http://localhost/guacamole
    auth_username: cmkadmin
    auth_password: cmkadmin
    hostgroup: group1
    alias: webservers
    state: present
'''

RETURN = '''
hostgroup_info:
    description: Information about the created or updated hostgroup
    type: dict
    returned: always
msg:
    description: Some extra info about what the module did
    type: str
    returned: always
'''


def main():

    # define the available arguments/parameters that a user can pass to the module
    module_args = dict(
        base_url=dict(type='str', aliases=['url'], required=True),
        auth_username=dict(type='str', aliases=['username'], required=True),
        auth_password=dict(type='str', aliases=['password'], required=True, no_log=True),
        validate_certs=dict(type='bool', default=True),
        hostgroup=dict(type='str', aliases=['hostname'], required=True),
        alias=dict(type='str', aliases=['alias']),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
        activate_changes=dict(type='bool', default=True)
    )

    result = dict(changed=False, msg='', hostgroup_info={})

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # login to the API
    api = WebApi(module.params.get('base_url'), \
                 username=module.params.get('auth_username'), \
                 secret=module.params.get('auth_password'))

    all_hostgroups_before = api.get_all_hostgroups()

    # check if the group already exists in check_mk
    hostgroup_exists = False
    for groupname, alias in all_hostgroups_before.items():
       if groupname == module.params.get('hostgroup'):
           hostgroup_exists = True
           break

    if module.params.get('state') == 'present':

        if hostgroup_exists:
            result['msg'] = "Group '%s' already exists" % module.params.get('hostgroup')
        else:
            api.add_hostgroup(group=module.params.get('hostgroup'), alias=module.params.get('alias'))
            result['msg'] = "hostgroup added: " + module.params.get('hostgroup')

        result['hostgroup_info']['hostgroup'] = module.params.get('hostgroup')
        result['hostgroup_info'] = api.get_hostgroup(module.params.get('hostgroup'))

    if module.params.get('state') == 'absent':

       if hostgroup_exists:
           result['hostgroup_info']['hostgroup'] = module.params.get('hostgroup')
           result['hostgroup_info'] = api.get_hostgroup(module.params.get('hostgroup'))
           api.delete_hostgroup(module.params.get('hostgroup'))
           result['msg'] = "hostgroup deleted: " + module.params.get('hostgroup')
       else:
           # the hostgroup doesn't exists so we just return a msg
           result['msg'] = "There is no hostgroup named " + module.params.get('hostgroup')

    all_hostgroups_after = api.get_all_hostgroups()

    if all_hostgroups_before != all_hostgroups_after:
        result['changed'] = True

    if module.params.get('activate_changes'):
        if result['changed']:
            api.activate_changes()

    module.exit_json(**result)


if __name__ == '__main__':
    main()
