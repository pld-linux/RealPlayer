#
# Todo:
#	- add the licence agreement mechanism
#	- check if this works in opera/konqueror
#
%define		_name	realplay
Summary:	RealPlayer - RealAudio and RealVideo player
Summary(pl):	RealPlayer - odtwarzacz RealAudio i RealVideo
Name:		RealPlayer
%ifarch	%{ix86}
%define		minor_ver	7
%else
%define		minor_ver	5
%endif
Version:	10.0.%{minor_ver}
Release:	1
License:	Helix DNA Technology Binary Research Use License (not distributable, see LICENSE)
Group:		X11/Applications/Multimedia
# download from https://helixcommunity.org/project/showfiles.php?group_id=154
%ifarch %{ix86}
Source0:	RealPlayer10GOLD.rpm
# NoSource0-md5:	3de2e377fd6f00ea1de8f3016469fe5e
NoSource:	0
%endif
%ifarch ppc
Source1:	https://helixcommunity.org/download.php/1346/realplay-%{version}.756-linux-2.2-libc6-gcc32-powerpc.bin
# NoSource1-md5:	d87d35617f07ab9435341f37229dd3ae
NoSource:	1
%endif
URL:		http://www.real.com/linux/
BuildRequires:	cpio
BuildRequires:	rpmbuild(macros) >= 1.312
BuildRequires:	sed >= 4.0
Provides:	helix-core
Requires:	sed >= 4.0
Obsoletes:	G2player
Obsoletes:	RealPlayer-gnome
Conflicts:	realplayer
ExclusiveArch:	%{ix86} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_plugindir	%{_libdir}/browser-plugins
%define		browsers	mozilla, mozilla-firefox, netscape, seamonkey

%description
Streaming audio/video/flash/pix/text player.

%description -l pl
Odtwarzacz strumieni audio/video/flash/pix/tekst.

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
rpm2cpio %{SOURCE0} | cpio -dimu
mv -f usr/local/RealPlayer/* .
%endif
%ifarch ppc
dd if=%{SOURCE1} bs=1 skip=158895 | tar xjf -
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_plugindir} \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{_name},%{_datadir}/locale} \
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

cp -rf share/locale/* $RPM_BUILD_ROOT%{_datadir}/locale

install mozilla/*.{so,xpt} $RPM_BUILD_ROOT%{_plugindir}

install realplay* $RPM_BUILD_ROOT%{_libdir}/%{_name}
ln -sf ../lib/%{_name}/realplay $RPM_BUILD_ROOT%{_bindir}/realplay

install share/realplay.desktop $RPM_BUILD_ROOT%{_desktopdir}

install -d $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/{default,realplay}

install share/realplay/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/realplay
install share/default/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/default
install share/*.html $RPM_BUILD_ROOT%{_libdir}/%{_name}/share
install share/*.css $RPM_BUILD_ROOT%{_libdir}/%{_name}/share

%{__sed} -i -e 's&#[ \t]*HELIX_LIBS[ \t]*=.*$&HELIX_LIBS=%{_libdir}/%{_name} ; export HELIX_LIBS&' \
	$RPM_BUILD_ROOT%{_libdir}/realplay/realplay

# "player" and "widget" domains
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

%triggerin -- mozilla-firefox
%nsplugin_install -d %{_libdir}/mozilla-firefox/plugins nphelix.so nphelix.xpt

%triggerun -- mozilla-firefox
%nsplugin_uninstall -d %{_libdir}/mozilla-firefox/plugins nphelix.so nphelix.xpt

%triggerin -- mozilla
%nsplugin_install -d %{_libdir}/mozilla/plugins nphelix.so nphelix.xpt

%triggerun -- mozilla
%nsplugin_uninstall -d %{_libdir}/mozilla/plugins nphelix.so nphelix.xpt

#triggerin -- konqueror
#nsplugin_install -d %{_libdir}/kde3/plugins/konqueror nphelix.so

#triggerun -- konqueror
#nsplugin_uninstall -d %{_libdir}/kde3/plugins/konqueror nphelix.so

#triggerin -- opera
#nsplugin_install -d %{_libdir}/opera/plugins nphelix.so

#triggerun -- opera
#nsplugin_uninstall -d %{_libdir}/opera/plugins nphelix.so

%triggerin -- seamonkey
%nsplugin_install -d %{_libdir}/seamonkey/plugins nphelix.so nphelix.xpt

%triggerun -- seamonkey
%nsplugin_uninstall -d %{_libdir}/seamonkey/plugins nphelix.so nphelix.xpt

# as rpm removes the old obsoleted package files after the triggers
# above are ran, add another trigger to make the links there.
%triggerpostun -- mozilla-firefox-plugin-macromedia-flash
%nsplugin_install -f -d %{_libdir}/mozilla-firefox/plugins nphelix.so nphelix.xpt

%triggerpostun -- mozilla-plugin-macromedia-flash
%nsplugin_install -f -d %{_libdir}/mozilla/plugins nphelix.so nphelix.xpt

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc LICENSE README 
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

%{_iconsdir}/hicolor/*/*/*.png
%{_desktopdir}/*.desktop

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_plugindir}/*.so
%{_plugindir}/*.xpt
