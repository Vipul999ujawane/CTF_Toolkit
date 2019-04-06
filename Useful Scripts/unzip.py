import os
import subprocess
import shutil
import time
for iter in range(1000):
    path = "/home/vipul/Desktop/EncryptCTF/ziptunnel/files/"
    file = os.listdir()
    extract=""
    for i in file:
        if("flag" in str(i)):
            extract = str(i)
            break
    print("EXTRACT =>",extract)
    cmd = "7z x {}".format(extract)
    print(cmd)
    subprocess.Popen(cmd,shell=True)
    time.sleep(1)
    subprocess.Popen("mv {} {}".format(extract,iter),shell=True)
    time.sleep(1)
    print(os.listdir())