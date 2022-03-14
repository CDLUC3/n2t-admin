#! /usr/bin/env python3

# make sure stdout and stderr are encoded for utf8

# XXX add count of days and average stats per day

import sys, codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# XXX add 99152/h (N) and 99152/p0 (E) and 99152/t3 (N) counts
# XXX add 99166/w6? (N) counts

# This next becomes the __doc__ docstring, available to help(...).
# It also prints under -h due to epilog attribute given to argparse.
"""
Assumptions: all file args given on command line will be all the files
needed, in the correct order, to count resolutions or to generate ids
that don't correspond to resolutions. CALLER IS RESPONSIBLE for the
completeness and ordering of files on command line, eg,

   $ tlog non-res Start transaction_log.2020.06.0{7,8} transaction_log

to print all ids and operations since Start time.
"""

# XXX filter out internal tests and rchecks and z_prefixes tests
# do PYTHONIOENCODING=utf8 before running
# eg, PYTHONIOENCODING=utf8 ./tlog.py transaction_log.201* > y3

from datetime import datetime, timedelta, date, time

def count_operations(file):
    """
    (A numpydoc-like description docstring.)

    Parameters
    ----------
    file : filename
        an input file in eggnog transaction log format

    Returns
    -------
    string
        time string for last log entry tread

    Raises
    ------
    ValueError?
        bad parameters

    Process a transaction log file and produce counts of various
    categories of incoming resolution requests.
    """

    # Partials
    global schemes, naans, naan_class, arks, dois
    global nonmatchcnt, matchcnt, testcnt

    # Totals
    global Tschemes, Tnaans, Tnaan_class, Tarks, Tdois
    global Tnonmatchcnt, Tmatchcnt, Ttestcnt, Tlinecnt, Tpre_start_linecnt
    global Terrlinecnt 
    global starttime, reporttime, endtime
    global tidark1, tiddoi1, tiddoi2, arkclass, doiclass

    # compiled regex's
    global Rres, Rnaan, Rinternal_api, Rinternal_res, Rmods

    started = False
    somefile = "<somefile>"
    phphack = "<phphack>"

    # specify newline else ^M in log will terminate the line
    # with open(file, newline="\n", encoding="latin1") as input:
    with open(file, newline="\n", encoding="latin1") as input:
        linecnt = 0
        errlinecnt = 0
        skip_rest = False
        for line in input:
            # skip rest of input if we're past time we're supposed to end
            if skip_rest:
                continue
            linecnt += 1
            try:
                populator, origin, time, txnid, rest = line.split(
                    sep=" ", maxsplit=4
                )
                # Do a couple very quick input checks. Time should look like
                #   2021.01.10_12:26:53.867470    
                if populator == "":
                    raise ValueError(f"line begins with a SPACE")
                if not (time[0] in [ "2", "1" ] and len(time) == 26):
                    raise ValueError(f"not a TEMPER time value")

            except Exception as exc:
                print(
                    f"ERROR: malformed log line in {file},",
                    f"line {linecnt}, {exc}\nSkipping: {line}",
                    end="",             # already ends in newline
                    #file=sys.stderr,
                )
                errlinecnt += 1
                continue

            # XXX extract txn id too, which should leave a smaller "rest" that
            # you can re.match() against (instead of re.search()

            if not started:
                # if time < "2017.12.25_00:00:01.330":
                if starttime == "0":
                    starttime = time    # initialize starttime from first log line
                if starttime and not reporttime:
                    reporttime = next_report(starttime, args.when)
                if starttime > reporttime:
                    raise ValueError(f"starttime {starttime} > reporttime {reporttime}")

                if time < starttime:
                    continue
                else:
                    started = True
                    Tpre_start_linecnt += linecnt - 1
                    if args.verbose and linecnt > 1:
                        print(
                            f"Starting time trigger {time} found in file",
                            f'"{file}"at line {linecnt:,d}',
                        )

            # if time >= "2017.12.25_00:00:08":
            if time >= reporttime:
                if args.verbose:
                    print(
                        f"Reporting time trigger {reporttime}",
                        f"found at line {linecnt:,d}",
                    )
                report_subtotals(time)
                flush_subtotals()
                if args.verbose:
                    print(f"... report {reporttime}", file=sys.stderr)
                if time >= endtime:
                    skip_rest = True
                    continue
                starttime = time
                reporttime = next_report(starttime, args.when)

            # start real business of collecting counts
            rest = rest.rstrip()        # strip line-ending
            m = re.match(Rres, rest) if Rres else None
            if not m:   # if not counting resolution or not this line...
                nonmatchcnt += 1    # yyy really means: "not resolution"
                # r"BEGIN (\S*)\.(\w+)\b"
                m = re.match(Rmods, rest) if Rmods else None
                if not m:   # if not counting mods or not this line...
                    continue            # restart loop

                ##### --mods code #####
                op = m.group(2)
                #print(f"++ {m.group(2):6s} {m.group(1)}")
                #NB: inconsistent eggnog log format for ids and elements:
                # (1) <id>|<elem>.set     vs    (2) <id>.rm <elem>
                id = m.group(1)
                id_end = id.rfind("|")
                if id_end > 0:          # case (1)
                    id = id[0:id_end]   # drop element name
                # yyy keep (for now?) internal test stuff since there's
                # not much of it
                if not m.group(2):      # yyy collect element names too?
                    print(f"no element for {id}")
                ops[op] = ops.get(op, 0) + 1
                ids[id] = ids.get(id, 0) + 1
                if id.startswith(arkclass):
                    testids[arkclass] = testids.get(arkclass, 0) + 1
                    if id.startswith(tidark1):
                        testids[tidark1] = testids.get(tidark1, 0) + 1
                    elif id.startswith(tiddoi1):    # DOI as shadow ARK
                        testids[tiddoi1] = testids.get(tiddoi1, 0) + 1
                elif id.startswith(doiclass):
                    testids[doiclass] = testids.get(doiclass, 0) + 1
                    if id.startswith(tiddoi2):
                        testids[tiddoi2] = testids.get(tiddoi2, 0) + 1
                else:
                    testids["noclass"] = testids.get("noclass", 0) + 1

                # Listing set members in order of probable frequence,
                # hoping but not knowing if that will speed things up
                if op in {"set", "purge", "rm", "add", "del", "let"}:
                    # yyy are there other ops that modify?
                    modified[f"{populator} {id}"] = True
                continue                # restart loop
            # fi: no fall-through - only way out of this "if" is via continue

            ##### --res code #####
            # if we get here, we're dealing with a resolution request
            matchcnt += 1
            if ".php" in rest:  # not much interested in hacks
                schemes[phphack] = schemes.get(phphack, 0) + 1
                continue  # restart loop
            if "!ra=127.0.0.1" in rest:  # skip internal use or testing
                testcnt += 1
                continue
            scheme = m.group(1)
            postscheme = m.group(2)  # usually ":" + rest
            naan = m.group(3)
            blade = m.group(4)
            if not postscheme.startswith(":"):
                schemes[somefile] = schemes.get(somefile, 0) + 1
                if postscheme.startswith("ark") or postscheme.startswith("doi"):
                    print("XXX no colon ark or doi")
                continue  # restart loop
            # yyy didn't we already check for .php above?
            if ".php" in blade or ".php" in postscheme:
                schemes[phphack] = schemes.get(phphack, 0) + 1
            else:
                schemes[scheme] = schemes.get(scheme, 0) + 1
            if not scheme == "ark" and not scheme == "doi":
                continue  # restart loop
            # if ark or doi, we stay and collect some more info
            schnaan = scheme + ":" + naan
            naans[schnaan] = naans.get(schnaan, 0) + 1
            # yyy not counting EZID DOI customers
            class_letter = naan_reg.get(naan, "D")[0]  # DOI or shadow ARK?
            naan_class[class_letter] = naan_class.get(class_letter, 0) + 1
        # end for line in input loop
    # end with open

    Tlinecnt += linecnt  # update total line count
    Terrlinecnt += errlinecnt  # update total error line count
    if not time >= starttime:
        print(f"Starttime not found: {starttime}")
        print(f"Latest time found:   {time}")
        return ""
    return time

