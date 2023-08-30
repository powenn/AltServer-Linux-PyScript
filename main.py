import os
import json
import shutil
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
"""
Versions will be fetch with FetchVersion()
"""
Latest_AltServer_Version = ""
Latest_AltStore_Version = ""
Latest_Netmuxd_Version = ""
Latest_Anisette_Server_Version = ""
Latest_Script_Version = ""

# PATH AND URL
"""
URL value default is "" , value will be update with FetchVersion()
"""
VERSION_JSON_PATH = os.path.join(CURRENT_DIRECTORY, "version.json")

ALTSERVER_PATH = os.path.join(RESOURCE_DIRECTORY, "AltServer")
Altserver_URL = ""

ALTSTORE_PATH = os.path.join(RESOURCE_DIRECTORY, "AltStore.ipa")
AltStore_URL = ""

NETMUXD_PATH = os.path.join(RESOURCE_DIRECTORY, "netmuxd")
Netmuxd_URL = ""

ANISETTE_SERVER_PATH = os.path.join(RESOURCE_DIRECTORY, "anisette-server")
Anisette_Server_URL = ""

SCRIPT_PATH = os.path.join(CURRENT_DIRECTORY, "main.py")
SCRIPT_URL = "https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/main.py"

# UPDATABLE BOOLS
"""
Default is false , value will be update with CheckUpdate()
"""
AltServer_Is_Updatable = False
AltStore_Is_Updatable = False
Nermuxd_Is_Updatable = False
Anisette_Server_Is_Updatable = False
Script_Is_Updatable = False


Version_Fetched = False


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


def FetchVersion() -> dict:
    print("Fetching version ...")

    global Latest_AltServer_Version, Latest_AltStore_Version, Latest_Anisette_Server_Version, Latest_Netmuxd_Version, Latest_Script_Version

    AltStore_Response = requests.get(
        "https://cdn.altstore.io/file/altstore/apps.json").json()["apps"][0]["versions"][0]
    Latest_AltStore_Version = AltStore_Response["version"]

    Latest_AltServer_Version = requests.get(
        "https://api.github.com/repos/NyaMisty/AltServer-Linux/releases/latest").json()["tag_name"]
    Latest_Netmuxd_Version = requests.get(
        "https://api.github.com/repos/jkcoxson/netmuxd/releases/latest").json()["tag_name"]
    Latest_Anisette_Server_Version = requests.get(
        "https://api.github.com/repos/Dadoum/Provision/releases/latest").json()["tag_name"]
    Latest_Script_Version = requests.get(
        "https://api.github.com/repos/powenn/AltServer-Linux-PyScript/releases/latest").json()["tag_name"]

    global Altserver_URL, AltStore_URL, Netmuxd_URL, Anisette_Server_URL, Version_Fetched

    Altserver_URL = f"https://github.com/NyaMisty/AltServer-Linux/releases/download/{Latest_AltServer_Version}/AltServer-{ARCH}"
    Netmuxd_URL = f"https://github.com/jkcoxson/netmuxd/releases/download/{Latest_Netmuxd_Version}/{ARCH}-linux-netmuxd"
    Anisette_Server_URL = f"https://github.com/Dadoum/Provision/releases/download/{Latest_Anisette_Server_Version}/anisette-server-{ARCH}"
    AltStore_URL = AltStore_Response["downloadURL"]

    Version_Fetched = True

    print("Done")
    json_data = {"AltServer": Latest_AltServer_Version, "AltStore": Latest_AltStore_Version, "Netmuxd": Latest_Netmuxd_Version,
                 "Anisette-Server": Latest_Anisette_Server_Version, "Script": Latest_Script_Version}
    DebugPrint(json_data)
    return json_data


