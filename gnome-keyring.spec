# TODO
#  Aug 14 13:19:00 haarber gnome-keyring-daemon[6524]: couldn't list keyrings at: /etc/certs: Error opening directory '/etc/certs': Permission denied
#
# Conditional build:
%bcond_with	p11_tests	# PKCS#11 tests
#
Summary:	Keep passwords and other user's secrets
Summary(pl.UTF-8):	Przechowywanie haseł i innych tajnych danych użytkowników
Name:		gnome-keyring
Version:	3.2.1
Release:	1
License:	LGPL v2+ (library), GPL v2+ (programs)
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-keyring/3.2/%{name}-%{version}.tar.xz
# Source0-md5:	ec1abc290c7a04415c6ad7675ba5de0c
URL:		http://live.gnome.org/GnomeKeyring
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	cairo-devel
BuildRequires:	dbus-devel >= 1.2.0
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gtk+3-devel >= 3.0.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcap-ng-devel
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libselinux-devel
BuildRequires:	libtasn1-devel >= 0.3.4
BuildRequires:	libtool
BuildRequires:	p11-kit-devel >= 0.6
%{?with_p11_tests:BuildRequires:	p11-tests-devel >= 0.1}
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
Requires:	dbus >= 1.2.0
Requires:	hicolor-icon-theme
Conflicts:	rpm < 4.4.2-0.2
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
GNOME Keyring is a program that keeps password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

%description -l pl.UTF-8
GNOME Keyring to program do przechowywania haseł i innych tajnych
danych użytkowników. Działa jako demon w sesji, podobnie do
ssh-agenta, a inne aplikacje mogą znaleźć go poprzez zmienną
środowiskową.

%package libs
Summary:	GNOME keyring support libraries
Summary(pl.UTF-8):	Biblioteki wspomagające GNOME keyring
License:	LGPL v2+
Group:		X11/Libraries
Requires:	dbus-libs >= 1.2.0
Requires:	glib2 >= 1:2.26.0
Requires:	libgcrypt >= 1.2.2
Requires:	p11-kit >= 0.6

%description libs
GNOME keyring support libraries:
- gck: GObject bindings for PKCS#11
- gcr: GObject and GUI library for high level crypto parsing and
  display

%description libs -l pl.UTF-8
Biblioteki wspomagające GNOME keyring:
- gck: wiązania GObject do PKCS#11
- gcr: biblioteka GObject i GUI do wysokopoziomowej analizy i
  wyświetlania danych związanych z kryptografią.

%package devel
Summary:	Headers for GNOME keyring support libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek wspomagających GNOME keyring
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 1.2.0
Requires:	glib2-devel >= 1:2.26.0
Requires:	gtk+3-devel >= 3.0.0
Requires:	libgcrypt-devel >= 1.2.2
Requires:	p11-kit-devel >= 0.6

%description devel
Headers for GNOME keyring support libraries (gck and gcr).

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek wspomagających GNOME keyring (gck i gcr).

%package static
Summary:	Static GNOME keyring support libraries
Summary(pl.UTF-8):	Statyczne biblioteki wspomagające GNOME keyring
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GNOME keyring support libraries (gck and gcr).

%description static -l pl.UTF-8
Statyczne biblioteki wspomagające GNOME keyring (gck i gcr).

%package apidocs
Summary:	GNOME keyring (gck and gcr) API documentation
Summary(pl.UTF-8):	Dokumentacja API GNOME keyring (gck i gcr)
License:	LGPL v2+
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
GNOME keyring (gck and gcr) API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API GNOME keyring (gck i gcr).

%package -n pam-pam_gnome_keyring
Summary:	A PAM module for unlocking keyrings at login time
Summary(pl.UTF-8):	Moduł PAM do odblokowywania zbiorów kluczy w czasie logowania
License:	LGPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	gnome-keyring-pam

%description -n pam-pam_gnome_keyring
A PAM module that can automatically unlock the "login" keyring when
the user logs in and start the keyring daemon.

%description -n pam-pam_gnome_keyring -l pl.UTF-8
Moduł PAM, który może automatycznie odblokowywać zbiór kluczy "login"
w czasie logowania użytkownika i uruchamiania demona keyring.

%prep
%setup -q

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_p11_tests:--disable-p11-tests} \
	--disable-tests \
	--enable-gtk-doc \
	--enable-static \
	--with-html-dir=%{_gtkdocdir} \
	--with-pam-dir=/%{_lib}/security \
	--with-root-certs=%{_sysconfdir}/certs
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install-pam \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/pam_gnome_keyring.{l,}a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pkcs11/gnome-keyring-pkcs11.{l,}a
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gnome-keyring/devel/*.{l,}a

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_mime_database
%update_desktop_database_post
%update_icon_cache hicolor
%glib_compile_schemas

%postun
%update_mime_database
%update_desktop_database_postun
%update_icon_cache hicolor
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/gcr-viewer
%attr(755,root,root) %{_bindir}/gnome-keyring
%attr(755,root,root) %{_bindir}/gnome-keyring-3
%attr(755,root,root) %{_bindir}/gnome-keyring-daemon
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libexecdir}/gnome-keyring-prompt
%attr(755,root,root) %{_libexecdir}/gnome-keyring-prompt-3
%attr(755,root,root) %{_libdir}/pkcs11/gnome-keyring-pkcs11.so
%dir %{_libdir}/%{name}/devel
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-gnome2-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-roots-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-secret-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-ssh-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-xdg-store-standalone.so
%{_sysconfdir}/xdg/autostart/gnome-keyring-gpg.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-secrets.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-ssh.desktop
%{_datadir}/GConf/gsettings/*.convert
%{_datadir}/dbus-1/services/org.freedesktop.secrets.service
%{_datadir}/dbus-1/services/org.gnome.keyring.service
%{_datadir}/gcr-3
%{_datadir}/glib-2.0/schemas/*.gschema.xml
%{_datadir}/gnome-keyring-3
%{_desktopdir}/gcr-viewer.desktop
%{_desktopdir}/gnome-keyring-prompt.desktop
%{_sysconfdir}/pkcs11/modules/gnome-keyring-module
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/mime/packages/gcr-crypto-types.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgcr-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcr-3.so.1
%attr(755,root,root) %{_libdir}/libgck-1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgck-1.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgcr-3.so
%attr(755,root,root) %{_libdir}/libgck-1.so
%{_includedir}/gcr-3
%{_includedir}/gck-1
%{_pkgconfigdir}/gcr-3.pc
%{_pkgconfigdir}/gck-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libgcr-3.a
%{_libdir}/libgck-1.a

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gcr-3
%{_gtkdocdir}/gck

%files -n pam-pam_gnome_keyring
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_gnome_keyring.so