def report_subtotals(time):

    # Partials
    global schemes, naans, naan_class, arks, dois
    global nonmatchcnt, matchcnt, testcnt
    global ids, ops, testids, modified

    # Totals
    global Tschemes, Tnaans, Tnaan_class, Tarks, Tdois
    global Tnonmatchcnt, Tmatchcnt, Ttestcnt
    global Tids, Tops, Ttestids, Tmodified

    global starttime, reporttime

    report_out(
        starttime,
        time,
        reporttime,
        schemes=schemes,
        naans=naans,
        naan_class=naan_class,
        testcnt=testcnt,
        matchcnt=matchcnt,
        nonmatchcnt=nonmatchcnt,
        ids=ids,
        ops=ops,
        testids=testids,
        modified=modified,
    )

#def report_and_reset(time):
def flush_subtotals():

    # Partials
    global schemes, naans, naan_class, arks, dois
    global nonmatchcnt, matchcnt, testcnt
    global ids, ops, testids, modified

    # Totals
    global Tschemes, Tnaans, Tnaan_class, Tarks, Tdois
    global Tnonmatchcnt, Tmatchcnt, Ttestcnt
    global Tids, Tops, Ttestids, Tmodified

    # Now update overall totals
    for k, v in schemes.items():
        Tschemes[k] = Tschemes.get(k, 0) + v
    for k, v in naans.items():
        Tnaans[k] = Tnaans.get(k, 0) + v
    for k, v in naan_class.items():
        Tnaan_class[k] = Tnaan_class.get(k, 0) + v
    for k, v in ids.items():
        Tids[k] = Tids.get(k, 0) + v
    for k, v in ops.items():
        Tops[k] = Tops.get(k, 0) + v
    for k, v in testids.items():
        Ttestids[k] = Ttestids.get(k, 0) + v
    for k, v in modified.items():
        Tmodified[k] = Tmodified.get(k, 0) + v
    #    Tarks = {}
    #    Tdois = {}
    Tnonmatchcnt += nonmatchcnt
    Tmatchcnt += matchcnt
    Ttestcnt += testcnt

    # Now re-set local counters
    schemes.clear()
    naans.clear()
    naan_class.clear()
    nonmatchcnt = 0
    matchcnt = 0
    testcnt = 0
    ids.clear()
    ops.clear()
    testids.clear()
    modified.clear()

    return matchcnt

