#!/bin/bash

docker-compose up -d

# update login for automation user to "automation:automation"
docker exec check-mk-ci bash -c "until [ -f /opt/omd/sites/cmk/var/check_mk/web/automation/automation.secret ]; do sleep 1; done; echo automation > /opt/omd/sites/cmk/var/check_mk/web/automation/automation.secret"
