##########################################################################
# Importattion des bibliothèques
##########################################################################

import os
import mysql.connector

##########################################################################
# Importation des classes
##########################################################################

from Security import Class_Security
import ping
import SetPingable

##########################################################################
# Début du script
##########################################################################

try : 
    connection_params = {
        'host': Class_Security().HostBDD,
        'user': Class_Security().UserBDD,
        'password': Class_Security().PasswdBDD,
        'database': Class_Security().NameBDD,
        }
    mysqlrequest=("SELECT IP FROM PoolIP")
    with mysql.connector.connect(**connection_params) as db :
                with db.cursor() as c:
                    c.execute(mysqlrequest)
                    myresult = c.fetchall()
except (RuntimeError, TypeError, NameError) as e :
    print (e)

for IP in myresult :
    Pingable = ping(IP)
    SetPingable(Pingable, IP)