def report_out(
    starttime,
    time,
    reporttime,
    schemes=None,
    naans=None,
    naan_class=None,
    testcnt=None,
    matchcnt=None,
    nonmatchcnt=None,
    ids=None,
    ops=None,
    testids=None,
    modified=None,
):
    """
    Parameters

    Returns
        xxx
    """

    print(f"# ======== {starttime} to {reporttime}")
    if time and time < reporttime and not args.iddump:
        print(f"      * Log end at {time}")

    if args.res:
        # xxx see str.replace(old, new[, count])
        print("== schemes:", len(schemes))
        #n = 0
        for k, v in sorted(
            schemes.items(), key=lambda item: item[1], reverse=True
        ):
            orgname = prefix_reg.get(k)
            if not orgname:
                orgname = "not registered"
            print(f"{v:12,d} {orgname[:55]}  {k}")
            #print(f"{v:12,d} {k}")
            #n += 1
        #print("== schemes encountered: ", n)
        # XXX need to check in with more than EBI prefixes -- do entire
        #     prefixes.yaml file!
        # XXX schemes are semi-opaque&should be looked up and reported just like NAANs

        print("== naans")
        n = 0
        n_of_interest = 10
        for k, v in sorted(
            naans.items(), key=lambda item: item[1], reverse=True
        ):
            #orgname = ""
            # if v > n_of_interest:    # maybe do something different
            m = re.match(Rnaan, k)
            # XXX redo this w.o. regex?
            lookup = m.group(1) if m else k
            orgname = naan_reg.get(lookup)
            if not orgname:
                orgname = "not registered"
            i = orgname.find(" (=)")
            if i != -1:
                orgname = orgname[:i]
            # need PYTHONIOENCODING=utf8 for this next
            print(f"{v:12,d} {orgname[:55]}  {k}")
            n += 1

        print("== naan classes (E=ezid ARK, N=non-ezid ARK, D=DOI or shadow ARK)")
        for k, v in sorted(
            naan_class.items(), key=lambda item: item[1], reverse=True
        ):
            print(f"{v:12,d} {k}")
    # fi args.res:

    if args.mods:
        # ops, ids, testids, modified
        print("== ops")
        n = 0
        for k, v in sorted(ops.items(), key=lambda item: item[1], reverse=True):
            print(f"{v:13,d} {k}")
            n += 1
        print(f"== ops encountered: {n:13,d}")

        print("== ids")
        # yyy these ids are mostly counted already under "modified",
        #     so we don't bother to print mostly uninteresting output
        #n = 0
        #for k, v in sorted(ids.items(), key=lambda item: item[1], reverse=True):
        #    # print(f"{v:13,d} {k}")   
        #    n += 1
        #print(f"== ids encountered: {n:13,d}")
        print(f"== ids encountered: {len(ids):13,d}")

        print("== testid classes")
        n = 0
        for k, v in sorted(
            testids.items(), key=lambda item: item[1], reverse=True
        ):
            print(f"{v:13,d} {k}")
            n += 1
        print(f"== testid classes encountered: {n:13,d}")

        print("== ids modified")
        print("   sorted to optimize btree insertion time")
        n = 0
        for k, v in sorted(modified.items()):
            print(f"+=mod== {k}")  # +=mod== makes it more grep-able
            n += 1
        print(f"== ids modified: {n:13,d}")
    # fi args.mods:

    if args.iddump:
        n = 0
        for k, v in sorted(modified.items()):
            print("", k)
            n += 1
        # all data lines starts with one " " (due to "" + "," in print)
        # all comment lines start with "#"
        print(f"# operations:", end="")
        for k, v in sorted(ops.items(), key=lambda item: item[1], reverse=True):
            print(f" {v}.{k}", end="")
        print()
        print(f"# report end time: {reporttime}")
        print(f"# {n:6d} mods from {starttime} to {reporttime}")
        print(f"# next harvest: {reporttime} -")
    # fi args.iddump:

    if args.iddump:
        return matchcnt         # return before printing more
    print(f"         internal testing lines {testcnt:13d}")
    print(f"               resolution lines {matchcnt:13d}")
    if nonmatchcnt > 0:
        print(f"           non-resolution lines {nonmatchcnt:13d}")
    # print(f"   sum of above numbers {testcnt + matchcnt + nonmatchcnt:9d}")
    return matchcnt

