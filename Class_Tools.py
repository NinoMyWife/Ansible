##########################################################################
# Importation des bibliotheques
##########################################################################

from pickle import FALSE
from random import getrandbits
#from tkinter.messagebox 
from xml.etree.ElementTree import TreeBuilder
import paramiko
import winrm
import sys
import mysql.connector
import socket
from datetime import datetime
import inspect
import Class_Colors

##########################################################################
# Importation des classes
##########################################################################

from Class_Security import Class_Security

class Class_Tools(Exception):

    """A class which contains some usefull tools:

    - GetUserAnsible
    - GetPassAnsible
    - HostnameExist
    - GetHostnameWindows
    - GetHostnameLinux
    - GetUserAdmin
    - GetPassAdmin
    - Get_VLAN_Name
    - IsHostnameANDIPAlreadyExist
    - IpAlreadyAffectedToServer
    - IsSameHostname
    - Cartouchetop
    - Cartouchebottom
    - CheckProperty
    """
    
    def __init__(self, MyObjLog, MonWinRM, MaBDD):
        self._MyObjLog = MyObjLog
        self._MonWinRM = MonWinRM
        self._MaBDD = MaBDD
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

    def GetUserAnsible (self, IDServer): # ? PAS UTILISE

        """This function will return the Ansible User

        Args:
            IDServer (int): A Server ID

        Raises:
            mysql.connector.errors.Error: Request error

        Returns:
            str: Return the Ansible User
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer l'utilisateur d'un Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT UserAnsible FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'utilisateur ansible : {myresult}", self.TopExit, True)
                return (myresult)
            else :
                self._MyObjLog.AjouteLog("La requête n'a pas ramener de données", self.TopExit, True)
                raise mysql.connector.errors.Error("La requête n'a pas ramener de données")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetPassAnsible (self, IDServer): # ? PAS UTILISE

        """This function will return the Ansible Password

        Args:
            IDServer (int): A Server ID

        Raises:
            mysql.connector.errors.Error: Request error

        Returns:
            str: Return the Ansible Password
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le password d'un Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT PassAnsible FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de le PassAnsible ansible : {myresult}", self.TopExit, True)
                return (myresult)
            else :
                self._MyObjLog.AjouteLog("La requête n'a pas ramener de données", self.TopExit, True)
                raise mysql.connector.errors.Error("La requête n'a pas ramener de données")

        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def HostnameExist(self, Hostname):
        
        """This function Check if Hostname already Exist

        Args:
            IPServer (str): IP of the Server
            Hostname (str): Hostname of the Server

        Raises:
            mysql.connector.errors.Error: Error mysql

        Returns:
            Bool: 0 Server doesn't exist, 1 Server exist
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier que le Hostname si le Hostname est présent ou pas dans la table Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT EXISTS( SELECT Servers.ID FROM Servers WHERE Hostname = '{Hostname}' AND Deleted = 0)")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                if myresult[0][0] == 1:
                    self._MyObjLog.AjouteLog(f"OK - Hostname existe déjà : {myresult[0][0]}", self.TopExit, True)
                    return (myresult[0][0])
                elif myresult[0][0] == 0 :
                    self._MyObjLog.AjouteLog(f"OK - Hostname n'existe pas encore : {myresult[0][0]}", self.TopExit, True)
            else :
                self._MyObjLog.AjouteLog("La requête n'a pas ramener de données", self.TopExit, True)
                raise mysql.connector.errors.Error("La requête n'a pas ramener de données")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetHostnameWindows (self, IPServer):

        """This function will return the Windows Hostname

        Args:
            IPServer (str): A Server IP
            UserAnsible (str): User Ansible
            PassAnsible (str): Password Ansible

        Raises:
            Exception: Connection error

        Returns:
            str: Windows Hostname
        """

        try :
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de récupérer le hostname
            mycmd = "hostname"
            self._MonWinRM.Run_WinRM_CMD_Session(mycmd)
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                if (self._MonWinRM.std_err == None):
                    CleanedHostName = self._MonWinRM.std_out
                    self._MyObjLog.AjouteLog(f"OK - Récupération du Hostname windows : {CleanedHostName}", self.TopExit, True)
                else:
                    self._MyObjLog.AjouteLog("NOT OK - Erreur lors de la récupération du Hostname windows", self.TopExit, True)
                    raise Exception("NOT OK - Erreur lors de la récupération du Hostname windows")
            else:
                self._MyObjLog.AjouteLog(f"NOT OK - Erreur d'execution WinRM - command={mycmd} - std_out={self._MonWinRM.std_out} / status_code={self._MonWinRM.status_code}", self.TopExit, True)
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update TopAnsible a 1
            MaBDD.UpdateRow(db, f"UPDATE PoolIP SET TopAnsible = '1' WHERE IP = '{IPServer}' AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update TopAnsible => 1", self.TopExit, True)
            return(CleanedHostName)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetHostnameLinux (self, IPServer, UserAnsible, PassAnsible):

        """This function will return the Linux Hostname

        Args:
            IPServer (str): A Server IP
            
            UserAnsible (str): User Ansible
            PassAnsible (str): Password Ansible

        Raises:
            Exception: Connection error

        Returns:
            str: Linux Hostname
        """

        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant d'obtenir le hostname
            stdin, stdout, stderr = ssh.exec_command("hostname")
            self._MyObjLog.AjouteLog("OK - Connection SSH pour le Hostname", self.TopExit, True)
            try :
                # Vérification que la commande c'est bien passé
                if stdout.channel.recv_exit_status() != 0:
                    self._MyObjLog.AjouteLog("Erreur lors de la récupération du Hostname Linux", self.TopExit, True)
                    raise Exception("Erreur lors de la récupération du Hostname Linux")
                else :
                    try :
                        # Nettoyage du stdout 
                        HostName = stdout.readlines()
                        HostName = HostName[0]
                        self._MyObjLog.AjouteLog(f"OK - Récupération du Hostname Linux : {HostName}", self.TopExit, True)
                        # Instanciation de l'objet de connexion a la base de données
                        MaBDD = self._MaBDD
                        db = MaBDD.mysqlconnector()
                        # Requête qui va Update TopAnsible à 1
                        MaBDD.UpdateRow(db, f"UPDATE PoolIP SET TopAnsible = '1' WHERE IP = '{IPServer}' AND Deleted = 0")
                        self._MyObjLog.AjouteLog("OK - Update TopAnsible => 1", self.TopExit, True)
                    except (Exception) as err :
                        self._MyObjLog.AjouteLog(f"Erreur lors de l'update : {err}", self.TopExit, True)
                        raise
            except (Exception) as err :
                self._MyObjLog.AjouteLog(f"Erreur de traitement du retour : {err}", self.TopExit, True)
                raise
            return (HostName[0:(len(HostName)-1)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetUserAdmin (self, IDServer): # ? PAS UTILISE

            """This function will return the User Administrator from database

            Args:
                IDServer (int): A Server ID

            Raises:
                mysql.connector.errors.Error: Request error

            Returns:
                str: Return the Administrator User
            """

            try :
                # Instanciation de l'objet de connexion a la base de données
                MaBDD = self._MaBDD
                db = MaBDD.mysqlconnector()
                # Requête qui va récupérer l'utilisateur admin d'un Serveur grâce a l'ID
                myresult = MaBDD.SelectRow(db, f"SELECT UserAdmin FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
                # Vérification que le retour de la requête n'est pas vide
                if myresult:
                    self._MyObjLog.AjouteLog(f"OK - Récupération de l'utilisateur Admin : {myresult}", self.TopExit, True)
                    return (myresult)
                else :
                    self._MyObjLog.AjouteLog("La requête n'a pas ramener de données", self.TopExit, True)
                    raise mysql.connector.errors.Error("La requête n'a pas ramener de données")
            except (mysql.connector.errors.Error) as err:
                self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
                raise

    def GetPassAdmin (self, IDServer): # ? PAS UTILISE

        """This function will return the Password Administrator

        Args:
            IDServer (int): A Server ID

        Raises:
            mysql.connector.errors.Error: Request error

        Returns:
            str: Return the Administrator Password
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le password admin d'un Serveur grâce a l'ID
            myresult = MaBDD.SelectRow(db, f"SELECT PassAdmin FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'utilisateur Admin : {myresult}", self.TopExit, True)
                return (myresult)
            else :
                self._MyObjLog.AjouteLog("La requête n'a pas ramener de données", self.TopExit, True)
                raise mysql.connector.errors.Error("La requête n'a pas ramener de données")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def Get_Name_VLAN(self, IPServer):

        """This function will return the name of VLAN

        Args:
            IPServer (str): PoolIP ID

        Raises:
            Exception: Connection error

        Return:
            str: Name of VLAN
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le Nom du VLAN
            myresult = MaBDD.SelectRow(db, f"SELECT Name FROM VLAN INNER JOIN PoolIP ON VLAN.ID = PoolIP.IDVLAN WHERE IP LIKE '{IPServer}' AND PoolIP.Deleted = 0 AND VLAN.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - VLAN Name : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog(f"Récupération du nom du VLAN pour PoolIP.IP= {IPServer} impossible", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def IsHostnameANDIPAlreadyExist (self, Hostname, IPServer):

        """This function will check if IP AND Hostname are already used

        Args:
            Hostname (str): Hostname of Server
            IPServer (str): IP of Server

        Raises:
            mysql.connector.errors.Error: Request error

        Returns:
            Bool: 0 Server doesn't exist, 1 Server exist
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si l'IP et le Hostname existe déjà
            myresult = MaBDD.SelectRow(db, f"SELECT EXISTS (SELECT Servers.ID FROM Servers INNER JOIN IpServer ON Servers.ID = IpServer.IDServer INNER JOIN PoolIP ON IpServer.IDPoolIP = PoolIP.ID WHERE Hostname LIKE '{Hostname}' AND PoolIP.IP LIKE '{IPServer}')")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Hostname et IP déjà utilisé pour le couple : Hostname={Hostname}/IPServer={IPServer}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog(f"Hostname et IP pas utilisé pour le couple : Hostname={Hostname}/IPServer={IPServer}", self.TopExit, True)
                raise mysql.connector.errors.Error(f"Hostname et IP pas utilisé pour le couple : Hostname={Hostname}/IPServer={IPServer}")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def IpAlreadyAffectedToServer (self, IPServer):

        """This function test if the IP is already register in IpServer

        Args:
            IDServer (str): A Server ID
            IDPoolIP (str): A PoolIP ID

        Raises:
            Exception: Connection error

        Return:
            bool: 1 = good | 0 = no match
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si l'IP est déjà affecté a un Serveur
            myresult = MaBDD.SelectRow(db, f"SELECT COUNT(*) FROM IpServer INNER JOIN PoolIP ON PoolIP.ID = IpServer.IDPoolIP WHERE PoolIP.IP LIKE '{IPServer}' AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Vérification de si l'IP est déjà affecté à un Serveur", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la vérification de si l'IP est déjà affecté à un Serveur", self.TopExit, True)
                raise
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"Erreur dans la classe : Class_Tools fonction : IpAlreadyExist - erreur :  {err}", self.TopExit, True)
            raise

    def SameIpButDiffHostname(self, IPServer, Hostname) :
        
        """This function test if the Hostname not Change 

        Args:
            IDServer (str): A Server ID
            IDPoolIP (str): A PoolIP ID

        Raises:
            Exception: Connection error

        Return:
            bool: 1 = good | 0 = no match
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si le Hostname est le même
            myresult = MaBDD.SelectRow(db, f"SELECT COUNT(*) FROM Servers INNER JOIN IpServer ON Servers.ID = IpServer.IDServer INNER JOIN PoolIP ON PoolIP.ID = IpServer.IDPoolIP WHERE PoolIP.IP LIKE '{IPServer}' AND Hostname NOT LIKE '{Hostname}' AND Servers.Deleted = 0 AND PoolIP.Deleted = 0 AND IpServer.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Vérification de si le Hostname existe déjà", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la vérification de si le Hostname existe déjà", self.TopExit, True)
                raise
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"Erreur dans la classe : Class_Tools fonction : IpAlreadyExist - erreur :  {err}", self.TopExit, True)
            raise

    def Cartouchetop(self):
        try :
            cartouche = "================================================================================================================================================================================================================================="
            cartouche = f"{cartouche} \n\nDébut de l'éxecution du Cron de découverte d'IP, le {datetime.now()}"
            cartouche = f"{cartouche} \n\n================================================================================================================================================================================================================================="
            return(cartouche)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def Cartouchebottom(self):

        try :
            cartouche = "================================================================================================================================================================================================================================="
            cartouche = f"{cartouche} \n\nFin de l'éxecution du Cron {datetime.now()}"
            cartouche = f"{cartouche} \n\n================================================================================================================================================================================================================================="
            return(cartouche)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise