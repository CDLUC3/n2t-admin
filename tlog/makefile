SHELL=bash

# ./bin dir holds the version used by installed script (~/bin/local/tlog).

APPHOME=/apps/n2t
PUB=$(APPHOME)/sv/cur/apache2/htdocs/e/pub
PFX_SOURCES= $(PUB)/naan_registry.txt $(PUB)/naan_table.txt $(PUB)/shoulder_registry.txt $(PUB)/ebi.anvl
#INSTALL= $(APPHOME)/local/bin/tlog $(APPHOME)/local/bin/lonlat
LBIN= $(APPHOME)/local/bin
UTILITIES=$(LBIN)/tlog $(LBIN)/lonlat
ALL= venv prefixes.txt doi_naans.txt naan_table.txt $(INSTALL)
# should there be a separate install step?

#GROWTH= $(APPHOME)/sv/cur/apache2/htdocs/e/images/naan_growth.png

#	tlog --when monthly 2017.12.17_00:00:00 - > xx # xxx bug? errors
#	echo "YYYY-MM,Resolutions" > z.csv
#	perl -nE 'm/^# ========.* to (.*)/ and $date = $1; m/^  *resolution lines *(.*)/ and ($n = $1, $date =~ s/\./-/, say "$date,$n")' y >> z.csv
#	@scp z.csv intracdl@intracdl.cdlib.org:/intracdl/apache/htdocs/dashboard/cdl_dash_amcharts/data/IdentifiersN2T.csv
#
# YYYY-MM,DOI,ARK
# 2010-09,0,5
# 2010-10,0,8
# 2010-11,0,43029

#all: virtual_env bin bin/tlog.py bin/tlog doi_naans.txt $(APPHOME)/local/bin/tlog
all: $(ALL) utilities
	@true

utilities: $(UTILITIES)

# this uses a "static pattern"
$(UTILITIES): $(LBIN)/%: %
	cp -p $< $(LBIN)

## XXX maybe fresh copies should always be in ../e/pub ?
##     so we can drop this harvest
## use 'make refresh' to harvest naan sources
#refresh:
#	curl --silent -O 'https://n2t.net/e/pub/naan_{registry,table}.txt'
#
## use 'make growth' to regenerate image of NAAN registry growth
#growth: $(GROWTH)
#
## xxx is this needed?
#$(GROWTH): naan_growth.png
#	cp -p $^ $@
#	@echo "Image at https://$(EGNAPA_HOST)/e/images/naan_growth.png"

naan_growth.png: plot growth.py naan_dates venv
	venv/bin/python growth.py

# if newer, local copy overrides published copy
naan_dates: naan_registry.txt
	sed -n 's/^when: *//p' $^ | sed 1d | sort > $@

naan_registry.txt: $(PUB)/naan_registry.txt
	cp -p $^ $@

test: venv all pytest

pytest: venv/bin/pytest venv
	venv/bin/pytest -q

venv/bin/pytest: venv
	source venv/bin/activate && pip install pytest

venv:
	python3 -m venv venv

# yyy temporary no-op
plot: venv/bin/f2py
	@true

# f2py is installed by numpy, which is required by matplotlib
# kludge: let f2py's existence signal whether matplotlib is installed
# install geopy at same time (for lonlat.sh and openstreetmap)
venv/bin/f2py: venv
	source venv/bin/activate && pip install matplotlib
	source venv/bin/activate && pip install geopy

# this script calls bin/tlog.py via the correct venv-established python binary
bin/tlog: bin bin/tlog.py tlog.sh
	cp tlog.sh $@

bin/tlog.py: bin tlog.py
	cp tlog.py $@

bin/lonlat: bin lonlat.sh
	cp lonlat.sh $@

bin:
	mkdir -p $@

## make changes in tlog.sh or tlog.py visible at system level
#$(INSTALL): bin/tlog bin/lonlat
#	cp -p $^ $@

# Save a CSV version of EBI prefixes file, and add duplicates for aliases (kludge).

#	granvl 'print v(":"), "\t", v("name"), "\n"; 0' ebi.anvl | perl -nE '' > $@
# xxx bug in granvl: when name but no value is given, v() return next line!!
#     get around for now by eliminating such lines
# "alias: x" means whenever you find :: going forward, as all or the tail of a prefix,
# generate an extra key with :: replaced by x and give it "name" as value.
# "synonym(for): y" means do one-time lookup of y and assign its name as value of ::

naan_table.txt: $(PUB)/naan_table.txt
	cp -p $^ $@

prefixes.txt: ebi.anvl
	perl -nE '! /^[^:]+:\s*$$/ and print' < $^ | granvl \
	  'print v(":"), "\t", v("name"), "\t", v("alias"), "\t", v("for"), "\n"; 0' \
	> $@

ebi.anvl: $(PUB)/ebi.anvl
	cp -p $^ $@

#	granvl 'print v(":"), "\t", v("name"), "\t", v("alias"), "\t", v("for"), "\n"; 0' ebi.anvl > $@
#	granvl 'print v(":"), "\t", v("name"), "\n"; 0' ebi.anvl | sed -n -e /./p -e 's/taxonomy/taxon/p' -e 's/pubmed/pmid/p' -e 's/uniprot/uniprotkb/p' -e 's/ec-code/ec/p' > $@

# Save a CSV version of shoulders file with ark:/... normalized to ark:...
# and remove any datacenter lines.

doi_naans.txt: shoulder_registry.txt
	granvl 'print v(":"), "\t", v("name"), "\t", uc(v("manager")), "\n"; 0' shoulder_registry.txt | sed -e '/^datacite/d' -e 's,^ark://*,ark:,' > $@

shoulder_registry.txt: $(PUB)/shoulder_registry.txt
	cp -p $^ $@

$(PFX_SOURCES):
	mkdir -p $(PUB)
	(cd $(PUB); curl --silent -O 'https://n2t.net/e/pub/{ebi.anvl,naan_registry.txt,naan_table.txt,shoulder_registry.txt}')

