##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
import sys
from Class_Security import Class_Security

##########################################################################
# * Début du script
##########################################################################

class Class_ServerApps(Exception):
    
    def __init__(self, ObjLog, MaBDD):
        self._MyObjLog = ObjLog
        self._MaBDD = MaBDD
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        
    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    
    # ? setter method
    def set_MyObjLog(self, value):
        if (type(value) == type(self._MonWinRM)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MyObjLog = value
        else :
            raise "Property Error"

    def InsertServerApp(self, IDServer, IDApplication):

        """This function will insert the Server App

        Args:
            IDServer (Int): A Server ID
            IDApplication (Int): A Application ID

        Raises:
            Exception: Connection error
        """
        
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Insérer dans ServerApp
            MaBDD.InsertRow(db, f"INSERT INTO ServerApps (IDServer, IDApplication, Deleted) VALUES ({IDServer}, {IDApplication}, 0)")
            self._MyObjLog.AjouteLog("OK - L'insertion dans ServerApps c'est bien passée", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def UpdateServerApp(self, IDServer, IDApplication): # ? PAS UTILISE
        
        """This function will update the Server App

        Args:
            IDServer (Int): A Server ID
            IDApplication (Int): A Application ID

        Raises:
            Exception: Connection error
        """
        
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 0
            MaBDD.UpdateRow(db, f"Update ServerApps SET Deleted = 0 WHERE IdServer = {IDServer} AND IDApplication = {IDApplication} AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update de la table ServerApps", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteServerApp(self, IDServer):

        """This function will delete the Server App

        Args:
            IDServer (Int): A Server ID
            IDApplication (Int): A Application ID

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 1
            MaBDD.UpdateRow(db, f"UPDATE ServerApps SET Deleted = 1 WHERE IdServer = {IDServer}")
            self._MyObjLog.AjouteLog("OK - Delete de la table ServerApps", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteAllAppForServerInServerApp(self, IDServer):

        """This function will delete all the Server App

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Delete la ligne correspondant a l'ID du Serveur
            MaBDD.DeleteRow(db, f"DELETE FROM `ServerApps` WHERE IdServer = {IDServer} AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Delete de la table ServerApps", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def IDServerAlreadyExistInServerApps(self, IDServer):
        
        """This function will check if the server id already exist in ServerApps

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
            
        Return:
            Int : The number of occurrences
        """
        
        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si l'ID Serveur est déjà présent dans ServerApps
            myresult = MaBDD.SelectRow(db, f"SELECT EXISTS(SELECT IdServer FROM ServerApps WHERE IdServer = {IDServer} AND Deleted = 0)")
            if myresult[0][0] == 0:
                self._MyObjLog.AjouteLog(f"OK - L'id n'est pas déjà présent dans la base : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            elif myresult[0][0] == 1:
                self._MyObjLog.AjouteLog(f"OK - L'id est déjà présent dans la base : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération de l'IP du serveur accessible a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de l'IP du serveur accessible a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
