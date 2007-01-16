%define		_modname	dio
%define		_status		beta
%define		_rc rc1
Summary:	%{_modname} - Direct I/O functions
Summary(pl):	%{_modname} - funkcje bezpo¶redniego we/wy
Name:		php-pecl-%{_modname}
Version:	5.0
Release:	0.%{_rc}.1
License:	PHP 2.02
Group:		Development/Languages/PHP
#Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
Source0:	%{_modname}.tgz
# Source0-md5:	b926091229d356253f9f30f99e1e2253
URL:		http://pecl.php.net/package/dio/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Obsoletes:	php-dio
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%setup -q -n %{_modname}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
