#!/bin/bash

if ps -elf | egrep "(dagster-daemon run|dagster-webserver)$" >/dev/null
then
    echo 'Failed!'
    echo 'Check ps -elf | egrep "(dagster-daemon run|dagster-webserver -h 10.26.103.210 -p 8080)$"'
else
    # find script path
    SCRIPT=$(readlink -f "$0")
    SCRIPTPATH=$(dirname "$SCRIPT")
    cd $SCRIPTPATH
    #activate virtual dagster-env
    . dagster-env/Scripts/activate
    # run scheduler
    DAGSTER_HOME=${PWD} dagster-daemon run >>daemon.log 2>&1 &
    # run dagit ui -> не актуально -> DAGSTER_HOME=${PWD} dagit -h 10.26.103.210 -p 8080 >>dagit.log 2>&1 &
    DAGSTER_HOME=${PWD} dagster-webserver -h 10.26.103.210 -p 8080 >>dagit.log 2>&1 &
    # deactivate virtual env
    deactivate
    # print result
    echo 'Success'
fi