# if time >= "2017.12.25_00:00:08":
# assume report each month

def next_report(starttime, when):

    """
    starttime is 0 or a formatted TEMPER-style datetime string
    if 0, caller says start with first time found in first log file,
    so we return 0 for now expected caller will try again later

    For daily reporting we need to compute a TEMPER-style string for the
    next day, and we use python datetime so we don't have to know the
    number of days in each month (and increment the month and year).
    With a python datetime string we can do a +1 day delta operation
    and then convert it back. Unfortunately, we can't do that for
    +1 month, so we do it manually.
    """

    if not starttime:
        return ""
    if when == "end":
        global end_of_time
        return end_of_time

    year, month, rest = starttime.split(sep=".", maxsplit=2)

    day, rest = rest.split(sep="_", maxsplit=1)

    # if not daily:  # int(month)-1+1 adds 1 to range 0-11
    if when == "monthly":  # int(month)-1+1 adds 1 to range 0-11
        m = (int(month) % 12) + 1  # finally add 1 to get human month
        y = int(year) + (1 if m == 1 else 0)
        return f"{y}.{m:02}"

    # If here, when == "daily"
    pysdate = date(int(year), int(month), int(day))
    pyrdate = pysdate + timedelta(days=1)
    # interval = if daily timedelta(days=1) else timedelta(months=1)
    return f"{pyrdate.year}.{pyrdate.month:02}.{pyrdate.day:02}"


