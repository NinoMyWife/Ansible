##########################################################################
# Importattion des bibliothèques
##########################################################################

from ast import Break
import os
import sys
from queue import Empty
import mysql.connector
import inspect
import Class_Colors
import re
from time import strftime

##########################################################################
# Importation des classes
##########################################################################

from Class_Hypervisor import Class_Hypervisor
from Class_OS import Class_OS
from Class_Tools import Class_Tools
from Class_Connectivity import Class_Connectivity
from Class_Security import Class_Security
from Class_PoolIP import Class_PoolIP
from Class_IPServer import Class_IPServer
from Class_ServerGroup import Class_ServerGroup
from Class_ServerApps import Class_ServerApps
from Class_Ansible_Security import Class_Ansible_Security

class Class_Servers(Exception):

    """A class which contains all the methods on the Server:
    
    - Get Infos Server Windows
    - Get InfosServer Linux
    - Insert Server BDD
    - Add Server
    - Delete Server
    - Set Unknown Server BDD
    """

    def __init__(self, MyObjLog, MonWinRM, MaBDD):
        self._MyObjLog = MyObjLog
        self._MonWinRM = MonWinRM
        self._MaBDD = MaBDD
        self._hostname = "Unknown"
        self._idhyperviseur = 3
        self._idos = 1
        self._commonname = "Unknown"
        self._useransible = "ansible"
        self._passansible = Class_Ansible_Security.Decrypt_Password(self, "XXXXXX", Class_Ansible_Security.GetSalt(self))
        self._deleted = 0
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        self._IDServer = None
        self._IDPoolIP = None
        self._Type = None
        self._Name_VLAN = None
        self._NewUserAnsible = None
        self._NewPassAnsible = None
        self._IpIsSecondary = False
        self.Mdp = False


    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonWinRM(self):
        return self._MonWinRM
    def get_hostname(self):
        return self._hostname
    def get_idhyperviseur(self):
        return self._idhyperviseur
    def get_idos(self):
        return self._idos
    def get_commonname(self):
        return self._commonname
    def get_useransible(self):
        return self._useransible
    def get_passansible(self):
        return self._passansible
    def get_deleted(self):
        return self._deleted
    def get_IDServer(self):
        return self._IDServer
    def get_IDPoolIP(self):
        return self._IDPoolIP
    def get_Type(self):
        return self._Type
    def get_Name_VLAN(self):
        return self._Name_VLAN
    def get_NewUserAnsible(self):
        return self._NewUserAnsible
    def get_NewPassAnsible(self):
        return self._NewPassAnsible
    def get_IpIsSecondary(self):
        return self._IpIsSecondary
    
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
    def set_hostname(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._hostname = value
        else :
            raise "Property Error"
    def set_idhyperviseur(self, value):
        if (type(value) == int):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._idhyperviseur = value
        else :
            raise "Property Error"
    def set_idos(self, value):
        if (type(value) == int):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._idos = value
        else :
            raise "Property Error"
    def set_commonname(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._commonname = value
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
    def set_deleted(self, value):
        if (type(value) == int):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._deleted = value
        else :
            raise "Property Error"
    def set_IDServer(self, value):
        if (type(value) == int):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._IDServer = value
        else :
            raise "Property Error"
    def set_IDPoolIP(self, value):
        if (type(value) == int):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._IDPoolIP = value
        else :
            raise "Property Error"
    def set_Type(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._Type = value
        else :
            raise "Property Error"
    def set_Name_VLAN(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._Name_VLAN = value
        else :
            raise "Property Error"
    def set_NewUserAnsible(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._NewUserAnsible = value
        else :
            raise "Property Error"
    def set_NewPassAnsible(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._NewPassAnsible = value
        else :
            raise "Property Error"
    def set_IpIsSecondary(self, value):
        if (type(value) == bool):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._NewPassAnsible = value
        else :
            raise "Property Error"

    def __del__(self):
        print("Objet detruit")
    
    def GetInfosServerWindows(self, IPServer):
        
        """This function return informations of Windows Server

        Args:
            IP (str): A Server IP

        Returns:
            str: Return informations of Windows Server
        """
        try :
            # Instanciation des Objets MonTools, MonOS, MonIPServer, MonHypervisor, MonPoolIP
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonOs = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonIPServer = Class_IPServer(self._MyObjLog, self._MaBDD)
            MonHypervisor = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            self._hostname = MonTools.GetHostnameWindows(IPServer)
            self._commonname = self._hostname
            self._Type = "windows"
            self._Name_VLAN = MonTools.Get_Name_VLAN(IPServer)
            self._MyObjLog.AjouteLog(f"OK - Attribution du common name: {self._commonname}", self.TopExit, True)
            # Si l'IP est la même mais que le Hostname est différent
            if (MonTools.SameIpButDiffHostname(IPServer, self._hostname) == 1):     
                self._IDServer = self.GetServeurID(IPServer)
                self.DeleteAllForServerByServerID(self._IDServer)
                return
            # Si le Hostname est déjà existant en base
            if (MonTools.HostnameExist(self._hostname) == 1):
                try :
                    # Si le couple {Hostname,IP} n'est pas deja enregistré en base
                    if (MonTools.IsHostnameANDIPAlreadyExist(self._hostname, IPServer) == 0) :
                        self._IDServer = self.GetIdServerWithHostname(self._hostname)
                        self._IDPoolIP = MonPoolIP.GetPoolIPID(IPServer)
                        self._idhyperviseur = MonHypervisor.GetHypervisorIDForWindowsServer(IPServer)
                        self._idos = MonOs.GetOSIDWindows(IPServer)
                        MonIPServer.AddIpOnIPServer(self._IDPoolIP, self._IDServer)
                        if self.Mdp == True:
                            # Récupération des login du Server déjà enregistré en base
                            PassAnsibleUserAnsibleIDServerByHostname = self.GetPassAnsibleUserAnsibleIDServerByHostname(self._hostname)
                            # Attribution du login du Server déjà enregistré
                            self._NewUserAnsible = PassAnsibleUserAnsibleIDServerByHostname[0]
                            # Instanciation des Objets MonAnsibleSecurity, MaConnectivity
                            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
                            MaConnectivity = Class_Connectivity(self._MyObjLog, self._MonWinRM)
                            # Attribution du password du Server déjà enregistré
                            self._NewPassAnsible = MonAnsibleSecurity.Decrypt_Password(PassAnsibleUserAnsibleIDServerByHostname[1], MonAnsibleSecurity.GetSalt())
                            # Création compte ServiceLocalxxx + droit admin et connexion via profil ServiceLocalxxx du Server déjà enregistré
                            MonAnsibleSecurity.SetupAnsible2(IPServer, self._NewPassAnsible, self._NewUserAnsible)
                            self.set_useransible(self._NewUserAnsible)
                            self.set_passansible(self._NewPassAnsible)
                            MonAnsibleSecurity._MonWinRM.set_useransible(self._NewUserAnsible)
                            MonAnsibleSecurity._MonWinRM.set_passansible(self._NewPassAnsible)
                            # Suppression du compte ansible
                            MonAnsibleSecurity.RemoveUserWindows(IPServer, "ansible")
                            # On se remet en profil de connexion par défaut le ServiceLocalxxx du Server déjà enregistré
                            self._MonWinRM.set_useransible(self._NewUserAnsible)
                            self._MonWinRM.set_passansible(self._NewPassAnsible)
                            # On teste la connexion pour voir si les login sont bon
                            if (MaConnectivity.TestConnexionAnsible(IPServer, self._useransible, self._passansible, self._Type) == True) :
                                self._MyObjLog.AjouteLog("OK - L'utilisateur Ansible et le Password Ansible ont bien été changé car on peut se connecter", self.TopExit, True)
                            else :
                                self._MyObjLog.AjouteLog("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé", self.TopExit, True)
                                raise Exception("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé")
                        self._IpIsSecondary = True
                    # Si le couple {Hostname,IP} est deja enregistré en base
                    else:
                        self._IDServer = self.GetIdServerWithHostname(self._hostname)
                        self._IDPoolIP = MonPoolIP.GetPoolIPID(IPServer)
                        self._idhyperviseur = MonHypervisor.GetHypervisorIDForWindowsServer(IPServer)
                        self._idos = MonOs.GetOSIDWindows(IPServer)
                        MonPoolIP.UpdateIsUsed(IPServer)
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur dans la partie où le hostname est présent dans la base : {err}", self.TopExit, True)
                    raise
            # Si l'IP et le Hostname ne sont pas présent dans la base alors c'est un nouveau serveur
            else:
                try:
                    # Lorsqu'on enregistre un nouveau serveur on change le nom d'utilisateur ansible et on crer un nouveau mot de passe
                    # Instanciation des Objets MonAnsibleSecurity, MaConnectivity
                    MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
                    MaConnectivity = Class_Connectivity(self._MyObjLog, self._MonWinRM)
                    self._idhyperviseur = MonHypervisor.GetHypervisorIDForWindowsServer(IPServer)
                    self._idos = MonOs.GetOSIDWindows(IPServer)
                    if self.Mdp == True:
                        # Créer un nom de compte ServiceLocalXXX
                        self._NewUserAnsible = MonAnsibleSecurity.CreateUserAnsible()
                        # Créer un password pour le compte ServiceLocalXXX
                        self._NewPassAnsible = MonAnsibleSecurity.CreatePassword(16)
                        # Création compte ServiceLocalxxx + droit admin et connexion via profil ServiceLocalxxx
                        MonAnsibleSecurity.SetupAnsible2(IPServer, self._NewPassAnsible, self._NewUserAnsible)
                        self.set_useransible(self._NewUserAnsible)
                        self.set_passansible(self._NewPassAnsible)
                        MonAnsibleSecurity._MonWinRM.set_useransible(self._NewUserAnsible)
                        MonAnsibleSecurity._MonWinRM.set_passansible(self._NewPassAnsible)
                        # Suppression du compte temporaire Ansible2
                        MonAnsibleSecurity.RemoveUserWindows(IPServer, "ansible")
                        #On se remet en profil de connexion par défaut ServiceLocalxxx
                        self._MonWinRM.set_useransible(self._NewUserAnsible)
                        self._MonWinRM.set_passansible(self._NewPassAnsible)
                        # On teste la connexion pour voir si les login sont bon
                        if (MaConnectivity.TestConnexionAnsible(IPServer, self._useransible, self._passansible, self._Type) == True) :
                            self._MyObjLog.AjouteLog("OK - L'utilisateur Ansible et le Password Ansible ont bien été changé car on peut se connecter", self.TopExit, True)
                        else :
                            self._MyObjLog.AjouteLog("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé", self.TopExit, True)
                            raise Exception("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé")
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur dans la partie où le hostname n'est pas présent dans la base : {err}", self.TopExit, True)
                    raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopRaise, True)

    def GetInfosServerLinux(self, IPServer):

        """This function return informations of Linux Server

        Args:
            IP (str): A Server IP

        Returns:
            str: Return informations of Linux Server
        """
        try:
            # Instanciation des Objets MonTools, MonOS, MonIPServer, MonHypervisor, MonPoolIP
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonIPServer = Class_IPServer(self._MyObjLog,self._MaBDD)
            MonOs = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonHypervisor = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            self._hostname = MonTools.GetHostnameLinux(IPServer, self._useransible, self._passansible)
            self._commonname = self._hostname
            self._Type = "linux"
            self._Name_VLAN = MonTools.Get_Name_VLAN(IPServer)
            self._MyObjLog.AjouteLog(f"OK - Attribution du common name: {self._commonname}", self.TopExit, True)
            # Si l'IP est la même mais que le Hostname est différent
            if (MonTools.SameIpButDiffHostname(IPServer, self._hostname) == 1):     
                self._IDServer = self.GetServeurID(IPServer)
                self.DeleteAllForServerByServerID(self._IDServer)
                return
            # Si le Hostname est déjà existant en base
            if (MonTools.HostnameExist(self._hostname) == 1):
                try: 
                    # Si le couple {Hostname,IP} n'est pas deja enregistré en base
                    if (MonTools.IsHostnameANDIPAlreadyExist(self._hostname, IPServer) == 0) :
                        self._IDServer = self.GetIdServerWithHostname(self._hostname)
                        self._IDPoolIP = MonPoolIP.GetPoolIPID(IPServer)
                        self._idos = MonOs.GetOSIDLinux (IPServer, self._useransible, self._passansible)
                        self._idhyperviseur = MonHypervisor.GetHypervisorIDForLinuxServer(IPServer, self._useransible, self._passansible, self._idos)
                        MonIPServer.AddIpOnIPServer(self._IDPoolIP, self._IDServer)
                        if self.Mdp == True:
                            # Récupération des login du Server déjà enregistré en base
                            PassAnsibleUserAnsibleIDServerByHostname = self.GetPassAnsibleUserAnsibleIDServerByHostname(self._hostname)
                            # Attribution du login du Server déjà enregistré
                            self._NewUserAnsible = PassAnsibleUserAnsibleIDServerByHostname[0]
                            # Instanciation des Objets MonAnsibleSecurity, MaConnectivity
                            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
                            MaConnectivity = Class_Connectivity(self._MyObjLog, self._MonWinRM)
                            # Attribution du password du Server déjà enregistré
                            self._NewPassAnsible = MonAnsibleSecurity.Decrypt_Password(PassAnsibleUserAnsibleIDServerByHostname[1], MonAnsibleSecurity.GetSalt())
                            # Création compte ServiceLocalxxx + droit admin et connexion via profil ServiceLocalxxx du Server déjà enregistré
                            MonAnsibleSecurity.SetupUserAnsibleLinux(IPServer, self._useransible, self._passansible, self._NewUserAnsible, self._NewPassAnsible, self._idos)
                            # Suppression du compte ansible
                            MonAnsibleSecurity.DelUserLinux(IPServer, self._useransible, self._NewUserAnsible, self._NewPassAnsible)
                            # On se remet en profil de connexion par défaut le ServiceLocalxxx du Server déjà enregistré
                            self.set_useransible(self._NewUserAnsible)
                            self.set_passansible(self._NewPassAnsible)
                            # On teste la connexion pour voir si les login sont bon
                            if (MaConnectivity.TestConnexionAnsible(IPServer, self._useransible, self._passansible, self._Type) == True) :
                                self._MyObjLog.AjouteLog("OK - L'utilisateur Ansible et le Password Ansible ont bien été changé car on peut se connecter", self.TopExit, True)
                            else :
                                self._MyObjLog.AjouteLog("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé", self.TopExit, True)
                                raise Exception("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé")
                        self._IpIsSecondary = True
                            
                    # Si le couple {Hostname,IP} est deja enregistré en base
                    else:
                        self._IDServer = self.GetIdServerWithHostname(self._hostname)
                        self._IDPoolIP = MonPoolIP.GetPoolIPID(IPServer)
                        self._idos = MonOs.GetOSIDLinux (IPServer, self._useransible, self._passansible)
                        self._idhyperviseur = MonHypervisor.GetHypervisorIDForLinuxServer(IPServer, self._useransible, self._passansible, self._idos)
                        MonPoolIP.UpdateIsUsed(IPServer)
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur dans la partie où le hostname est présent dans la base : {err}", self.TopExit, True)
            # Si l'IP et le Hostname ne sont pas présent dans la base alors c'est un nouveau serveur
            else:
                try:
                    # Lorsqu'on enregistre un nouveau serveur on change le nom d'utilisateur ansible et on crer un nouveau mot de passe
                    # Instanciation des Objets MonAnsibleSecurity, MaConnectivity
                    MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
                    MaConnectivity = Class_Connectivity(self._MyObjLog, self._MonWinRM)
                    self._idos = MonOs.GetOSIDLinux (IPServer, self._useransible, self._passansible)
                    self._idhyperviseur = MonHypervisor.GetHypervisorIDForLinuxServer(IPServer, self._useransible, self._passansible, self._idos)
                    if self.Mdp == True:
                        # Créer un nom de compte ServiceLocalXXX
                        self._NewUserAnsible = MonAnsibleSecurity.CreateUserAnsible()
                        # Créer un password pour le compte ServiceLocalXXX
                        self._NewPassAnsible = MonAnsibleSecurity.CreatePassword(16)
                        # Création compte ServiceLocalxxx + droit admin et connexion via profil ServiceLocalxxx
                        MonAnsibleSecurity.SetupUserAnsibleLinux(IPServer, self._useransible, self._passansible, self._NewUserAnsible, self._NewPassAnsible, self._idos)
                        # Suppression du compte ansible
                        MonAnsibleSecurity.DelUserLinux(IPServer, self._useransible, self._NewUserAnsible, self._NewPassAnsible)
                        #On se remet en profil de connexion par défaut ServiceLocalxxx
                        self.set_useransible(self._NewUserAnsible)
                        self.set_passansible(self._NewPassAnsible)
                        # On teste la connexion pour voir si les login sont bon
                        if (MaConnectivity.TestConnexionAnsible(IPServer, self._useransible, self._passansible, self._Type) == True) :
                            self._MyObjLog.AjouteLog("OK - L'utilisateur Ansible et le Password Ansible ont bien été changé car on peut se connecter", self.TopExit, True)
                        else :
                            self._MyObjLog.AjouteLog("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé", self.TopExit, True)
                            raise Exception("NOT OK - Le changement de mot de passe et le changement d'utilisateur s'est mal passé")
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur dans la partie où le hostname n'est pas présent dans la base : {err}", self.TopExit, True)
                    raise
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetServeurID(self, IPServer):

        """This function will return the Server ID

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error

        Return:
            int: ID of Server
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si un Serveur est associé a une IP en récupérant l'ID
            myresult = MaBDD.SelectRow(db, f"SELECT EXISTS(SELECT Servers.id FROM Servers INNER JOIN IpServer ON IpServer.IDServer = Servers.id INNER JOIN PoolIP ON PoolIP.id = IpServer.IDPoolIP WHERE PoolIP.IP = '{IPServer}' AND Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0)")
            if myresult[0][0] > 0:
                # Instanciation de l'objet de connexion a la base de données
                MaBDD = self._MaBDD
                db = MaBDD.mysqlconnector()
                # Requête qui va récupérer l'ID su Serveur
                myresult = MaBDD.SelectRow(db, f"SELECT Servers.id FROM Servers INNER JOIN IpServer ON IpServer.IDServer = Servers.id INNER JOIN PoolIP ON PoolIP.id = IpServer.IDPoolIP WHERE PoolIP.IP = '{IPServer}' AND Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0")
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'id du serveur : {myresult[0][0]}", self.TopExit, True)
                return (myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("NOTICE - Pas de serveur associé a cette IP", self.TopExit, True, None, Class_Colors.IBlue)
                return None
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def InsertServerBDD(self, Hostname, Commonname, Idhyperviseur, Idos, Useransible, Passansible, Deleted, IPServer) :

        """This function insert the object Server into the DataBase
        Raises:
            mysql.connector.errors.Error:  Error mysql
        """
        try :
            # Instanciation des Objets MonIPServer, MonPoolIP, MonAnsibleSecurity
            MonIPServer = Class_IPServer(self._MyObjLog, self._MaBDD)
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            Passansible = MonAnsibleSecurity.Crypt_Password(Passansible, MonAnsibleSecurity.GetSalt())
            self._IDServer = self.GetServeurID(IPServer)
            self._IDPoolIP = MonPoolIP.GetPoolIPID(IPServer)
            # Si le serveur est déjà présent dans la base alors on update
            if (self._IDServer != None) :
                try :
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va Update un Serveur
                    MaBDD.UpdateRow(db, f"Update Servers SET Hostname = '{Hostname}', IDHypervisor = {Idhyperviseur}, Idos = {Idos}, Useransible = '{Useransible}', Passansible = '{Passansible}', Deleted = {Deleted} WHERE ID = {self._IDServer} AND Deleted = 0")
                    self._MyObjLog.AjouteLog(f"OK - Update de la table server : Hostname = '{Hostname}', IDHypervisor = '{Idhyperviseur}', Idos = {Idos}, Useransible = '{Useransible}', Passansible = '{Passansible}', Deleted = {Deleted} WHERE ID = {self._IDServer} AND Deleted = 0", self.TopExit, True)
                except (mysql.connector.errors.Error) as err:
                    self._MyObjLog.AjouteLog(f"Erreur lors de l'update dans la table server : {err}", self.TopExit, True)
                    raise
            # Si le serveur n'est pas déjà présent dans la base alors on l'insère.
            else :
                try :
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    date = strftime("%Y-%m-%d")
                    db = MaBDD.mysqlconnector()
                    # Requête qui va Insérer un Serveur
                    MaBDD.InsertRow(db, f"INSERT INTO Servers (Hostname, Commonname, IDHypervisor, Idos, Useransible, Passansible, Deleted, UpdateDatePassword) VALUE ('{Hostname}', '{Commonname}', {Idhyperviseur}, {Idos}, '{Useransible}', '{Passansible}', {Deleted}, '{date}')")
                    self._MyObjLog.AjouteLog(f"OK - Insert dans la table server : (Hostname, Commonname, IDHypervisor, Idos, Useransible, Passansible, Deleted, UpdateDatePassword) VALUE ('{Hostname}', '{Commonname}', {Idhyperviseur}, {Idos}, '{Useransible}', '{Passansible}', {Deleted}, '{date}')", self.TopExit, True)
                except (mysql.connector.errors.Error) as err:
                    self._MyObjLog.AjouteLog(f"Erreur lors de l'insert dans la table server : {err}", self.TopExit, True)
                    raise
                try :
                    # On ajoute l'IP au Serveur que l'on vient de créer
                    self._IDServer = self.GetLastIDServer()
                    MonIPServer.AddIpOnIPServer(self._IDPoolIP, self._IDServer)     # On met a jour la table IpServeur
                except Exception as err :
                    self._MyObjLog.AjouteLog(f"Erreur lors de l'ajout de l'ip a un serveur déjà existant : {err}", self.TopExit, True)
                    raise
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK - Exception in {__file__} Class:{__class__.__name__} - Method: {sys._getframe().f_code.co_name} - Erreur = {err}", self.TopExit, True)
            raise

    def DeleteServer(self, IDServer):

        """This function remove a Server from the DataBase

        Args:
            IDServer (int): ID of the Server

        Raises:
            mysql.connector.errors.Error: Error mysql

        Returns:
            Bool: 0 it's good, 1 An error has occured
        """

        try:
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 1 pour un Serveur
            MaBDD.UpdateRow(db, f"UPDATE Servers SET Deleted = 1 WHERE ID = {IDServer}")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetLastIDServer(self):

        """This function will retrieve the last record from the server table in order to retrieve the id

        Raises:
            Exception: Connection error

        Return:
            ID of Table server
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le dernier ID Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT ID FROM Servers WHERE Deleted = 0 ORDER BY ID DESC LIMIT 0,1")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Obtention du dernier ID de serveur : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération du dernier ID a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération du dernier ID a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetIdServerWithHostname(self, Hostname):

        """This function will  get the IDServer with the Hostname

        Args:
            Hostname (str): Hostname

        Raises:
            Exception: Connection error
            
        Return:
            Int : Server ID
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer l'ID du Serveur grâce au Hostname
            myresult = MaBDD.SelectRow(db, f"SELECT id FROM Servers WHERE hostname = '{Hostname}' AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Obtention de l'ID du serveur avec le Hostname : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération du dernier ID du server grace au Hostname a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération du dernier ID du server grace au Hostname a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetIDServerWithIP(self, IPServer):

        """This function will  get the IDServer with the IP

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error
            
        Return:
            Int : Server ID
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer l'ID du Serveur grâce à l'IP
            myresult = MaBDD.SelectRow(db, f"SELECT Servers.ID FROM Servers INNER JOIN IpServer ON Servers.ID = IpServer.IDServer INNER JOIN PoolIP ON IpServer.IDPoolIP = PoolIP.ID WHERE PoolIP.IP LIKE '{IPServer}' AND Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération de l'ID a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de l'ID a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetHostnameWithIDServer(self, IDServer):
        
        """This function will  get the Hostname with the ID

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str: Hostname
        """
        
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le Hostname grâce a l'IDServeur
            myresult = MaBDD.SelectRow(db, f"SELECT Hostname FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult :
                self._MyObjLog.AjouteLog("OK - L'Hostname a bien été récupéré", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("L'Hostname n'a pas pu être récupéré", self.TopExit, True)
                raise mysql.connector.errors.Error("L'Hostname n'a pas pu être récupéré")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteAllForServerByServerID (self, IDServer):

        """This function will delete all link with the Server

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
        """
        
        try:
            # Instanciation des Objets MyIPServer, MyServerApps, MyServerGroup
            MyIPServer = Class_IPServer(self._MyObjLog, self._MaBDD)
            MyServerApps = Class_ServerApps(self._MyObjLog, self._MaBDD)
            MyServerGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            # Suppression de tout ce qui est lié avec ce Serveur en mettant Deleted a 1
            # Suppression de toutes les IP lié a ce Serveur
            MyIPServer.DeleteAllIPServerByIDServer(IDServer)
            self._MyObjLog.AjouteLog("OK - Update Deleted => 1 For IPServer", self.TopExit, True)
            # Suppression de toutes les Applications lié a ce Serveur
            MyServerApps.DeleteServerApp(IDServer)
            self._MyObjLog.AjouteLog("OK - Update Deleted => 1 For ServerApps", self.TopExit, True)
            # Suppression de tous les Groupes lié a ce Serveur
            MyServerGroup.DeleteServerGroup(IDServer)
            self._MyObjLog.AjouteLog("OK - Update Deleted => 1 For ServerGroup", self.TopExit, True)
            # Suppression du Serveur
            self.DeleteServer(IDServer)
            self._MyObjLog.AjouteLog("OK - Update Deleted => 1 For Server", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
                        self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopRaise, True)

    def GetServerPassword(self, IDServer):

        """This function will  get the Server password with the ID

        Args:
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Password
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui récupérer le password du Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT Passansible FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération du mot de passe : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération du mot de passe a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération du mot de passe a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetServerLogin(self, IDServer):

        """This function will  get the Server Login with the ID

        Args:
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Login
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui récupérer le user du Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT Useransible FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération du login : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération du login a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération du login a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetPassAnsibleUserAnsibleIDServerByIPServer(self, IPServer):

        """This function will  get the Server Login with the ID

        Args:
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Login
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui récupérer le user et le password du Serveur grâce a l'IP
            myresult = MaBDD.SelectRow(db, f"SELECT Servers.ID, Servers.UserAnsible, Servers.PassAnsible, Servers.Hostname FROM Servers INNER JOIN IpServer ON IpServer.IDServer = Servers.ID INNER JOIN PoolIP ON PoolIP.ID = IpServer.IDPoolIP WHERE PoolIP.IP LIKE '{IPServer}' AND Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération des infos Ansible : ID = {myresult[0][0]} | Useransible = {myresult[0][1]} | PassAnsible = {myresult[0][2]}", self.TopExit, True)
                return(myresult[0])
            else:
                self._MyObjLog.AjouteLog("Récupération des infos Ansible a échoué", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetPassAnsibleUserAnsibleIDServerByHostname(self, Hostname):

        """This function will  get the Server Login with the ID

        Args:
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Login
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui récupérer le user et le password du Serveur grâce au Hostname
            myresult = MaBDD.SelectRow(db, f"SELECT UserAnsible, PassAnsible FROM Servers WHERE Hostname LIKE '{Hostname}' AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération des infos Ansible : Useransible = {myresult[0][0]} | PassAnsible = {myresult[0][1]}", self.TopExit, True)
                return(myresult[0])
            else:
                self._MyObjLog.AjouteLog("Récupération des infos Ansible a échoué", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise


    def UpdateUserAnsibleAndPasswordAnsible(self, NewPasswordAnsible, OldPassansible, IDServer):

        """This function will update the Servers table with the New User Ansible and the New Password Ansible

        Args:
            NewPasswordAnsible (str): New Password Ansible
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Login
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            date = strftime("%Y-%m-%d")
            db = MaBDD.mysqlconnector()
            # Requête qui va Update l'utilisateur et le password d'un serveur
            MaBDD.UpdateRow(db, f"Update Servers SET Passansible = '{NewPasswordAnsible}', OldPassansible = '{OldPassansible}', UpdateDatePassword = '{date}' WHERE ID = {IDServer} AND Deleted = 0")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetOldPassAnsible(self, IDServer):

        """This function will get the old pass Ansible With IDServer

        Args:
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Login
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer l'ancien mot de passe d'un Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT OldPassAnsible FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération du OldPassAnsible : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération du OldPassAnsible a échoué", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)

    def GetServerTypeWithIDServer(self, IDServer):

        """This function will get the Type of the server

        Args:
            IDServer (int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Str : Login
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le type du serveur grâce a l'IDServeur
            myresult = MaBDD.SelectRow(db, f"SELECT OS.`Type` FROM OS INNER JOIN Servers ON Servers.IDOS = OS.ID WHERE Servers.ID = {IDServer} AND Servers.Deleted = 0 AND OS.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération du Type : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération du Type a échoué", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetServerListWherePasswordNeedUpdate(self, NbrMonth):

        """This function will get the list of server which need to change password

        Raises:
            Exception: Connection error
            
        Return:
            list : List of server
        """
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer la liste des Serveurs qui ont besoin de mettre a jour leur password
            myresult = MaBDD.SelectRow(db, f"SELECT IP FROM PoolIP INNER JOIN IpServer ON PoolIP.ID = IpServer.IDPoolIP INNER JOIN Servers ON IpServer.IDServer = Servers.ID WHERE Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0 AND DATE(UpdateDatePassword) < DATE(DATE_SUB(NOW(), INTERVAL {NbrMonth} MONTH))")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog("OK - Récupération de la liste des IP", self.TopExit, True)
                return myresult
            else:
                self._MyObjLog.AjouteLog("Récupération de la liste des IP impossible", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de la liste des IP impossible")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetAllIpAddressForOneMachine(self, IPServer):
        
        try :
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de récupérer toutes les IP lié a cette Machine
            self._MonWinRM.Run_WinRM_PS_Session('Get-NetIPAddress -AddressFamily:IPv4 | Where-Object IPAddress -NotMatch "169*"  | Where-Object IPAddress -NotMatch "127*" | select IPAddress | ft -hide', False)
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                # Nettoyage de la liste
                ListIP = re.split("\s+", self._MonWinRM.std_out)
                ListIP.pop(0)
                ListIP.pop(len(ListIP)-1)
                self._MyObjLog.AjouteLog(f"OK - Récupération des IP windows : {ListIP}", self.TopExit, True)
                return (ListIP)
            else:
                self._MyObjLog.AjouteLog("NOT OK - Erreur lors de la récupération des IP windows", self.TopExit, True)
                raise Exception("NOT OK - Erreur lors de la récupération des IP windows")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetServerListWithTopAnsible(self):

        """This function will get the list of server with TopAnsible = 1

        Raises:
            Exception: Connection error
            
        Return:
            list : List of server
        """
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer la liste des Serveurs avec TopAnsible à 1
            myresult = MaBDD.SelectRow(db, f"SELECT IP FROM PoolIP WHERE TopAnsible = 1 AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog("OK - Récupération de la liste des IP", self.TopExit, True)
                return myresult
            else:
                self._MyObjLog.AjouteLog("Récupération de la liste des IP impossible", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de la liste des IP impossible")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetAllPasswordForAnIP(self, IP):
        
        """Cette fonction va renvoyer tous les mots de passes enregistrer pour une IP.
        
        Args:
            IP (Str): IP of the server.

        Raises:
            Exception: SQL error
            
        Return:
            List: List of password
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer tout les passwords pour une IP
            myresult = MaBDD.SelectRow(db, f"SELECT PassAnsible, OldPassansible FROM Servers INNER JOIN IpServer ON Servers.ID = IpServer.IDServer INNER JOIN PoolIP ON PoolIP.ID = IpServer.IDPoolIp WHERE PoolIP.IP LIKE '{IP}' AND Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération des Password: {myresult}", self.TopExit, True)
                ListPasswords = f"{myresult[0][1]},{myresult[0][0]}"
                return(ListPasswords)
            else:
                self._MyObjLog.AjouteLog("Récupération des Password a échoué", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DecryptAllPassword(self, IP):

        """Cette fonction va decrypter tous les mots de passes envoyé en entrée.
        
        Args:
            IP (Str): IP of the server.

        Raises:
            Exception: SQL error
            
        Return:
            List: List of decrypted password
        """

        try :
            # Instanciation de l'objet MonAnsibleSecurity
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de tout les passwords d'un Serveur
            AllPassword = self.GetAllPasswordForAnIP(IP)
            DecryptPasswordList = []
            ListDecrypt = AllPassword.split(",")
            # Déchiffrement de tout les passwords
            for CryptPassword in ListDecrypt:
                DecryptPasswordList.append(MonAnsibleSecurity.Decrypt_Password(CryptPassword, MonAnsibleSecurity.GetSalt()))
            return(DecryptPasswordList)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
