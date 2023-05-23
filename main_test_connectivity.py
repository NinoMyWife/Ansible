
#?#########################################################################
#? Importattion des bibliothèques
#?#########################################################################

import sys

#?#########################################################################
#? Importation des classes
#?########################################################################

from Class_WinRM import Class_WinRM
from Class_Ansible_Security import Class_Ansible_Security
from Class_Logs import Class_Logs
from Class_Servers import Class_Servers
from Class_Connectivity import Class_Connectivity
from Class_Mail import Class_Mail

#?###################################################################################################
#? Ce main a pour but de vérifier la connectivité des serveurs avec l'utilisateur ansible
#?###################################################################################################

try: 
    # Instanciation des Objets MyObjLog, MonWinRM, MonAnsibleSecurity, MonSeveur, MaConnectivity, MonMail
    MyObjLog = Class_Logs()
    MyObjLog.directory= "/root/ScriptsInventaireDynamique/Maintest/"
    MyObjLog.filename= "LogConnectivityAnsible.txt"
    MyObjLog.writemode = 'w'
    MyObjLog.CreateLogFile("Début du Cron de test de connectivité d'Ansible : \n\n")
    MonWinRM = Class_WinRM(MyObjLog)
    MonAnsibleSecurity = Class_Ansible_Security(MyObjLog, MonWinRM)
    MonSeveur = Class_Servers(MyObjLog, MonWinRM)
    MaConnectivity = Class_Connectivity(MyObjLog, MonWinRM)
    MonMail = Class_Mail (MyObjLog)

    ListIp = MonSeveur.GetServerListWithTopAnsible() # la liste des ip des servers avec le top ansible a 1
    # ListIp = ["185.190.91.32"] 
    try: 
        # Boucle qui va passer sur toutes les IPs
        for IP in ListIp :
            try:
                IP = IP[0]
                # Récupération du login et du mot de passe lié a cette IP
                PassAnsibleUserAnsibleIDServerByIPServer = MonSeveur.GetPassAnsibleUserAnsibleIDServerByIPServer(IP)
                UserAnsible = PassAnsibleUserAnsibleIDServerByIPServer[1]
                PassAnsible = PassAnsibleUserAnsibleIDServerByIPServer[2]
                # Déchiffrement du password
                DecryptedPassAnsible = MonAnsibleSecurity.Decrypt_Password(PassAnsible, MonAnsibleSecurity.GetSalt())
                # On affecte les login a l'objet de connexion Windows (WinRM)
                MonWinRM.set_useransible(UserAnsible)
                MonWinRM.set_passansible(DecryptedPassAnsible)
                # Récupération de l'ID du Serveur
                IDServer = MonSeveur.GetServeurID(IP)
                # Récupération du type du Serveur
                Type = MonSeveur.GetServerTypeWithIDServer(IDServer)
                # Test de connectivité
                if (MaConnectivity.TestConnexionAnsible(IP, UserAnsible, PassAnsible, Type) == True) :
                    MyObjLog.AjouteLog(f"OK - La connectivité est valide pour l'IP : {IP}", MyObjLog.TopExit, True)
                else :
                    MyObjLog.AjouteLog(f"NOT OK - La connectivité n'est pas valide pour l'IP : {IP}", MyObjLog.TopExit, True)
            except Exception as err :
                MyObjLog.AjouteLog("\nNOT OK - Erreur dans le changement de mot de passe", MyObjLog.TopExit, False)
                raise
        # Envoi du rapport par mail
        LogReport = MonAnsibleSecurity.GetErrorReport(f"{MyObjLog.directory}{MyObjLog.filename}")
        MonMail.SendReportMail(LogReport[0], LogReport[1])
    except Exception as err :
        MyObjLog.AjouteLog("\nNOT OK - Erreur lors du parcours des IP", MyObjLog.TopExit, False)
        raise
except Exception as err :
    MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}", MyObjLog.TopExit, True)
    raise