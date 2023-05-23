##########################################################################
# Importation des classes
##########################################################################

from Security import Class_Security

##########################################################################
# Importation des bibliothèques
##########################################################################

import sys
import os
import mysql.connector

##########################################################################
# Début du script
##########################################################################

def SetPingable(Pingable, IP):
    
    """This function will update the BDD if IP is pingable

    Args:
        Pingable (bool) : 0 it's ok, 1 it's not ok
        IP (str): A Server IP

    Raises:
        mysql.connector.errors.Error: Request error
    """
    
    if (Pingable == "0"):
        try:
            connection_params = {
                'host': Class_Security().HostBDD,
                'user': Class_Security().UserBDD,
                'password': Class_Security().PasswdBDD,
                'database': Class_Security().NameBDD,
                }
            mysqlrequest=("UPDATE PoolIP SET Pingable = 1 WHERE IP = '%s'" % IP)
            with mysql.connector.connect(**connection_params) as db :
                        with db.cursor() as c:
                            c.execute(mysqlrequest)
                            db.commit()
        except (RuntimeError, TypeError, NameError) as e :
            print (e)
    else:
        exit()

print(SetPingable.__doc__)
