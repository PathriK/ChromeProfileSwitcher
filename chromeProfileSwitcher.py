#! /usr/bin/env python3

import json
from string import Template

chromeProfiles = "/home/pathrik/.config/google-chrome/Local State"
appPath = "/home/pathrik/.local/share/applications"
appName = "chrome-profiles.desktop"

contentsBase = """[Desktop Entry]
Version=1.0
Name=Chrome Profiles
GenericName=Web Browser
Comment=Access the Internet
Exec=/usr/bin/google-chrome-stable --profile-directory=Default %U
StartupNotify=true
Terminal=false
Icon=google-chrome
Type=Application
Categories=Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml_xml;image/webp;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;
StartupWMClass=google-chrome"""

profileTemp = Template("--profile-directory=${profileDir}")
contentActionKey = "Actions="
contentActions = [
    {
        'id': "new-window",
        'name': "New Window",
        'param': profileTemp.substitute(profileDir="Default")
    },
    {
        'id': "new-private-window",
        'name': "New Incognito Window",
        'param': "--incognito " + profileTemp.substitute(profileDir="Default")
    }
]

contentActionTempl = Template(
    """[Desktop Action ${id}]
Name=${name}
Exec=/usr/bin/google-chrome-stable ${param}
"""
)

with open(chromeProfiles) as json_file:
    data = json.load(json_file)
    for profName, profData in data['profile']['info_cache'].items():
        # print(profName)
        # print(profData['gaia_given_name'])
        name = profData['gaia_given_name'] if 'gaia_given_name' in profData else profData['name']
        if("Default" == profName):
            continue
        contentActions.append({
            'id': profName.lower().replace(' ', '_'),
            'name': name,
            'param': profileTemp.substitute(profileDir=profName.replace(' ', r'\ '))
        })


fileContents = contentsBase + "\n" + contentActionKey + \
    ";".join(map(lambda action: action['id'], contentActions)) + ";\n\n" + \
    "\n".join(
        map(lambda action: contentActionTempl.substitute(action), contentActions))

with open(appPath + "/" + appName, "+w") as appFile:
    appFile.write(fileContents)
