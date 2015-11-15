all: tags


PYSRC=$(shell ls src/tfoto/*.py)
SRC=$(PYSRC) scripts/tfoto
tags: $(SRC)
	ctags -R .

clean:
	@echo "Cleaning pyc files"
	pyclean .
	@echo "Removing old tags"
	rm -f tags
