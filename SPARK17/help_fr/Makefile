DESTDIR =
LANG = fr
JEKYLL = jekyll
STATIC_OUTPUTDIR = MD_HTML

all:
	mkdir -p $(STATIC_OUTPUTDIR)
	$(JEKYLL) build --incremental

clean:
	rm -rf $(STATIC_OUTPUTDIR)

install:
	install -d $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)
	cp -a $(STATIC_OUTPUTDIR)/* $(DESTDIR)/usr/share/expeyes/eyes17/help_$(LANG)

.PHONY: all clean install
