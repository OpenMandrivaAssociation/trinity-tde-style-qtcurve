%bcond clang 1
%bcond gamin 1

# TDE variables
%define tde_pkg tde-style-qtcurve
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%undefine _debugsource_template

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Version:	14.1.6
Release:	1
Summary:	This is a set of widget styles for Trinity based apps
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{version}/main/applications/themes/%{tarball_name}-%{version}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DINCLUDE_INSTALL_DIR=%{tde_prefix}/include/tde
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DTDE_INCLUDE_DIR=%{tde_prefix}/include/tde
BuildOption:    -DQTC_QT_ONLY=OFF
BuildOption:    -DQTC_STYLE_SUPPORT=ON
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{version}
BuildRequires:	trinity-tdebase-devel >= %{version}
BuildRequires:	trinity-tde-cmake >= %{version}

BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires: libtool

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes


# IDN support
BuildRequires:	pkgconfig(libidn)

# ACL support
BuildRequires:  pkgconfig(libacl)

# GAMIN support
%{?with_gamin:BuildRequires:	pkgconfig(gamin)}

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xft)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


Obsoletes:		trinity-kde-style-qtcurve < %{EVRD}
Provides:		trinity-kde-style-qtcurve = %{EVRD}
Obsoletes:		trinity-style-qtcurve < %{EVRD}
Provides:		trinity-style-qtcurve = %{EVRD}


%description
This package together with gtk2-engines-qtcurve aim to provide a unified look
and feel on the desktop when using TDE and Gnome applications.

This package is most useful when installed together with 
gtk2-engines-qtcurve.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
%find_lang qtcurve || touch qtcurve.lang


%files -f qtcurve.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{tde_prefix}/%{_lib}/trinity/tdestyle_qtcurve_config.la
%{tde_prefix}/%{_lib}/trinity/tdestyle_qtcurve_config.so
%{tde_prefix}/%{_lib}/trinity/plugins/styles/qtcurve.so
%{tde_prefix}/%{_lib}/trinity/plugins/styles/qtcurve.la
%{tde_prefix}/share/apps/tdedisplay/color-schemes/QtCurve.kcsrc
%{tde_prefix}/share/apps/tdestyle/themes/qtcurve.themerc
%{tde_prefix}/share/apps/QtCurve/