# MAIN

# some constants
home = "/apps/n2t"
tlogdir = home + "/n2t_create/tlog"
n2tlog = home + "/sv/cur/apache2/logs/transaction_log"
tmplog = "/tmp/tltail"

start_of_time = "1900"
end_of_time = "9999.12.31"

import argparse

parser = argparse.ArgumentParser(
    description="Process transaction logs.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=__doc__,
)
parser.add_argument(
    "starttime",
    metavar="Starttime",
    help="Start time for report, either 0 to start from the beginning "
    "or a format like 2017.12.25_00:00:01.330876 including any initial "
    "substring, eg, 2018.02; use '-' as shorthand for beginning of the "
    "current day",
)
parser.add_argument(
    "files",
    metavar="File",
    nargs="+",
    help=f"""Transaction log files. Use '-' as shorthand for the current
    N2T transaction_log "set", which includes the active log ({n2tlog})
    and older versions having the same name but with dated extensions of
    the form '.YYYY.MM.DD' (containing transactions up to but not
    including any beyond the day given by YYYY.MM.DD). The set is the
    latest chronological sequence of log files that includes the
    Starttime. For example, "tlog --iddump 2019.12.25_00:00:01.330876 -"
    will process a sequence of files, the first of which has the latest
    dated extension that is earlier than or equal to 2019.12.25.  As a
    kludge, use '-N' to process the last N lines of the active log file,
    eg, "tlog --iddump - -200" """,
)
parser.add_argument(
    "--mods", action="store_true", help="Report ids modified",
)
parser.add_argument(
    "--iddump", action="store_true",
    help="Report ids modified, but using format for input to 'egg iddump'",
)
parser.add_argument(
    "--res", action="store_true", help="Report resolutions (default)",
)
parser.add_argument(
    "--when",
    action="store",
    default="end",
    choices=["daily", "monthly", "end"],
    help="Report frequency (default: end)",
)
parser.add_argument(
    "--endtime",
    action="store",
    default=end_of_time,
    help=f"Stop counting after this time (default: {end_of_time})",
)
parser.add_argument(  # xxx deprecate
    "--daily",
    action="store_true",
    help="Report resolutions daily instead of monthly",
)
parser.add_argument(
    "-v", "--verbose", action="store_true", help="Be more verbose",
)
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
# when=daily, monthly, end
# what=res, mods

args = parser.parse_args()

import csv

# In this section we read several files that help us map shorter names into more
# descriptive names: for NAANs, shoulders, and prefixes

# Define naan_reg dict to identify NAANs and DOI Prefixes
# yyy need makefile to harvest updates to naan_table.txt
# XXX need to add master_shoulders.txt info

with open(tlogdir + "/naan_table.txt", encoding="utf-8") as infile:
    reader = csv.reader(infile, delimiter="\t")
    # naan_reg = {row[0]: f"{row[2][0]} {row[1]}" for row in reader}
    naan_reg = {}
    for row in reader:
        type = row[2][0]
        if type != "E":
            type = "N"  # "N" means "not E"
        naan_reg[row[0]] = f"{type} {row[1]}"

with open(tlogdir + "/doi_naans.txt", encoding="utf-8") as infile:
    reader = csv.reader(infile, delimiter="\t")
    shoulder_reg = {}
    for row in reader:
        # print(f"row[0] is {row[0]}")
        # fqshoulder = row[0]
        # naan, shoulder = fqshoulder.split(sep="/", maxsplit=1)
        naan, shoulder = row[0].split(sep="/", maxsplit=1)
        type = row[2][0]
        if type != "E":
            type = "N"  # like above

        # Register shoulder, eg, E doi:10.1234/X5 or E ark:b1234/x5
        # yyy not currently using this shoulder_reg hash
        shoulder_reg[row[0]] = f"{type} {row[1]}"

        if naan not in naan_reg:  # add missing Prefixes-as-NAANs
            # NB: only first shoulder's NAAN gets recorded
            naan_reg[naan] = f"{type} {naan}"

