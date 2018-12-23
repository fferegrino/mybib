#!/usr/bin/env bash

RUN_IN_PIPENV="pipenv run"

notebooks ()
{
    $RUN_IN_PIPENV jupyter notebook
}

app () {
    export PYTHONPATH=$PWD
    $RUN_IN_PIPENV gunicorn --chdir mybib/web app:app
}

"$@"