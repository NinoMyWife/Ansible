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

class Class_IPServer(Exception):
    
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
    
    def AddIpOnIPServer(self, IDPoolIP, IDServer):

        """This function will add a secondary ip to a server

        Args:
            IDPoolIP (str): ID of PoolIp
            IDServer (str): ID of IDServer

        Raises:
            mysql.connector.errors.Error: Request error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va ajouter une IP a un serveur 
            MaBDD.InsertRow(db, f"INSERT INTO IpServer (IDPoolIP, IDServer, Deleted) VALUES ({IDPoolIP}, {IDServer}, 0)")
            self._MyObjLog.AjouteLog("OK - Ajout d'une IP a un Serveur", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteAllIPServerByIDServer(self, IDServer):
        
        """This function remove all IPServer link with IDServer from the DataBase

        Args:
            IDServer (int): ID of the Server

        Raises:
            mysql.connector.errors.Error: Error mysql
        """

        try:
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 1 là où l'id serveur est present dans IPServer
            MaBDD.UpdateRow(db, f"UPDATE IpServer SET Deleted = 1 WHERE IDServer = {IDServer}")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopRaise, True)
            raise
        except Exception as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopRaise, True)
            raise

    def DeleteIPServerByIDPoolIP(self, IDPoolIP):

        """This function will delete a secondary ip from IPServer

        Args:
            IDPoolIP (str): ID of PoolIp

        Raises:
            mysql.connector.errors.Error: Request error
        """

        try:
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 1 là où l'id de PoolIP est present dans IPServer
            MaBDD.UpdateRow(db, f"UPDATE IpServer SET Deleted = 1 WHERE IDPoolIP = {IDPoolIP} and Deleted = 0")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopRaise, True)
            raise
        except Exception as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopRaise, True)
            raise

