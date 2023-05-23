##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
import sys
import paramiko
from Class_Security import Class_Security
from Class_Servers import Class_Servers
from Class_ServerApps import Class_ServerApps
from Class_Ansible_Security import Class_Ansible_Security
from Class_OS import Class_OS

##########################################################################
# * Début du script
##########################################################################

class Class_App(Exception):
    
    def __init__(self, MyObjLog, MonWinRM, MaBDD, MonServer):
        self._MyObjLog = MyObjLog
        self._MonWinRM = MonWinRM
        self._MonServer = MonServer
        self._MaBDD = MaBDD
        self._useransible = Class_Security().UserAnsible
        self._passansible = Class_Security().PassAnsible
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False

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

    def AffectApplicationsToServerForWindows(self, IPServer, IDOS):

        """This function will affect an application to a windows server

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error
        """
        
        try :
            # Instanciation des Objets AppList, Monserver, MonServerApps
            AppList = self.GetIDANDApplicationList(IDOS)
            MonServerApps = Class_ServerApps(self._MyObjLog, self._MaBDD)
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            IDServer = self._MonServer.GetIDServerWithIP(IPServer)
            IDServerAlreadyExistInServerApp = MonServerApps.IDServerAlreadyExistInServerApps(IDServer)
            # Commande permettant de récupérer les services en cours d'éxecution Windows
            self._MonWinRM.Run_WinRM_PS_Session("Get-Service | Where Status -eq 'Running' | Select Name")
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                for App in AppList :
                    if App[1] in self._MonWinRM.std_out:
                        # Si le serveur ne possède pas deja des entree dans la table ServerApps on insere
                        if (IDServerAlreadyExistInServerApp == 0) :
                            Hostname = self._MonServer.GetHostnameWithIDServer(IDServer)
                            MonServerApps.InsertServerApp(IDServer, App[0])
                            self._MyObjLog.AjouteLog(f"NOTICE - Hostname = {Hostname}, IDServer = {IDServer}, ID = {App[0]}, App = {App[1]}", self.TopExit, True)
                        # Sinon le serveur possède deja des entree dans la table ServerApps on delete pour reinserer
                        else :
                            IDServerAlreadyExistInServerApp = 0
                            Hostname = self._MonServer.GetHostnameWithIDServer(IDServer)
                            MonServerApps.DeleteAllAppForServerInServerApp(IDServer)
                            MonServerApps.InsertServerApp(IDServer, App[0])
                            self._MyObjLog.AjouteLog(f"NOTICE - Hostname = {Hostname}, IDServer = {IDServer}, ID = {App[0]}, App = {App[1]}", self.TopExit, True)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def AffectApplicationsToServerForLinux(self, IPServer, IDOS):
        
        """This function will affect an application to a linux server

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error
        """
        
        try :
            # Instanciation des Objets AppList, Monserver, MonServerApps, MonOS
            AppList = self.GetIDANDApplicationList(IDOS)
            MonServerApps = Class_ServerApps(self._MyObjLog, self._MaBDD)
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            IDServer = self._MonServer.GetIDServerWithIP(IPServer)
            IDServerAlreadyExistInServerApp = MonServerApps.IDServerAlreadyExistInServerApps(IDServer)
            GetOSInfo = MonOS.GetOSInfo(IPServer)
            Version = int(GetOSInfo[0][0])
            OSName = GetOSInfo[0][1]
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, self._MonServer.get_useransible(), self._MonServer.get_passansible())
            # Pour les machines centos version 7 et + la commande n'est pas la meme
            if OSName == "CentOS Linux" and Version >= 7 : 
                # Commande permettant de récupérer les service en cours d'éxecution Linux     
                stdin, stdout, stderr = ssh.exec_command("systemctl --type=service --state=running")
                self._MyObjLog.AjouteLog("OK - Connection SSH pour les services CentOS Linux", self.TopExit, True)
            else :
                # Commande permettant de récupérer les service en cours d'éxecution Linux
                # En mettant le mot de passe root automatiquement (grâce a "-S -p ''" et "stdin.write")
                # Et vide la variable stdin
                stdin, stdout, stderr = ssh.exec_command("sudo -S -p '' service --status-all | grep -v '[-]'")
                stdin.write(self._MonServer.get_passansible() + "\n")
                stdin.flush()
                self._MyObjLog.AjouteLog("OK - Connection SSH pour les services Debian", self.TopExit, True)
            # Nettoyage du stdout
            serviceslist = stdout.readlines()
            separator = ""
            services = separator.join(serviceslist)
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog("Erreur lors de la récupération du Hostname Linux", self.TopExit, True)
                raise Exception("Erreur lors de la récupération du Hostname Linux")
            else :
                for App in AppList :
                    if App[1] in services:
                        # Si le serveur ne possède pas deja des entree dans la table ServerApps on insere
                        if (IDServerAlreadyExistInServerApp == 0) :
                            Hostname = self._MonServer.GetHostnameWithIDServer(IDServer)
                            MonServerApps.InsertServerApp(IDServer, App[0])
                            self._MyObjLog.AjouteLog(f"NOTICE - Hostname = {Hostname}, IDServer = {IDServer}, ID = {App[0]}, App = {App[1]}", self.TopExit, True)
                        # Sinon le serveur possède deja des entree dans la table ServerApps on delete pour reinserer
                        else :
                            IDServerAlreadyExistInServerApp = 0
                            Hostname = self._MonServer.GetHostnameWithIDServer(IDServer)
                            MonServerApps.DeleteAllAppForServerInServerApp(IDServer)
                            MonServerApps.InsertServerApp(IDServer, App[0])
                            self._MyObjLog.AjouteLog(f"NOTICE - Hostname = {Hostname}, IDServer = {IDServer}, ID = {App[0]}, App = {App[1]}", self.TopExit, True)
                    else :
                        continue
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetIDANDApplicationList(self, IDOS):
        
        """This function collect the application list

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error

        Return:
            list
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête permettant de récupérer les ID et la liste des Application
            myresult = MaBDD.SelectRow(db, f"SELECT ID, ServiceNames FROM Applications WHERE Deleted = 0 AND IDOS = {IDOS}")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog("OK - Récupération de la liste des Applications", self.TopExit, True)
                return myresult
            else:        
                self._MyObjLog.AjouteLog("NOT OK - Erreur lors de la recupération de la liste des Applications", self.TopExit, True)
                raise mysql.connector.errors.Error("NOT OK - Erreur lors de la recupération de la liste des Applications")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
