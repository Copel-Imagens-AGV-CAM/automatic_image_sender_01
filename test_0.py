#!/usr/bin/env python3
import ftplib
from posixpath import split
import subprocess
import time
import os
#from tkinter import image_names
import paramiko, sys

FTP_HOST = "172.31.0.11"
FTP_USER = "agvuser"
FTP_PASS = "lpee@2022"
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

images_directory = '/home/user/Imagens'         # diretório local de origem
sent_directory = '/home/user/Enviados'          # diretório local para realocação
remote_path = '/home/shared/pasta_teste/'       # diretório remoto de destino
os.makedirs(images_directory, exist_ok=True)
os.makedirs(sent_directory, exist_ok=True)
mission_folder = [os.path.join(images_directory, name) for name in os.listdir(images_directory)]
#print(mission_folder,len(mission_folder))
for i  in range(len(mission_folder)):
    folder_name_list = mission_folder[i].split("_")
    #print(folder_name_list)
    folder_name = folder_name_list[-3]+"_"+folder_name_list[-2]+"_"+folder_name_list[-1]
    local_directory = sent_directory + "/" + folder_name
    os.makedirs(local_directory, exist_ok=True)
    folders_in_mission_list = [ name for name in os.listdir(mission_folder[i]) if os.path.isdir(os.path.join(mission_folder[i], name)) ]
    for j in range(len(folders_in_mission_list)):
        folders_in_mission = local_directory +"/"+ folders_in_mission_list[j]
        print(folders_in_mission)
        os.makedirs(folders_in_mission, exist_ok=True)
    #print(folder_name)
    remote_folder = remote_path+folder_name
    #print(remote_folder)
    images_directory = mission_folder[i]
    caminhos = [os.path.join(images_directory, name) for name in os.listdir(images_directory)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]
    #print(jpgs)
    
    transport = paramiko.Transport((FTP_HOST, 22))
    transport.connect(username = FTP_USER, password = FTP_PASS)
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        sftp.chdir(remote_folder)  # Test if remote_path exists
    except IOError:
        sftp.mkdir(remote_folder)  # Create remote_path
        sftp.chdir(remote_folder)
    
    #print(len(jpgs))
    #print(remote_folder)
    print("try")
    for j in range(len(jpgs)):
        image_path = jpgs[j].split("/")
        image_name = image_path[-1]
        #print("top",jpgs[j], image_name)
        sftp.put(jpgs[j], os.path.join(remote_folder, image_name))
        #my_list = os.listdir(mission_folder[i])
        #sftp.put(jpgs[j], remote_folder)
        '''
        try:
            print("a")
            sftp.put(jpgs[j], remote_path)
            print("b")
        except:
            print("c")
            pass
        '''
    for j in range(len(folders_in_mission_list)):
        folders_in_mission = remote_path + folder_name +"/"+ folders_in_mission_list[j]
        #print(folders_in_mission)
        #os.makedirs(folders_in_mission_list, exist_ok=True)
        try:
            sftp.chdir(folders_in_mission)  # Test if remote_path exists
        except IOError:
            sftp.mkdir(folders_in_mission)  # Create remote_path
            sftp.chdir(folders_in_mission)
        images_directory = images_directory+"/"+ folders_in_mission_list[j]
        #print(images_directory)
        caminhos = [os.path.join(images_directory, name) for name in os.listdir(images_directory)]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]
        for k in range(len(jpgs)):
            image_path = jpgs[k].split("/")
            image_name = image_path[-1]
            remote_folder = remote_path + folder_name +"/"+ folders_in_mission_list[j]
            #print("pow",jpgs[k], image_name,remote_folder)
            
            sftp.put(jpgs[k], os.path.join(remote_folder, image_name))
            #my_list = os.listdir(mission_folder[i])
            #sftp.put(jpgs[j], remote_folder)
            '''
            try:
                print("a")
                sftp.put(jpgs[j], remote_path)
                print("b")
            except:
                print("c")
                pass
            '''
    sftp.close()
    transport.close()

#print("caminhos")
#print(len(caminhos))
#print("arquivos")
#print(len(arquivos))
#print("jpgs")
#print(len(jpgs))

'''
import paramiko, sys

ssh = paramiko.SSHClient()
ssh.connect(FTP_HOST, 22, FTP_USER, FTP_PASS)
ssh.exec_command('mkdir -p ' + remote_path)
ssh.close

transport = paramiko.Transport((myhost, 22))
transport.connect(username = myusername, password = mypassword)

sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put(local_path, remote_path)
sftp.close()

transport.close()
sftp = paramiko.SFTPClient.from_transport(transport)
try:
    sftp.chdir(remote_path)  # Test if remote_path exists
except IOError:
    sftp.mkdir(remote_path)  # Create remote_path
    sftp.chdir(remote_path)
sftp.mkdir(remote_path)
sftp.put(local_path, '.')    # At this point, you are in remote_path in either case
sftp.close()

data = time.strftime("%Y%m%d-%H%M%S")
file_name = data +'.tar.gz'
path = '/home/user/Imagens' + file_name
subprocess.call("tar -czf "+ file_name + " '/copel/imagens'",shell=True)
try:
    session = ftplib.FTP(FTP_HOST,FTP_USER,FTP_PASS)
    session.cwd("img")
    file = open(file_name,'rb')                  # file to send
    session.storbinary('STOR '+file_name, file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
except:
    pass
os.remove(path)
'''