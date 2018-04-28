#!/bin/bash
#
#restart docker container
docker restart bsc_web_1
#
# L Nix <lornix@lornix.com>
# reload browser window
#
# whether to use SHIFT+CTRL+R to force reload without cache
RELOAD_KEYS="F5"
#RELOAD_KEYS="SHIFT+CTRL+R"
#
# set to whatever's given as argument
BROWSER=$1
#
# if was empty, default set to name of browser, firefox/chrome/opera/etc..
if [ -z "${BROWSER}" ]; then
    BROWSER=Firefox
fi

PKG="xdotool"
if dpkg -s ${PKG}
then
    echo "True"
else
    sudo apt-get install xdotool
fi

sleep 2s
xdotool search --sync --onlyvisible --class ${BROWSER} key --clearmodifiers ${RELOAD_KEYS}
xdotool search --sync --onlyvisible --class ${BROWSER} windowactivate