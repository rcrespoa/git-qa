#!/bin/bash
EXECUTION_PATHS=$1
CONFIG=$2

# split PATH by comma and execute each one
for execution_path in ${EXECUTION_PATHS//,/ }
do
    if ! isort $execution_path --check-only --diff --sp $CONFIG; then
        echo "Early exit: isort exited with code != 0"
        exit 1
    fi
done

