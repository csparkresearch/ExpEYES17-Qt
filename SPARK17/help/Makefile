DESTDIR =
LANG = en
JEKYLL = jekyll
STATIC_OUTPUTDIR = MD_HTML
MD_FILES = $(shell find . -name "*.md")

all:
	mkdir -p $(STATIC_OUTPUTDIR)
	$(JEKYLL) build --incremental

todo:
	@for f in $(MD_FILES); do \
	  g=../help/$$f; \
	  if cmp -s $$f $$g; then echo "Not translated: $$f"; fi; \
	  if [ $$g -nt $$f ]; then echo "Update? $$g is newer than $$f"; fi; \
	done

manual/manual.pdf: $(MD_FILES)
	LANG=en_IN.UTF-8 ../textManual/textManual.py

clean:
	rm -rf $(STATIC_OUTPUTDIR) manual

install:
	install -d $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)
	cp -a $(STATIC_OUTPUTDIR)/* $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)

.PHONY: all clean install todo
