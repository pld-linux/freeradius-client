#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	FreeRADIUS Client framework
Summary(pl.UTF-8):	Szkielet klienta FreeRADIUS
Name:		freeradius-client
Version:	1.1.7
Release:	2
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.freeradius.org/pub/radius/%{name}-%{version}.tar.gz
# Source0-md5:	43b4d21715b613dc4fe8ef128467fe78
URL:		http://www.freeradius.org/
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FreeRADIUS Client is a framework and library for writing RADIUS
clients which additionally includes radlogin, a flexible RADIUS aware
login replacement, a command line program to send RADIUS accounting
records and a utility to query the status of a (Merit) RADIUS server.

%description -l pl.UTF-8
FreeRADIUS Client to szkielet i biblioteka do tworzenia klientów
RADIUS; szkielet dodatkowo zawiera program radlogin (elastyczny
zamiennik programu login obsługujący RADIUS), klienta linii poleceń do
wysyłania rekordów rozliczeniowych RADIUS oraz narzędzie do
odpytywania stanu (właściwego) serwera RADIUS.

%package libs
Summary:	FreeRADIUS Client library
Summary(pl.UTF-8):	Biblioteka kliencka FreeRADIUS
Group:		Libraries

%description libs
FreeRADIUS Client library.

%description libs -l pl.UTF-8
Biblioteka kliencka FreeRADIUS.

%package devel
Summary:	Header files for FreeRADIUS Client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki FreeRADIUS Client
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for FreeRADIUS Client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki FreeRADIUS Client.

%package static
Summary:	Static FreeRADIUS Client library
Summary(pl.UTF-8):	Statyczna biblioteka FreeRADIUS Client
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static FreeRADIUS Client library.

%description static -l pl.UTF-8
Statyczna biblioteka FreeRADIUS Client.

%prep
%setup -q

%build
%configure \
	ac_cv_lib_nsl_gethostbyaddr=no \
	ac_cv_lib_socket_socket=no \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc BUGS COPYRIGHT README.radexample README.rst doc/{ChangeLog,README,instop.html}
# dummy
#%attr(755,root,root) %{_sbindir}/login.radius
%attr(755,root,root) %{_sbindir}/radacct
%attr(755,root,root) %{_sbindir}/radembedded
%attr(755,root,root) %{_sbindir}/radexample
%attr(755,root,root) %{_sbindir}/radiusclient
%attr(755,root,root) %{_sbindir}/radlogin
%attr(755,root,root) %{_sbindir}/radstatus
%dir %{_sysconfdir}/radiusclient
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/dictionary
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/dictionary.ascend
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/dictionary.compat
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/dictionary.merit
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/dictionary.sip
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/issue
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/port-id-map
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/radiusclient.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/radiusclient/servers

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-client.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfreeradius-client.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfreeradius-client.so
%{_libdir}/libfreeradius-client.la
%{_includedir}/freeradius-client.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libfreeradius-client.a
%endif
