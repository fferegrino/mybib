#!/usr/bin/env bash

RUN_IN_PIPENV="pipenv run"

notebooks ()
{
    $RUN_IN_PIPENV jupyter notebook
}

test () {
    $RUN_IN_PIPENV pytest -vvv
}

app () {
    export PYTHONPATH=$PWD
    $RUN_IN_PIPENV gunicorn --chdir mybib/web --reload app:app
}

"$@"