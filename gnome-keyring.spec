Summary:	Keep passwords and other user's secrets
Summary(pl.UTF-8):	Przechowywanie haseł i innych tajnych danych użytkowników
Name:		gnome-keyring
Version:	2.20.2
Release:	1
License:	LGPL v2+/GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-keyring/2.20/%{name}-%{version}.tar.bz2
# Source0-md5:	0a868f7f661a0ca8fecaf3c55931f489
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel >= 1.1.2
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	gtk-doc >= 1.8
BuildRequires:	hal-devel >= 0.5.9
BuildRequires:	intltool >= 0.36.2
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libtool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.197
Requires:	dbus >= 1.1.2
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Keyring is a program that keeps password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

The library libgnome-keyring is used by applications to integrate with
the GNOME keyring system.

%description -l pl.UTF-8
GNOME Keyring to program do przechowywania haseł i innych tajnych
danych użytkowników. Działa jako demon w sesji, podobnie do
ssh-agenta, a inne aplikacje mogą znaleźć go poprzez zmienną
środowiskową.

Biblioteka libgnome-keyring jest używana przez aplikacje do integracji
z systemem kluczy GNOME.

%package libs
Summary:	GNOME keyring library
Summary(pl.UTF-8):	Biblioteka GNOME keyring
Group:		Libraries

%description libs
GNOME keyring library.

%description libs -l pl.UTF-8
Biblioteka GNOME keyring.

%package devel
Summary:	Headers for GNOME keyring library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GNOME keyring
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 1.1.2
Requires:	glib2-devel >= 1:2.14.1

%description devel
Headers for GNOME keyring library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GNOME keyring.

%package static
Summary:	Static GNOME keyring libraries
Summary(pl.UTF-8):	Statyczne biblioteki GNOME keyring
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of GNOME keyring libraries.

%description static -l pl.UTF-8
Statyczne biblioteki GNOME keyring.

%package apidocs
Summary:	GNOME keyring API documentation
Summary(pl.UTF-8):	Dokumentacja API GNOME keyring
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GNOME keyring API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GNOME keyring.

%package pam
Summary:	A PAM module for unlocking keyrings at login time
Summary(pl.UTF-8):	Moduł PAM do odblokowywania zbiorów kluczy w czasie logowania
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description pam
A PAM module that can automatically unlock the "login" keyring when
the user logs in and start the keyring daemon.

%description pam -l pl.UTF-8
Moduł PAM, który może automatycznie odblokowywać zbiór kluczy "login"
w czasie logowania użytkownika i uruchamiania demona keyring.

%prep
%setup -q

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-gtk-doc \
	--enable-static \
	--with-html-dir=%{_gtkdocdir} \
	--with-pam-dir=/%{_lib}/security
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-pam \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

rm -f $RPM_BUILD_ROOT/%{_lib}/security/pam_gnome_keyring.{l,}a
rm -f $RPM_BUILD_ROOT%{_libdir}/pam_gnome_keyring*

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
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

%files pam
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_gnome_keyring*.so
