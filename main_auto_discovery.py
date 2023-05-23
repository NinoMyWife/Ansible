##########################################################################
# Importattion des bibliotheques
##########################################################################

import sys
import Class_Colors
import inspect
import subprocess

##########################################################################
# Importation des classes
#########################################################################

from Class_Servers import Class_Servers
from Class_Tools import Class_Tools
from Class_Connectivity import Class_Connectivity
from Class_Logs import Class_Logs
from Class_WinRM import Class_WinRM
from Class_Applications import Class_App
from Class_Groups import Class_Groups
from Class_PoolIP import Class_PoolIP
from Class_Ansible_Security import Class_Ansible_Security
from Class_Mail import Class_Mail
from Class_MySQL import Class_MySQL
from Class_IPServer import Class_IPServer

##########################################################################
#INITIALISATION BDD#
##########################################################################
try:

    #! prerequis test existance repertoire
    #! Vérifier que la table PoolIP n'est pas vide auquel cas il faudra exécuter "main_fill_ip.py"

    # Permet de clear le prompt à chaque exécution du script
    subprocess.call("clear",shell=True)

    # Instanciation des Objets MyObjLog, MaBDD, MonPoolIP, MonWinRM, MonAnsibleSecurity, MonTools, MaConnectivity, MonMail
    MyObjLog = Class_Logs()
    MaBDD = Class_MySQL(MyObjLog)
    MaBDD.NameBDD = "InventaireDynamique"
    MonPoolIP = Class_PoolIP(MyObjLog, MaBDD)
    MyObjLog.directory= "/root/ScriptsInventaireDynamique/Maintest/"
    MyObjLog.filename= "LogAutoDiscoveryAnsible.txt"
    MyObjLog.writemode = 'w'
    MyObjLog.CreateLogFile("Debut du Cron Auto_Discovery_Ansible")
    MonWinRM = Class_WinRM(MyObjLog)
    MonAnsibleSecurity = Class_Ansible_Security(MyObjLog, MonWinRM, MaBDD)
    MonTools = Class_Tools(MyObjLog, MonWinRM, MaBDD)
    MaConnectivity = Class_Connectivity(MyObjLog, MonWinRM)
    MyObjLog.AjouteLog(MonTools.Cartouchetop())
    MonMail = Class_Mail(MyObjLog)
    # Récupération de la liste des IPs de la table PoolIP
    # ListIP = MonPoolIP.GetPoolIpList()
    # Récupération de la liste des IPs de la table PoolIP qui correspondent au VLAN
    ListIP = MonPoolIP.GetListIpWithVLAN(15)

    try:
        if sys.argv :
            changemdp = sys.argv[1]
        monkey = ["192.168.200.41", "192.168.200.42", "192.168.200.43", "192.168.200.44", "10.10.50.250", "10.10.50.251", "10.10.0.240", "10.10.10.238", "10.10.50.242", "10.10.50.169"]
        # ipaanalyser = ["185.190.91.14", "10.10.50.36", "10.10.50.97", "185.190.91.12"]
        # testsimple = ["185.190.91.32"]
        # testsimplelinetsimplewin = ["192.168.200.29", "185.190.91.32", "192.168.200.38", "192.168.200.39"]
        # testmultiple = ["185.190.91.22", "185.190.91.117", "185.190.91.118", "185.190.91.119", "185.190.91.120"]
        # test3ip = ['185.190.91.22', '192.168.200.216', '10.10.10.251']
        # testmemeservwindow = ["93.93.184.124", "93.93.184.106"]
        # testmemeservlinux = ["185.190.91.62", "192.168.200.83"]

        # Boucle qui va passer sur toutes les IPs
        for IP in ListIP:
            # Instanciation des Objets MonWinRM, Monserver, MonGroup, MyApp qui seront détruit a la fin de chaque boucle et recréer au début de chaque boucle
            MonWinRM = Class_WinRM(MyObjLog)
            Monserver = Class_Servers(MyObjLog, MonWinRM, MaBDD)
            if changemdp == "True" :
                Monserver.Mdp = True
            MonGroup = Class_Groups(MyObjLog, Monserver, MaBDD)
            IP = IP[0]
            MyObjLog.AjouteLog(f"\n\nDecouverte de l'IP : {IP}\n")
            PassAnsibleUserAnsibleIDServerByIPServer = Monserver.GetPassAnsibleUserAnsibleIDServerByIPServer(IP)
            # On verifie si le serveur est deja enregistrer en base pour utiliser ses informations de connection
            if PassAnsibleUserAnsibleIDServerByIPServer != None :
                TestConnectivity = MaConnectivity.TestConnectivity(IP)
                if TestConnectivity[1] == True :
                    Type = "linux"
                if TestConnectivity[0] == True:
                    Type = "windows"
                if (TestConnectivity[0] == False and TestConnectivity[1] == False and TestConnectivity[2] == True):
                    Type = "unknow"
                # Si on arrive pas se connecter on retente avec le mot de passe ansible car l'IP a peut être été réatribuée
                if (MaConnectivity.TestConnexionAnsible(IP, PassAnsibleUserAnsibleIDServerByIPServer[1], MonAnsibleSecurity.Decrypt_Password(PassAnsibleUserAnsibleIDServerByIPServer[2], MonAnsibleSecurity.GetSalt()), Type) != True) :
                    Monserver.set_passansible(Monserver.get_passansible())
                    MonWinRM.set_useransible(Monserver.get_useransible())
                    MonWinRM.set_passansible(Monserver.get_passansible())
                    # Le Hostname n'est pas déjà enregistré mais on enlève la liaison dans IPServer car l'IP est une IP Secondaire
                    # Et pour Unknown on skip car on peut avoir plusieurs Serveur Unknown et si on supprime l'IP dans PoolIP ça re-instancierais le Serveur a chaque fois
                    if PassAnsibleUserAnsibleIDServerByIPServer[3] != "Unknown" : 
                        MonIPServer = Class_IPServer(MyObjLog, MaBDD)
                        IDPoolIP = MonPoolIP.GetPoolIPID(IP)
                        MonIPServer.DeleteIPServerByIDPoolIP(IDPoolIP)
                # Sinon on se connecte avec les login récupérés
                else :
                    Monserver.set_useransible(PassAnsibleUserAnsibleIDServerByIPServer[1])
                    Monserver.set_passansible(MonAnsibleSecurity.Decrypt_Password(PassAnsibleUserAnsibleIDServerByIPServer[2], MonAnsibleSecurity.GetSalt()))
                    MonWinRM.set_useransible(Monserver.get_useransible())
                    MonWinRM.set_passansible(Monserver.get_passansible())
            # Si le Server n'est pas déjà enregistré on prends les login par défault
            else :
                Monserver.set_passansible(Monserver.get_passansible())
                MonWinRM.set_useransible(Monserver.get_useransible())
                MonWinRM.set_passansible(Monserver.get_passansible())
            Monserver.set_MonWinRM(MonWinRM)
            # On teste la connectivite pour savoir si le serveur est accessible en SSH, WinRM ou juste pingable
            TestConnectivity = MaConnectivity.TestConnectivity(IP)

    ##########################################################################
    #TEST WinRM#
    ##########################################################################

            try:
                # Ici on verifie que le serveur en question est bien un serveur Linux et que le SSH est actif puis on recupere ses informations
                if TestConnectivity[1] == True :
                    try:
                        MyObjLog.AjouteLog("NOTICE - Machine Linux", MyObjLog.TopExit, True)
                        # On recupere les informations necessaire sur le serveur
                        Monserver.GetInfosServerLinux(IP)
                        if Monserver.get_IpIsSecondary() == False :
                            Monserver.InsertServerBDD(Monserver.get_hostname(),Monserver.get_commonname(), Monserver.get_idhyperviseur(), Monserver.get_idos(), Monserver.get_useransible(), Monserver.get_passansible(), Monserver.get_deleted(), IP)
                        MyObjLog.AjouteLog(f"NOTICE - hostname : {Monserver.get_hostname()}, commonname: {Monserver.get_commonname()}, idhyperviseur : {Monserver.get_idhyperviseur()}, idos : {Monserver.get_idos()}, useransible : {Monserver.get_useransible()}, passansible : {Monserver.get_passansible()}, deleted : {Monserver.get_deleted()}, IP : {IP}, IDServer : {Monserver.get_IDServer()}, IDPoolIP : {Monserver.get_IDPoolIP()}", MyObjLog.TopExit, True)
                    except Exception as err :
                        # Même si ça catch on enregistre le serveur avec les informations qu'on a pu recuperer
                        if Monserver.get_IpIsSecondary() == False :
                            Monserver.InsertServerBDD(Monserver.get_hostname(),Monserver.get_commonname(), Monserver.get_idhyperviseur(), Monserver.get_idos(), Monserver.get_useransible(), Monserver.get_passansible(), Monserver.get_deleted(), IP)
                            MyObjLog.AjouteLog(f"NOTICE - hostname : {Monserver.get_hostname()}, commonname: {Monserver.get_commonname()}, idhyperviseur : {Monserver.get_idhyperviseur()}, idos : {Monserver.get_idos()}, useransible : {Monserver.get_useransible()}, passansible : {Monserver.get_passansible()}, deleted : {Monserver.get_deleted()}, IP : {IP}, IDServer : {Monserver.get_IDServer()}, IDPoolIP : {Monserver.get_IDPoolIP()}", MyObjLog.TopExit, True)
                        raise
                    try:
                        # ? POUR LES GROUPES
                        MyObjLog.AjouteLog("\nServerGroup\n", MyObjLog.TopExit, True)
                        IDServer = Monserver.GetIDServerWithIP(IP)
                        MonGroup.AffectGroup(IDServer)
                    except Exception as err :
                        MyObjLog.AjouteLog("\nNOT OK - Erreur lors de l'affectation des groupes Linux", MyObjLog.TopExit, True)
                        raise
                    try:
                        # ? POUR LES APPS
                        MyObjLog.AjouteLog("\nServerApp\n", MyObjLog.TopExit, True)
                        MyApp = Class_App(MyObjLog, MonWinRM, MaBDD, Monserver)
                        MyApp.AffectApplicationsToServerForLinux(IP, Monserver.get_idos())
                    except Exception as err :
                        MyObjLog.AjouteLog("\nNOT OK - Erreur lors de l'affectation des apps Linux", MyObjLog.TopExit, True)
                        raise
            except Exception as err :
                MyObjLog.AjouteLog(f"ERREUR - main_auto_discovery - Section SSH - Erreur : {err}", MyObjLog.TopExit, True)
            try:
                # Ici on verifie que le serveur en question est bien un serveur Windows et que le port WinRM est accessible puis on recupere ses informations
                if TestConnectivity[0] == True:
                    try:
                        MyObjLog.AjouteLog("NOTICE - Machine Windows", MyObjLog.TopExit, True)
                        # On recupere les informations necessaire sur le serveur
                        Monserver.GetInfosServerWindows(IP)
                        if Monserver.get_IpIsSecondary() == False :
                            Monserver.InsertServerBDD(Monserver.get_hostname(),Monserver.get_commonname(), Monserver.get_idhyperviseur(), Monserver.get_idos(), Monserver.get_useransible(), Monserver.get_passansible(), Monserver.get_deleted(), IP)
                        MyObjLog.AjouteLog(f"NOTICE - hostname : {Monserver.get_hostname()}, commonname: {Monserver.get_commonname()}, idhyperviseur : {Monserver.get_idhyperviseur()}, idos : {Monserver.get_idos()}, useransible : {Monserver.get_useransible()}, passansible : {Monserver.get_passansible()}, deleted : {Monserver.get_deleted()}, IP : {IP}, IDServer : {Monserver.get_IDServer()}, IDPoolIP : {Monserver.get_IDPoolIP()}", MyObjLog.TopExit, True)
                    except Exception as err :
                        MyObjLog.AjouteLog(f"ERREUR - main_auto_discovery - Section Windows - Erreur : {err}", MyObjLog.TopExit, True)
                        # Même si ça catch on enregistre le serveur avec les informations qu'on a pu recuperer
                        if Monserver.get_IpIsSecondary() == False :
                            Monserver.InsertServerBDD(Monserver.get_hostname(),Monserver.get_commonname(), Monserver.get_idhyperviseur(), Monserver.get_idos(), Monserver.get_useransible(), Monserver.get_passansible(), Monserver.get_deleted(), IP)
                            MyObjLog.AjouteLog(f"NOTICE - hostname : {Monserver.get_hostname()}, commonname: {Monserver.get_commonname()}, idhyperviseur : {Monserver.get_idhyperviseur()}, idos : {Monserver.get_idos()}, useransible : {Monserver.get_useransible()}, passansible : {Monserver.get_passansible()}, deleted : {Monserver.get_deleted()}, IP : {IP}, IDServer : {Monserver.get_IDServer()}, IDPoolIP : {Monserver.get_IDPoolIP()}", MyObjLog.TopExit, True)
                    try:
                        # ? POUR LES GROUPES
                        MyObjLog.AjouteLog("\nServerGroup\n", MyObjLog.TopExit, True)
                        IDServer = Monserver.GetIDServerWithIP(IP)
                        MonGroup.AffectGroup(IDServer)
                    except Exception as err :
                        MyObjLog.AjouteLog("\nNOT OK - Erreur lors de l'affectation des groupes Windows", MyObjLog.TopExit, True)
                        raise
                    try:
                        # ? POUR LES APPS
                        MyObjLog.AjouteLog("\nServerApp\n", MyObjLog.TopExit, True)
                        MyApp = Class_App(MyObjLog, MonWinRM, MaBDD, Monserver)
                        MyApp.AffectApplicationsToServerForWindows(IP, Monserver.get_idos())
                    except Exception as err :
                        MyObjLog.AjouteLog("\nNOT OK - Erreur lors de l'affectation des apps Windows", MyObjLog.TopExit, True)
                        raise
            except Exception as err :
                MyObjLog.AjouteLog(f"ERREUR - main_auto_discovery - Section WinRM - Erreur : {err}", MyObjLog.TopExit, True)
            try:
                # Si le serveur est pingable on Update le champ Pingable de l'IP dans PoolIP
                if TestConnectivity[2] == True :
                    MonPoolIP.UpdatePingable(IP)
                    MyObjLog.AjouteLog(f"NOTICE - L'IP : {IP} est pingable", MyObjLog.TopExit, True)
            except Exception as err :
                MyObjLog.AjouteLog(f"ERREUR - main_auto_discovery - Section Pingable - Erreur : {err}", MyObjLog.TopExit, True)
            # Ici on verifie que le serveur en question est ni un serveur Windows et ni un serveur Linux mais qu'il est Pingable alors on le met en unknow
            if (TestConnectivity[0] == False and TestConnectivity[1] == False and TestConnectivity[2] == True):
                try:
                    MyObjLog.AjouteLog("NOTICE - Machine inconnue", MyObjLog.TopExit, True)
                    Monserver.InsertServerBDD(Monserver.get_hostname(),Monserver.get_commonname(), Monserver.get_idhyperviseur(), Monserver.get_idos(), Monserver.get_useransible(), Monserver.get_passansible(), Monserver.get_deleted(), IP)
                    MonPoolIP.UpdateTopAnsible(IP)
                    MyObjLog.AjouteLog(f"NOTICE - hostname : {Monserver.get_hostname()}, commonname: {Monserver.get_commonname()}, idhyperviseur : {Monserver.get_idhyperviseur()}, idos : {Monserver.get_idos()}, useransible : {Monserver.get_useransible()}, passansible : {Monserver.get_passansible()}, deleted : {Monserver.get_deleted()}, IP : {IP}, IDServer : {Monserver.get_IDServer()}, IDPoolIP : {Monserver.get_IDPoolIP()}", MyObjLog.TopExit, True)
                except Exception as err :
                    MyObjLog.AjouteLog(f"ERREUR - main_auto_discovery - Section Unknown - Erreur : {err}", MyObjLog.TopExit, True)
            del Monserver
        # Envoi du rapport par mail
        LogReport = MonAnsibleSecurity.GetErrorReport(f"{MyObjLog.directory}{MyObjLog.filename}")
        MonMail.SendReportMail(LogReport[0], LogReport[1])
    except Exception as err :
        MyObjLog.AjouteLog("\nNOT OK - Recuperation de la liste des IP de HostUP", MyObjLog.TopExit, True)
        raise
except Exception as err :
    MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}", MyObjLog.TopExit, True)
    raise