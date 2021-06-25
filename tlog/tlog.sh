#! /usr/bin/env bash

# Invoke transaction log python script via its virtual env

dir=/apps/n2t/tlog

$dir/venv/bin/python $dir/bin/tlog.py "$@"