import re

with open(tlogdir + "/prefixes.txt", encoding="utf-8") as infile:
    reader = csv.reader(infile, delimiter="\t")
    # prefix \t longname \t alias \t synonym
    # 0         1            2        3
    prefix_reg = {}
    alias_reg = {}
    for row in reader:
        # naan, shoulder = fqshoulder.split(sep="/", maxsplit=1)
        # from granvl output (see makefile)
        # "alias: x" means whenever you find :: going forward, as all or the
        # tail of a prefix, generate an extra key with :: replaced by x and
        # give it "name" as value.
        # "synonym(for): y" means do one-time lookup of y and assign its
        # name as value of ::

        extprefix, longname, alias, synonym = row
        # if it has a name field, assign it now to extprefix (prefix
        # with any extension it might have)
        if longname:   
            prefix_reg[extprefix] = longname   
        elif synonym:   # if it is a synonym, use its name, eg, xyz/pdb syn: pdb
            prefix_reg[extprefix] = prefix_reg[synonym]
            # kludge Z for synonym case bug: take pure prefix, see if it's
            # aliased, and register it too
            m = re.search(r"([^/]+)$", extprefix)
            if not m:
                print(f'Error: bad prefix {extprefix}', file=sys.stderr)
                exit(1)
            a = alias_reg.get(m.group(1), "")
            if a:
                newkey = re.sub(r"[^/]+$", a, extprefix)
                prefix_reg[newkey] = longname

        # if there's an alias (just 1? yyy), eg, alias pmid for pubmed,
        # we will take it as an alternate pure prefix (no provider code) and
        # generate a new key from the current key, replacing the prefix (not
        # provider code with the alias, and assigning it the same longname
        if alias:  
            # kludge Z reverse map to fix missing alias from first synonym
            alias_reg[extprefix] = alias
            # in newkey we replace prefix (not pcode) with the alias
            newkey = re.sub(r"[^/]+$", alias, extprefix)
            prefix_reg[newkey] = longname
    #for k, v in prefix_reg.items():
    #    print("XXX k", k, v)
    #exit(1)

# ./tlog.py 2017.12.25_00:00:01.330 transaction_log.2017.12.31
# /apps/n2t/sv/cv2/apache2/logs/transaction_log.2018.*
# /apps/n2t/sv/cv2/apache2/logs/transaction_log.2019.*
# /apps/n2t/sv/cv2/apache2/logs/transaction_log.2020.*

# log traces from internal use and testing
# ezid ids-n2t2-stg 2020.05.08_18:33:27.971308 wAIuFZWR6hGVghXGey~1qg BEGIN resolve e/prefix_overview !!!pr=http!!!ac=*/*!!!ff=!!!ra=127.0.0.1!!!co=!!!re=!!!ua=Wget/1.14 (linux-gnu)!!!
# xref 127.0.0.1 2020.05.08_18:33:30.994976 Il77FpWR6hGJhx6Yey~1qg BEGIN doi:10.5072/EOITEST|_t.set https://crossref.org/
# oca 172.30.5.148 2017.12.25_00:00:16.611367 iu3fpEnp5xG2vpGHYSA6uQ BEGIN ark:/13960/t26b3j87c|_t.set
# oca 172.30.5.148 2017.12.25_00:00:16.611367 iu3fpEnp5xG2vpGHYSA6uQ BEGIN ark:/13960/t26b3j87c.rm _t
# ezid 172.30.32.230 2020.07.27_08:47:13.262534 lGV3cCDQ6hGjli8TQYxKWg BEGIN doi:10.7272/Q65M63XF|_t.set http://datadryad.org/stash/dataset/doi:10.7272/Q65M63XF
# +n2t ids-n2t-prd-2a 2020.08.10_00:00:49.564981 ihfmONfa6hGY7dvcywAfZQ BEGIN resolve ark:/65666/v1/12609 !!!pr=https!!!ac=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8!!!ff=!!!ra=172.30.32.230!!!co=!!!re=https://www.google.com/url?q=https%3A%2F%2Fn2t.net%2Fark%3A%2F65666%2Fv1%2F12609&sa=D&sntz=1&usg=AFQjCNHSNqxWdbU0HdWbzvRMerIdaetDLA!!!ua=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0!!!
# +n2t ids-n2t-prd-2a 2020.08.10_00:00:49.565682 ihfmONfa6hGY7dvcywAfZQ END SUCCESS ark:/65666/v1/12609 (ark:/65666/v1/12609) PFX ark:/65666 -> redir302 https://edl.beniculturali.it/id/ark:/65666/v1/12609

