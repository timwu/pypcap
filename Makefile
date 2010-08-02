# $Id: Makefile 102 2010-07-17 19:07:07Z kosma@kosma.pl $

PYTHON	= python
PYTHON_DIR = c:\\python27
ifeq (${OS},Windows_NT)
RMDIR = rmdir /S /Q
RM = del /Q
else
RMDIR = rm -rf
RM = rm -f
endif

#CONFIG_ARGS = --with-pcap=$(HOME)/build/libpcap-0.8.3

# PYTHON = C:\\Python23\\python.exe
CONFIG_ARGS = --with-pcap=c:\\Users\\tim\\Downloads\\wpdpack

PKGDIR	= pypcap-`egrep version setup.py | cut -f2 -d"'"`
URL	= `egrep url setup.py | cut -f2 -d"'"`

all: pcap.c
	$(PYTHON) setup.py config $(CONFIG_ARGS)
	$(PYTHON) setup.py build

pcap.c: pcap.pyx
ifeq (${OS},Windows_NT)
	${PYTHON} ${PYTHON_DIR}\scripts\pyrexc.py pcap.pyx
else
	pyrexc pcap.pyx
endif

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
	- ${RMDIR} build dist
	- ${RM} pcap.c *~

cleandir distclean: clean
	$(PYTHON) setup.py clean -a
	- ${RM} config.h *~

# mingw32-make fix
.PHONY: install
