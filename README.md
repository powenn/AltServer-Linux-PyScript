# AltServer-Linux-PyScript

## About the script 

It's just a simple script to make the operation of AltServer-Linux more easier with cli,now inclides features below

## Features

- [x] WiFi Refreshing
- [x] WiFi Installation
- [x] Tethered Refreshing
- [x] Tethered Installation
- [x] Updating


# Usage

`curl https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/main.py > main.py`

`python3 main.py`

**If WiFi refreshing not working**

Check the two service, if not enable or running , then start

`avahi-daemon.service` and `avahi-daemon.socket`

**Check status**

`systemctl status avahi-daemon.service`

`systemctl status avahi-daemon.socket`

**Start**

`systemctl start avahi-daemon.service`

`systemctl start avahi-daemon.socket`

## Getting start

`apt setup dependencies`
```
sudo apt-get install usbmuxd libimobiledevice6 libimobiledevice-utils
```
```
sudo apt-get install wget curl libavahi-compat-libdnssd-dev
```

# Credits

[NyaMisty](https://github.com/NyaMisty) for [AltServer-Linux](https://github.com/NyaMisty/AltServer-Linux)

[jkcoxson](https://github.com/jkcoxson) for [netmuxd](https://github.com/jkcoxson/netmuxd)

[Dadoum](https://github.com/Dadoum) for [Provision](https://github.com/Dadoum/Provision)

[Macley](https://github.com/Macleykun) for testing and figure out avahi-daemon issue
