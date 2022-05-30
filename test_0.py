#!/usr/bin/env python3
import ftplib
import subprocess
import time
import os

FTP_HOST = "200.134.25.161"
FTP_USER = "imagens"
FTP_PASS = "Lp3e2o2!"
"""
ftp = FTP(FTP_HOST)
ftp.login(FTP_USER,FTP_PASS)
ftp.cwd('/www/copel/')
#
#session = ftplib.FTP(FTP_HOST,FTP_USER,FTP_PASS)
file_name = 'test_pic.jpg'
ftp.storbinary('STOR ' + file_name, open(file_name, "rb"))
ftp.quit() # Terminate the FTP connection
my_file.close() # Close the local file you had opened for downloading/storing its content
ftp.dir()
"""


data = time.strftime("%Y%m%d-%H%M%S")
file_name = data +'.tar.gz'
path = '/copel/test_4g_sub_copel/' + file_name
subprocess.call("tar -czf "+ file_name + " '/copel/imagens'",shell=True)
try:
    session = ftplib.FTP(FTP_HOST,FTP_USER,FTP_PASS)
    session.cwd("img-upload-test")
    file = open(file_name,'rb')                  # file to send
    session.storbinary('STOR '+file_name, file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
except:
    pass
os.remove(path)