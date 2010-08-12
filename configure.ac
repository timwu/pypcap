AC_INIT([pypcap], [1.0], [tim.wu.0@gmail.com], [pypcap], [])
AM_INIT_AUTOMAKE([foreign])
AC_CONFIG_MACRO_DIR([m4])
AC_CANONICAL_SYSTEM

# Check python availability
AX_WITH_PYTHON
AX_PYTHON_MODULE([Pyrex], [1])

# Check for pcap
AC_ARG_WITH([pcap], [--with-pcap=DIR provide the path to pcap], [PCAP_DIR=$withval], 
            [PCAP_DIR=]
)
AS_IF([test "$PCAP_DIR" != ""], [
   AS_IF([test -d $PCAP_DIR/include],
      [CPPFLAGS="$CPPFLAGS -I$PCAP_DIR/include"],
      [AC_MSG_ERROR([Can't find an include dir in the given pcap folder $PCAP_DIR])]
   )
   AS_IF([test -d $PCAP_DIR/lib],
      [LDFLAGS="$LDFLAGS -L$PCAP_DIR/Lib"],
      [AC_MSG_ERROR([Can't find an lib dir in the given pcap folder $PCAP_DIR])]
   )
   PCAP_BUILD_EXT_FLAGS="-I$PCAP_DIR/include -L$PCAP_DIR/Lib"
   AC_SUBST([PCAP_BUILD_EXT_FLAGS])
   ]
)
PCAP_LIB=pcap
case $host in
*mingw32*)
   PCAP_LIB=wpcap
   ;;
esac
AC_CHECK_HEADER([pcap.h])
AC_CHECK_LIB([$PCAP_LIB], [pcap_create], , [AC_MSG_ERROR(Can't find libpcap.)])
AC_CHECK_FUNCS([pcap_file pcap_compile_nopcap pcap_setnonblock])

AC_CONFIG_FILES([Makefile src/Makefile])
AC_CONFIG_HEADERS([src/config.h])
AC_CONFIG_SRCDIR([src/pcap.pyx])
AC_OUTPUT
