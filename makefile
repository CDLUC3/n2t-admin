# yyy? Support for creating an exportable tar file of "n2t_create".

#PATH=$(HOME)/local/bin:/usr/local/bin:/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/sbin
SHELL=bash
HOST=`hostname -f`
# ?= differs from = in not setting the value if it's already set; more at
#EGNAPA_HOST_CLASS ?= `admegn class | sed 's/ .*//'`
#EGNAPA_HOST_CLASS ?= `perl -Mblib egg cfq class | sed 's/ .*//'`
EGNAPA_HOST_CLASS ?= `(egg --home ~/sv/cur/apache2 cfq class || (read -t 60 -p "HOST_CLASS (loc,dev,stg,prd): " && echo $${REPLY:-loc})) | sed 's/ .*//'`

#EGNAPA_HOST_CLASS=`admegn class | sed 's/ .*//'`
LBIN=$(HOME)/local/bin
LLIB=$(HOME)/local/lib
LOGS=$(HOME)/sv/cur/apache2/logs
TMP=/tmp/n2t_create
# removed recently: $(HOME)/init.d/apache 
#
UTILITIES=$(LBIN)/n2t $(LBIN)/wegn $(LBIN)/wegnpw $(LBIN)/admegn \
	$(LBIN)/logwhich $(LBIN)/logwatch $(LBIN)/bdbkeys \
		$(LBIN)/mrm $(LBIN)/aper \
		$(LBIN)/ezcl $(LBIN)/ia $(LBIN)/ezmdsadmin \
		$(LBIN)/pfx $(LBIN)/mg $(LBIN)/showargs \
		$(LBIN)/make_shdr $(LBIN)/shdr_exists $(LBIN)/make_ezacct \
		$(LBIN)/doip2naan $(LBIN)/naan $(LBIN)/valsh \
		$(LBIN)/validate_naans \
	$(LBIN)/granvl $(LBIN)/replicate \
	$(LBIN)/egg_batch $(LBIN)/aws-ec2-metadata
FILES=boot_install_n2t db-5.3.28.tar.gz zlib-1.2.8.tar.gz \
	make_instance replicate n2t apache svu_run
# NB: that the two ezid rlogs get pride of place over all other binders
QL=$(HOME)/logs
QLOGLINKS=$(QL)/access_log $(QL)/error_log $(QL)/rewrite_log \
	$(QL)/binders/ezid/egg.rlog \
	$(QL)/binders/ezid/rrm.rlog

# default target
basic: basicdirs basicfiles hostname svu utilities $(HOME)/init.d/apache crontab tlogdir

# a bigger target
all: basic n2t_create.tar.gz

# a recursive target
tlogdir:
	(cd tlog; make)

# sub-targets of "basic"
utilities: $(UTILITIES) $(LLIB)/NAAN.pm 

# this uses a "static pattern"
$(UTILITIES): $(LBIN)/%: %
	cp -p $< $(LBIN)

$(LLIB)/NAAN.pm: NAAN.pm
	cp -p $^ $@
	@echo "Did you sync changes to the naan_reg_priv repo?"

svu: $(LBIN)/svu_run $(HOME)/sv

# yyy this making of env.sh likely obsolete!
# See ec2_bootmake for contents of this file.

hostname: $(HOME)/warts/env.sh

$(HOME)/warts/env.sh:
	true

#$(HOME)/warts/env.sh:
#	@echo -e > $@ \
#"#!/bin/sh\n\
#\n\
## This file is initialized by n2t_create/makefile. Changes to it\n\
## only take effect upon "n2t rollout" (not "apache restart").\n\
## This shell script sets some instance-specific environment variables\n\
## that the build_server_tree script (in the eggnog source) reads for\n\
## host and certificate configuration.\n\
##\n\
## Use EGNAPA_SSL_CERTFILE for the full path of a signed certificate,\n\
## if any, and similarly for EGNAPA_SSL_KEYFILE and EGNAPA_SSL_CHAINFILE.\n\
##\n\
##"
#	@read -t 60 -p "HOSTNAME (default $(HOST)): " && echo -e >> $@ \
#"export EGNAPA_HOST=$${REPLY:-$(HOST)}\n\
##export EGNAPA_HOST_CLASS=$${EGNAPA_HOST_CLASS:-mac}              # eg, one of dev, stg, prd, loc\n\
#\n\
#export EGNAPA_SSL_CERTFILE=\n\
#export EGNAPA_SSL_KEYFILE=\n\
#export EGNAPA_SSL_CHAINFILE=\n\
#"
#
#egnapa:
#	@echo "Defining host class \"$(EGNAPA_HOST_CLASS)\""
#
#egnapa:
#	@if [[ -z "$(EGNAPA_HOST_CLASS)" ]]; then \
#		echo "EGNAPA_HOST_CLASS not defined (see ~/warts/env.sh)"; \
#		exit 1; \
#	fi
#	@echo "Defining $(EGNAPA_CLASS) host class \"$(EGNAPA_HOST_CLASS)\" via ~/warts/env.sh. xxx next time via 'admegn class'"
#
# yyy to do: preprocess crontab files so that MAILTO var gets set via a
#     setting in warts/env.sh
#
#cron: egnapa
#
#cron:
#	@cd cron; \
#	if [[ ! -s $$( readlink crontab ) ]]; then \
#		rm -f crontab; \
#		ln -s "crontab.$(EGNAPA_HOST_CLASS)" crontab; \
#	fi; \
#	if [[ ! -s $$( readlink crontab ) ]]; then \
#		echo 'Error: not updating crontab from zero-length file'; \
#	elif [[ $$(readlink crontab) != crontab.$(EGNAPA_HOST_CLASS) ]]; then \
#		echo "Error: crontab doesn't link to a $(EGNAPA_HOST_CLASS)-class file"; \
#	else \
#		crontab -l > crontab_saved; \
#		cmp --silent crontab_saved crontab && { \
#			exit 0; \
#		}; \
#		echo Updating crontab via $$( readlink crontab ); \
#		crontab crontab; \
#	fi
# XXX change .dev to nothing
#
#	#@if [[ ! -s crontab.master ]]; then \
#	#	echo 'Error: not updating crontab from zero-length file'; \
#	#	exit 1; \
#	#fi; \
#	#else \
#	#	crontab -l > crontab_saved; \
#	#	cmp --silent crontab_saved crontab.master && { \
#	#		exit 0; \
#	#	}; \
#	#	echo Updating crontab via crontab.master; \
#	#	crontab crontab.master; \
#	#fi

