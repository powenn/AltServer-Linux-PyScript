import os
import getpass
import datetime
import platform
import requests
import subprocess

DEBUGGING = False
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


# ANISETTE-SERVER
ANISETTE_HOST = "127.0.0.1"
ANISETTE_PORT = 6969

# ARCH
ARCH = platform.machine()
if ARCH == "armv7l":
    ARCH = "armv7"
NETMUXD_AVAILABLE_ARCHS = ("x86_64", "aarch64", "armv7")
NETMUXD_IS_AVAILABLE = ARCH in NETMUXD_AVAILABLE_ARCHS
Netmuxd_is_on = True if NETMUXD_IS_AVAILABLE else False


# DIRECTORY
CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RESOURCE_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "resource")

# VERSIONS
ALTSERVER_VERSION = "v0.0.5"
ALTSTORE_VERSION = "1_6_3"
NETMUXD_VERSION = "v0.1.4"
ANISETTE_SERVER_VERSION = "2.1.0"
SCRIPT_VERSION = "0.1"

# PATH AND URL
ALTSERVER_PATH = os.path.join(RESOURCE_DIRECTORY, "AltServer")
ALTSERVER_URL = f"https://github.com/NyaMisty/AltServer-Linux/releases/download/{ALTSERVER_VERSION}/AltServer-{ARCH}"

ALTSTORE_PATH = os.path.join(RESOURCE_DIRECTORY, "AltStore.ipa")
ALTSTORE_URL = f"https://cdn.altstore.io/file/altstore/apps/altstore/{ALTSTORE_VERSION}.ipa"

NETMUXD_PATH = os.path.join(RESOURCE_DIRECTORY, "netmuxd")
NETMUXD_URL = f"https://github.com/jkcoxson/netmuxd/releases/download/{NETMUXD_VERSION}/{ARCH}-linux-netmuxd"

ANISETTE_SERVER_PATH = os.path.join(RESOURCE_DIRECTORY, "anisette-server")
ANISETTE_SERVER_URL = f"https://github.com/Dadoum/Provision/releases/download/{ANISETTE_SERVER_VERSION}/anisette-server-{ARCH}"

SCRIPT_PATH = os.path.join(CURRENT_DIRECTORY, "main.py")
SCRIPT_URL = "https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/main.py"


def getAnswer(text):
    try:
        return input(text)
    except KeyboardInterrupt:
        print("\nCtrl+C pressed, aborting")
        exit(-2)


def DebugPrint(msg):
    now = datetime.datetime.now().strftime(TIME_FORMAT)
    if DEBUGGING:
        print(f"[DEBUG] {now}\n== {msg} ==")


def CheckResource():
    if not os.path.exists(RESOURCE_DIRECTORY):
        print("Creating 'resource' directory")
        os.mkdir(RESOURCE_DIRECTORY)
    if not os.path.exists(ALTSERVER_PATH):
        print("Downloading Altserver")
        response = requests.get(ALTSERVER_URL)
        open(ALTSERVER_PATH, "wb").write(response.content)
    if not os.path.exists(ALTSTORE_PATH):
        print("Downloading AltStore ipa")
        response = requests.get(ALTSTORE_URL)
        open(ALTSTORE_PATH, "wb").write(response.content)
    if not os.path.exists(NETMUXD_PATH) and NETMUXD_IS_AVAILABLE:
        print("Downloading netmuxd")
        response = requests.get(NETMUXD_URL)
        open(NETMUXD_PATH, "wb").write(response.content)
    if not os.path.exists(ANISETTE_SERVER_PATH):
        print("Downloading anisette-server")
        response = requests.get(ANISETTE_SERVER_URL)
        open(ANISETTE_SERVER_PATH, "wb").write(response.content)

    if not os.access(ALTSERVER_PATH, os.X_OK):
        print("Setting AltServer exec permission")
        os.chmod(ALTSERVER_PATH, 0o755)
    if not os.access(NETMUXD_PATH, os.X_OK):
        print("Setting netmuxd exec permission")
        os.chmod(NETMUXD_PATH, 0o755)
    if not os.access(ANISETTE_SERVER_PATH, os.X_OK):
        print("Setting anisette-server permission")
        os.chmod(ANISETTE_SERVER_PATH, 0o755)

    DebugPrint(subprocess.getoutput(f"ls -al {RESOURCE_DIRECTORY}"))


