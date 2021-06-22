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
module: folder

short_description: Administer check_mk folders using the http API

version_added: "2.10"

description:
    - "Administer check_mk folders using the http API"

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

    folder_name:
        description:
            - Name of the folder to add/delete/update
        aliases: ['folder']
        required: true
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

- name: Create a folder in check_mk for the tenant via WATO API
  pescobar.check_mk.folder:
    base_url: "{{ check_mk_agent_monitoring_host_url }}"
    username: "{{ check_mk_agent_monitoring_host_wato_username }}"
    password: "{{ check_mk_agent_monitoring_host_wato_secret }}"
    folder_name: "{{ check_mk_agent_monitoring_host_folder }}"
    state: present
  delegate_to: localhost
  become: false

'''

RETURN = '''
folder_info:
    description: Information about the created or updated folder
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
        folder_name=dict(type='str', aliases=['hostname'], required=True),
        state=dict(type='str', choices=['absent', 'present'], default='present'),
        activate_changes=dict(type='bool', default=True)
    )

    result = dict(changed=False, msg='', folder_info={})

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # login to the API
    api = WebApi(module.params.get('base_url'), username=module.params.get('auth_username'), secret=module.params.get('auth_password'))

    all_folders_before = api.get_all_folders()

    # check if the folder already exists in check_mk
    folder_exists = False
    for folder_name, meta_data in all_folders_before.items():
       if folder_name == module.params.get('folder_name'):
           folder_exists = True
           break

    if module.params.get('state') == 'present':

        if folder_exists:
            result['msg'] = "Folder '%s' already exists" % module.params.get('folder_name')
        else:
            api.add_folder(module.params.get('folder_name'), meta_data={"created_at":datetime.today().strftime('%Y%m%d'), "created_by":"ansible"})
            result['msg'] = "Folder added: '%s'" % module.params.get('folder_name')

        result['folder_info'] = api.get_folder(module.params.get('folder_name'))
        result['folder_info']['folder_name'] = module.params.get('folder_name')

    if module.params.get('state') == 'absent':

       if folder_exists:
           result['folder_info'] = api.get_folder(module.params.get('folder_name'))
           result['folder_info']['folder_name'] = module.params.get('folder_name')
           api.delete_folder(module.params.get('folder_name'))
           result['msg'] = "Folder deleted: '%s'" % module.params.get('folder_name')
       else:
           result['msg'] = "There is no folder named '%s'" % module.params.get('folder_name')

    all_folders_after = api.get_all_folders()

    if all_folders_before != all_folders_after:
        result['changed'] = True

    if module.params.get('activate_changes'):
        if result['changed']:
            api.activate_changes()

    module.exit_json(**result)


if __name__ == '__main__':
    main()
