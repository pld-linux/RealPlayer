# TODO:
#	- add the licence agreement mechanism
#	- check if this works in opera/konqueror
# NOTE: there are partial sources available
# (https://helixcommunity.org/frs/download.php/2153/realplay-10.0.8-source.tar.bz2)
# but included binary blobs are only for x86
#
# Conditional build:
%bcond_without	autodeps	# don't BR packages needed only for resolving deps
#
%define		_name	realplay
Summary:	RealPlayer - RealAudio and RealVideo player
Summary(pl):	RealPlayer - odtwarzacz RealAudio i RealVideo
Name:		RealPlayer
%ifarch	%{ix86}
%define		minor_ver	8
%else
%define		minor_ver	5
%endif
Version:	10.0.%{minor_ver}
Release:	1
License:	Helix DNA Technology Binary Research Use License (not distributable, see LICENSE)
Group:		X11/Applications/Multimedia
# download from https://helixcommunity.org/project/showfiles.php?group_id=154
%ifarch %{ix86}
Source0:	https://helixcommunity.org/frs/download.php/2151/realplay-%{version}.805-linux-2.2-libc6-gcc32-i586.bin
# NoSource0-md5:	d28b31261059231a3e93c7466f8153e6
NoSource:	0
%endif
%ifarch ppc
Source1:	https://helixcommunity.org/frs/download.php/1346/realplay-%{version}.756-linux-2.2-libc6-gcc32-powerpc.bin
# NoSource1-md5:	d87d35617f07ab9435341f37229dd3ae
NoSource:	1
%endif
Patch0:		realplayer-desktop.patch
URL:		http://www.real.com/linux/
BuildRequires:	cpio
BuildRequires:	rpmbuild(macros) >= 1.312
BuildRequires:	sed >= 4.0
%if %{with autodeps}
BuildRequires:	atk
BuildRequires:	glib2
BuildRequires:	gtk+2
BuildRequires:	libgcc
BuildRequires:	libstdc++
BuildRequires:	pango
%endif
Requires(post,postun):	hicolor-icon-theme
Requires:	sed >= 4.0
Provides:	helix-core
Obsoletes:	G2player
Obsoletes:	RealPlayer-gnome
Obsoletes:	realplayer
ExclusiveArch:	%{ix86} ppc
ExcludeArch:	i386 i486
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins
%define		browsers	mozilla, mozilla-firefox, netscape, seamonkey
%define		_noautocompressdoc  LICENSE README

%description
Streaming audio/video/flash/pix/text player.
%ifarch ppc

WARNING: this package is vulnerable - see CVE-2006-0323!
%endif

%description -l pl
Odtwarzacz strumieni audio/video/flash/pix/tekst.
%ifarch ppc

UWAGA: ten pakiet jest niebezpieczny - szczegó³y w CVE-2006-0323!
%endif

%package -n browser-plugin-%{name}
Summary:	RealPlayer plugin for WWW browsers
Summary(pl):	Wtyczka RealPlayer do przegl±darek WWW
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins(%{_target_base_arch})

%description -n browser-plugin-%{name}
RealPlayer plugin for WWW browsers.

Supported browsers: %{browsers}.

%description -n browser-plugin-%{name} -l pl
Wtyczka RealPlayer dla przegl±darek WWW.

Obs³ugiwane przegl±darki: %{browsers}.

%prep
%setup -q -c -T
%ifarch %{ix86}
dd if=%{SOURCE0} bs=1 skip=143273 | tar xjf -
%endif
%ifarch ppc
dd if=%{SOURCE1} bs=1 skip=158895 | tar xjf -
%endif
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_plugindir} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{_name}} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/{48x48,128x128}/mimetypes \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}/apps

cp -a codecs common plugins lib $RPM_BUILD_ROOT%{_libdir}/%{_name}

icons="mime-application-generic \
mime-application-ogg \
mime-application-ram \
mime-application-rpm \
mime-application-smil \
mime-audio-aiff \
mime-audio-au \
mime-audio-generic \
mime-audio-mp3 \
mime-audio-mp4 \
mime-audio-ogg \
mime-audio-ra \
mime-audio-wav \
mime-text-realtext \
mime-video-avi \
mime-video-generic \
mime-video-mov \
mime-video-ogg \
mime-video-rv \
mime-video-swf"

cd share/icons
for i in $icons; 
do
install ${i}_48x48.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/mimetypes/${i}.png
# SIC! there is no 192 size defined in hicolor, therefore use 128
install ${i}_192x192.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/128x128/mimetypes/${i}.png
done
install realplay_16x16.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/realplay.png
install realplay_32x32.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/realplay.png
install realplay_48x48.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/realplay.png
install realplay_192x192.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/128x128/apps/realplay.png
cd -

