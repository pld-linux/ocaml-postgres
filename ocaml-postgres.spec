Summary:	PostgreSQL binding for OCaml
Summary(pl):	Wi±zania PostgreSQL dla OCamla
Name:		ocaml-postgres
Version:	20010808
Release:	1
License:	LGPL
Group:		Libraries
Vendor:		Alain Frisch <Alain.Frisch@ens.fr>
Source0:	http://www.eleves.ens.fr/home/frisch/info/postgres-%{version}.tar.gz
# Source0-md5:	a6b03ad1636d0dc8b6b5da86bd5c17b6
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	ocaml
BuildRequires:	ocaml-findlib
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library allows OCaml programs to access PostgreSQL databases.
This package contains files needed to run bytecode OCaml programs
using this library.

%description -l pl
Biblioteka ta umo¿liwia programom pisanym w OCamlu dostêp do baz
danych PostgreSQL. Pakiet ten zawiera binaria potrzebne do
uruchamiania programów u¿ywaj±cych tej biblioteki.

%package devel
Summary:	PostgreSQL binding for OCaml - development part
Summary(pl):	Wi±zania PostgreSQL dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This library allows OCaml programs to access PostgreSQL databases.
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
Biblioteka ta umo¿liwia programom pisanym w OCamlu dostêp do baz
danych PostgreSQL. Pakiet ten zawiera pliki niezbêdne do tworzenia
programów u¿ywaj±cych tej biblioteki.

%prep
%setup -q -n postgres-%{version}

%build
%{__make} POSTGRES_INCLUDE=%{_includedir}/postgresql/server

%{__cc} %{rpmcflags} -fpic \
	-I%{_includedir}/postgresql/server \
	-c libpq_stub.c

ocamlmklib -o postgres postgres.cm[xo] libpq_stub.o -lpq

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/postgres
install *.cm[ixa]* *.a dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/postgres
(cd $RPM_BUILD_ROOT%{_libdir}/ocaml && ln -s postgres/dll*.so .)

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
%dir %{_libdir}/ocaml/postgres
%attr(755,root,root) %{_libdir}/ocaml/postgres/*.so
%{_libdir}/ocaml/*.so

%files devel
%defattr(644,root,root,755)
%doc README *.mli
%{_libdir}/ocaml/postgres/*.cm[ixa]*
%{_libdir}/ocaml/postgres/*.a
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/postgres
