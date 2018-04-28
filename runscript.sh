#!/bin/bash

#restart docker container
CONTAINER_NAME=bsc_web_1

if docker ps | grep ${CONTAINER_NAME}
then
    echo "Restarting ${CONTAINER_NAME}"
    docker restart ${CONTAINER_NAME}
elif docker ps -a | grep ${CONTAINER_NAME}
then
    echo "Starting ${CONTAINER_NAME}"
    docker start bsc_web_1
else
    docker-compose up -d
fi


# whether to use SHIFT+CTRL+R to force reload without cache
RELOAD_KEYS="F5"
#RELOAD_KEYS="SHIFT+CTRL+R"

# set to whatever's given as argument
BROWSER=$1
#
# if was empty, default set to name of browser, firefox/chrome/opera/etc..
if [ -z "${BROWSER}" ]; then
    BROWSER=firefox
fi

#check and install xdotool if not 
PKG="xdotool"
if ! dpkg -s ${PKG}
then
    sudo apt-get install xdotool
fi

# sleep for container to reload
sleep 2s

#check and open browser if not
URL=localhost:8069/web
if ps -e | grep ${BROWSER}
then
    echo "Reloading your active window"
    # reload active tab of browser
    xdotool search --sync --onlyvisible --class ${BROWSER} key --clearmodifiers ${RELOAD_KEYS}
    # take you to active window
    xdotool search --sync --onlyvisible --class ${BROWSER} windowactivate
else
    echo "Opening URL ${URL} in ${BROWSER}"
    firefox ${URL}
fi