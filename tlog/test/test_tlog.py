#! /usr/bin/env python3

import os

# XXX use pytest builtin tmpfiles

def test_mres():
    #cmd = "PYTHONIOENCODING=utf8 "
    tfile = "test/.test1"
    cmd = ""
    cmd += "./tlog.py --when monthly 0 test/transaction_log_test "
    cmd += f"> {tfile}; diff {tfile} test/monthly_res_out"
    test = os.popen(cmd).read()
    assert test == ""
    os.popen(f"rm {tfile}")

def test_dmods():
    #cmd = "PYTHONIOENCODING=utf8 "
    tfile = "test/.test2"
    cmd = ""
    cmd = "./tlog.py --when daily --mods 0 test/transaction_log_test "
    cmd += f"> {tfile}; diff {tfile} test/daily_mods_out"
    test = os.popen(cmd).read()
    assert test == ""
    os.popen(f"rm {tfile}")

def test_diddump():
    #cmd = "PYTHONIOENCODING=utf8 "
    tfile = "test/.test3"
    cmd = ""
    cmd = "./tlog.py --iddump 0 test/transaction_log_test "
    cmd += f"> {tfile}; diff {tfile} test/daily_iddump_out"
    test = os.popen(cmd).read()
    assert test == ""
    os.popen(f"rm {tfile}")

