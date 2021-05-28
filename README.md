[![CI-tests](https://github.com/pescobar/ansible-collection-check-mk/workflows/ci-test/badge.svg)](https://github.com/pescobar/ansible-collection-check-mk/actions?query=workflow%3Aci-test)

# Ansible Collection - pescobar.check_mk

To use the ansible modules included in this collection you first need to activate the "automation" user in check_mk to interact with the API. 

Check [official check_mk docs](https://docs.checkmk.com/latest/en/wato_user.html#automation) to enable automation user for API access.

SSL certs are not verified so you can use self-signed certs.

## role pescobar.check_mk.check_mk_agent

Use this role to install and configure the check_mk agent in your machines.

Role vars:

```
# check_mk_agent_package_url: ""   # define the url to download the check_mk agent from your server
# check_mk_agent_hostname_to_register: ""  # define a custom hostname for the host to register. Default is inventory_hostname
check_mk_agent_over_ssh: true
check_mk_agent_over_xinetd: false
check_mk_agent_with_sudo: false
check_mk_agent_plugins_requirements: []
check_mk_agent_plugins: []
check_mk_agent_local_checks: {}
check_mk_agent_ssh_pubkey: ""
check_mk_agent_add_to_wato: false
check_mk_agent_monitoring_host_url: ""
check_mk_agent_monitoring_host_wato_username: ""
check_mk_agent_monitoring_host_wato_secret: ""
check_mk_agent_monitoring_host_folder: ""
```

## module pescobar.check_mk.host 

```

> PESCOBAR.CHECK_MK.HOST    (~/.ansible/collections/ansible_collections/pescobar/check_mk/plugins/modules/host.py)

        Administer check_mk hosts using the http API

OPTIONS (= is mandatory):

- activate_changes
        Should we activate the changes on execution?
        [Default: True]
        type: bool

= auth_password
        Password to login to the API
        (Aliases: password)
        type: str

= auth_username
        User to login to the API
        (Aliases: username)
        type: str

= base_url
        Url to access the check_mk server. e.g. http://mymonitoring-
        server.com/mysite
        (Aliases: url)
        type: str

- discover_services
        Should we discover services in added host?
        [Default: True]
        type: bool

- host_alias
        Alias for a host
        (Aliases: alias)[Default: (null)]
        type: str

- host_folder
        Folder where to add the host
        (Aliases: folder)[Default: /]
        type: str

- host_ip
        IP of the host
        (Aliases: ipaddress)[Default: (null)]
        type: str

= host_name
        Name of the host to add/delete/update
        (Aliases: hostname)
        type: str

- host_tags
        Dict of tags to apply to the host (NOT IMPLEMENTED YET)
        (Aliases: tags)[Default: (null)]
        type: dict

- state
        Create or delete the host?
        (Choices: present, absent)[Default: present]
        type: str

- validate_certs
        Validate ssl certs?
        [Default: True]
        type: bool


AUTHOR: Pablo Escobar Lopez (@pescobar)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community


VERSION_ADDED_COLLECTION: pescobar.check_mk

EXAMPLES:

- name: Add host to check_mk instance via WATO API
  pescobar.check_mk.host:
    base_url: "{{ check_mk_agent_monitoring_host_url }}"
    username: "{{ check_mk_agent_monitoring_host_wato_username }}"
    password: "{{ check_mk_agent_monitoring_host_wato_secret }}"
    hostname: "{{ check_mk_agent_hostname_to_register | default(inventory_hostname) }}"
    folder: "{{ check_mk_agent_monitoring_host_folder }}"
    state: present
  delegate_to: localhost
  become: false


RETURN VALUES:
- host_info
        Information about the created or updated host

        returned: always
        type: dict

- msg
        Some extra info about what the module did

        returned: always
        type: str
```

## module pescobar.check_mk.folder

```
> PESCOBAR.CHECK_MK.FOLDER    (~/.ansible/collections/ansible_collections/pescobar/check_mk/plugins/modules/folder.py)

        Administer check_mk folders using the http API

OPTIONS (= is mandatory):

- activate_changes
        Should we activate the changes on execution?
        [Default: True]
        type: bool

= auth_password
        Password to login to the API
        (Aliases: password)
        type: str

= auth_username
        User to login to the API
        (Aliases: username)
        type: str

= base_url
        Url to access the check_mk server. e.g. http://mymonitoring-
        server.com/mysite
        (Aliases: url)
        type: str

= folder_name
        Name of the folder to add/delete/update
        (Aliases: folder)
        type: str

- state
        Create or delete the host?
        (Choices: present, absent)[Default: present]
        type: str

- validate_certs
        Validate ssl certs?
        [Default: True]
        type: bool


AUTHOR: Pablo Escobar Lopez (@pescobar)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community


VERSION_ADDED_COLLECTION: pescobar.check_mk

EXAMPLES:

- name: Create a folder in check_mk for the tenant via WATO API
  pescobar.check_mk.folder:
    base_url: "{{ check_mk_agent_monitoring_host_url }}"
    username: "{{ check_mk_agent_monitoring_host_wato_username }}"
    password: "{{ check_mk_agent_monitoring_host_wato_secret }}"
    folder_name: "{{ check_mk_agent_monitoring_host_folder }}"
    state: present
  delegate_to: localhost
  become: false


RETURN VALUES:
- folder_info
        Information about the created or updated folder

        returned: always
        type: dict

- msg
        Some extra info about what the module did

        returned: always
        type: str
```

## module pescobar.check_mk.hostgroup

```
> PESCOBAR.CHECK_MK.HOSTGROUP    (~/.ansible/collections/ansible_collections/pescobar/check_mk/plugins/modules/hostgroup.py)

        Administer check_mk hostgroups using the http API

OPTIONS (= is mandatory):

- activate_changes
        Should we activate the changes on execution?
        [Default: True]
        type: bool

- alias
        Alias for the hostgroup
        [Default: (null)]
        type: str

= auth_password
        Password to login to the API
        (Aliases: password)
        type: str

= auth_username
        User to login to the API
        (Aliases: username)
        type: str

= base_url
        Url to access the check_mk server. e.g. http://mymonitoring-
        server.com/mysite
        (Aliases: url)
        type: str

= hostgroup
        Name of the group to add/delete/update

        type: str

- state
        Create or delete the host?
        (Choices: present, absent)[Default: present]
        type: str

- validate_certs
        Validate ssl certs?
        [Default: True]
        type: bool


AUTHOR: Pablo Escobar Lopez (@pescobar)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community


VERSION_ADDED_COLLECTION: pescobar.check_mk

EXAMPLES:

- name: Create a hostgroup in check_mk for the tenant via WATO API
  pescobar.check_mk.hostgroup:
    base_url: "{{ check_mk_agent_monitoring_host_url }}"
    username: "{{ check_mk_agent_monitoring_host_wato_username }}"
    password: "{{ check_mk_agent_monitoring_host_wato_secret }}"
    hostgroup: "new_hostgroup"
    state: present
  delegate_to: localhost
  become: false


RETURN VALUES:
- hostgroup_info
        Information about the created or updated hostgroup

        returned: always
        type: dict

- msg
        Some extra info about what the module did

        returned: always
        type: str
```

## module pescobar.check_mk.servicegroup

```
> PESCOBAR.CHECK_MK.HOST    (~/.ansible/collections/ansible_collections/pescobar/check_mk/plugins/modules/host.py)

        Administer check_mk hosts using the http API

OPTIONS (= is mandatory):

- activate_changes
        Should we activate the changes on execution?
        [Default: True]
        type: bool

= auth_password
        Password to login to the API
        (Aliases: password)
        type: str

= auth_username
        User to login to the API
        (Aliases: username)
        type: str

= base_url
        Url to access the check_mk server. e.g. http://mymonitoring-
        server.com/mysite
        (Aliases: url)
        type: str

- discover_services
        Should we discover services in added host?
        [Default: True]
        type: bool

- host_alias
        Alias for a host
        (Aliases: alias)[Default: (null)]
        type: str

- host_folder
        Folder where to add the host
        (Aliases: folder)[Default: /]
        type: str

- host_ip
        IP of the host
        (Aliases: ipaddress)[Default: (null)]
        type: str

= host_name
        Name of the host to add/delete/update
        (Aliases: hostname)
        type: str

- host_tags
        Dict of tags to apply to the host (NOT IMPLEMENTED YET)
        (Aliases: tags)[Default: (null)]
        type: dict

- state
        Create or delete the host?
        (Choices: present, absent)[Default: present]
        type: str

- validate_certs
        Validate ssl certs?
        [Default: True]
        type: bool


AUTHOR: Pablo Escobar Lopez (@pescobar)

METADATA:
  metadata_version: '1.1'
  status:
  - preview
  supported_by: community


VERSION_ADDED_COLLECTION: pescobar.check_mk

EXAMPLES:

- name: Add host to check_mk instance via WATO API
  pescobar.check_mk.host:
    base_url: "{{ check_mk_agent_monitoring_host_url }}"
    username: "{{ check_mk_agent_monitoring_host_wato_username }}"
    password: "{{ check_mk_agent_monitoring_host_wato_secret }}"
    hostname: "{{ check_mk_agent_hostname_to_register | default(inventory_hostname) }}"
    folder: "{{ check_mk_agent_monitoring_host_folder }}"
    state: present
  delegate_to: localhost
  become: false


RETURN VALUES:
- host_info
        Information about the created or updated host

        returned: always
        type: dict

- msg
        Some extra info about what the module did

        returned: always
        type: str
```
