%define		_name	realplay
Summary:	RealPlayer - RealAudio and RealVideo player
Summary(pl):	RealPlayer - odtwarzacz RealAudio i RealVideo
Name:		RealPlayer
Version:	10.0.3
Release:	1
License:	Helix DNA Technology Binary Research Use License (not distributable, see LICENSE)
Group:		X11/Applications/Multimedia
# download from https://helixcommunity.org/project/showfiles.php?group_id=154
%ifarch %{ix86}
Source0:	https://helixcommunity.org/download.php/964/%{name}-%{version}.748-20050223.i586.rpm
# NoSource0-md5:	cea221a981b26c27e6e50a58aa285011
NoSource:	0
%endif
%ifarch ppc
Source1:	https://helixcommunity.org/download.php/973/realplay-%{version}.748-linux-2.2-powerpc.bin
# NoSource1-md5:	f7ab7ddb4f7f53df0f16445c6df4caa2
NoSource:	1
%endif
URL:		http://www.real.com/
BuildRequires:	cpio
BuildRequires:	sed >= 4.0
Requires:	sed >= 4.0
Obsoletes:	G2player
Conflicts:	realplayer
ExclusiveArch:	%{ix86} ppc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Streaming audio/video/flash/pix/text player.

%description -l pl
Odtwarzacz strumieni audio/video/flash/pix/tekst.

%package -n mozilla-plugin-%{name}
Summary:	RealPlayer Mozilla plugin
Summary(pl):	Wtyczka Mozilli RealPlayer
Group:		X11/Applications/Multimedia
PreReq:		mozilla-embedded
Requires:	%{name} = %{version}-%{release}

%description -n mozilla-plugin-%{name}
RealPlayer Mozilla plugin

%description -n mozilla-plugin-%{name} -l pl
Wtyczka Mozilli RealPlayer

%package -n mozilla-firefox-plugin-%{name}
Summary:	RealPlayer Mozilla Firefox plugin
Summary(pl):	Wtyczka Mozilli Firefox RealPlayer
Group:		X11/Applications/Multimedia
PreReq:		mozilla-firefox
Requires:	%{name} = %{version}-%{release}

%description -n mozilla-firefox-plugin-%{name}
RealPlayer Mozilla plugin

%description -n mozilla-firefox-plugin-%{name} -l pl
Wtyczka Mozilli RealPlayer

%package gnome
Summary:	GNOME data for Realplayer
Summary(pl):	Dane Realplayera dla GNOME
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-mime-data

%description gnome
Mime information and application registry data for GNOME.

%description gnome -l pl
Dane MIME oraz wpisy do rejestru aplikacji dla GNOME.

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
	$RPM_BUILD_ROOT%{_libdir}/mozilla/plugins \
	$RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/plugins \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{_name},%{_datadir}/locale} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/{48x48,128x128}/mimetypes \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}/apps \
	$RPM_BUILD_ROOT%{_datadir}/{application-registry,mime-info}

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

install mozilla/*.{so,xpt} $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
install mozilla/*.{so,xpt} $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/plugins

install realplay* $RPM_BUILD_ROOT%{_libdir}/%{_name}
ln -sf ../lib/%{_name}/realplay $RPM_BUILD_ROOT%{_bindir}/realplay

install share/realplay.applications $RPM_BUILD_ROOT%{_datadir}/application-registry
install share/realplay.mime $RPM_BUILD_ROOT%{_datadir}/mime-info
install share/realplay.keys $RPM_BUILD_ROOT%{_datadir}/mime-info

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

%postun
umask 022
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

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

%files gnome
%defattr(644,root,root,755)
%{_datadir}/application-registry/*.applications
%{_datadir}/mime-info/*

%files -n mozilla-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mozilla/plugins/*.so
%{_libdir}/mozilla/plugins/*.xpt

%files -n mozilla-firefox-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/mozilla-firefox/plugins/*.so
%{_libdir}/mozilla-firefox/plugins/*.xpt
