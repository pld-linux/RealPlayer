%define		_name	realplay
Summary:	Welcome to RealPlayer 10!
Summary(pl):	RealPlayer - odtwarzacz RealAudio i RealVideo
Name:		RealPlayer
Version:	10
Release:	1
License:	Helix DNA Technology Binary Research Use License (not distributable, see LICENSE)
Group:		X11/Applications/Multimedia
URL:		http://www.real.com/
Source0:	http://software-dl.real.com/06c1f73fd206f3264217/unix/%{name}%{version}GOLD.bin
# NoSource0-md5:	1e6435241bfb0ea6c015ec717fbf141a
Conflicts:	realplayer
Obsoletes:	G2player
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
NoSource:	0
ExclusiveArch:	%{ix86} 

%description
Streaming audio/video/flash/pix/text player.

%description -l pl
Odtwarzacz strumieni audio/video/flash/pix/tekst.

%package -n mozilla-plugin-%{name}
Summary:	RealPlayer Mozilla plugin
Summary(pl):	Wtyczka Mozilli RealPlayer
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}
Prereq:		mozilla-embedded

%description -n mozilla-plugin-%{name}
RealPlayer Mozilla plugin

%description -n mozilla-plugin-%{name} -l pl
Wtyczka Mozilli RealPlayer

%package -n mozilla-firefox-plugin-%{name}
Summary:        RealPlayer Mozilla Firefox plugin
Summary(pl):    Wtyczka Mozilli Firefox RealPlayer
Group:          X11/Applications/Multimedia
Requires:       %{name} = %{version}
Prereq:         mozilla-firefox

%description -n mozilla-firefox-plugin-%{name}
RealPlayer Mozilla plugin

%description -n mozilla-firefox-plugin-%{name} -l pl
Wtyczka Mozilli RealPlayer

%package gnome
Summary:	GNOME data for Realplayer
Summary(pl):	Dane Realplayera dla GNOME
Group:		X11/Applications/Multimedia
Requires:	%{name} = %{version}
Requires:	gnome-libs

%description gnome
Mime information and application registry data for GNOME.

%description gnome -l pl
Dane MIME oraz wpisy do rejestru aplikacji dla GNOME.


%prep
%setup -q -c -T
dd if=%{SOURCE0} skip=1 bs=129460| %{__bzip2} -d | %{__tar} xvf -

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_desktopdir} \
	$RPM_BUILD_ROOT%{_libdir}/mozilla/plugins \
	$RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/plugins \
	$RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{_name},%{_datadir}/{locale}} \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/{48x48,128x128}/mimetypes \
	$RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48,128x128}/apps \
	$RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES \
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

install share/locale/fr.mo $RPM_BUILD_ROOT%{_datadir}/locale/fr/LC_MESSAGES/realplay.mo

install mozilla/*.so $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins
install mozilla/*.so $RPM_BUILD_ROOT%{_libdir}/mozilla-firefox/plugins

install realplay*  $RPM_BUILD_ROOT%{_libdir}/%{_name}
ln -sf ../lib/%{_name}/realplay $RPM_BUILD_ROOT%{_bindir}/realplay

install share/realplay.applications $RPM_BUILD_ROOT%{_datadir}/application-registry
install share/realplay.mime $RPM_BUILD_ROOT%{_datadir}/mime-info
install share/realplay.keys $RPM_BUILD_ROOT%{_datadir}/mime-info

install share/realplay.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a share/realplay $RPM_BUILD_ROOT%{_datadir}

install -d $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/default

install share/default/* $RPM_BUILD_ROOT%{_libdir}/%{_name}/share/default
install share/*.html $RPM_BUILD_ROOT%{_libdir}/%{_name}/share
install share/*.css $RPM_BUILD_ROOT%{_libdir}/%{_name}/share
%{__sed} -i -e "s%#[ \t]*HELIX_LIBS[ \t]*=.*$%HELIX_LIBS=%{_libdir}/%{_name} ; export HELIX_LIBS%" \
	$RPM_BUILD_ROOT%{_libdir}/realplay

%find_lang realplay

%clean
rm -rf $RPM_BUILD_ROOT

%files -f realplay.lang
%defattr(644,root,root,755)
%doc LICENSE README 
%attr(755,root,root) %{_bindir}/realplay
%dir %{_libdir}/%{_name}
%dir %{_libdir}/%{_name}/codecs
%dir %{_libdir}/%{_name}/common
%dir %{_libdir}/%{_name}/lib
%dir %{_libdir}/%{_name}/plugins

%attr(755,root,root) %{_libdir}/%{_name}/codecs/*.so*
%attr(755,root,root) %{_libdir}/%{_name}/common/*.so*
%attr(755,root,root) %{_libdir}/%{_name}/lib/*.so*
%attr(755,root,root) %{_libdir}/%{_name}/plugins/*.so*
%attr(755,root,root) %{_libdir}/%{_name}/realplay*
%{_libdir}/%{_name}/share
%{_datadir}/%{_name}
%{_iconsdir}/hicolor/*/*/*.png
%{_desktopdir}/*.desktop

%files gnome
%defattr(644,root,root,755)
%{_datadir}/application-registry
%{_datadir}/mime-info

%files -n mozilla-plugin-%{name}
%defattr(644,root,root,755)
%{_libdir}/mozilla/plugins/*

%files -n mozilla-firefox-plugin-%{name}
%defattr(644,root,root,755)
%{_libdir}/mozilla-firefox/plugins/*
