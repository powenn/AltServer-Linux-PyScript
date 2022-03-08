# AltServer-Linux Script python edition
# Author of the script : powen

# import 
import subprocess
import os
import zipfile
import shutil
# Version 
LocalVersion=subprocess.check_output("sed -n 1p version",shell=True).decode('utf-8').replace("\n", "")
LatestVersion=subprocess.check_output("curl -Lsk https://github.com/powenn/AltServer-Linux-PyScript/raw/main/version",shell=True).decode('utf-8')
Arch=subprocess.check_output("sed -n 2p version",shell=True).decode('utf-8').replace("\n", "")
DIRPATH=os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRPATH)

UpdateLog="""

What updated in version %s ?
  Script:
    - None
  AltStore:
    - Updated to 1.4.9
    
For more information: https://github.com/powenn/AltServer-Linux-PyScript
<< PLease rerun the script to apply the new version >>
""" %LatestVersion

if LatestVersion != LocalVersion :
    GetReleaseCMD='wget https://github.com/powenn/AltServer-Linux-PyScript/releases/download/%s/AltServer-%s.zip' %(LatestVersion,Arch)
    ReleaseFileName='AltServer-%s.zip' %Arch
    subprocess.run("rm -rf AltStore.ipa main.py",shell=True)
    subprocess.run(GetReleaseCMD,shell=True)
    zipfile.ZipFile((ReleaseFileName),'r').extractall(DIRPATH)
    ExtractedFolderName='AltServer-%s' %Arch
    MoveFilesCMD="mv ./%s/* %s" % (ExtractedFolderName,DIRPATH)
    subprocess.run(MoveFilesCMD,shell=True)
    os.remove(ReleaseFileName)
    shutil.rmtree(ExtractedFolderName)
    print("Done")
    print(UpdateLog)
if LatestVersion == LocalVersion :
    print("you are using the latest release")
