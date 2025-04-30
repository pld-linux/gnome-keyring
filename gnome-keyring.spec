# TODO
#  Aug 14 13:19:00 haarber gnome-keyring-daemon[6524]: couldn't list keyrings at: /etc/certs: Error opening directory '/etc/certs': Permission denied
#
# Conditional build:
%bcond_with	p11_tests	# PKCS#11 tests
#
Summary:	Keep passwords and other user's secrets
Summary(pl.UTF-8):	Przechowywanie haseł i innych tajnych danych użytkowników
Name:		gnome-keyring
Version:	48.0
Release:	1
License:	LGPL v2+ (library), GPL v2+ (programs)
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/gnome-keyring/48/%{name}-%{version}.tar.xz
# Source0-md5:	d19a99eadeb5d92774b7960c51d1c5dc
URL:		https://wiki.gnome.org/Projects/GnomeKeyring
BuildRequires:	docbook-dtd412-xml
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	gcr-devel >= 3.28.0
BuildRequires:	gcr-ui-devel >= 3.28.0
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	glib2-devel >= 1:2.80
BuildRequires:	libcap-ng-devel
BuildRequires:	libgcrypt-devel >= 1.2.2
BuildRequires:	libselinux-devel
# for some test only
BuildRequires:	libtasn1-devel >= 0.3.4
BuildRequires:	libxslt-progs
BuildRequires:	meson >= 1.0
BuildRequires:	ninja >= 1.5
# for ssh-agent,ssh-add binaries detection by meson
BuildRequires:	openssh-clients
BuildRequires:	p11-kit-devel >= 0.16
%{?with_p11_tests:BuildRequires:	p11-tests-devel >= 0.1}
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.80
Requires:	filesystem >= 4.0-28
Requires:	gcr >= 3.28.0
Requires:	glib2 >= 1:2.80
Requires:	hicolor-icon-theme
Requires:	libgcrypt >= 1.2.2
Requires:	p11-kit >= 0.16
Conflicts:	rpm < 4.4.2-0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GNOME Keyring is a program that keeps password and other secrets for
users. It is run as a daemon in the session, similar to ssh-agent, and
other applications can locate it by an environment variable.

%description -l pl.UTF-8
GNOME Keyring to program do przechowywania haseł i innych tajnych
danych użytkowników. Działa jako demon w sesji, podobnie do
ssh-agenta, a inne aplikacje mogą znaleźć go poprzez zmienną
środowiskową.

%package -n pam-pam_gnome_keyring
Summary:	A PAM module for unlocking keyrings at login time
Summary(pl.UTF-8):	Moduł PAM do odblokowywania zbiorów kluczy w czasie logowania
License:	LGPL v2+
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	gnome-keyring-pam < 2.30.1-2

%description -n pam-pam_gnome_keyring
A PAM module that can automatically unlock the "login" keyring when
the user logs in and start the keyring daemon.

%description -n pam-pam_gnome_keyring -l pl.UTF-8
Moduł PAM, który może automatycznie odblokowywać zbiór kluczy "login"
w czasie logowania użytkownika i uruchamiania demona keyring.

%prep
%setup -q

%build
%meson \
	-Dselinux=enabled \
	-Dssh-agent=true \
	-Dsystemd=enabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

# meson.build doesn't support split /usr, adjust manually
install -d $RPM_BUILD_ROOT/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/security $RPM_BUILD_ROOT/%{_lib}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas

%postun
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/gnome-keyring
%attr(755,root,root) %{_bindir}/gnome-keyring-3
%attr(755,root,root) %{_bindir}/gnome-keyring-daemon
%attr(755,root,root) %{_libdir}/pkcs11/gnome-keyring-pkcs11.so
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/devel
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-gnome2-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-secret-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-ssh-store-standalone.so
%attr(755,root,root) %{_libdir}/%{name}/devel/gkm-xdg-store-standalone.so
%{_sysconfdir}/xdg/autostart/gnome-keyring-pkcs11.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-secrets.desktop
%{_sysconfdir}/xdg/autostart/gnome-keyring-ssh.desktop
%{_datadir}/GConf/gsettings/org.gnome.crypto.cache.convert
%{_datadir}/dbus-1/services/org.freedesktop.impl.portal.Secret.service
%{_datadir}/dbus-1/services/org.freedesktop.secrets.service
%{_datadir}/dbus-1/services/org.gnome.keyring.service
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.cache.gschema.xml
%{_datadir}/p11-kit/modules/gnome-keyring.module
%{_datadir}/xdg-desktop-portal/portals/gnome-keyring.portal
%{systemduserunitdir}/gnome-keyring-daemon.service
%{systemduserunitdir}/gnome-keyring-daemon.socket
%{_mandir}/man1/gnome-keyring.1*
%{_mandir}/man1/gnome-keyring-3.1*
%{_mandir}/man1/gnome-keyring-daemon.1*

%files -n pam-pam_gnome_keyring
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/security/pam_gnome_keyring.so
