##########################################################################
# Importation des bibliotheques
##########################################################################

from pickle import FALSE
from random import getrandbits
#from tkinter.messagebox 
from xml.etree.ElementTree import TreeBuilder
import paramiko
import os
import inspect
import Class_Colors
import winrm
import sys
import socket
from Class_Security import Class_Security

##########################################################################
# Importation des classes
##########################################################################

class Class_Connectivity(Exception):

    """A class which contains some usefull tools for connectivity:

    - IPIsPingable
    - TestConnexionAnsible
    - IsSSHAccessible
    - WinrmPort
    """

    def __init__(self, MyObjLog, MonWinRM):
        self._MyObjLog = MyObjLog
        self._MonWinRM = MonWinRM
        self._file_conf_path = "/var/log"
        self._namelogpy = "LogAutoDiscoveryAnsible.txt"
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False

    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonWinRM(self):
        return self._MonWinRM
    def get_file_conf_path(self):
        return self._file_conf_path
    def get_namelogpy(self):
        return self._namelogpy
    
    # ?  setter method
    def set_MyObjLog(self, value):
        if (type(value) == type(self._MonWinRM)):
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
    def set_file_conf_path(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._file_conf_path = value
        else :
            raise "Property Error"
    def set_namelogpy(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._namelogpy = value
        else :
            raise "Property Error"

    def IsSSHAccessible(self, host):

        """This function will test the ssh port for Linux Server

        Args:
            host (str): IP of Linux Server

        Returns:
            bool: 1 = error | 0 = good
        """

        try:
            # Connexion à un port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host,22))

            if result == 0:
                self._MyObjLog.AjouteLog("OK - Le SSH est accessible", self.TopExit, True)
                sock.close()
                return 1
            else:
                self._MyObjLog.AjouteLog("NOTICE - Le SSH n'est pas accessible", self.TopExit, True, None, Class_Colors.IBlue)
                sock.close()
                return 0
        except (socket.error) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def WinrmPort(self, host):

        """This function will test the ssh port for Windows Server

        Args:
            host (str): IP of Linux Server

        Returns:
            bool: 1 = error | 0 = good
        """

        try:
            # Connexion à un port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, 5985))
            
            if result == 0:
                self._MyObjLog.AjouteLog("NOTICE - Le port WINRM est accessible", self.TopExit, True)
                sock.close()
                return 1
            else:
                self._MyObjLog.AjouteLog("NOTICE - Le port WINRM n'est pas accessible", self.TopExit, True)
                sock.close()
                return 0
        except (socket.error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def IPIsPingable(self, IPServer):

        """This function will test if IP is pingable

        Args:
            host (str): A Server IP

        Raises:
            Error : Ping error

        Returns:
            Bool : 0 it's ok, 1 it's not ok
        """
    
        try:
            # Commande permettant de ping l'IP d'un serveur
            response = os.system("ping -c 1 " + IPServer)

            if response == 0:
                return(1)
            else:
                return(0)

        except (Exception) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def TestConnexionAnsible(self, IPServer, UserAnsible, PassAnsible, TypeOS):

        """This function test the connection to Ansible

        Args:
            IPServer (str): A Server IP
            UserAnsible (str): User Ansible
            PassAnsible (str): Password Ansible
            TypeOS (str): Type of the OS

        Raises:
            Exception: Connection error
        """

        try:
            # Si la machine est une machine Windows on teste la connexion WinRM
            if TypeOS == 'windows' :
                try:
                    # Attribution de l'IP et des logins a l'Objet de connexion Windows (WinRM)
                    self._MonWinRM.IP = IPServer
                    self._MonWinRM.set_useransible(UserAnsible)
                    self._MonWinRM.set_passansible(PassAnsible)
                    # Commande permettant de récupérer toutes les IP lié a cette Machine
                    self._MonWinRM.Run_WinRM_PS_Session('test', False)
                    self._MyObjLog.AjouteLog("OK - Connexion Ansible", self.TopExit, True)
                    return True
                
                except Exception as err :
                    self._MyObjLog.AjouteLog("NOT OK - N'arrive pas a se connecter", self.TopExit, True)
                    return False
            # Si la machine est une machine Linux on teste la connexion SSH via Paramiko
            elif TypeOS == 'linux':
                try:
                    # Connexion a Paramiko
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
                    self._MyObjLog.AjouteLog("OK - Connexion SSH Linux", self.TopExit, True)
                    return True
                except (Exception) as err :
                    self._MyObjLog.AjouteLog("Erreur de connexion Ansible pour Linux OS", self.TopExit, True)
            else :
                self._MyObjLog.AjouteLog("N'arrive pas a se connecter", self.TopExit, True)
                return False
        except (Exception) as err :
            self._MyObjLog.AjouteLog("NOT OK - Exception in % Class:%s - Method: %s - Erreur = %s" % (__file__,__class__.__name__, inspect.stack()[0][3], err), self.TopExit, True)

    def TestConnectivity(self, IP, TopWinRm = False, TopSSH= False, TopPing = False) :

        """This function will test if IP is pingable

        Args:
            IP (str): A Server IP
            TopWinRm (bool) : For Server Windows
            TopSSH (bool) : For Server Linux
            TopPing (bool) : Try to test if it's pingable

        Raises:
            Error : Ping error

        Returns:
            Bool : 0 it's ok, 1 it's not ok
        """

        if self.IPIsPingable(IP) == 1 :
            TopPing = True
        if self.WinrmPort(IP) == 1 :
            TopWinRm = True
        if self.IsSSHAccessible(IP) == 1 :
            TopSSH= True
        if TopSSH == True and TopWinRm == True :
            TopSSH = False
        return (TopWinRm, TopSSH, TopPing)