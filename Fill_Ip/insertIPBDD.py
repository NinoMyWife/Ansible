##########################################################################
# Importation des classes
##########################################################################

from Security import Class_Security

##########################################################################
# Importation des bibliothèques
##########################################################################

import mysql.connector
import ipaddress

##########################################################################
# Début du script
##########################################################################

poolip =['192.168.200.0/24','10.10.0.0/24','10.10.1.0/24','10.10.10.0/24','10.10.50.0/24','10.10.60.0/24','10.10.70.0/24','10.10.80.0/24','10.20.0.0/24','10.21.0.0/24','10.22.0.0/24','10.23.0.0/24','185.190.91.0/24','93.93.184.0/25','93.93.185.224/28']

try :
    for plageip in poolip:
        for ip in ipaddress.IPv4Network(plageip):
            ip = str(ip)
            ip = [ip]
            connection_params = {
                'host': Class_Security().HostBDD,
                'user': Class_Security().UserBDD,
                'password': Class_Security().PasswdBDD,
                'database': Class_Security().NameBDD,
                }
            mysqlrequest=("INSERT into PoolIP (IP) VALUES ('%s') " % ip)
            with mysql.connector.connect(**connection_params) as db :
                        with db.cursor() as c:
                            c.execute(mysqlrequest)
                            db.commit()
except (RuntimeError, TypeError, NameError) as e :
    print (e)