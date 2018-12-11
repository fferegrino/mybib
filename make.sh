#!/usr/bin/env bash

RUN_IN_PIPENV="pipenv run"

notebooks ()
{
    $RUN_IN_PIPENV jupyter notebook
}

app ()
{
    export FLASK_APP=mybib/web/app.py
    $RUN_IN_PIPENV flask run
}

"$@"