Mods = args.mods or args.iddump

# if neither --res nor --mods, then default to --res
#if not args.res and not args.mods and not args.iddump:
if not args.res and not Mods:
    args.res = True

# setting this to None speeds things up alot; note re.search is not re.match!
#Rmods = re.compile(r"BEGIN (\S*)\.(\w+)\b") if args.mods else None
Rmods = re.compile(r"BEGIN (\S*)\.(\w+)\b") if Mods else None

# setting this to None speeds things up alot; note re.search is not re.match!
Rres = (
    re.compile(r"BEGIN resolve ([^: ]*)(:?/?([^/ ]*)(.*?)) !!!")
    if args.res
    else None
)

Rnaan = re.compile(r"[^:]+:(.*)")   # yyy inefficient, redo without r.e.
Rinternal_api = re.compile(r"^[^ ]+ 127\.0\.0\.1 ")
Rinternal_res = re.compile(r"BEGIN resolve .*!ra=127\.0\.0\.1")

endtime = args.endtime
#starttime = args.starttime if args.starttime != "0" else ""
starttime = args.starttime
reporttime = ""

# other default Starttime is the start of the current day
if starttime == "-":
    starttime = datetime.today().strftime("%Y.%m.%d")
elif starttime == "0":
    starttime = start_of_time

#reporttime = next_report(starttime, args.when)
# else we'll have to get reporttime after we read first timestamp from log

# Initialize partials
schemes = {}
naans = {}
naan_class = {}
arks = {}
dois = {}
nonmatchcnt = matchcnt = testcnt = Tpre_start_linecnt = 0
ids = {}
ops = {}
testids = {}
modified = {}

# Initialize totals
Tschemes = {}
Tnaans = {}
Tnaan_class = {}
Tarks = {}
Tdois = {}
Tnonmatchcnt = Tmatchcnt = Ttestcnt = 0
Tids = {}
Tops = {}
Ttestids = {}
Tmodified = {}
Tlinecnt = Terrlinecnt = 0

# Some constant id prefixes to count
tidark1 = "ark:/99999/fk4"
tiddoi1 = "ark:/b5072/fk2"
tiddoi2 = "doi:10.5072/FK2"
arkclass = "ark:"
doiclass = "doi:"

import glob

m = re.match(r"(\d\d\d\d)(\.(\d\d)(\.(\d\d)(_(.*))?)?)?$", starttime)
#              1         2  3     4  5     6 7  76 4 2

if not m:
    print(
        # xxx document
        f"Error: starttime ({starttime}) should be TEMPER format, eg,\n",
        f"  2021 | 2021.01 | 2021.01.23 | 2021.01.13_12:26:53.867470",
        file=sys.stderr,
    )
    exit(1)

year = m.group(1)
month = m.group(3) or "01"
day = m.group(5) or "01"
timestamp = m.group(7) or "00:00:00.000000"

# Normalize starttime and save as original_starttime
starttime = f"{year}.{month}.{day}_{timestamp}"
# save original starttime for final report since starttime can get updated
original_starttime = starttime
ymd = f"{year}.{month}.{day}"

