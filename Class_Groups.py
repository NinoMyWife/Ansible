##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
import sys
import inspect
from queue import Empty
from Class_Security import Class_Security
from Class_Servers import Class_Servers
from Class_ServerGroup import Class_ServerGroup

##########################################################################
# * Début du script
##########################################################################

class Class_Groups(Exception):
    
    def __init__(self, ObjLog, MonServer, MaBDD):
        self._MyObjLog = ObjLog
        self._MonServer = MonServer
        self._MaBDD = MaBDD
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False
        
    # ? getter method
    def get_MyObjLog(self):
        return self._MyObjLog
    def get_MonServer(self):
        return self._MonServer
    
    # ? setter method
    def set_MyObjLog(self, value):
        if (type(value) == type(self._MonWinRM)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MyObjLog = value
        else :
            raise "Property Error"
    def set_MonServer(self, value):
        if (type(value) == type(self._MonServer)):
            self._MyObjLog.AjouteLog("OK - La variable d'entrée est du bon type pour le setter", self.TopExit, True)
            self._MonServer = value
        else :
            raise "Property Error"
    
    def GetGroupIDWithIDServer(self, IDServer):

        """This function will get the GroupID with the ServerID

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
        
        Return:
            Int: Group ID
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Execution de la requête qui va récupérer Le GroupID grâce a l'ID du serveur
            myresult = MaBDD.SelectRow(db, f"SELECT Groups.ID FROM Groups INNER JOIN OS ON OS.Type = Groups.GroupName INNER JOIN Servers ON Servers.IDOS = OS.ID WHERE Servers.ID = {IDServer} AND Groups.Deleted = 0 AND OS.Deleted = 0 AND Servers.Deleted = 0")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog(f"OK - Récupération de l'ID du serveur accessible : {myresult[0][0]}", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération de l'ID du serveur accessible a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de l'ID du serveur accessible a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetGroupList(self):
        
        """This function will get all info of table Groups

        Args:
            IDServer (Int): A Server ID

        Raises:
            Exception: Connection error
        
        Return:
            List : Content of table Groups
            List : Name of column
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Execution de la requête qui va récupérer contenu de la table Groups
            myresult = MaBDD.SelectRow(db, f"SELECT * FROM Groups", True)
            return(myresult)

        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)

    def AffectGroup(self, ID):
        
        """This function affect a group to server in Servergroups

        Args:
            ID (Int): A Server ID

        Raises:
            Exception: Connection error
        """
        try : 
            # Instanciation de l'objet MonServerGroup
            MonServerGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            IDServerAlreadyExistInServerGroup = MonServerGroup.IDServerAlreadyExistInServerGroup(ID)
            # Récupération des informations des groupes
            GroupList = self.GetGroupList()
            # L'ID Serveur n'est pas déjà présent dans la table ServerGroup donc on insère
            if IDServerAlreadyExistInServerGroup == 0:
                for Group in GroupList[0] :
                    GroupID = Group[0]  # ID_Group
                    GroupName = Group[1]
                    RegExProperty= Group[2]   # regex_expression_GROUPS
                    Regex = Group[3]
                    # Si le regex est présent dans le type du serveur on insère
                    if Regex in self._MonServer.get_Type() :
                        MonServerGroup.InsertServerGroup(ID, GroupID)
                        self._MyObjLog.AjouteLog(f"NOTICE -  GroupName : {GroupName}, GroupID : {GroupID}, ID : {ID}\n", self.TopExit, True)
                    # Si le regex est présent dans le VLAN du serveur on insère
                    if Regex in self._MonServer.get_Name_VLAN() :
                        MonServerGroup.InsertServerGroup(ID, GroupID)
                        self._MyObjLog.AjouteLog(f"NOTICE -  GroupName : {GroupName}, GroupID : {GroupID}, ID : {ID}\n", self.TopExit, True)
            # L'ID Serveur est déjà présent dans la table ServerGroup donc on supprime tout les groupes qui sont en liason avec ce serveur pour tout re-insérer
            else :
                MonServerGroup.DeleteAllGroupForServerInServerGroup(ID)
                for Group in GroupList[0] :
                    GroupID = Group[0]  # ID_Group
                    GroupName = Group[1]
                    RegExProperty= Group[2]   # regex_expression_GROUPS
                    Regex = Group[3]   # regex_expression_GROUPS
                    # Si le regex est présent dans le type du serveur on insère
                    if Regex in self._MonServer.get_Type() :
                        MonServerGroup.InsertServerGroup(ID, GroupID)
                        self._MyObjLog.AjouteLog(f"NOTICE -  GroupName : {GroupName}, GroupID : {GroupID}, ID : {ID}\n", self.TopExit, True)
                    # Si le regex est présent dans le VLAN du serveur on insère
                    if Regex in self._MonServer.get_Name_VLAN() :
                        MonServerGroup.InsertServerGroup(ID, GroupID)
                        self._MyObjLog.AjouteLog(f"NOTICE -  GroupName : {GroupName}, GroupID : {GroupID}, ID : {ID}\n", self.TopExit, True)
        except Exception as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise