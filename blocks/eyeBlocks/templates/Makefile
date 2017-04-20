UI_FILES = $(shell ls *.ui)
UI_COMPILED = $(patsubst %.ui, ui_%.py, $(UI_FILES))
RC_FILES = $(shell ls *.qrc)
SVG_FILES = $(shell ls *.svg)
RC_COMPILED = $(patsubst %.qrc, %_rc.py, $(RC_FILES))

PYUIC = pyuic4
PYRCC = pyrcc4

all: $(RC_COMPILED) $(UI_COMPILED) 

clean:
	rm -f $(RC_COMPILED) $(UI_COMPILED) 
	rm -rf *.pyc *~ __pycache__

ui_%.py:  %.ui
	$(PYUIC) $< -o $@

%_rc.py: %.qrc $(SVG_FILES)
	$(PYRCC) $< -o $@



.PHONY: all clean
