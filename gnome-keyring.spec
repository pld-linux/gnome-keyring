Summary:	Keep passwords and other user's secrets
Summary(pl):	Przechowywanie hase³ i innych tajnych danych u¿ytkowników
Name:		gnome-keyring
Version:	0.1.2
Release:	1
License:	LGPL v2+/GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/%{name}/0.1/%{name}-%{version}.tar.bz2
# Source0-md5:	15ce1b6e53e5964d36fc7098c0123611
URL:		http://www.gnome.org/
BuildRequires:	glib2-devel >= 2.3.1
BuildRequires:	gtk+2-devel >= 2.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gnome Keyring is a program that keeps password and other secrets for
users. It is run as a deamon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

The library libgnome-keyring is used by applications to integrate with
the GNOME keyring system.

%description -l pl
Gnome Keyring to program do przechowywania hase³ i innych tajnych
danych u¿ytkowników. Dzia³a jako demon w sesji, podobnie do
ssh-agenta, a inne aplikacje mog± znale¼æ go poprzez zmienn±
¶rodowiskow±.

Biblioteka libgnome-keyring jest u¿ywana przez aplikacje do integracji
z systemem kluczy GNOME.

%package libs
Summary:	Gnome keyring library
Summary(pl):	Biblioteka gnome keyring
Group:		Libraries

%description libs
Gnome keyring library.

%description libs -l pl
Biblioteka gnome keyring.

%package devel
Summary:	Headers for gnome keyring library
Summary(pl):	Pliki nag³ówkowe biblioteki gnome keyring
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}
Requires:	glib2-devel >= 2.3.1

%description devel
Headers for gnome keyring library.

%description devel -l pl
Pliki nag³ówkowe biblioteki gnome keyring.

%package static
Summary:	Static gnome keyring libraries
Summary(pl):	Statyczne biblioteki gnome keyring
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static version of gnome keyring libraries.

%description static -l pl
Statyczne biblioteki gnome keyring.

%prep
%setup -q

%build
%configure \
	--enable-static 

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	pkgconfigdir=%{_pkgconfigdir}

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_pkgconfigdir}/*.pc
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
