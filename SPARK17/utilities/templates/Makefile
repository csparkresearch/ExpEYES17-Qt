UI_FILES = $(shell ls *.ui)
UI_COMPILED = $(patsubst %.ui, ui_%.py, $(UI_FILES))
RC_FILES = $(shell ls *.qrc)
RC_COMPILED = $(patsubst %.qrc, %_rc.py, $(RC_FILES))

all: $(UI_COMPILED) $(RC_COMPILED)

clean:
	rm -f $(UI_COMPILED)
	rm -rf *.pyc *~ __pycache__

ui_%.py:  %.ui
	$(PYUIC) --from-import $< -o $@

%_rc.py: %.qrc
	$(PYRCC)  $< -o $@

.PHONY: all clean
