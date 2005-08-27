%define		_modname	dio
%define		_status		stable

Summary:	%{_modname} - Direct I/O functions
Summary(pl):	%{_modname} - funkcje bezpo¶redniego we/wy
Name:		php-pecl-%{_modname}
Version:	not-yet
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	ee90a55b753975faac607f4230ece2b4
URL:		http://pecl.php.net/package/dio/
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	php-devel >= 3:5.0.0
Requires:	php-common >= 3:5.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
PHP supports the direct I/O functions as described in the Posix
Standard (Section 6) for performing I/O functions at a lower level
than the C-Language stream I/O functions (fopen(), fread(),..). The
use of the DIO functions should be considered only when direct control
of a device is needed. In all other cases, the standard filesystem
functions are more than adequate.

In PECL status of this extension is: %{_status}.

%description -l pl
PHP obs³uguje funkcje bezpo¶redniego we/wy wg opisu w standardzie
POSIX (sekcji 6) do wykonywania operacji we/wy na poziomie ni¿szym ni¿
funkcje strumieni we/wy w jêzyku C (fopen(), fread()...). U¿ycie
funkcji DIO powinno byæ rozwa¿ane tylko je¶li potrzebna jest
bezpo¶rednia kontrola nad urz±dzeniem. We wszystkich innych
przypadkach odpowiedniejsze s± standardowe funkcje operacji na
systemie plików.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php-cgi.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php-cgi.ini
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