crontab:
	@ ctab=crontab.main; \
	[[ -e cronstop ]] && ctab=cronstop; \
	crontab -l > crontab_saved; \
	cmp --silent crontab_saved $$ctab && { \
		exit 0; \
	}; \
	echo Updating crontab via $$ctab; \
	crontab $$ctab

# Goal here is to reflect basic skeleton in the maintenance/role account.
# Since these files are maintained in a separate "dotfiles" repo, sometimes
# a reverse update (from the installed account dotfiles) is necessary.

update_basicfiles:
	@cd skel; rsync --info=NAME -a \
		$(HOME)/.{bash_profile,bashrc,gitconfig,vimrc} .

basicfiles:
	@cd skel; rsync --info=NAME -a \
		.bash_profile .bashrc .gitconfig .svudef .vimrc $(HOME)

#basicfiles:
#	@cd skel; \
#	for f in .bash_profile .bashrc .gitconfig .svudef .vimrc ; \
#	do \
#		if [[ $$f -nt $(HOME)/$$f ]]; then \
#			echo cp -p $$f $(HOME)/$$f; \
#			cp -p $$f $(HOME)/$$f; \
#		fi; \
#	done; true

BASICDIRS=$(LBIN) $(LLIB) $(HOME)/warts $(HOME)/warts/ssl $(HOME)/ssl \
	$(HOME)/.ssh $(HOME)/logs $(HOME)/init.d $(HOME)/backups \
	$(HOME)/minters $(HOME)/binders $(HOME)/naans $(HOME)/batches \

basicdirs: $(BASICDIRS)

# xxx test this!
# Create backups directory so that TMPDIR can be set to it,
#    avoiding overuse and performance problems using /tmp.
# mkdir -p $(HOME)/../n2tbackup/backups/tmp; \
	#if [[ -d $(HOME)/../n2tbackup ]]; then \
	#	ln -s $(HOME)/../n2tbackup/backups $(HOME)/backups; \
	#fi

$(HOME)/backups $(HOME)/naans:
	mkdir -p $@

$(LBIN) $(LLIB) $(HOME)/warts $(HOME)/warts/ssl $(HOME)/init.d $(HOME)/batches:
	mkdir -p $@

# XXX better: point env.sh directly to ~/ssl/*/.cer, because it's easier
#     and safer to test by simply swapping the env.sh file instead of
#     swapping it along with the ~/warts/ssl files
# XXX drop this since we already have readable .cnf file
#sslreadme:
#	@ cfile=$$( echo $(HOME)/warts/ssl/*_cert.cer ); \
#	  rfile=$(HOME)/warts/ssl/README ; \
#	if [[ -f "$$cfile" && ( ! -f $$rfile || $$cfile -nt $$rfile ) ]]; \
#	then \
#		openssl x509 -in $$cfile -text -noout > $$rfile ; \
#	fi

# xxx add $(HOME) to last arg of ln -s ...  ?? (else problem if run in
# wrong directory)
$(HOME)/logs:
	mkdir -p $@
	-ln -s $(LOGS)/{access,error,rewrite}_log $@
	-ln -s $(HOME)/sv/cur/apache2/binders/ezid/egg.rlog $@/ezid.rlog
	-ln -s $(HOME)/sv/cur/apache2/binders/ezid/rrm.rlog $@/ezid.rrmlog

# NB: don't create dirs under apache2, since "n2t rollout" does special
#     processing the first time through

$(HOME)/minters $(HOME)/binders:
	rm -f $@
	ln -s $(HOME)/sv/cur/apache2/$$(basename $@) $@

$(HOME)/.ssh: $(HOME)/.ssh/id_rsa
	@mkdir -p $@

$(HOME)/.ssh/id_rsa:
	ssh-keygen -t rsa
	chmod 700 $(HOME)/.ssh

$(HOME)/init.d/apache: $(LBIN)/apache $(LBIN)/egnapa apache
	cp -p apache $(HOME)/init.d/

$(LBIN)/apache:
	-ln -s $(HOME)/init.d/apache $(LBIN)/apache

$(LBIN)/egnapa:
	-ln -s $(HOME)/init.d/apache $(LBIN)/egnapa

$(LBIN)/svu_run: svu_run
	@echo NOTE: svu is maintained in its own repo.
	cp -p $^ $(LBIN)

$(HOME)/sv:
	@echo "Initializing SVU."
	@export PATH=$(LBIN):$$PATH; /bin/bash -c "cd; source .svudef; svu init"

n2t_create.tar.gz: $(FILES) makefile
	rm -fr $(TMP)
	mkdir $(TMP)
	cp -p $^ $(TMP)
	(cd /tmp; tar cf - n2t_create) > n2t_create.tar
	gzip n2t_create.tar
