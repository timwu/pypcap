EXTRA_DIST = setup.py pcap.pyx pcap_ex.c pcap_ex.h

PKGDIR	= pypcap-`egrep version setup.py | cut -f2 -d"'"`
URL	= `egrep url setup.py | cut -f2 -d"'"`

all: 
	$(PYTHON) setup.py build_ext @PCAP_BUILD_EXT_FLAGS@

install:
	$(PYTHON) setup.py install

test:
	$(PYTHON) test.py

doc:
	epydoc -o doc -n pcap -u $(URL) --docformat=plaintext pcap

pkg_win32:
	$(PYTHON) setup.py bdist_wininst

pkg_osx:
	bdist_mpkg --readme=README --license=LICENSE
	mv dist $(PKGDIR)
	hdiutil create -srcfolder $(PKGDIR) $(PKGDIR).dmg
	mv $(PKGDIR) dist

clean:
	$(PYTHON) setup.py clean

cleandir distclean: clean
	$(PYTHON) setup.py clean -a

# mingw32-make fix
.PHONY: install