def CheckResource():
    resource_list = os.listdir(RESOURCE_DIRECTORY) if os.path.exists(
        RESOURCE_DIRECTORY) else []
    Resource_Missed = not all(resource in resource_list for resource in [
                              'AltServer', 'anisette-server', 'AltStore.ipa', 'netmuxd'])
    latest_version_json = {}

    DebugPrint(f"RESOURCE_MISSED : {Resource_Missed}")

    if not os.path.exists(VERSION_JSON_PATH):
        print("version.json not exists")
        latest_version_json: dict = FetchVersion()
        DebugPrint(latest_version_json)
        with open(VERSION_JSON_PATH, "w") as outfile:
            json.dump(latest_version_json, outfile)
        # Remove all executable binaries to get new binaries
        if os.path.exists(RESOURCE_DIRECTORY):
            shutil.rmtree(RESOURCE_DIRECTORY)

    if Resource_Missed and not Version_Fetched:
        latest_version_json: dict = FetchVersion()

    current_version_json = json.load(open(VERSION_JSON_PATH))
    # Resource dir
    if not os.path.exists(RESOURCE_DIRECTORY):
        print("Creating 'resource' directory")
        os.mkdir(RESOURCE_DIRECTORY)
    # AltServer
    if not os.path.exists(ALTSERVER_PATH):
        print(f"Downloading Altserver {Latest_AltServer_Version}")
        DebugPrint(Altserver_URL)
        response = requests.get(Altserver_URL)
        open(ALTSERVER_PATH, "wb").write(response.content)
        current_version_json["AltServer"] = Latest_AltServer_Version
    # AltStore
    if not os.path.exists(ALTSTORE_PATH):
        print(f"Downloading AltStore ipa {Latest_AltStore_Version}")
        DebugPrint(AltStore_URL)
        response = requests.get(AltStore_URL)
        open(ALTSTORE_PATH, "wb").write(response.content)
        current_version_json["AltStore"] = Latest_AltStore_Version
    # Netmuxd
    if not os.path.exists(NETMUXD_PATH) and NETMUXD_IS_AVAILABLE:
        print(f"Downloading netmuxd {Latest_Netmuxd_Version}")
        DebugPrint(Netmuxd_URL)
        response = requests.get(Netmuxd_URL)
        open(NETMUXD_PATH, "wb").write(response.content)
        current_version_json["Netmuxd"] = Latest_Netmuxd_Version
    # Anisette-Server
    if not os.path.exists(ANISETTE_SERVER_PATH):
        print(f"Downloading anisette-server {Latest_Anisette_Server_Version}")
        DebugPrint(Anisette_Server_URL)
        response = requests.get(Anisette_Server_URL)
        open(ANISETTE_SERVER_PATH, "wb").write(response.content)
        current_version_json["Anisette-Server"] = Latest_Anisette_Server_Version

    # Write updated json data into version.json
    with open(VERSION_JSON_PATH, "w") as outfile:
        json.dump(current_version_json, outfile)

    if not os.access(ALTSERVER_PATH, os.X_OK):
        print("Setting AltServer exec permission")
        os.chmod(ALTSERVER_PATH, 0o755)
    if os.path.exists(NETMUXD_PATH) and not os.access(NETMUXD_PATH, os.X_OK):
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
    if not Version_Fetched:
        FetchVersion()
    with open(VERSION_JSON_PATH, 'r') as openfile:
        json_data = json.load(openfile)

    Current_Script_Version = json_data["Script"]
    Current_AltServer_Version = json_data["AltServer"]
    Current_AltStore_Version = json_data["AltStore"]
    Current_Netmuxd_Version = json_data["Netmuxd"]
    Current_Anisette_Server_Version = json_data["Anisette-Server"]

    global Script_Is_Updatable, AltServer_Is_Updatable, AltStore_Is_Updatable, Nermuxd_Is_Updatable, Anisette_Server_Is_Updatable
    # script
    if Latest_Script_Version != Current_Script_Version:
        Script_Is_Updatable = True
        print(
            f"Script is updatable , current ver : {Current_Script_Version} , latest ver : {Latest_Script_Version}")
    # altserver
    if Latest_AltServer_Version != Current_AltServer_Version:
        AltServer_Is_Updatable = True
        print(
            f"AltServer is updatable , current ver : {Current_AltServer_Version} , latest ver : {Latest_AltServer_Version}")
    # altstore
    if Latest_AltStore_Version != Current_AltStore_Version:
        AltStore_Is_Updatable = True
        print(
            f"AltStrore is updatable , current ver : {Current_AltStore_Version} , latest ver : {Latest_AltStore_Version}")
    # netmuxd
    if Latest_Netmuxd_Version != Current_Netmuxd_Version:
        Nermuxd_Is_Updatable = True
        print(
            f"Netmuxd is updatable , current ver : {Current_Netmuxd_Version} , latest ver : {Latest_Netmuxd_Version}")
    # anisette server
    if Latest_Anisette_Server_Version != Current_Anisette_Server_Version:
        Anisette_Server_Is_Updatable = True
        print(
            f"Anisette-Server is updatable , current ver : {Current_Anisette_Server_Version} , latest ver : {Latest_Anisette_Server_Version}")

    return AltServer_Is_Updatable or AltStore_Is_Updatable or Nermuxd_Is_Updatable or Anisette_Server_Is_Updatable or Script_Is_Updatable


def RemoveOutdatedResource():
    if AltServer_Is_Updatable:
        os.remove(ALTSERVER_PATH)
    if AltStore_Is_Updatable:
        os.remove(ALTSTORE_PATH)
    if Anisette_Server_Is_Updatable:
        os.remove(ANISETTE_SERVER_PATH)
    if Nermuxd_Is_Updatable:
        os.remove(NETMUXD_PATH)


def Update():
    if CheckUpdate():
        answer = getAnswer("Update available, Update now ? (y/n) : ").lower()
        if answer == 'y':
            print("Removing outdated resource ...")
            RemoveOutdatedResource()
            if Script_Is_Updatable:
                print("Downloading the lastest script ...")
                response = requests.get(
                    "https://raw.githubusercontent.com/powenn/AltServer-Linux-PyScript/rewrite/main.py")
                open(SCRIPT_PATH, "wb").write(response.content)
            print("\n\nUpdate done\nYou can find update log in https://github.com/powenn/AltServer-Linux-PyScript/releases\nScript requires restart to apply updates\nUse `e` option to exit the script\n\n")
    else:
        print("All resources and script are up to dated :)")


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
        try:
            index = int(
                getAnswer("Enter the index of the device for installation : "))
            self.selectedDevice = devices[index]
        except:
            print("Invalid index")
            self.selectedDevice = None

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
            filePath = getAnswer("Enter the absolute path of the file : ")
            if filePath != "":
                self.filePath = filePath
            else:
                self.filePath = None
                print("No file path entered")
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
        input("Press enter to exit : ")
        exit(-1)
    CheckResource()
    CheckUpdate()
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
            if installaion_manager.selectedDevice == None:
                continue
            installaion_manager.getAccount()
            installaion_manager.getPassword()
            installaion_manager.selectFile()
            if installaion_manager.filePath == None:
                continue
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
                print(f"{d.name} , {d.UDID}")

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
