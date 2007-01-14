#
# TODO:
# - check if Patch0 is needed
#
Summary:	Keep passwords and other user's secrets
Summary(pl):	Przechowywanie hase� i innych tajnych danych u�ytkownik�w
Name:		gnome-keyring
Version:	0.7.3
Release:	0.1
License:	LGPL v2+/GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-keyring/0.7/%{name}-%{version}.tar.bz2
# Source0-md5:	4478d21d3ef56a3992411bee7ab6df73
Patch0:		%{name}-single-unlock-dialog.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk+2-devel >= 2:2.10.2
BuildRequires:	gtk-doc >= 1.7
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Keyring is a program that keeps password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

The library libgnome-keyring is used by applications to integrate with
the GNOME keyring system.

%description -l pl
GNOME Keyring to program do przechowywania hase� i innych tajnych
danych u�ytkownik�w. Dzia�a jako demon w sesji, podobnie do
ssh-agenta, a inne aplikacje mog� znale�� go poprzez zmienn�
�rodowiskow�.

Biblioteka libgnome-keyring jest u�ywana przez aplikacje do integracji
z systemem kluczy GNOME.

%package libs
Summary:	GNOME keyring library
Summary(pl):	Biblioteka GNOME keyring
Group:		Libraries

%description libs
GNOME keyring library.

%description libs -l pl
Biblioteka GNOME keyring.

%package devel
Summary:	Headers for GNOME keyring library
Summary(pl):	Pliki nag��wkowe biblioteki GNOME keyring
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.10.3

%description devel
Headers for GNOME keyring library.

%description devel -l pl
Pliki nag��wkowe biblioteki GNOME keyring.

%package static
Summary:	Static GNOME keyring libraries
Summary(pl):	Statyczne biblioteki GNOME keyring
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of GNOME keyring libraries.

%description static -l pl
Statyczne biblioteki GNOME keyring.

%package apidocs
Summary:	GNOME keyring API documentation
Summary(pl):	Dokumentacja API GNOME keyring
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GNOME keyring API documentation.

%description apidocs -l pl
Dokumentacja API GNOME keyring.

%prep
%setup -q
#%patch0 -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--enable-static \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libexecdir}/%{name}-ask

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
