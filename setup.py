from distutils.core import setup
from distutils.extension import Extension
from distutils.command import config, clean
from distutils import util
from Pyrex.Distutils import build_ext
import os.path
import sys, os

class pypcap_config(config.config):
    description = 'configure pcap paths'
    user_options = [ ('with-pcap=', None,
                      'path to pcap build or installation directory') ]

    def initialize_options(self):
        config.config.initialize_options(self)
        self.with_pcap = None

    def _make_config_h(self, filename):
        headers = ["pcap.h"]
        f = open(filename, "w")
        if self.with_pcap:
            f.write("// Using pcap install prefix: %s\n" % self.with_pcap) 
        if self.check_header("pcap-int.h", include_dirs=self._get_includes()):
            self.announce("Found pcap-int.h")
            f.write("#define HAVE_PCAP_INT_H 1\n")
        if self.check_func("pcap_file", headers=headers,
                include_dirs=self._get_includes()):
            self.announce("Found pcap_file()")
            f.write("#define HAVE_PCAP_FILE 1\n") 
        if self.check_func("pcap_compile_nopcap", headers=headers, 
                include_dirs=self._get_includes()):
            self.announce("Found pcap_compile_nopcap")
            f.write("#define HAVE_PCAP_COMPILE_NOPCAP 1\n")
        if self.check_func("pcap_setnonblock", headers=headers, 
                include_dirs=self._get_includes()):
            self.announce("Found pcap_setnonblock")
            f.write("#define HAVE_PCAP_SETNONBLOCK 1\n")
        f.close()

    def _get_includes(self):
        if self.with_pcap:
            return [os.path.join(self.with_pcap, "include")]
        else:
            return None

    def _get_libraries(self):
        if self.with_pcap:
            return [os.path.join(self.with_pcap, "libs")]
        else:
            return None

    def run(self):
        config_h = "config.h"
        if not self.check_header("pcap.h"):
            self.announce("Couldn't find a pcap installation.")
            raise Exception("Error, pcap.h not found.")
        if util.get_platform() == 'win32' and \
                not self.check_lib("wpcap", library_dirs=self._get_libraries()):
            self.announce("Couldn't find libwpcap.a")
            raise Exception("Error, libwpcap.a not found")
        elif not self.check_lib("pcap", library_dirs=self._get_libraries()):
            self.announce("Couldn't find libpcap.a")
            raise Exception("Error, libpcap.a not found.")
        self.make_file(["setup.py"], config_h, self._make_config_h, [config_h]) 

class pypcap_clean(clean.clean):
    def run(self):
        os.unlink("config.h")
        os.unlink("pcap.c")

includes = []
libdirs = []
lib = ""
if util.get_platform() == 'win32':
    lib = "wpcap"
else:
    lib = "pcap"
if os.path.exists(os.path.join(os.path.dirname(sys.argv[0]), "config.h")):
    f = open(os.path.join(os.path.dirname(sys.argv[0]), "config.h"), "r")
    libpath = f.readline()
    if "// Using pcap install prefix: " in libpath:
       libpath = libpath.replace("// Using pcap install prefix: ","")
       includes = [os.path.join(libpath, "include")]
       libdirs = [os.path.join(libpath, "libs")]
    f.close()
    
pcap_extension = Extension( name="pcap",
                            sources=["pcap.pyx", "pcap_ex.c"],
                            include_dirs=includes,
                            library_dirs=libdirs,
                            libraries=[ lib ]
                 )

setup(  name = "pypcap",
        version = "1.1",
        ext_modules=[pcap_extension],
        cmdclass = {'build_ext' : build_ext, 
                    'config' : pypcap_config, 
                    'clean' : pypcap_clean }
)
