##########################################################################
# Importation des bibliothèques
##########################################################################

import sys
import mysql.connector
import paramiko

##########################################################################
# Importation des classes
##########################################################################

from Class_Tools import Class_Tools
from Class_Security import Class_Security

class Class_OS(Exception):

    """A class which contains all the methods on the OS:
    
    - Add New OS
    - OS Exists
    - Remove OS
    - Get OS ID Linux
    - Get OS ID Windows
    """

    def __init__(self, ObjLog, MonWinRM, MaBDD):
        self._MyObjLog = ObjLog
        self._MonWinRM = MonWinRM
        self._MaBDD = MaBDD
        self._OS = ""
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        
    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonWinRM(self):
        return self._MonWinRM
    def get_OS(self):
        return self._OS
    
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
    def set_OS(self, value):
        if (type(value) == str):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._OS = value
        else :
            raise "Property Error"

    def AddNewOS (self, Name, Type, Version):

        """This function add a new OS from the DataBase

        Args:
            Name (str): Name of the OS
            Type (str): Type of the OS
            Version (str): Version if the OS

        Raises:
            mysql.connector.errors.Error: Error mysql

        Returns:
            Bool: 0 it's good, 1 An error has occured
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Inserer un nouvel OS
            MaBDD.InsertRow(db, f"INSERT INTO OS (Name, Type, Version) VALUE ('{Name}', '{Type}', '{Version}')")
            self._MyObjLog.AjouteLog("OK - Ajout d'un nouvel OS en base", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def OsExist(self, Name): # ? PAS UTILISE

        """This function will verify if the OS exist in DataBase

        Args:
            Name (str): Name of the OS

        Raises:
            mysql.connector.errors.Error: Mysql error

        Returns:
            int: 1 OS exist, 0 OS doesn't exist
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si l'OS existe
            # Renvoi 0 ou 1 si 0 = pas de lignes, si 1 = une ligne
            myresult = MaBDD.SelectRow(db, f"SELECT EXISTS(SELECT * FROM OS WHERE NAME = '{Name}' AND Deleted = 0) as RESULT")
            self._MyObjLog.AjouteLog("OK - L'OS existe", self.TopExit, True)
            return (myresult)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def RemoveOS (self, Name): # ? PAS UTILISE

        """This function remove a OS from the DataBase

        Args:
            Name (str): Name of the OS

        Raises:
            mysql.connector.errors.Error: Error mysql

        Returns:
            Bool: 0 it's good, 1 An error has occured
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 1
            MaBDD.UpdateRow(db, f"UPDATE OS SET Deleted = '1' WHERE Name = '{Name}' AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Suppression de l'OS dans la base", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetOSIDLinux (self, IPServer, UserAnsible, PassAnsible):
        
        """This function get the OS ID of Linux Server

        Args:
            IPServer (str): A Server IP
            UserAnsible (str): User Ansible
            PassAnsible (str): Password Ansible

        Raises:
            Exception: Connection error | Execution error
            mysql.connector.errors.Error: Mysql Connection error

        Returns:
            int: Return the ID of Linux Server OS 
        """
        try:
            try :
                # Connexion a Paramiko
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
                # Commande permettant de récupérer l'OS
                stdin, stdout, stderr = ssh.exec_command("cat /etc/os-release | grep \"^NAME=\" | grep -o '\"[^\"]\+\"' | sed 's/\"//g'")
                # Nettoyage du stdout
                Name = stdout.readlines()
                Name = Name[0]
                CleanedName = Name[0:(len(Name)-1)]
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'OS Linux : {CleanedName}", self.TopExit, True)
            except (Exception) as err :
                self._MyObjLog.AjouteLog(f"NOT OK - Erreur lors de la récuperation de l'OS Linux | source: Method GetOSIDLinux1 - erreur : {err}", self.TopExit, True)
                raise
            try :
                # Connexion a Paramiko
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(IPServer, 22, UserAnsible, PassAnsible)
                # Commande permettant de récupérer la version de l'OS
                stdin, stdout, stderr = ssh.exec_command("cat /etc/os-release | grep \"VERSION_ID\" | grep -o '\"[^\"]\+\"' | sed 's/\"//g'")
                # Nettoyage du stdout
                Version = stdout.readlines()
                Version = Version[0]
                CleanedVersion = Version[0:(len(Version)-1)]
                self._MyObjLog.AjouteLog(f"OK - Récupération de la version de l'OS Linux : {CleanedVersion}", self.TopExit, True)
            except (Exception) as err :
                self._MyObjLog.AjouteLog(f"NOT OK - Erreur lors de la récuperation de la version de l'OS Linux | source: Method GetOSIDLinux2 - erreur : {err}", self.TopExit, True)
                raise
            try :
                # Instanciation de l'objet de connexion a la base de données
                MaBDD = self._MaBDD
                db = MaBDD.mysqlconnector()
                # Requête qui va vérifier si l'OS est déjà présente dans la base
                myresult = MaBDD.SelectRow(db, f"SELECT EXISTS(SELECT id FROM OS WHERE NAME = '{CleanedName}' AND VERSION = '{CleanedVersion}' AND Deleted = 0)")
                self._MyObjLog.AjouteLog("OK - L'IDOS Linux existait pas", self.TopExit, True)
            except (Exception) as err :
                self._MyObjLog.AjouteLog(f"NOT OK - L'IDOS Linux existait déjà | source: Method GetOSIDLinux3 - erreur : {err}", self.TopExit, True)
            # Si l'OS est déjà présente alors on récupère l'ID de L'OS
            if (myresult[0][0] == 1):
                try:
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va récupérer l'ID de l'OS
                    myresult = MaBDD.SelectRow(db, f"SELECT id FROM OS WHERE NAME = '{CleanedName}' AND VERSION = '{CleanedVersion}' AND Deleted = 0")
                    # Vérification que le retour de la requête n'est pas vide
                    if myresult:
                        self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        return (myresult[0][0])
                    else :
                        self._MyObjLog.AjouteLog(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        raise mysql.connector.errors.Error(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}")
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur lors de la récupération de l'ID de l'OS : {err}", self.TopExit, True)
                    raise
            # Si l'OS n'est pas déjà présente alors on insère
            else :
                try :
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va insérer un nouvel OS
                    MaBDD.InsertRow(db, f"INSERT INTO OS (Name, Type, Version, Deleted) Values ('{CleanedName}', 'linux', '{CleanedVersion}', 0)")
                    self._MyObjLog.AjouteLog(f"OK - Insertion d'un nouvel OS : {CleanedName}, ainsi que sa version : {CleanedVersion}", self.TopExit, True)
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur lors de l'insertion d'un nouvel OS et de sa version : {err}", self.TopExit, True)
                    raise
                
                try :
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va récupérer l'ID de l'OS
                    myresult = MaBDD.SelectRow(db, f"SELECT id FROM OS WHERE NAME = '{CleanedName}' AND VERSION = '{CleanedVersion}' AND Deleted = 0")
                    # Vérification que le retour de la requête n'est pas vide
                    if myresult:
                        self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        return (myresult[0][0])
                    else :
                        self._MyObjLog.AjouteLog(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        raise mysql.connector.errors.Error(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}")
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"Erreur lors de la récupération de l'ID de l'OS : {err}", self.TopExit, True)
                    raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetOSIDWindows (self, IPServer):
        
        """This function will get the OSID for Windows

        Args:
            IPServer (Str): A Server IP

        Raises:
            Exception: Connection error
            
        Return:
            Int: OS ID
        """
        
        try :
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de récupérer version de l'OS sur Windows
            self._MonWinRM.Run_WinRM_PS_Session('(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").CurrentBuild')
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                CleanedVersion = self._MonWinRM.std_out
                self._MyObjLog.AjouteLog(f"OK - Récupération de la version de l'OS Windows : {CleanedVersion}", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog("NOT OK - Récupération de la version de l'OS Windows", self.TopExit, True)
                raise Exception("NOT OK - Récupération de la version de l'OS Windows")
            # Commande permettant de récupérer l'OS sur Windows
            self._MonWinRM.Run_WinRM_PS_Session('(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion").ProductName')
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                CleanedName = self._MonWinRM.std_out
                Type = "windows"
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'OS Windows : {CleanedName}", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog("NOT OK - Récupération l'OS Windows", self.TopExit, True)
                raise Exception("NOT OK - Récupération l'OS Windows")
            try :
                # Instanciation de l'objet de connexion a la base de données
                MaBDD = self._MaBDD
                db = MaBDD.mysqlconnector()
                # Requête qui va vérifier si l'OS est déjà présente dans la base
                myresult = MaBDD.SelectRow(db, f"SELECT EXISTS(SELECT id FROM OS WHERE NAME = '{CleanedName}' AND Type = '{Type}' AND VERSION = '{CleanedVersion}' AND Deleted = 0)")
                self._MyObjLog.AjouteLog("OK - L'IDOS Windows existait pas", self.TopExit, True)
            except (Exception) as err :
                self._MyObjLog.AjouteLog(f"NOT OK - L'IDOS Windows existait déjà : {err}", self.TopExit, True)
            # Si l'OS est déjà présente alors on récupère l'ID de L'OS
            if (myresult[0][0] == 1):
                try:
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va récupérer l'ID de l'OS
                    myresult = MaBDD.SelectRow(db, f"SELECT id FROM OS WHERE NAME = '{CleanedName}' AND Type = '{Type}' AND VERSION = '{CleanedVersion}' AND Deleted = 0")
                    # Vérification que le retour de la requête n'est pas vide
                    if myresult:
                        self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        return (myresult[0][0])
                    else :
                        self._MyObjLog.AjouteLog(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        raise mysql.connector.errors.Error(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}")
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"NOT OK - Récupération de l'IDOS : {err}", self.TopExit, True)
                    raise
            # Si l'OS n'est pas déjà présente alors on insère
            else :
                try :
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va insérer un nouvel OS
                    MaBDD.InsertRow(db, f"INSERT INTO OS (Name, Type, Version, Deleted) Values ('{CleanedName}', '{Type}', '{CleanedVersion}', 0)")
                    self._MyObjLog.AjouteLog(f"OK - Insertion d'un nouvel OS : {CleanedName}, ainsi que sa version : {CleanedVersion}", self.TopExit, True)
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"NOT OK - Erreur lors de l'insertion d'un nouvel OS et de sa version : {err}", self.TopExit, True)
                    raise
                try :
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Requête qui va récupérer l'ID de l'OS
                    myresult = MaBDD.SelectRow(db, f"SELECT id FROM OS WHERE NAME = '{CleanedName}' AND VERSION = '{CleanedVersion}' AND Deleted = 0")
                    # Vérification que le retour de la requête n'est pas vide
                    if myresult:
                        self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        return (myresult[0][0])
                    else :
                        self._MyObjLog.AjouteLog(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}", self.TopExit, True)
                        raise mysql.connector.errors.Error(f"Echec de la récupération de l'ID de l'OS : {myresult[0][0]}")
                except (Exception) as err :
                    self._MyObjLog.AjouteLog(f"NOT OK - Erreur lors de la récupération de l'ID de l'OS : {err}", self.TopExit, True)
                    raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetOSInfo(self, IPServer):
        
        """This function will return the OS Version
        
        Args:
            IPServer (Str): IP of the server

        Raises:
            Exception: Connection error

        Return:
            int: Version of the OS
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer la version de l'OS et l'OS
            myresult = MaBDD.SelectRow(db, f"SELECT OS.`Version`, OS.Name FROM OS INNER JOIN Servers ON OS.ID = Servers.IDOS INNER JOIN IpServer ON IpServer.IDServer = Servers.ID INNER JOIN PoolIP ON PoolIP.ID = IpServer.IDPoolIP WHERE PoolIP.IP LIKE '{IPServer}'")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de la version de l'OS et de l'OS : {myresult}", self.TopExit, True)
                return myresult
            else:
                self._MyObjLog.AjouteLog("Récupération de la version de l'OS et de l'OS impossible", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de la version de l'OS et de l'OS impossible")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetOSName(self, IDOS) :

        """This function will return the OS Version
        
        Args:
            IPServer (Str): IP of the server

        Raises:
            Exception: Connection error

        Return:
            int: Version of the OS
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer le nom de l'OS
            myresult = MaBDD.SelectRow(db, f"SELECT Name FROM OS WHERE ID = {IDOS} AND Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de la version de l'OS et de l'OS : {myresult}", self.TopExit, True)
                return myresult[0][0]
            else:
                self._MyObjLog.AjouteLog("Récupération de la version de l'OS et de l'OS impossible", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de la version de l'OS et de l'OS impossible")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
