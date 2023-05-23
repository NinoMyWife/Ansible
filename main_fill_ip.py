
#? #########################################################################
#? Importattion des bibliothèques
#?#########################################################################

import sys

#?#########################################################################
#? Importation des classes
#?#########################################################################

from Class_Logs import Class_Logs
from Class_Security import Class_Security
from Class_Fill_IP import Class_Fill_IP
from Class_Mail import Class_Mail
from Class_Ansible_Security import Class_Ansible_Security
from Class_WinRM import Class_WinRM

#?#########################################################################
#? Début du script
#?#########################################################################

try :
    # Instanciation des Objets MyObjLog, MonWinRM, MonAnsibleSecurity, MonMail, MonFillIP
    MyObjLog = Class_Logs()
    MyObjLog.directory= "/root/ScriptsInventaireDynamique/Maintest/"
    MyObjLog.filename= "LogFillIP.txt"
    MyObjLog.writemode = 'w'
    MyObjLog.CreateLogFile("Debut du Script FillIP")
    MonWinRM = Class_WinRM()
    MonAnsibleSecurity = Class_Ansible_Security(MyObjLog, MonWinRM)
    MonMail = Class_Mail()
    MonFillIP = Class_Fill_IP()
    # Insertion de toutes les tranches IPs dans la table PoolIP
    MonFillIP.InsertPoolIP()
    # Récupération de la liste des IPs
    ListeIP = MonFillIP.SelectAllIpFromPoolIP()

    # Boucle qui va passer sur toutes les IPs
    for IP in ListeIP :
        # On teste si l'IP est pingable ou non et on Update la colonne Pingable dans la table PoolIP
        Pingable = MonFillIP.ping(IP)
        MonFillIP.SetPingable(Pingable, IP)

    # Envoi du rapport par mail 
    LogReport = MonAnsibleSecurity.GetErrorReport(f"{MyObjLog.directory}{MyObjLog.filename}")
    MonMail.SendReportMail(LogReport[0], LogReport[1])

except Exception as err :
    MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , False, True)
    raise