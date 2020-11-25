GREEN = $$(tput setaf 2)
YELLOW = $$(tput setaf 3)
RESET = $$(tput sgr0)

all: help

help:                  #~ Show this help
	@fgrep -h "#~"  $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e "s/^\([^:]*\):/${GREEN}\1${RESET}/;s/#~r/${RESET}/;s/#~y/${YELLOW}/;s/#~ //"

setup:
	cp config.ini.dist config.ini

compile:
	python3 bin/compiler.py

update:
	python3 bin/config-updater.py

.PHONY: setup compile update