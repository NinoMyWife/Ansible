import sys
import unittest
import paramiko
import datetime
from unittest import mock
from Class_OS import Class_OS
from Class_Mail import Class_Mail
from Class_Logs import Class_Logs
from Class_MySQL import Class_MySQL
from Class_WinRM import Class_WinRM
from Class_Tools import Class_Tools
from Class_MySQL import Class_MySQL
from Class_PoolIP import Class_PoolIP
from Class_Groups import Class_Groups
from Class_Servers import Class_Servers
from Class_Applications import Class_App
from Class_IPServer import Class_IPServer
from Class_ServerApps import Class_ServerApps
from Class_Hypervisor import Class_Hypervisor
from Class_ServerGroup import Class_ServerGroup
from Class_Connectivity import Class_Connectivity
from Class_Ansible_Security import Class_Ansible_Security

class Test(unittest.TestCase) :

    def __init__(self, *args, **kwargs) :
        super(Test, self).__init__(*args, **kwargs)
        MyObjLog = Class_Logs()
        MonWinRM = Class_WinRM(MyObjLog)
        MaBDD = Class_MySQL(MyObjLog)
        MonServer = Class_Servers(MyObjLog, MonWinRM, MaBDD)
        self._MyObjLog = MyObjLog
        self._MonWinRM = MonWinRM
        self._MonServer = MonServer
        self._MaBDD = MaBDD
        self.IPLinuxCentOS = "192.168.200.29"
        self.IPLinuxDebian = "192.168.200.28"
        self.IPWindows = "185.190.91.32"
        self.UserAnsible = "ansible"
        self.PassAnsible = Class_Ansible_Security.Decrypt_Password(self, "XXXXXX", Class_Ansible_Security.GetSalt(self))
        # self.PassAnsible = "q9!lw#OX#lF.jG@w"
        self._MonWinRM.set_useransible(self.UserAnsible)
        self._MonWinRM.set_passansible(self.PassAnsible)
        self._MaBDD.NameBDD = "AnsibleTest"
        self._MyObjLog.directory= "/root/ScriptsInventaireDynamique/Maintest/"
        self._MyObjLog.filename= "LogClassTest.txt"
        self._MyObjLog.writemode = 'w'
        self._MyObjLog.CreateLogFile("Debut de la classe de test")
        self.TopExit = False
        self.TopRaise = False
        self.TopPrintLog = False



