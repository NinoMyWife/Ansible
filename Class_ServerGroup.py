##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
import sys
from Class_Security import Class_Security

##########################################################################
# * Début du script
##########################################################################

class Class_ServerGroup(Exception):
    
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

    def InsertServerGroup(self, IDServer, GroupIDServer):
    
        """This function will insert a servergroup in Servergroups

        Args:
            IDServer (Int): A Server ID
            GroupIDServer (Int): A goup ID

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Insérer dans ServerGroup
            MaBDD.InsertRow(db, f"INSERT INTO ServerGroup (IdServer, IdGroup) VALUE ({IDServer}, {GroupIDServer})")
            self._MyObjLog.AjouteLog("OK - Insertion dans la base ServerGroup réussie", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def UpdateServerGroup(self, IDServer, GroupIDServer):

        """This function will update a servergroup in Servergroups

        Args:
            IDServer (Int): A Server ID
            GroupIDServer (Int): A goup ID

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update IdGroup
            MaBDD.UpdateRow(db, f"Update ServerGroup SET IdGroup = {GroupIDServer} WHERE IdServer = {IDServer} and Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Update de la base ServerGroup réussie", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteServerGroup(self, IDServer):

        """This function will delete a servergroup in Servergroups

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va Update Deleted a 1
            MaBDD.UpdateRow(db, f"UPDATE ServerGroup SET Deleted = '1' WHERE IdServer = {IDServer}")
            self._MyObjLog.AjouteLog("OK - Delete de la table ServerGroup", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def IDServerAlreadyExistInServerGroup(self, IDServer):
        
        """This function will check if the ServerIS already Exist in ServerGroup
        
        Args:
            IDServer (Int): A Server ID
            
        Raises:
            Exception: Connection error
        
        Return:
            Int: The number of occurrences
        """        

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Requête qui va vérifier si l'IDServer est déjà présent dans ServerGroup
            myresult = MaBDD.SelectRow(db, f"SELECT EXISTS(SELECT IdServer FROM ServerGroup WHERE IdServer = {IDServer} AND Deleted = 0)")
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

    def DeleteAllGroupForServerInServerGroup(self, IDServer):

        """This function will delete all the ServerGroup

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
            MaBDD.DeleteRow(db, f"DELETE FROM `ServerGroup` WHERE IdServer = {IDServer} AND Deleted = 0")
            self._MyObjLog.AjouteLog("OK - Delete de la table ServerGroup", self.TopExit, True)
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
