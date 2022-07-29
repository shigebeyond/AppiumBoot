#!/bin/sh
cd `dirname $0`

# 启动appium
pids=`ps -ef |grep Appium-linux-1.21.0.AppImage |grep -v grep | awk '{print $2}'`
if [ "$pids" == "" ]; then
    /home/shi/setup/appium/Appium-linux-1.21.0.AppImage &
fi

# 测试
AppiumBoot example/step-material.yml
AppiumBoot example/step-zhs.yml
AppiumBoot example/step-sk.yml
AppiumBoot example/step-weibo.yml