# ?#########################################################################
# ? Class_Ansible_Security
# ?#########################################################################



    def GetAdministratorWindows(self, IPServeur):
        try :
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServeur
            # Commande permettant de récupérer tous les utilisateurs appartenant au groupe Administrateur
            self._MonWinRM.Run_WinRM_PS_Session(f'Get-LocalGroupMember -Group "Administrateurs"')
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - Les utilisateurs Admin ont bien étaient récupéré", self.TopExit, True)
                return self._MonWinRM.std_out
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la récupération des utilisateurs Admin", self.TopExit, True)
                raise Exception("Erreur lors de la récupération des utilisateurs Admin")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetListUserLinux(self, IPServeur, UserAnsible, PassAnsible, NbrUserToFind):
        try :
            # Connexion a Paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(IPServeur, 22, UserAnsible, PassAnsible)
            # Si le nombre d'utilisateur a trouver est 2 (ansible et testtom)
            if NbrUserToFind  == 2 : 
                # Commande permettant de vérifier si les utilisateur son bien créé
                stdin, stdout, stderr = ssh.exec_command(command=f"cat /etc/passwd | grep -cim1 'ansible\|testtom'")
            # Si le nombre d'utilisateur a trouver est 1 (ansible)
            if NbrUserToFind  == 1 : 
                # Commande permettant de vérifier si les utilisateur son bien créé
                stdin, stdout, stderr = ssh.exec_command(command=f"cat /etc/passwd | grep -cim1 'ansible'")
            # Vérification que la commande c'est bien passé
            if stdout.channel.recv_exit_status() != 0:
                self._MyObjLog.AjouteLog(f"Erreur lors de la recupération des utilisateurs", self.TopExit, True)
                raise Exception("Erreur lors de la recupération des utilisateurs")
            else :
                self._MyObjLog.AjouteLog(f"OK - Récupération des utilisateurs", self.TopExit, True)
                return stdout.readlines()
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    # def test_CreateUserAnsible(self): #? SKIP
    #     MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
    #     CreateUserAnsible = MonAnsibleSecurity.CreateUserAnsible()
    #     self.assertEqual()

    # def test_CreatePassword(self): #? SKIP
    #     MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
    #     CreatePassword = MonAnsibleSecurity.CreatePassword(16)
    #     self.assertEqual()

    def test_1ChangePasswordLinux(self):
        try :
            # Instanciation de l'objet MonAnsibleSecurity
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            TempPassw = "K2jn477_3K1RpGY0"
            # Changement de password sur la machine CentOS
            MonAnsibleSecurity.ChangePasswordLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible, TempPassw)
            # Attribution du mot de passe a l'objet de connexion
            self._MonWinRM.set_passansible("K2jn477_3K1RpGY0")
            # Test de connectivité afin de voir si le mot de passe a bien été changé
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertEqual(TestConnectivity, (False, True, True))
            # On remet l'ancien password afin de revenir a l'état d'origine
            OldPassw = Class_Ansible_Security.Decrypt_Password(self, "XXXXXX", Class_Ansible_Security.GetSalt(self))
            MonAnsibleSecurity.ChangePasswordLinux(self.IPLinuxCentOS, self.UserAnsible, self._MonWinRM.get_passansible(), OldPassw)
            # Attribution de l'ancien mot de passe a l'objet de connexion
            self._MonWinRM.set_passansible(OldPassw)
            # Test de connectivité afin de voir si le mot de passe a bien été changé
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertEqual(TestConnectivity, (False, True, True))
        except Exception as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

        try:
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            TempPassw = "K2jn477_3K1RpGY0"
            MonAnsibleSecurity.ChangePasswordLinux(self.IPLinuxCentOS, "toto", self.PassAnsible, TempPassw)
        except Exception :
            self.assertRaises(paramiko.ssh_exception.AuthenticationException)

    def test_2SetupAnsible2(self):
        try :
            # Instanciation de l'objet MonAnsibleSecurity
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Création des variables temporaires
            TempPassw = "K2jn477_3K1RpGY0"
            TempUser1 = "Ansible2" 
            TempUser2 = "testtom"
            # Création du compte temporaire Windows et attribution des droits Administrateur
            MonAnsibleSecurity.SetupAnsible2(self.IPWindows, self.PassAnsible)
            # Vérification si le compte est bien Administrateur et si il a bien été créé
            GetAdministratorWindows = self.GetAdministratorWindows(self.IPWindows)
            self.assertEqual(GetAdministratorWindows, "ObjectClass Name                    PrincipalSource  ----------- ----                    ---------------  Utilisateur TEST-PVE Administrateur Local            Utilisateur TEST-PVE ansible        Local            Utilisateur TEST-PVE Ansible2       Local")
            # Changement du nom d'utilisateur du compte temporaire
            MonAnsibleSecurity.ChangeUserWindows(self.IPWindows, TempUser1, TempUser2)
            # Vérification si le compte a bien changé de nom
            GetAdministratorWindows = self.GetAdministratorWindows(self.IPWindows)
            self.assertEqual(GetAdministratorWindows, "ObjectClass Name                    PrincipalSource  ----------- ----                    ---------------  Utilisateur TEST-PVE Administrateur Local            Utilisateur TEST-PVE ansible        Local            Utilisateur TEST-PVE testtom        Local")
            # Changement du nom d'utilisateur du compte temporaire, on reviens a l'état initial
            MonAnsibleSecurity.ChangeUserWindows(self.IPWindows, TempUser2, TempUser1)
            # Vérification si le compte a bien changé de nom
            GetAdministratorWindows = self.GetAdministratorWindows(self.IPWindows)
            self.assertEqual(GetAdministratorWindows, "ObjectClass Name                    PrincipalSource  ----------- ----                    ---------------  Utilisateur TEST-PVE Administrateur Local            Utilisateur TEST-PVE ansible        Local            Utilisateur TEST-PVE Ansible2       Local")
            # Changement de mot de passe pour un compte Windows
            MonAnsibleSecurity.ChangePasswordWindows(self.IPWindows, TempUser1, TempPassw)
            # Attribution des login a l'objet de connexion
            self._MonWinRM.set_useransible(TempUser1)
            self._MonWinRM.set_passansible(TempPassw)
            # Test de connexion pour voir si les nouveaux logins sont bon
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertEqual(TestConnectivity, (True, False, True))
            # Attribution des login ansible a l'objet de connexion afin de modifier l'utilisateur temporaire
            self._MonWinRM.set_useransible(self.UserAnsible)
            self._MonWinRM.set_passansible(self.PassAnsible)
            OldPassw = Class_Ansible_Security.Decrypt_Password(self, "XXXXXX", Class_Ansible_Security.GetSalt(self))
            # Changement du mot de passe de l'utilisateur temporaire
            MonAnsibleSecurity.ChangePasswordWindows(self.IPWindows, TempUser1, OldPassw)
            # Attribution des login a l'objet de connexion
            self._MonWinRM.set_useransible(TempUser1)
            self._MonWinRM.set_passansible(OldPassw)
            # Test de connexion pour voir si les nouveaux logins sont bon
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertEqual(TestConnectivity, (True, False, True))
            # Attribution des login ansible a l'objet de connexion
            self._MonWinRM.set_useransible(self.UserAnsible)
            self._MonWinRM.set_passansible(self.PassAnsible)
            # Suppression de l'utilisateur temporaire
            MonAnsibleSecurity.RemoveUserWindows(self.IPWindows)
            # Vérification si l'utilisateur temporaire a bien été supprimé
            GetAdministratorWindows = self.GetAdministratorWindows(self.IPWindows)
            self.assertEqual(GetAdministratorWindows, "ObjectClass Name                    PrincipalSource  ----------- ----                    ---------------  Utilisateur TEST-PVE Administrateur Local            Utilisateur TEST-PVE ansible        Local")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

        try :
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            MonAnsibleSecurity.SetupAnsible2(self.IPLinuxCentOS, self.PassAnsible)
        except Exception :
            self.assertRaises(OSError)

    def test_3CryptDecrypt(self):
        try :
            passwd = "toto"
            # Chiffrement d'un mot de passe
            crypt = Class_Ansible_Security.Crypt_Password(self, passwd, Class_Ansible_Security.GetSalt(self))
            decrypt = Class_Ansible_Security.Decrypt_Password(self, crypt, Class_Ansible_Security.GetSalt(self))
            # Vérification de si le mot de passe déchiffré est le même que le mot de passe de départ
            self.assertEqual(decrypt, "toto")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

        try :
            # Test  en donnant le mauvais type a la variable d'entré
            passwd = b'toto'
            # Chiffrement d'un mot de passe
            crypt = Class_Ansible_Security.Crypt_Password(self, passwd, Class_Ansible_Security.GetSalt(self))
            decrypt = Class_Ansible_Security.Decrypt_Password(self, crypt, Class_Ansible_Security.GetSalt(self))
            # Vérification de si le mot de passe déchiffré est le même que le mot de passe de départ
            self.assertEqual(decrypt, "toto")
        except (TypeError) :
            self.assertRaises(TypeError)

    def test_4GetSalt(self):
        try :
            # Vérification de si on obtient bien le salt
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            GetSalt = MonAnsibleSecurity.GetSalt()
            self.assertEqual(GetSalt, b'grlnGkOKrrwdSvYSrwY87DTbz-4NlbFLfW6Fq099X1s=')
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_5GetErrorReport(self):
        try :
            # Vérification de si on obtient bien le rapport d'erreur
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            GetErrorReport = MonAnsibleSecurity.GetErrorReport("/root/ScriptsInventaireDynamique/Maintest/TestLogReport.log")
            self.assertEqual(GetErrorReport ,('NOT OK azertyuiopqsdfghjklmwxcvbn0123456789/*-+&é"\\\'(-è_çà)=$^*ù!:;,<>?./§%µ£¨+°²~#{[|`\\\\^@]}¤\n\nNOT OK azertyuiopqsdfghjklmwxcvbn0123456789/*-+&é"\\\'(-è_çà)=$^*ù!:;,<>?./§%µ£¨+°²~#{[|`\\\\^@]}¤\nOK azertyuiopqsdfghjklmwxcvbn0123456789/*-+&é"\\\'(-è_çà)=$^*ù!:;,<>?./§%µ£¨+°²~#{[|`\\\\^@]}¤', 1))
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

        try :
            # Test en lui donnant le mauvais chemin de fichier
            # Vérification de si on obtient bien le rapport d'erreur
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            GetErrorReport = MonAnsibleSecurity.GetErrorReport("/root/ScriptsInventaireDynamique/TestLogReport.log")
            self.assertEqual(GetErrorReport ,('NOT OK azertyuiopqsdfghjklmwxcvbn0123456789/*-+&é"\\\'(-è_çà)=$^*ù!:;,<>?./§%µ£¨+°²~#{[|`\\\\^@]}¤\n\nNOT OK azertyuiopqsdfghjklmwxcvbn0123456789/*-+&é"\\\'(-è_çà)=$^*ù!:;,<>?./§%µ£¨+°²~#{[|`\\\\^@]}¤\nOK azertyuiopqsdfghjklmwxcvbn0123456789/*-+&é"\\\'(-è_çà)=$^*ù!:;,<>?./§%µ£¨+°²~#{[|`\\\\^@]}¤', 1))
        except FileNotFoundError :
            self.assertRaises(FileNotFoundError)

    def test_6SetupUserAnsibleLinux(self): #* Le test de CreateUserLinux, AddPassword et de AddGroupLinux se font aussi dans cette fonction de test
        try :
            # Machine CentOS
            # Instanciation de l'objet MonAnsibleSecurity
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Création du compte temporaire Linux et attribution des droits Administrateur
            MonAnsibleSecurity.SetupUserAnsibleLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible, "testtom", "q9!lw#OX#lF.jG@w", 2)
            # Vérification de la liste des utilisateurs Linux afin de voir si l'tuilisateur a bien été créé
            GetListUserLinux = self.GetListUserLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible, 2)
            self.assertEqual(GetListUserLinux, ['1\n'])
            # Suppression de l'utilisateur temporaire
            MonAnsibleSecurity.DelUserLinux(self.IPLinuxCentOS, "testtom", self.UserAnsible, self.PassAnsible)
            # Vérification de si l'utilisateur temporaire a bien été supprimé
            GetListUserLinux = self.GetListUserLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible, 1)
            self.assertEqual(GetListUserLinux, ['1\n'])
            
            # Machine Debian
            # Instanciation de l'objet MonAnsibleSecurity
            MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Création du compte temporaire Linux et attribution des droits Administrateur
            MonAnsibleSecurity.SetupUserAnsibleLinux(self.IPLinuxDebian, self.UserAnsible, self.PassAnsible, "testtom", "q9!lw#OX#lF.jG@w", 4)
            # Vérification de la liste des utilisateurs Linux afin de voir si l'tuilisateur a bien été créé
            GetListUserLinux = self.GetListUserLinux(self.IPLinuxDebian, self.UserAnsible, self.PassAnsible, 2)
            self.assertEqual(GetListUserLinux, ['1\n'])
            # Suppression de l'utilisateur temporaire
            MonAnsibleSecurity.DelUserLinux(self.IPLinuxDebian, "testtom", self.UserAnsible, self.PassAnsible)
            # Vérification de si l'utilisateur temporaire a bien été supprimé
            GetListUserLinux = self.GetListUserLinux(self.IPLinuxDebian, self.UserAnsible, self.PassAnsible, 1)
            self.assertEqual(GetListUserLinux, ['1\n'])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



