#!/usr/bin/env python

import check_mk_web_api

api = check_mk_web_api.WebApi('http://localhost:9090/cmk/check_mk/webapi.py', username='automation', secret='automation')
#api.add_host('webserver01.com')
#lala = api.get_host('webserver01.com')
#lala = api.get_all_folders()
lala = api.get_all_hostgroups()
#  print(lala)
#api.activate_changes()


hostgroup_exists = False
#for groupname in all_hostgroups_before.items():
for groupname, alias in lala.items():
  print(groupname)
  #print(alias)
  #if groupname == module.params.get('hostgroup'):
  if groupname == 'hostgroup1':
    hostgroup_exists = True
    break

print(hostgroup_exists)
