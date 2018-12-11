#!/usr/bin/env bash

RUN_IN_PIPENV="pipenv run"

notebooks ()
{
    $RUN_IN_PIPENV jupyter notebook
}

"$@"