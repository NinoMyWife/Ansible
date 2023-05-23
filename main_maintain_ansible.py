
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
from Class_MySQL import Class_MySQL

#?#########################################################################
#? Ce main a pour but d'entretenir les utilisateur ansible des servers
#?#########################################################################

try:
    # Instanciation des Objets MyObjLog, MaBDD, MonWinRM, MonAnsibleSecurity, MonSeveur, MaConnectivity, MonMail
    MyObjLog = Class_Logs()
    MyObjLog.directory= "/root/ScriptsInventaireDynamique/Maintest/"
    MyObjLog.filename= "LogMaintainAnsible.txt"
    MyObjLog.writemode = 'w'
    MyObjLog.CreateLogFile("Début du Cron de maintenance d'Ansible : \n\n")
    MaBDD = Class_MySQL(MyObjLog)
    MonWinRM = Class_WinRM(MyObjLog)
    MonAnsibleSecurity = Class_Ansible_Security(MyObjLog, MonWinRM)
    MonSeveur = Class_Servers(MyObjLog, MonWinRM, MaBDD)
    MaConnectivity = Class_Connectivity(MyObjLog, MonWinRM)
    MonMail = Class_Mail(MyObjLog)

    ListIp = MonSeveur.GetServerListWherePasswordNeedUpdate(1) # la liste des ip des servers a changer le mdp selon la derniere date de mise a jour
    # ListIp = ["192.168.200.29", "185.190.91.32"] 
    try: 
        # Boucle qui va passer sur toutes les IPs
        for IP in ListIp :
            try: 
                IP = IP[0]
                # On récupère le login et le mot de passe ansible pour pouvoir se connecter a la machine
                PassAnsibleUserAnsibleIDServerByIPServer = MonSeveur.GetPassAnsibleUserAnsibleIDServerByIPServer(IP)
                UserAnsible = PassAnsibleUserAnsibleIDServerByIPServer[1]
                PassAnsible = PassAnsibleUserAnsibleIDServerByIPServer[2]
                DecryptedPassAnsible = MonAnsibleSecurity.Decrypt_Password(PassAnsible, MonAnsibleSecurity.GetSalt())
                MonWinRM.set_useransible(UserAnsible)
                MonWinRM.set_passansible(DecryptedPassAnsible)
                MyObjLog.AjouteLog("Création du mot de passe ansible :", MyObjLog.TopExit, False)
                NewPassAnsible = MonAnsibleSecurity.CreatePassword(16)
                MyObjLog.AjouteLog("Création du mot de passe de l'utilisateur temporaire :", MyObjLog.TopExit, False)
                PassAnsible2 = MonAnsibleSecurity.CreatePassword(16)
                IDServer = MonSeveur.GetServeurID(IP)
                Type = MonSeveur.GetServerTypeWithIDServer(IDServer)
                MyObjLog.AjouteLog(f"UserAnsible = {UserAnsible} | PassAnsible = {DecryptedPassAnsible} | NewPassAnsible = {NewPassAnsible} | IDServer = {IDServer} | Type = {Type}", MyObjLog.TopExit, MyObjLog.TopRaise, False)
                # On regarde le type de la machine afin de savoir si on a affaire a une machine Windows ou Linux afin de changer le mot de passe
                if Type == "windows" :
                    MonAnsibleSecurity.SetupAnsible2(IP, PassAnsible2)
                    MonWinRM.set_useransible("Ansible2")
                    MonWinRM.set_passansible(PassAnsible2)
                    MonAnsibleSecurity.ChangePasswordWindows(IP, UserAnsible, NewPassAnsible)
                    MonWinRM.set_useransible(UserAnsible)
                    MonWinRM.set_passansible(NewPassAnsible)
                    MonAnsibleSecurity.RemoveUserWindows(IP)
                elif Type == "linux" :
                    MonAnsibleSecurity.ChangePasswordLinux(IP, UserAnsible, DecryptedPassAnsible, NewPassAnsible)
                else :
                    MyObjLog.AjouteLog("\nNOT OK - Erreur sur le type de la machine", MyObjLog.TopExit, False)
                # On teste si le changement de mot de passe c'est bien passé en essayant de se connecter a la machine
                if (MaConnectivity.TestConnexionAnsible(IP, UserAnsible, NewPassAnsible, Type) == True) :
                    MyObjLog.AjouteLog("OK - L'utilisateur Ansible et le Password Ansible ont bien été changé car on peut se connecter", MyObjLog.TopExit, True)
                    OldPassAnsible = MonSeveur.GetOldPassAnsible(IDServer)
                    if OldPassAnsible == None:      # Ici on remplis le champs OldPassAnsible car il est vide (c'est la première fois qu'on change le mdp du serveur)
                        OldPassAnsible = f"{PassAnsible}"
                    else :      # Ici on remet OldPassAnsible sous forme de liste et on lui ajoute le dernier mot de passe
                        OldPassAnsible = OldPassAnsible.split(", ")
                        if len(OldPassAnsible) < 25 :
                            OldPassAnsible.append(PassAnsible)
                            OldPassAnsible = ", ".join(OldPassAnsible)
                        else :      # Ici si il y a plus de 25 mot de passe dans la liste-, on supprime le premier et on ajoute le nouveau a la fin
                            OldPassAnsible.pop(0)
                            OldPassAnsible.append(PassAnsible)
                            OldPassAnsible = ", ".join(OldPassAnsible)
                    CryptedNewPassAnsible = MonAnsibleSecurity.Crypt_Password(NewPassAnsible, MonAnsibleSecurity.GetSalt())
                    MonSeveur.UpdateUserAnsibleAndPasswordAnsible(CryptedNewPassAnsible, OldPassAnsible, IDServer)
                else :
                    MyObjLog.AjouteLog("NOT OK - L'utilisateur Ansible et le Password Ansible n'ont pas été changé car on ne peut pas se connecter :", MyObjLog.TopExit, True)  
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
    raise err