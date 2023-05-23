
#?#########################################################################
#? Importation des biblioth�ques
#?#########################################################################

import mysql.connector
import winrm
import paramiko
import inspect
import sys
import Class_Colors

#?#########################################################################
#? Importation des classes
#?#########################################################################

from Class_Security import Class_Security
from Class_OS import Class_OS

class Class_Hypervisor(Exception):

    """A class which contains all the methods on the hypervisors:
    
    - Add New Hypervisor
    - Get Hypervisor ID Windows Server
    - Get Hypervisor ID Linux Server
    - Hypervisor Exists
    - Remove Hypervisor
    """


    def __init__(self, ObjLog, MonWinRM, MaBDD):
        self._MyObjLog = ObjLog
        self._MonWinRM = MonWinRM
        self._MaBDD = MaBDD
        self._hypervisor = ""
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False

    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonWinRM(self):
        return self._MonWinRM

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

    def GetHypervisorWindows(self, IPServer):
        
        """This function will get the Hypervisor for Windows

        Args:
            IPServer (Str): A Server IP

        Raises:
            Exception: Connection error
            
        Return:
            Str: Hypervisor name
        """
        
        try : 
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant d'obtenir l'Hyperviseur Windows
            self._MonWinRM.Run_WinRM_PS_Session("gcim Win32_ComputerSystem | fl Manufacturer")
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog("OK - Récupération de l'Hyperviseur", self.TopExit, True)
                CleanedHypervisor = self._MonWinRM.std_out
                if (('QEMU' in CleanedHypervisor) == True ):
                    return ('proxmox')
                elif (('VMware' in CleanedHypervisor) == True):
                    return ('vmware')
                else :
                    return('unknown')
            else:
                self._MyObjLog.AjouteLog("NOT OK - Echec de la récupération de l'Hyperviseur", self.TopExit, True)
                raise Exception("NOT OK - Echec de la récupération de l'Hyperviseur")
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetHypervisorLinux(self, IPServer, UserAnsible, PassAnsible, IDOS):
        
        """This function will get the Hypervisor for Linux

        Args:
            IPServer (Str): A Server IP

        Raises:
            Exception: Connection error
            
        Return:
            Str: Hypervisor name
        """
        
        try :
            # Instanciation de l'objet MonOS
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            OSName = MonOS.GetOSName(IDOS)
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
            # Commande permettant d'obtenir l'Hyperviseur Linux
            if OSName != "CentOS Linux" :
                stdin, stdout, stderr = ssh.exec_command("lspci")
            else :
                stdin, stdout, stderr = ssh.exec_command("lscpu")
            # Nettoyage du stdout
            Hyperviseur = stdout.readlines()
            Hyperviseur = " ".join(Hyperviseur)
            self._MyObjLog.AjouteLog("OK - Récupération de l'Hyperviseur", self.TopExit, True)
            # Renvoie le bon Hyperviseur
            if (('QEMU' in Hyperviseur) == True ):
                return ('proxmox')
            elif (('KVM'in Hyperviseur) == True ) :
                return ('proxmox')
            elif (('PVE' in Hyperviseur) == True):
                return ('vmware')
            else :
                return('unknown')
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetHypervisorIDForWindowsServer (self, IPServer):

        """This function get the Hypervisor ID of Windows Server

        Args:
            IPServer (str): A Server IP

        Raises:
            mysql.connector.errors.Error: Mysql Connection error
            mysql.connector.errors.Error: Request Error

        Returns:
            int: Return the ID of Windows Server Hypervisor 
        """
        try :
            # Récuperation de l'Hyperviseur
            Hyperviseur = self.GetHypervisorWindows(IPServer)
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête permettant de récupérer les ID des Hyperviseurs
            myresult = MaBDD.SelectRow(db, f"SELECT ID FROM Hypervisor WHERE Name = '{Hyperviseur}' AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID de l'hyperviseur : {myresult [0][0]} a l'IP", self.TopExit, True)
                return (myresult[0][0])
            else :
                self._MyObjLog.AjouteLog(f"Echec de la récupération de l'ID de l'hyperviseur : {myresult [0][0]} a l'IP", self.TopExit, True)
                raise mysql.connector.errors.Error(f"Echec de la récupération de l'ID de l'hyperviseur : {myresult [0][0]} a l'IP")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetHypervisorIDForLinuxServer (self, IPServer, UserAnsible, PassAnsible, IDOS):

        """This function get the Hypervisor ID of Linux Server 

        Args:
            IPServer (str): A Server IP
            UserAnsible (str): User Ansible
            PassAnsible (str): Password Ansible

        Raises:
            Exception: Connection error | Execution error
            mysql.connector.errors.Error: Mysql Connection error

        Returns:
            int: Return the ID of Windows Server Hypervisor 
        """
        
        try :
            # Récuperation de l'Hyperviseur
            Hyperviseur = self.GetHypervisorLinux(IPServer, UserAnsible, PassAnsible, IDOS)
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête permettant de récupérer les ID des Hyperviseurs
            myresult = MaBDD.SelectRow(db, f"SELECT ID FROM Hypervisor WHERE Name = '{Hyperviseur}' AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID de l'hyperviseur : {myresult [0][0]} a l'IP", self.TopExit, True)
                return (myresult[0][0])
            else :
                self._MyObjLog.AjouteLog(f"Echec de la récupération de l'ID de l'hyperviseur : {myresult [0][0]} a l'IP", self.TopExit, True)
                raise mysql.connector.errors.Error(f"Echec de la récupération de l'ID de l'hyperviseur : {myresult [0][0]} a l'IP")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def AddNewHypervisor (self, HypervisorName):

        """This function add a new hypervisor from the DataBase

        Args:
            HypervisorName (str): The Name of Hypervisor

        Raises:
            mysql.connector.errors.Error: Error mysql

        Returns:
            Bool: 0 it's good, 1 An error has occured
        """
        
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête permettant d'insérer l'Hyperviseur dans la table Hypervisor
            MaBDD.InsertRow(db, f"INSERT INTO Hypervisor (Name) VALUE ('{HypervisorName}')")
            self._MyObjLog.AjouteLog(f"OK - Insertion de l'hyperviseur : {HypervisorName} dans la base", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def HypervisorExists(self, HypervisorName):

        """This function will verify if the hypervisor exist in DataBase

        Args:
            HypervisorName (str): The Name of Hypervisor

        Raises:
            mysql.connector.errors.Error: Mysql error

        Returns:
            int: 1 hypervisor exist, 0 hypervisor doesn't exist
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête permettant de vérifier si l'hyperviseur existe déjà
            # Renvoi 0 ou 1 si 0 = pas de lignes, si 1 = une ligne
            myresult = MaBDD.SelectRow(db, f'SELECT EXISTS(SELECT * FROM Hypervisor WHERE NAME = "{HypervisorName}" AND Deleted = 0) as RESULT')
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog("OK - Vérification de l'existance de l'Hyperviseur", self.TopExit, True)
                return (myresult[0][0])
            else :
                self._MyObjLog.AjouteLog(f"Echec de la vérification de l'existance de l'Hyperviseur", self.TopExit, True)
                raise mysql.connector.errors.Error(f"Echec de la vérification de l'existance de l'Hyperviseur")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def RemoveHypervisor (self, HypervisorName):

        """This function remove a hypervisor from the DataBase

        Args:
            HypervisorName (str): The Name of Hypervisor

        Raises:
            mysql.connector.errors.Error: Error mysql

        Returns:
            Bool: 0 it's good, 1 An error has occured
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête permettant de supprimer un hyperviseur en mettant le Deleted a 1
            MaBDD.UpdateRow(db, f"UPDATE Hypervisor SET Deleted = '1' WHERE Name LIKE '{HypervisorName}' AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update de la table Hyperviseur, Deleted => 1", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise