#!/bin/bash

if ps -elf | egrep "(dagster-daemon run|dagster-webserver)$" >/dev/null
then
    echo 'Failed!'
    echo 'Check ps -elf | egrep "(dagster-daemon run|dagster-webserver -h 0.0.0.0 -p 3000)$"'
else
    # find script path
    cd /home/yc-user
    #activate virtual dagster-env
    source venv/bin/activate
    # run scheduler
    cd /home/yc-user/otus_projects
    DAGSTER_HOME=${PWD} dagster-daemon run >&1 &
    # run dagit ui -> не актуально -> DAGSTER_HOME=${PWD} dagit -h 10.26.103.210 -p 8080 >>dagit.log 2>&1 &
    DAGSTER_HOME=${PWD} dagster-webserver -h 0.0.0.0 -p 3000 >&1 &
    # deactivate virtual env
    deactivate
    # print result
    echo 'Success'
fi