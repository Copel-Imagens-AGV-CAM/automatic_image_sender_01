#!/usr/bin/env python3

from ast import If
from multiprocessing import connection
import os
from re import T
import paramiko
import shutil
from datetime import datetime

FTP_HOST = "172.31.0.11"                        # credenciais de acesso
FTP_USER = "agvuser"
FTP_PASS = "lpee@2022"
images_to_server_flag = False                   # flag para indicar se há imagnes a serem enviadas para o servidor ou não
folder_exists = False                           # flag para indicar se exite as pastas necessárias no seridor ou se elas precisam ser cridas
connection_flag = False                         # flag para indicar se há conecxão
sent_images = 0
images_directory = '/home/user/continuous_capture'         # diretório local de origem
sent_directory = '/home/user/Enviados/continuous_capture'  # diretório local para realocação
sent_directory_rgb = '/home/user/Enviados/rgb_data'        # diretório local para realocação rg
remote_path = '/home/shared/A700_fixa/'                    # diretório remoto de destino
remote_path_rgb='/home/shared/inspecoes/rgb_data/'         # diretório remoto de destino rgb
os.makedirs(images_directory, exist_ok=True)    # cria diretório de origem caso não exista
os.makedirs(sent_directory, exist_ok=True)      # cria diretório de realocação caso não exista
mission_folder = [os.path.join(images_directory, name) for name in os.listdir(images_directory)] # lista todas as pastas do diretório de origem
for i  in range(len(mission_folder)):               # para cada pasta do diretório de origem
    folder_name_list = mission_folder[i].split("/")[-1].split("_") # separa o nome das pastas do caminho do diretório de origem em relação ao caractere A
    if(len(folder_name_list)<=3):
        folder_name = 'fixa_'+folder_name_list[0] #folder_name_list[-3]+"_"+folder_name_list[-2]+"_"+folder_name_list[-1]    # cria o nome correto da pasta
        local_directory = sent_directory + "/" + folder_name
        remote_folder = remote_path + folder_name
    else:
        folder_name = 'fixa_'+folder_name_list[0]+'_RGB'
        local_directory = sent_directory_rgb + "/" + folder_name
        remote_folder = remote_path_rgb + folder_name                                    # cria o caminho para diretório local de realcação
    dia_atual=datetime.now().day
    dia_pasta = folder_name.split('_')[1].split('-')[2]
    if(int(dia_pasta)!=int(dia_atual)):
        os.makedirs(local_directory, exist_ok=True)                                             # cria o diretório local de realocação se ele não existir
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
        if(int(dia_pasta)!=int(dia_atual)):
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
        if(int(dia_pasta)!=int(dia_atual)):
            for j in range(len(jpgs)):
                image_path = jpgs[j].split("/") # Divide o a string do caminhos dos aquivos a partir do /.
                image_name = 'fixa_'+image_path[-1]     # Seleciona aparte fianl do string dividido como o nome do arquivo.
                try:
                    sftp.put(jpgs[j], os.path.join(remote_folder, image_name))  # Faz upload do arquivo para os ervidor FTP
                    os.replace(jpgs[j],local_directory +"/"+ image_name)        # Move o arquivo da pasta iamgens para a pasta enviados.
                    sent_images+=1
                except:
                    pass
    else:
        shutil.rmtree(mission_folder[i])

if(images_to_server_flag==True):
    if(connection_flag==True):
        sftp.close()
        transport.close()
# else:
#     # delatar todas as pastas e subpastas contidas na pasta Imagens
#     for i in range(len(mission_folder)):
#         shutil.rmtree(mission_folder[i])