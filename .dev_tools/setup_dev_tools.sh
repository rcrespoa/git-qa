#!/bin/sh
SCRIPT_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
ENV_PATH=$SCRIPT_PATH/env
ROOT_PATH=$SCRIPT_PATH/..

############################################################################
# Set up main VENV
############################################################################
python3 -m venv $ENV_PATH
source $ENV_PATH/bin/activate
pip3 install -r $SCRIPT_PATH/dev-requirements.txt


# ############################################################################
# # Set up custom bash pre-commit hooks
# ############################################################################
# cat $SCRIPT_PATH/hooks/on_pre_commit_check_todo_fixme.sh >> $SCRIPT_PATH/../.git/hooks/pre-commit
# cat $SCRIPT_PATH/hooks/on_pre_commit_diff_testci.sh >> $SCRIPT_PATH/../.git/hooks/pre-commit