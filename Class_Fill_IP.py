##########################################################################
# * Importation des bibliotheques
##########################################################################

import mysql.connector
import ipaddress
import os
import sys
import inspect
from Class_Security import Class_Security

##########################################################################
# * Début du script
##########################################################################

class Class_Fill_IP(Exception):

    def __init__(self, MaBDD):
        self._MaBDD = MaBDD
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False

    def SetPingable(self, Pingable, IP):
        
        """This function will update the BDD if IP is pingable

        Args:
            Pingable (bool) : 0 it's ok, 1 it's not ok
            IP (str): A Server IP

        Raises:
            mysql.connector.errors.Error: Request error
        """
        
        if (Pingable == 1):
            try:
                # Instanciation de l'objet de connexion a la base de données
                MaBDD = self._MaBDD
                db = MaBDD.mysqlconnector()
                # Execution de la requête qui va mettre a jour toutes les IP Pingable
                MaBDD.UpdateRow(db, f"UPDATE PoolIP SET Pingable = 1 WHERE IP = '{IP}' and Deleted = 0")
            except (RuntimeError, TypeError, NameError) as e :
                print (e)
        else:
            exit()

    def ping(self, host):
        
        """This function will test if IP is pingable

        Args:
            host (str): A Server IP

        Raises:
            Error : Ping error

        Returns:
            Bool : 1 it's ok, 0 it's not ok
        """
        
        try:
            # Commande permettant de ping l'IP d'un serveur
            response = os.system("ping -c 1 " + host)
            print(response)
        except Exception as e :
            raise (e)

        if response == 0:
            return(1)
        else:
            return(0)

    def InsertPoolIP(self) : 

        """This function will Insert IP in PoolIP

        Raises:
            mysql.connector.errors.Error: Request error
        """

        try :
            # Liste des tranches IP du parc informatique
            poolip =['192.168.200.0/24','10.10.0.0/24','10.10.1.0/24','10.10.10.0/24','10.10.50.0/24','10.10.60.0/24','10.10.70.0/24','10.10.80.0/24','10.20.0.0/24','10.21.0.0/24','10.22.0.0/24','10.23.0.0/24','185.190.91.0/24','93.93.184.0/25','93.93.185.224/28', '51.91.103.68/32', '10.25.0.0/24']
            # Insertion de toute les IP dans la table PoolIP
            for plageip in poolip:
                for ip in ipaddress.IPv4Network(plageip):
                    ip = str(ip)
                    ip = [ip]
                    # Instanciation de l'objet de connexion a la base de données
                    MaBDD = self._MaBDD
                    db = MaBDD.mysqlconnector()
                    # Execution de la requête qui va insérer toutes les IP dans la table
                    MaBDD.InsertRow(db, f"INSERT into PoolIP (IP) VALUES ('{ip}')")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def SelectAllIpFromPoolIP(self) :

        """This function will select all IP in PoolIP

        Raises:
            mysql.connector.errors.Error: Request error

        Returns:
            List : List of Ip from PoolIP
        """

        try :
            # Instanciation de l'objet de connexion a la base de données
            MaBDD = self._MaBDD
            db = MaBDD.mysqlconnector()
            # Execution de la requête qui va récupérer toutes les IP de la table PoolIP
            myresult = MaBDD.SelectRow(db, "SELECT IP FROM PoolIP")
            # Vérification que le retour de la requête n'est pas vide
            if myresult:
                self._MyObjLog.AjouteLog("OK - Obtention de la liste des IP de PoolIP", self.TopExit, True)
                return(myresult[0][0])
            else:
                self._MyObjLog.AjouteLog("Récupération de la liste des IP de PoolIp a échoué", self.TopExit, True)
                raise mysql.connector.errors.Error("Récupération de la liste des IP de PoolIp a échoué")
        except (mysql.connector.errors.Error) as err:
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise
