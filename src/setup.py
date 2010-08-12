from distutils.core import setup
from distutils.extension import Extension
from distutils import util
from Pyrex.Distutils import build_ext
import os.path

# Hack to get around build_ext's inability to handle multiple
# libraries in its --libraries= argument.
libs = []
if util.get_platform() == 'win32':
   libs = [ "wpcap", "iphlpapi" ]
else:
   libs = [ "pcap" ]
    
pcap_extension = Extension( name="pcap",
                            sources=["pcap.pyx", "pcap_ex.c"],
                            libraries=libs
                 )

setup(  name = "pypcap",
        version = "1.1",
        ext_modules=[pcap_extension],
        cmdclass = {'build_ext' : build_ext}
)
