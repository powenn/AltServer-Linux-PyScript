# AltServer-Linux-PyScript

## About the script 

It's a script to make the operation of AltServer-Linux easier so you could sideload with Linux easyily

# Features

- [x] WiFi Refreshing
- [x] WiFi Installation
- [x] Tethered Refreshing
- [x] Tethered Installation
- [x] Install your own iPA file by entering the absolute path
- [x] Script Updating
- [x] Independently Resource Updating

# Getting start

`apt setup dependencies`
```
sudo apt-get install usbmuxd libimobiledevice6 libimobiledevice-utils
```
```
sudo apt-get install wget curl libavahi-compat-libdnssd-dev
```

# Usage

`curl https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/main.py > main.py`

`python3 main.py`

**If WiFi refreshing is not working**

Check the two services, if they aren't up and running, then these commands down below will start them

`avahi-daemon.service` and `avahi-daemon.socket`

**Check the status**

`systemctl status avahi-daemon.service`

`systemctl status avahi-daemon.socket`

**Start**

`systemctl start avahi-daemon.service`

`systemctl start avahi-daemon.socket`

**To run automatically on boot use the *enable* command**

`systemctl enable avahi-daemon.service`

`systemctl enable avahi-daemon.socket`

# Want to use it as an app?

![Screenshot](https://github.com/powenn/AltServer-Linux-PyScript/blob/rewrite/Images/01.png)

`curl https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/AltServer.desktop > AltServer.desktop`

You might want to give it an app icon  
I am using `https://altstore.io/images/AltStore_AppIcon-p-500.png` as app icon  
download the image and edit the desktop file

set  
`Icon=THE_ABSOLUTE_PATH_OF_THE_IMAGE`  
set  
`Path=THE_DIR_WHICH_CONTAINS_THE_PYTHON_SCRIPT`  
then  
`sudo cp 'THE_DESKTOP_ENTRY_FILE' '/usr/share/applications/AltServer.desktop'`

[Demo video](https://github.com/powenn/AltServer-Linux-PyScript/discussions/7)

# Credits

[NyaMisty](https://github.com/NyaMisty) for [AltServer-Linux](https://github.com/NyaMisty/AltServer-Linux)

[jkcoxson](https://github.com/jkcoxson) for [netmuxd](https://github.com/jkcoxson/netmuxd)

[Dadoum](https://github.com/Dadoum) for [Provision](https://github.com/Dadoum/Provision)

[Macley](https://github.com/Macleykun) for testing and figure out avahi-daemon issue
