#!/usr/bin/python

# Copyright: (c) 2020, Pablo Escobar <pablo.escobarlopez@unibas.ch>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

import check_mk_web_api

from ansible.module_utils.basic import AnsibleModule
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: host

short_description: Administer check_mk hosts using the http API

version_added: "2.10"

description:
    - "Administer check_mk hosts using the http API"

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

    host_name:
        description:
            - Name of the host to add/delete/update
        required: true
        aliases: ['hostname']
        type: str

    host_folder:
        description:
            - Folder where to add the host
        aliases: ['folder']
        default: '/'
        type: str

    host_ip:
        description:
            - IP of the host
        required: true
        aliases:
          - ipaddress
        type: str

    #  host_tags:
    #      description:
    #          - Dict of tags to apply to the host
    #      aliases: ['tags']
    #      type: dict

    host_alias:
        description:
            - Alias for a host
        aliases: ['alias']
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

- name: Add a host
  scicore.guacamole.guacamole_connection:
    base_url: http://localhost/guacamole
    auth_username: cmkadmin
    auth_password: cmkadmin
    host: test_host
    state: present
'''

RETURN = '''
host_info:
    description: Information about the created or updated host
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
        host_name=dict(type='str', aliases=['hostname'], required=True),
        host_folder=dict(type='str', aliases=['folder'], default='/'),
        host_ip=dict(type='str', aliases=['ipaddress'], required=True),
        #host_tags=dict(type='dict', aliases=['tags']),
        host_alias=dict(type='str', aliases=['alias']),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
        activate_changes=dict(type='bool', default=True)
    )

    result = dict(changed=False, msg='', host_info={})

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # login to the API
    api = check_mk_web_api.WebApi(module.params.get('base_url'), username=module.params.get('auth_username'), secret=module.params.get('auth_password'))

    all_hosts_before = api.get_all_hosts()

    # check if the host already exists in check_mk
    host_exists = False
    for hostname, attributes in all_hosts_before.items():
       if hostname == module.params.get('host_name'):
           host_exists = True
           break


    if module.params.get('state') == 'present':

        if host_exists:
            # when updating/editing a host we cannot change the folder
            # if you want to change the folder you should remove/add the host
            api.edit_host(module.params.get('host_name'), ipaddress=module.params.get('host_ip'), alias=module.params.get('host_alias'))
        else:
            api.add_host(module.params.get('host_name'), folder=module.params.get('host_folder'), ipaddress=module.params.get('host_ip'), alias=module.params.get('host_alias'))


    if module.params.get('state') == 'absent':

       if host_exists:
           api.delete_host(module.params.get('host_name'))
       else:
           # the host doesn't exists so we just return a msg
           result['msg'] = "There is no host named " + module.params.get('host_name')

    module.exit_json(**result)


if __name__ == '__main__':
    main()