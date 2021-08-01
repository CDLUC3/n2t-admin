#! /usr/bin/env bash

# Invoke transaction log python script via its virtual env

DIR=/apps/n2t/n2t_create/tlog

$DIR/venv/bin/python $DIR/bin/tlog.py "$@"
