# AltServer-Linux Script python edition
# Author of the script : powen

# import 
import os
import subprocess

DIRPATH=os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRPATH)

HasExistAccount=subprocess.check_output("cat saved.txt",shell=True).decode('utf-8')
HasExistipa=subprocess.check_output("ls ipa",shell=True).decode('utf-8')
UDID=subprocess.check_output("lsusb -v 2> /dev/null | grep -e 'Apple Inc' -A 2 | grep iSerial | awk '{print $3}'",shell=True).decode('utf-8').replace("\n", "")
global PATH
# Default var
mainScript=0
NoIpaFile=0
AccountSaving=0
# Def
def getAnswer(text):
     return input(text)

# Check if there exists saved account
# Ask if want to use saved account
def AskAccount() :
    global AppleID
    global password
    if HasExistAccount != "" :
        reply=getAnswer("Do you want to use saved Account ? [y/n] :")
        if reply.lower() == "n" or reply.lower() == "no":
            UseExistAccount=0
        if reply.lower() == "y" or reply.lower() == "yes":
            UseExistAccount=1
            print("Which account you want to use ? ")
            subprocess.run("nl saved.txt",shell=True)
            number=getAnswer("please enter the number :")
            AppleIDCMD='sed -n %sp saved.txt | cut -d , -f 1' %number
            passwordCMD='sed -n %sp saved.txt | cut -d , -f 2' %number
            AppleID=subprocess.check_output(AppleIDCMD,shell=True).decode('utf-8').replace("\n", "")
            password=subprocess.check_output(passwordCMD,shell=True).decode('utf-8').replace("\n", "")
    if HasExistAccount == "" :
        UseExistAccount=0
    if UseExistAccount == 0 :
        AppleID=getAnswer("Please provide your AppleID :")
        password=getAnswer("Please provide the password of AppleID :")

# Execute AltServer
# Check if this account existed before
def AltServer() :
    global AccountSaving
    AltServerCMD='./AltServer -u %s -a %s -p %s %s' % (UDID,AppleID,password,PATH)
    subprocess.run(AltServerCMD,shell=True)
    subprocess.run('read key',shell=True)
    if CheckAccount.returncode == 1 :
        AccountSaving=1
    if CheckAccount.returncode == 0 :
        AccountSaving=0

# Check if there exists ipa files in ipa folder
# Ask which ipa want to install
def ipaCheck() :
    global NoIpaFile
    global Existipa
    if HasExistipa != "" :
        ipaListCMD='echo "%s" > ipaList.txt' %HasExistipa
        subprocess.run(ipaListCMD,shell=True)
        subprocess.run("nl ipaList.txt",shell=True)
        ipanumber=getAnswer("Please provide the number of ipa :")
        ExistipaCMD='sed -n %sp ipaList.txt' %ipanumber
        Existipa=subprocess.check_output(ExistipaCMD,shell=True).decode('utf-8').replace("\n", "")
    if HasExistipa == "" :
        print("There is no ipa filess in ipa folder ")
        NoIpaFile=1

# Ask to save the new account
def SaveAcccount() :
    ans=getAnswer("Do you want to save this Account ? [y/n] :")
    if ans.lower() == "n" or ans.lower() == "no":
        pass
    if ans.lower() == "y" or ans.lower() == "yes":
        SaveAcccountCMD='echo "%s" >> saved.txt' %Account
        subprocess.run(SaveAcccountCMD,shell=True)
        print("saved")

# Help2 message
HELP2="""

----------------------
InstallUsage: [OPTION]

OPTIONS

  1, --Install AltStore
    Install AltStore to your device
  2, --Install ipa files
    Install ipa files to your device
  b, --Back
    Back to previous script
"""

# Start Script Main
subprocess.run('idevicepair pair > /dev/null',shell=True)
RunScriptMain=0
while RunScriptMain==0 :
    print(HELP2)
    option=getAnswer("Enter OPTION to continue :")
    if option == '1' : # Install-AltStore
        mainScript=1
        RunScriptMain=1
    if option == '2' : # Install-ipa-files
        mainScript=2
        RunScriptMain=1
    if option == 'b' : # Back
        RunScriptMain=1

if mainScript == 1 :
    AskAccount()
    Account=AppleID+','+password
    CheckAccountCMD='grep %s saved.txt' %Account
    CheckAccount=subprocess.run(CheckAccountCMD,shell=True)
    PATH='./AltStore.ipa'
    AltServer()
if mainScript == 2 :
    ipaCheck()
    if NoIpaFile != 1 :
        AskAccount()
        Account=AppleID+','+password
        CheckAccountCMD='grep %s saved.txt' %Account
        CheckAccount=subprocess.run(CheckAccountCMD,shell=True)
        PATH='./%s' %Existipa
        AltServer()
if AccountSaving == 1 :
    SaveAcccount()
if AccountSaving ==0 :
    pass

print("<<  Back to AltServer script  >>")