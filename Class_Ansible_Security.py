##########################################################################
# * Importation des bibliotheques
##########################################################################

import sys
import paramiko
import bcrypt
from cryptography.fernet import Fernet
from Class_Security import Class_Security
from Class_WinRM import Class_WinRM
from Class_OS import Class_OS
from random import choice, randint
import base64
import time

##########################################################################
# * Début du script
##########################################################################

class Class_Ansible_Security(Exception):

    """This class will do ....
    
    """
    def __init__(self, ObjLog, MonWinRM, MaBDD):
        self._MyObjLog = ObjLog
        self._MonWinRM = MonWinRM
        self._MaBDD = MaBDD
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        self._useransible = Class_Security().UserAnsible
        self._passansible = Class_Security().PassAnsible

    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonWinRM(self):
        return self._MonWinRM
    def get_useransible(self):
        return self._useransible
    def get_passansible(self):
        return self._passansible

    # ? setter method
    def set_MyObjLog(self, value):
        if (type(value) == type(self._MyObjLog)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MyObjLog = value
        else :
            raise "Property Error"
    def set_MonWinRM(self, value):
        if (type(value) == type(self._MonWinRM)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MonWinRM = value
        else :
            raise "Property Error"
    def set_useransible(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._useransible = value
        else :
            raise "Property Error"
    def set_passansible(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._passansible = value
        else :
            raise "Property Error"

    def CreateUserAnsible(self) : 

        """Cette fonction va créer l'utilisateur ansible.

        Raises:
            Exception: error on user ansible creation
        """
        
        try:
            # Créer le nouveau nom d'utilisateur Ansible
            UserAnsible = f"Service_Local_{randint(1000, 9999)}"
            self._MyObjLog.AjouteLog(f"OK - Création du User : {UserAnsible}", self.TopExit, True)
            return UserAnsible
        except Exception as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def CreatePassword(self, longueur , min = True, maj = True, chif = True, cs = True):
        
        """Cette fonction va créer un mot de passe.
        
        Args:
            longueur (Int): longueur du mot de passe souhaité

        Raises:
            Exception: error on password creation
        """
        
        try:
            # Liste qui contient tout l'alphabet en minuscule
            alphabet_min = [ chr(i) for i in range(97,123) ]
            # Liste qui contient tout l'alphabet en majuscule
            alphabet_maj = [ chr(i) for i in range(65,91) ]
            # Liste qui contient tout les chiffres
            chiffres = [ chr(i) for i in range(48,58) ]
            #Liste des caractères spéciaux
            caracteres_speciaux = ['_', '!', '#']
            alphabets = dict()
            key = 0
            if min:
                alphabets[key] = alphabet_min
                key += 1
            if maj:
                alphabets[key] = alphabet_maj
                key += 1
            if chif:
                alphabets[key] = chiffres
                key += 1
            if cs:
                alphabets[key] = caracteres_speciaux
                key += 1
            
            mdp = ''
            for i in range(longueur):
                    s = randint(0,key-1)
                    mdp += choice( alphabets[s] )
            self._MyObjLog.AjouteLog(f"OK - Création du mot de passe : {mdp}", self.TopExit, True)
            return mdp

        except Exception as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def ChangePasswordLinux(self, IPServer, UserAnsible, PassAnsible, NewPassAnsible):
        
        """Cette fonction va changer le mot de passe ansible pour Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewPassAnsible (Str): New Password Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant de changer de mot de passe Linux
            stdin, stdout, stderr = ssh.exec_command(f"echo -e '{PassAnsible}\n{NewPassAnsible}\n{NewPassAnsible}' | passwd")
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors du changement de mot de passe {NewPassAnsible} sur Linux", self.TopExit, True)
                raise
            else :
                self._MyObjLog.AjouteLog(f"OK - Le mot de passe a bien été changé {NewPassAnsible} sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def ChangePasswordWindows(self, IPServer, UserAnsible, NewPassAnsible):
        
        """Cette fonction va changer le mot de passe ansible pour Windows.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewPassAnsible (Str): New Password Ansible

        Raises:
            Exception: Connection error or change username error
        """

        try :
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de changer de mot de passe Windows
            self._MonWinRM.Run_WinRM_PS_Session(f'Set-LocalUser -Name {UserAnsible} -Password (ConvertTo-SecureString "{NewPassAnsible}" -AsPlainText -Force)')
            # Vérification que la commande c'est bien passé 
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - Le mot de passe a bien été changé {NewPassAnsible} sur Windows", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors du changement de mot de passe {NewPassAnsible} sur Windows", self.TopExit, True)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def ChangeUserLinux(self, IPServer, UserAnsible, PassAnsible, NewUserAnsible):
        
        """Cette fonction va changer l'utilisateur ansible for Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant de changer le nom d'utilisateur Linux
            # En mettant le mot de passe automatiquement root (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' usermod -l {NewUserAnsible} {UserAnsible}")
            stdin.write(PassAnsible + "\n")
            stdin.flush()
            # Vérification que la commande c'est bien passé 
            if stdout.channel.recv_exit_status() != 1:
                self._MyObjLog.AjouteLog(f"Erreur lors du changement du nom d'utilisteur {NewUserAnsible} sur Linux", self.TopExit, True)
                raise Exception(f"Erreur lors du changement du nom d'utilisteur {NewUserAnsible} sur Linux")
            else :
                self._MyObjLog.AjouteLog(f"OK - L'utilisateur a bien été changé {NewUserAnsible} sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def ChangeUserWindows(self, IPServer, UserAnsible, NewUserAnsible):
        
        """Cette fonction va changer l'utilisateur ansible for Windows.
        
        Args:
            IPServer (Str): Ip of the Server
            NewUserAnsible (Str): New user Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de changer le nom d'utilisateur Windows
            self._MonWinRM.Run_WinRM_PS_Session(f"Rename-LocalUser -Name '{UserAnsible}' -NewName '{NewUserAnsible}'")
            # Vérification que la commande c'est bien passé 
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - Le nom d'utilisateur a bien été changé {NewUserAnsible} sur Windows", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors du changement du nom d'utilisateur {NewUserAnsible} sur Windows", self.TopExit, True)
                raise Exception(f"Erreur lors du changement du nom d'utilisateur {NewUserAnsible} sur Windows")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def CreateTempUserAnsibleForWindows(self, IPServer, TempPasswdAnsible, TempUserAnsible = "Ansible2"):

        """Cette fonction va créer un utilisateur Ansible2 sur windows.
        
        Args:
            IPServer (Str): Ip of the Server
            PassAnsible (Str): Password Ansible

        Raises:
            Exception: Connection error or change username error
        """
        try:
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de créer un utilisateur temporaire avec un mot de passe
            self._MonWinRM.Run_WinRM_PS_Session(f'New-LocalUser "{TempUserAnsible}" -Password (ConvertTo-SecureString "{TempPasswdAnsible}" -AsPlainText -Force)')
            # Vérification que la commande c'est bien passé 
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - L'utilisateur {TempUserAnsible} a bien été créé windows", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la création de {TempUserAnsible} windows", self.TopExit, True)
                raise Exception(f"Erreur lors de la création de {TempUserAnsible} windows")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def AddAnsible2InAdminGroupForWindows(self, IPServer, TempUserAnsible = "Ansible2") :

        """Cette fonction va ajouter l'utilisateur Ansible2 en Admin sur Windows.
        
        Args:
            IPServer (Str): Ip of the Server

        Raises:
            Exception: Connection error or change username error
        """
        try:
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de mettre l'utilisateur dans le group d'administrateur sur Windows
            self._MonWinRM.Run_WinRM_PS_Session(f'net localgroup administrateurs {TempUserAnsible} /add')
            # Vérification que la commande c'est bien passé 
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - L'utilisateur {TempUserAnsible} a bien été ajouter a Administrateurs sur windows", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la l'ajout au groupe Administrateurs pour {TempUserAnsible} sur windows", self.TopExit, True)
                raise Exception(f"Erreur lors de la l'ajout au groupe Administrateurs pour {TempUserAnsible} sur windows")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def SetupAnsible2(self, IPServer, TempPasswdAnsible, TempUserAnsible = "Ansible2"):

        """Cette fonction va creer et ajouter ansible2 au groupe Administrateurs.
        
        Args:
            IPServer (Str): Ip of the Server
            PassAnsible (Str): Password Ansible

        Raises:
            Exception: Connection error or change username error
        """

        try :
            # Fonction qui éxecute deux sous fonction qui vont créer un utilisateur Windows et le mettre dans le groupe d'administrateur Windows
            self.CreateTempUserAnsibleForWindows(IPServer, TempPasswdAnsible, TempUserAnsible)
            self.AddAnsible2InAdminGroupForWindows(IPServer, TempUserAnsible)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def RemoveUserWindows(self, IPServer, User = "Ansible2") :

        """Cette fonction va supprimer l'utilisateur Ansible2 du groupe Admin sur Windows.
        
        Args:
            IPServer (Str): Ip of the Server

        Raises:
            Exception: Connection error or change username error
        """
        try:
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de supprimer un utilisateur Windows
            self._MonWinRM.Run_WinRM_PS_Session(f'Remove-LocalUser -Name "{User}"')
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - L'utilisateur {User} a bien été supprimé sur windows", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la suppresion de {User} sur windows", self.TopExit, True)
                raise Exception(f"Erreur lors de la suppresion de {User} sur windows")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def Crypt_Password(self, Password, Key):
        
        """Cette fonction va chiffrer le mot de passe de l'utilisateur ansible.
        
        Args:
            Password (Str): Password of User ansible

        Raises:
            Exception: Crypt error
            
        Return:
            Str: Crypted Password
        """

        try :
            # Instanciation de la Class Fernet
            f = Fernet(Key)
            # Encodage du password en UTF-8 puis cast en byte
            Password = bytes(Password, 'utf-8')
            # Chiffrement du password
            CryptedPassword = f.encrypt(Password)
            return (CryptedPassword.decode())
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def Decrypt_Password(self, CryptedPassword, Key):
        
        """Cette fonction va déchiffrer le mot de passe de l'utilisateur ansible.
        
        Args:
            Password (Str): Password of User ansible

        Raises:
            Exception: decrypt error
            
        Return:
            Str: Decrypted Password
        """

        try :
            # Instanciation de la Class Fernet
            f = Fernet(Key)
            # Encodage du password en UTF-8 puis cast en byte
            CryptedPassword = bytes(CryptedPassword, 'utf-8')
            # Déchiffrement du password
            DecryptedPassword = f.decrypt(CryptedPassword)
            return (DecryptedPassword.decode())
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetSalt(self, Path=None) :

        """Cette fonction va aller chercher le salt.
        
        Args:
            Path (Str): Path of the salt

        Raises:
            Exception: file error
            
        Return:
            Str: salt
        """

        try :
            # Clé de chiffrement
            return(b'grlnGkOKrrwdSvYSrwY87DTbz-4NlbFLfW6Fq099X1s=')
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetErrorReport(self, Path) :

        """Cette fonction va compter le nombre de NOT OK dans le fichier de log.
        
        Args:
            Path (Str): Path to the log file.

        Raises:
            Exception: file error
            
        Return:
            Str: Content of the log file
            Int: Count of NOT OK
        """
        
        try :
            NotOkList = []
            OkList = []
            # Ouverture du fichier
            LogToRead = open(Path, "r")
            # Lecture du fichier ligne par ligne
            # Tri les "OK" et les met dans une liste et fait la même chose pour les "NOT OK" 
            for line in LogToRead:
                if "NOT OK" in line:
                    NotOkList.append(line)
                if "OK" in line : 
                    OkList.append(line)
            LogToRead.close()
            NotOkStr = "".join(NotOkList)
            OkStr = "".join(OkList)
            # Concatène les 2 listes et met les "NOT OK" en premier
            Report = f"{NotOkStr}\n{OkStr}"
            NbrError = len(NotOkList)
            return(Report, NbrError)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def CreateUserLinux(self, IPServer, UserAnsible, PassAnsible, NewUserAnsible, OSName) :

        """Cette fonction va creer un utilisateur ansible pour Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant d'ajouter un utilisateur Linux
            # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            stdin, stdout, stderr = ssh.exec_command(command=f"sudo -S -p '' useradd {NewUserAnsible} -m")
            stdin.write(PassAnsible + "\n")
            stdin.flush()
            # Vérification que la commande c'est bien passé 
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors de la création de l'utilisteur {NewUserAnsible} sur Linux erreur : {stderr.readlines()}", self.TopExit, True)
                raise Exception(f"Erreur lors de la création de l'utilisteur {NewUserAnsible} sur Linux erreur : {stderr.readlines()}")
            else :
                self._MyObjLog.AjouteLog(f"OK - Création de l'utilisteur {NewUserAnsible} sur Linux", self.TopExit, True)
            if OSName != "CentOS Linux" :
                # Connexion a Paramiko
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
                # Commande permettant de mettre le bon interpreteur pour un utilisateur Linux
                # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
                # Et vide la variable stdin
                stdin, stdout, stderr = ssh.exec_command(command=f"sudo -S -p '' usermod --shell /bin/bash {NewUserAnsible}")
                stdin.write(PassAnsible + "\n")
                stdin.flush()
                # Vérification que la commande c'est bien passé 
                if stdout.channel.recv_exit_status() != 0:
                    self._MyObjLog.AjouteLog(f"Erreur lors de la mise a jour de l'interpréteur {NewUserAnsible} sur Linux erreur : {stderr}", self.TopExit, True)
                    raise Exception(f"Erreur lors de la mise a jour de l'interpréteur {NewUserAnsible} sur Linux erreur : {stderr}")
                else :
                    self._MyObjLog.AjouteLog(f"OK - Mise a jour de l'interpreteur {NewUserAnsible} sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def AddPassword(self, IPServer, UserAnsible, PassAnsible, NewUserAnsible, NewPassAnsible) :

        """Cette fonction va creer un utilisateur ansible pour Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible
            NewPassAnsible (Str): New pass Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant de mettre un password pour un utilisateur Linux
            # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' passwd {NewUserAnsible}")
            stdin.write(PassAnsible + "\n" + NewPassAnsible + "\n" + NewPassAnsible + "\n")
            stdin.flush()
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors de l'ajout du mot de passe pour l'utilisteur {NewUserAnsible} sur Linux", self.TopExit, True)
                raise Exception(f"Erreur lors de l'ajout du mot de passe pour l'utilisteur {NewUserAnsible} sur Linux")
            else :
                self._MyObjLog.AjouteLog(f"OK - Ajout du mot de passe pour l'utilisteur {NewUserAnsible} sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def AddGroupLinux(self, IPServer, UserAnsible, PassAnsible, NewUserAnsible, OSName) :

        """Cette fonction va ajouter un utilisateur ansible au groupe root sur Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant de mettre un utilisateur Linux dans le groupe sudoer
            # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            if OSName == "CentOS Linux" :
                stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' usermod -aG wheel {NewUserAnsible}")
                stdin.write(PassAnsible + "\n")
                stdin.flush()
            else :
                stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' usermod -aG sudo {NewUserAnsible}")
                stdin.write(PassAnsible + "\n")
                stdin.flush()
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors de l'ajout de l'utilisteur {NewUserAnsible} dans le groupe root sur Linux", self.TopExit, True)
                raise Exception(f"Erreur lors de l'ajout de l'utilisteur {NewUserAnsible} dans le groupe root sur Linux")
            else :
                self._MyObjLog.AjouteLog(f"OK - Ajout de l'utilisteur {NewUserAnsible} dans le groupe root sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DelUserLinux(self, IPServer, UserAnsible, NewUserAnsible, NewPassAnsible) :

        """Cette fonction va supprimer un utilisateur ansible sur Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Suppression des process en cours lié à l'utilisateur que l'on veut supprimer
            self.KillProcessLinux(IPServer, UserAnsible, NewUserAnsible, NewPassAnsible)
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, NewUserAnsible, NewPassAnsible)
            # Commande permettant de supprimer un utilisateur Linux
            # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' userdel {UserAnsible}")
            stdin.write(NewPassAnsible + "\n")
            stdin.flush()
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors de la suppression de l'utilisteur {UserAnsible} sur Linux {stderr.readlines()}", self.TopExit, True)
                raise Exception(f"Erreur lors de la suppression de l'utilisteur {UserAnsible} sur Linux {stderr.readlines()}")
            else :
                self._MyObjLog.AjouteLog(f"OK - Suppression de l'utilisteur {UserAnsible} sur Linux", self.TopExit, True)
            # Commande permettant de supprimer le dossier /home de l'utilisateur
            # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' rm -r -f /home/{UserAnsible}")
            stdin.write(NewPassAnsible + "\n")
            stdin.flush()
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors de la suppression du dossier /home de l'utilisteur {UserAnsible} sur Linux", self.TopExit, True)
                raise Exception(f"Erreur lors de la suppression du dossier /home de l'utilisteur {UserAnsible} sur Linux")
            else :
                self._MyObjLog.AjouteLog(f"OK - Suppression du dossier /home de l'utilisteur {UserAnsible} sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def KillProcessLinux(self, IPServer, UserAnsible, NewUserAnsible, NewPassAnsible):

        """Cette fonction va arreter le process ansible sur Linux.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible

        Raises:
            Exception: Connection error or change username error
        """
        
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, NewUserAnsible, NewPassAnsible)
            cmd_sudo = """sudo -s su"""
            # Commande permettant de supprimer les process liés à un utilisateur Linux
            # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
            # Et vide la variable stdin
            chan = ssh.invoke_shell()
            chan.send(cmd_sudo + '\n')
            chan.send(f'{NewPassAnsible}' + '\n')
            time.sleep(1)
            chan.send(f"echo $?" + "\n")
            time.sleep(1)
            chan.send(f"pkill -u {UserAnsible}" + "\n")
            time.sleep(1)
            # stdin, stdout, stderr = ssh.exec_command(f"sudo -S -p '' killall -u {UserAnsible}")
            # stdin.write(NewPassAnsible + "\n")
            # # Vérification que la commande c'est bien passé
            # if stdout.channel.recv_exit_status() != 0:
            #     self._MyObjLog.AjouteLog(f"Erreur lors de l'arret du process {UserAnsible} sur Linux", self.TopExit, True)
            #     raise Exception(f"Erreur lors de l'arret du process {UserAnsible} sur Linux : {stderr.readlines()}", self.TopExit, True)
            # else :
            #     self._MyObjLog.AjouteLog(f"OK - Arret de l'utilisteur {UserAnsible} sur Linux", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def SetupUserAnsibleLinux(self, IPServer, UserAnsible, PassAnsible, NewUserAnsible, NewPassAnsible, IDOS):

        """Cette fonction va creer et ajouter le nouvel utilisateur ansible au groupe Administrateurs.
        
        Args:
            IPServer (Str): Ip of the Server
            UserAnsible (Str): User Ansible
            PassAnsible (Str): Password Ansible
            NewUserAnsible (Str): New user Ansible
            NewPassAnsible (Str): New pass Ansible
            IDOS (int): ID of the OS

        Raises:
            Exception: Connection error or change username error
        """

        try :
            # Fonction qui éxecute trois sous fonctions qui vont créer un utilisateur Linux, lui attribuer un password et le mettre dans le groupe d'administrateur Linux
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            OSName = MonOS.GetOSName(IDOS)
            self.CreateUserLinux(IPServer, UserAnsible, PassAnsible, NewUserAnsible, OSName)
            self.AddPassword(IPServer, UserAnsible, PassAnsible, NewUserAnsible, NewPassAnsible)
            self.AddGroupLinux(IPServer, UserAnsible, PassAnsible, NewUserAnsible, OSName)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
