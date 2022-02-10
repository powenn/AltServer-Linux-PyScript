# AltServer-Linux-PyScript
## AltServer-Linux Script python edition

AltServer from https://github.com/NyaMisty/AltServer-Linux/releases

Special thanks to [NyaMisty](https://github.com/NyaMisty) for AltServer-Linux project 

## About the script 

It's just a simple script to make the operation of AltServer-Linux more easier with cli,now inclides features below

For ShellScript edition,you can get from [AltServer-Linux-ShellScript](https://github.com/powenn/AltServer-Linux-ShellScript)

## Features
- account saving
- enter number to select and use saved account
- enter number to select ipa
- only need one command to use the script `python3 run.py`
- Daemon mode will start automatically after device connected and press Enter
- Update option and update notification

## Announcement

AltServer for Linux is from [NyaMisty](https://github.com/NyaMisty),so you should thank to NyaMisty more ,also for any question to AltServer-Linux,you should ask or crate issue in https://github.com/NyaMisty/AltServer-Linux rather than this repository,I just providing scripts to make the operation more easier. 

## Note 

Just run `python3 run.py` and follow the instruction

***Not work on every linux distribution and architectures,report issues to [issues](https://github.com/powenn/AltServer-Linux-PyScript/issues)***

## Get start

Get the release which support your device architecture

You need idevicemobile

`apt setup dependencies`
```
sudo apt-get install usbmuxd libimobiledevice6 libimobiledevice-utils
```
```
sudo apt-get install wget curl
```
Please storage your ipa files into AltServer/ipa

run `python3 run.py` to start

