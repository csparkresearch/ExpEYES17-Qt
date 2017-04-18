# Main Makefile for Expeyes-Blocks

SUBDIRS = eyePlot doc

all: recursive_all

recursive_all:
	for d in $(SUBDIRS); do [ ! -f $$d/Makefile ] || make -C $$d all; done

clean: recursive_clean
	rm -rf *.pyc *~ __pycache__

recursive_clean:
	for d in $(SUBDIRS); do [ ! -f $$d/Makefile ] || make -C $$d clean; done
	
doc:
	make -f Makefile.sphinx html

.PHONY: all recursive_all clean recursive_clean doc
