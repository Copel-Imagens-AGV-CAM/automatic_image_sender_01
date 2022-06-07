#!/usr/bin/env python3

from ast import If
from multiprocessing import connection
import os
from re import T
import paramiko
import shutil

FTP_HOST = "172.31.0.11"                        # credenciais de acesso
FTP_USER = "agvuser"
FTP_PASS = "lpee@2022"
images_to_server_flag = False                   # flag para indicar se há imagnes a serem enviadas para o servidor ou não
folder_exists = False                           # flag para indicar se exite as pastas necessárias no seridor ou se elas precisam ser cridas
connection_flag = False                         # flag para indicar se há conecxão
sent_images = 0
images_directory = '/home/user/Imagens'         # diretório local de origem
sent_directory = '/home/user/Enviados'          # diretório local para realocação
remote_path = '/home/shared/pasta_teste/'       # diretório remoto de destino
os.makedirs(images_directory, exist_ok=True)    # cria diretório de origem caso não exista
os.makedirs(sent_directory, exist_ok=True)      # cria diretório de realocação caso não exista
mission_folder = [os.path.join(images_directory, name) for name in os.listdir(images_directory)] # lista todas as pastas do diretório de origem
for i  in range(len(mission_folder)):               # para cada pasta do diretório de origem
    folder_name_list = mission_folder[i].split("_") # separa o nome das pastas do caminho do diretório de horigem em relação ao caractere A
    folder_name = folder_name_list[-3]+"_"+folder_name_list[-2]+"_"+folder_name_list[-1]    # cria o nome correto da pasta
    local_directory = sent_directory + "/" + folder_name                                    # cria o caminho para diretório local de realcação
    os.makedirs(local_directory, exist_ok=True)                                             # cria o diretório local de realocação se ele não existir
    folders_in_mission_list = [ name for name in os.listdir(mission_folder[i]) if os.path.isdir(os.path.join(mission_folder[i], name)) ] # lista todas as pastas no diretório de missão
    for j in range(len(folders_in_mission_list)):                                           # para cada pasta dentro de uma pasta de missão
        folders_in_mission = local_directory +"/"+ folders_in_mission_list[j]               # cria o caminho para diretório local de realcação (rgb_data)
        os.makedirs(folders_in_mission, exist_ok=True)                                      # cria o diretório local de realcação (rgb_data)
    remote_folder = remote_path + folder_name                                               # cria caminho para o diretório remoto
    images_directory = mission_folder[i]                                                    # salva listagem de conteúdo do diretório local
    caminhos = [os.path.join(images_directory, name) for name in os.listdir(images_directory)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]
    if(len(jpgs)>0):
        if(images_to_server_flag==False):
            images_to_server_flag = True
            try:
                transport = paramiko.Transport((FTP_HOST, 22))                      # conectar com servidor sftp
                transport.connect(username = FTP_USER, password = FTP_PASS)         # autenticação
                sftp = paramiko.SFTPClient.from_transport(transport)
                connection_flag = True
            except:
                connection_flag = False
        if(connection_flag==True):
            try:
                sftp.chdir(remote_folder)  # Test if remote_path exists. Cria pastas.
                folder_exists = True
            except IOError:
                folder_exists = False
            if(folder_exists==False):
                try:
                    sftp.mkdir(remote_folder)  # Create remote_path
                    sftp.chdir(remote_folder)
                except:
                    pass
        for j in range(len(jpgs)):
            image_path = jpgs[j].split("/") # Divide o a string do caminhos dos aquivos a partir do /.
            image_name = image_path[-1]     # Seleciona aparte fianl do string dividido como o nome do arquivo.
            try:
                sftp.put(jpgs[j], os.path.join(remote_folder, image_name))  # Faz upload do arquivo para os ervidor FTP
                os.replace(jpgs[j],local_directory +"/"+ image_name)        # Move o arquivo da pasta iamgens para a pasta enviados.
                sent_images+=1
            except:
                pass    
    for j in range(len(folders_in_mission_list)):   # para as imagens dentro de pastas rgb-data
        images_directory = images_directory+"/"+ folders_in_mission_list[j]     # Gera ceminho para as imagens das subpastas
        caminhos = [os.path.join(images_directory, name) for name in os.listdir(images_directory)]
        arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
        jpgs = [arq for arq in arquivos if arq.lower().endswith(".jpg")]    # lista imagens.
        if(len(jpgs)>0):
            if(images_to_server_flag==False):
                images_to_server_flag = True
                try:
                    transport = paramiko.Transport((FTP_HOST, 22))                      # conectar com servidor sftp
                    transport.connect(username = FTP_USER, password = FTP_PASS)         # autenticação
                    sftp = paramiko.SFTPClient.from_transport(transport)
                    connection_flag = True
                except:
                    connection_flag = False
            folders_in_mission = remote_path + folder_name +"/"+ folders_in_mission_list[j] #gera caminhos para as subpasta da pasta imagens
            if(connection_flag==True):
                try:
                    sftp.chdir(folders_in_mission)  # Test if remote_path. Cria subpastas na pasta enviados.
                    folder_exists = True
                except IOError:
                    folder_exists = False
                if(folder_exists==False):
                    try:
                        sftp.mkdir(folders_in_mission)  # Create remote_path.
                        sftp.chdir(folders_in_mission)
                    except:
                        pass
            for k in range(len(jpgs)):          # para cada imagem em dada subpasta.
                image_path = jpgs[k].split("/")
                image_name = image_path[-1]     # gera nome da imagem a partir da string do caminho
                remote_folder = remote_path + folder_name +"/"+ folders_in_mission_list[j]  # Gera caminho remoto no servidor.
                try:            
                    sftp.put(jpgs[k], os.path.join(remote_folder, image_name)) # transfere imagens das subpastas para o servidor sftp
                    os.replace(jpgs[k],local_directory +"/"+ folders_in_mission_list[j] +"/"+ image_name) # move imagens das subapstas da pasta imagens para a pasta enviados.
                    sent_images+=1
                except:
                    pass
if(images_to_server_flag==True):
    if(connection_flag==True):
        sftp.close()
        transport.close()
else:
    # delatar todas as pastas e subpastas contidas na pasta Imagens
    for i in range(len(mission_folder)):
        shutil.rmtree(mission_folder[i])