# install locales in proper domains
cd share/locale
for LC in *; do
	install -d $RPM_BUILD_ROOT%{_datadir}/locale/${LC}/LC_MESSAGES
	cp -a ${LC}/player.mo $RPM_BUILD_ROOT%{_datadir}/locale/${LC}/LC_MESSAGES/realplay.mo
	cp -a ${LC}/widget.mo $RPM_BUILD_ROOT%{_datadir}/locale/${LC}/LC_MESSAGES/libgtkhx.mo
done
cd ../..

install mozilla/*.{so,xpt} $RPM_BUILD_ROOT%{_plugindir}

install realplay* $RPM_BUILD_ROOT%{_libdir}/%{_name}
ln -sf ../%{_lib}/%{_name}/realplay $RPM_BUILD_ROOT%{_bindir}/realplay

install share/realplay.desktop $RPM_BUILD_ROOT%{_desktopdir}

install -d $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/{default,realplay}

install share/realplay/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/realplay
install share/default/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/default
install share/*.html $RPM_BUILD_ROOT%{_libdir}/%{_name}/share
install share/*.css $RPM_BUILD_ROOT%{_libdir}/%{_name}/share
cp -a README LICENSE $RPM_BUILD_ROOT%{_libdir}/%{_name}
rm -rf docs
install -d docs
ln -s %{_libdir}/%{_name}/README docs
ln -s %{_libdir}/%{_name}/LICENSE docs

%{__sed} -i -e 's&#[ \t]*HELIX_LIBS[ \t]*=.*$&HELIX_LIBS=%{_libdir}/%{_name} ; export HELIX_LIBS&' \
	$RPM_BUILD_ROOT%{_libdir}/realplay/realplay

# "realplay" and "libgtkhx" domains
%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:
%update_icon_cache hicolor

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1
%update_icon_cache hicolor

%triggerin -n browser-plugin-%{name} -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins nphelix.so nphelix.xpt

%triggerun -n browser-plugin-%{name} -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins nphelix.so nphelix.xpt

%triggerin -n browser-plugin-%{name} -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins nphelix.so nphelix.xpt

%triggerun -n browser-plugin-%{name} -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins nphelix.so nphelix.xpt

#triggerin -n browser-plugin-%{name} -- konqueror
#nsplugin_install -d %{_libdir}/kde3/plugins/konqueror nphelix.so

#triggerun -n browser-plugin-%{name} -- konqueror
#nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror nphelix.so

#triggerin -n browser-plugin-%{name} -- opera
#nsplugin_install -d %{_libdir}/opera/plugins nphelix.so

#triggerun -n browser-plugin-%{name} -- opera
#nsplugin_uninstall -d %{_libdir}/opera/plugins nphelix.so

%triggerin -n browser-plugin-%{name} -- seamonkey
%nsplugin_install -d %{_libdir}/seamonkey/plugins nphelix.so nphelix.xpt

%triggerun -n browser-plugin-%{name} -- seamonkey
%nsplugin_uninstall -d %{_libdir}/seamonkey/plugins nphelix.so nphelix.xpt

# as rpm removes the old obsoleted package files after the triggers
# above are ran, add another trigger to make the links there.
%triggerpostun -n browser-plugin-%{name} -- mozilla-firefox-plugin-RealPlaer
%nsplugin_install -f -d %{_libdir}/mozilla-firefox/plugins nphelix.so nphelix.xpt

%triggerpostun -n browser-plugin-%{name} -- mozilla-plugin-RealPlayer
%nsplugin_install -f -d %{_libdir}/mozilla/plugins nphelix.so nphelix.xpt

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc docs/{LICENSE,README}
%attr(755,root,root) %{_bindir}/realplay
%dir %{_libdir}/%{_name}
%dir %{_libdir}/%{_name}/codecs
%attr(755,root,root) %{_libdir}/%{_name}/codecs/*.so*
%dir %{_libdir}/%{_name}/common
%attr(755,root,root) %{_libdir}/%{_name}/common/*.so*
%dir %{_libdir}/%{_name}/lib
%attr(755,root,root) %{_libdir}/%{_name}/lib/*.so*
%dir %{_libdir}/%{_name}/plugins
%attr(755,root,root) %{_libdir}/%{_name}/plugins/*.so*
%attr(755,root,root) %{_libdir}/%{_name}/realplay
%attr(755,root,root) %{_libdir}/%{_name}/realplay.bin
%{_libdir}/%{_name}/share
%{_libdir}/%{_name}/LICENSE
%{_libdir}/%{_name}/README
%{_iconsdir}/hicolor/*/*/*.png
%{_desktopdir}/*.desktop

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/*.so
%{_plugindir}/*.xpt
