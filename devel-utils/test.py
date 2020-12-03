#!/usr/bin/env python

import check_mk_web_api

api = check_mk_web_api.WebApi('http://localhost:9090/cmk/check_mk/webapi.py', username='automation', secret='automation')
#api.add_host('webserver01.com')
lala = api.get_host('webserver01.com')
#lala = api.get_all_folders()
print(lala)
#api.activate_changes()
