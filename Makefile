all: tags


PYSRC=$(shell ls src/tfoto/*.py)
SRC=$(PYSRC) scripts/tfoto
tags: $(SRC)
	ctags -R .
