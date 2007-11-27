%define		ocaml_ver	1:3.09.2
Summary:	PostgreSQL binding for OCaml
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla
Name:		ocaml-postgres
Version:	20040120
Release:	7
License:	LGPL v2
Group:		Libraries
URL:		http://www.eleves.ens.fr/home/frisch/soft
# note: no / at the end of URL
Source0:	http://www.eleves.ens.fr/home/frisch/info/postgres-%{version}.tar.gz
# Source0-md5:	08a8fb35c2101d7262dc25375018df34
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-findlib
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows OCaml programs to access PostgreSQL databases.
This package contains files needed to run bytecode OCaml programs
using this library.

%description -l pl.UTF-8
Biblioteka ta umożliwia programom pisanym w OCamlu dostęp do baz
danych PostgreSQL. Pakiet ten zawiera binaria potrzebne do
uruchamiania programów używających tej biblioteki.

%package devel
Summary:	PostgreSQL binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania PostgreSQL dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This library allows OCaml programs to access PostgreSQL databases.
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Biblioteka ta umożliwia programom pisanym w OCamlu dostęp do baz
danych PostgreSQL. Pakiet ten zawiera pliki niezbędne do tworzenia
programów używających tej biblioteki.

%prep
%setup -q -n postgres-%{version}

%build
%{__make} POSTGRES_INCLUDE='-I %{_includedir}/postgresql/server'

%{__cc} %{rpmcflags} -fpic \
	-I%{_includedir}/postgresql/server \
	-c libpq_stub.c

ocamlmklib -o postgres postgres.cm[xo] libpq_stub.o -lpq

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{postgres,stublibs}

install *.cm[ixa]* *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/postgres
install dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r tests/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# META for findlib
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/postgres
echo 'directory = "+postgres"' >> META
install META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/postgres

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dll*.so

%files devel
%defattr(644,root,root,755)
%doc README *.mli
%dir %{_libdir}/ocaml/postgres
%{_libdir}/ocaml/postgres/*.cm[ixa]*
%{_libdir}/ocaml/postgres/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/postgres
