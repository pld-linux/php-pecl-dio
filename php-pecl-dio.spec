#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	dio
Summary:	%{modname} - Direct I/O functions
Summary(pl.UTF-8):	%{modname} - funkcje bezpośredniego we/wy
Name:		%{php_name}-pecl-%{modname}
Version:	0.0.7
Release:	4
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	a1a4df428a17dbe1ab4277b492dfa052
URL:		http://pecl.php.net/package/dio/
BuildRequires:	%{php_name}-devel >= 3:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-dio
Obsoletes:	php-pecl-dio < 0.0.7-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PHP supports the direct I/O functions as described in the Posix
Standard (Section 6) for performing I/O functions at a lower level
than the C-Language stream I/O functions (fopen(), fread(),..). The
use of the DIO functions should be considered only when direct control
of a device is needed. In all other cases, the standard filesystem
functions are more than adequate.

%description -l pl.UTF-8
PHP obsługuje funkcje bezpośredniego we/wy wg opisu w standardzie
POSIX (sekcji 6) do wykonywania operacji we/wy na poziomie niższym niż
funkcje strumieni we/wy w języku C (fopen(), fread()...). Użycie
funkcji DIO powinno być rozważane tylko jeśli potrzebna jest
bezpośrednia kontrola nad urządzeniem. We wszystkich innych
przypadkach odpowiedniejsze są standardowe funkcje operacji na
systemie plików.

%prep
%setup -qc
mv %{modname}-%{version}*/* .
# all files with 1970 timestamp
find -newer php_dio_stream_wrappers.h -o -print | xargs touch --reference %{SOURCE0}

%build
phpize
%configure
%{__make}

%if %{with tests}
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
unset TZ LANG LC_ALL || :
%{__make} test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