# #?#########################################################################
# #? Class_Connectivity
# #?#########################################################################



    def test_9ConnectivityWindows(self) :
        try :
            # Test de connectivité Linux
            # Vérification que le résultat est WinRM = True | SSH = False | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertEqual(TestConnectivity, (True, False, True))
            # Vérification que le résultat n'est pas WinRM = True | SSH = False | Ping = False
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertNotEqual(TestConnectivity, (True, False, False))
            # Vérification que le résultat n'est pas WinRM = False | SSH = False | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertNotEqual(TestConnectivity, (False, False, True))
            # Vérification que le résultat n'est pas WinRM = False | SSH = True | Ping = False
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertNotEqual(TestConnectivity, (False, True, True))
            # Vérification que le résultat n'est pas WinRM = False | SSH = False | Ping = False
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertNotEqual(TestConnectivity, (False, False, False))
            # Vérification que le résultat n'est pas WinRM = True | SSH = True | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPWindows)
            self.assertNotEqual(TestConnectivity, (True, True, True))
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_10ConnectivityLinux(self) :
        try :
            # Test de connectivité Linux
            # Vérification que le résultat est WinRM = False | SSH = True | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertEqual(TestConnectivity, (False, True, True))
            # Vérification que le résultat n'est pas WinRM = True | SSH = False | Ping = False
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertNotEqual(TestConnectivity, (True, False, False))
            # Vérification que le résultat n'est pas WinRM = False | SSH = False | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertNotEqual(TestConnectivity, (False, False, True))
            # Vérification que le résultat n'est pas WinRM = True | SSH = False | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertNotEqual(TestConnectivity, (True, False, True))
            # Vérification que le résultat n'est pas WinRM = False | SSH = False | Ping = False
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertNotEqual(TestConnectivity, (False, False, False))
            # Vérification que le résultat n'est pas WinRM = True | SSH = True | Ping = True
            TestConnectivity = Class_Connectivity.TestConnectivity(Class_Connectivity(self._MyObjLog, self._MonWinRM), self.IPLinuxCentOS)
            self.assertNotEqual(TestConnectivity, (True, True, True))
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_Groups
#?#########################################################################



    def GetGroupForServer(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer l'ID Group d'un Serveur
            query = self._MaBDD.SelectRow(db, f"SELECT IDGroup FROM ServerGroup WHERE IDServer = {IDServer} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_11GetGroupIDWithIDServer(self):
        try :
            # Instanciation de l'objet MonGroup
            MonGroup = Class_Groups(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'ID Serveur pour Linux et pour Windows
            GetGroupIDWithIDServerWindows = MonGroup.GetGroupIDWithIDServer(2)
            GetGroupIDWithIDServerLinux = MonGroup.GetGroupIDWithIDServer(1)
            # Vérification des IDs obtenue
            self.assertEqual(GetGroupIDWithIDServerWindows, 1)
            self.assertEqual(GetGroupIDWithIDServerLinux, 2)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_12GetGroupList(self):
        try:
            # Instanciation de l'objet MonGroup
            MonGroup = Class_Groups(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de la liste des groupes
            GetGroupList = MonGroup.GetGroupList()
            # Vérification de la liste des groupes
            self.assertEqual(GetGroupList, ([(1, 'windows', 'get_Type()', 'windows', None, 0, datetime.datetime(2022, 10, 25, 14, 11, 52)), (2, 'linux', 'get_Type()', 'linux', None, 0, datetime.datetime(2022, 10, 25, 14, 13, 10)), (3, 'maxplus', 'get_Name_VLAN()', '820', None, 0, datetime.datetime(2022, 10, 25, 14, 13, 17))], ('ID', 'GroupName', 'RegexProperties', 'Regex', 'InsertDate', 'Deleted', 'UpdateDate')))
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_13AffectGroup(self):
        try:
            # Instanciation des objets MonGroup, MonTool
            MonGroup = Class_Groups(self._MyObjLog, self._MonServer, self._MaBDD)
            MonTool = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Attribution du VLAN a l'attribut Name_VLAN de la classe Server
            self._MonServer.set_Name_VLAN(MonTool.Get_Name_VLAN(self.IPWindows))
            # Attribution du Type a l'attribut Type de la classe Server
            self._MonServer.set_Type("windows")
            # Affectation du groupe
            MonGroup.AffectGroup(2)
            # Récupération de la liste des Server du ayant pour numéro de groupe 2
            GroupWindows = self.GetGroupForServer(2)
            # Vérification que de l'ID du Serveur ayant pour numéro de groupe 2
            self.assertEqual(GroupWindows, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_Hypervisor
#?#########################################################################



    def test_14GetHypervisorWindows(self):
        try :
            # Instanciation de l'objet MonHyperviseur
            MonHyperviseur = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'hyperviseur pour Windows
            GetHypervisorWindows = MonHyperviseur.GetHypervisorWindows(self.IPWindows)
            # Vérification de l'hyperviseur obtenu
            self.assertEqual(GetHypervisorWindows, "proxmox")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_15GetHypervisorLinux(self):
        try :
            # Instanciation de l'objet MonHyperviseur
            MonHyperviseur = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'hyperviseur pour Linux
            GetHypervisorLinux = MonHyperviseur.GetHypervisorLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible, 2)
            # Vérification de l'hyperviseur obtenu
            self.assertEqual(GetHypervisorLinux, "proxmox")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_16GetHypervisorIDForWindowsServer(self):
        try :
            # Instanciation de l'objet MonHyperviseur
            MonHyperviseur = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'ID de l'hyperviseur pour Windows
            GetHypervisorIDForWindowsServer = MonHyperviseur.GetHypervisorIDForWindowsServer(self.IPWindows)
            # Vérification de L'ID hyperviseur obtenu
            self.assertEqual(GetHypervisorIDForWindowsServer, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_17GetHypervisorIDForLinuxServer(self):
        try :
            # Instanciation de l'objet MonHyperviseur
            MonHyperviseur = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'ID de l'hyperviseur pour Linux
            GetHypervisorIDForLinuxServer = MonHyperviseur.GetHypervisorIDForLinuxServer(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible, 3)
            # Vérification de L'ID hyperviseur obtenu
            self.assertEqual(GetHypervisorIDForLinuxServer, 3)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_18HypervisorExists(self):
        try :
            # Instanciation de l'objet MonHyperviseur
            MonHyperviseur = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Requetage en base pour savoir si l'Hyperviseur existe
            HypervisorExists_proxmox = MonHyperviseur.HypervisorExists("proxmox")
            HypervisorExists_vmware = MonHyperviseur.HypervisorExists("vmware")
            HypervisorExists_unknown = MonHyperviseur.HypervisorExists("unknown")
            # Vérification des résultats obtenus
            self.assertEqual(HypervisorExists_proxmox, 1)
            self.assertEqual(HypervisorExists_vmware, 1)
            self.assertEqual(HypervisorExists_unknown, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

        try :
            # Test en essayant avec un hyperviseur non présent en base
            # Instanciation de l'objet MonHyperviseur
            MonHyperviseur = Class_Hypervisor(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Requetage en base pour savoir si l'Hyperviseur existe
            HypervisorExists_proxmox = MonHyperviseur.HypervisorExists("toto")
            # Vérification qu'il n'existe pas
            self.assertNotEqual(HypervisorExists_proxmox, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_IPServer
#?#########################################################################



    def GetIDPoolIPWithIDServer(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer l'ID de PoolIP depuis IPServer
            query = self._MaBDD.SelectRow(db, f"SELECT IDPoolIP FROM IpServer WHERE IDServer = {IDServer} and Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_19AddIpOnIPServer(self):
        try :
            # Instanciation de l'objet MonIpServ
            MonIpServ = Class_IPServer(self._MyObjLog, self._MaBDD)
            # Ajout d'une ligne dans IPServer avec IDPoolIP = 3070 et IDServer = 1
            MonIpServ.AddIpOnIPServer(3070, 1)
            # Récupération des IDPoolIP ou l'ID Server vaut 1 dans IPServer
            IPServer = self.GetIDPoolIPWithIDServer(1)
            # Vérification des IDPoolIP ayant l'IDServer 1
            self.assertEqual(IPServer, [(2,), (3070,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_20DeleteIPServerByIDServer(self): 
        try :
            # Instanciation de l'objet MonIpServ
            MonIpServ = Class_IPServer(self._MyObjLog, self._MaBDD)
            # Suppression de toutes les IPs liés a un IDServer
            MonIpServ.DeleteAllIPServerByIDServer(3)
            # Récupération des IDPoolIP ou l'ID Server vaut 3 dans IPServer
            GetIDPoolIPWithIDServer = self.GetIDPoolIPWithIDServer(3)
            # Vérification des IDPoolIP ayant l'IDServer 3
            self.assertEqual(GetIDPoolIPWithIDServer, [])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_Mail
#?#########################################################################



    # def test_SendReportMail(self): #? SKIP
    #     MonMail = Class_Mail(self._MyObjLog)
    #     SendReportMail = MonMail.SendReportMail()



#?#########################################################################
#? Class_OS
#?#########################################################################



    def GetOS(self):
        try:
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer le Nom, le Type, la Version
            query = self._MaBDD.SelectRow(db, f"SELECT Name, Type, Version FROM OS WHERE Name LIKE 'test' AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_21AddNewOS(self): 
        try :
            # Instanciation de l'objet MonOS
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Ajout d'un nouvel OS  dans la table OS
            MonOS.AddNewOS("test", "test", "test")
            # Récupération de ce qu'on vient d'insérer en base
            GetOS = self.GetOS()
            # Vérification que tout c'est bien inséré
            self.assertEqual(GetOS,  [('test', 'test', 'test')])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_22GetOSIDLinux(self):
        try:
            # Instanciation de l'objet MonOS
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'IDOS de Linux
            GetOSIDLinux = MonOS.GetOSIDLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible)
            # Vérification que l'IDOS est bien celui de Linux
            self.assertEqual(GetOSIDLinux, 2)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_23GetOSIDWindows(self):
        try :
            # Instanciation de l'objet MonOS
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'IDOS de Windows
            GetOSIDWindows = MonOS.GetOSIDWindows(self.IPWindows)
            # Vérification que l'IDOS est bien celui de Windows
            self.assertEqual(GetOSIDWindows, 3)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_24GetOSInfo(self):
        try :
            # Instanciation de l'objet MonOS
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération des information de l'OS Linux
            GetOSInfo_Linux = MonOS.GetOSInfo(self.IPLinuxCentOS)
            # Vérification que les informations sont correcte
            self.assertEqual(GetOSInfo_Linux, [('7', 'CentOS Linux')])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_25GetOSName(self):
        try :
            # Instanciation de l'objet MonOS
            MonOS = Class_OS(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du Nom de l'OS Windows
            GetOSNameWindows = MonOS.GetOSName(3)
            # Récupération du Nom de l'OS Linux
            GetOSNameLinux = MonOS.GetOSName(2)
            # Vérification du nom de l'OS Windows
            self.assertEqual(GetOSNameWindows, "Windows Server 2019 Standard")
            # Vérification du nom de l'OS Linux
            self.assertEqual(GetOSNameLinux, "CentOS Linux")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_PoolIP
#?#########################################################################



    def GetPingablePoolIP(self, IPServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer Pingable dans la table PoolIP
            query = self._MaBDD.SelectRow(db, f"SELECT Pingable From PoolIP WHERE IP LIKE '{IPServer}' AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetTopAnsiblePoolIP(self, IPServer):
        try:
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer TopAnsible dans la table PoolIP
            query = self._MaBDD.SelectRow(db, f"SELECT TopAnsible From PoolIP WHERE IP LIKE '{IPServer}' AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetIsUsedPoolIP(self, IPServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer IsUsed dans la table PoolIP
            query = self._MaBDD.SelectRow(db, f"SELECT IsUsed From PoolIP WHERE IP LIKE '{IPServer}' AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def CountIPPoolIP(self):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va compter le nombre d'IP dans PoolIP
            query = self._MaBDD.SelectRow(db, f"SELECT COUNT(IP) FROM PoolIP WHERE Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_26GetPoolIPID(self):
        try :
            # Instanciation de l'objet MonPoolIP
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            # Récupération du PoolIP ID pour l'IP Windows
            GetPoolIPIDWindows = MonPoolIP.GetPoolIPID(self.IPWindows)
            # Récupération du PoolIP ID pour l'IP Linux
            GetPoolIPIDLinux = MonPoolIP.GetPoolIPID(self.IPLinuxCentOS)
            # Vérification de l'ID de PoolIP pour la machine Windows
            self.assertEqual(GetPoolIPIDWindows, 3)
            # Vérification de l'ID de PoolIP pour la machine Linux
            self.assertEqual(GetPoolIPIDLinux, 2)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_27GetPoolIpList(self): 
        try :
            # Instanciation de l'objet MonPoolIP
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            # Récupération de la list des IPs dans PoolIP
            ListIP = MonPoolIP.GetPoolIpList()
            LenListIP = len(ListIP)
            # Récupération du nombre d'IP présente dans la table PoolIP
            TotalIP = self.CountIPPoolIP()
            # Vérification qu'il y est le bon nombre d'IP
            self.assertEqual(TotalIP[0][0], LenListIP)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_28UpdatePingable(self):
        try :
            # Instanciation de l'objet MonPoolIP
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            # Update de la colonne Pingable dans PoolIP pour l'IP Windows
            MonPoolIP.UpdatePingable(self.IPWindows)
            # On récupère la valeur de Pingable dans la table PoolIP pour l'IP Windows
            GetPingablePoolIP = self.GetPingablePoolIP(self.IPWindows)
            # Vérification que l'Update c'est bien passé
            self.assertEqual(GetPingablePoolIP, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_29UpdateTopAnsible(self):
        try:
            # Instanciation de l'objet MonPoolIP
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            # Update de la colonne TopAnsible dans PoolIP pour l'IP Windows
            MonPoolIP.UpdateTopAnsible(self.IPWindows)
            # On récupère la valeur de TopAnsible dans la table PoolIP pour l'IP Windows
            GetTopAnsiblePoolIP = self.GetTopAnsiblePoolIP(self.IPWindows)
            # Vérification que l'Update c'est bien passé
            self.assertEqual(GetTopAnsiblePoolIP, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_30UpdateIsUsed(self):
        try :
            # Instanciation de l'objet MonPoolIP
            MonPoolIP = Class_PoolIP(self._MyObjLog, self._MaBDD)
            # Update de la colonne IsUsed dans PoolIP pour l'IP Windows
            MonPoolIP.UpdateIsUsed(self.IPWindows)
            # On récupère la valeur de IsUsed dans la table PoolIP pour l'IP Windows
            GetIsUsedPoolIP = self.GetIsUsedPoolIP(self.IPWindows)
            # Vérification que l'Update c'est bien passé
            self.assertEqual(GetIsUsedPoolIP, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_ServerApps
#?#########################################################################



    def GetServerApptest(self, IDServer, IDApplication):
        try:
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va nous dire si un Serveur possède une application
            query = self._MaBDD.SelectRow(db, f"SELECT COUNT(IDServer) FROM ServerApps WHERE IDServer = {IDServer} AND IDApplication = {IDApplication} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteServerApptest(self, IDServer, IDApplication):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va supprimer une ligne lié a un Serveur dans ServerApps
            query = self._MaBDD.UpdateRow(db, f"DELETE FROM ServerApps WHERE IDServer = {IDServer} AND IDApplication = {IDApplication} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def InsertServerApp(self, IDServer, IDApplication):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va insérer une ligne dans ServerApps
            query = self._MaBDD.InsertRow(db, f"INSERT INTO ServerApps (IDServer, IDApplication, Deleted) VALUES ({IDServer}, {IDApplication}, 0)")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_31InsertServerApp(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServApp = Class_ServerApps(self._MyObjLog, self._MaBDD)
            # Insertion d'une ligne dans la table ServerApps IDServer = 3, IDApp = 2
            MonServApp.InsertServerApp(3, 2)
            # Récupération de si une ligne contient bien ces informations
            GetServerApptest = self.GetServerApptest(3, 2)
            # Vérifications qu'il y ait bien une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServerApptest, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_32DeleteServerApp(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServApp = Class_ServerApps(self._MyObjLog, self._MaBDD)
            # Suppression de la ligne ou l'IDServer vaut 3
            MonServApp.DeleteServerApp(3)
            # Récupération de si une ligne contient ces informations
            GetServerApptest = self.GetServerApptest(3, 2)
            # Vérifications qu'il n'y ait pas une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServerApptest, [(0,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_33DeleteAllAppForServerInServerApp(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServApp = Class_ServerApps(self._MyObjLog, self._MaBDD)
            # Suppression de toutes les lignes dans ServeurApps lié a l'IDServer
            MonServApp.DeleteAllAppForServerInServerApp(4)
            # Récupération de si une ligne contient ces informations
            GetServerApptest = self.GetServerApptest(4, 2)
            # Vérifications qu'il n'y ait pas une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServerApptest, [(0,)])
            # Récupération de si une ligne contient ces informations
            GetServerApptest = self.GetServerApptest(4, 3)
            # Vérifications qu'il n'y ait pas une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServerApptest, [(0,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_34IDServerAlreadyExistInServerApps(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServApp = Class_ServerApps(self._MyObjLog, self._MaBDD)
            # Vérification de si l'IDServer est déjà présent dans la table
            IDServerAlreadyExistInServerApps_Windows = MonServApp.IDServerAlreadyExistInServerApps(2)
            IDServerAlreadyExistInServerApps_Linux = MonServApp.IDServerAlreadyExistInServerApps(1)
            # Vérification que l'IDServer d'une machine Linux et Windows sont présent dans la table 
            self.assertEqual(IDServerAlreadyExistInServerApps_Windows, 1)
            self.assertEqual(IDServerAlreadyExistInServerApps_Linux, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



# # #?#########################################################################
# # #? Class_ServerGroup
# # #?#########################################################################



    def GetServeGrouptest(self, IDServer, IdGroup):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va nous dire si un Serveur possède un Groupe
            query = self._MaBDD.SelectRow(db, f"SELECT COUNT(IDServer) FROM ServerGroup WHERE IDServer = {IDServer} AND IdGroup = {IdGroup} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteServerGrouptest(self, IDServer, IdGroup):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va supprimer une ligne lié a un Serveur dans ServerGroup
            query = self._MaBDD.UpdateRow(db, f"DELETE FROM ServerGroup WHERE IDServer = {IDServer} AND IdGroup = {IdGroup} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def InsertServerGroup(self, IDServer, IdGroup):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va insérer une ligne dans ServerGroup
            query = self._MaBDD.InsertRow(db, f"INSERT INTO ServerGroup (IDServer, IdGroup, Deleted) VALUES ({IDServer}, {IdGroup}, 0)")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_35InsertServerGroup(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            # Insertion d'une ligne dans la table ServerGroup IDServer = 3, GroupID = 2
            MonServGroup.InsertServerGroup(3, 2)
            # Récupération de si une ligne contient bien ces informations
            GetServeGrouptest = self.GetServeGrouptest(3, 2)
            # Vérifications qu'il y ait bien une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServeGrouptest, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_36UpdateServerGroup(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            # Update du Groupe grace a l'ID du Serveur
            MonServGroup.UpdateServerGroup(3, 3)
            # Récupération de si une ligne contient bien ces informations
            GetServeGrouptest = self.GetServeGrouptest(3, 3)
            # Vérifications qu'il y ait bien une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServeGrouptest, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_37DeleteServerGroup(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            # Suppression de la ligne ou l'IDServer vaut 3
            MonServGroup.DeleteServerGroup(3)
            # Récupération de si une ligne contient ces informations
            GetServeGrouptest = self.GetServeGrouptest(3, 3)
            # Vérifications qu'il n'y ait pas une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServeGrouptest, [(0,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_38IDServerAlreadyExistInServerGroup(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            # Vérification de si l'IDServer est déjà présent dans la table
            IDServerAlreadyExistInServerGroup_Windows = MonServGroup.IDServerAlreadyExistInServerGroup(2)
            IDServerAlreadyExistInServerGroup_Linux = MonServGroup.IDServerAlreadyExistInServerGroup(1)
            # Vérification que l'IDServer d'une machine Linux et Windows sont présent dans la table 
            self.assertEqual(IDServerAlreadyExistInServerGroup_Windows, 1)
            self.assertEqual(IDServerAlreadyExistInServerGroup_Linux, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_39DeleteAllGroupForServerInServerGroup(self):
        try :
            # Instanciation de l'objet MonServApp
            MonServGroup = Class_ServerGroup(self._MyObjLog, self._MaBDD)
            # Suppression de toutes les lignes dans ServerGroup lié a l'IDServer
            MonServGroup.DeleteAllGroupForServerInServerGroup(4)
            # Récupération de si une ligne contient ces informations
            GetServeGrouptest = self.GetServeGrouptest(4, 3)
            # Vérifications qu'il n'y ait pas une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServeGrouptest, [(0,)])
            # Récupération de si une ligne contient ces informations
            GetServeGrouptest = self.GetServeGrouptest(4, 4)
            # Vérifications qu'il n'y ait pas une ligne correspondant a ce qu'on a inséré
            self.assertEqual(GetServeGrouptest, [(0,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



#?#########################################################################
#? Class_Servers
#?#########################################################################



    def GetInfoServer(self, Hostname):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer IDHypervisor, IDOS, Hostname, Commonname, UserAnsible, Deleted dans la table Server
            query = self._MaBDD.SelectRow(db, f"SELECT IDHypervisor, IDOS, Hostname, Commonname, UserAnsible, Deleted FROM Servers WHERE Hostname = '{Hostname}' AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetInfoServerPassword(self, Hostname):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer PassAnsible, OldPassansible dans la table Servers
            query = self._MaBDD.SelectRow(db, f"SELECT PassAnsible, OldPassansible FROM Servers WHERE Hostname = '{Hostname}' AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetServerDeleted(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer Deleted dans la table Servers
            query = self._MaBDD.SelectRow(db, f"SELECT Deleted FROM Servers WHERE ID = {IDServer} AND Deleted = 1")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def UpdateDeleted(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va Update la table Servers et mettre Deleted a 0 a un certains IDServer
            query = self._MaBDD.UpdateRow(db, f"UPDATE Servers SET Deleted = '0' WHERE ID = {IDServer} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def InsertServer(self):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va Insérer ID = 7, IDHypervisor = 7, IDOS = 7, Commonname = 'tomtom', Hostname = 'tomtom', Deleted = 0 dans la table Server
            query = self._MaBDD.InsertRow(db, f"INSERT INTO Servers (ID, IDHypervisor, IDOS, Commonname, Hostname, Deleted) VALUES (7, 7 , 7, 'tomtom', 'tomtom', 0)")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def DeleteServer(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va Supprimer une ligne dans la table Servers lié a un IDServer
            query = self._MaBDD.UpdateRow(db, f"DELETE FROM Servers WHERE ID = {IDServer} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def GetAllForAServerWithDeleted1(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va tout Récupérer d'une ligne de la table Servers lié a un IDServer
            query = self._MaBDD.SelectRow(db, f"SELECT COUNT(*) FROM Servers INNER JOIN IpServer ON Servers.ID = IpServer.IDServer INNER JOIN ServerGroup ON IpServer.IDServer = ServerGroup.IDServer INNER JOIN ServerApps ON ServerGroup.IDServer = ServerApps.IDServer WHERE Servers.ID = {IDServer} and Servers.Deleted = 1 AND IpServer.Deleted = 1 AND ServerGroup.Deleted = 1 AND ServerApps.Deleted = 1")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def RemoveUserWindows(self, IPServer, User) :
        try:
            # Attribution de l'IP a l'Objet de connexion Windows (WinRM)
            self._MonWinRM.IP = IPServer
            # Commande permettant de Supprimer un Utilisateur Windows
            self._MonWinRM.Run_WinRM_PS_Session(f'Remove-LocalUser -Name "{User}"')
            # Vérification que la commande c'est bien passé
            if (self._MonWinRM.ExecutionCommandSucess):
                self._MyObjLog.AjouteLog(f"OK - L'utilisateur Ansible2 a bien été supprimé sur windows", self.TopExit, True)
            else:
                self._MyObjLog.AjouteLog(f"Erreur lors de la suppresion de Ansible2 sur windows", self.TopExit, True)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_40GetInfosServerWindows(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération des information du Server Windows
            MonServeur.GetInfosServerWindows(self.IPWindows)
            # Vérification des informations récupéré
            self.assertEqual(MonServeur.get_hostname(), "TEST-PVE")
            self.assertEqual(MonServeur.get_commonname(), "TEST-PVE")
            self.assertEqual(MonServeur.get_idhyperviseur(), 1)
            self.assertEqual(MonServeur.get_idos() , 3)
            self.assertEqual(MonServeur.get_Type(), "windows")
            self.assertEqual(self.UserAnsible, "ansible")
            self.assertEqual(self.PassAnsible, Class_Ansible_Security.Decrypt_Password(self, "XXXXXX", Class_Ansible_Security.GetSalt(self)))
            self.assertEqual(MonServeur.get_deleted(), 0)
            try :
                # Ici on va remettre l'utilisateur ansible par défault car dans la fonction GetInfosServerWindows l'utilisateur ansible devient Service_Local_XXXX
                # Attribution des login de Service_Local_XXXX a l'objet de connexion _MonWinRM
                self._MonWinRM.set_useransible(MonServeur.get_NewUserAnsible())
                self._MonWinRM.set_passansible(MonServeur.get_NewPassAnsible())
                # Instanciation de l'objet MonAnsibleSecurity
                MonAnsibleSecurity = Class_Ansible_Security(self._MyObjLog, self._MonWinRM, self._MaBDD)
                TempUser1 = "Ansible2"
                # Création compte ansible + droit admin
                MonAnsibleSecurity.SetupAnsible2(self.IPWindows, self.PassAnsible)
                # On rename l'utilisateur Ansible2 en ansible
                MonAnsibleSecurity.ChangeUserWindows(self.IPWindows, TempUser1, self.UserAnsible)
                # On se remet en profil de connexion par défaut ansible
                MonAnsibleSecurity._MonWinRM.set_useransible(self.UserAnsible)
                MonAnsibleSecurity._MonWinRM.set_passansible(self.PassAnsible)
                # Suppression Service_Local_XXXX
                self.RemoveUserWindows(self.IPWindows, MonServeur.get_NewUserAnsible())
            except (Exception) as err :
                self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
                raise
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_41GetInfosServerLinux(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération des information du Server Linux
            MonServeur.GetInfosServerLinux(self.IPLinuxCentOS)
            # Vérification des informations récupéré
            self.assertEqual(MonServeur.get_hostname(), "machinetomtest")
            self.assertEqual(MonServeur.get_commonname(), "machinetomtest")
            self.assertEqual(MonServeur.get_idhyperviseur(), 1)
            self.assertEqual(MonServeur.get_idos() , 2)
            self.assertEqual(MonServeur.get_Type(), "linux")
            self.assertEqual(self.UserAnsible, "ansible")
            self.assertEqual(self.PassAnsible, Class_Ansible_Security.Decrypt_Password(self, "XXXXXX", Class_Ansible_Security.GetSalt(self)))
            self.assertEqual(MonServeur.get_deleted(), 0)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_42InsertServerBDD(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Insertion d'un Server
            MonServeur.InsertServerBDD("TEST-PVE", "TEST-PVE", 1, 3, "ansible", "q9!lw#OX#lF.jG@w", 0, "185.190.91.32")
            # Récupération des informations du Server que l'on vient d'insérer
            GetInfoServer = self.GetInfoServer("TEST-PVE")
            # Vérification que les informations que l'on a inséré sont correcte
            self.assertEqual(GetInfoServer, [(1, 3, 'TEST-PVE', 'TEST-PVE', 'ansible', 0)])

            # On re-insère le Server afin de Simuler un Update du Server en changeant l'IDHypevisor 1 -> 2
            MonServeur.InsertServerBDD("TEST-PVE", "TEST-PVE", 2, 3, "ansible", "q9!lw#OX#lF.jG@w", 0, "185.190.91.32")
            # Récupération des informations du Server que l'on vient d'update
            GetInfoServer = self.GetInfoServer("TEST-PVE")
            # Vérification que les informations que l'on a inséré sont correcte
            self.assertEqual(GetInfoServer, [(2, 3, 'TEST-PVE', 'TEST-PVE', 'ansible', 0)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_43GetServeurID(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On récupère l'ID du Server Windows et Linux et on vérifie qu'ils soient correcte 
            self.assertEqual(MonServeur.GetServeurID(self.IPWindows), 6)
            self.assertEqual(MonServeur.GetServeurID(self.IPLinuxCentOS), 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_44DeleteServer(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On Update le champs Deleted dans Server qui a pour ID 1
            MonServeur.DeleteServer(3)
            # Récupération du Server qui a pour ID 1 et Deleted a 1
            GetServerDeleted = self.GetServerDeleted(3)
            # Vérfication qu'il y en ait un
            self.assertEqual(GetServerDeleted, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_45GetLastIDServer(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du dernier ID inséré dans la table Servers et Vérification de ce dernier
            self.assertEqual(MonServeur.GetLastIDServer(), 6)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_46GetIdServerWithHostname(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération de l'ID du Server grâce au hostname et vérification des informations récupérées
            self.assertEqual(MonServeur.GetIdServerWithHostname("TEST-PVE"), 6)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_47GetIDServerWithIP(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On remet Deleted a 0 pour le Server a l'ID 1
            self.UpdateDeleted(1)
            # On récupère l'IDServer d'une machine Linux et Windows grâce a leur IP et vérification des informations récupérées
            self.assertEqual(MonServeur.GetIDServerWithIP(self.IPLinuxCentOS), 1)
            self.assertEqual(MonServeur.GetIDServerWithIP(self.IPWindows), 6)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_48GetHostnameWithIDServer(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On récupère le Hostname et vérification des informations récupérées
            self.assertEqual(MonServeur.GetHostnameWithIDServer(6), "TEST-PVE")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_49DeleteAllForServerByServerID(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On met Deleted a 1 dans toutes les tables où les lignes sont liées a L'IDServer 
            MonServeur.DeleteAllForServerByServerID(5)
            # Récupération des informations d'un Server ayant pour ID 5 et Deleted a 1 de partout
            GetAllForAServerWithDeleted1 = self.GetAllForAServerWithDeleted1(5)
            # Vérfication qu'il y en ait un
            self.assertEqual(GetAllForAServerWithDeleted1, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_50GetServerPassword(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Déchirffrement du password
            decrypt = Class_Ansible_Security.Decrypt_Password(self, MonServeur.GetServerPassword(1), Class_Ansible_Security.GetSalt(self))
            # Vérification du résultat obtenu
            self.assertEqual(decrypt, "q9!lw#OX#lF.jG@w")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_51GetServerLogin(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du login
            GetServerLogin = MonServeur.GetServerLogin(1)
            # Vérification du résultat obtenu
            self.assertEqual(GetServerLogin, "ansible")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_52GetPassAnsibleUserAnsibleIDServerByIPServer(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du login et password et de l'IDServer grâce a L'IP
            GetPassAnsibleUserAnsibleIDServerByIPServer = MonServeur.GetPassAnsibleUserAnsibleIDServerByIPServer(self.IPLinuxCentOS)
            # Vérification du résultat obtenu
            self.assertEqual(GetPassAnsibleUserAnsibleIDServerByIPServer[0], 1)
            self.assertEqual(GetPassAnsibleUserAnsibleIDServerByIPServer[1], "ansible")
            self.assertEqual(Class_Ansible_Security.Decrypt_Password(self, GetPassAnsibleUserAnsibleIDServerByIPServer[2], Class_Ansible_Security.GetSalt(self)), "XXXXXX")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_53UpdateUserAnsibleAndPasswordAnsible(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Insertion d'un Server
            self.InsertServer()
            # On Update les champs du Server que l'on vient d'insérer
            MonServeur.UpdateUserAnsibleAndPasswordAnsible("tomtom", "tomtom", 7)
            # On récupère les informations du Server que l'on vient de modifier
            GetInfoServerPassword = self.GetInfoServerPassword("tomtom")
            # Vérification du résultat obtenu
            self.assertEqual(GetInfoServerPassword, [('tomtom', 'tomtom')])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    # def test_GetOldPassAnsible(self): #* ON LE FAIT DEJA DANS test_DecryptAllPassword
    #     MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
    #     GetOldPassAnsible = MonServeur.GetOldPassAnsible(1)
    #     self.assert(GetOldPassAnsible, 2)

    def test_54GetServerTypeWithIDServer(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du type de machine des, machines Linux et Windows grâce a leur IDServer
            GetServerTypeWithIDServer_Windows = MonServeur.GetServerTypeWithIDServer(2)
            GetServerTypeWithIDServer_Linux = MonServeur.GetServerTypeWithIDServer(1)
            # Vérification du résultat obtenu
            self.assertEqual(GetServerTypeWithIDServer_Windows, "windows")
            self.assertEqual(GetServerTypeWithIDServer_Linux, "linux")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_55GetServerListWherePasswordNeedUpdate(self):
        try :
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On récupère la liste des IP des Servers qui ont besoin d'Update leur password
            GetServerListWherePasswordNeedUpdate = MonServeur.GetServerListWherePasswordNeedUpdate(1)
            # Vérification du résultat obtenu
            self.assertEqual(GetServerListWherePasswordNeedUpdate, [('192.168.200.29',)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    # def test_GetAllIpAddressForOneMachine(self): #? A VOIR COMMENT TRAITER CE CAS ET ADAPTER LA FCT POUR LINUX FCT PAS ENCORE UTILISE DE BASE DANS LE SCRIPT
    #     MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
    #     GetAllIpAddressForOneMachine_Windows = MonServeur.GetAllIpAddressForOneMachine(self.IPWindows)
    #     GetAllIpAddressForOneMachine_Linux = MonServeur.GetAllIpAddressForOneMachine(self.IPLinuxCentOS)
    #     self.assertEqual(GetAllIpAddressForOneMachine_Windows, ['10.10.50.60', '10.10.0.61', '185.190.91.32'])

    # def test_GetServerListWithTopAnsible(self): #? POUR QUE CE TEST MARCHE IL FAUDRAIT UNE BASE QU'AVEC LES 2 SEVEURS
    #     MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
    #     GetServerListWithTopAnsible = MonServeur.GetServerListWithTopAnsible()
    #     self.assertEqual(GetServerListWithTopAnsible, ['192.168.200.29', '185.190.91.32'])

    # def test_GetAllPasswordForAnIP(self): #* ON LE FAIT DEJA DANS test_DecryptAllPassword
    #     MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
    #     GetAllPasswordForAnIP_Windows = MonServeur.GetAllPasswordForAnIP(self.IPWindows)
    #     self.assertEqual(GetAllPasswordForAnIP_Windows, [])

    def test_56DecryptAllPassword(self): 
        try : 
            # Instanciation de l'objet MonServeur
            MonServeur = Class_Servers(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # On déchiffre tous les mots de passes présent dans la liste
            DecryptAllPassword = MonServeur.DecryptAllPassword(self.IPLinuxCentOS)
            # Vérification du résultat obtenu
            self.assertEqual(DecryptAllPassword, ['q9!lw#OX#lF.jG@w', 'q9!lw#OX#lF.jG@w'])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



# # #?#########################################################################
# # #? Class_Tools
# # #?#########################################################################



    def test_57HostnameExist(self):
        try :
            # Instanciation de l'objet MonTools
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Vérification que les hostname existent en base
            HostnameExist_Windows = MonTools.HostnameExist("TEST-PVE")
            HostnameExist_Test = MonTools.HostnameExist("toto")
            # Vérification du résultat obtenu
            self.assertEqual(HostnameExist_Windows, 1)
            self.assertEqual(HostnameExist_Test, None)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_58GetHostnameWindows(self):
        try :
            # Instanciation de l'objet MonTools
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du Hostname Windows
            GetHostnameWindows = MonTools.GetHostnameWindows(self.IPWindows)
            # Vérification du résultat obtenu
            self.assertEqual(GetHostnameWindows, "TEST-PVE")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_59GetHostnameLinux(self):
        try :
            # Instanciation de l'objet MonTools
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du Hostname Linux
            GetHostnameLinux = MonTools.GetHostnameLinux(self.IPLinuxCentOS, self.UserAnsible, self.PassAnsible)
            # Vérification du résultat obtenu
            self.assertEqual(GetHostnameLinux, "machinetomtest")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_60Get_Name_VLAN(self):
        try :
            # Instanciation de l'objet MonTools
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Récupération du VLAN Windows
            Get_Name_VLAN_Windows = MonTools.Get_Name_VLAN(self.IPWindows)
            # Vérification du résultat obtenu
            self.assertEqual(Get_Name_VLAN_Windows, "VLAN 1001 : 185.190.91.0/24")
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_61IsHostnameANDIPAlreadyExist(self):
        try :
            # Instanciation de l'objet MonTools
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Vérification en base si L'IP et le Hostname existent 
            IsHostnameANDIPAlreadyExist = MonTools.IsHostnameANDIPAlreadyExist("TEST-PVE", self.IPWindows)
            # Vérification du résultat obtenu
            self.assertEqual(IsHostnameANDIPAlreadyExist, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_62IpAlreadyAffectedToServer(self):
        try :
            # Instanciation de l'objet MonTools
            MonTools = Class_Tools(self._MyObjLog, self._MonWinRM, self._MaBDD)
            # Vérification en base si l'IP est déjà affectée
            IpAlreadyAffectedToServer = MonTools.IpAlreadyAffectedToServer(self.IPWindows)
            # Vérification du résultat obtenu
            self.assertEqual(IpAlreadyAffectedToServer, 1)
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



# #?#########################################################################
# #? Class_App
# #?#########################################################################



    def GetAppForServer(self, IDServer):
        try :
            # Connection a la base de données
            db = self._MaBDD.mysqlconnector()
            # Requête qui va récupérer IDApp
            query = self._MaBDD.SelectRow(db, f"SELECT IDApplication FROM ServerApps WHERE IDServer = {IDServer} AND Deleted = 0")
            return query
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_63AffectApplicationsToServerForWindows(self):
        try :
            # Instanciation de l'objet MonApp
            MonApp = Class_App(self._MyObjLog, self._MonWinRM, self._MaBDD, self._MonServer)
            # Affectation des Applications a un Server Windows
            MonApp.AffectApplicationsToServerForWindows(self.IPWindows)
            # Récupération des Application lié au Server Windows
            AppList = self.GetAppForServer(2)
            # Vérification du résultat obtenu
            self.assertEqual(AppList, [(2,), (10,), (11,), (12,), (13,), (14,), (18,), (20,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_64AffectApplicationsToServerForLinux(self): 
        try :
            # Instanciation de l'objet MonApp
            MonApp = Class_App(self._MyObjLog, self._MonWinRM, self._MaBDD, self._MonServer)
            # Affectation des Applications a un Server Linux
            MonApp.AffectApplicationsToServerForLinux(self.IPLinuxCentOS)
            # Récupération des Application lié au Server Linux
            AppList = self.GetAppForServer(1)
            # Vérification du résultat obtenu
            self.assertEqual(AppList, [(1,)])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise

    def test_65GetIDANDApplicationList(self):
        try :
            # Instanciation de l'objet MonApp
            MonApp = Class_App(self._MyObjLog, self._MonWinRM, self._MaBDD, self._MonServer)
            # Récupération des ID et des Applications sous forme de liste
            GetIDANDApplicationList = MonApp.GetIDANDApplicationList()
            # Vérification du résultat obtenu
            self.assertEqual(GetIDANDApplicationList, [(1, 'ssh'),(2, 'ftp'),(3, 'rdp'),(4, 'iis'),(5, 'WEBDEV'),(6, 'Hyper File Server : *'),(7, 'apache'),(8, 'mysql'),(9, 'sql server'),(10, 'ftpsvc'),(11, 'Zabbix Agent'),(12, 'W3SVC'),(13, 'WinRM'),(14, 'IPBAN'),(15, 'MDaemon'),(16, 'VMTools'),(17, 'MSSQL$*'),(18, 'FileZilla Server'),(20, 'nxlog'),(21, 'chocolatey')])
        except (Exception) as err :
            self._MyObjLog.AjouteLog(f"NOT OK Exception in {__file__} - Class:{sys._getframe().f_code.co_name} -  Erreur = {err}" , self.TopExit, True)
            raise



    if __name__ == '__main__':
        unittest.main()
