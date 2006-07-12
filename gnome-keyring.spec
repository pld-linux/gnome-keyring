Summary:	Keep passwords and other user's secrets
Summary(pl):	Przechowywanie hase³ i innych tajnych danych u¿ytkowników
Name:		gnome-keyring
Version:	0.5.1
Release:	2
License:	LGPL v2+/GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/gnome-keyring/0.5/%{name}-%{version}.tar.bz2
# Source0-md5:	63e3614d864198d7793b1dba9189e992
Patch0:		%{name}-single-unlock-dialog.patch
URL:		http://www.gnome.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.12.0
BuildRequires:	gtk+2-devel >= 2:2.10.0
BuildRequires:	gtk-doc >= 1.6
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
GNOME Keyring to program do przechowywania hase³ i innych tajnych
danych u¿ytkowników. Dzia³a jako demon w sesji, podobnie do
ssh-agenta, a inne aplikacje mog± znale¼æ go poprzez zmienn±
¶rodowiskow±.

Biblioteka libgnome-keyring jest u¿ywana przez aplikacje do integracji
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
Summary(pl):	Pliki nag³ówkowe biblioteki GNOME keyring
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= 1:2.10.0

%description devel
Headers for GNOME keyring library.

%description devel -l pl
Pliki nag³ówkowe biblioteki GNOME keyring.

%package static
Summary:	Static GNOME keyring libraries
Summary(pl):	Statyczne biblioteki GNOME keyring
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static versions of GNOME keyring libraries.

%description static -l pl
Statyczne biblioteki GNOME keyring.

%prep
%setup -q
%patch0 -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
LDFLAGS="%{rpmldflags} -Wl,--as-needed"
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
%{_gtkdocdir}/%{name}

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
