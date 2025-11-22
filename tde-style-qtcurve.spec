#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg tde-style-qtcurve
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.55.2
Release:	%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:	This is a set of widget styles for Trinity based apps
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/themes/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}
BuildRequires: libtool
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# IDN support
BuildRequires:	pkgconfig(libidn)

# ACL support
BuildRequires:  pkgconfig(libacl)

# GAMIN support
#  Not on openSUSE.
%if 0%{!?suse_version}
%define with_gamin 1
BuildRequires:	pkgconfig(gamin)
%endif

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


Obsoletes:		trinity-kde-style-qtcurve < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-kde-style-qtcurve = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:		trinity-style-qtcurve < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:		trinity-style-qtcurve = %{?epoch:%{epoch}:}%{version}-%{release}


%description
This package together with gtk2-engines-qtcurve aim to provide a unified look
and feel on the desktop when using TDE and Gnome applications.

This package is most useful when installed together with 
gtk2-engines-qtcurve.


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}



%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Shitty hack for RHEL4 ...
if [ -d "/usr/X11R6" ]; then
  export CMAKE_INCLUDE_PATH="${CMAKE_INCLUDE_PATH}:/usr/X11R6/include:/usr/X11R6/%{_lib}"
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

# Error in "po/tr.po"
%if 0%{?rhel} == 4
%__rm -f "po/tr.po"
%endif

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DBIN_INSTALL_DIR=%{tde_bindir} \
  -DINCLUDE_INSTALL_DIR=%{tde_tdeincludedir} \
  -DLIB_INSTALL_DIR=%{tde_libdir} \
  -DSHARE_INSTALL_PREFIX=%{tde_datadir} \
  \
  -DTDE_INCLUDE_DIR=%{tde_tdeincludedir} \
  -DQTC_QT_ONLY=false \
  -DQTC_STYLE_SUPPORT=true \
  -DBUILD_ALL=on \
  ..

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang qtcurve || touch qtcurve.lang


%files -f qtcurve.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_tdelibdir}/tdestyle_qtcurve_config.la
%{tde_tdelibdir}/tdestyle_qtcurve_config.so
%{tde_tdelibdir}/plugins/styles/qtcurve.so
%{tde_tdelibdir}/plugins/styles/qtcurve.la
%{tde_datadir}/apps/tdedisplay/color-schemes/QtCurve.kcsrc
%{tde_datadir}/apps/tdestyle/themes/qtcurve.themerc
%{tde_datadir}/apps/QtCurve/