def CheckNetworkConnection() -> bool:
    try:
        requests.get('http://google.com')
        return True
    except:
        return False


def CheckUpdate() -> bool:
    latest_version = requests.get(
        "https://github.com/powenn/AltServer-Linux-PyScript/raw/rewrite/version.txt").content.decode().replace('\n', '')
    if latest_version != SCRIPT_VERSION:
        print(f"latest version : {latest_version}")
        print(f"current version : {SCRIPT_VERSION}")
        msg = """
++++++++++++++++++++++++
+                      +
+   Update available   +
+                      +
++++++++++++++++++++++++
        """
        print(msg)
        return True
    return False


def Update():
    if CheckUpdate():
        answer = getAnswer("Update available, Update now ? (y/n) : ").lower()
        if answer == 'y':
            print("Downloading the lastest script")
            response = requests.get(
                "https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/main.py")
            open(SCRIPT_PATH, "wb").write(response.content)
            print("Update done")
            print("If resouce files need to update, remove them and you will get new one")
            print(
                "You can find update log in https://github.com/powenn/AltServer-Linux-PyScript/releases")
            print("Please exit and restart the script using -e option")
    else:
        print("You are using the latest version")


class AnisetteServer:
    def __init__(self, host=ANISETTE_HOST, port=ANISETTE_PORT):
        self.host = host
        self.port = port
        os.environ["ALTSERVER_ANISETTE_SERVER"] = f"http://{host}:{port}"
        DebugPrint(os.environ["ALTSERVER_ANISETTE_SERVER"])
        DebugPrint(f"{ANISETTE_SERVER_PATH} -n {host} -p {port}")
        self.server = subprocess.Popen(
            f"{ANISETTE_SERVER_PATH} -n {host} -p {port}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def kill(self):
        print(subprocess.getoutput("killall anisette-server"))


class AltServerDaemon:
    def __init__(self):
        self.start()

    def start(self):
        self.altserver = subprocess.Popen(
            ALTSERVER_PATH, shell=True)  # ,env=os.environ)

    def kill(self):
        print(subprocess.getoutput("killall AltServer"))

    def restart(self):
        self.kill()
        self.start()


class Netmuxd:
    def __init__(self):
        if Netmuxd_is_on:
            if subprocess.getoutput("echo $(pidof usbmuxd)") != "":
                print(subprocess.getoutput("sudo kill -9 $(pidof usbmuxd)"))
            self.start()

    def start(self):
        self.netmuxd = subprocess.Popen(f"sudo -b {NETMUXD_PATH}", shell=True)

    def kill(self):
        print(subprocess.getoutput("sudo killall netmuxd"))

    def switchWiFi(self):
        global Netmuxd_is_on
        Netmuxd_is_on = True
        DebugPrint(f"NETMUXD : {Netmuxd_is_on}")
        print(subprocess.getoutput("sudo kill -9 $(pidof usbmuxd)"))
        self.kill()
        self.start()

    def switchTether(self):
        global Netmuxd_is_on
        Netmuxd_is_on = False
        DebugPrint(f"NETMUXD : {Netmuxd_is_on}")
        print(subprocess.getoutput("sudo usbmuxd"))
        self.kill()


def getSUDO():
    output = ""
    password = ""
    while output[:-1] != "0000":
        password = getpass.getpass("Enter sudo password : ")
        p = subprocess.Popen("sudo -S echo '0000'", stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, shell=True)
        prompt = p.communicate(password + '\n')
        output = prompt[0]
    DebugPrint(output[:-1])


class iDevice:
    def __init__(self, name, UDID):
        self.name = name
        self.UDID = UDID


class DeviceManager:
    def __init__(self, devices=[]):
        self.devices = devices

    def getDevices(self) -> list[iDevice]:
        DebugPrint(f"NETMUXD : {Netmuxd_is_on}")
        self.devices = []
        udids = subprocess.getoutput("idevice_id -n").split(
            '\n') if Netmuxd_is_on else subprocess.getoutput("idevice_id -l").split('\n')
        DebugPrint(udids)
        if udids == ['']:
            print("No devices found")
        else:
            for udid in udids:
                name = subprocess.getoutput(
                    f"ideviceinfo -n -u {udid} -k DeviceName") if Netmuxd_is_on else subprocess.getoutput(f"ideviceinfo -u {udid} -k DeviceName")
                d = iDevice(name=name, UDID=udid)
                self.devices.append(d)
        return self.devices


class InstallationManager:
    def __init__(self):
        pass

    def selectDevice(self, devices: list[iDevice]):
        for i in range(len(devices)):
            print(f"[{i}] : {devices[i].name} , {devices[i].UDID}")
        index = int(
            getAnswer("Enter the index of the device for installation : "))
        self.selectedDevice = devices[index]

    def getAccount(self):
        ac = getAnswer("Enter your Apple ID : ")
        self.account = ac

    def getPassword(self):
        pd = getpass.getpass("Enter password of the Apple ID : ")
        self.password = pd

    def selectFile(self):
        answer = getAnswer(
            "Do you want to install AltStore ? (y/n) [n for select your own iPA] : ").lower()
        if answer == 'n':
            self.filePath = getAnswer("Enter the absolute path of the file : ")
        else:
            self.filePath = ALTSTORE_PATH

    def run(self):
        subprocess.run(
            f"{ALTSERVER_PATH} -u {self.selectedDevice.UDID} -a {self.account} -p {self.password} {self.filePath}", shell=True)

    def getInfo(self) -> str:
        return [self.selectedDevice.name, self.account, self.password, self.filePath]


def main():
    if CheckNetworkConnection() == False:
        print("Please connect to network and re-run the script")
        exit(-1)
    CheckUpdate()
    CheckResource()
    if NETMUXD_IS_AVAILABLE:
        getSUDO()
    anisetteserver = AnisetteServer()
    netmuxd = Netmuxd()
    altserverdaemon = AltServerDaemon()
    device_manager = DeviceManager()
    installaion_manager = InstallationManager()
    print(HELP_MSG)
    while True:
        option = getAnswer("Enter OPTION to continue : ").lower()

        if option == 'i':
            devices = device_manager.getDevices()
            if len(devices) == 0:
                continue
            installaion_manager.selectDevice(devices=devices)
            installaion_manager.getAccount()
            installaion_manager.getPassword()
            installaion_manager.selectFile()
            DebugPrint(installaion_manager.getInfo())
            installaion_manager.run()

        elif option == 'w':
            if NETMUXD_IS_AVAILABLE:
                if not Netmuxd_is_on:
                    netmuxd.switchWiFi()
                    altserverdaemon.restart()
            else:
                print(f"Netmuxd is not support arch : {ARCH}")

        elif option == 't':
            if Netmuxd_is_on:
                netmuxd.switchTether()
                altserverdaemon.restart()

        elif option == 'e':
            altserverdaemon.kill()
            anisetteserver.kill()
            if Netmuxd_is_on:
                netmuxd.kill()
            break

        elif option == 'h':
            print(HELP_MSG)

        elif option == 'p':
            devices = device_manager.getDevices()
            for d in devices:
                print(f"{d.name}:{d.UDID}")

        elif option == 'u':
            Update()

        else:
            print("Invalid option")


HELP_MSG = """
#####################################
#  Welcome to the AltServer script  #
#####################################

ScriptUsage: [OPTION]

OPTIONS
    i, --Install AltStore or ipa files
        Install AltStore or ipa files to your device
    w, --Switch to wifi Daemode mode (Default using it after launch)
        Switch and restart to wifi Daemode mode to refresh apps or AltStore
    t, --Switch to usb tethered Daemode mode
        Switch and restart to usb tethered Daemode mode to refresh apps or AltStore
    e, --Exit
        Exit script
    h, --Help
        Show this message
    p, --Pair
        Show paired devices
    u, --Update
        Update this script
        
For more information: 
https://github.com/powenn/AltServer-Linux-PyScript

"""

if __name__ == '__main__':
    DebugPrint("Script Start")
    DebugPrint(
        f"RUNNING AT {CURRENT_DIRECTORY} , RESOURCE_DIR : {RESOURCE_DIRECTORY}")
    DebugPrint(f"ARCH : {ARCH} , NETMUXD_AVAILABLE : {NETMUXD_IS_AVAILABLE}")
    main()
