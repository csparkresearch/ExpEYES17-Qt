# Main Makefile for Expeyes-Blocks

SUBDIRS = eyeBlocks
UI_SOURCES = $(shell ls eyeBlocks/templates/*.ui)
PY_SOURCES = $(shell ls eyeBlocks/*.py)
TS_FILES = $(shell ls eyeBlocks/lang/*.ts)

all: recursive_all lang

Expeyes-Blocks.pro: $(UI_SOURCES) $(PY_SOURCES)
	echo "FORMS += $(UI_SOURCES)" > Expeyes-Blocks.pro
	echo -n "SOURCES += $(PY_SOURCES)" >> Expeyes-Blocks.pro
	echo -n "TRANSLATIONS += $(TS_FILES)" >> Expeyes-Blocks.pro

lang: Expeyes-Blocks.pro
	pylupdate4 Expeyes-Blocks.pro
	cd eyeBlocks/lang; for f in *.ts; do lrelease $$f; done

recursive_all:
	for d in $(SUBDIRS); do make -C $$d all; done

clean: recursive_clean
	rm -rf *.pyc *~ __pycache__

recursive_clean:
	for d in $(SUBDIRS); do make -C $$d clean; done

doc:
	make -C doc all
	echo "you can open the documentation by 'firefox doc/build/html/index.html'"

clean_doc:
	make -C doc clean

.PHONY: all recursive_all clean recursive_clean doc doc_clean lang
