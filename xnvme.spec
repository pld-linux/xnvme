# TODO: spdk (force using system?)
#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static libraries
%bcond_without	libvfn		# libvfn support

%ifnarch %{x8664} aarch64
%undefine	with_libvfn
%endif
Summary:	xNVMe: cross-platform libraries and tools for NVMe devices
Summary(pl.UTF-8):	xNVMe - wieloplatformowe biblioteki i narzędzia dla urządzeń NVMe
Name:		xnvme
Version:	0.7.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/xnvme/xnvme/releases
Source0:	https://github.com/xnvme/xnvme/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d3dab6e7843cbea13a0592f3b9f4a452
Patch0:		%{name}-sizes.patch
URL:		https://xnvme.io/
BuildRequires:	gcc >= 6:4.7
BuildRequires:	libaio-devel
BuildRequires:	libisal-devel >= 2.30
BuildRequires:	liburing-devel >= 2.2
%{?with_libvfn:BuildRequires:	libvfn-devel >= 5.0.0}
BuildRequires:	meson >= 0.58
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
Requires:	libisal >= 2.30
Requires:	liburing >= 2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
xNVMe provides the means to program and interact with NVMe devices
from user space.

%description -l pl.UTF-8
xNVMe udostępnia możliwość programowania i współpracy z urządzeniami
NVMe z przestrzeni użytkownika.

%package devel
Summary:	Header files for xNVMe library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki xNVMe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libaio-devel
Requires:	libisal-devel >= 2.30
Requires:	liburing-devel >= 2.2
%{?with_libvfn:Requires:	libvfn-devel >= 5.0.0}

%description devel
Header files for xNVMe library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki xNVMe.

%package static
Summary:	Static xNVMe library
Summary(pl.UTF-8):	Statyczna biblioteka xNVMe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static xNVMe library.

%description static -l pl.UTF-8
Statyczna biblioteka xNVMe.

%prep
%setup -q
%patch0 -p1

%{__sed} -i '1s,/usr/bin/env bash,/bin/bash,' toolbox/xnvme-driver.sh

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	-Dforce_completions=true

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst CONTRIBUTORS.md ISSUES.rst LICENSE MAINTAINERS.md README.md
%attr(755,root,root) %{_bindir}/kvs
%attr(755,root,root) %{_bindir}/lblk
%attr(755,root,root) %{_bindir}/xdd
%attr(755,root,root) %{_bindir}/xnvme
%attr(755,root,root) %{_bindir}/xnvme-driver
%attr(755,root,root) %{_bindir}/xnvme_*
%attr(755,root,root) %{_bindir}/zoned
%attr(755,root,root) %{_bindir}/zoned_io_async
%attr(755,root,root) %{_bindir}/zoned_io_sync
%attr(755,root,root) %{_libdir}/libxnvme.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libxnvme.so.0
%{bash_compdir}/kvs-completions
%{bash_compdir}/lblk-completions
%{bash_compdir}/xdd-completions
%{bash_compdir}/xnvme*-completions
%{bash_compdir}/zoned*-completions
%{_mandir}/man1/kvs.1*
%{_mandir}/man1/kvs-*.1*
%{_mandir}/man1/lblk.1*
%{_mandir}/man1/lblk-*.1*
%{_mandir}/man1/xdd.1*
%{_mandir}/man1/xdd-*.1*
%{_mandir}/man1/xnvme.1*
%{_mandir}/man1/xnvme-*.1*
%{_mandir}/man1/xnvme_*.1*
%{_mandir}/man1/zoned.1*
%{_mandir}/man1/zoned-*.1*
%{_mandir}/man1/zoned_io_async.1*
%{_mandir}/man1/zoned_io_async-*.1*
%{_mandir}/man1/zoned_io_sync.1*
%{_mandir}/man1/zoned_io_sync-*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxnvme.so
%{_includedir}/libxnvme*.h
%{_pkgconfigdir}/xnvme.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxnvme.a
%endif
