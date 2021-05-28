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
module: servicegroup

short_description: Administer check_mk servicegroups using the http API

version_added: "2.10"

description:
    - "Administer check_mk servicegroups using the http API"

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

    servicegroup:
        description:
            - Name of the servicegroup to add/delete/update
        required: true
        type: str

    alias:
        description:
            - Alias for the servicegroup
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

- name: Add a servicegroup
  pescobar.check_mk.servicegroup:
    base_url: http://localhost:9090/cmk
    auth_username: automation
    auth_password: automation
    servicegroup: servicegroup1
    alias: dbs
    state: present
'''

RETURN = '''
servicegroup_info:
    description: Information about the created or updated servicegroup
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
        servicegroup=dict(type='str', aliases=['hostname'], required=True),
        alias=dict(type='str'),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
        activate_changes=dict(type='bool', default=True)
    )

    result = dict(changed=False, msg='', servicegroup_info={})

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # login to the API
    api = WebApi(module.params.get('base_url'), \
                 username=module.params.get('auth_username'), \
                 secret=module.params.get('auth_password'))

    all_servicegroups_before = api.get_all_servicegroups()

    # check if the group already exists in check_mk
    servicegroup_exists = False
    for groupname, alias in all_servicegroups_before.items():
       if groupname == module.params.get('servicegroup'):
           servicegroup_exists = True
           break

    if module.params.get('state') == 'present':

        if servicegroup_exists:
            servicegroup_details = api.get_servicegroup(module.params.get('servicegroup'))
            if servicegroup_details.get('alias') != module.params.get('alias'):
                api.edit_servicegroup(group=module.params.get('servicegroup'), alias=module.params.get('alias'))
                result['msg'] = "Alias updated for servicegroup '%s'" % module.params.get('servicegroup')
            else:
                result['msg'] = "Group '%s' already exists" % module.params.get('servicegroup')
        else:
            api.add_servicegroup(group=module.params.get('servicegroup'), alias=module.params.get('alias'))
            result['msg'] = "servicegroup added: " + module.params.get('servicegroup')

        result['servicegroup_info'] = api.get_servicegroup(module.params.get('servicegroup'))
        result['servicegroup_info']['servicegroup'] = module.params.get('servicegroup')

    if module.params.get('state') == 'absent':

       if servicegroup_exists:
           result['servicegroup_info'] = api.get_servicegroup(module.params.get('servicegroup'))
           result['servicegroup_info']['servicegroup'] = module.params.get('servicegroup')
           api.delete_servicegroup(module.params.get('servicegroup'))
           result['msg'] = "servicegroup deleted: " + module.params.get('servicegroup')
       else:
           # the servicegroup doesn't exists so we just return a msg
           result['msg'] = "There is no servicegroup named " + module.params.get('servicegroup')

    all_servicegroups_after = api.get_all_servicegroups()

    if all_servicegroups_before != all_servicegroups_after:
        result['changed'] = True

    if module.params.get('activate_changes'):
        if result['changed']:
            api.activate_changes()

    module.exit_json(**result)


if __name__ == '__main__':
    main()