files = args.files
if files[0] == "-":
    if len(files) > 1:
        print(f'Error: no args allowed after \"-\" file', file=sys.stderr)
        exit(1)
    #m = re.match(r"(\d\d\d\d\.\d\d\.\d\d)", starttime)  # yyy not much check here
    #if not m:
    #    print(f'Error: with file "-", starttime ({starttime}) must be in TEMPER format',
    #        file=sys.stderr)
    #    exit(1)
    #ymd = m.group(1)
    targetymd = f"{n2tlog}.{ymd}"
    tlogs = glob.glob(f"{n2tlog}*")
    tlogs.sort(reverse=True)

    # Now tlogs looks like
    #   ...
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log.2017.12.31
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log.2017.12.24
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log.2017.12.17
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log

    rfiles = []                 # initialize reverse order file list we want
    for tlfile in tlogs:
        if tlfile < targetymd:  # tlfile contains only dates before our ymd
            break               # so we can stop our search
        else:
            rfiles.append(tlfile)
    rfiles.reverse()            # re-order list in chronological order
    rfiles.append(n2tlog)       # add active log to end
    files = rfiles
    #print("files:", *files, sep="\n ")

    # Now rfiles looks like
    #   ...
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log.2020.07.26
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log.2020.08.02
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log.2020.08.09
    #   /apps/n2t/sv/cur/apache2/logs/transaction_log

    # XXX document
    # NB: 2020.07.19 includes the START of 07.19, but not necessarily its end
    # Also: transaction_log.2020.07.19 contains no date AFTER end of 7/19
    # Also: transaction_log.2020.07.19 need not contain ALL items for 7/19
    # If you need to add log files between other files, EXTEND the date, eg,
    #       transaction_log.2020.07.19
    #       transaction_log.2020.07.19a
    #       transaction_log.2020.07.19b
    # A starttime on 7/19 will use all of these files, in this order.

for file in files:

    # default File is current N2T transaction_log
    m = re.match(r"-(\d+)$", file)
    if file == "-":
        file = n2tlog
    elif m:
        lines = m.group(1)
        import subprocess
        p = subprocess.Popen(f"tail -{lines} {n2tlog} >{tmplog}", shell=True)
        p.wait()
        file = tmplog

    # count_operations(file, "2017.12.25_00:00:01.330")
    time = count_operations(file)
    if not args.iddump:
        print(f"  -- (end {file})")
if not time:  # yyy does this happen?
    exit(1)

# XXX bug: if we don't call report_and_reset(), then the totals don't get
# updated for the last run!
#    *** split that into report_out and flush_subtotals()
#   and call update_globals() here below
if reporttime != end_of_time and time < reporttime:
    report_subtotals(time)
    #report_and_reset(time)
flush_subtotals()

reporttime = time
if not args.iddump:
    print()
    print("============================ TOTALS ================================")
    if len(files) == 1:
        print("# from log", files[0])
    else:
        print("# from logs", *files, sep="\n    ", end="\n")

# now print out totals
report_out(
    original_starttime,
    time,
    reporttime,
    schemes=Tschemes,
    naans=Tnaans,
    naan_class=Tnaan_class,
    testcnt=Ttestcnt,
    matchcnt=Tmatchcnt,
    nonmatchcnt=Tnonmatchcnt,
    ids=Tids,
    ops=Tops,
    testids=Ttestids,
    modified=Tmodified,
)
if not args.iddump:
    print(f"         internal testing lines {Ttestcnt:13d}")
    print(f"                pre-start lines {Tpre_start_linecnt:13d}")
    print()
    print(f"         total resolution lines {Tmatchcnt:13d}")
    print(f"     total non-resolution lines {Tnonmatchcnt:13d}")
    print(
        f"        sum of the above totals "
        f"{Ttestcnt + Tmatchcnt + Tnonmatchcnt + Tpre_start_linecnt:13d}"
    )
    print(f"          error lines processed {Terrlinecnt:13d}")
    print(f"          total lines processed {Tlinecnt:13d}")

# Traceback (most recent call last):
#  File "/apps/n2t/tlog/bin/tlog.py", line 771, in <module>
#    time = count_operations(file)
#  File "/apps/n2t/tlog/bin/tlog.py", line 79, in count_operations
#    sep=" ", maxsplit=4
#ValueError: not enough values to unpack (expected 5, got 4)
