##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
import sys
from Class_Security import Class_Security
from Class_WinRM import Class_WinRM

##########################################################################
# * Début du script
##########################################################################

class Class_PoolIP(Exception):
    
    def __init__(self, MyObjLog, MaBDD):
        self._MyObjLog = MyObjLog
        self._MaBDD = MaBDD
        self._useransible = Class_Security().UserAnsible
        self._passansible = Class_Security().PassAnsible
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        
    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
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
    
    
    def GetPoolIPID(self, IPServer):

        """This function will return the PoolIP ID

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error

        Return:
            int: ID of PoolIP
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer l'ID du de l'IP
            myresult = MaBDD.SelectRow(db, f"SELECT ID FROM PoolIP WHERE Ip = '{IPServer}' AND Deleted = 0" )
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'id de PoolIP : {myresult[0][0]}", self.TopExit, True)
                return myresult[0][0]
            else:
                self._MyObjLog.AjouteLog("Récupération de l'ID impossible", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de l'ID impossible")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetPoolIpList(self) :

        """This function will return the PoolIP List

        Args:
            

        Raises:
            Exception: Connection error

        Return:
            List : Ip List
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer la liste des IPs dans PoolIP
            myresult = MaBDD.SelectRow(db, "SELECT IP FROM PoolIP WHERE Deleted = 0")
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

    def GetListIpWithVLAN(self, NumVLAN) :

        """This function will return the PoolIP List

        Args:
            

        Raises:
            Exception: Connection error

        Return:
            List : Ip List
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va récupérer la liste des IPs dans PoolIP qui correspondent au bon VLAN
            myresult = MaBDD.SelectRow(db, f"SELECT IP FROM PoolIP WHERE IDVLAN = {NumVLAN} AND Deleted = 0")
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

    def UpdatePingable(self, IPServer):

        """This function will update the field Pingable in PoolIP

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Pingable a 1
            MaBDD.UpdateRow(db, f"UPDATE PoolIP SET Pingable = '1' WHERE IP = '{IPServer}' AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update Pingable => 1", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def UpdateTopAnsible(self, IPServer):

        """This function will update the field TopAnsible in PoolIP

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update TopAnsible a 1
            MaBDD.UpdateRow(db, f"UPDATE PoolIP SET TopAnsible = '1' WHERE IP = '{IPServer}' AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update TopAnsible => 1", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def UpdateIsUsed(self, IP):
        
        """This function will update the field IsUsed in PoolIP

        Args:
            IPServer (str): A Server IP

        Raises:
            Exception: Connection error
        """
        
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update IsUsed a 1
            MaBDD.UpdateRow(db, f"UPDATE PoolIP SET IsUsed = 1 WHERE IP = '{IP}' AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update de POOLIP => IsUsed = 1", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
